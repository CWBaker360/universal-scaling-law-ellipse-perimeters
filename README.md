# A Universal Scaling Law for Ellipse Perimeters

**Author:** Wayne Baker  
**Original date:** February 2026  
**Revised:** July 14, 2026  
**Status:** Revised preprint / source and reproducibility archive

This repository contains the rigorous revised paper:

> **A Universal Scaling Law for Ellipse Perimeters**

## Read the paper

- [`paper/universal_scaling_law_ellipse_perimeters.pdf`](paper/universal_scaling_law_ellipse_perimeters.pdf)
- [`paper/universal_scaling_law_ellipse_perimeters.tex`](paper/universal_scaling_law_ellipse_perimeters.tex)

## Main result

For the ellipse

\[
\mathbf q(\theta)=(a\cos\theta,b\sin\theta),
\qquad a\ge b>0,
\]

let \(P_N\) be the inscribed polygonal perimeter obtained from \(N\) equal
increments of the ellipse parameter. The exact factorization is

\[
P_N
=
\operatorname{sinc}\!\left(\frac{\pi}{N}\right)M_N,
\]

where \(M_N\) is the composite midpoint rule applied to the ellipse speed.

For every fixed nondegenerate ellipse,

\[
P_N
=
P\,\operatorname{sinc}\!\left(\frac{\pi}{N}\right)
+
O(e^{-\rho N}),
\qquad
0<\rho<\operatorname{artanh}(b/a).
\]

Therefore,

\[
P-P_N
=
P\left(
\frac{\pi^2}{6N^2}
-
\frac{\pi^4}{120N^4}
+
\frac{\pi^6}{5040N^6}
-\cdots
\right)
+
O(e^{-\rho N}).
\]

The algebraic relative-error coefficients are universal: they do not depend
on the ellipse axes.

## Tripling correction

The one-step N-series estimator

\[
\widehat P_N
=
P_{3N}
+
\frac{P_{3N}-P_N}{8}
\]

satisfies

\[
P-\widehat P_N
=
\frac{P\pi^4}{1080N^4}
+
O(N^{-6})
+
O(e^{-\rho N}).
\]

## Eccentricity dependence

Eccentricity affects the onset of the asymptotic regime through the analytic
strip width

\[
\rho_*=\operatorname{artanh}(b/a).
\]

For \(b/a\ll1\), \(\rho_*\sim b/a\), so resolving the exponential quadrature
remainder requires \(N\) of order \(a/b\), up to a
tolerance-dependent logarithmic factor.

## Numerical verification

Run from the repository root:

```bash
python scripts/verify_ellipse_scaling_law.py --precision 80 --outdir output
```

The script verifies:

- the exact polygon-midpoint factorization;
- convergence of \(N^2(P-P_N)/P\) to \(\pi^2/6\);
- convergence of \(N^4(P-\widehat P_N)/P\) to \(\pi^4/1080\);
- four axis ratios from \(b/a=0.90\) to \(b/a=0.01\).

## Claim boundary

The theorem concerns nondegenerate ellipses and equal increments of the
standard ellipse parameter. It does not assert the same sinc factorization
for arbitrary curves, parameterizations, or meshes.

## Related repositories

- [`scaling-cancellation-principle`](https://github.com/CWBaker360/scaling-cancellation-principle)
- [`nseries-pi-acceleration`](https://github.com/CWBaker360/nseries-pi-acceleration)
- [`ramanujan-landen-nseries-refinement`](https://github.com/CWBaker360/ramanujan-landen-nseries-refinement)

## Repository structure

```text
.
├── README.md
├── CITATION.cff
├── REPRODUCIBILITY.md
├── LICENSE_NOTICE.md
├── CHANGELOG.md
├── SHA256SUMS.txt
├── .gitignore
├── paper/
│   ├── universal_scaling_law_ellipse_perimeters.tex
│   ├── universal_scaling_law_ellipse_perimeters.pdf
│   └── README.md
├── scripts/
│   ├── verify_ellipse_scaling_law.py
│   └── README.md
├── output/
│   ├── ellipse_scaling_verification.csv
│   ├── ellipse_scaling_summary.txt
│   └── README.md
└── docs/
    ├── abstract.md
    ├── claim_boundary.md
    ├── main_result.md
    ├── repository_description.md
    ├── source_assessment.md
    └── github_upload_checklist.md
```

## Licensing

Copyright © 2026 C. Wayne Baker.

- The manuscript, LaTeX source, README, documentation, and non-code research materials are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).
- The verification software in `scripts/` is licensed separately under the MIT License; see `scripts/LICENSE`.

CC BY 4.0 requires appropriate attribution and indication of changes. The MIT License requires preservation of its copyright and permission notice.
