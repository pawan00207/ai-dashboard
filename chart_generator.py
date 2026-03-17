import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Design tokens (exact match to original impressive version)
# ---------------------------------------------------------------------------
COLORS = [
    "#E63946", "#F4A261", "#2A9D8F", "#457B9D",
    "#A8DADC", "#F1FAEE", "#264653", "#E9C46A",
    "#6A0572", "#118AB2",
]
TEMPLATE = "plotly_dark"

def generate_chart(result: pd.DataFrame, plan: dict) -> go.Figure:
    """
    Choose and construct the best Plotly figure for *result*.
    Restores the original styling with JetBrains Mono and YouTube-red accents.
    """
    hint    = plan.get("chart_hint", "bar")
    title   = plan.get("title",   "Chart")
    x_label = plan.get("x_label", "")
    y_label = plan.get("y_label", "")

    cols = list(result.columns)
    if not cols:
        return _empty("Result has no columns.")

    # x = first column
    x_col = cols[0]

    # y = first numeric column after x
    num_cols = [c for c in cols[1:] if pd.api.types.is_numeric_dtype(result[c])]
    y_col = num_cols[0] if num_cols else None

    if y_col is None:
        return _empty("No numeric column to plot.")

    # -- Route to chart builders --------------------------------------------
    if hint == "line":
        fig = _line(result, x_col, y_col, x_label, y_label)
    elif hint == "horizontal_bar":
        fig = _hbar(result, x_col, y_col, x_label, y_label)
    elif hint == "pie":
        fig = _pie(result, x_col, y_col)
    elif hint == "scatter" and len(num_cols) >= 2:
        fig = _scatter(result, num_cols[0], num_cols[1], x_label, y_label)
    else:
        fig = _bar(result, x_col, y_col, x_label, y_label)

    # -- Layout polish -------------------------------------------------------
    fig.update_layout(
        template=TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="'JetBrains Mono', 'Courier New', monospace",
                  color="#D1D5DB", size=12),
        title=dict(text=title, font=dict(size=18, color="#E63946"), x=0.02),
        margin=dict(l=40, r=20, t=56, b=48),
        showlegend=False,
    )
    return fig

# ---------------------------------------------------------------------------
# Individual builders (restored from original)
# ---------------------------------------------------------------------------

def _bar(df, x, y, xl, yl):
    fig = px.bar(df, x=x, y=y, color=x, color_discrete_sequence=COLORS,
                 labels={x: xl or x, y: yl or y})
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return fig

def _hbar(df, x, y, xl, yl):
    sorted_df = df.sort_values(y, ascending=True)
    fig = px.bar(sorted_df, x=y, y=x, orientation="h", color=y,
                 color_continuous_scale=["#1a1a2e", "#E63946"],
                 labels={y: xl or y, x: yl or x})
    fig.update_coloraxes(showscale=False)
    fig.update_traces(marker_line_width=0)
    return fig

def _line(df, x, y, xl, yl):
    fig = px.line(df, x=x, y=y, markers=True, color_discrete_sequence=["#E63946"],
                  labels={x: xl or x, y: yl or y})
    fig.update_traces(line_width=2.5, marker_size=6)
    fig.add_traces(px.area(df, x=x, y=y, color_discrete_sequence=["rgba(230, 57, 70, 0.2)"]).data)
    return fig

def _pie(df, names, values):
    fig = px.pie(df, names=names, values=values, color_discrete_sequence=COLORS, hole=0.38)
    fig.update_traces(textposition="inside", textinfo="percent+label", pull=[0.03] * len(df))
    return fig

def _scatter(df, x, y, xl, yl):
    fig = px.scatter(df, x=x, y=y, opacity=0.55, color_discrete_sequence=["#E63946"],
                     labels={x: xl or x, y: yl or y}, trendline="ols", trendline_color_override="#F4A261")
    fig.update_traces(marker_size=5)
    return fig

def _empty(msg: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                       font=dict(size=15, color="#E63946"))
    return fig
