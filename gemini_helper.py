import json
import json as json_lib  # Ensure it's imported
import google.generativeai as genai

def _fallback_plan(question: str) -> dict:
    q = question.lower()
    plan = {
        "query_type": "group_by",
        "group_col": "category",
        "agg_col": ["views"],
        "agg_func": "sum",
        "sort_desc": True,
        "chart_hint": "bar",
        "title": "Data Analysis",
        "description": "Rule-based generated chart.",
        "x_label": "Category",
        "y_label": "Total Views"
    }
    
    # ── Very basic rule engine fallback ─────────────────────────────────────
    if "trend" in q or "over time" in q:
        plan.update({
            "query_type": "time_series", "group_col": "month",
            "chart_hint": "line", "title": "Views Trend Over Time",
            "x_label": "Month"
        })
    elif "top" in q:
        import re
        m = re.search(r"top\s+(\d+)", q)
        top_n = int(m.group(1)) if m else 10
        plan.update({
            "group_col": "video_id", "top_n": top_n,
            "chart_hint": "horizontal_bar", "title": f"Top {top_n} Videos",
            "x_label": "Total Views", "y_label": "Video"
        })
    elif "region" in q:
        plan.update({
            "group_col": "region", "title": "Views by Region",
            "x_label": "Region"
        })
    elif "language" in q:
        plan.update({
            "group_col": "language", "title": "Views by Language",
            "x_label": "Language"
        })
    elif "sentiment" in q:
        plan.update({
            "agg_col": ["sentiment_score"], "agg_func": "mean",
            "title": "Average Sentiment Score", "y_label": "Sentiment Score"
        })
    elif "engagement" in q:
        plan.update({
            "agg_col": ["engagement"],
            "title": "Engagement Metrics", "y_label": "Total Engagement"
        })
    elif "compare likes and comments" in q:
        plan.update({
            "agg_col": ["likes", "comments"],
            "title": "Likes vs Comments", "y_label": "Count"
        })

    if "region" in q and "sentiment" in q:
        plan["group_col"] = "region"
        plan["x_label"] = "Region"

    return plan


def generate_query_plan(question: str, api_key: str = "") -> dict:
    """
    Generate a JSON plan to chart the requested query.
    If no API key evaluates true, fallback to the rule engine.
    """
    if not api_key:
        return _fallback_plan(question)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Create structured prompt
        prompt = f"""
        You are a smart data assistant generating JSON query plans.

        Available columns in 'dataset.csv':
         - category, language, region, video_id, timestamp, date, month, year
         - views, likes, comments, shares, duration_sec, sentiment_score, engagement

        Convert formatting into a strict, valid JSON object with the following schema:
        {{
            "query_type": "time_series" | "group_by" | "distribution" | "correlation",
            "group_col": string (e.g. "region", "month", null if n/a),
            "agg_col": [string, string...] (e.g. ["views"], ["likes", "comments"]),
            "agg_func": "sum" | "mean" | "count",
            "sort_desc": boolean,
            "top_n": integer or null,
            "chart_hint": "bar" | "line" | "horizontal_bar" | "pie" | "scatter",
            "title": string,
            "description": string (short blurb),
            "x_label": string,
            "y_label": string
        }}

        Do NOT wrap in markdown code blocks, just return exact JSON text.
        
        Question: "{question}"
        """

        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        return json_lib.loads(text)

    except Exception as e:
        print(f"AI Parse Error: {e}")
        return _fallback_plan(question)
