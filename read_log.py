import json
import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURATION ---
LOG_FILE = '11131.log'
PRODUCT = 'TOMATOES'  # Change to 'EMERALDS' or 'TOMATOES'
START_STEP = 0
END_STEP = 500       # Adjust as needed
# ---------------------

def analyze_performance_v2(file_path, product, start, end):
    with open(file_path, 'r') as f:
        log = json.load(f)

    # 1. Parse Data
    df_market = pd.read_csv(io.StringIO(log['activitiesLog']), sep=';')
    df_trades = pd.DataFrame(log['tradeHistory'])

    # Filter market data
    df_m = df_market[(df_market['product'] == product) &
                     (df_market['timestamp'] >= start*100) &
                     (df_market['timestamp'] <= end*100)].copy()
    df_m['step'] = df_m['timestamp'] // 100

    # Filter trades
    df_t = df_trades[(df_trades['symbol'] == product) &
                     (df_trades['timestamp'] >= start*100) &
                     (df_trades['timestamp'] <= end*100)].copy()
    df_t['step'] = df_t['timestamp'] // 100

    # Separate My Trades (SUBMISSION) into Buys and Sells
    my_buys = df_t[df_t['buyer'] == 'SUBMISSION'].copy()
    my_sells = df_t[df_t['seller'] == 'SUBMISSION'].copy()
    others_trades = df_t[(df_t['buyer'] != 'SUBMISSION') & (df_t['seller'] != 'SUBMISSION')]

    # 2. CREATE VISUALIZATION
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), sharex=True,
                                        gridspec_kw={'height_ratios': [2, 1, 1]})

    # --- TOP PANEL: Order Book & Trades ---
    for i in [1, 2, 3]:
        # Market Depth (Bids/Asks)
        ax1.scatter(df_m['step'], df_m[f'bid_price_{i}'], s=df_m[f'bid_volume_{i}']*10,
                    color='green', alpha=0.15, edgecolors='none')
        ax1.scatter(df_m['step'], df_m[f'ask_price_{i}'], s=df_m[f'ask_volume_{i}']*10,
                    color='red', alpha=0.15, edgecolors='none')

    # Others' Trades
    if not others_trades.empty:
        ax1.scatter(others_trades['step'], others_trades['price'],
                    color='black', s=40, marker='x', label="Market Trades", alpha=0.3)

    # MY BUYS (Lime Star)
    if not my_buys.empty:
        ax1.scatter(my_buys['step'], my_buys['price'],
                    color='lime', s=160, marker='*', label="MY BUYS",
                    edgecolors='black', linewidth=1, zorder=10)

    # MY SELLS (Orange Star)
    if not my_sells.empty:
        ax1.scatter(my_sells['step'], my_sells['price'],
                    color='orange', s=160, marker='*', label="MY SELLS",
                    edgecolors='black', linewidth=1, zorder=10)

    # Axis Limits & Formatting
    p_min = df_m['bid_price_1'].min() - 5
    p_max = df_m['ask_price_1'].max() + 5
    ax1.set_ylim(p_min, p_max)
    ax1.set_ylabel("Price")
    ax1.set_title(f"Market Microstructure & My Executions: {product}")
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle=':', alpha=0.5)

    # --- MIDDLE PANEL: PnL ---
    ax2.plot(df_m['step'], df_m['profit_and_loss'], color='blue', linewidth=2)
    ax2.fill_between(df_m['step'], df_m['profit_and_loss'], color='blue', alpha=0.1)
    ax2.set_ylabel("PnL (Shells)")
    ax2.set_title("Cumulative PnL")
    ax2.grid(True, linestyle='--', alpha=0.3)

    # --- BOTTOM PANEL: Market Trend ---
    ax3.plot(df_m['step'], df_m['mid_price'], color='gray', linestyle='--', alpha=0.5)
    ax3.set_ylabel("Mid Price Reference")
    ax3.set_xlabel("Time Step (100ms)")
    ax3.set_title("Market Trend Reference")
    ax3.grid(True, linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.show()

analyze_performance_v2(LOG_FILE, PRODUCT, START_STEP, END_STEP)