import ast
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import seaborn as sn

save_dir = "C:\\Users\\lenovo\\Documents\\analytics\\Amazon_Books_Data\\src\\Data_Visualization"

def top10_discounted_titles(df, save_dir):
    #show the top 10 most discounted in percentage titles in a horizontal bar chart
    top10 = df.sort_values('discount_pct', ascending = False).head(10)
    top10 = top10.sort_values('discount_pct')
    #truncate the titles having more than 50 characters
    top10['title'] = top10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)

    plt.figure(figsize =(10,6))
    bars = plt.barh(top10['title'], top10['discount_pct'], color='lightblue')
    plt.bar_label(bars, fmt='%.2f', fontsize=8, color='black', label_type='center')
    plt.barh(top10['title'], top10['discount_pct'], color = 'lightblue')
    plt.xlabel('Discount(%)', fontweight = 'bold')
    plt.ylabel('Titles', fontweight = 'bold')
    plt.title('Top 10 Most Discounted Titles', fontname = 'Georgia', fontsize = 16)
    plt.yticks(fontsize=6)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\Top10_Most_Discounted.png")
    plt.show()
    plt.gcf()
    plt.close()
    
def top10_cheapest_categories(df, save_dir):
    avg_price = df.groupby('categories').agg(
        avg_final_price=('final_price', 'mean'),
        count=('final_price', 'count')
    ).reset_index()
    
    avg_price_grouped = avg_price.groupby('categories').agg(
        avg_final_price=('avg_final_price', 'mean'),
        count=('count', 'sum')
    ).reset_index()

    top10 = avg_price_grouped.nsmallest(10, 'avg_final_price').sort_values('avg_final_price')
    
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top10['categories'], top10['avg_final_price'], color='lightblue')
    plt.bar_label(bars, fmt='%.2f', fontsize=8, color='black', label_type='center')
    plt.barh(top10['categories'], top10['avg_final_price'], color='lightblue')
    plt.xlabel('Avg price ($)', fontweight='bold')
    plt.ylabel('Category', fontweight='bold')
    plt.title("Top 10 Cheapest Categories", fontname = 'Georgia', fontsize = 16)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\top10_cheapest_categories")
    plt.show()
    plt.gcf()
    plt.close()
    
def top10_expensive_categories(df, save_dir):
    avg_price = df.groupby('categories').agg(
        avg_final_price=('final_price', 'mean'),
        count=('final_price', 'count')
    ).reset_index()
    
    avg_price_grouped = avg_price.groupby('categories').agg(
        avg_final_price=('avg_final_price', 'mean'),
        count=('count', 'sum')
    ).reset_index()

    top10 = avg_price_grouped.nlargest(10, 'avg_final_price').sort_values('avg_final_price')
    
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top10['categories'], top10['avg_final_price'], color='lightblue')
    plt.bar_label(bars, fmt='%.2f', fontsize=8, color='black', label_type='center')
    plt.barh(top10['categories'], top10['avg_final_price'], color='lightblue')
    plt.xlabel('Avg price ($)', fontweight='bold')
    plt.ylabel('Category', fontweight='bold')
    plt.title("Top 10 Most Expensive Categories", fontname = 'Georgia', fontsize = 16)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\top10_expensive_categories")
    plt.show()
    plt.gcf()
    plt.close()
    
def top10_most_reviewed(df, save_dir):
    #show the top 10 titles with the most reviews in a bar chart
    top10 = df.sort_values('reviews_count', ascending = False).head(10).copy()
    top10 = top10.sort_values('reviews_count')
    #truncate the titles having more than 50 characters
    top10['title'] = top10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)

    bars = plt.barh(top10['title'], top10['reviews_count'], color='lightblue')
    plt.bar_label(bars, fmt='%.0f', fontsize=7, color='black', label_type='center')
    
    plt.xlabel('Reviews Count', fontweight='bold')
    plt.ylabel('Title', fontweight='bold')
    plt.title('Top 10 Most Reviewed Books', fontweight='bold')
    plt.yticks(fontsize=6)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\Top10_Most_Reviewed.png")
    plt.show()
    plt.gcf()
    plt.close()
    
