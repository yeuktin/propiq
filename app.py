import streamlit as st
import pandas as pd
import plotly.express as px
from excel_handler import get_properties, get_sample_data
from analyser import analyse_property

st.set_page_config(page_title="PropIQ", page_icon="🏢", layout="wide")
st.title("🏢 PropIQ")
st.subheader("AI-Powered Real Estate Investment Analyser")
st.divider()

with st.sidebar:
    st.header("How to use")
    st.markdown("1. Download sample file\n2. Fill with your properties\n3. Upload and click Analyse\n4. Download your report")
    st.divider()
    sample_df = get_sample_data()
    st.download_button("📥 Download Sample File", sample_df.to_csv(index=False), "propiq_sample.csv", "text/csv")
    st.divider()
    st.markdown("**Required columns:**")
    st.code("property_name\nlocation\nprice\nrental_income\nexpenses")

uploaded_file = st.file_uploader("Upload your property file (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    properties, errors = get_properties(uploaded_file)

    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        st.stop()

    st.markdown(f"**{len(properties)} properties found**")

    with st.expander("👀 Preview your data"):
        st.dataframe(pd.DataFrame(properties), use_container_width=True)

    st.divider()

    if st.button("🤖 Analyse Properties", type="primary", use_container_width=True):
        results = []
        progress = st.progress(0, text="Starting analysis...")
        status = st.empty()

        for i, prop in enumerate(properties):
            name = prop.get("property_name", f"Property {i+1}")
            status.markdown(f"🔍 Analysing **{name}**...")
            result = analyse_property(prop)
            results.append(result)
            progress.progress((i + 1) / len(properties), text=f"Analysed {i+1} of {len(properties)}")

        progress.empty()
        status.empty()
        st.success(f"✅ Done — {len(results)} properties analysed")
        st.divider()

        results_df = pd.DataFrame(results)
        successful = [r for r in results if r.get("status") == "success"]

        if successful:
            col1, col2, col3, col4 = st.columns(4)
            scores = [r.get("investment_score", 0) for r in successful]
            yields = [r.get("calculated_rental_yield", 0) for r in successful]
            rois = [r.get("calculated_roi", 0) for r in successful]
            col1.metric("Properties Analysed", len(successful))
            col2.metric("Avg Investment Score", f"{sum(scores)/len(scores):.1f}/10")
            col3.metric("Avg Rental Yield", f"{sum(yields)/len(yields):.1f}%")
            col4.metric("Avg ROI", f"{sum(rois)/len(rois):.1f}%")
            st.divider()

            for result in successful:
                with st.expander(f"🏠 {result.get('property_name')} — Score: {result.get('investment_score')}/10 | {result.get('recommendation', 'N/A')}", expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Investment Score", f"{result.get('investment_score')}/10")
                    c2.metric("Rental Yield", f"{result.get('calculated_rental_yield')}%")
                    c3.metric("ROI", f"{result.get('calculated_roi')}%")
                    c4.metric("Risk Level", result.get('risk_level', 'N/A'))
                    st.markdown(f"**Location:** {result.get('location')}")
                    st.markdown(f"**Price:** ${result.get('price', 0):,.0f}")
                    st.markdown(f"**Payback Period:** {result.get('payback_years', 'N/A')} years")
                    st.markdown(f"**Recommendation:** **{result.get('recommendation', 'N/A')}**")
                    st.markdown(f"**Summary:** {result.get('summary', 'N/A')}")
                    col_pros, col_cons = st.columns(2)
                    with col_pros:
                        st.markdown("**✅ Pros**")
                        for pro in result.get("pros", []):
                            st.markdown(f"- {pro}")
                    with col_cons:
                        st.markdown("**❌ Cons**")
                        for con in result.get("cons", []):
                            st.markdown(f"- {con}")

            st.divider()
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                fig1 = px.bar(results_df, x="property_name", y="investment_score", title="Investment Score by Property", color="investment_score", color_continuous_scale="RdYlGn")
                st.plotly_chart(fig1, use_container_width=True)
            with chart_col2:
                fig2 = px.scatter(results_df, x="calculated_rental_yield", y="calculated_roi", text="property_name", title="Rental Yield vs ROI")
                st.plotly_chart(fig2, use_container_width=True)

            st.divider()
            st.download_button("📥 Download Full Report (CSV)", results_df.to_csv(index=False), "propiq_report.csv", "text/csv", use_container_width=True)

        failed = [r for r in results if r.get("status") == "error"]
        if failed:
            for f in failed:
                st.error(f"{f.get('property_name')}: {f.get('error')}")

else:
    st.info("👆 Upload a property file above, or download the sample from the sidebar.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📊 Financial Metrics**\n- Rental Yield\n- ROI\n- Payback Period\n- Net Income")
    with col2:
        st.markdown("**🤖 AI Insights**\n- Investment Score\n- Risk Level\n- Pros & Cons\n- Summary")
    with col3:
        st.markdown("**🎯 Decisions**\n- Buy / Hold / Avoid\n- Charts\n- Downloadable Report")
