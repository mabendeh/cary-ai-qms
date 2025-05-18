
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cary Products AI QMS", layout="wide")

st.title("🧠 Cary Products - AI QMS System")
st.markdown("Upload your molding or inspection data to analyze performance, track issues, and get AI-driven insights.")

uploaded_file = st.file_uploader("Upload Molding or Inspection Data", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📊 Uploaded Data")
        st.dataframe(df)

        df["Cycle Time Deviation (%)"] = ((df["ACTUAL CYCLE (sec)"] - df["STD CYCLE (sec)"]) / df["STD CYCLE (sec)"]) * 100

        def evaluate_risks(row):
            risks = []
            if row["Cycle Time Deviation (%)"] < -10:
                risks.append("⚠️ Cycle time too fast - Risk of short shot or sink marks.")
            if row["DRYER TEMP (°F)"] < 190:
                risks.append("⚠️ Dryer temp slightly low - Risk of moisture in ABS.")
            if row["COOLING TIME (sec)"] < 12:
                risks.append("⚠️ Cooling time too short - May cause warpage.")
            if row["INJECTION PRESSURE 1 (PSI)"] < 900:
                risks.append("⚠️ Low injection pressure - Check for cold slugs.")
            return " | ".join(risks) if risks else "✅ No immediate risks detected."

        df["AI Risk Assessment"] = df.apply(evaluate_risks, axis=1)

        st.subheader("🧠 AI Risk Assessment")
        st.dataframe(df[["MOLD #", "PRESS #", "ACTUAL CYCLE (sec)", "Cycle Time Deviation (%)", "AI Risk Assessment"]])

        st.download_button("📥 Download Full Report", df.to_csv(index=False), file_name="AI_Molding_Report.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("Please upload a molding or inspection file to begin analysis.")
