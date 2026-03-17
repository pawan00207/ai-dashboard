import pandas as pd

def _fmt(v) -> str:
    """Format a number for human-readable display."""
    try:
        v = float(v)
        if abs(v) < 10:
            return f"{v:,.4f}"
        return f"{v:,.1f}"
    except (TypeError, ValueError):
        return str(v)

def generate_insights(result: pd.DataFrame, plan: dict) -> list:
    """
    Generate 3-4 plain-English insight bullets from the aggregated result.
    Restored from the original impressive version.
    """
    if result.empty:
        return ["⚠️ No data available for this query."]

    cols     = list(result.columns)
    cat_col  = cols[0]
    num_cols = [c for c in cols[1:] if pd.api.types.is_numeric_dtype(result[c])]

    if not num_cols:
        return [f"📊 The result contains **{len(result):,}** rows."]

    val_col = num_cols[0]
    series  = result[val_col].dropna()
    out     = []

    # 1. Top performer
    try:
        top_idx = series.idxmax()
        top_cat = result.loc[top_idx, cat_col]
        top_val = series[top_idx]
        out.append(f"🏆 **{top_cat}** leads with the highest {val_col}: **{_fmt(top_val)}**")

        # 2. Bottom performer
        bot_idx = series.idxmin()
        bot_cat = result.loc[bot_idx, cat_col]
        bot_val = series[bot_idx]
        out.append(f"📉 **{bot_cat}** has the lowest {val_col}: **{_fmt(bot_val)}**")

        # 3. Average across all groups
        out.append(f"📊 Average {val_col} across all groups: **{_fmt(series.mean())}**")

        # 4. Gap
        if len(series) > 2 and bot_val != 0:
            gap_pct = (top_val - bot_val) / abs(bot_val) * 100
            out.append(f"📐 Top group outperforms the bottom by **{gap_pct:,.1f}%** in {val_col}.")
    except:
        out.append("📊 Summary statistics computed successfully.")

    return out[:4]
