#!/usr/bin/env python3
"""
Daily US swing-trade screener.

Does the number-heavy steps of the US swing prompt with code: liquidity, trend,
relative strength vs SPY, RSI, setup detection, overextension, ATR band, stop,
target, R:R after costs and position size. It also applies the exclusions that
free files can answer: price floor, recent IPOs, listing exchange, ETFs / test
issues, partnerships / warrants / units / preferreds (by security name), Nasdaq
deficiency / delinquency / bankruptcy status, the Nasdaq Reg SHO threshold list,
reverse splits, wild gaps, and (for the top-ranked stocks only) fund type,
short interest and the next earnings date from Yahoo.

Universe: S&P 500, S&P MidCap 400, S&P SmallCap 600 and the Russell Microcap,
taken from the daily holdings files of the iShares ETFs that track them
(IVV, IJH, IJR, IWC), with Wikipedia and a saved copy as fallbacks.

Output: output/latest.json and latest.md (plus output/history/). A Claude
task reads them before the US open and does the judgment steps: market context,
fundamentals, news and events.

The indicator maths and setup rules are the same as in the Indian scanner.
Every download fails soft: a check whose data can't be fetched is marked
"unverified" for Claude instead of being guessed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import math
import re
import sys
import time
import traceback
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import yaml


ROOT = Path(__file__).resolve().parent
ET = ZoneInfo("America/New_York")
IST = ZoneInfo("Asia/Kolkata")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
SCHEMA_VERSION = 1
SPY = "SPY"
INDEX_ETFS = ["SPY", "QQQ", "IWM"]
VOL_TICKERS = ["^VIX", "^VIX3M"]
SECTOR_ETFS = {
    "XLK": "Technology", "XLF": "Financials", "XLV": "Health Care", "XLE": "Energy",
    "XLI": "Industrials", "XLY": "Consumer Discretionary", "XLP": "Consumer Staples",
    "XLU": "Utilities", "XLB": "Materials", "XLRE": "Real Estate", "XLC": "Communication Services",
    "SMH": "Semiconductors", "IGV": "Software", "XBI": "Biotech", "KRE": "Regional Banks",
    "ITA": "Aerospace & Defense", "XHB": "Homebuilders",
}
MACRO = {"^TNX": "US 10-year yield %", "DX-Y.NYB": "US Dollar Index", "CL=F": "WTI crude $",
         "GC=F": "Gold $", "INR=X": "USD-INR"}
SESSION_DONE = dt.time(16, 15)           # ET; daily bars are final after this
ALLOWED_EXCHANGES = {"Nasdaq", "NYSE", "NYSE American"}
OTHER_EXCHANGE_CODES = {"N": "NYSE", "A": "NYSE American", "P": "NYSE Arca",
                        "Z": "Cboe BZX", "V": "IEX"}
NASDAQ_STATUS = {"D": "deficient", "E": "delinquent", "Q": "bankrupt",
                 "G": "deficient and bankrupt", "H": "deficient and delinquent",
                 "J": "delinquent and bankrupt", "K": "deficient, delinquent and bankrupt"}
# security-name patterns for things the prompt excludes (K-1 partnerships, warrants, units...)
NAME_EXCLUDE = re.compile(
    r"\b(?:warrants?|units?|rights|preferred (?:stock|shares?|securities)|exchange[- ]traded|etn|"
    r"limited partnership|lp|acquisition corp(?:oration)?)\b|\bL\.\s?P\.", re.I)
CHINA = {"China", "Hong Kong", "Macau", "Macao"}

STEPS = [
    "enough price history",
    "price floor",
    "listing checks",
    "no reverse split / wild gaps",
    "liquidity",
    "primary uptrend (50 EMA, 200)",
    "20 EMA",
    "3M relative strength vs SPY > 0",
    "RSI 40-75",
    "named setup",
    "not overextended",
    "ATR band",
    "stop within limit",
    "target & R:R after costs",
    "position size",
    "short interest / fund type",
]
PROFILE_STEP = len(STEPS) - 1            # applied after ranking, to the top stocks only


# --------------------------------------------------------------------------
# shared indicator maths and setup rules (same code as the Indian scanner)
# --------------------------------------------------------------------------
def r2(x):
    """Round for output; keep None/NaN as None so JSON stays valid."""
    if x is None:
        return None
    try:
        if isinstance(x, (float, np.floating)) and (math.isnan(x) or math.isinf(x)):
            return None
        return round(float(x), 2)
    except (TypeError, ValueError):
        return x


def http_get(client, url: str, tries: int = 3, pause: float = 1.5):
    last = "no response"
    for i in range(tries):
        try:
            r = client.get(url)
            if r.status_code == 200 and r.content:
                return r
            last = f"HTTP {r.status_code}"
        except Exception as e:  # network errors, timeouts
            last = f"{type(e).__name__}: {e}"
        time.sleep(pause * (i + 1))
    raise RuntimeError(f"{url} -> {last}")


def _wilder(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    c, h, l = df["close"], df["high"], df["low"]
    out = pd.DataFrame(index=df.index)
    out["ema20"] = c.ewm(span=20, adjust=False).mean()
    out["ema50"] = c.ewm(span=50, adjust=False).mean()
    out["ema200"] = c.ewm(span=200, adjust=False).mean()
    out["sma200"] = c.rolling(200).mean()

    delta = c.diff()
    avg_gain = _wilder(delta.clip(lower=0), 14)
    avg_loss = _wilder(-delta.clip(upper=0), 14)
    rsi = 100 - 100 / (1 + avg_gain / avg_loss)
    out["rsi"] = rsi.where(avg_loss != 0, 100.0)

    prev_close = c.shift()
    tr = pd.concat([h - l, (h - prev_close).abs(), (l - prev_close).abs()], axis=1).max(axis=1)
    atr = _wilder(tr, 14)
    out["atr"] = atr

    up, down = h.diff(), -l.diff()
    plus_dm = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=df.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=df.index)
    plus_di = 100 * _wilder(plus_dm, 14) / atr
    minus_di = 100 * _wilder(minus_dm, 14) / atr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    out["adx"] = _wilder(dx, 14)

    macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
    out["macd"] = macd
    out["macd_signal"] = macd.ewm(span=9, adjust=False).mean()
    out["macd_hist"] = out["macd"] - out["macd_signal"]
    return out


def pivot_highs(high: pd.Series, left: int = 5, right: int = 5) -> list[float]:
    h = high.to_numpy()
    return [h[i] for i in range(left, len(h) - right)
            if h[i] == h[i - left:i + right + 1].max()]


def detect_setups(df: pd.DataFrame, ind: pd.DataFrame, vol_x: float):
    """Return ([(name, family, entry_trigger or None)], volume_ratio). Ordered by preference."""
    c, o, h, l, v = (df[k] for k in ("close", "open", "high", "low", "volume"))
    C, O, H, L = c.iloc[-1], o.iloc[-1], h.iloc[-1], l.iloc[-1]
    atr, ema20 = ind["atr"].iloc[-1], ind["ema20"]
    vol20 = v.iloc[-21:-1].mean()
    vr = v.iloc[-1] / vol20 if vol20 > 0 else float("nan")
    hi20, lo20 = h.iloc[-21:-1].max(), l.iloc[-21:-1].min()
    hi252 = h.iloc[-253:-1].max()
    atr_pct = atr / C * 100
    found = []

    if C > hi252 and vr >= vol_x:
        found.append(("52-week high breakout", "breakout", None))
    base_range_pct = (hi20 / lo20 - 1) * 100 if lo20 > 0 else float("inf")
    if C > hi20 and vr >= vol_x and base_range_pct <= 7 * atr_pct:
        found.append(("Base breakout on volume", "breakout", None))

    if len(c) >= 30:
        # flag box = the 5 sessions before today; pole = the 20 sessions before the box
        pole = c.iloc[-7] / c.iloc[-27] - 1
        fh, fl = h.iloc[-6:-1].max(), l.iloc[-6:-1].min()
        box = max(fh, H) - min(fl, L)
        if pole >= 0.08 and box <= 2.5 * atr and C <= fh and C >= 0.95 * hi20:
            found.append(("Bull flag / tight consolidation", "consolidation", fh * 1.002))

    touched = bool((l.iloc[-3:] <= ema20.iloc[-3:] * 1.01).any())
    rising = ema20.iloc[-1] > ema20.iloc[-6]
    body, rng = abs(C - O), H - L
    lower_wick = min(C, O) - L
    bullish = (C > O and C > c.iloc[-2]) or (rng > 0 and lower_wick >= 2 * body and (C - L) / rng >= 0.6)
    if touched and rising and bullish and C >= ema20.iloc[-1] * 0.98:
        found.append(("Pullback to 20 EMA", "pullback", None))

    near_res = C >= 0.95 * hi20
    if H < h.iloc[-2] and L > l.iloc[-2] and near_res:
        found.append(("Inside bar near resistance", "consolidation", H * 1.002))
    ranges = (h - l).iloc[-7:]
    if ranges.iloc[-1] <= ranges.min() and near_res:
        found.append(("NR7 near resistance", "consolidation", H * 1.002))
    # a buy-above trigger only counts if it is within 1 ATR of today's close
    found = [s for s in found if s[2] is None or (s[2] - C) <= atr]
    return found, vr


def clean_record(rec: dict) -> dict:
    out = {}
    for k, v in rec.items():
        if isinstance(v, (float, np.floating)):
            out[k] = r2(v)
        elif isinstance(v, (np.integer,)):
            out[k] = int(v)
        elif isinstance(v, (np.bool_,)):
            out[k] = bool(v)
        else:
            out[k] = v
    return out


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def load_config(path: Path | None = None) -> dict:
    with open(path or ROOT / "us_config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def log(msg: str) -> None:
    print(f"[{dt.datetime.now(IST):%H:%M:%S} IST] {msg}", flush=True)


def http_client():
    import httpx
    return httpx.Client(http2=True, timeout=30.0, follow_redirects=True,
                        headers={"User-Agent": UA, "Accept": "*/*",
                                 "Accept-Language": "en-US,en;q=0.9"})


def yahoo_symbol(sym: str) -> str:
    """Exchange / index style (BRK.B, BRK/B) -> Yahoo style (BRK-B)."""
    return re.sub(r"[./ ]", "-", str(sym).strip().upper())


def last_complete_session(now_et: dt.datetime) -> dt.date:
    """Most recent weekday whose regular session has finished (holidays are caught later)."""
    d = now_et.date()
    if d.weekday() < 5 and now_et.time() >= SESSION_DONE:
        return d
    d -= dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


def trading_days_between(start: dt.date, end: dt.date) -> int:
    """Weekdays after `start` up to and including `end` (US holidays not removed)."""
    return int(np.busday_count(start + dt.timedelta(days=1), end + dt.timedelta(days=1)))


def floor_qty(q: float, fractional: bool) -> float:
    if not q or q <= 0 or math.isnan(q):
        return 0.0
    return math.floor(q * 100) / 100 if fractional else float(math.floor(q))


# --------------------------------------------------------------------------
# parsers
# --------------------------------------------------------------------------
def parse_ishares_holdings(text: str):
    """iShares holdings CSV -> ([{symbol, name, sector}], as_of). Keeps equities only."""
    lines = text.lstrip("﻿").splitlines()
    start = next((i for i, ln in enumerate(lines)
                  if ln.strip().strip('"').lower().startswith("ticker")), None)
    if start is None:
        raise ValueError("no 'Ticker' header row in holdings file")
    as_of = None
    for ln in lines[:start]:
        if "as of" in ln.lower():
            parts = next(csv.reader([ln]))
            as_of = parts[1].strip() if len(parts) > 1 else None
    rows = list(csv.reader(lines[start:]))
    header = [h.strip().lower() for h in rows[0]]
    col = {h: i for i, h in enumerate(header)}
    ti, ai = col.get("ticker"), col.get("asset class")
    ni, si = col.get("name"), col.get("sector")
    out, seen = [], set()
    for r in rows[1:]:
        if len(r) < max(2, len(header) - 3):
            continue                                  # disclaimer / trailer lines
        t = r[ti].strip().upper()
        if ai is not None and r[ai].strip().lower() != "equity":
            continue
        if not re.fullmatch(r"[A-Z][A-Z0-9./ ]{0,9}", t) or t in seen:
            continue
        seen.add(t)
        out.append({"symbol": t.replace(" ", "."),
                    "name": r[ni].strip() if ni is not None else "",
                    "sector": r[si].strip() if si is not None else ""})
    return out, as_of


def parse_wikipedia_constituents(html: str):
    tables = []
    try:
        tables = pd.read_html(io.StringIO(html), attrs={"id": "constituents"})
    except Exception:
        pass
    if not tables:
        tables = pd.read_html(io.StringIO(html))
    best = None
    for t in tables:
        if isinstance(t.columns, pd.MultiIndex):
            t.columns = [" ".join(map(str, c)) for c in t.columns]
        sc = next((c for c in t.columns if re.search(r"symbol|ticker", str(c), re.I)), None)
        if sc is not None and (best is None or len(t) > len(best[0])):
            best = (t, sc)
    if best is None:
        raise ValueError("no table with a Symbol column")
    t, sc = best
    nc = next((c for c in t.columns if re.search(r"security|company", str(c), re.I)), None)
    gc = next((c for c in t.columns if re.search(r"sector", str(c), re.I)), None)
    out = []
    for _, row in t.iterrows():
        s = str(row[sc]).strip().upper()
        if re.fullmatch(r"[A-Z][A-Z0-9./]{0,9}", s):
            out.append({"symbol": s, "name": str(row[nc]) if nc is not None else "",
                        "sector": str(row[gc]) if gc is not None else ""})
    return out


def parse_nasdaq_listed(text: str) -> dict:
    out = {}
    rows = [ln.split("|") for ln in text.splitlines() if "|" in ln]
    if not rows:
        return out
    header = [h.strip() for h in rows[0]]
    for p in rows[1:]:
        rec = dict(zip(header, (x.strip() for x in p)))
        sym = rec.get("Symbol", "")
        if not sym or sym.startswith("File Creation Time"):
            continue
        out[yahoo_symbol(sym)] = {
            "exchange": "Nasdaq", "name": rec.get("Security Name", ""),
            "etf": rec.get("ETF") == "Y", "test": rec.get("Test Issue") == "Y",
            "financial_status": rec.get("Financial Status") or None}
    return out


def parse_other_listed(text: str) -> dict:
    out = {}
    rows = [ln.split("|") for ln in text.splitlines() if "|" in ln]
    if not rows:
        return out
    header = [h.strip() for h in rows[0]]
    for p in rows[1:]:
        rec = dict(zip(header, (x.strip() for x in p)))
        sym = rec.get("ACT Symbol", "")
        if not sym or sym.startswith("File Creation Time"):
            continue
        code = rec.get("Exchange", "")
        out[yahoo_symbol(sym)] = {
            "exchange": OTHER_EXCHANGE_CODES.get(code, f"other ({code})"),
            "name": rec.get("Security Name", ""),
            "etf": rec.get("ETF") == "Y", "test": rec.get("Test Issue") == "Y",
            "financial_status": None}
    return out


def parse_regsho(text: str) -> set[str]:
    syms = set()
    for ln in text.splitlines():
        if "|" not in ln:
            continue
        s = ln.split("|")[0].strip().upper()
        if s and s != "SYMBOL" and re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,9}", s):
            syms.add(yahoo_symbol(s))
    return syms


def resolve_symbol(sym: str, listing: dict | None, stripped: dict) -> str:
    """iShares drops the share-class dot (BRKB); find the real listing symbol (BRK-B)."""
    y = yahoo_symbol(sym)
    if not listing or y in listing:
        return y
    return stripped.get(y.replace("-", ""), y)


def stripped_index(listing: dict | None) -> dict:
    if not listing:
        return {}
    return {k.replace("-", ""): k for k in listing if re.fullmatch(r"[A-Z]+-[A-Z]", k)}


# --------------------------------------------------------------------------
# data loading (network)
# --------------------------------------------------------------------------
def load_listing(client):
    """Nasdaq Trader symbol directory: exchange, ETF flag, test issue, Nasdaq financial status."""
    listing, status = {}, {}
    for name, url, parser in [
        ("nasdaqlisted", "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt", parse_nasdaq_listed),
        ("otherlisted", "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt", parse_other_listed),
    ]:
        try:
            part = parser(http_get(client, url, tries=2).text)
            if len(part) < 1000:
                raise ValueError(f"only {len(part)} symbols")
            listing.update(part)
            status[name] = f"ok ({len(part)} symbols)"
        except Exception as e:
            status[name] = f"FAILED: {str(e)[:140]}"
    if not all(v.startswith("ok") for v in status.values()):
        return None, status                       # partial directory would cause false rejects
    return listing, status


def fetch_regsho(client, data_date: dt.date):
    """Nasdaq Reg SHO threshold list for data_date (or the latest of the 3 sessions before)."""
    d, errs = data_date, []
    for _ in range(4):
        url = f"https://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{d:%Y%m%d}.txt"
        try:
            return parse_regsho(http_get(client, url, tries=2).text), f"ok (file {d})"
        except Exception as e:
            errs.append(f"{d}: {str(e)[:80]}")
        d -= dt.timedelta(days=1)
        while d.weekday() >= 5:
            d -= dt.timedelta(days=1)
    return None, "FAILED: " + "; ".join(errs[:2])


def load_us_constituents(cfg: dict, client, listing: dict | None, refresh: bool = True):
    """Download each index list (iShares holdings, then Wikipedia); fall back to the saved copy.
    Each stock is kept only in the largest index it belongs to."""
    cdir = ROOT / "data" / "constituents"
    cdir.mkdir(parents=True, exist_ok=True)
    stripped = stripped_index(listing)
    lists, status = {}, {}
    for key, cat in cfg["categories"].items():
        path = cdir / f"{key.lower()}.csv"
        rows, how, errs = None, None, []
        if refresh and client is not None:
            sources = [("iShares holdings", cat.get("holdings_url"), "ishares"),
                       ("Wikipedia", cat.get("wikipedia_url"), "wiki")]
            for label, url, kind in sources:
                if not url:
                    continue
                try:
                    text = http_get(client, url, tries=2).text
                    if kind == "ishares":
                        got, as_of = parse_ishares_holdings(text)
                    else:
                        got, as_of = parse_wikipedia_constituents(text), None
                    if len(got) < cat.get("min_size", 1):
                        raise ValueError(f"only {len(got)} stocks")
                    rows, how = got, label + (f" as of {as_of}" if as_of else "")
                    break
                except Exception as e:
                    errs.append(f"{label}: {str(e)[:120]}")
        if rows is not None:
            for r in rows:
                r["symbol"] = resolve_symbol(r["symbol"], listing, stripped)
            pd.DataFrame(rows, columns=["symbol", "name", "sector"]).to_csv(path, index=False)
            lists[key], status[key] = rows, f"downloaded ({how}, {len(rows)} stocks)"
        elif path.exists():
            saved = pd.read_csv(path, dtype=str).fillna("")
            lists[key] = saved.to_dict("records")
            status[key] = "saved copy" + (f" (download failed: {'; '.join(errs)})" if errs else "")
        else:
            lists[key], status[key] = [], f"MISSING (download failed: {'; '.join(errs)})"
    out, taken = {}, set()
    for key in cfg["categories"]:                 # config order = largest index first
        uniq = []
        for r in lists[key]:
            s = r["symbol"]
            if s and s not in taken:
                taken.add(s)
                uniq.append(s)
        out[key] = uniq
    names = {r["symbol"]: r for rows in lists.values() for r in rows}
    return out, names, status


def _frame_us(data: pd.DataFrame, ticker: str) -> pd.DataFrame | None:
    """One ticker's OHLCV (+ stock splits if present) out of a yfinance download."""
    if data is None or data.empty:
        return None
    cols = data.columns
    if isinstance(cols, pd.MultiIndex):
        if ticker in cols.get_level_values(0):
            df = data[ticker]
        elif ticker in cols.get_level_values(1):
            df = data.xs(ticker, axis=1, level=1)
        else:
            return None
    else:
        df = data
    df = df.rename(columns=lambda c: str(c).strip().lower())
    need = ["open", "high", "low", "close", "volume"]
    if not all(c in df.columns for c in need):
        return None
    keep = need + (["stock splits"] if "stock splits" in df.columns else [])
    df = df[keep].apply(pd.to_numeric, errors="coerce").dropna(subset=["close", "high", "low"])
    if df.empty:
        return None
    idx = pd.to_datetime(df.index)
    if getattr(idx, "tz", None) is not None:
        idx = idx.tz_convert(ET).tz_localize(None)
    df.index = idx.normalize()
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df["volume"] = df["volume"].fillna(0)
    if "stock splits" in df.columns:
        df["stock splits"] = df["stock splits"].fillna(0)
    return df.astype(float)


