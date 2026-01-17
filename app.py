import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Market Intelligence Dashboard",
    layout="wide"
)

# =====================================================
# DATA LOADING
# =====================================================
@st.cache_data
def load_data():
    sales = pd.read_csv(
        "master_sales_data.csv",
        parse_dates=["invoice_date"]
    )
    forecast = pd.read_csv("forecast_results.csv")
    segments = pd.read_csv("customer_segments.csv")
    segment_summary = pd.read_csv("customer_segment_summary.csv")
    pricing = pd.read_csv("pricing_recommendation.csv")
    production = pd.read_csv("production_plan.csv")
    pricing_sim = pd.read_csv("pricing_simulation.csv")

    return sales, forecast, segments, segment_summary, pricing, production, pricing_sim


(
    sales_df,
    forecast_df,
    segments_df,
    segment_summary_df,
    pricing_df,
    production_df,
    pricing_sim_df
) = load_data()

# =====================================================
# BUILD PRODUCT-LEVEL HISTORICAL TRENDS
# =====================================================
@st.cache_data
def build_product_trends(sales_df):
    product_trends = {}

    for product, group in sales_df.groupby("product_name"):
        monthly = (
            group
            .groupby(pd.Grouper(key="invoice_date", freq="ME"))["quantity"]
            .sum()
            .reset_index()
        )

        if len(monthly) < 3:
            product_trends[product] = "Insufficient data"
            continue

        monthly["time_index"] = range(len(monthly))

        slope = np.polyfit(
            monthly["time_index"],
            monthly["quantity"],
            1
        )[0]

        if slope > 0:
            product_trends[product] = "Increasing"
        elif slope < 0:
            product_trends[product] = "Decreasing"
        else:
            product_trends[product] = "Stable"

    return product_trends


product_trend_lookup = build_product_trends(sales_df)

# =====================================================
# BUSINESS CONTEXT
# =====================================================
def build_business_context(
    sales_df,
    forecast_df,
    segment_summary_df,
    pricing_df,
    production_df
):
    context = {}

    overall_monthly = (
        sales_df
        .groupby(pd.Grouper(key="invoice_date", freq="ME"))["quantity"]
        .sum()
    )

    slope = np.polyfit(
        range(len(overall_monthly)),
        overall_monthly.values,
        1
    )[0]

    context["overall_trend"] = "Growing" if slope > 0 else "Declining"

    top_growth = forecast_df.sort_values(
        "expected_growth_pct", ascending=False
    ).iloc[0]

    context["top_product"] = top_growth["product_name"]
    context["top_growth_pct"] = top_growth["expected_growth_pct"]

    top_segment = segment_summary_df.sort_values(
        "Avg_Monetary", ascending=False
    ).iloc[0]

    context["top_segment"] = top_segment["segment_label"]

    context["price_sensitive_count"] = pricing_df[
        pricing_df["pricing_recommendation"].str.contains("Reduce")
    ].shape[0]

    context["capacity_constraints"] = production_df[
        production_df["production_action"] == "Capacity Constrained"
    ].shape[0]

    return context


business_context = build_business_context(
    sales_df,
    forecast_df,
    segment_summary_df,
    pricing_df,
    production_df
)

# =====================================================
# FUTURE TREND GENERATOR (NEW)
# =====================================================
def generate_future_trend_series(base_value, growth_pct, periods):
    growth_rate = growth_pct / 100
    values = []
    current = base_value

    for _ in range(periods):
        current = current * (1 + growth_rate / periods)
        values.append(round(current, 2))

    return values