def top10_sellers(df,save_dir):
    #show the top 10 sellers name with the lowest prices and the top 10 sellers name with highest prices
    avg_price = df.groupby('seller_name')['final_price'].mean().reset_index()
    top10_cheapest = avg_price.nsmallest(10, 'final_price').sort_values('final_price')
    top10_lowest = avg_price.nlargest(10, 'final_price').sort_values('final_price')
    
    fig, axes = plt.subplots(2, 1,figsize = (10,7), sharex=False)
    bars1 = axes[0].barh(top10_cheapest['seller_name'], top10_cheapest['final_price'], color='seagreen')
    axes[0].bar_label(bars1, fmt = '%.2f', fontsize = 8, color = 'black', label_type = 'center')
    axes[1].set_title('Top 10 Most Expensive Sellers', fontweight = 'bold')
    axes[0].set_xlabel('Avg. price($)', fontweight = 'bold')
    axes[0].set_ylabel('Seller', fontweight = 'bold')
    axes[0].invert_yaxis()
    
    bars2 = axes[1].barh(top10_lowest['seller_name'], top10_lowest['final_price'], color = 'salmon')
    axes[1].bar_label(bars2, fmt = '%.2f', fontsize = 8, color = 'black', label_type = 'center')
    axes[0].set_title('Top 10 Cheapest Sellers', fontweight = 'bold')
    axes[0].set_xlabel('Avg. price($)', fontweight = 'bold')
    axes[0].set_ylabel('Seller', fontweight = 'bold')
    axes[0].invert_yaxis()
    
    plt.subplots_adjust(hspace=0.30)
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\top10_sellers_prices.png")
    plt.show()
    plt.close()
    
    
    

    
    
def rank_vs_titles(df, save_dir):
    ranks = df[df['main_rank'].notna()]

    # Top 10 most popular(lower rank value)
    top10 = ranks.sort_values('main_rank').head(10).copy()
    top10['title'] = top10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)

    # Top 10 less popular(higher rank value)
    bottom10 = ranks.sort_values('main_rank', ascending=False).head(10).copy()
    bottom10['title'] = bottom10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=False)

    # Formatter to format x-axes values
    formatter = FuncFormatter(lambda x, _: f'{x:.3f}')

    # most popular titles chart
    bars1 = axes[0].barh(top10['title'], top10['main_rank'], color='seagreen')
    axes[0].bar_label(bars1, fmt='%.2f', fontsize=7, color='white', label_type='center')
    axes[0].set_title('Top 10 Most Popular Books', fontweight='bold')
    axes[0].set_xlabel('Main Rank', fontweight='bold')
    axes[0].invert_yaxis()
    axes[0].xaxis.set_major_formatter(formatter)

    # less popular chart
    bars2 = axes[1].barh(bottom10['title'], bottom10['main_rank'], color='salmon')
    axes[1].bar_label(bars2, fmt='%.2f', fontsize=7, color='black', label_type='center')
    axes[1].set_title('Top 10 Least Popular Books', fontweight='bold')
    axes[1].set_xlabel('Main Rank', fontweight='bold')
    axes[1].invert_yaxis()
    axes[1].xaxis.set_major_formatter(formatter)

    plt.subplots_adjust(left = 0.40,hspace=0.29)
    plt.savefig(f"{save_dir}\\titles_popularity.png")
    plt.show()
    plt.close()

    
def categories_vs_rating(df, save_dir):
    #Show the top 10 best rated categories and the top 10 lowest rated categories in 2 side-by-side bar charts
    df['categories'] = df['categories'].apply(
        lambda x: ast.literal_eval(x)[0] if isinstance(x, str) and x.startswith('[') else str(x)
    )
    categories_rating = df.groupby('categories')['rating'].mean().sort_values(ascending=False)
    top10 = categories_rating.sort_values(ascending=False).head(10)
    bottom10 = categories_rating.sort_values().head(10)

    #create 2 subframes
    fig,axes = plt.subplots(1,2, figsize = (14,6), sharey = True)
    
    #top 10 best rated bar chart
    axes[0].barh(top10.index[::-1], top10.values[::-1], color='seagreen')  
    axes[0].set_title('Top 10 Best Rated Categories', fontweight='bold')
    axes[0].set_xlabel('Rating', fontweight='bold')
    axes[0].set_ylabel('Category', fontweight='bold')
    axes[0].set_xlim(0, 5)
    axes[0].tick_params(labelsize=8)
    
    # top 10 lowest rated bar chart
    axes[1].barh(bottom10.index[::-1], bottom10.values[::-1], color='salmon')  
    axes[1].set_title('Top 10 Lowest Rated Categories', fontweight='bold')
    axes[1].set_xlabel('Rating', fontweight='bold')
    axes[1].set_xlim(0, 5)
    axes[1].tick_params(labelsize=8)
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\Top_Bottom10_Categories_Rating.png")
    plt.show()
    plt.close()
    
def format_vs_rating(df,save_dir):
    #show the best rated book format  and the lowest rated book format  in 2 side-by-side bar charts
    format_rating = df.groupby('book_format')['rating'].mean().sort_values(ascending = False)
    plt.figure(figsize = (10,6))
    plt.title('Books Format Rating')
    plt.xlabel('Format', fontweight = 'bold')
    plt.ylabel('Rating', fontweight = 'bold')
    plt.xticks(rotation = 90, ha='center', fontsize = 7)
    bars = plt.bar(format_rating.index, format_rating.values, color='lightblue')
    plt.bar_label(bars, fmt='%.2f', fontsize=7, color='black', label_type='center')
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.32)
    plt.bar(format_rating.index, format_rating.values, color = 'lightblue')
    plt.savefig(f"{save_dir}\\format_vs_rating.png")
    plt.show()
    plt.gcf()
    plt.close()
    
