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
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    dataframes = []

    for file in uploaded_files:
        df = pd.read_csv(file)

        # Remove blank Excel columns
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        # Add source file name
        df["SOURCE_FILE"] = file.name

        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    st.success(f"{len(uploaded_files)} file(s) loaded successfully!")

    st.subheader("Combined Data Preview")
    st.dataframe(combined_df)

    st.markdown("---")
    st.subheader("Dashboard Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Cases", len(combined_df))

    with col2:
        if "SURGEON" in combined_df.columns:
            st.metric("Unique Surgeons", combined_df["SURGEON"].nunique())
        else:
            st.metric("Unique Surgeons", "N/A")

    with col3:
        if "PROCEDURE" in combined_df.columns:
            st.metric("Unique Procedures", combined_df["PROCEDURE"].nunique())
        else:
            st.metric("Unique Procedures", "N/A")

    with col4:
        if "CALLBACK" in combined_df.columns:
            callback_count = combined_df["CALLBACK"].astype(str).str.upper().eq("YES").sum()
            st.metric("Callback Cases", callback_count)
        else:
            st.metric("Callback Cases", "N/A")

    st.markdown("---")
    st.subheader("Quick Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Operational Trends"):
            st.write("Operational trend analysis will be added in the next version.")

    with col2:
        if st.button("Staffing Analysis"):
            if "XR_STAFF_PULLED" in combined_df.columns:
                staff_pulled = combined_df["XR_STAFF_PULLED"].astype(str).str.upper().eq("YES").sum()
                st.write(f"Staff were pulled in {staff_pulled} case(s).")
            else:
                st.write("XR_STAFF_PULLED column was not found.")

    with col3:
        if st.button("Executive Recommendations"):
            st.write("Executive recommendations will be added in the AI phase.")

    st.markdown("---")
    st.subheader("Future Dashboard Features")

    st.write("Case Volume Trends")
    st.write("Staffing Heat Maps")
    st.write("Equipment Utilization")
    st.write("AI Operational Insights")

else:
    st.info("Upload one or more CSV files to begin analysis.")
