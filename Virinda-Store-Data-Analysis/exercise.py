import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from load_data import load_dataset
import clean_data as cd
import analyze_data as ad
import Plots as pl
os.chdir(os.path.dirname(os.path.abspath(__file__)))


save_dir = os.path.join("plots")
data_path = os.path.join("resources", "Vrinda Store Data Analysis.xlsx")

#load the dataset VAStra Store from the excel file to a pandas dataframe:
df = load_dataset(data_path)

print(df.head(10))
#introduce NaN values and handle them:
new_df = cd.introduce_nan(df)
print(cd.show_values_nan(new_df))
print(cd.fill_missing_Age_values(new_df))
print(cd.fill_missing_shipState(new_df))
print(cd.fill_missing_status(new_df))
print(cd.fill_missing_SKU(new_df))
#show the dataframe after handling missing values:
new_df = new_df.reset_index(drop=True)  # Reset index after filling NaN values
print("\nDataframe after handling missing values:\n")
print(cd.show_values_nan(new_df))

#calculate total revenue of the store:
total_revenue = ad.calculate_revenue(new_df)
print(f"\nTotal revenue of the store: {total_revenue :.2f}")

#total number of clients:
total_clients = ad.calculate_number_clients(new_df)
print(f"\nTotal number of clients: {total_clients}")

total_ord = ad.calculate_orders(new_df)
print(f"\nTotal number of orders: {total_ord}")

#calculate mean monthly sales:
mean_monthly_sales = ad.mean_montly_sales(new_df)
print(f"\nMean monthly sales: {mean_monthly_sales}")
#mean monthly sales bar chart
pl.monthly_average_sales_chart(new_df, save_dir)


#calculate mean daily sales:
mean_daily_sales = ad.mean_daily_sales(new_df)
print(f"\nMean daily sales: {mean_daily_sales}")

#calculate the peak of the month having the highest revenue:
peak_month = ad.sales_month_peak(new_df)
print(f"\nPeak month with the highest revenue: {peak_month}")

#show the top 10 clients with the highest mean order value and then the mean order value of all clients:
mean_order_per_client = ad.mean_order_per_client(new_df)
print(f"\nMean order value of all clients: {mean_order_per_client :.2f}")

#show the total number of 'Returned' products:
returned_products = ad.calculate_returned_products(new_df)
print(f"\nTotal number of returned products: {returned_products}")
#show the total number of 'Delivered' products:
delivered_products = ad.calculate_delivered_products(new_df)
print(f"\nTotal number of delivered products: {delivered_products}")
#show the total number of 'Cancelled' products:
cancelled_products = ad.calculate_cancelled_products(new_df)
print(f"\nTotal number of cancelled products: {cancelled_products}")
#pie chart for the total number of 'Returned', 'Delivered' and 'Cancelled' products:
pl.show_orders_status(new_df, save_dir)

#Generate the bar chart for the most influent ship-states:
orders_ship_state = ad.highest_state_sales(new_df)
pl.orders_ship_state_chart(new_df, save_dir)


#show the distribution of the most 20 influent ship-city and generate the bar chart for the top 20 cities:
print("\nDistribution of the orders for the top 20 ship-city:\n")
top20 = new_df['ship-city'].value_counts().nlargest(20)
print(top20)
pl.orders_ship_city_chart(new_df, save_dir)


#distribution of the orders for gender and generate the pie chart of the results:
genderM = ad.calculate_sales_by_genderM(new_df)
genderW = ad.calculate_sales_by_genderW(new_df)
print("\nTotal orders and total turnover of orders made by men:\n")
print(genderM)
print("\nTotal orders and total turnover of orders made by women:\n")
print(genderW)

#pie chart for the total orders made by Men and Women:
pl.orders_by_gender_chart(new_df, save_dir)

#show the distribution of the orders for gender-Age Group-ship-state:
print("\nDistribution of the orders based on Gender,Age Group and ship-state:\n")
ad.orders_by_genderAge_GroupShipState(new_df)


#distribution of the orders based on the range Age(5-18,19-30,31-40,41-50,51-60,61-70,71-80):
ad.orders_by_rangeAge(new_df)
#bar chart for the distribution of the orders based on the range Age:
pl.orders_by_rangeAge(new_df, save_dir)


#distribution of the orders based on the range Age(5-18,19-30,31-40,41-50,51-60,61-70,71-80) and Gender:
ad.orders_by_rangeAge_Gender(new_df)


print("\nPearson correlation:")
correlation_matrix = ad.calculate_correlations_matrix(new_df)
print(correlation_matrix)

print("\nSpearman correlation:")
spearman_matrix = ad.calculate_spearman_matrix(new_df)
print(spearman_matrix)
print("\n")


#calculate and show the main metrics of the dataset
print("-" * 50)
print("Main metrics of the dataset:")
print("\nNumeric KPI:")
numeric_kpi = ad.showNumericKPI(new_df)
for key in numeric_kpi:
    print(f"\n{key} : {numeric_kpi[key]}")

print("\nText KPI:")
text_kpi = ad.showTextMetrics(new_df)
for key in text_kpi:
    print(f"\n{key} : {text_kpi[key]}")
print("-" * 50)
    

# create and save the dataframe that contains all metrics
kpi_df = ad.create_kpi_dataframe(new_df)
kpi_df.to_csv(os.path.join('resources', 'all_kpi.csv'), index=False, encoding='utf-8', sep=',')

# save text metrics to a separate file
text_metrics_df = pd.DataFrame(list(text_kpi.items()), columns=['Metric', 'Value'])
text_metrics_df['Category'] = 'General KPI'
text_metrics_df.to_csv(os.path.join('resources', 'text_kpi.csv'), index=False, encoding='utf-8', sep=',')