def reviews_range_vs_price(df, save_dir):
    #Analyze and visualize the average price of books grouped by number of reviews range using a pie chart.
    bins = [0,10000,20000,30000,40000,50000,float('inf')]
    labels = ['0-10000','10000-20000','20000-30000','30000-40000','40000-50000','50000+']
    df['num_reviews_range'] = pd.cut(df['reviews_count'], bins = bins, labels = labels, right = False)
    
    avg_price = df.groupby('num_reviews_range', observed = True)['final_price'].mean().reset_index()
    avg_price = avg_price[avg_price['final_price'].notna()]
    
   
    plt.figure(figsize=(10,6))
    bars = plt.bar(avg_price['num_reviews_range'], avg_price['final_price'], color = 'lightblue', width = 0.5)
    plt.title('Average Price by Reviews Count Range', fontweight='bold')
    plt.xlabel('Reviews Count', fontweight = 'bold')
    plt.ylabel('Avg. Price($)', fontweight = 'bold')
    plt.gca().bar_label(bars, fmt='%.2f', fontsize=8, color='black', label_type='center')
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\reviews_vs_price.png")
    plt.show()
    plt.gcf()
    plt.close()  
    
def histogram_reviews(df, save_dir):
    #Show how the number of reviews (reviews_count) is distributed across all books using a histogram
    plt.figure(figsize=(10, 6))
    
    n, bins, patches = plt.hist(df['reviews_count'].dropna(), bins=30, color='skyblue', edgecolor='black')

    # add the number of books on the bars
    for count, edge_left, edge_right in zip(n, bins[:-1], bins[1:]):
        x = (edge_left + edge_right) / 2
        y = count
        plt.text(x, y + 0.5, str(int(count)), ha='center', va='bottom', fontsize=7)
    
    plt.title('Reviews Count per Book', fontweight='bold')
    plt.xlabel('Reviews Count', fontweight='bold')
    plt.ylabel('Number Books', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\histogram_reviews_count.png")
    plt.show()
    plt.close()
    
def histogram_rating(df,save_dir):
    #show how rating(rating) values are distributed across all books using a histogram
    plt.figure(figsize=(10,6))
    n, bins, patches = plt.hist(df['rating'].dropna(), bins=5, color='skyblue', edgecolor='black')
    
    for count, edge_left, edge_right in zip(n, bins[:-1], bins[1:]):
        x = (edge_left + edge_right) / 2
        y = count
        plt.text(x, y + 0.5, str(int(count)), ha='center', va='bottom', fontsize=7)
    
    plt.title('Rating Value per Book', fontweight='bold')
    plt.xlabel('Rating', fontweight='bold')
    plt.ylabel('Number Books', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\histogram_rating.png")
    plt.show()
    plt.close()
    
def histogram_price(df,save_dir):
    #Show how the final prices(final_price) are distributed across all books using a histogram
    plt.figure(figsize=(10,6))
    n,bins,patches = plt.hist(df['final_price'].dropna(), bins = 15, color = 'skyblue', edgecolor = 'black')
    
    for count, edge_left, edge_right in zip(n,bins[:-1], bins[1:]):
        x = (edge_left+edge_right) / 2
        y = count
        plt.text(x,y+0.5, str(int(count)), ha='center', va='bottom', fontsize = 7)
        
    plt.title('Final Price per Book', fontweight = 'bold')
    plt.xlabel('Final Price', fontweight = 'bold')
    plt.ylabel('Number Books', fontweight = 'bold')
    
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\histogram_price.png")
    plt.show()
    plt.close()
    
def show_book_availability(df, save_dir):
    """
    This pie chart aims to show the total percentage of available and unavailable books in the dataset by analyzing the column is_in_stock which has values:
       0-unavailable
       1-available 
    """
    title_counts = df['title'].value_counts()
    df['is_in_stock'].value_counts(normalize = True).plot.pie(
        labels = ['Available', 'Not Available'],
        autopct = '%1.1f%%',
        startangle = 90,
        colors = ['lightblue', 'salmon']
    )
    plt.title('Books Availability')
    plt.ylabel('')
    plt.show()
    plt.savefig(f"{save_dir}\\Books_Availability.png")
    plt.gcf()
    plt.close()
    
def show_not_available_titles(df,save_dir):
    not_available = df[df['is_in_stock'] == 0]
    not_available_titles = not_available['title'].value_counts()
    not_available_titles.index = not_available_titles.index.to_series().apply(
        lambda x: x[:50] + '...' if len(x) > 50 else x
    )
    bars = plt.barh(not_available_titles.index[::-1], not_available_titles.values[::-1], color = 'lightblue')
    plt.title('Titles not Available', fontweight = 'bold')
    plt.yticks(fontsize=6)
    plt.tight_layout()
    plt.subplots_adjust(left=0.5) 
    plt.savefig(f"{save_dir}\\not_available_titles.png")
    plt.show()
    plt.gcf()
    plt.close()
    
    
    
    