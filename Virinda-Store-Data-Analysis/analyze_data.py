import pandas as pd
import numpy as np
"""
    in the file some KPI are calculated, the main descriptive statistical analyses,
    statistical distributions and their charts.
    KPI:
        - Sales KPI: total number of orders, mean value of size of ordered cycles,
                     number of products returned-cancelled-delivered.
                     
        
        - Clients KPI: number of unique clients, mean order value per client, 
                       number of sales grouped by gender Men and by gender Women,
                       number of sales grouped by Age Group.
                       
        - Geographic KPI: Number of sales in the city with the most shipments made,
                          number of sales in the state with the most shipments made.
        
        - Time KPI: mean monthly sales, mean daily sales, sales month peak.
        
    DISTRIBUTIONS:
        - Distribution of the orders by ship-state. 
        - Distribution of the orders by ship-city.
        - Distribution of the orders by gender.
        - Distribution of the orders by gender-Age Group-ship-state.
        - Distribution of the orders based on the range Age(5-18,19-30,31-40,41-50,51-60,61-70,71-80).
        - Distribution of the orders based on the range Age and Gender.
"""

def calculate_orders(df):
    #calculate the total number of orders by counting the unique rows of the column SKU
    return int(df['SKU'].nunique())

def calculate_revenue(df):
    #calculate total revenue of the store:
    return df['Amount'].sum().round(2)

def calculate_mean_size(df):
    #calculate the total number of ordered products based on the Size column
    total_qty_per_size = df.groupby('Size')['Qty'].sum()
    return total_qty_per_size
def calculate_returned_products(df):
    #calculate the total number of returned products
    return int(df[df['Status'] == 'Returned']['Qty'].sum())

def calculate_delivered_products(df):
    #calculate the total number of delivered products
    return int(df[df['Status'] == 'Delivered']['Qty'].sum())

def calculate_cancelled_products(df):
    #calculate the total number of cancelled products
    return int(df[df['Status'] == 'Cancelled']['Qty'].sum())

def calculate_number_clients(df):
    #calculate the total number of unique clients based on Cust ID column
    return int(df['Cust ID'].nunique())

def mean_order_per_client(df):
    """
    calculate the mean order value of the clients based on Cust ID and Amount columns
        then show the top 10 clients with the highest mean order value:
    """
    mean_order = df.groupby('Cust ID')['Amount'].mean()
    top_10_clients = mean_order.nlargest(10)
    print(top_10_clients)
    return round(mean_order.mean(),2)


def calculate_sales_by_genderM(df):
    """
    Calculate the total number of products and the total turnover obtained by sales To Men.
    The method filters the dataframe for rows where the value of Gender is 'Men'.
    The method returns a Series composed by 2 rows: the total number of products ordered by men and the total
       amount of money spent by men.
    
    """
    filtered = df[df['Gender'] == 'Men']
    return pd.Series({
        'Qty': filtered['Qty'].sum(),
        'Amount': filtered['Amount'].sum()
    })

def calculate_sales_by_genderW(df):
    """
    Calculate the total number of products and the total turnover obtained by sales To Women.
    The method filters the dataframe for rows where the value of Gender is 'women'.
    The method returns a Series composed by 2 rows: the total number of products ordered by women and the total
       amount of money spent by women.
    
    """
    filtered = df[df['Gender'] == 'Women']
    return pd.Series({
        'Qty': filtered['Qty'].sum(),
        'Amount': filtered['Amount'].sum()
    })

def highest_city_sales(df):
    """
    calculate the city and the number of sales of the city with the most shipments made:
       first group by ship-city and Qty,calculate the max value and then return the city and the number of sales
    """
    cities_sales = df.groupby('ship-city')['Qty'].sum()
    top_city_sales = cities_sales.idxmax()
    top_num_sales = cities_sales.max()
    return top_city_sales, top_num_sales