def fetch_prices(tickers: list[str], period: str, chunk: int = 50, pause: float = 2.0,
                 second_pass_cap: int = 120):
    """Daily OHLCV + split events from Yahoo, in batches with retries. Prices are
    split-adjusted, not dividend-adjusted, so the last close matches the market."""
    import yfinance as yf

    def download(batch):
        for attempt in range(3):
            try:
                return yf.download(batch, period=period, interval="1d", group_by="ticker",
                                   auto_adjust=False, actions=True, threads=True,
                                   progress=False)
            except Exception as e:
                log(f"  yahoo batch error ({type(e).__name__}); retry {attempt + 1}")
                time.sleep(10 * (attempt + 1))
        return None

    frames: dict[str, pd.DataFrame] = {}
    for i in range(0, len(tickers), chunk):
        batch = tickers[i:i + chunk]
        data = download(batch)
        for t in batch:
            df = _frame_us(data, t)
            if df is not None and len(df) > 0:
                frames[t] = df
        log(f"  prices: {min(i + chunk, len(tickers))}/{len(tickers)} requested, {len(frames)} received")
        time.sleep(pause)
    for t in [t for t in tickers if t not in frames][:second_pass_cap]:
        time.sleep(1.0)
        df = _frame_us(download([t]), t)
        if df is not None and len(df) > 0:
            frames[t] = df
    return frames


