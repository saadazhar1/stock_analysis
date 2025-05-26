import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

def analyze_stock(ticker, start_date, end_date):
    """
    Analyze weekly performance of a stock.
    
    Args:
        ticker (str): Stock ticker symbol
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
    """
    try:
        print(f"\nAnalyzing {ticker}...")
        
        # Download data
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"No data found for {ticker}")
            return None
            
        # Convert index to datetime and remove duplicates
        data.index = pd.to_datetime(data.index)
        data = data[~data.index.duplicated(keep='last')]
        
        # Calculate weekly returns
        weekly = data['Close'].resample('W-FRI').last()
        weekly_pct_change = weekly.pct_change().dropna()
        
        # Convert to numpy array for comparison
        pct_change_values = weekly_pct_change.to_numpy()
        
        # Separate up and down weeks
        up_weeks = pct_change_values[pct_change_values > 0]
        down_weeks = pct_change_values[pct_change_values < 0]
        
        # Get current price and calculate YTD change
        current_price = data['Close'].iloc[-1]
        initial_price = data['Close'].iloc[0]
        ytd_change = ((current_price / initial_price) - 1) * 100
        
        # Calculate statistics
        stats = {
            'Ticker': ticker,
            'Total Weeks': len(pct_change_values),
            'Up Weeks': len(up_weeks),
            'Down Weeks': len(down_weeks),
            'Average Up Week Change (%)': round(np.mean(up_weeks) * 100, 2) if len(up_weeks) > 0 else 0,
            'Average Down Week Change (%)': round(np.mean(down_weeks) * 100, 2) if len(down_weeks) > 0 else 0,
            'Current Price': round(current_price.item(), 2),
            'YTD Change (%)': round(ytd_change.item(), 2)
        }
        
        # Print statistics
        print("\nStatistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        try:
            # Create visualization
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Create bar plot data
            weeks = weekly_pct_change.index.strftime('%Y-%m-%d')
            x_pos = np.arange(len(weeks))
            values = pct_change_values * 100
            
            # Plot bars
            for i, (x, val) in enumerate(zip(x_pos, values)):
                color = 'green' if val > 0 else 'red'
                ax.bar(x, val, color=color)
            
            # Customize the plot
            ax.set_title(f'{ticker} Weekly Returns ({start_date} to {end_date})', fontsize=12, pad=15)
            ax.set_xlabel('Week', fontsize=10)
            ax.set_ylabel('Return (%)', fontsize=10)
            ax.grid(True, alpha=0.3)
            
            # Format x-axis
            if len(weeks) > 20:
                # If more than 20 weeks, show every 4th date
                ax.set_xticks(x_pos[::4])
                ax.set_xticklabels(weeks[::4], rotation=45, ha='right')
            else:
                ax.set_xticks(x_pos)
                ax.set_xticklabels(weeks, rotation=45, ha='right')
            
            # Add horizontal line at y=0
            ax.axhline(y=0, color='black', linestyle='-', alpha=0.2)
            
            # Add legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='green', label='Up'),
                Patch(facecolor='red', label='Down')
            ]
            ax.legend(handles=legend_elements)
            
            # Adjust layout
            plt.tight_layout()
            plt.show()
            
        except Exception as plot_error:
            print(f"Error creating plot: {plot_error}")
            import traceback
            print(traceback.format_exc())
        
        return stats
    
    except Exception as e:
        print(f"Error analyzing {ticker}: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

def main():
    # Set up the plot style
    plt.style.use('default')
    sns.set_style("whitegrid")
    
    # Define analysis parameters
    tickers = ['TSLA', 'PLTR', 'MSFT']
    start_date = '2024-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Analyze each stock
    results = []
    for ticker in tickers:
        stats = analyze_stock(ticker, start_date, end_date)
        if stats is not None:
            results.append(stats)
    
    # Create summary DataFrame
    if results:
        results_df = pd.DataFrame(results)
        print("\nSummary of All Stocks:")
        pd.set_option('display.float_format', '{:.2f}'.format)
        print(results_df.set_index('Ticker'))
    else:
        print("\nNo valid results to display.")

if __name__ == "__main__":
    main() 