def highest_state_sales(df):
    #calculate the state and the number of sales in the state with the most shipments made:
    state_sales = df.groupby('ship-state')['Qty'].sum()
    top_state_sales = state_sales.idxmax()
    top_num_sales = state_sales.max()
    return top_state_sales, top_num_sales


def calculate_sales_per_state(df):
    #calculate the number of sales per state
    return df.groupby('Ship State')['Qty'].sum()

def mean_montly_sales(df):
    """
    calculate the mean value of monthly sales:
        first convert Date to datetime values,
        calculate monthly total sales by grouping for date(full date must be converted to month using the pandas function to_period())
            and Amount.
        calculate the mean value of the monthly sales
    """
    montly_total_sales = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
    mean_montly_sales = montly_total_sales.mean()
    return round(mean_montly_sales, 2)
    
def mean_daily_sales(df):
    """
    This method has the same logic of the previous method(mean_montly_sales) but the grouping is performed on columns:
       Date(full date must be converted to days using the pandas function to_period()) and Amount
    """
    daily_total_sales = df.groupby(df['Date'].dt.date)['Amount'].sum()
    daily_sales_mean = daily_total_sales.mean()
    return round(daily_sales_mean, 2)

def sales_month_peak(df):
    #calculate the peak of the month having the highest revenue
    montly_total_sales =  df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
    peak_month = montly_total_sales.idxmax()
    peak_value = montly_total_sales.max()
    return f"{str(peak_month)}: {peak_value}"


def orders_by_genderAge_GroupShipState(df):
    #normalize the values for ship-state,Age Group and Gender and show the distribution of the orders for gender-Age Group-ship-state:
    print(df.groupby(['Gender', 'Age Group', 'ship-state']).size().unstack())
    

def orders_by_rangeAge(df):
    #show the distribution of the orders based on the range Age(5-18,19-30,31-40,41-50,51-60,61-70,71-80):
    age_bins = [4,18,30,40,50,60,70,80]
    age_labels = ['5-18', '19-30', '31-40', '41-50', '51-60', '61-70', '71-80']
    age_range = pd.cut(df['Age'], bins = age_bins, labels = age_labels).value_counts().sort_index()
    age_range = age_range.astype(int)  
    print("\nDistribution of the orders based on the range Age:\n")
    print(age_range)
    return age_range
    
def orders_by_rangeAge_Gender(df):
    age_gender_distribution = df.groupby(['Age Group', 'Gender']).size().unstack()
    age_gender_distribution = age_gender_distribution.astype(int)
    print("\nDistribution of the orders based on the range Age and Gender:\n")
    print(age_gender_distribution)





def calculate_correlations_matrix(df):
    # Calculate the Pearson correlation between the numeric variables Age, Qty, Amount, ship-postal-code of a dataframe
    numeric_columns = ['Age', 'Qty', 'Amount', 'ship-postal-code']
    correlation_matrix = df[numeric_columns].corr()
    return correlation_matrix

def calculate_spearman_matrix(df):
    #calculate the spearman correlation matrix between the numeric variables Age, Qty, Amount, ship-postal-code of a dataframe 
    spearman_matrix = df[['Age', 'Qty', 'Amount']].corr(method = 'spearman')
    return spearman_matrix


def analyze_temporal_trends(df):
    """
    Analyze temporal trends in sales data.
    This function processes a DataFrame containing sales data with a 'Date' column and an 'Amount' column.
    It performs the following analyses:
        - Converts the 'Date' column to datetime format.
        - Aggregates sales amounts by month.
        - Calculates a 3-month rolling mean of monthly sales.
        - Computes the month-over-month percentage growth rate of sales.
    Parameters:
        df (pandas.DataFrame): Input DataFrame with at least 'Date' and 'Amount' columns.
    Returns:
        tuple: A tuple containing:
            - str: Description for monthly sales.
            - pandas.Series: Monthly aggregated sales.
            - str: Description for 3-month rolling mean sales.
            - pandas.Series: 3-month rolling mean of monthly sales.
            - str: Description for monthly growth rate.
            - pandas.Series: Month-over-month percentage growth rate of sales.
    """
   
    df['Date'] = pd.to_datetime(df['Date']) #cast the variable Date to datetime
    
    
    monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum() #monthly sales
    
    
    rolling_mean = monthly_sales.rolling(window=3).mean()  #rolling mean of 3 months
    
    
    growth_rate = monthly_sales.pct_change() * 100  #monthly increment rate of the sales
    
    return (
        "Monthly sales: ", monthly_sales,
        "\nRolling mean sales of 3 months: ",  rolling_mean,
        "\nMonthly growth rate: ", growth_rate
    )

