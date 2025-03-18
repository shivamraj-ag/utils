#!~/anaconda3/bin/python
import sys
import numpy as np
import pandas as pd

def compute_stats(numbers):
    if len(numbers) == 0:
        print("No numbers received.")
        return
    
    mean = np.mean(numbers)
    median = np.median(numbers)
    stddev = np.std(numbers, ddof=1)
    
    percentiles = {
        "1%": np.percentile(numbers, 1),
        "5%": np.percentile(numbers, 5),
        "25%": np.percentile(numbers, 25),
        "50%": np.percentile(numbers, 50),
        "75%": np.percentile(numbers, 75),
        "90%": np.percentile(numbers, 90),
        "99%": np.percentile(numbers, 99)
    }
    
    min_val = np.min(numbers)
    max_val = np.max(numbers)
    
    sharpe_ratio = mean / stddev if stddev != 0 else float('nan')
    
    data = {
        "Statistic": ["Mean", "Median", "StdDev", "1%", "5%", "25%", "50%", "75%", "90%", "99%", "Min", "Max", "Sharpe"],
        "Value": [mean, median, stddev] + list(percentiles.values()) + [min_val, max_val, sharpe_ratio]
    }
    
    df = pd.DataFrame(data)
    print(df.to_string(index=False))

def main():
    numbers = []
    for line in sys.stdin:
        try:
            numbers.append(float(line.strip()))
        except ValueError:
            continue
    compute_stats(numbers)

if __name__ == "__main__":
    main()