# =====================================================
# AI INSIGHT CHATBOT (EXTENDED)
# =====================================================
def ai_insight_bot(query, context, product_trends):
    q = query.lower()

    # -------- FUTURE FORECAST QUESTIONS --------
    if any(x in q for x in ["after", "future", "next", "3 month", "3 months"]):
        for product in forecast_df["product_name"]:
            if product.lower() in q:
                row = forecast_df[forecast_df["product_name"] == product].iloc[0]

                if row["forecast_trend"] == "Increasing":
                    return (
                        f"Yes. **{product}** is expected to see an **increase in demand "
                        f"over the next 3 months**, with projected growth of "
                        f"**{row['expected_growth_pct']}%**."
                    )
                elif row["forecast_trend"] == "Decreasing":
                    return (
                        f"No. **{product}** is expected to **decline in demand "
                        f"over the next 3 months**, with projected change of "
                        f"**{row['expected_growth_pct']}%**."
                    )
                else:
                    return (
                        f"Demand for **{product}** is expected to remain **stable "
                        f"over the next 3 months**."
                    )

    # -------- HISTORICAL QUESTIONS --------
    if "trend" in q or "increasing" in q or "decreasing" in q:
        for product in product_trends:
            if product.lower() in q:
                return (
                    f"The historical demand trend for **{product}** is "
                    f"**{product_trends[product]}**, based on past sales data."
                )

    if "overall" in q or "market" in q:
        return f"The overall market trend is **{context['overall_trend']}**."

    if "fastest" in q or "top product" in q:
        return (
            f"**{context['top_product']}** is the fastest growing product "
            f"with expected growth of **{context['top_growth_pct']}%**."
        )

    if "customer" in q or "segment" in q:
        return f"The most valuable customer segment is **{context['top_segment']}**."

    if "pricing" in q or "price" in q:
        return (
            f"There are **{context['price_sensitive_count']}** highly price-elastic products."
        )

    if "production" in q or "capacity" in q:
        return (
            f"There are **{context['capacity_constraints']}** products "
            "constrained by production capacity."
        )

    return (
        "I can explain historical trends, future demand, pricing, "
        "customer segments, and production planning."
    )

# =====================================================
# SIDEBAR CONTROLS
# =====================================================
st.sidebar.title("🔎 Controls")

granularity = st.sidebar.selectbox(
    "Trend Granularity",
    ["Monthly", "Quarterly", "Yearly"]
)

freq_map = {"Monthly": "M", "Quarterly": "Q", "Yearly": "Y"}

product_list = sorted(sales_df["product_name"].unique())[:500]

selected_product = st.sidebar.selectbox(
    "Select Product",
    product_list
)

