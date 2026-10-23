# US Swing Scanner — daily US swing-trade shortlist

A free GitHub Actions job screens the S&P 500, S&P MidCap 400, S&P SmallCap 600 and the
Russell Microcap after every US session. A daily Claude task reads the results before the
US open, does the judgment checks (market context, fundamentals, news, events) and sends a
short shortlist.

```
~3:47 AM IST  GitHub Actions ── us_screener.py ──▶ output/latest.json + latest.md
 (after the US close)            (Yahoo Finance candles, iShares IVV/IJH/IJR/IWC holdings,
                                  Nasdaq Trader symbol directory & Reg SHO list, Yahoo profiles)
6:00 PM IST   Claude scheduled task "US Stock Selection" ── reads output/latest.json
 (before the US open)            ── futures, events, fundamentals & news checks ──▶ your shortlist
```

The scan uses the last finished US session's close; the shortlist is a plan for that night's
session. On a US market holiday the run keeps the last good scan instead of overwriting it.

## Files

| File | What it is |
|---|---|
| `us_screener.py` | the scan |
| `us_config.yaml` | capital (₹ converted at the day's USD-INR rate, or a fixed `capital_usd`), risk, costs, thresholds per category — edit this, not the code |
| `requirements.txt` | Python packages the job installs |
| `.github/workflows/us-daily-scan.yml` | runs Mon–Fri at 22:17 UTC, with retries at 23:17 and 03:17 UTC that skip themselves once a scan succeeded |
| `output/` | created by the job: `latest.json` (what Claude reads), `latest.md` (readable), `last_run.json`, `history/` |
| `data/constituents/` | created by the job: saved index lists, used if a download fails |

## Setup

1. Create a **public** repo named `us-swing-scanner` and upload these files, keeping
   `.github/workflows/us-daily-scan.yml` at that path.
2. **Settings → Actions → General → Workflow permissions → Read and write permissions → Save.**
3. **Actions → us-swing-scan → Run workflow.** After it finishes (10–20 min), open `output/latest.md`.
   You can run it any time; during US market hours it scans the last *finished* session.

## What the code checks

- **Exclusions:** price ≥ $5; ≥ 220 sessions of history (so no IPOs from the last 6 months);
  listed on NYSE / Nasdaq / NYSE American; no ETFs or test issues; no partnerships, warrants, units,
  preferreds or SPACs (by security name); Nasdaq deficient / delinquent / bankrupt status; Nasdaq Reg SHO
  threshold list; no reverse split in the last year; no more than one ±15% gap in 10 sessions.
- **Liquidity:** 20-day dollar volume ≥ $50M / $10M / $3M / $1M; ≥ 100k shares a day for small and
  micro caps; position ≤ 1% of dollar volume.
- **Trend and setup:** close > 50 EMA > 200 EMA, close > 20 EMA (pullbacks up to 2% below),
  3-month RS vs SPY > 0, RSI 40–75, a named setup (52-week-high or base breakout on volume, gap
  continuation, bull flag, pullback to 20 EMA, inside bar, NR7), not more than 10% above the 20 EMA or
  15% up in 5 days, ATR within the category band.
- **Trade plan:** stop below the 5-day swing low or 1–1.5× ATR, never more than 5%; target just below the
  nearest resistance, 3% (S&P 500) / 4% minimum, 10% maximum; R:R ≥ 2 after 0.3% round-trip costs;
  quantity = lower of 1%-risk size and 25% of capital, to 0.01 share.
- **Top 8 per category only (Yahoo profile):** fund type, short interest (> 20% of float or > 10 days to
  cover is excluded), next earnings date (quantity halved if earnings fall in the first 5 trading days).

Everything else in the US prompt — fundamentals, news, dilution, VIE structure, biotech catalysts,
NYSE deficiency notices — is checked by Claude on the web, for the shortlisted stocks only.

Entries: `LMT` = limit at the last close (breakouts, pullbacks, gaps); `BS` = buy-stop just above the
last high (inside bar, NR7, flag).

## Things to know

- Free data can fail. Yahoo can throttle ~3,000 tickers; `data_checks` in the output shows how many
  were received, and checks that couldn't be done are marked `unverified` instead of guessed.
- GitHub can pause scheduled workflows in a public repo after 60 days with no activity. The daily
  commits normally prevent that; if runs stop, re-enable the workflow in the Actions tab.
- The logic was tested on generated data (`tests/`). Check `output/latest.md` after the first live runs.

## Run it on your own computer

```
pip install -r requirements.txt
python us_screener.py                     # last finished US session
python us_screener.py --asof 2026-10-22   # re-run a past session
python -m pytest -q tests                 # offline tests
```

Research candidates only, not investment advice.
