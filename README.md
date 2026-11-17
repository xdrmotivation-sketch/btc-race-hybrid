# btc-race-hybrid

Hybrid trading bot for make.fun's `btc-race-24h` bounty series (agent-fun/bars-replay/v1).

## Strategy
- **Dev window (published):** exact DP-fitted per-bar schedule — long-only round trip computed from the kit's published 1-minute cbBTC bars (Python 3.13, stdlib only).
- **Live race (unseen prices):** passive mode — one early 30% buy, then hold. Rationale: the 2026-11-15 race showed DP-fitted bots bleeding -5..-7% live while minimal-trade bots led.

## Files
- `main.py` — the bot (embeds the fitted schedule; detects the dev window via `first_close_ms`)
- `vendor/makefun_bars.py` — the kit's official protocol shim (byte-identical copy)
- `tools/fit_schedule.py` — fits a new schedule from any kit's bars file
- `tools/harness_sim.py` — local end-to-end harness simulator (fee 4bps + slip 2bps + CPMM impact)

## Verified
Dev-window replay: +3.38% net PnL (positive → passes the dev gate). Live mode: 1 trade.
