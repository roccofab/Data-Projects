import os
import analyze_data as ad
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

save_dir = r"plots"
def orders_ship_state_chart(df, save_dir):
    """
    Generate a bar chart for the distribution of orders by ship-state.
    """
    state_sales = df.groupby('ship-state')['Qty'].sum()
    plt.figure(figsize=(12,6))
    plt.title("Distribution of the orders for ship-state")
    plt.xlabel('Ship State', fontsize = 12)
    plt.ylabel('Number Orders', fontsize = 12)
    yticks = [0,100,500,1000,1500,2000,2500,3000,3500,4000,4500,5000]
    plt.yticks(yticks, fontsize = 7)
    plt.xticks(rotation = 90, ha='center', fontsize = 7)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.32)
    plt.bar(state_sales.index, state_sales.values, color='skyblue', width=0.5)
    plt.savefig(os.path.join(save_dir, "distribution_ship_state.png"))
    plt.show()
    plt.gcf()
    plt.close()
    
def orders_ship_city_chart(df, save_dir):
    """
    Generate a bar chart for the distribution of orders by ship-city.
    The number of cities is limited to the top 20 cities with the most orders for better readability.
    """
    top20_ship_city = df['ship-city'].value_counts().nlargest(20)
    plt.figure(figsize =(8,4))
    plt.title("Distribution of the top 20 cities with the most orders")
    plt.xlabel('Ship City', fontsize = 12)
    plt.ylabel('Number Orders', fontsize = 12)
    yticks = [0,100,500,1000,1500,2000,2500,3000]
    plt.yticks(yticks, fontsize = 7) # Set y-axis ticks and font size
    plt.xticks(rotation = 75, ha='right', fontsize = 7) # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.30) # Adjust bottom margin
    plt.bar(top20_ship_city.index, top20_ship_city.values, color='skyblue', width= 0.5)
    plt.savefig(os.path.join(save_dir, "distribution_ship_city.png"))
    plt.show()
    plt.gcf()
    plt.close()
    
def orders_by_gender_chart(df, save_dir):
    """
     Calculate the total number of orders made by women and men and show it in a pie chart:
        to calculate the total number of orders by gender I count the Men and Women values ​​in the Gender column.
    This chart does not consider successful and unsuccessful orders but it is based on the total orders placed by different genders.
    """
    
    orders_gender = df['Gender'].value_counts() #total number of orders made by women and men
    plt.figure(figsize =(6,4))
    plt.title("Distribution of the orders for gender")
    explode = (0.01,0.01)
    plt.pie(orders_gender, explode=explode, labels = orders_gender.index, autopct='%1.1f%%', colors = ['#ff9999',"#f8f848"], startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(os.path.join(save_dir, "distribution_gender.png"))
    plt.show()
    plt.gcf()
    plt.close()
    
def orders_by_rangeAge(df,save_dir):
    """
    Show the distribution of the orders based on the range Age(5-18,19-30,31-40,41-50,51-60,61-70,71-80) in a bar chart.
    The age_range is calculated using the pd.cut() function to categorize the 'Age' column into specified bins.
    The chart displays the number of orders in each age range.
    """
    age_bins = [4,18,30,40,50,60,70,80]
    age_labels = ['5-18', '19-30', '31-40', '41-50', '51-60', '61-70', '71-80']
    age_range = pd.cut(df['Age'], bins = age_bins, labels = age_labels).value_counts().sort_index()
    plt.figure(figsize =(9,6))
    plt.title("Distribution of the orders based on the range Age")
    plt.xlabel('Age Range', fontsize = 12)
    plt.ylabel('Number Orders', fontsize = 12)
    yticks = [0,1000,2000,3000,4000,5000,6000,7000,8000]
    plt.yticks(yticks, fontsize = 7) 
    plt.xticks(rotation = 75, ha='right', fontsize = 7) 
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.30)
    plt.bar(age_range.index, age_range.values, color='skyblue', width= 0.5)
    plt.savefig(os.path.join(save_dir, "distribution_age.png"))
    plt.show()
    plt.gcf()
    plt.close()
    
def show_orders_status(df, save_dir):
    """
    Calculate the toal numbers of "Returned", "Delivered" and "Cancelled orders and show it in a pie chart:
    """
    returned = ad.calculate_returned_products(df)
    delivered = ad.calculate_delivered_products(df)
    cancelled = ad.calculate_cancelled_products(df)
    status_counts = pd.Series({
        'Returned': returned,
        'Delivered': delivered,
        'Cancelled': cancelled
    })
    plt.figure(figsize=(10, 6))
    plt.title("Distribution of the orders based on Status")
    explode = (0.15, 0.01, 0.01)
    plt.pie(status_counts, explode=explode, labels=status_counts.index, autopct='%1.1f%%', colors=['#ff9999', '#f8f848', '#85e085'], startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(os.path.join(save_dir, "distribution_status.png"))
    plt.show()
    plt.gcf()
    plt.close()
    
def monthly_average_sales_chart(df, save_dir):
    """
    Generate a bar chart of the average sales for each month.
    
    Compute the average daily sales for each month based on the 'Amount' column in df then
       compute the average of these aggregate daily sales for each month,to get average daily sales per month.

    Generate the bar chart where the x-axis is the name of the month(%b-%Y) and y-axis the daily average sales
        and at the top of each bar the exact value of the average sales of the month.
    """
    # cast Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    #total daily sales
    daily_total_sales = df.groupby(df['Date'].dt.date)['Amount'].sum()
    
    #cast index to datetime
    daily_total_sales.index = pd.to_datetime(daily_total_sales.index)

    #Group by month and calculate the average
    monthly_avg_daily_sales = daily_total_sales.groupby(daily_total_sales.index.to_period('M')).mean()
    
    # Cast PeriodIndex to string
    x_labels = monthly_avg_daily_sales.index.strftime('%b %Y').str.upper()
    
    plt.figure(figsize=(12, 6))
    plt.title("Mean Monthly sales", fontsize=14)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Mean sales', fontsize=12)
    bars = plt.bar(x_labels, monthly_avg_daily_sales.values, color='skyblue', width=0.6)
    
    # add values on the top of the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}',
                 ha='center', va='bottom')

    
    plt.xticks(rotation=45, ha='right') 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "monthly_average_sales_corrected.png"))
    plt.show()
    plt.gcf()
    plt.close()