def _to_date(x):
    if x is None:
        return None
    try:
        if isinstance(x, (int, float)):
            return dt.datetime.fromtimestamp(x, tz=ET)
        ts = pd.Timestamp(x)
        return None if pd.isna(ts) else ts
    except Exception:
        return None


def fetch_profile(ticker: str) -> dict:
    """Yahoo quote profile for one stock: fund type, short interest, ownership, a few
    fundamentals and earnings dates. Missing fields stay None (= unverified)."""
    import yfinance as yf
    t = yf.Ticker(ticker)
    prof: dict = {"ok": False}
    try:
        info = t.info or {}
    except Exception as e:
        info = {}
        prof["error"] = f"{type(e).__name__}: {str(e)[:100]}"
    if info:
        prof["ok"] = True
    g = info.get
    prof.update(
        name=g("longName") or g("shortName"), quote_type=g("quoteType"), exchange=g("exchange"),
        country=g("country"), sector=g("sector"), industry=g("industry"),
        market_cap=g("marketCap"), float_shares=g("floatShares"),
        inst_pct=(g("heldPercentInstitutions") * 100 if g("heldPercentInstitutions") is not None else None),
        short_pct_float=(g("shortPercentOfFloat") * 100 if g("shortPercentOfFloat") is not None else None),
        days_to_cover=g("shortRatio"), ttm_eps=g("trailingEps"))
    debt, cash, ebitda = g("totalDebt"), g("totalCash"), g("ebitda")
    prof["net_debt_to_ebitda"] = ((debt - (cash or 0)) / ebitda
                                  if debt is not None and ebitda and ebitda > 0 else None)
    stamps = []
    for k in ("earningsTimestamp", "earningsTimestampStart", "earningsTimestampEnd"):
        ts = _to_date(g(k))
        if ts is not None:
            stamps.append(ts)
    try:
        cal = t.calendar or {}
        for d in (cal.get("Earnings Date") or []):
            ts = _to_date(d)
            if ts is not None:
                stamps.append(ts)
    except Exception:
        pass
    prof["earnings_stamps"] = stamps
    return prof


