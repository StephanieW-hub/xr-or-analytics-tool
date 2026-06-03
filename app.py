import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="XR OR Analytics Tool",
    layout="wide"
)

st.title("XR OR Analytics Tool")
st.subheader("AI-Powered Operational Intelligence for Healthcare Leaders")

st.markdown("---")

uploaded_files = st.file_uploader(
    "Upload OR Data Files",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)

def clean_data(df):
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    return df

def count_event(df, keyword):
    if "EVENT_TYPE" in df.columns:
        return df["EVENT_TYPE"].astype(str).str.upper().str.contains(keyword, na=False).sum()
    return 0

if uploaded_files:
    dataframes = []

    for file in uploaded_files:
        df = load_file(file)
        df = clean_data(df)
        df["SOURCE_FILE"] = file.name
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    st.success(f"{len(uploaded_files)} file(s) loaded successfully!")

    st.subheader("Executive Dashboard Summary")

    total_cases = len(combined_df)

    callback_cases = 0
    if "CALLBACK" in combined_df.columns:
        callback_cases = combined_df["CALLBACK"].astype(str).str.upper().eq("YES").sum()

    staff_shortages = count_event(combined_df, "STAFF")
    cancelled_cases = count_event(combined_df, "CANCEL")
    add_on_cases = count_event(combined_df, "ADD")

    avg_case_minutes = "N/A"
    if "CASE_MINUTES" in combined_df.columns:
        avg_case_minutes = round(pd.to_numeric(combined_df["CASE_MINUTES"], errors="coerce").mean(), 1)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Cases", total_cases)

    with col2:
        st.metric("Callbacks", callback_cases)

    with col3:
        st.metric("Staff Shortages", staff_shortages)

    with col4:
        st.metric("Cancelled Cases", cancelled_cases)

    with col5:
        st.metric("Avg Case Minutes", avg_case_minutes)

    st.markdown("---")

    st.subheader("Operational Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if "DAY_OF_THE_WEEK" in combined_df.columns:
    st.write("Cases by Day of Week")

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_counts = (
        combined_df["DAY_OF_THE_WEEK"]
        .value_counts()
        .reindex(day_order, fill_value=0)
    )

    st.bar_chart(day_counts)

    with chart_col2:
        if "EQUIPMENT_USAGE" in combined_df.columns:
            st.write("Equipment Utilization")
            equipment_counts = combined_df["EQUIPMENT_USAGE"].value_counts().head(10)
            st.bar_chart(equipment_counts)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        if "SURGEON" in combined_df.columns:
            st.write("Top Surgeons by Case Volume")
            surgeon_counts = combined_df["SURGEON"].value_counts().head(10)
            st.bar_chart(surgeon_counts)

    with chart_col4:
        if "EVENT_TYPE" in combined_df.columns:
            st.write("Event Type Trends")
            event_counts = combined_df["EVENT_TYPE"].value_counts().head(10)
            st.bar_chart(event_counts)

    st.markdown("---")

    st.subheader("Ask XR OR Analytics")

    question = st.text_input(
        "Ask a question about the uploaded OR data",
        placeholder="Example: What staffing risks do you see?"
    )

    if st.button("Analyze"):
        if question:
            st.write("AI analysis will be connected in the next step using OpenAI.")
        else:
            st.warning("Please enter a question first.")

    st.markdown("---")

    st.subheader("Combined Data Preview")
    st.dataframe(combined_df)

else:
    st.info("Upload one or more CSV or Excel files to begin analysis.")
