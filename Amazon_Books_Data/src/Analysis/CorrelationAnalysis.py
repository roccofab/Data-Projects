from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import chi2_contingency
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import pandas as pd

save_dir = "C:\\Users\\lenovo\\Documents\\analytics\\Amazon_Books_Data\\src\\Data_Visualization"
def numerical_variables_correlation(df):
    """
    Calculate the linear correlation between the numerical variables:
        - 'initial_price'
        - 'final_price'
        - 'discount'
        - discount_pct
        - rating
        - reviews_count
    """
    cols = ['initial_price', 'final_price', 'discount', 'discount_pct', 'rating',
            'reviews_count',  'item_weight', 'quantity_in_stock']
    return df[cols].corr(method='pearson').round(2)


def categories_vs_rating(df):
  """
   Calculate the variability between 'categories-rating' groups using Anova test.
    This test checks if there are significant differences in the ratings across different categories.
    The test aims to answer the question: does the book category have a significant impact on the average rating?
    
    It returns the F-value and p-value of the ANOVA test:
      - F-value: Indicates the ratio of variance between the groups to the variance within the groups.
      - p-value: Indicates the probability of observing the data if the null hypothesis is true (no difference in means).
    If p-value < 0.05, it suggests that there are significant differences in ratings across categories and we can reject the null hypothesis.
    and find out which categories have significant differences in ratings using the test Tukey HSD (Honestly Significant Difference).
    Then the result of the test Tukey is casted to a DataFrame and sorted by the adjusted p-value ('p-adj') in ascending order,
       so that the most significant differences appear first and the less significant differences appear last. 
  """
  category_groups = df.groupby('categories')['rating']
  # Test ANOVA
  f_val, p_val = stats.f_oneway(*[group[1] for group in category_groups])
  print(f"ANOVA: F-value={f_val:.2f}, p-value={p_val:.4f}")
  
  # Tukey hsd test:
  if p_val < 0.05:
      tukey_test = pairwise_tukeyhsd(df['rating'], df['categories'])
      #cast tukey  results table  to a dataframe
      tukey_df = pd.DataFrame(data=tukey_test._results_table.data[1:], columns=tukey_test._results_table.data[0])
      # filter the results to show only significant differences
      tukey_significant = tukey_df[tukey_df['reject'] == True]
      return tukey_significant.reset_index(drop=True).sort_values(by='p-adj', ascending=True).round(4)
  else:
      print( "No significant differences in ratings across categories (p-value >= 0.05)")
      return None
      
def brand_vs_price(df):
    
    """
    Calculate the variability across 'brand-final_price' groups using Anova test.
    The test aims to answer the question: do some brands have higher prices than the average price?
    """ 
    brand_groups = df.groupby('brand')['final_price']
    
    f_val,p_val = stats.f_oneway(*[group[1] for group in brand_groups])
    print(f"ANOVA: F-value={f_val:.2f}, p-value={p_val:.4f}")
    
    #tukey hsd test
    if p_val < 0.05:
      tukey_test = pairwise_tukeyhsd(df['final_price'], df['brand'])
      #cast tukey  results table  to a dataframe
      tukey_df = pd.DataFrame(data=tukey_test._results_table.data[1:], columns=tukey_test._results_table.data[0])
      # filter the results to show only significant differences
      tukey_significant = tukey_df[tukey_df['reject'] == True]
      return tukey_significant.reset_index(drop=True).sort_values(by='p-adj', ascending=True).round(4)
    else:
      print( "No significant differences in final_price across brand groups (p-value >= 0.05)")
      return None
  
def brand_vs_rating(df):
    """
    Calculate the variability across 'brand-rating' groups using Anova test.
    The test aims to answer the question: Do some brands have higher average ratings? 
    """
    brand_groups = df.groupby('brand')['rating']
    
    f_val,p_val = stats.f_oneway(*[group[1] for group in brand_groups])
    print(f"ANOVA: F-value={f_val:.2f}, p-value={p_val:.4f}")
    
    #tukey hsd test
    if p_val < 0.05:
      tukey_test = pairwise_tukeyhsd(df['rating'], df['brand'])
      #cast tukey  results table  to a dataframe
      tukey_df = pd.DataFrame(data=tukey_test._results_table.data[1:], columns=tukey_test._results_table.data[0])
      # filter the results to show only significant differences
      tukey_significant = tukey_df[tukey_df['reject'] == True]
      return tukey_significant.reset_index(drop=True).sort_values(by='p-adj', ascending=True).round(4)
    else:
      print( "No significant differences in rating across brand groups (p-value >= 0.05)")
      return None
  
  
def bookformat_vs_price(df):
    """
    Calculate the variability across 'categories-final_price' groups using Anova test.
    The test aims to answer the question: do some book formats have higher prices than the average price?
    """
    categories_groups = df.groupby('book_format')['final_price']
    
    f_val,p_val = stats.f_oneway(*[group[1] for group in categories_groups])
    print(f"Anova: F-value={f_val:.2f}, p-value={p_val:.4f}")
    
    #tukey hsd test
    if p_val < 0.05:
        tukey_test = pairwise_tukeyhsd(df['final_price'], df['book_format'])
        #cast tukey  results table  to a dataframe
        tukey_df = pd.DataFrame(data=tukey_test._results_table.data[1:], columns=tukey_test._results_table.data[0])
        # filter the results to show only significant differences
        tukey_significant = tukey_df[tukey_df['reject'] == True]
        return tukey_significant.reset_index(drop=True).sort_values(by='p-adj', ascending=True).round(4)
    else:
      print( "No significant differences in final_price across book_format groups (p-value >= 0.05)")
      return None