def get_top_customers(df, n=10):
    """
    Identify the top clients
    """
    
    customer_frequency = df.groupby('Cust ID').size()  #calculate customer purchase frequency
    
   
    customer_value = df.groupby('Cust ID')['Amount'].sum() #calculate customers order value
    
    
    customer_metrics = pd.DataFrame({  #The customer metrics dataframe contains the customer frequency and customer value variables 
        'frequency': customer_frequency,
        'total_value': customer_value
    })
    
    #sort the dataframe by frequency in descending order and take the first 10 rows
    top_customers = customer_metrics.sort_values('frequency', ascending=False).head(n) 
    
    return top_customers

def showTextMetrics(df):
    """
    Show text KPIs in a text box
    """
    # get only the name of the state and the name of the city with the most shipments made
    most_fluent_state = highest_state_sales(df)[0]
    most_fluent_city = highest_city_sales(df)[0]
    
    # format values for sales by gender men and sales by gender women
    men_sales = calculate_sales_by_genderM(df)
    women_sales = calculate_sales_by_genderW(df)
    
    men_sales_str = f"Qty: {men_sales['Qty']} Amount: {men_sales['Amount']}"
    women_sales_str = f"Qty: {women_sales['Qty']} Amount: {women_sales['Amount']}"
    
    # Format bike sizes data as a dictionary with new lines
    bike_sizes = calculate_mean_size(df).to_dict()
    bike_sizes_str = "\n".join([f"{size}: {qty}" for size, qty in bike_sizes.items()])
    
    text_metrics = {
        "Peak sales month": sales_month_peak(df),
        "Number of bikes sold by size": bike_sizes_str,
        "Sales by gender Men": men_sales_str,
        "Sales by gender Women": women_sales_str,
        "Most fluent city": most_fluent_city,
        "Most fluent state": most_fluent_state
    }
    return text_metrics

def showNumericKPI(df):
    """
    store the numeric KPI in a dictionary
    """
    numeric_kpi = {
        "Total orders": calculate_orders(df),
        "Avg. monthly sales": mean_montly_sales(df),
        "Avg. daily sales": mean_daily_sales(df),
        "Orders successfully delivered": calculate_delivered_products(df),
        "Orders returned": calculate_returned_products(df),
        "Cancelled orders": calculate_cancelled_products(df),
        "Number of clients": calculate_number_clients(df),
        "Avg. order per client": mean_order_per_client(df)
    }
    return numeric_kpi

