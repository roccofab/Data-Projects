import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from matplotlib import pyplot as plt
import streamlit as sl
import pandas as pd
import datetime as dt
import numpy as np
import altair as alt
from src.eda import eda_metrics as em, eda_plots as ep

    
sl.sidebar.subheader("Debug Info")
db_host = os.getenv("DB_HOST", "localhost")
db_user = os.getenv("DB_USER", "root")
db_name = os.getenv("DB_NAME", "agri_data")

for var, value in [("DB_HOST", db_host), ("DB_USER", db_user), ("DB_NAME", db_name)]:
    sl.sidebar.write(f"{var}: {value}")

# Warning if the environment variables are not configured correctly
if db_host == "localhost" or db_user == "root" or db_name == "agri_data":
    sl.sidebar.error("⚠️ Warning: Environment variables not configured correctly")
    
sl.set_page_config(page_title="Analytics Olive Oil and Olive Production Company", layout="wide")
sl.title("Analytics Olive Oil and Olive Production Company Dashboard")

tab1, tab2, tab3 = sl.tabs(["Production", "Consumption/Costs", "Profits & Turnover"])

axis=alt.Axis(    # Common axis properties
                labelColor="black",
                titleColor="black",
                labelFontSize=14,
                titleFontSize=16,
                labelFont="Segoe UI",
                titleFont="Segoe UI Bold"
            )

with tab1:
    # Page 1 content
    col1, col2 = sl.columns(2)
    col3, col4 = sl.columns(2)
    #column 1 chart
    with col1:
        sl.header("Net Yield per Hectare")
        df = em.harvest_efficiency_per_year()
        if not df.empty:
            chart1 = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X("year:O", title="Year", axis=axis),
                    y=alt.Y("net_yield_per_hectare:Q", title="Net Yield (Kg)", axis=axis),
                    tooltip=[
                        alt.Tooltip("year:O", title="Year"),
                        alt.Tooltip("net_yield_per_hectare:Q", title="Net Yield/Ha", format=".2f")
                    ]
                )
                .properties(width=400, height=350, title="Net Yield per Hectare Over the Years")
            )
            sl.altair_chart(chart1, use_container_width=True)
            
    #column 2 chart        
    with col2:
        sl.header("Average Yield per Plant")
        df = em.avg_yield_per_plant()
        if not df.empty:
            chart2 = (
                alt.Chart(df)
                .mark_line(point=True)
                .encode(
                    x=alt.X("year:O", title="Year", axis=axis),
                    y=alt.Y("avg_yield_per_plant:Q", title="Avg Yield (Kg)", axis=axis),
                    tooltip=[
                        alt.Tooltip("year:O", title="Year"),
                        alt.Tooltip("avg_yield_per_plant:Q", title="Avg Yield/Plant", format=".2f")
                    ]
                )
                .properties(width=400, height=350, title="Average Yield per Plant")
            )
            sl.altair_chart(chart2, use_container_width=True)
            
    #column 3 chart
    with col3:
        prod_df = em.get_production_data().copy()
        # ensure 'year' exists
        if 'year' not in prod_df.columns and 'date' in prod_df.columns:
            prod_df['year'] = pd.to_datetime(prod_df['date'], errors='coerce').dt.year

        sl.header("New Plants per Year")
        if 'year' in prod_df.columns and not prod_df.empty:
            df = prod_df.sort_values(by='year').copy()
            df["new_plants"] = df["plants_counter"].diff().fillna(0)
            df["new_plants"] = df["new_plants"].apply(lambda x: x if x > 0 else 0)

            chart3 = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X("year:O", title="Year", axis=axis),
                    y=alt.Y("new_plants:Q", title="New Plants", axis=axis),
                    tooltip=[
                        alt.Tooltip("year:O", title="Year"),
                        alt.Tooltip("new_plants:Q", title="New Plants", format=".0f")
                    ]
                )
                .properties(width=400, height=350, title="New Plants per Year")
            )
            sl.altair_chart(chart3, use_container_width=True)
        else:
            sl.info("Production Data not Available'.")
            
    #column 4 chart
    with col4:
        sl.header('Oil Yield per Hectare')
        
        df = em.oil_yield_per_year()
        if not df.empty:
            chart4 = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x = alt.X("year:O", title = "Year", axis = axis),
                    y = alt.Y("oil_yield_per_hectare:Q", title = "Oil Quantity", axis = axis),
                    tooltip = [
                         alt.Tooltip("year:O", title="Year"),
                         alt.Tooltip("oil_yield_per_hectare:Q", title="Oil Quantity", format=".0f")
                    ]
                )
                .properties(width=400, height=350, title="Oil Yield per Hectare Over the Years")
            )
            sl.altair_chart(chart4, use_container_width=True)

