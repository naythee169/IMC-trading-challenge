import json
import pandas as pd

def extract_my_trades(log_filename, output_csv='my_trades.csv'):
    # 1. Load the JSON log file
    with open(log_filename, 'r') as f:
        log_data = json.load(f)

    # 2. Extract trade history and convert to a DataFrame
    trade_history = log_data.get('tradeHistory', [])
    if not trade_history:
        print("No trades found in the log.")
        return

    df_trades = pd.DataFrame(trade_history)

    # 3. Filter for your trades (where 'buyer' or 'seller' is 'SUBMISSION')
    my_trades = df_trades[(df_trades['buyer'] == 'SUBMISSION') |
                          (df_trades['seller'] == 'SUBMISSION')].copy()

    my_trades =  my_trades[my_trades['symbol'] == 'TOMATOES']

    # 4. Add a 'side' column to easily see if you bought or sold
    my_trades['side'] = my_trades.apply(
        lambda x: 'BUY' if x['buyer'] == 'SUBMISSION' else 'SELL', axis=1
    )

    # 5. Reorder columns for better readability
    cols = ['timestamp', 'symbol', 'side', 'price', 'quantity', 'buyer', 'seller']
    my_trades = my_trades[cols]

    # 6. Save to CSV
    my_trades.to_csv(output_csv, index=False)
    print(f"Successfully extracted {len(my_trades)} trades to {output_csv}")

# Example usage
extract_my_trades('11131.log')