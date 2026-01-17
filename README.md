# AI Market Intelligence Dashboard  
**AI-Driven Business Intelligence | Python • Machine Learning • Streamlit**

---

## 📌 Project Summary
The **AI Market Intelligence Dashboard** is an end-to-end data analytics and machine learning project designed to transform **raw retail and inventory data** into **actionable business insights**.

The system automates data processing, applies machine learning techniques for analysis, and presents results through an **interactive Streamlit dashboard**, enabling informed and data-driven business decisions.

This project demonstrates practical experience in **data engineering, machine learning, and business intelligence dashboarding**.

---

## 🎯 Problem Statement
Retail businesses often rely on raw transactional data that is:
- Difficult to interpret  
- Manually processed  
- Not directly usable for decision-making  

This leads to:
- Poor demand forecasting  
- Inefficient pricing strategies  
- Inventory mismanagement  

The project solves this by building a **code-driven AI pipeline** that converts raw data into **decision-ready insights**.

---

## 💡 Solution Approach
- Use **raw datasets as the single source of truth**
- Perform all data cleaning and feature engineering programmatically
- Apply machine learning for segmentation and forecasting
- Generate structured analytical outputs
- Visualize insights using an interactive Streamlit dashboard

---

## 🧠 Key Learning Outcomes
- End-to-end data analytics pipeline design  
- Feature engineering from transactional data  
- Customer behavior analysis  
- Time-series demand forecasting  
- Pricing strategy simulation  
- Streamlit dashboard development  
- Reproducible and automated analytics workflows  

---

## 🚀 Core Features
- Customer segmentation based on purchasing behavior  
- Demand forecasting using historical sales data  
- Pricing optimization through simulation  
- Production and inventory planning support  
- Interactive dashboard for KPI and insight visualization  

---

## 🛠️ Technology Stack

### Data & Machine Learning
- Python  
- pandas, numpy  
- scikit-learn  

### Visualization & Dashboard
- Streamlit  
- matplotlib, seaborn  

### Tools
- Jupyter Notebook  
- Git & GitHub  

---

## 📊 Dataset Information

### Raw Data Sources
- **Online Retail II Dataset**  
  Source: UCI Machine Learning Repository (via Kaggle)  
  https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci/data  
Sales & Inventory Data
Raw retail transaction and inventory datasets used for forecasting and planning
(Stored in the Data/ directory)

Note: Only raw datasets are stored in the repository.
All processed datasets and analytical outputs are generated entirely through code.

## 🏗️ System Architecture
Raw Retail & Inventory Data
            ↓
Data Cleaning & Feature Engineering
            ↓
Machine Learning & Analytics
            ↓
Generated Business Reports
            ↓
Streamlit Dashboard

## 📂 Project Structure

AI_Market_Intelligence/
│
├── app.py                 # Streamlit dashboard application
├── Market_Analysis.ipynb  # Complete analytics & ML pipeline
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


---

## ⚙️ How to Run the Project

### 1️⃣ Download Project
- Click **Code → Download ZIP**
- Extract the project folder

### 2️⃣ Install Dependencies
```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit


3️⃣ Run Analytics Pipeline

Open Market_Analysis.ipynb

Run all cells sequentially to generate outputs

4️⃣ Launch Streamlit Dashboard
streamlit run app.py


👨‍💻 Author

Jagtap Singh