# =====================================================
# HEADER & KPIs
# =====================================================
tabs = st.tabs([
    "📊 Overview",
    "📈 Product Trends",
    "🔮 Forecast & Planning",
    "👥 Customers & Pricing"
])
with tabs[0]:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 Revenue", f"{sales_df['revenue'].sum():,.0f}")
    k2.metric("📦 Products", sales_df["product_name"].nunique())
    k3.metric("👥 Customers", sales_df["customer_id"].nunique())
    k4.metric("🔮 Forecasted Products", forecast_df.shape[0])

    st.subheader("📊 Overall Market Trend")

    overall_trend_df = (
        sales_df
        .groupby(pd.Grouper(key="invoice_date", freq="M"))["quantity"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.line(overall_trend_df, x="invoice_date", y="quantity"),
        use_container_width=True
    )
with tabs[1]:
    st.subheader("📈 Historical Product Trend")

    product_trend = (
        sales_df[sales_df["product_name"] == selected_product]
        .groupby(pd.Grouper(key="invoice_date", freq=freq_map[granularity]))["quantity"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.line(product_trend, x="invoice_date", y="quantity", markers=True),
        use_container_width=True
    )

    st.subheader("🔮 Future Product Demand Trend")

    future_granularity = st.selectbox(
        "Future Trend Granularity",
        ["Monthly", "Quarterly", "Yearly"],
        key="future_trend"
    )

    product_forecast = forecast_df[
        forecast_df["product_name"] == selected_product
    ]

    if not product_forecast.empty:
        base_demand = product_forecast["forecast_demand"].values[0]
        growth_pct = product_forecast["expected_growth_pct"].values[0]

        if future_granularity == "Monthly":
            periods, label = 6, "Month"
        elif future_granularity == "Quarterly":
            periods, label = 4, "Quarter"
        else:
            periods, label = 3, "Year"

        future_values = generate_future_trend_series(
            base_demand, growth_pct, periods
        )

        future_df = pd.DataFrame({
            label: range(1, periods + 1),
            "Forecasted Demand": future_values
        })

        st.plotly_chart(
            px.line(
                future_df,
                x=label,
                y="Forecasted Demand",
                markers=True
            ),
            use_container_width=True
        )
with tabs[2]:
    st.subheader("📌 Forecast Summary – Top Products")
# =====================================================
# KPI DRILL-DOWN CONTROLS
# =====================================================
    # st.subheader("📌 Forecast & Planning")

    selected_kpi = st.selectbox(
        "Select KPI to Explore",
        ["Revenue", "Products", "Customers", "Forecast"]
    )
    if selected_kpi == "Revenue":
        st.subheader("💰 Revenue Drill-Down")

        revenue_monthly = (
            sales_df
            .groupby(pd.Grouper(key="invoice_date", freq="M"))["revenue"]
            .sum()
            .reset_index()
        )

        st.plotly_chart(
            px.line(
                revenue_monthly,
                x="invoice_date",
                y="revenue",
                title="Monthly Revenue Trend"
            ),
            use_container_width=True
        )
    elif selected_kpi == "Products":
        st.subheader("📦 Product Contribution")

        product_revenue = (
            sales_df
            .groupby("product_name")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        st.plotly_chart(
            px.bar(
                product_revenue,
                x="product_name",
                y="revenue",
                title="Top 10 Products by Revenue"
            ),
            use_container_width=True
        )
    elif selected_kpi == "Customers":
        st.subheader("👥 Customer Distribution")

        customer_value = (
            sales_df
            .groupby("customer_id")["revenue"]
            .sum()
            .reset_index()
        )

        st.plotly_chart(
            px.histogram(
                customer_value,
                x="revenue",
                nbins=40,
                title="Customer Revenue Distribution"
            ),
            use_container_width=True
        )
    elif selected_kpi == "Forecast":
        st.subheader("🔮 Forecast Insights")

        st.dataframe(
            forecast_df
            .sort_values("expected_growth_pct", ascending=False)
            .head(10),
            use_container_width=True
        )

        st.subheader("🏭 Production Planning")

        st.dataframe(
            production_df
            .sort_values("final_production_qty", ascending=False)
            .head(20),
            use_container_width=True
        )
    with tabs[3]:
        st.subheader("👥 Customer Segmentation")

        st.plotly_chart(
            px.pie(
                segment_summary_df,
                values="Customers",
                names="segment_label"
            ),
            use_container_width=True
        )

        st.subheader("💰 Pricing Intelligence")

        st.dataframe(pricing_df.head(20), use_container_width=True)

        st.subheader("📉 What-If Pricing Simulation")

        sim_product = st.selectbox(
            "Select Product",
            pricing_sim_df["product_name"].unique(),
            key="pricing_sim"
        )

        st.dataframe(
            pricing_sim_df[
                pricing_sim_df["product_name"] == sim_product
            ],
            use_container_width=True
        )

# #######



# #######
# =====================================================
# STICKY SIDEBAR AI CHATBOT
# =====================================================
st.sidebar.divider()
st.sidebar.subheader("🤖 AI Assistant")

st.sidebar.markdown(
    "Ask things like:\n"
    "- Will WHITE METAL LANTERN increase after 3 months?\n"
    "- Overall market trend?\n"
    "- Pricing recommendation?"
)

if "sidebar_chat" not in st.session_state:
    st.session_state.sidebar_chat = []

user_q = st.sidebar.text_input(
    "Ask a question",
    key="sidebar_chat_input"
)

if user_q:
    answer = ai_insight_bot(
        user_q,
        business_context,
        product_trend_lookup
    )
    st.session_state.sidebar_chat.append((user_q, answer))

for q, a in reversed(st.session_state.sidebar_chat[-5:]):
    st.sidebar.markdown(f"**You:** {q}")
    st.sidebar.markdown(f"**AI:** {a}")
