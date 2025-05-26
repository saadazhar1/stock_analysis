import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from matplotlib.patches import Patch

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configure plot settings
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def fetch_sp500_data(start_date, end_date):
    """Fetch S&P 500 data for the last 100 years."""
    end_date = end_date
    start_date = start_date  # 100 years of data
    sp500 = yf.download('^GSPC', start=start_date, end=end_date)
    return sp500

def get_return_category(return_value):
    """Helper function to categorize returns."""
    return_value = float(return_value)  # Convert numpy.float64 to float
    if return_value < 0:
        return "Down Year"
    elif return_value < 6:
        return "No Return"
    else:
        return "Good Return"

def analyze_yearly_returns(data):
    """Calculate and analyze yearly returns with mutually exclusive categories."""
    # Calculate yearly returns using year-end values
    yearly_data = data['Close'].resample('YE').last()
    yearly_returns = yearly_data.pct_change()
    
    # Remove any NaN values
    yearly_returns = yearly_returns.dropna()
    
    # Convert returns to percentages for easier comparison
    returns_pct = yearly_returns * 100
    
    # Create mutually exclusive categories using boolean masks
    down_mask = returns_pct < 0
    no_return_mask = (returns_pct >= 0) & (returns_pct < 6)
    good_return_mask = returns_pct >= 6
    
    # Apply masks to get the returns in each category
    down_years = returns_pct[down_mask]
    no_return_years = returns_pct[no_return_mask]
    good_return_years = returns_pct[good_return_mask]

    # Remove any NaN values
    down_years = down_years.dropna()
    # Remove any NaN values
    no_return_years = no_return_years.dropna()
    # Remove any NaN values
    good_return_years = good_return_years.dropna()
    
    # Calculate total positive return years
    total_positive_years = len(no_return_years) + len(good_return_years)
    
    # Verification of total years
    total_years = len(returns_pct)
    total_categorized = len(down_years) + len(no_return_years) + len(good_return_years)
    
    # Debug information
    print("\nYearly Returns Analysis:")
    print(f"Total years analyzed: {total_years}")
    print(f"Years categorized: {total_categorized}")  # Should equal total_years
    print(f"\nBreakdown:")
    print(f"Down Years (<0%): {len(down_years)} ({len(down_years)/total_years*100:.1f}%)")
    print(f"No Return Years (0-6%): {len(no_return_years)} ({len(no_return_years)/total_years*100:.1f}%)")
    print(f"Good Return Years (>6%): {len(good_return_years)} ({len(good_return_years)/total_years*100:.1f}%)")
    print(f"\nTotal Positive Years (>0%): {total_positive_years} ({total_positive_years/total_years*100:.1f}%)")
    
    # Verification check
    if total_categorized != total_years:
        print("\nWARNING: Category total doesn't match total years!")
        print(f"Difference: {total_years - total_categorized} years")
    
    # Print first few years for verification
    print("\nFirst 5 years of data for verification:")
    first_five = returns_pct.head()
    for date, value in zip(first_five.index, first_five.values):
        category = get_return_category(value)
        print(f"{date.strftime('%Y')}: {float(value):.2f}% - Category: {category}")
    
    # Print last few years for verification
    print("\nLast 5 years of data for verification:")
    last_five = returns_pct.tail()
    for date, value in zip(last_five.index, last_five.values):
        category = get_return_category(value)
        print(f"{date.strftime('%Y')}: {float(value):.2f}% - Category: {category}")
    
    return returns_pct, down_years, no_return_years, good_return_years

