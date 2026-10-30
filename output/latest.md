# US swing scan — 2026-10-30
Status: **ok** — scan complete  
Generated 2026-10-30 18:54 ET / 2026-10-31 04:24 IST

Capital $2106.59 (₹200,000 ÷ 94.94), risk $21.07 per trade, max position $526.65

## Data checks
```
{
  "session_scanned": "2026-10-30",
  "listing": {
    "nasdaqlisted": "ok (5616 symbols)",
    "otherlisted": "ok (7670 symbols)"
  },
  "constituents": {
    "SP500": "downloaded (Wikipedia, 503 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "SP400": "downloaded (Wikipedia, 400 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "SP600": "downloaded (Wikipedia, 603 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']",
    "MICRO": "downloaded (PROXY: Nasdaq screener, market cap $50M–$300M, price ≥ $5, 442 stocks) — earlier sources failed: iShares holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']; BlackRock holdings: no 'Ticker' header row in holdings file [got text/csv;charset=UTF-8: '<!DOCTYPE html> <html xmlns=\"http://www.w3.org/1999/xhtml\" prefix=\"og: http://ogp.me/ns#\"']"
  },
  "prices": {
    "source": "Yahoo Finance (yfinance)",
    "requested": 1945,
    "received": 1944,
    "missing": [
      "CWEN-A"
    ]
  },
  "market_tickers_missing": [],
  "regsho": "ok (file 2026-10-30)"
}
```

## Market
- SPY 755.72 | 20/50/200 EMA 767.73 / 765.92 / 732.96 | 5d -0.56% | 21d -1.08% | HH/HL True
- QQQ 690.49 | 20/50/200 EMA 721.13 / 723.04 / 685.21 | 5d -1.97% | 21d -6.95% | HH/HL False
- IWM 279.33 | 20/50/200 EMA 278.82 / 282.73 / 276.8 | 5d 1.3% | 21d 0.11% | HH/HL False
- VIX 19.42 (-0.15% 5d), VIX3M 20.78, contango (calm)
- Breadth: S&P 500 above 50 EMA 62.8%, above 200 EMA 61.4%
- Sectors 1M: XLE 11.67%, XLP 11.32%, XLV 11.23%, XLU 9.45%, XLB 8.65%, XLRE 6.12%, XLY 6.04%, XLF 5.71%, XHB 4.33%, KRE 2.94%, XBI 0.95%, ITA 0.82%, XLI -0.74%, IGV -3.64%, XLC -9.13%, XLK -9.25%, SMH -15.43%

## S&P 500 — 20 of 503 passed all filters; top 8 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| MO | 52-week high breakout | 78.03 | LMT 78.03 | 75.47 | 85.25 | 6.74 | 2.5 | 8.5 |  |
| CVX | 52-week high breakout | 235.52 | LMT 235.52 | 227.17 | 258.87 | 2.23 | 2.5 | 8.02 |  |
| EG | Gap continuation (gap held) | 410.97 | LMT 410.97 | 396.67 | 451.04 | 1.28 | 2.5 | 7.75 |  |
| XOM | 52-week high breakout | 187.25 | LMT 187.25 | 179.37 | 205.98 | 2.67 | 2.15 | 7.34 |  |
| AJG | 52-week high breakout | 276.07 | LMT 276.07 | 265.09 | 303.68 | 1.9 | 2.27 | 7.16 |  |
Funnel: universe 503 → enough price history 500 → price floor 500 → listing checks 499 → no reverse split / wild gaps 496 → liquidity 493 → primary uptrend (50 EMA, 200) 213 → 20 EMA 201 → 3M relative strength vs SPY > 0 170 → RSI 40-75 154 → named setup 68 → not overextended 66 → ATR band 52 → stop within limit 52 → target & R:R after costs 20 → position size 20 → short interest / fund type 20
Target step failures: resistance too close 20, R:R after costs < min 12

## MidCap 400 — 11 of 400 passed all filters; top 8 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| THG | 52-week high breakout | 242.09 | LMT 242.09 | 234.97 | 262.43 | 2.17 | 2.5 | 6.16 |  |
| EHC | 52-week high breakout | 135.9 | LMT 135.9 | 129.96 | 149.49 | 3.54 | 2.08 | 6.1 |  |
| MORN | Bull flag / tight consolidation | 226.19 | BS 226.74 | 217.18 | 249.41 | 2.2 | 2.15 | 5.5 |  |
| BJ | Bull flag / tight consolidation | 107.32 | BS 107.95 | 103.11 | 118.75 | 4.35 | 2.03 | 5.5 |  |
| CNO | Pullback to 20 EMA | 57.67 | LMT 57.67 | 55.97 | 62.53 | 9.13 | 2.5 | 5.5 |  |
Funnel: universe 400 → enough price history 400 → price floor 400 → listing checks 398 → no reverse split / wild gaps 398 → liquidity 398 → primary uptrend (50 EMA, 200) 144 → 20 EMA 134 → 3M relative strength vs SPY > 0 99 → RSI 40-75 82 → named setup 40 → not overextended 38 → ATR band 35 → stop within limit 32 → target & R:R after costs 11 → position size 11 → short interest / fund type 11
Target step failures: resistance too close 17, R:R after costs < min 4

## SmallCap 600 — 3 of 600 passed all filters; top 4 profile-checked, 3 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| ADUS | 52-week high breakout | 125.54 | LMT 125.54 | 121.39 | 137.23 | 2.09 | 2.5 | 5.55 | ⚠ Earnings on 2026-11-03 AMC |
| MD | Bull flag / tight consolidation | 29.82 | BS 30.61 | 29.25 | 33.67 | 15.48 | 2.04 | 5.5 |  |
| LPG | Pullback to 20 EMA | 54.43 | LMT 54.43 | 52.32 | 59.53 | 4.83 | 2.17 | -0.5 | ⚠ Earnings on 2026-11-05 BMO |
Funnel: universe 600 → enough price history 589 → price floor 576 → listing checks 574 → no reverse split / wild gaps 573 → liquidity 567 → primary uptrend (50 EMA, 200) 219 → 20 EMA 205 → 3M relative strength vs SPY > 0 150 → RSI 40-75 136 → named setup 60 → not overextended 55 → ATR band 47 → stop within limit 20 → target & R:R after costs 4 → position size 4 → short interest / fund type 3
Target step failures: resistance too close 12, R:R after costs < min 4

## Microcap — 0 of 442 passed all filters; top 0 profile-checked, 0 shown
NO TRADE — closest: III (failed: target & R:R after costs — target only 2.6% away (resistance too close))
_Universe is a market-cap PROXY, not index membership._
Funnel: universe 442 → enough price history 402 → price floor 392 → listing checks 375 → no reverse split / wild gaps 344 → liquidity 111 → primary uptrend (50 EMA, 200) 33 → 20 EMA 29 → 3M relative strength vs SPY > 0 28 → RSI 40-75 23 → named setup 10 → not overextended 7 → ATR band 6 → stop within limit 2 → target & R:R after costs 0 → position size 0 → short interest / fund type 0
Target step failures: resistance too close 2, R:R after costs < min 0