# --------------------------------------------------------------------------
# setups (US-only addition to the shared rules)
# --------------------------------------------------------------------------
def detect_gap_continuation(df: pd.DataFrame, lookback: int = 10, min_gap: float = 0.04,
                            vol_x: float = 2.0):
    """A gap-up of >= 4% on >= 2x average volume in the last 10 sessions that has held
    above the gap day's low ever since. Returns (name, family, trigger, details) or None."""
    o, h, l, c, v = (df[k].to_numpy() for k in ("open", "high", "low", "close", "volume"))
    n = len(df)
    for i in range(n - 1, max(n - 1 - lookback, 21), -1):     # most recent gap first
        gap = o[i] / c[i - 1] - 1
        vavg = v[i - 20:i].mean()
        if gap >= min_gap and vavg > 0 and v[i] >= vol_x * vavg:
            held = c[-1] >= l[i] and (i == n - 1 or l[i + 1:].min() >= l[i])
            if not held:
                return None
            return ("Gap continuation (gap held)", "gap", None,
                    {"gap_date": str(df.index[i].date()), "gap_pct": r2(gap * 100),
                     "gap_volume_x": r2(v[i] / vavg)})
    return None


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------
def capital_settings(cfg: dict, usd_inr: float | None) -> dict:
    rate, src = (usd_inr, "Yahoo INR=X") if usd_inr else (cfg["fallback_usd_inr"], "fallback in us_config.yaml")
    cap = float(cfg["capital_usd"]) if cfg.get("capital_usd") else cfg["capital_inr"] / rate
    return {"capital_usd": cap, "usd_inr": rate, "usd_inr_source": src,
            "capital_basis": "fixed capital_usd" if cfg.get("capital_usd") else f"₹{cfg['capital_inr']:,} ÷ {rate:.2f}",
            "risk_usd": cap * cfg["risk_pct"] / 100,
            "max_position_usd": cap * cfg["max_position_pct"] / 100}


