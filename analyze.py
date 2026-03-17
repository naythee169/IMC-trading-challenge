import pandas as pd

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