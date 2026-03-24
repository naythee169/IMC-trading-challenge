import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data using the semicolon separator
prices = pd.read_csv('TUTORIAL_ROUND_1/prices_round_0_day_-2.csv', sep=';')
trades = pd.read_csv('TUTORIAL_ROUND_1/trades_round_0_day_-2.csv', sep=';')

def display_market(product_name, start_step=0, end_step=50):
    # 1. Filter and prepare Price data
    df = prices[prices['product'] == product_name].copy()
    df['step'] = df['timestamp'] // 100
    df_range = df[(df['step'] >= start_step) & (df['step'] <= end_step)]

    # 2. Filter and prepare Trade data (symbol is usually the key in trades)
    t_df = trades[trades['symbol'] == product_name].copy()
    t_df['step'] = t_df['timestamp'] // 100
    t_df_range = t_df[(t_df['step'] >= start_step) & (t_df['step'] <= end_step)]

    plt.figure(figsize=(15, 7))

    # 3. Plot Order Book Depth (Bids in Green, Asks in Red)
    for level in [1, 2, 3]:
        plt.scatter(df_range['step'], df_range[f'bid_price_{level}'],
                    s=df_range[f'bid_volume_{level}'] * 5,
                    color='green', alpha=0.5, label=f'Bid L{level}' if level==1 else "")
        plt.scatter(df_range['step'], df_range[f'ask_price_{level}'],
                    s=df_range[f'ask_volume_{level}'] * 5,
                    color='red', alpha=0.5, label=f'Ask L{level}' if level==1 else "")

    # 4. NEW: Plot actual trades as black dots
    if not t_df_range.empty:
        plt.scatter(t_df_range['step'], t_df_range['price'],
                    color='black', s=30, label='Actual Trades', zorder=10)

    # Formatting
    plt.title(f'Order Book Depth + Trades: {product_name} (Steps {start_step} to {end_step})')
    plt.xlabel('Time Step (1 step = 100ms)')
    plt.ylabel('Price')

    # Optional: Shrink Y-axis for Emeralds consistency
    if product_name == 'EMERALDS':
        plt.ylim(9990, 10010)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.show()

# Create plots for both products
display_market('EMERALDS')
#display_market('TOMATOES')

'''
# 1. Load the datasets
# Note: we use sep=';' because these specific files use semicolons instead of commas
prices_df = pd.read_csv('TUTORIAL_ROUND_1/prices_round_0_day_-1.csv', sep=';')
trades_df = pd.read_csv('TUTORIAL_ROUND_1/trades_round_0_day_-1.csv', sep=';')

# 2. Filter the Prices DataFrame
emeralds_prices = prices_df[prices_df['product'] == 'EMERALDS']
tomatoes_prices = prices_df[prices_df['product'] == 'TOMATOES']

# 3. Filter the Trades DataFrame
emeralds_trades = trades_df[trades_df['symbol'] == 'EMERALDS']
tomatoes_trades = trades_df[trades_df['symbol'] == 'TOMATOES']

# Save Emeralds data
emeralds_prices.to_csv('emeralds_prices.csv', index=False)
emeralds_trades.to_csv('emeralds_trades.csv', index=False)

# Save Tomatoes data
tomatoes_prices.to_csv('tomatoes_prices.csv', index=False)
tomatoes_trades.to_csv('tomatoes_trades.csv', index=False)

# --- Optional: Display the first few rows to verify ---
print("First 5 rows of Emerald Prices:")
print(emeralds_prices.head())

print("\nFirst 5 rows of Tomato Trades:")
print(tomatoes_trades.head())

# --- Optional: Save these to separate files for easier backtesting ---
# emeralds_prices.to_csv('emeralds_only_prices.csv', index=False)
'''