def calculate_amazon_metrics(df):
    """
    Calculate key metrics for the Amazon sales channel using the data available in the dataset.
    """
    amazon_data = df[df['Channel '] == 'Amazon']
    
    #calculate the main metrics
    metrics = {
        'Total Revenue': amazon_data['Amount'].sum(),
        'Total number of orders': amazon_data['SKU'].nunique(),
        'Average order value': amazon_data['Amount'].mean(),
        'Delivered orders': amazon_data[amazon_data['Status'] == 'Delivered']['Qty'].sum(),
        'Returned orders': amazon_data[amazon_data['Status'] == 'Returned']['Qty'].sum(),
        'Cancelled orders': amazon_data[amazon_data['Status'] == 'Cancelled']['Qty'].sum(),
        'Orders delivered rate': (amazon_data[amazon_data['Status'] == 'Delivered']['Qty'].sum() / amazon_data['Qty'].sum()) ,
        'Orders returned rate': (amazon_data[amazon_data['Status'] == 'Returned']['Qty'].sum() / amazon_data['Qty'].sum()) ,
        'Women orders': amazon_data[amazon_data['Gender'] == 'Women']['Qty'].sum(),
        'Women orders percentage': (amazon_data[amazon_data['Gender'] == 'Women']['Qty'].sum() / amazon_data['Qty'].sum()) ,
        'Men orders': amazon_data[amazon_data['Gender'] == 'Men']['Qty'].sum(),
        'Men orders percentage': (amazon_data[amazon_data['Gender'] == 'Men']['Qty'].sum() / amazon_data['Qty'].sum()) ,
        'Teenagers orders': amazon_data[amazon_data['Age Group'] == 'Teenagers']['Qty'].sum(),
        'Teenagers orders percentage': (amazon_data[amazon_data['Age Group'] == 'Teenagers']['Qty'].sum() / amazon_data['Qty'].sum()) ,
        'Adults orders': amazon_data[amazon_data['Age Group'] == 'Adults']['Qty'].sum(),
        'Adults orders percentage': (amazon_data[amazon_data['Age Group'] == 'Adults']['Qty'].sum() / amazon_data['Qty'].sum()),
        'Senior orders': amazon_data[amazon_data['Age Group'] == 'Senior']['Qty'].sum(),
        'Senior orders percentage': (amazon_data[amazon_data['Age Group'] == 'Senior']['Qty'].sum() / amazon_data['Qty'].sum())
    }
    
    return metrics

def calculate_Myntra_metrics(df):
    """
    Calculate key metrics for the Myntra sales channel using the data available in the dataset.
    """
    myntra_data = df[df['Channel '] == 'Myntra']
    
    metrics = {
        'Total Revenue': myntra_data['Amount'].sum(),
        'Total number of orders': len(myntra_data),
        'Average order value': myntra_data['Amount'].mean(),
        'Delivered orders': myntra_data[myntra_data['Status'] == 'Delivered']['Qty'].sum(),
        'Returned orders': myntra_data[myntra_data['Status'] == 'Returned']['Qty'].sum(),
        'Cancelled orders': myntra_data[myntra_data['Status'] == 'Cancelled']['Qty'].sum(),
        'Orders delivered rate': (myntra_data[myntra_data['Status'] == 'Delivered']['Qty'].sum() / myntra_data['Qty'].sum()) ,
        'Orders returned rate': (myntra_data[myntra_data['Status'] == 'Returned']['Qty'].sum() / myntra_data['Qty'].sum()) ,
        'Women orders': myntra_data[myntra_data['Gender'] == 'Women']['Qty'].sum(),
        'Women orders percentage': (myntra_data[myntra_data['Gender'] == 'Women']['Qty'].sum() / myntra_data['Qty'].sum()) ,
        'Men orders' : myntra_data[myntra_data['Gender'] == 'Men']['Qty'].sum(),
        'Men orders percentage' : (myntra_data[myntra_data['Gender'] == 'Men']['Qty'].sum() / myntra_data['Qty'].sum()),
        'Teenagers orders' : myntra_data[myntra_data['Age Group'] == 'Teenagers']['Qty'].sum(),
        'Teenagers orders percentage' : (myntra_data[myntra_data['Age Group'] == 'Teenagers']['Qty'].sum() / myntra_data['Qty'].sum()) ,
        'Adults orders' : myntra_data[myntra_data['Age Group'] == 'Adults']['Qty'].sum(),
        'Adults orders percentage' : (myntra_data[myntra_data['Age Group'] == 'Adults']['Qty'].sum() / myntra_data['Qty'].sum()),
        'Senior orders' : myntra_data[myntra_data['Age Group'] == 'Senior']['Qty'].sum(),
        'Senior orders percentage' : (myntra_data[myntra_data['Age Group'] == 'Senior']['Qty'].sum() / myntra_data['Qty'].sum()) 
     }
    
    return metrics 