with tab2:
    # Page 2 content
    col1, col2 = sl.columns(2)  
    col3, col4 = sl.columns(2)
    col5,col6 = sl.columns(2)
    
    # column 1 chart
    with col1: 
        sl.header("Expenses Over the Years")
        
        df = em.get_consumption_data().copy()
        # ensure 'year' exists
        if 'year' not in df.columns and 'date' in df.columns:
            df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        # excludes the current year if the month of October has not yet been reached
        if current_month < 10:  
            if 'year' in df.columns:
                df = df[df["year"] < current_year]
        
        if not df.empty and all(col in df.columns for col in ['irrigation_expenses','fertilizer_costs','pesticide_costs','maintenance_expenses']) and 'year' in df.columns:
            df['total_expenses'] = df[['irrigation_expenses', 'fertilizer_costs', 'pesticide_costs', 'maintenance_expenses']].sum(axis = 1)
            
            chart1 = (
                alt.Chart(df)
                .mark_line(point = True)
                .encode(
                    x = alt.X("year:O", title = "Year", axis = axis),
                    y = alt.Y("total_expenses:Q", title = "expenses(€)", axis = axis),
                    tooltip = [
                        alt.Tooltip("year:O", title="Year"),
                        alt.Tooltip("total_expenses:Q", title="Total_Expenses", format=".0f")
                    ]
                )
                .properties(width=400, height=350, title="Total expenses over the years(irrigation, fertilization,pesticides,soil and plant maintenance)")
            )
            sl.altair_chart(chart1, use_container_width=True)
        else:
            sl.info("Consumption Data not Available.")
        
    # column 2 chart 
    with col2: 
        sl.header("Irrigation Volume(m^3)-Expenses(€)")
        
        df = em.get_consumption_data()
        if 'year' not in df.columns and 'date' in df.columns:
            df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
        
        if not df.empty and 'year' in df.columns and all(col in df.columns for col in ['irrigation_required_m3', 'irrigation_expenses']):
            chart2 = alt.Chart(df).mark_bar().encode(
                x=alt.X("year:O", title = "year", axis = axis),
                y = alt.Y("irrigation_required_m3:Q", title = "Volume(m^3)", axis = axis),
                tooltip = ["year", "irrigation_required_m3","irrigation_expenses"]
            )
            
            line_chart = alt.Chart(df).mark_line(color='red').encode(
                x='year:O',
                y=alt.Y('irrigation_expenses', title='expenses (€)', axis=alt.Axis(titleColor='red')), 
                tooltip=['year', 'irrigation_required_m3', 'irrigation_expenses']
            )

            # merge chart2 and line_chart and synchronize the X-axis
            combined_chart = alt.layer(chart2, line_chart).resolve_scale(
                y='independent' # the y-axes have two different value scales
            )

            sl.altair_chart(combined_chart, use_container_width=True)
        else:
            sl.info("Consumption Data not Available.")
        
    #column 3 chart
    with col3:
        sl.header("Pesticides Amount(Kg)-Expenses(€)")
        
        if not df.empty and 'year' in df.columns and all(col in df.columns for col in ['pesticide_required_kg', 'pesticide_costs']):
            chart3 = alt.Chart(df).mark_bar().encode(
                x = alt.X("year:O", title = "Year", axis = axis),
                y = alt.Y("pesticide_required_kg:Q", title = "Amount (Kg)", axis = axis),
                tooltip = ["year", "pesticide_required_kg", "pesticide_costs"]
            )
            
            line_chart = alt.Chart(df).mark_line(color='red').encode(
                x='year:O',
                y=alt.Y('pesticide_costs', title='expenses (€)', axis=alt.Axis(titleColor='red')), 
                tooltip=['year', 'pesticide_required_kg', 'pesticide_costs']
            )

            # merge chart2 and line_chart and synchronize the X-axis
            combined_chart = alt.layer(chart3, line_chart).resolve_scale(
                y='independent' # the y-axes have two different value scales
            )

            sl.altair_chart(combined_chart, use_container_width=True)
        else:
            sl.info("Pesticide Data not Available.")
        
    with col4:
        sl.header("Fertilizer Amount(Kg)-Expenses(€)")
        
        if not df.empty and 'year' in df.columns and all(col in df.columns for col in ['fertilizer_required_kg', 'fertilizer_costs']):
            chart4 = alt.Chart(df).mark_bar().encode(
                x = alt.X("year:O", title = "year", axis = axis),
                y = alt.Y("fertilizer_required_kg:Q", title = "Amount (Kg)", axis = axis),
                tooltip = ["year", "fertilizer_required_kg", "fertilizer_costs"]
            )
            
            line_chart = alt.Chart(df).mark_line(color = 'red').encode(
                x = "year:O",
                y = alt.Y("fertilizer_costs", title = "expenses (€)", axis = alt.Axis(titleColor='red')),
                tooltip = ["year", "fertilizer_required_kg", "fertilizer_costs"]
            )
            
            combined_chart = alt.layer(chart4, line_chart).resolve_scale(
                y='independent' # the y-axes have two different value scales
            )

            sl.altair_chart(combined_chart, use_container_width=True)
        else:
            sl.info("Fertilizer Data not Available.")
        
    with col5:
        sl.header("Annual Soil and Plant Maintenance Expenses")  
        
        if not df.empty and 'year' in df.columns and 'maintenance_expenses' in df.columns:
            chart5 = (
                alt.Chart(df)
                .mark_line(point = True)
                .encode(
                    x = alt.X("year:O", title = "Year", axis = axis),
                    y = alt.Y("maintenance_expenses:Q", title = "expenses(€)", axis = axis),
                    tooltip = [
                        alt.Tooltip("year:O", title="Year"),
                        alt.Tooltip("maintenance_expenses:Q", title="Total_Expenses", format=".0f")
                    ]
                )
                .properties(width=400, height=350, title="Soil and Plants Expenses Over the Years")
            )
            sl.altair_chart(chart5, use_container_width=True)
        else:
            sl.info("Maintenance Data not Available.")
         
        
    with col6:
        sl.header("Percentage Distribution of Expenses")
        
        if not df.empty and 'year' in df.columns and all(col in df.columns for col in ['irrigation_expenses', 'fertilizer_costs', 'pesticide_costs', 'maintenance_expenses']):
            years_list = sorted(df['year'].unique())  #list of unique years
            selected_year = sl.selectbox("Select Year", years_list, index=len(years_list) - 1)  #selectbox for year selection, default to the latest year
            df_selected = df[df["year"] == selected_year].copy()  # filter for the selected year
            
            df_selected['total_expenses'] = df_selected[['irrigation_expenses', 'fertilizer_costs', 'pesticide_costs', 'maintenance_expenses']].sum(axis=1)
            
            # Transform the 4 expense columns into a single Expense Type column and their values ​​into Amount (long format)
            df_melted = df_selected.melt(
                id_vars=["year"],
                value_vars=[
                    "irrigation_expenses",
                    "fertilizer_costs",
                    "pesticide_costs",
                    "maintenance_expenses",
                ],
                var_name="Expense Type",
                value_name="Amount (€)"
            )
            
            # Calculate percentages
            total = df_melted["Amount (€)"].sum()
            df_melted["Percentage"] = (df_melted["Amount (€)"] / total) * 100
            
            # Create pie chart
            chart_pie = (
                alt.Chart(df_melted)
                .mark_arc(outerRadius=150)
                .encode(
                    theta=alt.Theta("Percentage:Q", stack=True),
                    color=alt.Color("Expense Type:N", legend=alt.Legend(title="Expense Type")),
                    tooltip=[
                        alt.Tooltip("Expense Type:N", title="Type"),
                        alt.Tooltip("Amount (€):Q", format=".2f"),
                        alt.Tooltip("Percentage:Q", format=".2f", title="% of Total"),
                    ],
                ).properties(width=400,height=450,title=f"Expense Distribution for {selected_year}")
            )
            
            # Add percentage labels on the slices
            
            # Combine pie chart and text
            chart_pie = chart_pie 
            sl.altair_chart(chart_pie, use_container_width=True)
        else:
            sl.info("Expense Data not Available for Pie Chart.")

        
