# US swing scan — 2026-10-29
Status: **ok** — scan complete  
Generated 2026-10-29 18:57 ET / 2026-10-30 04:27 IST

Capital $2100.62 (₹200,000 ÷ 95.21), risk $21.01 per trade, max position $525.15

## Data checks
```
{
  "session_scanned": "2026-10-29",
  "listing": {
    "nasdaqlisted": "ok (5621 symbols)",
    "otherlisted": "ok (7672 symbols)"
  },
  "constituents": {
    "SP500": "downloaded (Wikipedia, 503 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "SP400": "downloaded (Wikipedia, 400 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "SP600": "downloaded (Wikipedia, 603 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "MICRO": "downloaded (PROXY: Nasdaq screener, market cap $50M–$300M, price ≥ $5, 444 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']"
  },
  "prices": {
    "source": "Yahoo Finance (yfinance)",
    "requested": 1947,
    "received": 1946,
    "missing": [
      "CWEN-A"
    ]
  },
  "market_tickers_missing": [],
  "regsho": "ok (file 2026-10-29)"
}
```

## Market
- SPY 769.36 | 20/50/200 EMA 769.0 / 766.34 / 732.81 | 5d 0.71% | 21d 0.88% | HH/HL True
- QQQ 715.34 | 20/50/200 EMA 724.35 / 724.37 / 685.24 | 5d 1.54% | 21d -3.3% | HH/HL True
- IWM 284.01 | 20/50/200 EMA 278.77 / 282.87 / 276.8 | 5d 2.65% | 21d 2.2% | HH/HL False
- VIX 17.2 (-9.62% 5d), VIX3M 19.37, contango (calm)
- Breadth: S&P 500 above 50 EMA 67.4%, above 200 EMA 64.4%
- Sectors 1M: XLE 11.72%, XLP 9.4%, XLU 9.38%, XLV 9.27%, XLB 7.86%, XLY 6.76%, XLF 6.63%, XHB 5.46%, XLRE 5.26%, KRE 4.93%, ITA 3.44%, XLI 1.89%, IGV 1.4%, XBI 0.07%, XLK -3.58%, SMH -7.77%, XLC -8.8%

## S&P 500 — 19 of 503 passed all filters; top 8 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| MSI | Base breakout on volume | 492.08 | LMT 492.08 | 479.5 | 528.7 | 0.53 | 2.5 | 6.01 | ⚠ Earnings on 2026-11-04 AMC |
| GEHC | Gap continuation (gap held) | 76.42 | LMT 76.42 | 73.33 | 84.06 | 6.79 | 2.23 | 5.73 |  |
| MO | Pullback to 20 EMA | 76.75 | LMT 76.75 | 74.35 | 83.56 | 6.84 | 2.5 | 5.5 |  |
| GILD | 52-week high breakout | 165.61 | LMT 165.61 | 159.53 | 182.17 | 1.58 | 2.44 | 4.95 | ⚠ Earnings on 2026-10-29 AMC |
| ABBV | Pullback to 20 EMA | 290.79 | LMT 290.79 | 280.6 | 319.32 | 0.9 | 2.5 | 4.5 | ⚠ Earnings on 2026-10-30 BMO |
Funnel: universe 503 → enough price history 500 → price floor 500 → listing checks 499 → no reverse split / wild gaps 496 → liquidity 493 → primary uptrend (50 EMA, 200) 227 → 20 EMA 221 → 3M relative strength vs SPY > 0 156 → RSI 40-75 143 → named setup 83 → not overextended 81 → ATR band 61 → stop within limit 61 → target & R:R after costs 19 → position size 19 → short interest / fund type 19
Target step failures: resistance too close 37, R:R after costs < min 5

## MidCap 400 — 9 of 400 passed all filters; top 8 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| EHC | 52-week high breakout | 131.49 | LMT 131.49 | 125.76 | 144.64 | 3.66 | 2.08 | 6.58 |  |
| RS | NR7 near resistance | 439.71 | BS 441.83 | 425.01 | 486.01 | 1.18 | 2.36 | 5.5 |  |
| MEDP | Inside bar near resistance | 677.56 | BS 691.38 | 660.24 | 760.52 | 0.67 | 2.02 | 4.5 |  |
| BJ | Bull flag / tight consolidation | 105.41 | BS 107.95 | 103.11 | 118.75 | 4.34 | 2.03 | 4.5 |  |
| NWE | Bull flag / tight consolidation | 79.22 | BS 80.37 | 77.88 | 87.44 | 3.26 | 2.5 | 4.0 | ⚠ Earnings on 2026-11-04 AMC |
Funnel: universe 400 → enough price history 400 → price floor 400 → listing checks 398 → no reverse split / wild gaps 398 → liquidity 398 → primary uptrend (50 EMA, 200) 161 → 20 EMA 155 → 3M relative strength vs SPY > 0 98 → RSI 40-75 85 → named setup 45 → not overextended 44 → ATR band 39 → stop within limit 29 → target & R:R after costs 10 → position size 10 → short interest / fund type 9
Target step failures: resistance too close 13, R:R after costs < min 6

## SmallCap 600 — 5 of 600 passed all filters; top 5 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| ADUS | Base breakout on volume | 124.34 | LMT 124.34 | 119.75 | 136.77 | 2.11 | 2.43 | 6.27 | ⚠ Earnings on 2026-11-03 AMC |
| UCB | NR7 near resistance | 37.21 | BS 37.43 | 36.04 | 41.17 | 14.03 | 2.41 | 5.0 |  |
| AMRX | Inside bar near resistance | 21.35 | BS 21.69 | 20.71 | 23.86 | 10.71 | 2.01 | 4.0 | ⚠ Earnings on 2026-11-03 BMO |
| LTC | Pullback to 20 EMA | 44.32 | LMT 44.32 | 42.85 | 48.46 | 5.92 | 2.5 | 3.5 | ⚠ Earnings on 2026-11-03 AMC |
| KNTK | Pullback to 20 EMA | 58.09 | LMT 58.09 | 55.61 | 63.9 | 4.23 | 2.12 | 3.0 | ⚠ Earnings on 2026-11-04 AMC |
Funnel: universe 600 → enough price history 589 → price floor 576 → listing checks 574 → no reverse split / wild gaps 573 → liquidity 566 → primary uptrend (50 EMA, 200) 241 → 20 EMA 233 → 3M relative strength vs SPY > 0 145 → RSI 40-75 127 → named setup 65 → not overextended 62 → ATR band 59 → stop within limit 38 → target & R:R after costs 5 → position size 5 → short interest / fund type 5
Target step failures: resistance too close 25, R:R after costs < min 8

## Microcap — 1 of 444 passed all filters; top 1 profile-checked, 1 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| PMTS | Pullback to 20 EMA | 26.23 | LMT 26.23 | 25.07 | 28.85 | 9.05 | 2.05 | 3.75 | ⚠ Earnings on 2026-11-04 BMO |
_Universe is a market-cap PROXY, not index membership._
Funnel: universe 444 → enough price history 404 → price floor 401 → listing checks 385 → no reverse split / wild gaps 349 → liquidity 116 → primary uptrend (50 EMA, 200) 36 → 20 EMA 35 → 3M relative strength vs SPY > 0 33 → RSI 40-75 27 → named setup 12 → not overextended 8 → ATR band 7 → stop within limit 1 → target & R:R after costs 1 → position size 1 → short interest / fund type 1
