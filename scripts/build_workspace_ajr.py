"""Execute the real AJR example and build the landing-page notebook preview.

Run with a Python environment containing pandas, pyfixest, matplotlib, and pygments.
Data: the repository's 64-country AED_INSTITUTIONS.DTA (Chapter 13).
"""
from pathlib import Path
import base64
import contextlib
import hashlib
import importlib.metadata
import io
import json
import os
import re
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "metricsai-ajr-matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = Path(__file__).resolve().parents[1]
DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/metricsai/main/data/AED_INSTITUTIONS.DTA"

SETUP = f'''import pandas as pd
import pyfixest as pf
import matplotlib.pyplot as plt

df = pd.read_stata("{DATA_URL}")
df = df.dropna(subset=["logpgp95", "avexpr", "logem4"])
plt.rcParams.update({{
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#334155", "xtick.color": "#475569",
    "ytick.color": "#475569", "axes.edgecolor": "#94a3b8",
    "figure.facecolor": "white", "axes.facecolor": "white",
}})'''

ESTIMATION = '''iv = pf.feols(
    "logpgp95 ~ 1 | avexpr ~ logem4",
    data=df, vcov="HC1"
)
iv.summary()'''

PLOT = '''first = pf.feols("avexpr ~ logem4", data=df)
fig, ax = plt.subplots(figsize=(7, 3.6))
for r in df.itertuples():
    ax.text(r.logem4, r.avexpr, r.shortnam,
            fontsize=7, ha="center", va="center")
ordered = df.sort_values("logem4")
ax.plot(ordered.logem4, first.predict(ordered), color="#008CB7")
ax.set(xlim=(1.5, 8), ylim=(2, 10), xlabel="Log settler mortality",
       ylabel="Protection against expropriation (1985–95)")
fig.tight_layout()
plt.show()'''


def main():
    import numpy as np
    import matplotlib.pyplot as plt
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import PythonLexer

    namespace = {}
    # Use identical tracked bytes locally; the delivered Colab cell loads the same file.
    setup_local = SETUP.replace(DATA_URL, str(ROOT / "data/AED_INSTITUTIONS.DTA"))
    exec(setup_local, namespace)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(ESTIMATION, namespace)
        exec(PLOT, namespace)
    df, first, iv, fig = [namespace[key] for key in ("df", "first", "iv", "fig")]

    # Independent matrix calculations validate both the first stage and 2SLS.
    z = np.column_stack([np.ones(len(df)), df.logem4])
    x = np.column_stack([np.ones(len(df)), df.avexpr])
    y = df.logpgp95.to_numpy()
    xhat = z @ np.linalg.lstsq(z, x, rcond=None)[0]
    expected_iv = np.linalg.solve(xhat.T @ x, xhat.T @ y)[1]
    expected_first = np.linalg.lstsq(z, df.avexpr.to_numpy(), rcond=None)[0][1]
    assert len(df) == 64
    assert np.isclose(iv.coef()["avexpr"], expected_iv, atol=1e-10)
    assert np.isclose(first.coef()["logem4"], expected_first, atol=1e-10)
    assert len(fig.axes[0].texts) == 64
    ordered = df.sort_values("logem4")
    assert np.allclose(fig.axes[0].lines[0].get_ydata(), first.predict(ordered))

    image = ROOT / "images/workspace-ajr-first-stage.png"
    fig.savefig(image, dpi=200)
    svg = image.with_suffix(".svg")
    fig.savefig(svg, metadata={"Date": None})
    plt.close(fig)

    result = {
        "source": "Acemoglu, Johnson, Robinson (2001); Chapter 13 AED_INSTITUTIONS.DTA",
        "source_url": "https://economics.mit.edu/people/faculty/daron-acemoglu/data-archive",
        "data_sha256": hashlib.sha256((ROOT / "data/AED_INSTITUTIONS.DTA").read_bytes()).hexdigest(),
        "n": len(df), "first_stage_slope": float(first.coef()["logem4"]),
        "iv_institutions_coefficient": float(iv.coef()["avexpr"]),
        "iv_hc1_se": float(iv.se()["avexpr"]),
        "iv_formula": "logpgp95 ~ 1 | avexpr ~ logem4",
        "versions": {pkg: importlib.metadata.version(pkg) for pkg in ("pyfixest", "pandas", "matplotlib")},
    }
    image.with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")

    def cell(source, count, outputs=None):
        return {"cell_type": "code", "execution_count": count, "metadata": {},
                "source": source.splitlines(keepends=True), "outputs": outputs or []}

    notebook = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}, "colab": {"name": "ajr_institutions_iv.ipynb"}},
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [
                "# Institutions and development: AJR (2001)\n",
                "Baseline 2SLS on the 64-country sample used in metricsAI Chapter 13.\n",
                "Instrument: log settler mortality (`logem4`); endogenous regressor: protection against expropriation (`avexpr`); outcome: log GDP per capita in 1995 (`logpgp95`). No additional controls.\n\n",
                "The first-stage graphic is generated below with Matplotlib, using country labels in the paper's style. The IV estimate uses PyFixest with HC1 standard errors.\n\n",
                "Sources: [AJR data archive](https://economics.mit.edu/people/faculty/daron-acemoglu/data-archive), [PyFixest IV documentation](https://pyfixest.org/tutorials/formula-syntax.html).\n",
                "Causal interpretation requires the instrument's relevance and exclusion assumptions.\n"]},
            cell("%pip -q install pyfixest==" + result["versions"]["pyfixest"], None),
            cell(SETUP, 1),
            cell(ESTIMATION, 2, [{"output_type": "stream", "name": "stdout", "text": stdout.getvalue().splitlines(keepends=True)}]),
            cell(PLOT, 3, [{"output_type": "display_data", "metadata": {}, "data": {
                "image/png": base64.b64encode(image.read_bytes()).decode(), "text/plain": ["AJR first-stage plot, 64 countries"]}}]),
        ],
    }
    for i, notebook_cell in enumerate(notebook["cells"]):
        notebook_cell["id"] = f"ajr-cell-{i}"
    (ROOT / "notebooks_colab/ajr_institutions_iv.ipynb").write_text(json.dumps(notebook, indent=1) + "\n")

    # The preview contains exactly the code executed above, never a separate mock example.
    index = ROOT / "index.html"
    html = index.read_text()
    for name, code in (("ajr-estimation-code", ESTIMATION), ("ajr-plot-code", PLOT)):
        markup = highlight(code, PythonLexer(), HtmlFormatter(nowrap=True)).rstrip()
        html, replacements = re.subn(r'(<code id="' + name + r'">).*?(</code>)',
                                     lambda m: m[1] + markup + m[2], html, flags=re.S)
        assert replacements == 1, f"Missing preview code block {name}"
    label = f"IV β̂ = {result['iv_institutions_coefficient']:.3f} · SE (HC1) = {result['iv_hc1_se']:.3f} · n = {len(df)}"
    html, replacements = re.subn(r'(<span id="ajr-result">).*?(</span>)',
                                 lambda m: m[1] + label + m[2], html, flags=re.S)
    assert replacements == 1
    index.write_text(html)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