def evaluate(sym: str, df: pd.DataFrame, cat: dict, cfg: dict, ctx: dict) -> dict:
    """Run hard filters 1-15 in order. Returns a record with steps_passed and either the
    trade plan (passed=True) or the first failed step and why. Step 16 (Yahoo profile)
    is applied later, to the top-ranked stocks only."""
    rec = {"symbol": sym, "passed": False, "steps_passed": 0, "flags": [], "unverified": []}

    def fail(detail):
        rec["failed_step"], rec["fail_detail"] = STEPS[rec["steps_passed"]], detail
        return rec

    def ok():
        rec["steps_passed"] += 1

    # 1 history (also excludes IPOs from the last 6 months)
    if df is None or len(df) < cfg["min_history_bars"]:
        return fail(f"only {0 if df is None else len(df)} daily bars (recent IPO or no data)")
    if df.index[-1].date() != ctx["data_date"]:
        return fail(f"last bar {df.index[-1].date()} (no trade on {ctx['data_date']})")
    ind = compute_indicators(df)
    last = ind.iloc[-1]
    if last[["ema20", "ema50", "ema200", "rsi", "atr", "adx", "macd"]].isna().any():
        return fail("indicators incomplete")
    ok()

    c = df["close"]
    C = float(c.iloc[-1])
    rec["last_close"] = C

    # 2 price floor
    if C < cfg["min_price"]:
        return fail(f"price ${C:.2f} < ${cfg['min_price']}")
    ok()

    # 3 listing checks
    listing = ctx.get("listing")
    if listing is None:
        rec["unverified"].append("listing status (exchange / ETF / deficiency)")
    else:
        li = listing.get(sym)
        if li is None:
            rec["unverified"].append("listing status (symbol not in exchange directory)")
        else:
            rec["exchange"] = li["exchange"]
            if li["exchange"] not in ALLOWED_EXCHANGES:
                return fail(f"listed on {li['exchange']}")
            if li["etf"] or li["test"]:
                return fail("ETF / test issue")
            m = NAME_EXCLUDE.search(li["name"] or "")
            if m:
                return fail(f"security name has '{m.group(0)}' ({li['name'][:60]})")
            fs = li.get("financial_status")
            if fs and fs != "N":
                return fail(f"Nasdaq financial status: {NASDAQ_STATUS.get(fs, fs)}")
    regsho = ctx.get("regsho")
    if regsho is None:
        rec["unverified"].append("Reg SHO threshold list")
    elif sym in regsho:
        return fail("on Nasdaq Reg SHO threshold list")
    ok()

    # 4 reverse split in last 12 months / more than one ±15% gap in last 10 sessions
    if "stock splits" in df.columns:
        sp = df["stock splits"].iloc[-252:]
        rev = sp[(sp > 0) & (sp < 1)]
        if len(rev):
            return fail(f"reverse split on {rev.index[-1].date()}")
    else:
        rec["unverified"].append("reverse split (last 12 months)")
    gaps = (df["open"] / c.shift() - 1).abs().iloc[-10:]
    if int((gaps >= 0.15).sum()) > 1:
        return fail(f"{int((gaps >= 0.15).sum())} gaps of ±15% in last 10 sessions")
    ok()

    # 5 liquidity
    adv = float((c * df["volume"]).iloc[-20:].mean())
    avg_sh = float(df["volume"].iloc[-20:].mean())
    rec["adv_usd_m"], rec["avg_volume_shares"] = adv / 1e6, avg_sh
    if adv < cat["min_adv_usd_m"] * 1e6:
        return fail(f"20-day avg dollar volume ${adv / 1e6:.1f}M < ${cat['min_adv_usd_m']}M")
    if avg_sh < cat.get("min_avg_shares", 0):
        return fail(f"20-day avg volume {avg_sh:,.0f} shares < {cat['min_avg_shares']:,}")
    ok()

    e20, e50, e200, s200 = (float(last[k]) for k in ("ema20", "ema50", "ema200", "sma200"))
    # 6 primary uptrend
    if not (C > e50 and (e50 > e200 or (not math.isnan(s200) and C > 1.05 * s200))):
        return fail(f"close {C:.2f} / 50 EMA {e50:.2f} / 200 EMA {e200:.2f}")
    ok()

    setups, vol_ratio = detect_setups(df, ind, cat["breakout_volume_x"])
    gap = detect_gap_continuation(df)
    if gap:
        n_brk = sum(1 for s in setups if s[1] == "breakout")
        setups = setups[:n_brk] + [gap[:3]] + setups[n_brk:]
        rec["gap"] = gap[3]
    rec["volume_ratio"] = vol_ratio
    primary = setups[0] if setups else None
    family = primary[1] if primary else None

    # 7 20 EMA (pullbacks may sit up to 2% below it)
    if not (C > e20 or (family == "pullback" and C >= 0.98 * e20)):
        return fail(f"close {(C / e20 - 1) * 100:.1f}% vs 20 EMA")
    ok()

    # 8 relative strength vs SPY
    def rel(bench, n):
        b = bench.reindex(df.index).ffill()
        return float(((c.iloc[-1] / c.iloc[-1 - n]) / (b.iloc[-1] / b.iloc[-1 - n]) - 1) * 100)
    spy = ctx["spy_close"]
    rs1, rs3 = rel(spy, 21), rel(spy, 63)
    rec["rs_1m_pct"], rec["rs_3m_pct"] = rs1, rs3
    if not rs3 > 0:
        return fail(f"3-month RS vs SPY {rs3:.1f}%")
    ok()

    # 9 RSI
    rsi = float(last["rsi"])
    rec["rsi"] = rsi
    if not 40 <= rsi <= 75:
        return fail(f"RSI {rsi:.1f}")
    ok()

    # 10 setup
    if not primary:
        return fail("no breakout / gap / flag / pullback / inside bar / NR7 detected")
    rec["setup"], rec["setup_family"] = primary[0], family
    rec["other_setups"] = [s[0] for s in setups[1:]]
    ok()

    # 11 overextension
    ext = (C / e20 - 1) * 100
    ret5 = (C / float(c.iloc[-6]) - 1) * 100
    rec["pct_above_ema20"], rec["ret_5d_pct"] = ext, ret5
    if ext > 10 or ret5 > 15:
        return fail(f"{ext:.1f}% above 20 EMA, {ret5:.1f}% in 5 sessions")
    ok()

    # 12 ATR band
    atr = float(last["atr"])
    atr_pct = atr / C * 100
    rec["atr_pct"] = atr_pct
    lo, hi = cat["atr_pct"]
    if not lo <= atr_pct <= hi:
        return fail(f"ATR {atr_pct:.2f}% outside {lo}-{hi}%")
    ok()

    # 13 entry & stop (cents)
    entry = round(float(primary[2]) if primary[2] else C, 2)
    swing_low = float(df["low"].iloc[-5:].min())
    stop_swing = swing_low - 0.1 * atr
    d = entry - stop_swing
    if d < 1.0 * atr:
        stop, stop_basis = entry - atr, "1× ATR"
    elif d <= 2.0 * atr:
        stop, stop_basis = stop_swing, "below 5-day swing low"
    else:
        stop, stop_basis = entry - 1.5 * atr, "1.5× ATR"
    stop = round(stop, 2)
    risk = entry - stop
    risk_pct = risk / entry * 100
    rec.update(entry=entry, stop=stop, stop_basis=stop_basis, risk_pct=risk_pct,
               entry_type="BS" if primary[2] else "LMT",
               entry_note=("buy-stop just above today's high" if primary[2]
                           else "limit at last close"))
    if risk <= 0 or risk_pct > cfg["max_stop_pct"]:
        return fail(f"stop {risk_pct:.1f}% below entry > {cfg['max_stop_pct']}%")
    ok()

    # 14 target & R:R after costs
    h = df["high"]
    hi252 = float(h.iloc[-253:-1].max())
    levels = [p for p in pivot_highs(h.iloc[-253:-5]) if p > entry * 1.01]
    if hi252 > entry * 1.01:
        levels.append(hi252)
    cap = entry * (1 + cfg["max_target_pct"] / 100)
    cost = entry * cfg["round_trip_cost_pct"] / 100
    if levels:
        res = min(levels)
        target, target_basis = min(res * 0.995, cap), f"just below resistance {res:.2f}"
    else:
        res = None
        floor_t = entry * (1 + cat["min_target_pct"] / 100)
        target = min(max(entry + 2.5 * (risk + cost) + cost, floor_t), cap)
        target_basis = "no overhead resistance (2.5R after costs, at least the minimum move)"
    target = round(target, 2)
    target_pct = (target / entry - 1) * 100
    rr = (target - entry) / risk
    rr_net = (target - entry - cost) / (risk + cost)
    rec.update(target=target, target_basis=target_basis, target_pct=target_pct, rr=rr,
               rr_after_costs=rr_net, nearest_resistance=res)
    if target_pct < cat["min_target_pct"]:
        return fail(f"target only {target_pct:.1f}% away (resistance too close)")
    if rr_net < cfg["min_rr"]:
        return fail(f"R:R after costs {rr_net:.2f} < {cfg['min_rr']}")
    ok()

    # 15 position size
    capx = ctx["capital"]
    qty = floor_qty(min(capx["risk_usd"] / risk, capx["max_position_usd"] / entry),
                    cfg.get("fractional_shares", True))
    pos = qty * entry
    rec.update(qty=qty, position_value=pos, risk_amount=qty * risk)
    if qty <= 0:
        return fail("quantity rounds to 0")
    if pos > adv * cfg["max_pct_of_adv"] / 100:
        return fail(f"position ${pos:,.0f} > {cfg['max_pct_of_adv']}% of daily dollar volume")
    ok()

    # ---- passed filters 1-15: score for ranking (never rejects) ----
    adx, adx_prev = float(last["adx"]), float(ind["adx"].iloc[-4])
    macd, sig = float(last["macd"]), float(last["macd_signal"])
    hist, hist_prev = float(last["macd_hist"]), float(ind["macd_hist"].iloc[-2])
    rsi_prev = float(ind["rsi"].iloc[-2])
    score, why = 0.0, []
    if rs1 > 0:
        score += 1.5; why.append("1M RS+")
    cat_etf = ctx["category_etf_close"].get(cat.get("category_etf") or "")
    if cat_etf is not None:
        rs_cat = rel(cat_etf, 21)
        rec["rs_1m_vs_category_pct"] = rs_cat
        if rs_cat > 0:
            score += 0.5; why.append(f"beats {cat['category_etf']} 1M")
    if family in ("breakout", "gap"):
        if 55 <= rsi <= 75:
            score += 1; why.append("RSI fits breakout")
        if macd > sig:
            score += 1; why.append("MACD>signal")
        if family == "breakout" and adx >= 20 and adx > adx_prev:
            score += 1; why.append("ADX≥20 rising")
        if family == "gap":
            score += 1; why.append("gap held")
        if not math.isnan(vol_ratio):
            score += min(max(vol_ratio - 1, 0), 1.5); why.append(f"vol {vol_ratio:.1f}x")
    elif family == "pullback":
        if 40 <= rsi <= 60 and rsi > rsi_prev:
            score += 1; why.append("RSI turning up")
        if macd > 0:
            score += 1; why.append("MACD>0")
        if adx >= 20:
            score += 0.5; why.append("trend ADX≥20")
    else:  # consolidation
        if macd >= -0.1 * atr:
            score += 1; why.append("MACD near/above 0")
        if hist > hist_prev:
            score += 1; why.append("MACD hist rising")
    if rr_net >= 2.5:
        score += 1; why.append(f"R:R {rr_net:.1f}")
    if stop_basis.startswith("below"):
        score += 0.5; why.append("stop under swing low")
    if C >= 0.95 * hi252:
        score += 0.5; why.append("near 52W high")
    rec.update(passed=True, score=round(score, 2), score_notes=why, adx=adx,
               macd_above_signal=bool(macd > sig))
    return rec


