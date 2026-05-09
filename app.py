import streamlit as st
import pandas as pd
import plotly.express as px
from excel_handler import get_properties, get_sample_data
from analyser import analyse_property

st.set_page_config(page_title="PropIQ", page_icon="🏢", layout="wide")

# ── Premium CSS ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0A0A0F; }
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    background: #0F0F18 !important;
    border-right: 1px solid #1E1E2E;
}

.hero { padding: 3rem 0 2rem; border-bottom: 1px solid #1E1E2E; margin-bottom: 2.5rem; }

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #2D2D4E;
    color: #7C7CFF;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 100px;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 400;
    color: #F0F0FF;
    line-height: 1.15;
    margin: 0 0 1rem;
    letter-spacing: -0.02em;
}

.hero-title span {
    background: linear-gradient(135deg, #7C7CFF, #C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub { font-size: 1rem; color: #6B6B88; font-weight: 300; margin: 0; }

.badge-buy {
    display: inline-block; background: #0D2818; color: #4ADE80;
    border: 1px solid #166534; padding: 4px 12px; border-radius: 100px;
    font-size: 12px; font-weight: 600;
}

.badge-avoid {
    display: inline-block; background: #2D0D0D; color: #F87171;
    border: 1px solid #7F1D1D; padding: 4px 12px; border-radius: 100px;
    font-size: 12px; font-weight: 600;
}

.badge-hold {
    display: inline-block; background: #1C1A0D; color: #FCD34D;
    border: 1px solid #78350F; padding: 4px 12px; border-radius: 100px;
    font-size: 12px; font-weight: 600;
}

.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 2rem 0; }

.feature-card {
    background: #0F0F18; border: 1px solid #1E1E2E;
    border-radius: 12px; padding: 1.5rem;
}

.feature-icon { font-size: 1.5rem; margin-bottom: 0.75rem; }
.feature-title { font-size: 14px; font-weight: 600; color: #D0D0E8; margin-bottom: 0.5rem; }
.feature-list { font-size: 13px; color: #6B6B88; line-height: 1.9; }

.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem; color: #F0F0FF; margin: 2rem 0 1rem; font-weight: 400;
}

.divider { border: none; border-top: 1px solid #1E1E2E; margin: 2rem 0; }

.stButton > button {
    background: linear-gradient(135deg, #4F4FD0, #7C3AED) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important; font-size: 14px !important;
    letter-spacing: 0.02em !important;
}

.stDownloadButton > button {
    background: #0F0F18 !important; color: #A0A0C8 !important;
    border: 1px solid #2D2D4E !important; border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stMetricValue"] { font-family: 'DM Serif Display', serif !important; color: #F0F0FF !important; }
[data-testid="stMetricLabel"] { color: #6B6B88 !important; font-size: 11px !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }

.stSuccess { background: #0D2818 !important; color: #4ADE80 !important; border: 1px solid #166534 !important; border-radius: 10px !important; }
.stInfo { background: #0D1628 !important; color: #7C7CFF !important; border: 1px solid #1E3A5F !important; border-radius: 10px !important; }
.stError { background: #2D0D0D !important; border: 1px solid #7F1D1D !important; border-radius: 10px !important; }

[data-testid="stExpander"] { background: #0F0F18 !important; border: 1px solid #1E1E2E !important; border-radius: 12px !important; }
.stProgress > div > div { background: linear-gradient(90deg, #4F4FD0, #7C3AED) !important; }
[data-testid="stFileUploader"] { background: #0F0F18 !important; border: 1px dashed #2D2D4E !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### PropIQ")
    st.markdown("<p style='color:#6B6B88;font-size:13px'>AI Real Estate Analyser</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<p style='color:#A0A0B8;font-size:12px;font-weight:600;letter-spacing:0.08em'>HOW TO USE</p>", unsafe_allow_html=True)
    st.markdown("<ol style='color:#6B6B88;font-size:13px;line-height:2.2;padding-left:1.2rem'><li>Download the sample file</li><li>Fill in your properties</li><li>Upload and click Analyse</li><li>Download your AI report</li></ol>", unsafe_allow_html=True)
    st.divider()
    sample_df = get_sample_data()
    # Save sample as xlsx in memory
    import io as _io
    _buf = _io.BytesIO()
    sample_df.to_excel(_buf, index=False, engine='openpyxl')
    _buf.seek(0)
    st.download_button("📥 Download Sample File (.xlsx)", _buf, "propiq_sample.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    st.divider()
    st.markdown("<p style='color:#A0A0B8;font-size:12px;font-weight:600;letter-spacing:0.08em'>REQUIRED COLUMNS</p>", unsafe_allow_html=True)
    st.code("property_name\nlocation\nprice\nrental_income\nexpenses")

# ── Hero ─────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <h1 class='hero-title'>🏢 <span>PropIQ</span></h1>
    <p class='hero-sub'>Upload your properties and get instant AI-powered analysis — ROI, rental yield, risk, and clear Buy/Hold/Avoid recommendations.</p>
</div>
""", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────
st.markdown("<p style='color:#6B6B88;font-size:13px;margin-bottom:0.5rem'>Upload your property file (.xlsx or .csv)</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["xlsx", "csv"], label_visibility="collapsed")

if uploaded_file:
    st.success(f"✅ {uploaded_file.name} uploaded successfully")
    properties, errors = get_properties(uploaded_file)

    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        st.stop()

    st.markdown(f"<p style='color:#6B6B88;font-size:13px'><b style='color:#D0D0E8'>{len(properties)} properties</b> ready for analysis</p>", unsafe_allow_html=True)

    with st.expander("👀 Preview data"):
        st.dataframe(pd.DataFrame(properties), use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if st.button("🤖  Run AI Analysis", type="primary", use_container_width=True):
        results = []
        progress = st.progress(0, text="Initialising analysis...")
        status = st.empty()

        for i, prop in enumerate(properties):
            name = prop.get("property_name", f"Property {i+1}")
            status.markdown(f"<p style='color:#7C7CFF;font-size:13px'>Analysing <b>{name}</b>...</p>", unsafe_allow_html=True)
            result = analyse_property(prop)
            results.append(result)
            progress.progress((i + 1) / len(properties), text=f"Analysed {i+1} of {len(properties)}")

        progress.empty()
        status.empty()
        st.success(f"✅ Analysis complete — {len(results)} properties analysed")

        results_df = pd.DataFrame(results)
        successful = [r for r in results if r.get("status") == "success"]

        if successful:
            scores = [r.get("investment_score", 0) for r in successful]
            yields = [r.get("calculated_rental_yield", 0) for r in successful]
            rois = [r.get("calculated_roi", 0) for r in successful]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Properties", len(successful))
            col2.metric("Avg Score", f"{sum(scores)/len(scores):.1f}/10")
            col3.metric("Avg Yield", f"{sum(yields)/len(yields):.1f}%")
            col4.metric("Avg ROI", f"{sum(rois)/len(rois):.1f}%")

            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<p class='section-title'>Property Analysis</p>", unsafe_allow_html=True)

            for result in successful:
                rec = result.get('recommendation', 'N/A')
                badge_class = "badge-buy" if rec == "Buy" else "badge-avoid" if rec == "Avoid" else "badge-hold"

                with st.expander(f"🏠  {result.get('property_name')}  ·  Score {result.get('investment_score')}/10", expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Investment Score", f"{result.get('investment_score')}/10")
                    c2.metric("Rental Yield", f"{result.get('calculated_rental_yield')}%")
                    c3.metric("ROI", f"{result.get('calculated_roi')}%")
                    c4.metric("Risk", result.get('risk_level', 'N/A'))

                    st.markdown(f"""
<div style='margin:1rem 0;padding:1rem;background:#0A0A0F;border-radius:10px;border:1px solid #1E1E2E'>
    <p style='color:#6B6B88;font-size:11px;margin:0 0 6px;text-transform:uppercase;letter-spacing:0.1em'>Recommendation</p>
    <span class='{badge_class}'>{rec}</span>
    <p style='color:#A0A0B8;font-size:13px;margin:1rem 0 0;line-height:1.7'>{result.get('summary', '')}</p>
</div>""", unsafe_allow_html=True)

                    col_l, col_r = st.columns(2)
                    with col_l:
                        st.markdown("<p style='color:#4ADE80;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em'>✅ Pros</p>", unsafe_allow_html=True)
                        for pro in result.get("pros", []):
                            st.markdown(f"<p style='color:#A0A0B8;font-size:13px;margin:4px 0'>· {pro}</p>", unsafe_allow_html=True)
                    with col_r:
                        st.markdown("<p style='color:#F87171;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em'>❌ Cons</p>", unsafe_allow_html=True)
                        for con in result.get("cons", []):
                            st.markdown(f"<p style='color:#A0A0B8;font-size:13px;margin:4px 0'>· {con}</p>", unsafe_allow_html=True)

                    st.markdown(f"<div style='margin-top:1rem;padding:0.75rem 1rem;background:#0A0A0F;border-radius:8px;border:1px solid #1E1E2E'><span style='color:#6B6B88;font-size:12px;margin-right:1.5rem'>📍 {result.get('location')}</span><span style='color:#6B6B88;font-size:12px;margin-right:1.5rem'>💰 ${result.get('price', 0):,.0f}</span><span style='color:#6B6B88;font-size:12px'>📅 {result.get('payback_years', 'N/A')} yr payback</span></div>", unsafe_allow_html=True)

            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<p class='section-title'>Charts</p>", unsafe_allow_html=True)

            chart_style = dict(
                paper_bgcolor='#0F0F18', plot_bgcolor='#0F0F18',
                font=dict(family='DM Sans', color='#6B6B88', size=12),
                margin=dict(l=20, r=20, t=40, b=20),
            )

            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                fig1 = px.bar(results_df, x="property_name", y="investment_score",
                    title="Investment Score", color="investment_score",
                    color_continuous_scale=["#F87171", "#FCD34D", "#4ADE80"])
                fig1.update_layout(**chart_style, title_font_color='#D0D0E8')
                fig1.update_xaxes(gridcolor='#1E1E2E', color='#6B6B88')
                fig1.update_yaxes(gridcolor='#1E1E2E', color='#6B6B88')
                st.plotly_chart(fig1, use_container_width=True)

            with chart_col2:
                fig2 = px.scatter(results_df, x="calculated_rental_yield", y="calculated_roi",
                    text="property_name", title="Yield vs ROI",
                    color="investment_score",
                    color_continuous_scale=["#F87171", "#FCD34D", "#4ADE80"])
                fig2.update_layout(**chart_style, title_font_color='#D0D0E8')
                fig2.update_xaxes(gridcolor='#1E1E2E', color='#6B6B88')
                fig2.update_yaxes(gridcolor='#1E1E2E', color='#6B6B88')
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.download_button("📥  Download Full Report (CSV)", results_df.to_csv(index=False), "propiq_report.csv", "text/csv", use_container_width=True)

        failed = [r for r in results if r.get("status") == "error"]
        if failed:
            for f in failed:
                st.error(f"{f.get('property_name')}: {f.get('error')}")

else:
    st.info("👆 Upload a property file above, or download the sample from the sidebar to get started.")
    st.markdown("""
<div class='feature-grid'>
    <div class='feature-card'>
        <div class='feature-icon'>📊</div>
        <div class='feature-title'>Financial Metrics</div>
        <div class='feature-list'>Rental Yield<br>ROI<br>Payback Period<br>Annual Net Income</div>
    </div>
    <div class='feature-card'>
        <div class='feature-icon'>🤖</div>
        <div class='feature-title'>AI Insights</div>
        <div class='feature-list'>Investment Score<br>Risk Assessment<br>Pros & Cons<br>Plain English Summary</div>
    </div>
    <div class='feature-card'>
        <div class='feature-icon'>🎯</div>
        <div class='feature-title'>Decision Support</div>
        <div class='feature-list'>Buy / Hold / Avoid<br>Comparison Charts<br>Downloadable Report<br>Side by side view</div>
    </div>
</div>
""", unsafe_allow_html=True)