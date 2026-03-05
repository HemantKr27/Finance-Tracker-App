import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def visualize_spending(transactions_df):
    st.markdown("<hr style='border:2px solid #D3D3D3;'>", unsafe_allow_html=True)
    st.subheader("bar graph")
    if not transactions_df.empty:
        category_summary = transactions_df.groupby(["category","type"])["amount"].sum().unstack(fill_value=0)

        st.bar_chart(category_summary)
        st.markdown("<hr style='border:2px solid #D3D3D3;'>", unsafe_allow_html=True)


        # Pie chart for income and expense
        st.subheader("pie chart")
        type_summary = transactions_df.groupby("category")["amount"].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(type_summary, labels=type_summary.index, autopct='%1.1f%%', startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        #line chart for spending trend
        st.markdown("<hr style='border:2px solid #D3D3D3;'>", unsafe_allow_html=True)
        st.subheader("Spending Trend")
        if not transactions_df.empty:
            transactions_df['date'] = pd.to_datetime(transactions_df['date'])
            trends = transactions_df.groupby(["date", "type"])["amount"].sum().unstack(fill_value=0)

            st.line_chart(trends)
    else:
        st.info("No transactions to display analytics.")


def monthly_trend_chart(df):
    monthly = (
        df.groupby([df["date"].dt.to_period("M"), "type"])["amount"]
        .sum()
        .unstack(fill_value=0)
    )

    monthly.index = monthly.index.astype(str)

    st.line_chart(monthly)


def category_bar_chart(df):
    summary = (
        df[df["type"] == "Expense"]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(summary)




def visualize_category_spending(df):

    if df.empty:
        st.info("No data to display")
        return

    fig = px.pie(
        df,
        values="total",
        names="category",
        title="Spending by Category"
    )

    st.plotly_chart(fig, use_container_width=True)