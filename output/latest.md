# US swing scan — 2026-10-26
Status: **ok** — scan complete  
Generated 2026-10-26 18:52 ET / 2026-10-27 04:22 IST

Capital $2101.39 (₹200,000 ÷ 95.18), risk $21.01 per trade, max position $525.35

## Data checks
```
{
  "session_scanned": "2026-10-26",
  "listing": {
    "nasdaqlisted": "ok (5625 symbols)",
    "otherlisted": "ok (7673 symbols)"
  },
  "constituents": {
    "SP500": "downloaded (Wikipedia, 503 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "SP400": "downloaded (Wikipedia, 400 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "SP600": "downloaded (Wikipedia, 603 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "MICRO": "downloaded (PROXY: Nasdaq screener, market cap $50M–$300M, price ≥ $5, 451 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']"
  },
  "prices": {
    "source": "Yahoo Finance (yfinance)",
    "requested": 1954,
    "received": 1953,
    "missing": [
      "CWEN-A"
    ]
  },
  "market_tickers_missing": [],
  "regsho": "ok (file 2026-10-26)"
}
```

## Market
- SPY 765.37 | 20/50/200 EMA 768.5 / 765.81 / 731.67 | 5d -0.14% | 21d -0.78% | HH/HL True
- QQQ 712.2 | 20/50/200 EMA 725.69 / 724.84 / 684.16 | 5d -0.86% | 21d -4.34% | HH/HL True
- IWM 276.99 | 20/50/200 EMA 277.65 / 282.99 / 276.66 | 5d 2.1% | 21d -1.77% | HH/HL False
- VIX 18.39 (-0.27% 5d), VIX3M 19.94, contango (calm)
- Breadth: S&P 500 above 50 EMA 61.2%, above 200 EMA 60.6%
- Sectors 1M: XLE 12.25%, XLU 7.69%, XLP 7.19%, IGV 5.07%, XLV 5.03%, XLY 3.35%, XLB 3.17%, XLRE 2.98%, XLF 2.15%, KRE 1.65%, XHB -0.38%, XLI -2.04%, XBI -2.94%, ITA -3.11%, XLK -5.07%, XLC -8.06%, SMH -10.71%

## S&P 500 — 7 of 503 passed all filters; top 7 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| FAST | Pullback to 20 EMA | 52.47 | LMT 52.47 | 50.82 | 57.15 | 10.01 | 2.5 | 5.5 |  |
| A | Bull flag / tight consolidation | 175.96 | BS 179.46 | 172.07 | 197.41 | 2.84 | 2.2 | 4.5 |  |
| AMGN | Bull flag / tight consolidation | 444.63 | BS 451.88 | 436.01 | 496.3 | 1.16 | 2.5 | 4.5 | ⚠ Earnings on 2026-11-03 AMC |
| ABNB | Pullback to 20 EMA | 171.05 | LMT 171.05 | 166.5 | 186.18 | 3.07 | 2.89 | 4.5 | ⚠ Earnings on 2026-11-05 AMC |
| KDP | Bull flag / tight consolidation | 34.99 | BS 35.47 | 34.17 | 39.02 | 14.81 | 2.45 | 4.0 | ⚠ Earnings on 2026-11-03 BMO |
Funnel: universe 503 → enough price history 500 → price floor 500 → listing checks 499 → no reverse split / wild gaps 496 → liquidity 493 → primary uptrend (50 EMA, 200) 206 → 20 EMA 200 → 3M relative strength vs SPY > 0 120 → RSI 40-75 106 → named setup 51 → not overextended 49 → ATR band 31 → stop within limit 29 → target & R:R after costs 7 → position size 7 → short interest / fund type 7
Target step failures: resistance too close 17, R:R after costs < min 5

## MidCap 400 — 4 of 400 passed all filters; top 4 profile-checked, 4 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| RGA | Inside bar near resistance | 265.15 | BS 269.76 | 262.26 | 291.34 | 1.94 | 2.5 | 4.5 | ⚠ Earnings on 2026-11-05 AMC |
| MORN | NR7 near resistance | 225.29 | BS 226.59 | 217.39 | 249.25 | 1.13 | 2.22 | 4.0 | ⚠ Earnings on 2026-10-28 AMC |
| BJ | Bull flag / tight consolidation | 106.36 | BS 107.95 | 103.77 | 118.75 | 4.86 | 2.33 | 4.0 |  |
| AVTR | NR7 near resistance | 17.29 | BS 17.41 | 16.7 | 19.15 | 14.79 | 2.21 | 3.0 | ⚠ Earnings on 2026-10-28 BMO |
Funnel: universe 400 → enough price history 400 → price floor 400 → listing checks 398 → no reverse split / wild gaps 398 → liquidity 398 → primary uptrend (50 EMA, 200) 138 → 20 EMA 133 → 3M relative strength vs SPY > 0 84 → RSI 40-75 73 → named setup 37 → not overextended 32 → ATR band 29 → stop within limit 23 → target & R:R after costs 4 → position size 4 → short interest / fund type 4
Target step failures: resistance too close 13, R:R after costs < min 6

## SmallCap 600 — 6 of 600 passed all filters; top 6 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| LQDT | Pullback to 20 EMA | 45.42 | LMT 45.42 | 43.82 | 49.9 | 11.56 | 2.5 | 5.5 |  |
| LTC | Pullback to 20 EMA | 43.96 | LMT 43.96 | 42.62 | 47.77 | 11.95 | 2.5 | 5.0 | ⚠ Earnings on 2026-11-03 AMC |
| UFCS | NR7 near resistance | 57.58 | BS 58.28 | 56.04 | 64.11 | 9.01 | 2.34 | 4.5 | ⚠ Earnings on 2026-11-03 AMC |
| DRH | Bull flag / tight consolidation | 13.94 | BS 14.08 | 13.44 | 15.49 | 32.83 | 2.0 | 4.5 | ⚠ Earnings on 2026-11-03 AMC |
| WAY | NR7 near resistance | 28.69 | BS 28.94 | 27.91 | 31.83 | 9.07 | 2.51 | 3.5 | ⚠ Earnings on 2026-11-02 AMC |
Funnel: universe 600 → enough price history 589 → price floor 574 → listing checks 572 → no reverse split / wild gaps 571 → liquidity 565 → primary uptrend (50 EMA, 200) 227 → 20 EMA 218 → 3M relative strength vs SPY > 0 117 → RSI 40-75 101 → named setup 55 → not overextended 50 → ATR band 48 → stop within limit 23 → target & R:R after costs 6 → position size 6 → short interest / fund type 6
Target step failures: resistance too close 16, R:R after costs < min 1

## Microcap — 1 of 451 passed all filters; top 1 profile-checked, 1 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| AUDC | Bull flag / tight consolidation | 11.47 | BS 11.6 | 11.08 | 12.76 | 40.41 | 2.03 | 5.0 | ⚠ Earnings on 2026-11-04 BMO |
_Universe is a market-cap PROXY, not index membership._
Funnel: universe 451 → enough price history 413 → price floor 406 → listing checks 392 → no reverse split / wild gaps 357 → liquidity 117 → primary uptrend (50 EMA, 200) 30 → 20 EMA 25 → 3M relative strength vs SPY > 0 24 → RSI 40-75 22 → named setup 12 → not overextended 9 → ATR band 7 → stop within limit 3 → target & R:R after costs 1 → position size 1 → short interest / fund type 1
Target step failures: resistance too close 2, R:R after costs < min 0