def calculate_Ajio_metrics(df):
    """
    Calculate key metrics for the Ajio sales channel using the data available in the dataset.
    """
    Ajio_data = df[df['Channel '] == 'Ajio']
    metrics = {
        'Total Revenue': Ajio_data['Amount'].sum(),
        'Total number of orders': len(Ajio_data),
        'Average order value': Ajio_data['Amount'].mean(),
        'Delivered orders': Ajio_data[Ajio_data['Status'] == 'Delivered']['Qty'].sum(),
        'Returned orders': Ajio_data[Ajio_data['Status'] == 'Returned']['Qty'].sum(),
        'Cancelled orders': Ajio_data[Ajio_data['Status'] == 'Cancelled']['Qty'].sum(),
        'Orders delivered rate': (Ajio_data[Ajio_data['Status'] == 'Delivered']['Qty'].sum() / Ajio_data['Qty'].sum()) ,
        'Orders returned rate': (Ajio_data[Ajio_data['Status'] == 'Returned']['Qty'].sum() / Ajio_data['Qty'].sum()) ,
        'Women orders': Ajio_data[Ajio_data['Gender'] == 'Women']['Qty'].sum(),
        'Women orders percentage': (Ajio_data[Ajio_data['Gender'] == 'Women']['Qty'].sum() / Ajio_data['Qty'].sum()) ,
        'Men orders' : Ajio_data[Ajio_data['Gender'] == 'Men']['Qty'].sum(),
        'Men orders percentage' : (Ajio_data[Ajio_data['Gender'] == 'Men']['Qty'].sum() / Ajio_data['Qty'].sum()),
        'Teenagers orders' : Ajio_data[Ajio_data['Age Group'] == 'Teenagers']['Qty'].sum(),
        'Teenagers orders percentage' : (Ajio_data[Ajio_data['Age Group'] == 'Teenagers']['Qty'].sum() / Ajio_data['Qty'].sum()) ,
        'Adults orders' : Ajio_data[Ajio_data['Age Group'] == 'Adults']['Qty'].sum(),
        'Adults orders percentage' : (Ajio_data[Ajio_data['Age Group'] == 'Adults']['Qty'].sum() / Ajio_data['Qty'].sum()),
        'Senior orders' : Ajio_data[Ajio_data['Age Group'] == 'Senior']['Qty'].sum(),
        'Senior orders percentage' : (Ajio_data[Ajio_data['Age Group'] == 'Senior']['Qty'].sum() / Ajio_data['Qty'].sum()) 
     }
    
    return metrics 
    
    

    
def calculate_Flipkart_metrics(df):
    """
    Calculate key metrics for the Flipkart sales channel using the data available in the dataset.
    """
    flipkart_data = df[df['Channel '] == 'Flipkart']
    metrics = {
        'Total Revenue': flipkart_data['Amount'].sum(),
        'Total number of orders': len(flipkart_data),
        'Average order value': flipkart_data['Amount'].mean(),
        'Delivered orders': flipkart_data[flipkart_data['Status'] == 'Delivered']['Qty'].sum(),
        'Returned orders': flipkart_data[flipkart_data['Status'] == 'Returned']['Qty'].sum(),
        'Cancelled orders': flipkart_data[flipkart_data['Status'] == 'Cancelled']['Qty'].sum(),
        'Orders delivered rate': (flipkart_data[flipkart_data['Status'] == 'Delivered']['Qty'].sum() / flipkart_data['Qty'].sum()),
        'Orders returned rate': (flipkart_data[flipkart_data['Status'] == 'Returned']['Qty'].sum() / flipkart_data['Qty'].sum()),
        'Women orders': flipkart_data[flipkart_data['Gender'] == 'Women']['Qty'].sum(),
        'Women orders percentage': (flipkart_data[flipkart_data['Gender'] == 'Women']['Qty'].sum() / flipkart_data['Qty'].sum()),
        'Men orders': flipkart_data[flipkart_data['Gender'] == 'Men']['Qty'].sum(),
        'Men orders percentage': (flipkart_data[flipkart_data['Gender'] == 'Men']['Qty'].sum() / flipkart_data['Qty'].sum()),
        'Teenagers orders': flipkart_data[flipkart_data['Age Group'] == 'Teenagers']['Qty'].sum(),
        'Teenagers orders percentage': (flipkart_data[flipkart_data['Age Group'] == 'Teenagers']['Qty'].sum() / flipkart_data['Qty'].sum()),
        'Adults orders': flipkart_data[flipkart_data['Age Group'] == 'Adults']['Qty'].sum(),
        'Adults orders percentage': (flipkart_data[flipkart_data['Age Group'] == 'Adults']['Qty'].sum() / flipkart_data['Qty'].sum()),
        'Senior orders': flipkart_data[flipkart_data['Age Group'] == 'Senior']['Qty'].sum(),
        'Senior orders percentage': (flipkart_data[flipkart_data['Age Group'] == 'Senior']['Qty'].sum() / flipkart_data['Qty'].sum())
    }
    return metrics

