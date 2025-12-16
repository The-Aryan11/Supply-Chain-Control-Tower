import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import io
import random

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="Supply Chain Control Tower", layout="wide")

# ======================================================
# DARK MODE UI
# ======================================================
st.markdown("""
<style>
body { background-color: #0e1117; }
h1, h2, h3, h4 { color: #e6edf3; }
div[data-testid="metric-container"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    padding: 16px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# TITLE
# ======================================================
st.title("🛢️ Supply Chain Control Tower – Oil & Gas")
st.caption("Risk-Driven | SAP-Aligned | Executive Decision System")

# ======================================================
# SCENARIO TOGGLE
# ======================================================
st.sidebar.header("🌍 Disruption Scenario")

scenario = st.sidebar.radio(
    "Select Scenario",
    ["Normal", "War / Sanctions", "Port Strike", "Supplier Failure"]
)

scenario_factor = {
    "Normal": 1.0,
    "War / Sanctions": 1.9,
    "Port Strike": 1.6,
    "Supplier Failure": 1.7
}[scenario]

# ======================================================
# FREIGHT RISK INDEX (API-READY SIMULATION)
# ======================================================
freight_risk_index = round(random.uniform(0.9, 2.2), 2)
st.sidebar.metric("🚢 Freight Risk Index", freight_risk_index)

# ======================================================
# DATA GENERATION (SAP-STYLE)
# ======================================================
np.random.seed(42)

df = pd.DataFrame({
    "MATNR": [f"MAT{1000+i}" for i in range(10)],
    "Material": [
        "Blowout Preventer","Drill Pipe","Safety Valves","Mud Pumps",
        "Wellhead Equipment","PPE Kits","Hydraulic Hoses",
        "Control Cables","Lubricants","Fire Suppression Units"
    ],
    "Annual_Demand": np.random.randint(300, 2200, 10),
    "Unit_Cost": np.random.randint(20000, 400000, 10),
    "Lead_Time": np.random.randint(15, 60, 10),
    "Supplier_Risk": np.random.choice(["Low","Medium","High"], 10),
    "HSE_Critical": ["Yes","Yes","Yes","Yes","Yes","Yes","No","No","No","Yes"],
    "Downtime_Cost_Day": np.random.randint(2_000_000, 12_000_000, 10)
})

# ======================================================
# SAP MM FIELD MAPPING
# ======================================================
df["WERKS"] = "IN01"
df["LGORT"] = "0001"
df["DISPO"] = "001"
df["BESKZ"] = "F"
df["STPRS"] = df["Unit_Cost"]

# ======================================================
# INVENTORY & RISK ENGINE
# ======================================================
df["Annual_Value"] = df["Annual_Demand"] * df["Unit_Cost"]

df = df.sort_values("Annual_Value", ascending=False)
df["Cum_%"] = df["Annual_Value"].cumsum() / df["Annual_Value"].sum()
df["ABC"] = pd.cut(df["Cum_%"], [0,0.7,0.9,1], labels=["A","B","C"])

supplier_factor = {"Low":1.0,"Medium":1.4,"High":1.8}
df["Supplier_Factor"] = df["Supplier_Risk"].map(supplier_factor)
df["HSE_Factor"] = np.where(df["HSE_Critical"]=="Yes",1.7,1.0)

ordering_cost = 20000
holding_rate = 0.28

df["EOQ"] = np.sqrt(
    (2 * df["Annual_Demand"] * ordering_cost *
     df["Supplier_Factor"] * freight_risk_index * scenario_factor) /
    (holding_rate * df["Unit_Cost"])
).round()

daily_demand = df["Annual_Demand"] / 365
z = norm.ppf(0.975)

df["Safety_Stock"] = (
    z * daily_demand * np.sqrt(df["Lead_Time"]) *
    df["HSE_Factor"] * freight_risk_index * scenario_factor
).round()

df["ROP"] = (daily_demand * df["Lead_Time"] + df["Safety_Stock"]).round()

df["Expected_Stockout_Days"] = np.where(
    df["HSE_Critical"]=="Yes",
    np.random.randint(2,7,10),
    np.random.randint(0,3,10)
)

df["Annual_Downtime_Loss"] = (
    df["Expected_Stockout_Days"] *
    df["Downtime_Cost_Day"] *
    scenario_factor
)

df["Enterprise_Risk_Score"] = (
    df["Annual_Downtime_Loss"]/1e6 +
    df["Supplier_Factor"]*15 +
    df["HSE_Factor"]*20 +
    freight_risk_index*10
).round(1)

# ======================================================
# KPI PANEL
# ======================================================
c1,c2,c3,c4 = st.columns(4)
c1.metric("Inventory Value (₹ Cr)", f"{df['Annual_Value'].sum()/1e7:.2f}")
c2.metric("Downtime Risk (₹ Cr)", f"{df['Annual_Downtime_Loss'].sum()/1e7:.2f}")
c3.metric("High-Risk Items", df[df["Enterprise_Risk_Score"]>55].shape[0])
c4.metric("Scenario", scenario)

# ======================================================
# DASHBOARD 1 – RISK HEATMAP
# ======================================================
st.subheader("🔥 Enterprise Risk Heatmap")
st.plotly_chart(
    px.bar(df.sort_values("Enterprise_Risk_Score", ascending=False),
           x="Material", y="Enterprise_Risk_Score",
           color="HSE_Critical"),
    width="stretch"
)

# ======================================================
# DASHBOARD 2 – EOQ vs ROP
# ======================================================
st.subheader("📦 Inventory Control (EOQ vs ROP)")
st.plotly_chart(
    px.scatter(df, x="EOQ", y="ROP",
               size="Annual_Downtime_Loss",
               color="Supplier_Risk",
               hover_name="Material"),
    width="stretch"
)

# ======================================================
# DASHBOARD 3 – ABC–HSE PRIORITY MATRIX
# ======================================================
st.subheader("🧠 Inventory Priority Matrix")
st.plotly_chart(
    px.scatter(df, x="Annual_Value", y="Enterprise_Risk_Score",
               color="ABC", size="Annual_Downtime_Loss",
               hover_name="Material"),
    width="stretch"
)

# ======================================================
# DASHBOARD 4 – YOY KPI TREND (SIMULATED)
# ======================================================
st.subheader("📈 YoY Enterprise Risk Trend")

years = ["2023","2024","2025"]
trend_df = pd.DataFrame({
    "Year": years,
    "Risk_Index": [df["Enterprise_Risk_Score"].mean()*x for x in [0.85,1.0,1.15]]
})

st.plotly_chart(
    px.line(trend_df, x="Year", y="Risk_Index", markers=True),
    width="stretch"
)

# ======================================================
# DASHBOARD 5 – SAP UPLOAD PREVIEW
# ======================================================
st.subheader("🧾 SAP MM Upload Preview")

sap_upload = df[[
    "MATNR","Material","WERKS","LGORT","DISPO","BESKZ",
    "STPRS","EOQ","ROP"
]]

st.dataframe(sap_upload, width="stretch")

csv = sap_upload.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download SAP MM Upload File",
    csv,
    "SAP_MM_Upload.csv",
    "text/csv"
)

# ======================================================
# BOARD-READY PDF EXPORT
# ======================================================
st.subheader("📄 Board-Level Executive Report")

def generate_pdf(df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Supply Chain Risk Executive Summary", styles["Title"]))
    elements.append(Spacer(1,12))
    elements.append(Paragraph(f"Scenario: {scenario}", styles["Normal"]))
    elements.append(Paragraph(f"Freight Risk Index: {freight_risk_index}", styles["Normal"]))
    elements.append(Spacer(1,12))

    table = [
        ["Metric","Value"],
        ["Inventory Value (₹ Cr)", f"{df['Annual_Value'].sum()/1e7:.2f}"],
        ["Downtime Exposure (₹ Cr)", f"{df['Annual_Downtime_Loss'].sum()/1e7:.2f}"],
        ["High-Risk Items", df[df["Enterprise_Risk_Score"]>55].shape[0]]
    ]

    elements.append(Table(table))
    doc.build(elements)
    buffer.seek(0)
    return buffer

pdf = generate_pdf(df)

st.download_button(
    "⬇️ Download Executive PDF",
    pdf,
    "Executive_Supply_Chain_Report.pdf",
    "application/pdf"
)

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
<hr>
<div style="text-align:center; color:gray; font-size:14px;">
Created by <b>Aryan Ranjan</b> · All Rights Reserved
</div>
""", unsafe_allow_html=True)
