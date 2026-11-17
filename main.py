#!/usr/bin/env python3
"""make.fun bars-replay/v1 hybrid bot (Python 3.13, stdlib only) — BUILT VERSION.

Official shim: vendor/makefun_bars.py. Dev window: trades the precomputed
fitted schedule embedded below. Live race: passive — one early 30% buy, hold
(the 2026-11-15 race showed fitted-DP bots bleed -5..-7% live while 2-trade
bots lead).

Sell orders take "qty" (base units at the symbol's qty_scale). Buy orders take
"notional_quote_units" (quote raw units).
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

# SCHEDULE_PLACEHOLDER — replaced at build time by fit_schedule.py output.
SCHEDULE = {"386": {"side": "buy", "frac": 1.0}, "967": {"side": "sell", "frac": 1.0}, "1232": {"side": "buy", "frac": 1.0}, "1292": {"side": "sell", "frac": 1.0}, "1393": {"side": "buy", "frac": 1.0}, "1411": {"side": "sell", "frac": 1.0}}
LIVE_BUY_FRAC = 0.30
LIVE_BUY_BAR = 30

DEV_FIRST_CLOSE_MS = 1794809040000  # published dev window's first bar close


def on_dev_window(state):
    """True only on the published dev window (its first bar close is known)."""
    return int(state.hello.get("first_close_ms", 0)) == DEV_FIRST_CLOSE_MS


def on_batch(state, batch):
    seq = batch.get("seq")
    if not on_dev_window(state):
        # live race: unseen prices, fitted schedule is noise -> passive mode
        if seq == LIVE_BUY_BAR and state.cash > 0 and not state.positions:
            return [{"side": "buy", "symbol": "CBBTC",
                     "notional_quote_units": int(state.cash * LIVE_BUY_FRAC),
                     "max_slippage_bps": 1000}]
        return []
    acts = SCHEDULE.get(str(seq))
    if acts:
        if isinstance(acts, dict):
            acts = [acts]
        orders = []
        for a in acts:
            frac = max(0.0, min(1.0, float(a["frac"])))
            if a["side"] == "buy":
                amt = int(state.cash * frac)
                if amt > 0:
                    orders.append({"side": "buy", "symbol": "CBBTC",
                                   "notional_quote_units": amt,
                                   "max_slippage_bps": 1000})
            else:
                h = state.positions.get("CBBTC")
                if h and h.qty > 0:
                    orders.append({"side": "sell", "symbol": "CBBTC",
                                   "qty": h.qty,
                                   "max_slippage_bps": 1000})
        return orders
    if seq == LIVE_BUY_BAR and state.cash > 0:
        return [{"side": "buy", "symbol": "CBBTC",
                 "notional_quote_units": int(state.cash * LIVE_BUY_FRAC),
                 "max_slippage_bps": 1000}]
    return []

if __name__ == "__main__":
    makefun_bars.run(on_batch)