def calculate_Meesho_metrics(df):
    """
    Calculate key metrics for the Meesho sales channel using the data available in the dataset.
    """
    meesho_data = df[df['Channel '] == 'Meesho']
    metrics = {
        'Total Revenue': meesho_data['Amount'].sum(),
        'Total number of orders': len(meesho_data),
        'Average order value': meesho_data['Amount'].mean(),
        'Delivered orders': meesho_data[meesho_data['Status'] == 'Delivered']['Qty'].sum(),
        'Returned orders': meesho_data[meesho_data['Status'] == 'Returned']['Qty'].sum(),
        'Cancelled orders': meesho_data[meesho_data['Status'] == 'Cancelled']['Qty'].sum(),
        'Orders delivered rate': (meesho_data[meesho_data['Status'] == 'Delivered']['Qty'].sum() / meesho_data['Qty'].sum()) ,
        'Orders returned rate': (meesho_data[meesho_data['Status'] == 'Returned']['Qty'].sum() / meesho_data['Qty'].sum()),
        'Women orders': meesho_data[meesho_data['Gender'] == 'Women']['Qty'].sum(),
        'Women orders percentage': (meesho_data[meesho_data['Gender'] == 'Women']['Qty'].sum() / meesho_data['Qty'].sum()),
        'Men orders': meesho_data[meesho_data['Gender'] == 'Men']['Qty'].sum(),
        'Men orders percentage': (meesho_data[meesho_data['Gender'] == 'Men']['Qty'].sum() / meesho_data['Qty'].sum()),
        'Teenagers orders': meesho_data[meesho_data['Age Group'] == 'Teenagers']['Qty'].sum(),
        'Teenagers orders percentage': (meesho_data[meesho_data['Age Group'] == 'Teenagers']['Qty'].sum() / meesho_data['Qty'].sum()),
        'Adults orders': meesho_data[meesho_data['Age Group'] == 'Adults']['Qty'].sum(),
        'Adults orders percentage': (meesho_data[meesho_data['Age Group'] == 'Adults']['Qty'].sum() / meesho_data['Qty'].sum()),
        'Senior orders': meesho_data[meesho_data['Age Group'] == 'Senior']['Qty'].sum(),
        'Senior orders percentage': (meesho_data[meesho_data['Age Group'] == 'Senior']['Qty'].sum() / meesho_data['Qty'].sum())
    }
    return metrics

