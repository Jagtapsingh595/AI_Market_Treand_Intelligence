AI Market Intelligence Dashboard
AI-Driven Business Intelligence System with Streamlit
Executive Overview

The AI Market Intelligence Dashboard is an end-to-end data analytics and machine learning solution that transforms raw retail and inventory datasets into actionable business intelligence.

All intermediate and final datasets are programmatically generated from raw data, ensuring reproducibility, transparency, and analytical integrity.

Insights are delivered through an interactive Streamlit dashboard, enabling data-driven decision-making for business stakeholders.

Dataset Information
Raw Data Sources

This project uses publicly available retail datasets:

Online Retail II Dataset
Source: UCI Machine Learning Repository (via Kaggle)
https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci/data

Sales & Inventory Data
Compiled retail transaction and inventory records used for demand forecasting and production planning
(Stored as raw CSV files in the Data/ directory)

Note:
Only raw datasets are stored in the repository.
All processed datasets, reports, and analytical outputs are generated entirely through code.

Core Implementation
Data Handling

Raw datasets act as the single source of truth

Data cleaning, feature engineering, and transformations are performed programmatically

No manually edited or pre-processed datasets are used

Analytical Components

Customer Segmentation – Behavioral analysis based on purchase patterns

Demand Forecasting – Time-series modeling for future demand estimation

Pricing Optimization – Simulation-based pricing recommendations

Production Planning – Inventory and production alignment using forecast results

Dashboard

Interactive Streamlit dashboard

Visualizes KPIs, trends, and model outputs

Designed for non-technical business users

Serves as the final decision-support layer

System Architecture
Raw Retail & Inventory Data
            ↓
Code-Driven Data Processing
            ↓
Analytics & Machine Learning
            ↓
Generated Business Reports
            ↓
Streamlit Dashboard

Project Structure
AI_Market_Intelligence/
│
├── app.py
│   └── Streamlit dashboard application
│
├── Market_Analysis.ipynb
│   └── Complete analytics and ML pipeline
│
├── Data/
│   ├── online_retail_II.csv
│   ├── master_sales_data.csv
│   └── current_inventory.csv
│
├── Outputs/
│   ├── customer_segments.csv
│   ├── forecast_results.csv
│   ├── pricing_recommendation.csv
│   └── production_plan.csv
│
└── README.md

Technology Stack

Python

pandas, numpy, scikit-learn

matplotlib, seaborn

Streamlit

Jupyter Notebook

How to Use
Step 1: Download

Click Code → Download ZIP

Extract the project folder

Step 2: Install Dependencies
pip install pandas numpy scikit-learn matplotlib seaborn streamlit

Step 3: Run Analytics

Open Market_Analysis.ipynb

Run all cells to generate processed datasets

Step 4: Launch Dashboard
streamlit run app.py

Author
Jagtap Singh
