import pandas as pd
import streamlit as st
import preprocessor

df=pd.read_csv("data_live.csv")
#
df=preprocessor.fetch_time_features(df)

# Title for dashboard
st.title("Sales Analytics DashBoard")

#side bar for filters
st.sidebar.title("Filters")

# filters
selected_year=preprocessor.multiselect("Select Year",df['Financial_Year'].unique())
selected_retailer=preprocessor.multiselect("Select Retailer",df['Retailer'].unique())
selected_company=preprocessor.multiselect("Select Company",df['Company'].unique())
selected_month=preprocessor.multiselect("Select Financial Month",df['Financial_Month'].unique())

filtered_df=df[(df["Financial_Year"].isin(selected_year)) & (df["Retailer"].isin(selected_retailer)) &(df["Company"].isin(selected_company)) & (df["Financial_Month"].isin(selected_month))]                                                                                                        

# KPI-key performance Indicator
# create column for displaying kpis
col1,col2,col3,col4=st.columns(4)
# Total sales
with col1:
    st.metric(label="Total Sales",value=int(filtered_df["Amount"].sum()))
# Total margin
with col2:
    st.metric(label="Total Margin",value=int(filtered_df["Margin"].sum()))
# Total Transactions
with col3:
    st.metric(label="Total Transactions",value=len(filtered_df))
# % Margin
with col4:
    st.metric(label="Margin Percentage",value=f"{int((filtered_df["Margin"].sum()*100)/(filtered_df["Amount"].sum()))}%")


# Visualization to analyze month-on-month sales trends
yearly_sales=(filtered_df[['Financial_Year','Financial_Month','Amount']].groupby(['Financial_Year','Financial_Month']).sum().reset_index().pivot(index='Financial_Month',columns='Financial_Year',values="Amount"))
st.line_chart(yearly_sales,x_label='Financial_Month',y_label="Total Sales")
# Visualize Retail Count by Revenue %
col5,col6=st.columns(2)
with col5:
    st.title("Retailer count by Revenue %")
    retailer_count=preprocessor.fetch_top_revenue_retailers(filtered_df)
    retailer_count.set_index("percentage revenue",inplace=True)
    st.bar_chart(retailer_count, x_label="percentage revenue",y_label="retailer_count")

with col6:
    st.title("Company count by Revenue %")
    company_count=preprocessor.fetch_top_revenue_companies(filtered_df)
    company_count.set_index("percentage revenue",inplace=True)
    st.bar_chart(company_count, x_label="percentage revenue",y_label="company_count")
