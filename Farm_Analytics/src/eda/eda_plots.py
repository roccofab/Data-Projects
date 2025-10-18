import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import seaborn as sn
from src.eda import eda_metrics as em
import datetime as dt

save_dir = "src/eda/Charts"
def netyield_per_hectare_plot():
    df = em.harvest_efficiency_per_year()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sn.barplot(x='year', y='net_yield_per_hectare', data=df, palette='mako', ax=ax)
    ax.set_title('Net Yield per Hectare Over Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Net Yield (Kg)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig 
def netyield_per_plant_plot():
    df = em.avg_yield_per_plant()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sn.barplot(x='year', y='avg_yield_per_plant', data=df, palette='mako', ax=ax)
    ax.set_title('Average Yield per Plant Over Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Avg. Yield (Kg)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig 
    
def top_lowest_production_plot():
    """
    Plots the top 5 and lowest 5 production years based on net harvest quantity side by side for comparison.
    """
    top5 = em.top5_production_years()
    low5 = em.lowest5_production_years()
    
    print("Top 5 production years:\n", top5[['year', 'net_qty', 'oil_yield']])
    print("Lowest 5 production years:\n", low5[['year', 'net_qty', 'oil_yield']])
    
    fig, ax = plt.subplots(2, 1, figsize=(10, 12))
    
    # Plot for the highest production years
    sn.barplot(x='year', y='net_qty', data=top5, ax=ax[0], palette='mako')
    ax[0].set_title('Top 5 Years with the Highest Net Harvest Quantity')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Net Qty (Kg)')

    # formatter to avoid scientific notation on y-axis in the first subplot
    formatter = ScalarFormatter(useOffset=False)
    formatter.set_scientific(False)
    ax[0].yaxis.set_major_formatter(formatter)

    # Plot for the lowest production years
    sn.barplot(x='year', y='net_qty', data=low5, ax=ax[1], palette='mako')
    ax[1].set_title('Lowest 5 Years with the Lowest Net Harvest Quantity')
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Net Qty (Kg)')

    # formatter to avoid scientific notation on y-axis in the second subplot
    ax[1].yaxis.set_major_formatter(formatter)

    plt.tight_layout()
    plt.savefig(f"{save_dir}/top_lowest_production_years.png")
    plt.close()
def oil_yield_trend_plot():
    df = em.oil_yield_per_year()
    
    years = list(range(df['year'].min(), df['year'].max() + 1))
    
    plt.figure(figsize = (10,6))
    sn.lineplot(x = 'year', y = 'oil_yield_per_hectare', data = df, marker='o', color=(0.2, 0.3, 0.9))
    plt.vlines(df['year'], 0, df['oil_yield_per_hectare'], linestyles='dashed', colors='gray', alpha=0.7)  
    plt.title('Oil Yield per Hectare Over Years')
    plt.xlabel('Year')
    plt.ylabel('Oil Yield (Kg)')
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/oil_yield_per_hectare.png")
    plt.close()
    
def oil_price_per_year():
        df = em.get_production_data().copy()
        
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        if current_month < 10:
            df = df[df["year"] < current_year]
        
        df['oil_price_per_kg'] = df['oil_revenue'] / df['oil_yield']
        
        years = list(range(df['year'].min(), df['year'].max() + 1))
        
        plt.figure(figsize = (10,6))
        sn.lineplot(x = 'year', y = 'oil_price_per_kg', data = df, marker='o', color=(0.2, 0.3, 0.9))
        plt.vlines(df['year'], 0, df['oil_price_per_kg'], linestyles='dashed', colors='gray', alpha=0.7)
        plt.title('Oil Price per Kg Over Years')
        plt.xlabel('Year')
        plt.ylabel('Oil Price per Kg (€)')
        plt.xticks(years, rotation=45)
        plt.tight_layout()
        plt.savefig(f"{save_dir}/oil_price_per_kg.png")
        plt.close()
        
def cost_per_liter_oil_plot():
    df = em.cost_per_l_oil()
    years = list(range(df['year'].min(), df['year'].max() + 1))
    
    plt.figure(figsize=(10,6))
    sn.lineplot(x = 'year', y = 'cost_per_liter_oil', data = df, marker = 'o', color = (0.2, 0.3, 0.9))
    plt.vlines(df['year'], 0, df['cost_per_liter_oil'], linestyle = 'dashed', colors = 'gray', alpha = 0.7)
    plt.title('Cost to Produce 1 Liter of Oil Over Years')
    plt.xlabel('Year')
    plt.ylabel('Cost per Liter of Oil (€)')
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/cost_per_liter_oil.png")
    plt.close()
    
def cost_per_ton_yield_plot():
    df = em.cost_per_ton_yield()
    years = list(range(df['year'].min(), df['year'].max() + 1))
    
    plt.figure(figsize=(10,6))
    sn.lineplot(x = 'year', y = 'cost_per_ton_yield', data = df, marker = 'o', color = (0.2, 0.3, 0.9))
    plt.vlines(df['year'], 0, df['cost_per_ton_yield'], linestyle = 'dashed', colors = 'gray', alpha = 0.7)
    plt.title('Cost per Ton of Yield Over Years')
    plt.xlabel('Year')
    plt.ylabel('Cost per Ton of Yield (€)')
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/cost_per_ton_yield.png")
    plt.close()
def cost_per_kg_yield_plot():
    df = em.cost_per_kg_yield()
    years = list(range(df['year'].min(), df['year'].max() + 1))
    
    plt.figure(figsize=(10,6))
    sn.lineplot(x = 'year', y = 'cost_per_kg_yield', data = df, marker = 'o', color = (0.2, 0.3, 0.9))
    plt.vlines(df['year'], 0, df['cost_per_kg_yield'], linestyle = 'dashed', colors = 'gray', alpha = 0.7)
    plt.title('Cost per Kg of Yield Over Years')
    plt.xlabel('Year')
    plt.ylabel('Cost per Kg of Yield (€)')
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/cost_per_kg_yield.png")
    plt.close()
    
def profit_per_year_plot():
    try:
        consumption = em.get_consumption_data()
        production = em.get_production_data()
        df = pd.merge(consumption, production, on='year', how='inner')
        years = list(range(df['year'].min(), df['year'].max() + 1))
         
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:
            df = df[df['year'] < current_year]
            
        df['total_expenses'] = (
            df['irrigation_expenses'] +
            df['fertilizer_costs'] +
            df['pesticide_costs'] +
            df['maintenance_expenses']
        )
        df['profit'] = df['oil_revenue'] - df['total_expenses']
        
        plt.figure(figsize=(10,6))
        sn.lineplot(x = 'year', y = 'profit', data = df, marker = 'o', color = (0.2, 0.3, 0.9))
        plt.vlines(df['year'], 0, df['profit'], linestyle = 'dashed', colors = 'gray', alpha = 0.7)
        plt.title('Profit Over Years')
        plt.xlabel('Year')
        plt.ylabel('Profit (€)')
        plt.xticks(years, rotation=45)
        plt.tight_layout()
        plt.savefig(f"{save_dir}/profit_per_year.png")
        plt.close()
        
    except Exception as e:
        print(f"Error calculating profit per year: {e}")
        return
        
def profit_per_hectare_plot():
    df = em.profit_per_hectare()
    years = list(range(df['year'].min(), df['year'].max() + 1))
    
    plt.figure(figsize=(10,6))
    sn.lineplot(x = 'year', y = 'profit_per_hectare', data = df, marker = 'o', color = (0.2, 0.3, 0.9))
    plt.vlines(df['year'], 0, df['profit_per_hectare'], linestyle = 'dashed', colors = 'gray', alpha = 0.7)
    plt.title('Profit per Hectare Over Years')
    plt.xlabel('Year')
    plt.ylabel('Revenue per Hectare (€)')
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/profit_per_hectare.png")
    plt.close()

def top_lowest_profit_plot():
    top5 = em.top5_highest_profit_years()
    low5 = em.top5_lowest_profit_years()
    fig, ax = plt.subplots(2, 1, figsize=(10, 12))
    

    # Plot for the highest profit years
    sn.barplot(x='year', y='profit', data=top5, ax=ax[0], palette='mako')
    ax[0].set_title('Top 5 Years with the Highest Profit')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Profit (€)')

    # Plot for the lowest profit years
    sn.barplot(x='year', y='profit', data=low5, ax=ax[1], palette='mako')
    ax[1].set_title('Top 5 Years with the Lowest Profit')
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Profit (€)')

    plt.tight_layout()
    plt.savefig(f"{save_dir}/top_lowest_profit_years.png")
    plt.close()
    
def harvestDays_vs_surface_plot():
    df = em.get_production_data()
    
    current_year = dt.date.today().year
    current_month = dt.date.today().month
    if current_month < 10:
        df = df[df["year"] < current_year]
        
    df['surface_area_ha'] = df['surface_area_in_m2'] / 10000  # Convert m2 to hectares
    
    plt.figure(figsize=(10, 6))
    sn.scatterplot(x='surface_area_ha', y='harvest_days', data=df, color='tab:blue', s=100)
    plt.title('Harvest Days vs Surface Area')
    plt.xlabel('Surface Area (Hectares)')
    plt.ylabel('Harvest Days')
    plt.tight_layout()
    plt.savefig(f"{save_dir}/harvestDays_vs_surface.png")
    plt.close()
    
def plants_per_year_plot():
    df = em.get_production_data().sort_values(by = 'year').copy()
    df["new_plants"] = df["plants_counter"].diff().fillna(0)  # Calculate new plants per year by taking the difference between consecutive years
    df["new_plants"] = df["new_plants"].apply(lambda x: x if x > 0 else 0)  # Set negative values to 0
    
    plt.figure(figsize=(10, 6))
    sn.barplot(x='year', y='new_plants', data=df, palette='mako')
    plt.title('Number of New Plants Grown Each Year')
    plt.xlabel('Year')
    plt.ylabel('Number of New Plants')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/new_plants_per_year.png")
    plt.close()
    
def expenses_per_year_plot():
    df = em.get_consumption_data().copy()
    
    current_year = dt.date.today().year
    current_month = dt.date.today().month
    #excludes the current year if the month of October has not yet been reached
    if current_month < 10:   
        df = df[df["year"] < current_year]
        
    df['total_expenses'] = df[['irrigation_expenses', 'fertilizer_costs', 'pesticide_costs', 'maintenance_expenses']].sum(axis = 1)
    years = list(range(df['year'].min(), df['year'].max() + 1))
    plt.figure(figsize = (10,6))
    sn.scatterplot(x='year', y='total_expenses', data=df, color='tab:blue', s=120)
    plt.title('Total Expenses Over Years')
    plt.xlabel('Year')
    plt.ylabel('Total Expenses (€)')
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/total_expenses_per_year.png")
    plt.close()
    
def mostExpensive_leastExpensive_years_plot():
    most_expensive = em.most_expensive_year_vs_yield()
    least_expensive = em.least_expensive_years_vs_yield()
    
    df = pd.concat([most_expensive, least_expensive], ignore_index=True)
    
    total = df["total_expenses"].sum()
    df["percentage"] = df["total_expenses"] / total * 100
    labels = [
        f"{row['year']} ({row['percentage']:.1f}%)"
        for _, row in df.iterrows()
    ]
    
    plt.figure(figsize=(7, 7))
    plt.pie(
        df["total_expenses"],
        labels=labels,
        autopct='%1.1f%%',     
        startangle=90,         
        counterclock=False     # Clockwise direction
    )
    plt.title("Most Expensive Years and Least Expensive Years")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/most_least_expensive_years.png")
    plt.close()
    
def treatments_expenses_years_plot():
    df = em.get_consumption_data()
    df['cost_treatments'] = df[['fertilizer_costs', 'pesticide_costs']].sum(axis = 1)
    
    current_year = dt.date.today().year
    current_month = dt.date.today().month
    #excludes the current year if the month of October has not yet been reached
    if current_month < 10:   
        df = df[df["year"] < current_year]
        
    plt.figure(figsize=(10, 6))
    sn.barplot(x='year', y='cost_treatments', data=df, palette='mako')
    plt.title('Cost of Soil and Plants Treatments Over Years(fertilizers + pesticides)')
    plt.xlabel('Year')
    plt.ylabel('Treatments expenses (€)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/treatments_expenses_years.png")
    plt.close()
    
def fertilizer_required_years_plot():
    df = em.get_consumption_data()
    
    current_year = dt.date.today().year
    current_month = dt.date.today().month
    #excludes the current year if the month of October has not yet been reached
    if current_month < 10:   
        df = df[df["year"] < current_year]
        
    plt.figure(figsize=(10, 6))
    sn.barplot(x='year', y='fertilizer_required_kg', data=df, palette='mako')
    plt.title('Fertilizer Required Over Years')
    plt.xlabel('Year')
    plt.ylabel('Fertilizer Quantity (Kg)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/fertilizer_required_years.png")
    plt.close()
    
def pesticide_required_years_plot():
    df = em.get_consumption_data()
    
    current_year = dt.date.today().year
    current_month = dt.date.today().month
    #excludes the current year if the month of October has not yet been reached
    if current_month < 10:   
        df = df[df["year"] < current_year]
        
    plt.figure(figsize=(10, 6))
    sn.barplot(x='year', y='pesticide_required_kg', data=df, palette='mako')
    plt.title('Pesticide Required Over Years')
    plt.xlabel('Year')
    plt.ylabel('Pesticide Quantity (Kg)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/pesticide_required_years.png")
    plt.close()
    
def irrigation_required_years_plot():
    df = em.get_consumption_data()
    
    current_year = dt.date.today().year
    current_month = dt.date.today().month
    #excludes the current year if the month of October has not yet been reached
    if current_month < 10:   
        df = df[df["year"] < current_year]
        
    plt.figure(figsize=(10, 6))
    sn.barplot(x='year', y='irrigation_required_m3', data=df, palette='mako')
    plt.title('Irrigation Water Required Over Years')
    plt.xlabel('Year')
    plt.ylabel('Irrigation Water (m³)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/irrigation_required_years.png")
    plt.close()
    
def prod_weather_corr_heatmap():
    prod = em.get_production_data()
    weather = em.aggregate_weather_data()
    df = pd.merge(prod, weather, on='year')
    corr = df[['net_qty', 'oil_yield',
               'avg_temp', 'total_precip', 'avg_wind']].corr()
    
    plt.figure(figsize=(8, 6))
    sn.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Correlation Heatmap: Production and Weather Variables')
    plt.tight_layout()
    plt.savefig(f"{save_dir}/prod_weather_corr_heatmap.png")
    plt.close()
    
def prod_cons_weather_corr_heatmap():
    prod = em.get_production_data()
    cons = em.get_consumption_data()
    weather = em.aggregate_weather_data()
    cons['treatments_required_kg'] = cons['fertilizer_required_kg'] + cons['pesticide_required_kg']
    df = pd.merge(prod, cons, on='year')
    df = pd.merge(df, weather, on='year')
    corr = df[['net_qty', 'oil_yield',
               'treatments_required_kg', 'irrigation_required_m3', 'maintenance_expenses',
               'avg_temp', 'total_precip', 'avg_wind']].corr()
    
    plt.figure(figsize=(10, 8))
    sn.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Correlation Heatmap: Production, Consumption and Weather Variables')
    plt.tight_layout()
    plt.savefig(f"{save_dir}/prod_cons_weather_corr_heatmap.png")
    plt.close()
    