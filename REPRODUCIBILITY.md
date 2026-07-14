# Reproducibility

## Requirements

- Python 3.10 or newer
- `mpmath`
- `pdflatex` for rebuilding the paper

Install the Python dependency with:

```bash
python -m pip install mpmath
```

## Run the numerical verification

From the repository root:

```bash
python scripts/verify_ellipse_scaling_law.py --precision 80 --outdir output
```

Expected verdict:

```text
cases_passed: 4/4
verification_passed: True
```

The command writes:

```text
output/ellipse_scaling_verification.csv
output/ellipse_scaling_summary.txt
```

## Rebuild the paper

From the repository root:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory paper paper/universal_scaling_law_ellipse_perimeters.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory paper paper/universal_scaling_law_ellipse_perimeters.tex
```

## Numerical reference

The exact ellipse perimeter is evaluated as

\[
P=4a\,E\!\left(1-\frac{b^2}{a^2}\right),
\]

using `mpmath.ellipe` in its parameter convention. Polygonal perimeters are
computed independently from the exact chord-midpoint identity proved in the
paper.
