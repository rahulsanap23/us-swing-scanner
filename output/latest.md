# US swing scan — 2026-10-27
Status: **ok** — scan complete  
Generated 2026-10-27 18:52 ET / 2026-10-28 04:22 IST

Capital $2102.94 (₹200,000 ÷ 95.11), risk $21.03 per trade, max position $525.73

## Data checks
```
{
  "session_scanned": "2026-10-27",
  "listing": {
    "nasdaqlisted": "ok (5621 symbols)",
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
  "regsho": "ok (file 2026-10-27)"
}
```

## Market
- SPY 769.66 | 20/50/200 EMA 768.61 / 765.96 / 732.05 | 5d 0.08% | 21d 0.53% | HH/HL True
- QQQ 721.25 | 20/50/200 EMA 725.27 / 724.7 / 684.52 | 5d 0.5% | 21d -2.07% | HH/HL True
- IWM 280.18 | 20/50/200 EMA 277.89 / 282.88 / 276.69 | 5d 1.6% | 21d 0.06% | HH/HL False
- VIX 17.52 (1.21% 5d), VIX3M 19.57, contango (calm)
- Breadth: S&P 500 above 50 EMA 62.4%, above 200 EMA 60.8%
- Sectors 1M: XLE 9.84%, XLU 9.17%, IGV 6.02%, XLY 5.92%, XLP 5.92%, XLB 4.67%, XLV 4.62%, XLF 3.12%, KRE 2.88%, XLRE 2.64%, XHB 1.91%, XLI -0.51%, XBI -1.13%, ITA -1.45%, XLK -2.59%, XLC -6.84%, SMH -7.0%

## S&P 500 — 7 of 503 passed all filters; top 7 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| WST | 52-week high breakout | 398.29 | LMT 398.29 | 386.14 | 432.85 | 0.65 | 2.5 | 6.03 | ⚠ Earnings on 2026-10-29 BMO |
| EXPD | Pullback to 20 EMA | 199.64 | LMT 199.64 | 193.3 | 217.59 | 1.31 | 2.5 | 4.5 | ⚠ Earnings on 2026-11-03 BMO |
| KDP | Bull flag / tight consolidation | 34.86 | BS 35.47 | 34.2 | 39.02 | 7.41 | 2.5 | 4.0 | ⚠ Earnings on 2026-11-03 BMO |
| IFF | Bull flag / tight consolidation | 93.21 | BS 94.84 | 92.12 | 102.64 | 2.77 | 2.5 | 3.5 | ⚠ Earnings on 2026-11-03 AMC |
| EMR | Pullback to 20 EMA | 166.27 | LMT 166.27 | 159.77 | 182.9 | 3.16 | 2.3 | 3.5 | ⚠ Earnings on 2026-11-04 BMO |
Funnel: universe 503 → enough price history 500 → price floor 500 → listing checks 499 → no reverse split / wild gaps 496 → liquidity 493 → primary uptrend (50 EMA, 200) 210 → 20 EMA 196 → 3M relative strength vs SPY > 0 105 → RSI 40-75 100 → named setup 47 → not overextended 44 → ATR band 28 → stop within limit 28 → target & R:R after costs 7 → position size 7 → short interest / fund type 7
Target step failures: resistance too close 17, R:R after costs < min 4

## MidCap 400 — 6 of 400 passed all filters; top 7 profile-checked, 5 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| RS | Bull flag / tight consolidation | 432.79 | BS 435.87 | 418.88 | 479.46 | 1.2 | 2.31 | 5.5 |  |
| SN | Bull flag / tight consolidation | 197.53 | BS 200.79 | 191.72 | 220.87 | 2.31 | 2.01 | 4.5 | ⚠ Earnings on 2026-11-04 BMO |
| PR | Inside bar near resistance | 25.46 | BS 25.97 | 24.86 | 28.57 | 18.94 | 2.12 | 4.0 | ⚠ Earnings on 2026-11-04 AMC |
| CRBG | Pullback to 20 EMA | 35.36 | LMT 35.36 | 33.85 | 38.9 | 6.96 | 2.12 | 4.0 | ⚠ Earnings on 2026-11-02 AMC |
| AMG | Inside bar near resistance | 391.99 | BS 396.33 | 380.92 | 435.96 | 0.66 | 2.32 | 3.5 | ⚠ Earnings on 2026-11-02 BMO |
Funnel: universe 400 → enough price history 400 → price floor 400 → listing checks 398 → no reverse split / wild gaps 398 → liquidity 398 → primary uptrend (50 EMA, 200) 134 → 20 EMA 126 → 3M relative strength vs SPY > 0 73 → RSI 40-75 64 → named setup 32 → not overextended 30 → ATR band 26 → stop within limit 19 → target & R:R after costs 7 → position size 7 → short interest / fund type 6
Target step failures: resistance too close 11, R:R after costs < min 1

## SmallCap 600 — 2 of 600 passed all filters; top 3 profile-checked, 2 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| CON | Bull flag / tight consolidation | 40.0 | BS 40.42 | 39.01 | 44.37 | 13.0 | 2.5 | 5.0 | ⚠ Earnings on 2026-11-05 AMC |
| URBN | Bull flag / tight consolidation | 90.73 | BS 92.05 | 87.96 | 101.26 | 5.14 | 2.05 | 5.0 |  |
Funnel: universe 600 → enough price history 588 → price floor 574 → listing checks 572 → no reverse split / wild gaps 571 → liquidity 564 → primary uptrend (50 EMA, 200) 227 → 20 EMA 211 → 3M relative strength vs SPY > 0 110 → RSI 40-75 99 → named setup 49 → not overextended 47 → ATR band 44 → stop within limit 24 → target & R:R after costs 3 → position size 3 → short interest / fund type 2
Target step failures: resistance too close 16, R:R after costs < min 5

## Microcap — 1 of 448 passed all filters; top 1 profile-checked, 1 shown
| Ticker | Setup | Last | Entry | Stop | Target | Qty | R:R net | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|
| FBLA | Pullback to 20 EMA | 17.2 | LMT 17.2 | 16.67 | 18.71 | 15.28 | 2.51 | 4.5 | ⚠ Earnings on 2026-10-29 AMC |
_Universe is a market-cap PROXY, not index membership._
Funnel: universe 448 → enough price history 410 → price floor 408 → listing checks 392 → no reverse split / wild gaps 358 → liquidity 117 → primary uptrend (50 EMA, 200) 34 → 20 EMA 31 → 3M relative strength vs SPY > 0 29 → RSI 40-75 27 → named setup 17 → not overextended 11 → ATR band 6 → stop within limit 2 → target & R:R after costs 1 → position size 1 → short interest / fund type 1
Target step failures: resistance too close 1, R:R after costs < min 0
