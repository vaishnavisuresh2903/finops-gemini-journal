import os
from datetime import datetime

import streamlit as st
from google import genai


st.set_page_config(
    page_title="FinOps Gemini Journal",
    page_icon="☁️",
    layout="wide",
)

st.title("☁️ FinOps Gemini Journal")
st.subheader("Cloud Waste Auditor & Smart Savings Planner")

st.write(
    "Analyze your cloud spending, identify potential waste, "
    "and generate an actionable savings plan with Gemini."
)

st.divider()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Cloud Cost Details")

    monthly_spend = st.number_input(
        "Monthly cloud spending ($)",
        min_value=0.0,
        value=5000.0,
        step=100.0,
    )

    compute_cost = st.number_input(
        "Compute cost ($)",
        min_value=0.0,
        value=2500.0,
        step=100.0,
    )

    storage_cost = st.number_input(
        "Storage cost ($)",
        min_value=0.0,
        value=800.0,
        step=50.0,
    )

    database_cost = st.number_input(
        "Database cost ($)",
        min_value=0.0,
        value=1000.0,
        step=50.0,
    )

    network_cost = st.number_input(
        "Network cost ($)",
        min_value=0.0,
        value=700.0,
        step=50.0,
    )

    workload_notes = st.text_area(
        "Workload notes",
        placeholder=(
            "Example: Several development VMs run 24/7. "
            "Some storage contains old backups."
        ),
    )

    analyze_button = st.button(
        "🔍 Analyze Cloud Costs",
        type="primary",
        use_container_width=True,
    )


# -----------------------------
# Dashboard
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Monthly Spend", f"${monthly_spend:,.0f}")
col2.metric("Compute", f"${compute_cost:,.0f}")
col3.metric("Storage", f"${storage_cost:,.0f}")
col4.metric("Database", f"${database_cost:,.0f}")

st.divider()

# -----------------------------
# Gemini analysis
# -----------------------------
if analyze_button:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.warning(
            "GEMINI_API_KEY is not configured yet. "
            "The application UI is working, but Gemini analysis "
            "will become available after the API key is configured."
        )

        st.info(
            "Next deployment steps will configure the Gemini API key "
            "securely using Google Cloud Secret Manager."
        )

    else:
        try:
            client = genai.Client(api_key=api_key)

            prompt = f"""
You are a FinOps cloud cost optimization expert.

Analyze the following monthly cloud spending information.

Monthly total: ${monthly_spend:,.2f}
Compute: ${compute_cost:,.2f}
Storage: ${storage_cost:,.2f}
Database: ${database_cost:,.2f}
Network: ${network_cost:,.2f}

Additional workload notes:
{workload_notes if workload_notes else "No additional notes provided."}

Provide a practical FinOps analysis with these sections:

1. Cost Summary
2. Potential Waste
3. Priority Optimization Opportunities
4. Recommended Actions
5. Estimated Savings Range
6. 30-Day Savings Plan

Focus on realistic cloud optimization actions such as:
- rightsizing
- idle resource removal
- scheduling non-production resources
- storage lifecycle policies
- committed-use or savings-plan opportunities
- monitoring and budget controls

Do not invent exact cloud billing data that was not provided.
"""

            with st.spinner("Gemini is analyzing your cloud costs..."):
                response = client.models.generate_content(
                    model="gemini-3.7-flash",
                    contents=prompt,
                )

            st.success("Cloud cost analysis completed.")

            st.header("🤖 Gemini FinOps Analysis")
            st.markdown(response.text)

            # Journal entry
            st.divider()
            st.header("📔 FinOps Journal")

            journal_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "monthly_spend": monthly_spend,
                "analysis": response.text,
            }

            st.json(journal_entry)

        except Exception as exc:
            st.error("Gemini analysis could not be completed.")
            st.exception(exc)

else:
    st.info(
        "Enter your cloud cost information in the sidebar and click "
        "**Analyze Cloud Costs** to generate your FinOps report."
    )

st.divider()

st.caption(
    "FinOps Gemini Journal • AI-powered cloud cost optimization"
)