def bookformat_vs_rating(df):
    """
    Calculate the variability across 'book_format-rating' groups using Anova test.
    The test aims to answer the question: does the book format affects the average rating?
    """
    bookformat_groups = df.groupby('book_format')['rating']
    
    f_val, p_val = stats.f_oneway(*[group[1] for group in bookformat_groups])
    print(f"ANOVA: F-value={f_val:.2f}, p-value={p_val:.4f}")
    
    #tukey hsd test
    if p_val < 0.05:
        tukey_test = pairwise_tukeyhsd(df['rating'], df['book_format'])
        tukey_df = pd.DataFrame(data=tukey_test._results_table.data[1:], columns=tukey_test._results_table.data[0])
        # filter the results to show only significant differences
        tukey_significant = tukey_df[tukey_df['reject'] == True]
        return tukey_significant.reset_index(drop=True).sort_values(by='p-adj', ascending=True).round(4)
    else:
      print( "No significant differences in rating across book_format groups (p-value >= 0.05)")
      return None 

def bookformat_vs_discount(df):
    """
    Calculate the variability across 'book_format-discount_pct' groups using Anova test.
    The test aims to answer the question: are some book formats more discounted than others?
    """
    bookformat_groups = df.groupby('book_format')['discount_pct']
    
    f_val,p_val = stats.f_oneway(*[group[1] for group in bookformat_groups])
    print(f"ANOVA: F-value={f_val:.2f}, p-value={p_val:.4f}")
    
    #tukey hsd test
    if p_val < 0.05:
        tukey_test = pairwise_tukeyhsd(df['discount_pct'], df['book_format'])
        tukey_df = pd.DataFrame(data=tukey_test._results_table.data[1:], columns=tukey_test._results_table.data[0])
        # filter the results to show only significant differences
        tukey_significant = tukey_df[tukey_df['reject'] == True]
        return tukey_significant.reset_index(drop=True).sort_values(by='p-adj', ascending=True).round(4)
    else:
      print( "No significant differences in discount percentage across book_format groups (p-value >= 0.05)")
      return None 
  
def sellername_vs_price(df):
    """
    Calculate the variability across 'seller_name-final_price' groups using Anova test.
    The test aims to answer the question: do some sellers sell at higher average prices?
    """
    sellername_groups = df.groupby('seller_name')['final_price']
    
    f_val, p_val = stats.f_oneway(*[group[1] for group in sellername_groups])
    print(f"ANOVA: F-value={f_val:.2f}, p-value={p_val:.4f}")
    
    #tukey hsd test
    if p_val < 0.05:
        tukey_test = pairwise_tukeyhsd(df['final_price'], df['seller_name'])
        tukey_df = pd.DataFrame(data=tukey_test._results_table.data[1:], columns=tukey_test._results_table.data[0])
        # filter the results to show only significant differences
        tukey_significant = tukey_df[tukey_df['reject'] == True]
        return tukey_significant.reset_index(drop=True).sort_values(by='p-adj', ascending=True).round(4)
    else:
      print( "No significant differences in final_price across seller_name groups (p-value >= 0.05)")
      return None 

def cramers_v_heatmap(df):
    """
    The function calculate Cramèr's V between categorial variables in the dataset and show the heatmap.

    La Cramér's V measures the correlation between two categorial variables:
        - 0: no correlation
        - 1: perfect correlation

    Parameters:
        df (pd.DataFrame): the DataFrame che contiene that contains the categorial variables.
    """
    # select 'object' types columns
    cat_cols = df.select_dtypes(include='object').columns
    n = len(cat_cols)


    cramers_matrix = pd.DataFrame(np.zeros((n, n)), index=cat_cols, columns=cat_cols)

    for col1 in cat_cols:
        for col2 in cat_cols:
            if col1 == col2:
                cramers_matrix.loc[col1, col2] = 1.0  # Perfect correlation with itself
            else:
                # contingency table
                confusion_matrix = pd.crosstab(df[col1], df[col2])
                
                #chi2 test across the contingency table
                chi2, _, _, _ = chi2_contingency(confusion_matrix)
                
                #the sum of the total number of observation
                n_obs = confusion_matrix.sum().sum()
                
                #phi2 has range from 0(no association) to +inf:this value overestimates the association for large or unbalanced tables
                phi2 = chi2 / n_obs
                
                #get contigency table's number of rows(r) and number of columns(k)
                r, k = confusion_matrix.shape
                
                #ensures that the phi2 values is not negative
                phi2 = max(0, phi2 - ((k-1)*(r-1)) / (n_obs-1))
                  
                r = r - ((r-1)**2)/(n_obs-1)
                k = k - ((k-1)**2)/(n_obs-1)
                
                #Calculate Cramér's V, as a normalized version of phi² and then assign the values too the tabel cells
                cramers_v = np.sqrt(phi2 / min((k-1), (r-1)))
                cramers_matrix.loc[col1, col2] = cramers_v

    # Plot heatmap
    plt.figure(figsize=(9, 6))
    sns.heatmap(cramers_matrix, annot=True, cmap='coolwarm', vmin=0, vmax=1, linewidths=0.5)
    plt.title("Cramér's V Heatmap of Categorical Variables", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{save_dir}\\cramer_matrix.png")
    plt.show()
    plt.close()
