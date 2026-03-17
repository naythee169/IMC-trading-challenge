import json
import pandas as pd
import io

def format_prosperity_log_corrected(file_path):
    # 1. Load the raw log file
    with open(file_path, 'r') as f:
        log_data = json.load(f)

    # 2. Process Market Activities (Semicolon separated string)
    activities_str = log_data.get("activitiesLog", "")
    activities_df = pd.read_csv(io.StringIO(activities_str), sep=';')

    # 3. Process Trades (In your file, this is under 'tradeHistory')
    # Use 'tradeHistory' as the key to fix the empty file issue
    trades_list = log_data.get("tradeHistory", [])
    trades_df = pd.DataFrame(trades_list)

    # 4. Save to nice formats
    activities_df.to_csv("formatted_activities.csv", index=False)
    trades_df.to_csv("formatted_trades.csv", index=False)

    print("Extraction Complete!")
    print(f"Market Activities saved: {len(activities_df)} rows")
    print(f"Trades extracted: {len(trades_df)} rows")

# Run the corrected formatter
format_prosperity_log_corrected('2389.log')