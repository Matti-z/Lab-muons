#!/usr/bin/env python3
"""Generate a CSV with two columns:
- first: integers from 0 to 15
- label: integers from 0 to 6

This writes all combinations (16 x 7 = 112 rows) to reorder_columns.csv in the
same directory.
"""
import csv
from itertools import product
from pathlib import Path
import numpy as np

OUT = Path(__file__).with_name("unif.csv")

def main():
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["first"] + list(np.round(30/6*np.array(range(1, 7)) -  , 2)))
        for first in range(1, 16):
            writer.writerow([np.round(80/15*first - 2.5 , 2)] + [0] * 7)

if __name__ == "__main__":
    main()