with tab3:
    # Page 2 content
    col1, col2 = sl.columns(2)  
    col3, col4 = sl.columns(2)
    col5,col6 = sl.columns(2)
    
    with col1:
        df = em.oil_profit_trend()
        
        sl.header("Profits(€) over the years generated by oil sales")
        chart1 = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x = alt.X("year:O", title = "Year", axis = axis),
                    y = alt.Y("revenue_€:Q", title = "Profit (€)", axis = axis),
                    tooltip = [
                         alt.Tooltip("year:O", title="Year"),
                         alt.Tooltip("revenue_€:Q", title="Profit (€)", format=".0f")
                    ]
            )
            .properties(width=400, height=350)
            
        )
        sl.altair_chart(chart1, use_container_width=True)
        
    with col2:
        df = em.profit_per_hectare()
        
        sl.header("Profit(€) per Hectare")
        chart2 = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                 x = alt.X("year:O", title = "Year", axis = axis),
                    y = alt.Y("profit_per_hectare:Q", title = "Profit (€)", axis = axis),
                    tooltip = [
                         alt.Tooltip("year:O", title="Year"),
                         alt.Tooltip("profit_per_hectare:Q", title="Profit (€)", format=".2f")
                    ]
            )
            .properties(width=400, height=350)
            
        )
        sl.altair_chart(chart2, use_container_width=True)
        
    with col3:
        df = em.get_production_data()
        if df.empty:
            sl.info("Production Data not Available.")
        else:
            if 'year' not in df.columns and 'date' in df.columns:
                df['year'] = pd.to_datetime(df['date'], errors='coerce').dt.year
            current_year = dt.date.today().year
            current_month = dt.date.today().month
            #excludes the current year if the month of October has not yet been reached
            if current_month < 10:   
                if 'year' in df.columns:
                    df = df[df["year"] < current_year]
                
            if not df.empty and 'oil_revenue' in df.columns and 'oil_yield' in df.columns:
                df['price_per_kg'] = df.apply(
                    lambda x: x['oil_revenue']/x['oil_yield'] if x['oil_yield'] > 0 else 0, axis = 1
                )
            else:
                sl.info("Oil revenue or yield data not available.")
        
        sl.header("Oil Price per Kg Over the Years")
        if not df.empty and 'price_per_kg' in df.columns:
            chart3 = (
                alt.Chart(df)
                .mark_line(point = True)
                .encode(
                    x = alt.X("year:O", title = "Year", axis = axis),
                    y = alt.Y("price_per_kg:Q", title = "Price", axis = axis),
                    tooltip = [
                        alt.Tooltip("year:O", title = "Year"),
                        alt.Tooltip("price_per_kg:Q", title = "Price_per_Kg", format = ".2f")
                    ]
                )
                .properties(width=400, height=350)
            )
            sl.altair_chart(chart3, use_container_width=True)
        else:
            sl.info("Oil price data not available.")
        
    with col4:
        try:
            prod = em.get_production_data()
            cons = em.get_consumption_data()
            if prod.empty or cons.empty:
                sl.info("Production or consumption data not available.")
            else:
                if 'year' not in prod.columns and 'date' in prod.columns:
                    prod['year'] = pd.to_datetime(prod['date'], errors='coerce').dt.year
                if 'year' not in cons.columns and 'date' in cons.columns:
                    cons['year'] = pd.to_datetime(cons['date'], errors='coerce').dt.year
                df = pd.merge(prod,cons,on = 'year',how = 'inner')
                current_year = dt.date.today().year
                current_month = dt.date.today().month
                #excludes the current year if the month of October has not yet been reached
                if current_month < 10:   
                    df = df[df["year"] < current_year]
                    
                if not df.empty and all(col in df.columns for col in ['irrigation_expenses', 'fertilizer_costs', 'pesticide_costs', 'maintenance_expenses', 'oil_revenue']):
                    df['total_expenses'] = df[['irrigation_expenses', 'fertilizer_costs', 'pesticide_costs', 'maintenance_expenses']].sum(axis = 1)
                    df['profit'] = df['oil_revenue'] - df['total_expenses']
                else:
                    sl.info("Required data columns not available.")
        except Exception as e:
            print(f"Error getting revenue and expenses: {e}")
            sl.info("Error loading data.")
            
        sl.header("Profit(€)-Expenses(€) Over the Years")
        if not df.empty and 'profit' in df.columns and 'total_expenses' in df.columns:
            chart4 = alt.Chart(df).mark_bar().encode(
                x=alt.X("year:O", title = "Year", axis = axis),
                y = alt.Y("profit:Q", title = "Profit (€)", axis = axis),
                tooltip = ["year", "total_expenses","profit"]
            )
            
            line_chart = alt.Chart(df).mark_line(color='red').encode(
                x='year:O',
                y=alt.Y('total_expenses', title='Expenses (€)', axis=alt.Axis(titleColor='red')), 
                tooltip=['year', 'total_expenses', 'profit']
            )

            # merge chart4 and line_chart and synchronize the X-axis
            combined_chart = alt.layer(chart4, line_chart).resolve_scale(
                y='independent' # the y-axes have two different value scales
            )

            sl.altair_chart(combined_chart, use_container_width=True)
        else:
            sl.info("Profit and expenses data not available.")
        
    with col5:
        sl.header("Profit(€)-Surface Area(m^2)")
        if not df.empty and 'profit' in df.columns and 'surface_area_in_m2' in df.columns:
            chart5 = alt.Chart(df).mark_bar().encode(
            x = alt.X("year:O", title = "Year", axis = axis),
            y = alt.Y("profit:Q", title = "Profit (€)", axis = axis),
            tooltip = ["year", "profit", "surface_area_in_m2"]
            )
            
            line_chart = alt.Chart(df).mark_line(color='red').encode(
                x = "year:O",
                y = alt.Y("surface_area_in_m2", title="Surface Area (m^2)", axis = alt.Axis(titleColor='red', title="Surface Area (m^2)")),
                tooltip=['year', 'profit', 'surface_area_in_m2']
            )
            
            # merge chart5 and line_chart and synchronize the X-axis
            combined_chart = alt.layer(chart5, line_chart).resolve_scale(
                y='independent' # the y-axes have two different value scales
            )

            sl.altair_chart(combined_chart, use_container_width=True)
        else:
            sl.info("Profit and surface area data not available.")
        
    with col6:
        sl.header("Profit(€)-Number of Plants")
        if not df.empty and 'profit' in df.columns and 'plants_counter' in df.columns:
            chart6 = alt.Chart(df).mark_bar().encode(
                x = alt.X("year:O", title = "Year", axis = axis),
                y = alt.Y("profit:Q", title = "Profit (€)", axis = axis),
                tooltip = ["year", "profit", "plants_counter"]
            )
            
            line_chart = alt.Chart(df).mark_line(color = 'red').encode(
                x = "year:O",
                y = alt.Y("plants_counter", title = "Number of Plants", axis = alt.Axis(titleColor='red', title = "Number of Plants")),
                tooltip=["year","profit","plants_counter"]
            )
            
            # merge chart6 and line_chart and synchronize the X-axis
            combined_chart = alt.layer(chart6, line_chart).resolve_scale(
                y='independent' # the y-axes have two different value scales
            )

            sl.altair_chart(combined_chart, use_container_width=True)
        else:
            sl.info("Profit and plants data not available.")
        
        
        
        
            
        
        



   
    