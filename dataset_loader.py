import pandas as pd
import streamlit as st

@st.cache_data
def load_data(source="dataset.csv"):
    """
    Load and cache the CSV dataset for the dashboard.
    Accepts a file path (str) or a Streamlit UploadedFile object.
    """
    try:
        df = pd.read_csv(source)
        # Derive columns as per original app
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            df['month'] = df['timestamp'].dt.to_period('M').astype(str)
            df['year'] = df['timestamp'].dt.year
            
        if 'likes' in df.columns and 'comments' in df.columns and 'shares' in df.columns:
            df['engagement'] = df['likes'] + df['comments'] + df['shares']
            
        return df
    except FileNotFoundError:
        st.error(f"Dataset not found at {source}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

def dataset_summary(df):
    """
    Returns summary statistics for the sidebar.
    """
    if df.empty:
        return {}
        
    summary = {
        "Rows": f"{len(df):,}",
    }
    
    if "views" in df.columns:
        summary["Total Views"] = f"{df['views'].sum():,}"
    if "category" in df.columns:
        summary["Categories"] = f"{df['category'].nunique()}"
    if "language" in df.columns:
        summary["Languages"] = f"{df['language'].nunique()}"
    if "region" in df.columns:
        summary["Regions"] = f"{df['region'].nunique()}"
        
    # Date range
    if "date" in df.columns:
        min_date = df['date'].min()
        max_date = df['date'].max()
        summary["Date Range"] = f"{min_date} → {max_date}"
        
    return summary
