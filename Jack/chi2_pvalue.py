"""Compute p-value from chi-squared statistic.

Usage:
  python chi2_pvalue.py 10.5 8

Provides `compute_pvalue(chi2_obs, dof)` returning the survival probability.
"""
from __future__ import annotations
import sys

def compute_pvalue(chi2_obs: float, dof: int) -> float:
    """Return p-value = P(chi2_dof >= chi2_obs).

    Tries to use SciPy (`scipy.stats.chi2.sf`). If SciPy is not available,
    attempts to use `scipy.special.gammaincc` (also SciPy). If neither is
    available, raises ImportError with a short message.
    """
    try:
        from scipy.stats import chi2
        return float(chi2.sf(chi2_obs, dof))
    except Exception:
        try:
            from scipy.special import gammaincc
            return float(gammaincc(dof / 2.0, chi2_obs / 2.0))
        except Exception:
            raise ImportError(
                "SciPy is required to compute the p-value. Install with: pip install scipy"
            )


def _main():
    import argparse

    p = argparse.ArgumentParser(description="Compute p-value from chi-squared.")
    p.add_argument("chi2", type=float, help="Observed chi-squared value")
    p.add_argument("dof", type=int, help="Degrees of freedom")
    args = p.parse_args()
    try:
        pval = compute_pvalue(args.chi2, args.dof)
    except ImportError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    print(f"chi2={args.chi2}, dof={args.dof} -> p-value={pval:.6g}")


if __name__ == "__main__":
    _main()
