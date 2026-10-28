# US swing scan — 2026-10-28
Status: **ok** — scan complete  
Generated 2026-10-28 18:56 ET / 2026-10-29 04:26 IST

Capital $2100.62 (₹200,000 ÷ 95.21), risk $21.01 per trade, max position $525.15

## Data checks
```
{
  "session_scanned": "2026-10-28",
  "listing": {
    "nasdaqlisted": "ok (5617 symbols)",
    "otherlisted": "ok (7670 symbols)"
  },
  "constituents": {
    "SP500": "downloaded (Wikipedia, 503 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "SP400": "downloaded (Wikipedia, 400 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "SP600": "downloaded (Wikipedia, 603 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "MICRO": "downloaded (PROXY: Nasdaq screener, market cap $50M–$300M, price ≥ $5, 448 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']"
  },
  "prices": {
    "source": "Yahoo Finance (yfinance)",
    "requested": 1951,
    "received": 1950,
    "missing": [
      "CWEN-A"
    ]
  },
  "market_tickers_missing": [],
  "regsho": "ok (file 2026-10-28)"
}
```

## Market
- SPY 772.31 | 20/50/200 EMA 768.96 / 766.21 / 732.45 | 5d -0.1% | 21d 1.06% | HH/HL True
- QQQ 725.61 | 20/50/200 EMA 725.3 / 724.73 / 684.97 | 5d 0.06% | 21d -1.67% | HH/HL True
- IWM 281.29 | 20/50/200 EMA 278.21 / 282.82 / 276.73 | 5d 1.74% | 21d 0.82% | HH/HL False
- VIX 16.91 (1.38% 5d), VIX3M 19.22, contango (calm)
- Breadth: S&P 500 above 50 EMA 59.2%, above 200 EMA 60.8%
- Sectors 1M: XLE 11.23%, XLU 7.0%, IGV 6.36%, XLP 6.1%, XLY 5.66%, XLB 5.62%, XLV 5.27%, XLF 3.93%, KRE 3.27%, XLRE 1.91%, XHB 1.03%, XBI 0.45%, XLI -0.38%, ITA -0.75%, XLK -1.8%, SMH -6.46%, XLC -7.47%

## S&P 500 — 11 of 503 passed all filters; top 8 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| GEHC | Base breakout on volume | 75.82 | LMT 75.82 | 72.72 | 83.4 | 6.77 | 2.21 | 7.0 |  |
| NDAQ | NR7 near resistance | 105.55 | BS 105.88 | 102.47 | 115.52 | 4.95 | 2.5 | 6.0 |  |
| TMO | Pullback to 20 EMA | 704.15 | LMT 704.15 | 673.78 | 774.57 | 0.69 | 2.1 | 4.5 |  |
| MDT | Pullback to 20 EMA | 94.78 | LMT 94.78 | 92.5 | 100.81 | 5.54 | 2.24 | 4.5 |  |
| VTRS | Bull flag / tight consolidation | 18.77 | BS 18.87 | 18.14 | 20.76 | 27.83 | 2.33 | 4.5 | ⚠ Earnings on 2026-11-05 BMO |
Funnel: universe 503 → enough price history 500 → price floor 500 → listing checks 499 → no reverse split / wild gaps 496 → liquidity 493 → primary uptrend (50 EMA, 200) 203 → 20 EMA 191 → 3M relative strength vs SPY > 0 123 → RSI 40-75 113 → named setup 54 → not overextended 54 → ATR band 38 → stop within limit 37 → target & R:R after costs 11 → position size 11 → short interest / fund type 11
Target step failures: resistance too close 21, R:R after costs < min 5

## MidCap 400 — 2 of 400 passed all filters; top 3 profile-checked, 2 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| SN | Bull flag / tight consolidation | 198.17 | BS 200.79 | 191.74 | 220.87 | 1.15 | 2.02 | 3.5 | ⚠ Earnings on 2026-11-04 BMO |
| PR | Inside bar near resistance | 25.52 | BS 25.9 | 24.83 | 28.49 | 9.81 | 2.19 | 3.0 | ⚠ Earnings on 2026-11-04 AMC |
Funnel: universe 400 → enough price history 400 → price floor 400 → listing checks 398 → no reverse split / wild gaps 398 → liquidity 398 → primary uptrend (50 EMA, 200) 126 → 20 EMA 122 → 3M relative strength vs SPY > 0 82 → RSI 40-75 76 → named setup 42 → not overextended 41 → ATR band 38 → stop within limit 33 → target & R:R after costs 3 → position size 3 → short interest / fund type 2
Target step failures: resistance too close 22, R:R after costs < min 8

## SmallCap 600 — 2 of 600 passed all filters; top 4 profile-checked, 2 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| CON | NR7 near resistance | 40.59 | BS 40.72 | 39.34 | 44.6 | 12.89 | 2.5 | 6.0 | ⚠ Earnings on 2026-11-05 AMC |
| KNTK | Pullback to 20 EMA | 56.61 | LMT 56.61 | 54.18 | 62.27 | 4.32 | 2.11 | 3.0 | ⚠ Earnings on 2026-11-04 AMC |
Funnel: universe 600 → enough price history 588 → price floor 573 → listing checks 571 → no reverse split / wild gaps 570 → liquidity 563 → primary uptrend (50 EMA, 200) 209 → 20 EMA 191 → 3M relative strength vs SPY > 0 118 → RSI 40-75 104 → named setup 44 → not overextended 40 → ATR band 38 → stop within limit 15 → target & R:R after costs 4 → position size 4 → short interest / fund type 2
Target step failures: resistance too close 9, R:R after costs < min 2

## Microcap — 2 of 448 passed all filters; top 2 profile-checked, 2 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| AUDC | Bull flag / tight consolidation | 11.66 | BS 11.76 | 11.24 | 12.94 | 20.19 | 2.06 | 4.0 | ⚠ Earnings on 2026-11-04 BMO |
| FBLA | Pullback to 20 EMA | 17.26 | LMT 17.26 | 16.74 | 18.74 | 15.21 | 2.5 | 3.5 | ⚠ Earnings on 2026-10-29 AMC |
_Universe is a market-cap PROXY, not index membership._
Funnel: universe 448 → enough price history 415 → price floor 413 → listing checks 393 → no reverse split / wild gaps 355 → liquidity 116 → primary uptrend (50 EMA, 200) 36 → 20 EMA 36 → 3M relative strength vs SPY > 0 36 → RSI 40-75 30 → named setup 19 → not overextended 16 → ATR band 13 → stop within limit 5 → target & R:R after costs 2 → position size 2 → short interest / fund type 2
Target step failures: resistance too close 2, R:R after costs < min 1
