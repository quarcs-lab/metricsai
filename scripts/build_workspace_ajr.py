"""Build the real AJR IV / Plotly Express preview and its Colab notebook.

Run with pandas, numpy, pyfixest, plotly, statsmodels, pygments and playwright.
The landing page uses a static SVG; Plotly is needed only when building it.
"""
from pathlib import Path
import base64
import contextlib
import hashlib
import importlib.metadata
import inspect
import io
import json
import re
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/metricsai/main/data/AED_INSTITUTIONS.DTA"
SETUP = f'''import pandas as pd
import pyfixest as pf
import plotly.express as px

df = pd.read_stata("{DATA_URL}")
df = df.dropna(subset=["logpgp95", "avexpr", "logem4"])'''
ESTIMATION = '''iv = pf.feols(
    "logpgp95 ~ 1 | avexpr ~ logem4",
    data=df, vcov="HC1"
)
iv.summary()'''
PLOT = '''import plotly.express as px
fig = px.scatter(
    df, x="logem4", y="avexpr",
    hover_name="shortnam",
    trendline="ols", template="plotly_dark"
)
fig.show()'''


def style_figure(fig, df):
    """Presentation styling, separate from the short teaching example."""
    fig.update_layout(
        width=800, height=650, showlegend=False,
        paper_bgcolor="#101b2d", plot_bgcolor="#101b2d",
        font=dict(family="Arial, sans-serif", size=21, color="#b0bed0"),
        margin=dict(l=85, r=20, t=32, b=85),
        xaxis=dict(title="Log settler mortality", range=[1.5, 8.2], dtick=2,
                   gridcolor="#25364d", zeroline=False, title_standoff=18),
        yaxis=dict(title="Institutional protection", range=[2, 10.8], dtick=2,
                   gridcolor="#25364d", zeroline=False, title_standoff=12),
    )
    fig.update_traces(marker=dict(size=13, color="#62c7da", opacity=.8,
                      line=dict(color="#101b2d", width=1.5)), selector=dict(mode="markers"))
    fig.update_traces(line=dict(color="#d8b4fe", width=3), selector=dict(mode="lines"))
    offsets = {"AUS": (8, -22), "CAN": (33, -3), "USA": (10, 24),
               "NZL": (-32, 12), "BRA": (0, -25), "IND": (26, 0),
               "GMB": (0, -24), "MLI": (-24, 0)}
    for country, (dx, dy) in offsets.items():
        row = df.loc[df.shortnam == country].iloc[0]
        fig.add_annotation(x=float(row.logem4), y=float(row.avexpr), text=country,
                           showarrow=False, xshift=dx, yshift=dy,
                           font=dict(size=20, color="#e2e8f0"))


