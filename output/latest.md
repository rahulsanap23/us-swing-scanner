# US swing scan — 2026-10-22
Status: **ok** — scan complete  
Generated 2026-10-23 14:02 ET / 2026-10-23 23:32 IST

Capital $2120.61 (₹200,000 ÷ 94.31), risk $21.21 per trade, max position $530.15

## Data checks
```
{
  "session_scanned": "2026-10-22",
  "listing": {
    "nasdaqlisted": "ok (5625 symbols)",
    "otherlisted": "ok (7674 symbols)"
  },
  "constituents": {
    "SP500": "downloaded (Wikipedia, 503 stocks)",
    "SP400": "downloaded (Wikipedia, 400 stocks)",
    "SP600": "downloaded (Wikipedia, 603 stocks)",
    "MICRO": "MISSING (download failed: iShares holdings: no 'Ticker' header row in holdings file)"
  },
  "prices": {
    "source": "Yahoo Finance (yfinance)",
    "requested": 1503,
    "received": 1502,
    "missing": [
      "CWEN-A"
    ]
  },
  "market_tickers_missing": [],
  "regsho": "ok (file 2026-10-22)"
}
```

## Market
- SPY 763.96 | 20/50/200 EMA 769.76 / 766.07 / 731.02 | 5d -1.01% | 21d -0.5% | HH/HL True
- QQQ 704.47 | 20/50/200 EMA 729.5 / 726.21 / 683.62 | 5d -3.23% | 21d -4.96% | HH/HL True
- IWM 276.67 | 20/50/200 EMA 277.92 / 283.54 / 276.64 | 5d 0.58% | 21d -1.86% | HH/HL False
- VIX 19.03 (15.61% 5d), VIX3M 20.12, contango (calm)
- Breadth: S&P 500 above 50 EMA 64.4%, above 200 EMA 61.2%
- Sectors 1M: XLP 9.17%, XLE 8.34%, XLU 7.85%, XLV 7.41%, XLY 3.94%, XLF 3.87%, KRE 2.88%, XLB 2.8%, XHB 2.17%, XLRE 1.63%, IGV 0.57%, XLI -1.98%, XBI -2.29%, ITA -4.41%, XLC -4.57%, XLK -6.66%, SMH -12.98%

## S&P 500 — 6 of 503 passed all filters; top 6 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| KDP | 52-week high breakout | 35.19 | LMT 35.19 | 34.06 | 38.38 | 15.06 | 2.5 | 7.42 | ⚠ Earnings on 2026-11-03 BMO |
| NDAQ | 52-week high breakout | 103.3 | LMT 103.3 | 99.77 | 113.21 | 2.56 | 2.5 | 6.41 | ⚠ Earnings on 2026-10-22 |
| ELV | Inside bar near resistance | 445.28 | BS 450.85 | 433.1 | 495.94 | 1.17 | 2.29 | 5.0 | unverified: earnings date |
| AAPL | Pullback to 20 EMA | 348.22 | LMT 348.22 | 338.06 | 377.28 | 1.52 | 2.5 | 5.0 | ⚠ Earnings on 2026-11-02 AMC |
| XOM | Bull flag / tight consolidation | 178.23 | BS 180.62 | 174.25 | 198.44 | 2.93 | 2.5 | 4.0 | ⚠ Earnings on 2026-10-30 BMO |
Funnel: universe 503 → enough price history 500 → price floor 500 → listing checks 499 → no reverse split / wild gaps 496 → liquidity 493 → primary uptrend (50 EMA, 200) 209 → 20 EMA 200 → 3M relative strength vs SPY > 0 142 → RSI 40-75 109 → named setup 45 → not overextended 44 → ATR band 35 → stop within limit 32 → target & R:R after costs 6 → position size 6 → short interest / fund type 6

## MidCap 400 — 3 of 400 passed all filters; top 3 profile-checked, 3 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| EQH | Pullback to 20 EMA | 55.04 | LMT 55.04 | 52.84 | 60.54 | 9.63 | 2.26 | 4.5 | ⚠ Earnings on 2026-11-02 AMC |
| CRBG | Pullback to 20 EMA | 35.59 | LMT 35.59 | 34.13 | 39.15 | 14.52 | 2.2 | 4.5 | ⚠ Earnings on 2026-11-02 AMC |
| AMG | Pullback to 20 EMA | 395.53 | LMT 395.53 | 379.19 | 435.08 | 1.29 | 2.19 | 4.5 | ⚠ Earnings on 2026-11-02 BMO |
Funnel: universe 400 → enough price history 400 → price floor 400 → listing checks 398 → no reverse split / wild gaps 398 → liquidity 398 → primary uptrend (50 EMA, 200) 142 → 20 EMA 135 → 3M relative strength vs SPY > 0 98 → RSI 40-75 86 → named setup 34 → not overextended 32 → ATR band 27 → stop within limit 19 → target & R:R after costs 3 → position size 3 → short interest / fund type 3

## SmallCap 600 — 5 of 600 passed all filters; top 6 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| UCB | 52-week high breakout | 37.23 | LMT 37.23 | 36.07 | 40.52 | 14.23 | 2.5 | 7.21 |  |
| MD | 52-week high breakout | 29.55 | LMT 29.55 | 28.32 | 32.51 | 8.61 | 2.18 | 5.62 | ⚠ Earnings on 2026-10-29 BMO |
| ICUI | Pullback to 20 EMA | 168.33 | LMT 168.33 | 161.5 | 185.16 | 3.1 | 2.23 | 4.5 | ⚠ Earnings on 2026-11-05 AMC |
| URBN | Bull flag / tight consolidation | 88.29 | BS 90.77 | 86.89 | 99.85 | 5.46 | 2.12 | 4.0 |  |
| MMSI | Pullback to 20 EMA | 93.94 | LMT 93.94 | 90.4 | 103.33 | 2.82 | 2.38 | 3.5 | ⚠ Earnings on 2026-10-29 AMC |
Funnel: universe 600 → enough price history 590 → price floor 576 → listing checks 574 → no reverse split / wild gaps 573 → liquidity 567 → primary uptrend (50 EMA, 200) 218 → 20 EMA 208 → 3M relative strength vs SPY > 0 126 → RSI 40-75 103 → named setup 50 → not overextended 47 → ATR band 43 → stop within limit 20 → target & R:R after costs 6 → position size 6 → short interest / fund type 5

## Microcap — 0 of 0 passed all filters; top 0 profile-checked, 0 shown
NO TRADE — closest: None (failed: None — None)
Funnel: universe 0 → enough price history 0 → price floor 0 → listing checks 0 → no reverse split / wild gaps 0 → liquidity 0 → primary uptrend (50 EMA, 200) 0 → 20 EMA 0 → 3M relative strength vs SPY > 0 0 → RSI 40-75 0 → named setup 0 → not overextended 0 → ATR band 0 → stop within limit 0 → target & R:R after costs 0 → position size 0 → short interest / fund type 0
