
# Log-concavity for Alternating Eulerian Polynomials

This repository contains the exact verification code accompanying the paper "Log-concavity for alternating Eulerian polynomials" by Lijie Wang and Sainan Zheng.

## Requirements

Python 3 (standard library only).

No additional packages are required. All computations use exact integer or rational arithmetic.

## Usage

Run the verification script:

    python3 verify_log_concavity.py

For an independent verification of the block coefficients:

    python3 verify_log_concavity.py --independent

## Verification Results

The program verifies the following results:

1. Proposition 4.1:
   - All 29,637 log-concavity inequalities are verified.
   - Equality occurs only at (s, j, k) = (73, 0, 1).

2. The finite verification for Theorem 1.3:
   - Log-concavity is verified for all 1 <= n <= 220.
   - A total of 11,990 exact comparisons are performed.
   - Equality occurs only at (n, k) = (3, 1).

The program also checks rational bounds used in the strong-factor estimates and the grouping argument.

## Successful Execution

A successful run ends with:

    ALL EXACT CHECKS PASSED

The program reports SHA-256 checksums to facilitate reproducibility.