def plot_yearly_returns_waterfall(yearly_returns):
    """Create a waterfall chart of yearly returns."""
    plt.figure(figsize=(20, 10))
    
    # Convert returns to list of floats for plotting
    returns_pct = [float(x) for x in yearly_returns.values]
    years = [x.strftime('%Y') for x in yearly_returns.index]
    
    # Create bar chart with three categories
    colors = []
    for ret in returns_pct:
        if ret < 0:
            colors.append('red')  # Down years
        elif ret < 6:
            colors.append('yellow')  # No return period (0-6%)
        else:
            colors.append('green')  # Good return (>6%)
    
    bars = plt.bar(range(len(returns_pct)), returns_pct, color=colors)
    
    plt.title('S&P 500 Yearly Returns (Last 100 Years)', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Return (%)', fontsize=12)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.2)
    plt.axhline(y=6, color='black', linestyle='--', alpha=0.2, label='6% Threshold')
    
    # Add legend
    legend_elements = [
        Patch(facecolor='green', label='Good Return (>6%)'),
        Patch(facecolor='yellow', label='No Return (0-6%)'),
        Patch(facecolor='red', label='Down Year (<0%)')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    # Set x-axis labels to years (showing every 5th year for readability)
    plt.xticks(range(0, len(years), 5), years[::5], rotation=45)
    
    # Add value labels on top of each bar
    for i, v in enumerate(returns_pct):
        if abs(v) > 3:  # Only show labels for returns > 3% to avoid clutter
            plt.text(i, v + (1 if v >= 0 else -1), 
                    f'{v:.1f}%', 
                    ha='center', va='bottom' if v >= 0 else 'top',
                    fontsize=8)
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_returns_distribution(yearly_returns, down_years, no_return_years, good_return_years):
    """Create a pie chart showing the distribution of returns."""
    plt.figure(figsize=(12, 6))
    
    # Calculate percentages
    total_years = len(yearly_returns)
    categories = [
        'Down Years (<0%)',
        'No Return (0-6%)',
        'Good Return (>6%)'
    ]
    values = [
        len(down_years),
        len(no_return_years),
        len(good_return_years)
    ]
    colors = ['red', 'yellow', 'green']
    
    plt.pie(values, labels=categories, colors=colors, 
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct*total_years/100)} years)')
    plt.title('S&P 500 Returns Distribution (Last 100 Years)')
    plt.show()

def analyze_rolling_returns(data):
    """Analyze and plot rolling returns for different periods."""
    # Calculate rolling returns
    periods = [5, 10, 15, 20]
    rolling_returns = {}
    
    for period in periods:
        rolling_return = (data['Close'].rolling(window=period*252)
                        .apply(lambda x: (x.iloc[-1]/x.iloc[0])**(1/period) - 1))
        rolling_returns[period] = rolling_return
    
    # Plot rolling returns with improved styling
    plt.figure(figsize=(15, 8))
    
    # Plot the returns
    for period in periods:
        plt.plot(rolling_returns[period] * 100,
                 label=f'{period}-Year Rolling Return',
                 linewidth=2)
    
    # Add 6% threshold line
    plt.axhline(y=6, color='r', linestyle='--', alpha=0.5, label='6% Threshold')
    
    plt.title('S&P 500: Rolling Returns and No-Return Threshold')
    plt.xlabel('Date')
    plt.ylabel('Annualized Return (%)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Print statistics about periods below 6% return
    # print("\nPeriods Below 6% Return:")
    for period in periods:
        below_threshold = rolling_returns[period][rolling_returns[period] < 0.06]
        pct_below = len(below_threshold) / len(rolling_returns[period].dropna()) * 100
        # print(f"{period}-Year Rolling Returns: {pct_below:.1f}% of time below 6% threshold")

def main():
    # Fetch data
    print("Fetching S&P 500 historical data...")

    start_date = '1926-01-01'
    end_date = '2025-01-01'
    print(f"Fetching data from {start_date} to {end_date}")
    sp500_data = fetch_sp500_data(start_date, end_date)
    
    # Analyze yearly returns
    yearly_returns, down_years, no_return_years, good_return_years = analyze_yearly_returns(sp500_data)
    
    # Plot yearly returns waterfall chart
    plot_yearly_returns_waterfall(yearly_returns)
    
    # Plot returns distribution
    plot_returns_distribution(yearly_returns, down_years, no_return_years, good_return_years)
    
    # Analyze and plot rolling returns
    analyze_rolling_returns(sp500_data)

if __name__ == "__main__":
    main() 