# Supply-Chain-Control-Tower

📌 Overview

This project is a Supply Chain Control Tower prototype designed for oil & gas operations, where inventory decisions must balance cost efficiency, operational continuity, and HSE (Health, Safety & Environment) compliance.

Unlike traditional inventory dashboards that optimize only holding cost, this system introduces risk-adjusted decision logic, integrating:

Supplier risk

Freight disruption risk

Safety-critical material prioritization

Scenario-based operational shocks

The result is an executive-ready decision support system, not a visualization demo.

🎯 Key Objectives

Optimize inventory policies using risk-adjusted EOQ and Reorder Point models

Quantify downtime risk in financial terms

Prioritize HSE-critical materials under uncertainty

Enable scenario-based decision making for leadership

Maintain SAP MM compatibility for ERP integration

🧠 Core Features
🔹 Risk-Adjusted Inventory Optimization

EOQ and safety stock dynamically adjusted using:

Supplier risk

Freight disruption index

Global scenario multipliers

Prevents stockouts of safety-critical materials without blind overstocking

🔹 Scenario Simulation

Leadership can simulate:

Normal operations

War / sanctions

Port strikes

Supplier failures

Each scenario recalculates inventory policies and enterprise risk exposure in real time.

🔹 HSE-First Logic

Safety-critical materials receive elevated risk weighting

Inventory decisions explicitly avoid HSE compromise, even when costs increase

🔹 SAP MM Field Mapping

The data model aligns with SAP MM structures, including:

Material master (MATNR, MAKTX)

Plant & storage location (WERKS, LGORT)

MRP & procurement parameters (DISPO, BESKZ)

Valuation price (STPRS)

An auto-generated CSV enables direct ERP upload or mock testing.

🔹 Executive Dashboards

The application includes multiple decision-grade dashboards:

Enterprise Risk Heatmap

Inventory Control (EOQ vs ROP)

ABC–HSE Priority Matrix

Year-over-Year Risk Trend

SAP Upload Readiness Panel

🔹 Board-Ready Reporting

One-click PDF executive summary

Designed for leadership and steering committee reviews

🛠️ Technology Stack

Python

Streamlit (application layer)

Pandas / NumPy (data processing)

Plotly (interactive analytics)

SciPy (statistical modeling)

ReportLab (executive PDF generation)

▶️ Running Locally
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py


The application will be available at:

http://localhost:8501

🌍 Deployment

The application can be deployed on:

Streamlit Community Cloud

Render

Any Python-based cloud service supporting Streamlit

📈 Power BI Compatibility

The data model and KPIs are intentionally designed to mirror Power BI-style measures, enabling:

Easy migration to .pbix

Consistent executive reporting across tools

👤 Author

Aryan Ranjan
Created for advanced supply chain analytics and decision-support use cases.

All Rights Reserved.

⚠️ Disclaimer

All data used in this project is synthetic and for demonstration purposes only.
The system represents a conceptual prototype and is not connected to live enterprise systems.