def calculate_Others_metrics(df):
    """
    Calculate key metrics for the Others sales channel using the data available in the dataset.
    """
    others_data = df[df['Channel '] == 'Others']
    metrics = {
        'Total Revenue': others_data['Amount'].sum(),
        'Total number of orders': len(others_data),
        'Average order value': others_data['Amount'].mean(),
        'Delivered orders': others_data[others_data['Status'] == 'Delivered']['Qty'].sum(),
        'Returned orders': others_data[others_data['Status'] == 'Returned']['Qty'].sum(),
        'Cancelled orders': others_data[others_data['Status'] == 'Cancelled']['Qty'].sum(),
        'Orders delivered rate': (others_data[others_data['Status'] == 'Delivered']['Qty'].sum() / others_data['Qty'].sum()),
        'Orders returned rate': (others_data[others_data['Status'] == 'Returned']['Qty'].sum() / others_data['Qty'].sum()) ,
        'Women orders': others_data[others_data['Gender'] == 'Women']['Qty'].sum(),
        'Women orders percentage': (others_data[others_data['Gender'] == 'Women']['Qty'].sum() / others_data['Qty'].sum()) ,
        'Men orders': others_data[others_data['Gender'] == 'Men']['Qty'].sum(),
        'Men orders percentage': (others_data[others_data['Gender'] == 'Men']['Qty'].sum() / others_data['Qty'].sum()) ,
        'Teenagers orders': others_data[others_data['Age Group'] == 'Teenagers']['Qty'].sum(),
        'Teenagers orders percentage': (others_data[others_data['Age Group'] == 'Teenagers']['Qty'].sum() / others_data['Qty'].sum()) ,
        'Adults orders': others_data[others_data['Age Group'] == 'Adults']['Qty'].sum(),
        'Adults orders percentage': (others_data[others_data['Age Group'] == 'Adults']['Qty'].sum() / others_data['Qty'].sum()) ,
        'Senior orders': others_data[others_data['Age Group'] == 'Senior']['Qty'].sum(),
        'Senior orders percentage': (others_data[others_data['Age Group'] == 'Senior']['Qty'].sum() / others_data['Qty'].sum()) 
    }
    return metrics

def calculate_Nalli_metrics(df):
    """
    Calculate key metrics for the Nalli sales channel using the data available in the dataset.
    """
    nalli_data = df[df['Channel '] == 'Nalli']
    metrics = {
        'Total Revenue': nalli_data['Amount'].sum(),
        'Total number of orders': len(nalli_data),
        'Average order value': nalli_data['Amount'].mean(),
        'Delivered orders': nalli_data[nalli_data['Status'] == 'Delivered']['Qty'].sum(),
        'Returned orders': nalli_data[nalli_data['Status'] == 'Returned']['Qty'].sum(),
        'Cancelled orders': nalli_data[nalli_data['Status'] == 'Cancelled']['Qty'].sum(),
        'Orders delivered rate': (nalli_data[nalli_data['Status'] == 'Delivered']['Qty'].sum() / nalli_data['Qty'].sum()) ,
        'Orders returned rate': (nalli_data[nalli_data['Status'] == 'Returned']['Qty'].sum() / nalli_data['Qty'].sum()) ,
        'Women orders': nalli_data[nalli_data['Gender'] == 'Women']['Qty'].sum(),
        'Women orders percentage': (nalli_data[nalli_data['Gender'] == 'Women']['Qty'].sum() / nalli_data['Qty'].sum()) ,
        'Men orders': nalli_data[nalli_data['Gender'] == 'Men']['Qty'].sum(),
        'Men orders percentage': (nalli_data[nalli_data['Gender'] == 'Men']['Qty'].sum() / nalli_data['Qty'].sum()) ,
        'Teenagers orders': nalli_data[nalli_data['Age Group'] == 'Teenagers']['Qty'].sum(),
        'Teenagers orders percentage': (nalli_data[nalli_data['Age Group'] == 'Teenagers']['Qty'].sum() / nalli_data['Qty'].sum()) ,
        'Adults orders': nalli_data[nalli_data['Age Group'] == 'Adults']['Qty'].sum(),
        'Adults orders percentage': (nalli_data[nalli_data['Age Group'] == 'Adults']['Qty'].sum() / nalli_data['Qty'].sum()) ,
        'Senior orders': nalli_data[nalli_data['Age Group'] == 'Senior']['Qty'].sum(),
        'Senior orders percentage': (nalli_data[nalli_data['Age Group'] == 'Senior']['Qty'].sum() / nalli_data['Qty'].sum()) 
    }
    return metrics

