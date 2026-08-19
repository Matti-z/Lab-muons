#!/usr/bin/env python3
"""Convert Geant4 CSV result files to chunked HDF5 files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import h5py
import numpy as np


DEFAULT_ROOTS = (
    Path(__file__).parent / "results" / "gmp",
    Path(__file__).parent / "results" / "mgp",
)
CHUNK_SIZE = 10_000


def _infer_value(value: str) -> tuple[Any, np.dtype[Any]]:
    if value in {"True", "False"}:
        return value == "True", np.dtype("bool")
    try:
        return int(value), np.dtype("int64")
    except ValueError:
        try:
            return float(value), np.dtype("float64")
        except ValueError:
            return value, h5py.string_dtype(encoding="utf-8")


def _column_types(csv_path: Path, fieldnames: list[str]) -> dict[str, np.dtype[Any]]:
    types: dict[str, np.dtype[Any]] = {}
    with csv_path.open(newline="") as source:
        reader = csv.DictReader(source)
        for row in reader:
            for fieldname in fieldnames:
                value = row[fieldname]
                if value == "":
                    types[fieldname] = h5py.string_dtype(encoding="utf-8")
                    continue
                _, value_type = _infer_value(value)
                if fieldname not in types:
                    types[fieldname] = value_type
                elif types[fieldname].kind in "iu" and value_type.kind == "f":
                    types[fieldname] = np.dtype("float64")
                elif types[fieldname].kind == "f" and value_type.kind in "iu":
                    pass
                elif types[fieldname].kind != value_type.kind:
                    types[fieldname] = h5py.string_dtype(encoding="utf-8")
    return {
        fieldname: types.get(fieldname, h5py.string_dtype(encoding="utf-8"))
        for fieldname in fieldnames
    }


def convert_file(csv_path: Path, overwrite: bool = False) -> Path | None:
    """Convert one CSV file and return its output path, or None if skipped."""
    h5_path = csv_path.with_suffix(".h5")
    if h5_path.exists() and not overwrite:
        return None

    with csv_path.open(newline="") as source:
        reader = csv.DictReader(source)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError(f"CSV file has no header: {csv_path}")

    types = _column_types(csv_path, fieldnames)
    with h5py.File(h5_path, "w") as output:
        group = output.create_group("data")
        datasets = {
            fieldname: group.create_dataset(
                fieldname,
                shape=(0,),
                maxshape=(None,),
                dtype=types[fieldname],
                chunks=True,
            )
            for fieldname in fieldnames
        }
        with csv_path.open(newline="") as source:
            reader = csv.DictReader(source)
            chunk = {fieldname: [] for fieldname in fieldnames}
            row_count = 0
            for row in reader:
                for fieldname in fieldnames:
                    value = row[fieldname]
                    if types[fieldname].kind == "b":
                        chunk[fieldname].append(value == "True")
                    elif types[fieldname].kind in "iu":
                        chunk[fieldname].append(int(value))
                    elif types[fieldname].kind == "f":
                        chunk[fieldname].append(float(value))
                    else:
                        chunk[fieldname].append(value)
                row_count += 1
                if row_count % CHUNK_SIZE == 0:
                    _append_chunk(datasets, chunk, row_count - len(chunk[fieldnames[0]]))
                    chunk = {fieldname: [] for fieldname in fieldnames}
            _append_chunk(datasets, chunk, row_count - len(chunk[fieldnames[0]]))
        output.attrs["columns"] = np.array(fieldnames, dtype=h5py.string_dtype())
    return h5_path


def _append_chunk(datasets: dict[str, h5py.Dataset], chunk: dict[str, list[Any]], start: int) -> None:
    size = len(next(iter(chunk.values())))
    if size == 0:
        return
    for fieldname, dataset in datasets.items():
        dataset.resize((start + size,))
        dataset[start : start + size] = chunk[fieldname]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "roots",
        nargs="*",
        type=Path,
        default=DEFAULT_ROOTS,
        help="Result directories to search (default: gmp and mgp).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace HDF5 files that already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List conversions without creating files.",
    )
    args = parser.parse_args()

    converted = 0
    skipped = 0
    for root in args.roots:
        csv_files = sorted(root.rglob("*.csv"))
        if not csv_files:
            print(f"No CSV files found in {root}")
        for csv_path in csv_files:
            h5_path = csv_path.with_suffix(".h5")
            if args.dry_run:
                print(f"{csv_path} -> {h5_path}")
                continue

            result = convert_file(csv_path, overwrite=args.overwrite)
            if result is None:
                skipped += 1
                print(f"Skipped {csv_path} (output exists)")
            else:
                converted += 1
                print(f"Converted {csv_path} -> {result}")

    if not args.dry_run:
        print(f"Done: {converted} converted, {skipped} skipped.")


if __name__ == "__main__":
    main()