def apply_profile(rec: dict, prof: dict | None, cat: dict, cfg: dict, data_date: dt.date) -> dict:
    """Step 16 + earnings handling for one stock that passed steps 1-15."""
    if not prof or not prof.get("ok"):
        rec["unverified"] += ["short interest", "fund type", "earnings date"]
        rec["steps_passed"] = len(STEPS)
        return rec
    keep = ("name", "quote_type", "country", "sector", "industry", "market_cap", "float_shares", "inst_pct",
            "short_pct_float", "days_to_cover", "ttm_eps", "net_debt_to_ebitda")
    rec["profile"] = {k: (r2(prof.get(k)) if isinstance(prof.get(k), float) else prof.get(k))
                      for k in keep}
    qt = prof.get("quote_type")
    if qt and qt.upper() != "EQUITY":
        rec.update(passed=False, failed_step=STEPS[PROFILE_STEP], fail_detail=f"Yahoo type {qt}")
        return rec
    si, dtc = prof.get("short_pct_float"), prof.get("days_to_cover")
    if si is None and dtc is None:
        rec["unverified"].append("short interest")
    if si is not None and si > cfg["max_short_pct_float"]:
        rec.update(passed=False, failed_step=STEPS[PROFILE_STEP],
                   fail_detail=f"short interest {si:.1f}% of float")
        return rec
    if dtc is not None and dtc > cfg["max_days_to_cover"]:
        rec.update(passed=False, failed_step=STEPS[PROFILE_STEP],
                   fail_detail=f"{dtc:.1f} days to cover")
        return rec
    rec["steps_passed"] = len(STEPS)

    score, why = rec["score"], rec["score_notes"]
    if prof.get("country") in CHINA:
        rec["flags"].append("⚠ China-based")
        rec["unverified"].append("VIE structure")
    ind = (prof.get("industry") or "").lower()
    if cat.get("flag_binary_events") and "biotech" in ind:
        rec["unverified"].append("FDA / trial date in window")
    fl = prof.get("float_shares")
    if fl is not None and fl >= 10e6:
        score += 0.25; why.append("float ≥10M")
    ip = prof.get("inst_pct")
    if ip is not None and ip >= 20:
        score += 0.25; why.append("inst ≥20%")

    # earnings: next date inside the holding window, and whether it already reported
    stamps = prof.get("earnings_stamps") or []
    upcoming, past = [], []
    for ts in stamps:
        d = ts.date() if hasattr(ts, "date") else ts
        hour = getattr(ts, "hour", 0)
        timing = "BMO" if 0 < hour < 12 else ("AMC" if hour >= 15 else None)
        if d > data_date or (d == data_date and timing != "BMO"):
            upcoming.append((d, timing))
        else:
            past.append(d)
    if upcoming:
        d, timing = min(upcoming, key=lambda x: (x[0], x[1] is None))
        k = trading_days_between(data_date, d)
        rec["next_earnings"] = {"date": str(d), "timing": timing, "trading_days_ahead": k}
        if k <= cfg["earnings_window_days"]:
            rec["flags"].append(f"⚠ Earnings on {d}{' ' + timing if timing else ''}")
            if k <= 5:
                rec["qty"] = floor_qty(rec["qty"] / 2, cfg.get("fractional_shares", True))
                rec["position_value"] = rec["qty"] * rec["entry"]
                rec["risk_amount"] = rec["qty"] * (rec["entry"] - rec["stop"])
                rec["qty_note"] = "halved: earnings in first 5 trading days"
                score -= 1; why.append("earnings in first 5 days (−1)")
                if rec["qty"] <= 0:
                    rec.update(passed=False, failed_step=STEPS[PROFILE_STEP],
                               fail_detail="quantity 0 after halving for earnings")
                    return rec
    else:
        rec["unverified"].append("earnings date")
    if past and (data_date - max(past)).days <= 45:
        rec["last_earnings"] = str(max(past))
        score += 0.5; why.append("already reported")
    rec["score"], rec["score_notes"] = round(score, 2), why
    return rec


def trend_block(df: pd.DataFrame) -> dict:
    ind = compute_indicators(df)
    c, last = df["close"], ind.iloc[-1]
    h, l = df["high"], df["low"]
    return {
        "close": r2(c.iloc[-1]),
        "ema20": r2(last["ema20"]), "ema50": r2(last["ema50"]), "ema200": r2(last["ema200"]),
        "above": {k: bool(c.iloc[-1] > last[k]) for k in ("ema20", "ema50", "ema200")},
        "ret_5d_pct": r2((c.iloc[-1] / c.iloc[-6] - 1) * 100),
        "ret_21d_pct": r2((c.iloc[-1] / c.iloc[-22] - 1) * 100),
        "rsi": r2(last["rsi"]),
        "higher_highs_and_lows_20d": bool(h.iloc[-20:].max() > h.iloc[-40:-20].max()
                                          and l.iloc[-20:].min() > l.iloc[-40:-20].min()),
    }


