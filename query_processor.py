import pandas as pd

def execute_plan(df: pd.DataFrame, plan: dict) -> pd.DataFrame:
    """
    Run the pandas operations described by *plan* against *df*.

    Returns
    -------
    pd.DataFrame  - aggregated result ready to be charted.
    """
    query_type = plan.get("query_type", "group_by")
    group_col  = plan.get("group_col")
    agg_col    = plan.get("agg_col", "views")
    agg_func   = plan.get("agg_func", "sum")
    sort_desc  = plan.get("sort_desc", True)
    top_n      = plan.get("top_n")

    # Normalise agg_col -> always a list internally
    if isinstance(agg_col, str):
        agg_cols = [agg_col]
    else:
        agg_cols = list(agg_col) if agg_col else ["views"]

    # Keep only columns that actually exist in df
    valid_agg = [c for c in agg_cols if c in df.columns]
    if not valid_agg:
        valid_agg = ["views"]

    # -- Time series --------------------------------------------------------
    if query_type == "time_series":
        time_col = group_col if group_col in df.columns else "month"
        result = (
            df.groupby(time_col)[valid_agg]
            .agg(agg_func)
            .reset_index()
        )
        # Convert Period to string so Plotly can handle it
        result[time_col] = result[time_col].astype(str)
        result = result.sort_values(time_col)
        return result

    # -- Group-by / top-N --------------------------------------------------
    if group_col and group_col in df.columns:
        result = (
            df.groupby(group_col)[valid_agg]
            .agg(agg_func)
            .reset_index()
            .sort_values(valid_agg[0], ascending=not sort_desc)
        )
        if top_n:
            result = result.head(int(top_n))
        return result

    # -- Distribution: value_counts on a column ----------------------------
    if query_type == "distribution":
        col = valid_agg[0]
        result = df[col].value_counts().reset_index()
        result.columns = [col, "count"]
        if top_n:
            result = result.head(int(top_n))
        return result

    # -- Correlation: return two numeric columns ---------------------------
    if query_type == "correlation" and len(valid_agg) >= 2:
        return df[valid_agg].dropna().head(5000)   # limit points for speed

    # -- Default: raw sample -----------------------------------------------
    return df[list(df.columns[:8])].head(50)
