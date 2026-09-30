#!/usr/bin/env python3
"""Verify the ellipse sinc-scaling and tripling-cancellation laws."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import mpmath as mp


def exact_perimeter(a: mp.mpf, b: mp.mpf) -> mp.mpf:
    """Exact ellipse perimeter, with mpmath's parameter convention E(m)."""
    if not (a >= b > 0):
        raise ValueError("Expected a >= b > 0")
    parameter = 1 - (b / a) ** 2
    return 4 * a * mp.ellipe(parameter)


def midpoint_speed_sum(a: mp.mpf, b: mp.mpf, n: int) -> mp.mpf:
    """Composite midpoint approximation to the perimeter integral."""
    if n < 3:
        raise ValueError("n must be at least 3")
    h = 2 * mp.pi / n
    total = mp.mpf("0")
    for j in range(n):
        t = (mp.mpf(j) + mp.mpf("0.5")) * h
        speed = mp.sqrt(a * a * mp.sin(t) ** 2 + b * b * mp.cos(t) ** 2)
        total += speed
    return h * total


def polygon_perimeter(a: mp.mpf, b: mp.mpf, n: int) -> mp.mpf:
    """Direct equal-parameter inscribed polygonal perimeter.

    The perimeter is computed independently from successive ellipse vertices,
    rather than from the sinc factorization that the verification is testing.
    """
    if n < 3:
        raise ValueError("n must be at least 3")

    h = 2 * mp.pi / n
    total = mp.mpf("0")
    for j in range(n):
        t0 = mp.mpf(j) * h
        t1 = mp.mpf(j + 1) * h

        x0 = a * mp.cos(t0)
        y0 = b * mp.sin(t0)
        x1 = a * mp.cos(t1)
        y1 = b * mp.sin(t1)

        dx = x1 - x0
        dy = y1 - y0
        total += mp.sqrt(dx * dx + dy * dy)

    return total


def corrected_perimeter(a: mp.mpf, b: mp.mpf, n: int) -> mp.mpf:
    """Tripling-based cancellation of the inverse-square term."""
    p_n = polygon_perimeter(a, b, n)
    p_3n = polygon_perimeter(a, b, 3 * n)
    return (9 * p_3n - p_n) / 8


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=80)
    parser.add_argument("--outdir", type=Path, default=Path("output"))
    args = parser.parse_args()

    if args.precision < 50:
        raise ValueError("precision must be at least 50 decimal digits")

    mp.mp.dps = args.precision
    cases = [
        (mp.mpf("0.90"), 162),
        (mp.mpf("0.50"), 486),
        (mp.mpf("0.10"), 1458),
        (mp.mpf("0.01"), 13122),
    ]

    raw_limit = mp.pi**2 / 6
    corrected_limit = mp.pi**4 / 1080

    rows: list[dict[str, str | int]] = []
    all_pass = True

    for ratio, n in cases:
        a = mp.mpf("1")
        b = ratio
        exact = exact_perimeter(a, b)
        midpoint = midpoint_speed_sum(a, b, n)
        polygon = polygon_perimeter(a, b, n)
        corrected = corrected_perimeter(a, b, n)

        sinc_factor = mp.sin(mp.pi / n) / (mp.pi / n)
        factorization_residual = abs(polygon - sinc_factor * midpoint)

        raw_relative = (exact - polygon) / exact
        corrected_relative = (exact - corrected) / exact
        raw_scaled = n**2 * raw_relative
        corrected_scaled = n**4 * corrected_relative
        rho_star = mp.atanh(ratio)

        raw_ok = abs(raw_scaled - raw_limit) < mp.mpf("5e-5")
        corrected_ok = abs(corrected_scaled - corrected_limit) < mp.mpf("2e-6")
        factorization_ok = factorization_residual < mp.power(10, -(args.precision - 15))
        case_pass = raw_ok and corrected_ok and factorization_ok
        all_pass = all_pass and case_pass

        rows.append(
            {
                "axis_ratio_b_over_a": mp.nstr(ratio, 12),
                "N": n,
                "rho_star": mp.nstr(rho_star, 30),
                "N_rho_star": mp.nstr(n * rho_star, 20),
                "exact_perimeter": mp.nstr(exact, 40),
                "polygon_perimeter": mp.nstr(polygon, 40),
                "corrected_perimeter": mp.nstr(corrected, 40),
                "raw_relative_error": mp.nstr(raw_relative, 30),
                "corrected_relative_error": mp.nstr(corrected_relative, 30),
                "N2_raw_relative_error": mp.nstr(raw_scaled, 30),
                "N4_corrected_relative_error": mp.nstr(corrected_scaled, 30),
                "factorization_residual": mp.nstr(factorization_residual, 12),
                "case_pass": str(case_pass),
            }
        )

    args.outdir.mkdir(parents=True, exist_ok=True)
    csv_path = args.outdir / "ellipse_scaling_verification.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = [
        "Universal ellipse scaling-law verification",
        f"precision_dps: {args.precision}",
        f"raw_limit_pi2_over_6: {mp.nstr(raw_limit, 40)}",
        f"corrected_limit_pi4_over_1080: {mp.nstr(corrected_limit, 40)}",
        f"cases_passed: {sum(row['case_pass'] == 'True' for row in rows)}/{len(rows)}",
        f"verification_passed: {all_pass}",
    ]
    summary_path = args.outdir / "ellipse_scaling_summary.txt"
    summary_path.write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))

    if not all_pass:
        raise SystemExit("verification thresholds were not met")


if __name__ == "__main__":
    main()