def market_snapshot(mk: dict, breadth: dict) -> dict:
    snap = {"indexes": {t: trend_block(mk[t]) for t in INDEX_ETFS if mk.get(t) is not None
                        and len(mk[t]) > 60},
            "breadth": {k: r2(v) for k, v in breadth.items()}}
    vix, vix3 = mk.get("^VIX"), mk.get("^VIX3M")
    if vix is not None and len(vix) > 6:
        v = {"level": r2(vix["close"].iloc[-1]),
             "change_5d_pct": r2((vix["close"].iloc[-1] / vix["close"].iloc[-6] - 1) * 100)}
        if vix3 is not None and len(vix3):
            v["vix3m"] = r2(vix3["close"].iloc[-1])
            v["term_structure"] = ("contango (calm)" if vix["close"].iloc[-1] < vix3["close"].iloc[-1]
                                   else "backwardation (stress)")
        snap["vix"] = v
    secs = []
    for t, name in SECTOR_ETFS.items():
        df = mk.get(t)
        if df is not None and len(df) > 22:
            c = df["close"]
            secs.append({"etf": t, "name": name, "ret_5d_pct": r2((c.iloc[-1] / c.iloc[-6] - 1) * 100),
                         "ret_21d_pct": r2((c.iloc[-1] / c.iloc[-22] - 1) * 100)})
    snap["sectors_by_1m"] = sorted(secs, key=lambda x: x["ret_21d_pct"] or -999, reverse=True)
    macro = {}
    for t, name in MACRO.items():
        df = mk.get(t)
        if df is not None and len(df) > 6:
            c = df["close"]
            macro[name] = {"last": r2(c.iloc[-1]), "change_5d_pct": r2((c.iloc[-1] / c.iloc[-6] - 1) * 100)}
    snap["macro"] = macro
    return snap


# --------------------------------------------------------------------------
# run
# --------------------------------------------------------------------------
def run(cfg: dict, constituents: dict, prices: dict, mk: dict, listing: dict | None,
        regsho: set | None, checks: dict, today: dt.date, profile_fn=None,
        names: dict | None = None) -> dict:
    spy = mk[SPY]
    data_date = spy.index[-1].date()
    inr = mk.get("INR=X")
    capx = capital_settings(cfg, float(inr["close"].iloc[-1]) if inr is not None and len(inr) else None)
    base = {"schema_version": SCHEMA_VERSION, "market_region": "US",
            "generated_at_ist": dt.datetime.now(IST).strftime("%Y-%m-%d %H:%M"),
            "generated_at_et": dt.datetime.now(ET).strftime("%Y-%m-%d %H:%M"),
            "run_date": str(today), "data_date": str(data_date),
            "settings": {**{k: r2(v) if isinstance(v, float) else v for k, v in capx.items()},
                         **{k: cfg[k] for k in ("risk_pct", "max_position_pct", "fractional_shares",
                                                "round_trip_cost_pct", "max_stop_pct",
                                                "max_target_pct", "min_rr")}},
            "data_checks": checks}
    if data_date != today:
        base.update(status="no_data_today",
                    message=(f"Latest US market data is from {data_date}, not {today}. Either the "
                             "US market was closed or the data had not updated when the scan ran."))
        return base

    ctx = {"data_date": data_date, "spy_close": spy["close"], "listing": listing,
           "regsho": regsho, "capital": capx,
           "category_etf_close": {t: mk[t]["close"] for t in ("IJH", "IJR", "IWC")
                                  if mk.get(t) is not None}}
    breadth_n = {"sp500_50": [0, 0], "sp500_200": [0, 0], "all_50": [0, 0]}
    categories = {}
    for key, cat in cfg["categories"].items():
        syms = constituents.get(key, [])
        recs = []
        for s in syms:
            df = prices.get(s)
            try:
                rec = evaluate(s, df, cat, cfg, ctx)
            except Exception as e:  # never let one bad series kill the scan
                rec = {"symbol": s, "passed": False, "steps_passed": 0, "flags": [], "unverified": [],
                       "failed_step": STEPS[0], "fail_detail": f"error: {e}"}
            recs.append(rec)
            if df is not None and len(df) >= 200 and df.index[-1].date() == data_date:
                c = df["close"]
                a50 = c.iloc[-1] > c.ewm(span=50, adjust=False).mean().iloc[-1]
                a200 = c.iloc[-1] > c.ewm(span=200, adjust=False).mean().iloc[-1]
                breadth_n["all_50"][0] += int(a50); breadth_n["all_50"][1] += 1
                if key == "SP500":
                    breadth_n["sp500_50"][0] += int(a50); breadth_n["sp500_50"][1] += 1
                    breadth_n["sp500_200"][0] += int(a200); breadth_n["sp500_200"][1] += 1

        # step 16 on the best-ranked stocks only (one Yahoo call each)
        ranked = sorted([r for r in recs if r["passed"]],
                        key=lambda r: (r["score"], r.get("rs_3m_pct", 0)), reverse=True)
        checked = 0
        for r in ranked[:cfg["profile_checks_per_category"]]:
            prof = None
            if profile_fn is not None:
                try:
                    prof = profile_fn(r["symbol"])
                except Exception as e:
                    prof = {"ok": False, "error": str(e)[:100]}
                time.sleep(0.4 if profile_fn is fetch_profile else 0)
            apply_profile(r, prof, cat, cfg, data_date)
            checked += 1
        for r in ranked[cfg["profile_checks_per_category"]:]:
            r["steps_passed"] = len(STEPS)                 # not checked; never shown as a pick
            r["profile_checked"] = False
        passed = sorted([r for r in ranked[:checked] if r["passed"]],
                        key=lambda r: (r["score"], r.get("rs_3m_pct", 0)), reverse=True)
        for r in passed:
            r["name"] = ((r.get("profile") or {}).get("name") or
                         ((names or {}).get(r["symbol"]) or {}).get("name") or "")
        n_passed = sum(1 for r in recs if r["passed"])

        funnel = [{"step": "universe", "remaining": len(syms)}]
        for i, name in enumerate(STEPS):
            funnel.append({"step": name, "remaining": sum(1 for r in recs if r["steps_passed"] > i
                                                          and (i < PROFILE_STEP or r["passed"]))})
        closest = None
        if not passed and recs:
            miss = max(recs, key=lambda r: (r["steps_passed"], r.get("rs_3m_pct") or -999))
            closest = {"symbol": miss["symbol"], "failed_step": miss.get("failed_step"),
                       "detail": miss.get("fail_detail"), "steps_passed": miss["steps_passed"]}
        categories[key] = {
            "label": cat["label"], "universe_size": len(syms),
            "passed_all_hard_filters": n_passed,
            "profile_checked": checked,
            "candidates": [clean_record(r) for r in passed[:cfg["candidates_per_category"]]],
            "closest_miss": closest, "funnel": funnel,
        }

    breadth = {"sp500_pct_above_50ema": None, "sp500_pct_above_200ema": None,
               "universe_pct_above_50ema": None}
    for k, out in (("sp500_50", "sp500_pct_above_50ema"), ("sp500_200", "sp500_pct_above_200ema"),
                   ("all_50", "universe_pct_above_50ema")):
        a, n = breadth_n[k]
        breadth[out] = a / n * 100 if n else None
    base.update(status="ok", message="scan complete",
                market=market_snapshot(mk, breadth), categories=categories)
    return base