def create_kpi_dataframe(df):
    # General numeric KPI 
    general_kpi = showNumericKPI(df)
    general_kpi_df = pd.DataFrame(list(general_kpi.items()), columns=['Metric', 'Value'])
    general_kpi_df['Category'] = 'General KPI'
    
    # Amazon KPI
    amazon_kpi = calculate_amazon_metrics(df)
    amazon_kpi_df = pd.DataFrame(list(amazon_kpi.items()), columns=['Metric', 'Value'])
    amazon_kpi_df['Category'] = 'Amazon KPI'
    
    # Myntra KPI
    myntra_kpi = calculate_Myntra_metrics(df)
    myntra_kpi_df = pd.DataFrame(list(myntra_kpi.items()), columns=['Metric', 'Value'])
    myntra_kpi_df['Category'] = 'Myntra KPI'
    
    # Ajio KPI
    ajio_kpi = calculate_Ajio_metrics(df)
    ajio_kpi_df = pd.DataFrame(list(ajio_kpi.items()), columns=['Metric', 'Value'])
    ajio_kpi_df['Category'] = 'Ajio KPI'
    
    # Flipkart KPI
    flipkart_kpi = calculate_Flipkart_metrics(df)
    flipkart_kpi_df = pd.DataFrame(list(flipkart_kpi.items()), columns=['Metric', 'Value'])
    flipkart_kpi_df['Category'] = 'Flipkart KPI'
    
    # Meesho KPI
    meesho_kpi = calculate_Meesho_metrics(df)
    meesho_kpi_df = pd.DataFrame(list(meesho_kpi.items()), columns=['Metric', 'Value'])
    meesho_kpi_df['Category'] = 'Meesho KPI'
    
    # Others KPI
    others_kpi = calculate_Others_metrics(df)
    others_kpi_df = pd.DataFrame(list(others_kpi.items()), columns=['Metric', 'Value'])
    others_kpi_df['Category'] = 'Others KPI'
    
    # Nalli KPI
    nalli_kpi = calculate_Nalli_metrics(df)
    nalli_kpi_df = pd.DataFrame(list(nalli_kpi.items()), columns=['Metric', 'Value'])
    nalli_kpi_df['Category'] = 'Nalli KPI'
    
    # merging dataframes
    all_kpi_df = pd.concat([
        general_kpi_df,
        amazon_kpi_df,
        myntra_kpi_df,
        ajio_kpi_df,
        flipkart_kpi_df,
        meesho_kpi_df,
        others_kpi_df,
        nalli_kpi_df
    ], ignore_index=True)
    
    def format_value(row):
        x = row['Value']
        metric = row['Metric']
        try:
            if any(word in metric.lower() for word in ['percentage', 'rate']):
                if isinstance(x, (float, int)) and 0 <= x <= 1:
                    return f"{x*100:.2f}%"
                return str(x)
            elif isinstance(x, (int, float)):
                return f"{x:.2f}"
            else:
                return str(x)
        except Exception as e:
            print(f"Error processing value for metric {metric}: {str(e)}")
            return str(x)
    
    # format values in all_kpi_df dataframe
    all_kpi_df['Value'] = all_kpi_df.apply(format_value, axis=1)
    
    return all_kpi_df

try:
    df = pd.read_excel(r"resources/Vrinda Store Data Analysis.xlsx", sheet_name = "VAStra Store")
    df['Date'] = pd.to_datetime(df['Date'])
    
    final_kpi_dataframe = create_kpi_dataframe(df)
    text_metrics = showTextMetrics(df)
    
    # Save text KPI into text_kpi.csv
    text_metrics_df = pd.DataFrame(list(text_metrics.items()), columns=['Metric', 'Value'])
    text_metrics_df['Category'] = 'General KPI'
    text_metrics_df.to_csv('resources/text_kpi.csv', index=False, header=True, encoding='utf-8', sep=',')
    
except Exception as e:
    print(f"Error: {e}")