def main():
    import numpy as np
    import plotly.express as px
    from playwright.sync_api import sync_playwright
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import PythonLexer

    namespace = {}
    exec(SETUP.replace(DATA_URL, str(ROOT / "data/AED_INSTITUTIONS.DTA")), namespace)
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(ESTIMATION, namespace)
    exec(PLOT.replace("fig.show()", ""), namespace)
    df, iv, fig = [namespace[key] for key in ("df", "iv", "fig")]
    z = np.column_stack([np.ones(len(df)), df.logem4])
    x = np.column_stack([np.ones(len(df)), df.avexpr])
    y = df.logpgp95.to_numpy()
    xhat = z @ np.linalg.lstsq(z, x, rcond=None)[0]
    expected_iv = np.linalg.solve(xhat.T @ x, xhat.T @ y)[1]
    expected_first = np.linalg.lstsq(z, df.avexpr.to_numpy(), rcond=None)[0]
    trend = px.get_trendline_results(fig).px_fit_results.iloc[0]
    assert len(df) == 64
    assert np.isclose(iv.coef()["avexpr"], expected_iv, atol=1e-10)
    assert np.allclose(trend.params, expected_first, atol=1e-10)
    assert len(fig.data[0].x) == 64
    assert np.allclose(fig.data[1].y,
                       expected_first[0] + expected_first[1] * fig.data[1].x)
    style_figure(fig, df)

    prefix = ROOT / "images/workspace-ajr-first-stage-v2"
    (ROOT / "SCRATCH").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "SCRATCH") as tmp:
        chart_path = Path(tmp) / "chart.html"
        fig.write_html(chart_path, include_plotlyjs=True, div_id="ajr-chart",
                       config=dict(staticPlot=True, displayModeBar=False))
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport=dict(width=850, height=700))
            page.goto(chart_path.as_uri())
            page.wait_for_function("document.getElementById('ajr-chart')._fullLayout !== undefined")
            uri = page.evaluate("Plotly.toImage('ajr-chart', {format:'svg', width:800, height:650})")
            prefix.with_suffix(".svg").write_text(unquote(uri.split(",", 1)[1]))
            uri = page.evaluate("Plotly.toImage('ajr-chart', {format:'png', width:800, height:650, scale:2})")
            prefix.with_suffix(".png").write_bytes(base64.b64decode(uri.split(",", 1)[1]))
            browser.close()

    result = {
        "source": "Acemoglu, Johnson, Robinson (2001); Chapter 13 AED_INSTITUTIONS.DTA",
        "source_url": "https://economics.mit.edu/people/faculty/daron-acemoglu/data-archive",
        "data_sha256": hashlib.sha256((ROOT / "data/AED_INSTITUTIONS.DTA").read_bytes()).hexdigest(),
        "n": len(df), "first_stage_slope": float(trend.params[1]),
        "iv_institutions_coefficient": float(iv.coef()["avexpr"]),
        "iv_hc1_se": float(iv.se()["avexpr"]),
        "iv_formula": "logpgp95 ~ 1 | avexpr ~ logem4", "plot_code": PLOT,
        "versions": {pkg: importlib.metadata.version(pkg)
                     for pkg in ("pyfixest", "pandas", "plotly", "statsmodels")},
    }
    prefix.with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")

    def cell(source, count, outputs=None):
        return {"cell_type": "code", "execution_count": count, "metadata": {},
                "source": source.splitlines(keepends=True), "outputs": outputs or []}

    styling = inspect.getsource(style_figure) + "\nstyle_figure(fig, df)\nfig.show()"
    notebook = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}, "colab": {"name": "ajr_institutions_iv.ipynb"}},
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [
                "# Institutions and development: AJR (2001)\n",
                "Baseline 2SLS on the 64-country sample used in metricsAI Chapter 13.\n",
                "Instrument: log settler mortality (`logem4`); endogenous regressor: protection against expropriation (`avexpr`); outcome: log GDP per capita in 1995 (`logpgp95`). No additional controls.\n\n",
                "PyFixest estimates IV with HC1 standard errors. Plotly Express draws the first-stage scatter and OLS fit in one call. The final optional styling cell reproduces the website preview.\n\n",
                "Sources: [AJR data archive](https://economics.mit.edu/people/faculty/daron-acemoglu/data-archive), [PyFixest IV documentation](https://pyfixest.org/tutorials/formula-syntax.html), [Plotly Express trendlines](https://plotly.com/python/linear-fits/).\n",
                "Causal interpretation requires the instrument's relevance and exclusion assumptions.\n"]},
            cell("%pip -q install " + " ".join(pkg + "==" + result["versions"][pkg]
                                             for pkg in ("pyfixest", "plotly", "statsmodels")), None),
            cell(SETUP, 1),
            cell(ESTIMATION, 2, [{"output_type": "stream", "name": "stdout", "text": stdout.getvalue().splitlines(keepends=True)}]),
            cell(PLOT, 3),
            cell(styling, 4, [{"output_type": "display_data", "metadata": {}, "data": {
                "image/png": base64.b64encode(prefix.with_suffix(".png").read_bytes()).decode(),
                "text/plain": ["AJR first-stage scatter and OLS fit, 64 countries"]}}]),
        ],
    }
    for i, notebook_cell in enumerate(notebook["cells"]):
        notebook_cell["id"] = f"ajr-cell-{i}"
    (ROOT / "notebooks_colab/ajr_institutions_iv.ipynb").write_text(json.dumps(notebook, indent=1) + "\n")

    index = ROOT / "index.html"
    html = index.read_text()
    for name, code in (("ajr-estimation-code", ESTIMATION), ("ajr-plot-code", PLOT)):
        markup = highlight(code, PythonLexer(), HtmlFormatter(nowrap=True)).rstrip()
        html, replacements = re.subn(r'(<code id="' + name + r'">).*?(</code>)',
                                     lambda m: m[1] + markup + m[2], html, flags=re.S)
        assert replacements == 1, f"Missing preview code block {name}"
    label = f"IV β̂ = {result['iv_institutions_coefficient']:.3f} · SE = {result['iv_hc1_se']:.3f} · n = {len(df)}"
    html, replacements = re.subn(r'(<span id="ajr-result">).*?(</span>)',
                                 lambda m: m[1] + label + m[2], html, flags=re.S)
    assert replacements == 1
    index.write_text(html)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