def to_markdown(rep: dict) -> str:
    L = [f"# US swing scan — {rep.get('data_date')}",
         f"Status: **{rep['status']}** — {rep.get('message', '')}  ",
         f"Generated {rep.get('generated_at_et')} ET / {rep.get('generated_at_ist')} IST", ""]
    st = rep.get("settings") or {}
    if st:
        L += [f"Capital ${st.get('capital_usd')} ({st.get('capital_basis')}), risk ${st.get('risk_usd')}"
              f" per trade, max position ${st.get('max_position_usd')}", ""]
    L += ["## Data checks", "```", json.dumps(rep.get("data_checks", {}), indent=2,
                                               ensure_ascii=False, default=str)[:3000], "```", ""]
    if rep["status"] != "ok":
        return "\n".join(L)
    m = rep["market"]
    L.append("## Market")
    for t, b in m["indexes"].items():
        L.append(f"- {t} {b['close']} | 20/50/200 EMA {b['ema20']} / {b['ema50']} / {b['ema200']} | "
                 f"5d {b['ret_5d_pct']}% | 21d {b['ret_21d_pct']}% | HH/HL {b['higher_highs_and_lows_20d']}")
    v = m.get("vix", {})
    L.append(f"- VIX {v.get('level')} ({v.get('change_5d_pct')}% 5d), VIX3M {v.get('vix3m')}, "
             f"{v.get('term_structure')}")
    br = m["breadth"]
    L.append(f"- Breadth: S&P 500 above 50 EMA {br['sp500_pct_above_50ema']}%, above 200 EMA "
             f"{br['sp500_pct_above_200ema']}%")
    if m.get("sectors_by_1m"):
        L.append("- Sectors 1M: " + ", ".join(f"{s['etf']} {s['ret_21d_pct']}%" for s in m["sectors_by_1m"]))
    L.append("")
    for key, c in rep["categories"].items():
        L.append(f"## {c['label']} — {c['passed_all_hard_filters']} of {c['universe_size']} passed "
                 f"all filters; top {c['profile_checked']} profile-checked, {len(c['candidates'])} shown")
        if c["candidates"]:
            L.append("| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |")
            L.append("|---|---|---|---|---|---|---|---|---|---|")
            for r in c["candidates"]:
                parts = list(r.get("flags", []))
                if r.get("unverified"):
                    parts.append("unverified: " + ", ".join(r["unverified"]))
                L.append(f"| {r['symbol']} | {r['setup']} | {r['last_close']} | {r['entry_type']} "
                         f"{r['entry']} | {r['stop']} | {r['target']} | {r['qty']} | "
                         f"{r['rr_after_costs']} | {r['score']} | {' '.join(parts)} |")
        else:
            cm = c["closest_miss"] or {}
            L.append(f"NO TRADE — closest: {cm.get('symbol')} (failed: {cm.get('failed_step')} — {cm.get('detail')})")
        L.append("Funnel: " + " → ".join(f"{f['step']} {f['remaining']}" for f in c["funnel"]))
        L.append("")
    return "\n".join(L)


def write_outputs(rep: dict, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "history").mkdir(exist_ok=True)
    js = json.dumps(rep, indent=2, ensure_ascii=False, default=str)
    (outdir / "history" / f"{rep.get('run_date')}.json").write_text(js, encoding="utf-8")
    (outdir / "last_run.json").write_text(json.dumps(
        {k: rep.get(k) for k in ("status", "message", "run_date", "data_date",
                                 "generated_at_et", "generated_at_ist")},
        indent=2, ensure_ascii=False), encoding="utf-8")
    latest = outdir / "latest.json"
    if rep.get("status") == "no_data_today" and latest.exists():
        try:
            if json.loads(latest.read_text(encoding="utf-8")).get("status") == "ok":
                return
        except Exception:
            pass
    latest.write_text(js, encoding="utf-8")
    (outdir / "latest.md").write_text(to_markdown(rep), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Daily US swing-trade screener")
    ap.add_argument("--config", type=Path, default=ROOT / "us_config.yaml")
    ap.add_argument("--out", type=Path, default=ROOT / "output")
    ap.add_argument("--asof", help="treat this date (YYYY-MM-DD) as the session to scan")
    ap.add_argument("--no-refresh-lists", action="store_true",
                    help="use the saved index lists instead of downloading them")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    today = (dt.date.fromisoformat(args.asof) if args.asof
             else last_complete_session(dt.datetime.now(ET)))
    checks: dict = {"session_scanned": str(today)}
    try:
        client = http_client()
        log("exchange symbol directory (Nasdaq Trader)")
        listing, checks["listing"] = load_listing(client)
        log("index constituents (iShares holdings)")
        constituents, names, checks["constituents"] = load_us_constituents(
            cfg, client, listing, not args.no_refresh_lists)
        all_syms = sorted({s for v in constituents.values() for s in v})
        if not all_syms:
            raise RuntimeError("no index lists could be downloaded or loaded — " + "; ".join(
                f"{k}: {v}" for k, v in checks["constituents"].items())[:400])

        mk_tickers = INDEX_ETFS + VOL_TICKERS + list(SECTOR_ETFS) + list(MACRO) + ["IJH", "IJR", "IWC"]
        log(f"market data for {len(mk_tickers)} tickers")
        mk = fetch_prices(mk_tickers, cfg["history_period"], chunk=len(mk_tickers), pause=1,
                          second_pass_cap=len(mk_tickers))
        if mk.get(SPY) is None:
            raise RuntimeError("could not download SPY data from Yahoo")
        log(f"prices for {len(all_syms)} stocks")
        prices = fetch_prices(all_syms, cfg["history_period"])
        # keep only finished sessions up to the one being scanned (drops a live intraday bar)
        cut = pd.Timestamp(today)
        mk = {t: d[d.index <= cut] for t, d in mk.items()}
        prices = {s: d[d.index <= cut] for s, d in prices.items()}
        missing = sorted(set(all_syms) - set(prices))
        checks["prices"] = {"source": "Yahoo Finance (yfinance)", "requested": len(all_syms),
                            "received": len(prices), "missing": missing[:60]}
        checks["market_tickers_missing"] = sorted(set(mk_tickers) - set(mk))

        regsho = None
        data_date = mk[SPY].index[-1].date()
        if data_date == today:
            log("Nasdaq Reg SHO threshold list")
            regsho, checks["regsho"] = fetch_regsho(client, data_date)
        rep = run(cfg, constituents, prices, mk, listing, regsho, checks, today,
                  profile_fn=fetch_profile, names=names)
        write_outputs(rep, args.out)
        log(f"done: {rep['status']} — {rep.get('message')}")
        return 0
    except Exception as e:
        rep = {"schema_version": SCHEMA_VERSION, "market_region": "US", "status": "error",
               "generated_at_ist": dt.datetime.now(IST).strftime("%Y-%m-%d %H:%M"),
               "generated_at_et": dt.datetime.now(ET).strftime("%Y-%m-%d %H:%M"),
               "run_date": str(today), "data_date": None,
               "message": f"{type(e).__name__}: {e}", "data_checks": checks,
               "traceback": traceback.format_exc()[-2000:]}
        write_outputs(rep, args.out)
        log(f"FAILED: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
