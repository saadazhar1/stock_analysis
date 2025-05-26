# S&P 500 Historical Analysis

This Python script analyzes the historical performance of the S&P 500 index over the last 100 years, focusing on yearly returns and their distribution across different thresholds.

## Features

- Fetches 100 years of S&P 500 historical data
- Analyzes yearly returns with three categories:
  - Down years (negative returns)
  - No return period (0-6% returns)
  - Good returns (>6%)
- Creates visualizations:
  - Yearly returns waterfall chart
  - Returns distribution pie chart
  - Rolling returns analysis for 5, 10, 15, and 20-year periods

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script from the src directory:
```bash
python sp500_improved_analysis.py
```

The script will:
1. Fetch historical S&P 500 data
2. Display analysis of yearly returns
3. Show multiple visualizations
4. Print statistics about different return periods

## Output

The script generates:
- Detailed statistics about yearly returns
- A waterfall chart showing all yearly returns color-coded by category
- A pie chart showing the distribution of returns
