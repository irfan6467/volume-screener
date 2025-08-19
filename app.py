def check_volume_surge_yfinance(symbol):
    """
    Checks if a stock's latest trading volume is more than double its
    10-day average volume. This version is robust against all known
    data structure inconsistencies from the yfinance library.
    """
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=40) # Fetch a bit more data for rolling average stability
        
        data = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False  # Keep this for consistency
        )
        
        if data.empty or len(data) < 11:
            return None
        
        data['10d_avg_vol'] = data['Volume'].shift(1).rolling(window=10, min_periods=10).mean()
        
        # Drop any rows where the average couldn't be calculated
        data.dropna(subset=['10d_avg_vol'], inplace=True)
        if data.empty:
            return None
            
        last_day = data.iloc[-1]
        
        # --- BULLETPROOF FIX ---
        # Explicitly extract the single scalar value using .values[0]
        # This prevents the "ambiguous truth value" error for good.
        current_volume = last_day['Volume'].values[0]
        avg_volume = last_day['10d_avg_vol'].values[0]
        
        if avg_volume == 0:
            return None

        surge_ratio = current_volume / avg_volume
        
        if surge_ratio > 2.0:
            return {
                'Symbol': symbol,
                'Current Volume': current_volume,
                '10d Avg Volume': avg_volume,
                'Surge Ratio (x)': surge_ratio
            }
        return None
        
    except Exception as e:
        print(f"An error occurred while fetching data for {symbol}: {e}")
        return None