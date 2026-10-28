
import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import comb


def require(test, detail):
    if not test:
        raise AssertionError(detail)


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def power(a, n):
    out = [1]
    for _ in range(n):
        out = multiply(out, a)
    return out


def analytic_bounds():
    v, p = F(7, 9), F(22, 7)
    z = p / 13
    require(p * (z - z**3 / 6 + z**5 / 120) / (1 - z*z / 2) < v,
            "pi tan(pi/13) < 7/9")
    require(1 + (v*v/2) / (1 - v*v/12) == F(1217, 923) < F(4, 3),
            "cosh(7/9) < 4/3")
    require(1 + (v/3)**2 < F(21, 20)**2, "pole-radius bound")
    require(F(21, 20)**4 / 54 < F(1, 40), "pole-tail bound")
    require((2*110 - 11)//104 == 2 and 29*2 >= 57,
            "grouping threshold")
    print("PASS: all rational analytic bounds")


def direct_block(s, j):
    # (2+3t+2t^2)^(8-j) (2+4t+2t^2)^j (1+t^2)^s
    r = 8 - j
    a = [sum(comb(r, ell) * comb(r-ell, k-2*ell)
             * 2**(r-k+2*ell) * 3**(k-2*ell)
             for ell in range(max(0, k-r), k//2+1))
         for k in range(2*r+1)]
    b = [2**j * comb(2*j, k) for k in range(2*j+1)]
    base = [sum(a[h] * b[k-h] for h in range(len(a))
                if 0 <= k-h < len(b)) for k in range(17)]
    return [sum(comb(s, ell) * base[k-2*ell]
                for ell in range(max(0, (k-15)//2), min(s, k//2)+1))
            for k in range(2*(8+s)+1)]


def block_checks(independent=False):
    rows = [multiply(power([2, 3, 2], 8-j), power([2, 4, 2], j))
            for j in range(9)]
    count, equalities, digest = 0, [], sha256()
    for s in range(74):
        if independent:
            rows = [direct_block(s, j) for j in range(9)]
        for j, row in enumerate(rows):
            require(len(row) == 2*(8+s)+1 and row == row[::-1],
                    ("block degree and symmetry", s, j))
            for k in range(1, 8+s+1):
                value = row[k]**2 - row[k-1]*row[k+1]
                require(value >= 0, ("block", s, j, k, value))
                if value == 0:
                    equalities.append((s, j, k))
                digest.update(f"{s},{j},{k}:{value}\n".encode())
                count += 1
        if not independent:
            rows = [multiply(row, [1, 0, 1]) for row in rows]
    require(count == 29637 and equalities == [(73, 0, 1)],
            ("block count and equalities", count, equalities))
    print(f"PASS: {count} endpoint inequalities; equalities: {equalities}")
    print("Endpoint SHA-256:", digest.hexdigest())
    return digest.hexdigest()


def finite_rows():
    row, factorial, count = [1], 1, 0
    equalities, digest = [], sha256()
    expected = {1: [1], 2: [1, 1], 3: [2, 2, 2], 4: [5, 7, 7, 5],
                5: [16, 26, 36, 26, 16],
                6: [61, 117, 182, 182, 117, 61]}
    for n in range(1, 221):
        factorial *= n
        require(len(row) == n and row == row[::-1] and
                all(x > 0 for x in row) and sum(row) == factorial,
                ("row invariants", n))
        if n in expected:
            require(row == expected[n], ("initial row", n))
        for k in range(1, (n+1)//2):
            value = row[k]**2 - row[k-1]*row[k+1]
            require(value >= 0, ("row", n, k, value))
            if value == 0:
                equalities.append((n, k))
            count += 1
        digest.update((str(n) + ":" + ",".join(map(str, row)) + "\n").encode())
        if n < 220:
            old = [0, 0] + row + [0, 0]
            numerators = [(k+1)*(old[k+3] + old[k+1]) +
                          (n-k+1)*(old[k+2] + old[k]) for k in range(n+1)]
            require(all(x % 2 == 0 for x in numerators), ("division", n))
            row = [x//2 for x in numerators]
    require(count == 11990 and equalities == [(3, 1)],
            ("row count and equalities", count, equalities))
    print(f"PASS: all n <= 220; {count} row inequalities; equalities: {equalities}")
    print("Rows SHA-256:", digest.hexdigest())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--independent", action="store_true")
    args = parser.parse_args()
    analytic_bounds()
    block_checks(args.independent)
    finite_rows()
    print("ALL EXACT CHECKS PASSED")
