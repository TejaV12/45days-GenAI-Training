import streamlit as st
import pandas as pd
import time
import os


try:
    from auth import login
    from utils.router import choose_models
    from utils.parallel import run_parallel
    from utils.rate_limiter import check_limit
    from utils.report import generate_report
except Exception as e:
    st.error(e)
    st.stop()

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="LLM Nexus | Enterprise Comparison",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ================= APP BACKGROUND ================= */
.stApp {
    background:
        radial-gradient(900px circle at 10% 10%, rgba(56,189,248,0.25), transparent 40%),
        radial-gradient(800px circle at 90% 20%, rgba(168,85,247,0.25), transparent 45%),
        linear-gradient(180deg, #f8fafc, #eef2ff);
    color: #0f172a;
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(15,23,42,0.08);
}

/* ================= HEADERS ================= */
.main-header {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0284c7, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-header {
    font-size: 1.1rem;
    color: #475569;
    margin-bottom: 2rem;
}

/* ================= TEXT AREA ================= */
.stTextArea textarea {
    background: rgba(255,255,255,0.9) !important;
    color: #0f172a !important;
    border: 1px solid rgba(15,23,42,0.2) !important;
    border-radius: 14px;
    padding: 14px;
    font-size: 15px;
}

.stTextArea textarea::placeholder {
    color: #64748b !important;
}

.stTextArea textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.35) !important;
}

/* ================= SELECTBOX ================= */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.95);
    border: 1px solid rgba(15,23,42,0.2);
    border-radius: 12px;
    color: #0f172a;
}

/* ================= BUTTONS ================= */
div.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #7c3aed);
    color: #ffffff;
    border: none;
    padding: 0.9rem 2.2rem;
    font-weight: 700;
    border-radius: 14px;
    width: 100%;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(124,58,237,0.35);
}

/* ================= MODEL CARDS ================= */
.model-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(15,23,42,0.12);
    border-radius: 18px;
    padding: 22px;
    height: 100%;
    transition: all 0.25s ease;
}

.model-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 18px 35px rgba(15,23,42,0.15);
}

.model-name {
    font-weight: 800;
    font-size: 0.8rem;
    letter-spacing: 1.8px;
    color: #0284c7;
    margin-bottom: 12px;
    text-transform: uppercase;
}

/* ================= METRICS ================= */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(15,23,42,0.12);
    padding: 14px 20px;
    border-radius: 14px;
}

/* ================= TABS ================= */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: #475569;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #0284c7;
    border-bottom: 3px solid #0284c7;
}

/* ================= SCROLLBAR ================= */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #38bdf8, #7c3aed);
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)



# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("⚙️ Controls")

    if "user" in st.session_state:
        st.info(f"👤 Logged in as: **{st.session_state.user}**")

    st.markdown("---")
    st.subheader("Configuration")
    model_temp = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Max Tokens", value=1024, step=256)
    st.markdown("---")
    st.caption("v2.1.0 | Enterprise Edition")

# ---------------- MAIN APP ---------------- #
def main():
    login()
    if "user" not in st.session_state:
        st.stop()

    st.markdown('<div class="main-header">LLM Nexus</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Intelligent routing & cost-analysis engine for Generative AI.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        task = st.selectbox(
            "Target Objective",
            ["General", "Coding", "Fast Response", "Cost Saving"]
        )
        st.metric("Active Models", "3 Online", "Healthy")

    with col2:
        prompt = st.text_area(
            "Input Prompt",
            height=160,
            placeholder="E.g. Write a secure Python function to connect to AWS S3..."
        )

    run_btn = st.button("⚡ Execute Query")

    if run_btn:
        if not check_limit(st.session_state.user):
            st.error("🚫 Rate limit reached.")
            st.stop()

        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt.")
            st.stop()

        with st.status("🔄 Running models...", expanded=True):
            models = choose_models(task)
            start = time.time()
            responses = run_parallel(prompt, models)
            elapsed = round(time.time() - start, 2)

        st.markdown("### 📊 Analysis Results")

        tab1, tab2, tab3, tab4 = st.tabs([
            "👁️ Visual Comparison",
            "📝 Raw Data",
            "📉 Cost Report",
            "📊 Performance Dashboard"
        ])

        with tab1:
            cols = st.columns(len(responses))
            for i, (model, text) in enumerate(responses.items()):
                with cols[i]:
                    st.markdown(
                        f"""
                        <div class="model-card">
                            <div class="model-name">{model}</div>
                            {text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        with tab2:
            st.json(responses)

        with tab3:
            generate_report(prompt, responses)
            c1, c2 = st.columns(2)
            c1.metric("Estimated Cost", "$0.0042", "-12%")
            c2.metric("Avg Latency", f"{elapsed}s", "Fast")

        with tab4:
            metrics_file = "data/metrics/metrics.csv"
            if os.path.exists(metrics_file):
                df = pd.read_csv(metrics_file)
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

                st.subheader("⏱️ Avg Latency")
                st.bar_chart(df.groupby("model")["latency"].mean())

                st.subheader("📏 Avg Response Length")
                st.bar_chart(df.groupby("model")["response_length"].mean())
            else:
                st.info("No metrics yet.")

if __name__ == "__main__":
    main()
