import streamlit as st
import plotly.express as px


def visualize_spending(df):

    expense_df = df[df["type"] == "Expense"]

    if expense_df.empty:
        st.info("No expense data available.")
        return

    category_spending = (
        expense_df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_spending,
        names="category",
        values="amount",
        title="Spending by Category",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)


def monthly_spending_chart(df):

    if df.empty:
        st.info("No transaction data.")
        return

    df["date"] = df["date"].astype("datetime64[ns]")
    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = (
        df.groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="month",
        y="amount",
        markers=True,
        title="Monthly Spending Trend"
    )

    st.plotly_chart(fig, use_container_width=True)