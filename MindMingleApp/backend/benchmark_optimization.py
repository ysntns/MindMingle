import pandas as pd
import time
import os
import sys

def load_data():
    # Adjust path relative to this script
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'netflix.csv')
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        print(f"Data file not found at {data_path}")
        return None

def filter_contents_baseline(data, mood):
    """
    Original implementation of filter_contents logic (before optimization).
    """
    if data is None:
        return pd.DataFrame()

    filtered_data = pd.DataFrame()
    # case insensitive search and handle NaN
    if mood == "Çok Mutlu" or mood == "Mutlu":
        filtered_data = data[data['listed_in'].str.contains("Comedy", na=False) | data['listed_in'].str.contains("Animation", na=False)]
    elif mood == "Üzgün":
        filtered_data = data[data['listed_in'].str.contains("Drama", na=False) | data['listed_in'].str.contains("Romantic", na=False) | data['listed_in'].str.contains("Comedy", na=False)]
    elif mood == "Keyifli":
        filtered_data = data[data['listed_in'].str.contains("Family", na=False) | data['listed_in'].str.contains("Documentary", na=False) | data['listed_in'].str.contains("Animation", na=False)]
    elif mood == "Melankolik":
        filtered_data = data[
            data['listed_in'].str.contains("Art House", na=False) | data['listed_in'].str.contains("Independent", na=False) | data['listed_in'].str.contains("Drama", na=False)]

    return filtered_data

def filter_contents_optimized(data, mood):
    """
    Optimized implementation using regex for single-pass filtering.
    Matches the updated implementation in main.py.
    """
    if data is None:
        return pd.DataFrame()

    filtered_data = pd.DataFrame()
    # case insensitive search and handle NaN
    if mood == "Çok Mutlu" or mood == "Mutlu":
        # Comedy|Animation
        filtered_data = data[data['listed_in'].str.contains("Comedy|Animation", na=False, regex=True)]
    elif mood == "Üzgün":
        # Drama|Romantic|Comedy
        filtered_data = data[data['listed_in'].str.contains("Drama|Romantic|Comedy", na=False, regex=True)]
    elif mood == "Keyifli":
        # Family|Documentary|Animation
        filtered_data = data[data['listed_in'].str.contains("Family|Documentary|Animation", na=False, regex=True)]
    elif mood == "Melankolik":
        # Art House|Independent|Drama
        filtered_data = data[data['listed_in'].str.contains("Art House|Independent|Drama", na=False, regex=True)]

    return filtered_data

def run_benchmark():
    data = load_data()
    if data is None:
        return

    moods = ["Mutlu", "Üzgün", "Keyifli", "Melankolik"]
    iterations = 100

    print(f"Benchmarking with {len(data)} rows over {iterations} iterations per mood.")

    for mood in moods:
        print(f"\n--- Mood: {mood} ---")

        # Verify correctness
        res_base = filter_contents_baseline(data, mood)
        res_opt = filter_contents_optimized(data, mood)

        if len(res_base) != len(res_opt):
            print(f"FAILED: Result length mismatch! Baseline: {len(res_base)}, Optimized: {len(res_opt)}")
            return

        # Also check if indices match
        if not res_base.index.equals(res_opt.index):
             print(f"FAILED: Indices mismatch!")
             return

        print(f"Correctness passed. Result count: {len(res_base)}")

        # Measure Baseline
        start_time = time.perf_counter()
        for _ in range(iterations):
            filter_contents_baseline(data, mood)
        end_time = time.perf_counter()
        avg_base = (end_time - start_time) / iterations
        print(f"Baseline Avg Time: {avg_base:.6f} s")

        # Measure Optimized
        start_time = time.perf_counter()
        for _ in range(iterations):
            filter_contents_optimized(data, mood)
        end_time = time.perf_counter()
        avg_opt = (end_time - start_time) / iterations
        print(f"Optimized Avg Time: {avg_opt:.6f} s")

        if avg_opt > 0:
            speedup = avg_base / avg_opt
            print(f"Speedup: {speedup:.2f}x")
        else:
             print("Speedup: N/A")

if __name__ == "__main__":
    run_benchmark()
