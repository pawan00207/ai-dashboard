import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# -- Import local modules (modular structure) -------------------------------
from dataset_loader    import load_data, dataset_summary
from gemini_helper     import generate_query_plan
from query_processor   import execute_plan
from chart_generator   import generate_chart
from insights_generator import generate_insights

# ══════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS (EXACTLY AS PER THE "IMPRESSIVE" VERSION)
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500&display=swap');

:root {
    --red:       #E63946;
    --red-glow:  #E6394430;
    --amber:     #F4A261;
    --bg:        #09090B;
    --surface:   #111113;
    --card:      #18181B;
    --border:    #27272A;
    --text:      #D1D5DB;
    --muted:     #71717A;
    --head-font: 'Syne', sans-serif;
    --mono-font: 'JetBrains Mono', monospace;
    --body-font: 'Inter', sans-serif;
}

.stApp            { background: var(--bg); color: var(--text); font-family: var(--body-font); }
.block-container  { padding-top: 1.4rem !important; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

/* Hero */
.hero { padding: 22px 0 14px; border-bottom: 1.5px solid var(--red); margin-bottom: 24px; position: relative; }
.hero::after { content:''; position:absolute; bottom:-2px; left:0; width:70px; height:3px; background:var(--amber); border-radius:2px; }
.hero-eyebrow { font-family:var(--mono-font); font-size:0.66rem; letter-spacing:3px; color:var(--red); text-transform:uppercase; margin-bottom:6px; }
.hero-title   { font-family:var(--head-font); font-size:2.8rem; font-weight:800; color:#fff; line-height:1.1; text-shadow:0 0 40px var(--red-glow); }
.hero-sub     { font-family:var(--mono-font); font-size:0.7rem; color:var(--muted); margin-top:7px; }

/* Section heading */
.sh { font-family:var(--mono-font); font-size:0.66rem; letter-spacing:3px; text-transform:uppercase; color:var(--muted); border-left:3px solid var(--red); padding-left:10px; margin:20px 0 10px; }

/* Input */
.stTextInput > div > div > input {
    background:var(--card)!important; border:1.5px solid var(--border)!important; border-radius:10px!important;
    color:#fff!important; font-family:var(--mono-font)!important; font-size:0.95rem!important;
}

/* Button */
.stButton > button {
    background:var(--red)!important; color:#fff!important; font-family:var(--mono-font)!important;
    font-size:0.78rem!important; font-weight:600!important; letter-spacing:1.5px!important;
    text-transform:uppercase!important; border:none!important; border-radius:8px!important;
}

/* Chips */
.chips { display:flex; flex-wrap:wrap; gap:8px; margin:4px 0 18px; }
.chip  { background:var(--card); border:1px solid var(--border); border-radius:100px; padding:5px 14px; font-family:var(--mono-font); font-size:0.67rem; color:var(--muted); white-space:nowrap; }

/* Insight cards */
.insight { background:var(--card); border:1px solid var(--border); border-left:3px solid var(--red); border-radius:8px; padding:12px 16px; margin-bottom:9px; font-size:0.88rem; line-height:1.65; }
.insight:nth-child(even) { border-left-color:var(--amber); }

/* Sidebar stats */
.stat   { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:9px 13px; margin-bottom:7px; display:flex; justify-content:space-between; align-items:center; font-size:0.78rem; }
.stat-k { color:var(--muted); font-family:var(--mono-font); }
.stat-v { color:var(--red);   font-family:var(--mono-font); font-weight:600; }

.badge      { display:inline-flex; align-items:center; gap:5px; padding:4px 12px; border-radius:100px; font-family:var(--mono-font); font-size:0.67rem; font-weight:600; letter-spacing:1px; text-transform:uppercase; }
.badge-ai   { background:#E6394618; color:var(--red);   border:1px solid #E6394440; }
.badge-rule { background:#F4A26118; color:var(--amber); border:1px solid #F4A26140; }

.hr { border-top:1px solid var(--border); margin:18px 0; }
[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:8px; }
.empty { text-align:center; padding:70px 0; color:var(--muted); font-family:var(--mono-font); font-size:0.82rem; }
#MainMenu, footer, header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("🔑 Gemini API Key", type="password", placeholder="AIza… (optional)")
    
    if api_key.strip():
        st.markdown('<span class="badge badge-ai">✦ Gemini AI active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-rule">⚡ Rule engine active</span>', unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Dataset")
    
    uploaded_file = st.file_uploader("Upload CSV Data", type=["csv"], help="Upload a custom dataset to analyse.")
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        df = load_data()

    for label, value in dataset_summary(df).items():
        st.markdown(f'<div class="stat"><span class="stat-k">{label}</span><span class="stat-v">{value}</span></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
#  MAIN PAGE
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">● live · natural language · ai-powered</div>
    <div class="hero-title">AI Analytics Dashboard</div>
    <div class="hero-sub">Type any question about the dataset — get an instant chart, data table, and insight summary.</div>
</div>
""", unsafe_allow_html=True)

EXAMPLE_QUERIES = [
    "Show views by category", "Top 10 videos by views", "Compare likes and comments by category",
    "Show engagement by region", "Views trend over time", "Average sentiment score by region"
]

st.markdown('<div class="sh">💡 Example queries</div>', unsafe_allow_html=True)
st.markdown('<div class="chips">' + "".join(f'<span class="chip">{q}</span>' for q in EXAMPLE_QUERIES) + "</div>", unsafe_allow_html=True)

st.markdown('<div class="sh">🔍 Ask a question</div>', unsafe_allow_html=True)

# -- Voice input (inline HTML approach) ------------------------------------
VOICE_HTML = """
<div style="display:flex;align-items:center;gap:12px;padding:4px 0 8px 0;">
  <button id="mic-btn" onclick="toggleMic()" title="Click to speak"
    style="width:44px;height:44px;border-radius:10px;border:1.5px solid #27272A;
           background:#18181B;color:#71717A;font-size:1.3rem;cursor:pointer;
           display:flex;align-items:center;justify-content:center;transition:all .3s;
           flex-shrink:0;">🎤</button>
  <span id="mic-status" style="font-size:0.72rem;color:#71717A;font-family:monospace;"></span>
</div>

<script>
var recog = null;
var listening = false;

function setStatus(msg, color) {
    var el = document.getElementById('mic-status');
    el.textContent = msg;
    el.style.color = color || '#71717A';
}

function setButton(active) {
    var btn = document.getElementById('mic-btn');
    if (active) {
        btn.style.background = '#E6394618';
        btn.style.borderColor = '#E63946';
        btn.style.color = '#E63946';
        btn.style.boxShadow = '0 0 12px #E6394640';
    } else {
        btn.style.background = '#18181B';
        btn.style.borderColor = '#27272A';
        btn.style.color = '#71717A';
        btn.style.boxShadow = 'none';
    }
}

function fillInput(text) {
    // Walk up iframe chain to find the Streamlit app's text input
    var targetWindow = window.parent;
    try {
        var inputs = targetWindow.document.querySelectorAll('input[type="text"], input:not([type])');
        for (var i = 0; i < inputs.length; i++) {
            var inp = inputs[i];
            // Look for the question input (has placeholder about category)
            if (inp.placeholder && inp.placeholder.toLowerCase().includes('show')) {
                var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(inp, text);
                inp.dispatchEvent(new Event('input', { bubbles: true }));
                break;
            }
        }
    } catch(e) {}
}

function toggleMic() {
    if (listening && recog) { recog.stop(); return; }
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { setStatus('⚠ Not supported in this browser', '#F4A261'); return; }
    recog = new SR();
    recog.lang = 'en-US';
    recog.interimResults = false;
    recog.onstart  = function() { listening=true;  setButton(true);  setStatus('● Listening…', '#E63946'); };
    recog.onend    = function() { listening=false; setButton(false); };
    recog.onerror  = function(e){ listening=false; setButton(false); setStatus('⚠ '+e.error, '#F4A261'); };
    recog.onresult = function(e) {
        var t = e.results[0][0].transcript;
        setStatus('✓ ' + t, '#4ade80');
        fillInput(t);
    };
    recog.start();
}
</script>
"""
components.html(VOICE_HTML, height=60)

col_q, col_btn = st.columns([6, 1])
with col_q:
    question = st.text_input("question", label_visibility="collapsed", placeholder="e.g. Show total views by category …")
with col_btn:
    go_clicked = st.button("Analyse →")

# -- RUN PIPELINE -----------------------------------------------------------
if (go_clicked or question.strip()) and question.strip():
    with st.spinner("🤖 Analysing..."):
        plan = generate_query_plan(question, api_key)
        
    try:
        result = execute_plan(df, plan)
        if not result.empty:
            st.markdown(f'<div class="sh">📈 {plan.get("title", "Result")}</div>', unsafe_allow_html=True)
            col_chart, col_table = st.columns([3, 2], gap="large")
            
            with col_chart:
                fig = generate_chart(result, plan)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                
            with col_table:
                st.markdown('<div class="sh" style="margin-top:0">📋 Data table</div>', unsafe_allow_html=True)
                st.dataframe(result, use_container_width=True, height=310)
                
            st.markdown('<div class="sh">💡 Insights</div>', unsafe_allow_html=True)
            for insight in generate_insights(result, plan):
                st.markdown(f'<div class="insight">{insight}</div>', unsafe_allow_html=True)
        else:
            st.warning("No data matched your query.")
    except Exception as e:
        st.error(f"Error: {e}")
elif not question.strip():
    st.markdown('<div class="empty"><div style="font-size:3rem;">📊</div><div>Type a question above and press <strong style="color:#E63946;">Analyse →</strong></div></div>', unsafe_allow_html=True)
