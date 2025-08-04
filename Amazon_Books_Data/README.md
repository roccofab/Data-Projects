# Amazon Books Data Analysis & Recommendation System

### Full Data Science Project that analyzes a medium/large dataset of books available on Amazon. The project covers the entire data pipeline—from data cleaning and exploratory analysis to machine learning and web visualization.The models and analyses focus on book features because the dataset does not contain information on sales and customers, but only details on books, prices, reviews, etc. <br> It Includes:<br>

-  Data exploration & visualization

-  Data preprocessing & normalization

-  Recommendation models using clustering and similarity techniques

-  Correlation & discount analysis

-  A web dashboard built with Dash for interactive visualizations

-  A live recommender system exposed through a web interface

## 🧰 Tools Used:
- **Python, Pandas, Numpy, Scikit-learn, Scipy, Matplotlib, Seaborn, Dash, Plotly, Flask, pytest...**

- **html,css,javascript.**

- **Render Server.** 

## Key Features:
- Cleaned & enriched book dataset with over 1000 titles.

- Complex **Data Cleaning** Operations.

- **Data Normalization**

- **Statistical analysis** on prices, ratings, reviews, discounts and sellers.

- **Data Visualization** using Matplotplib.

- **Machine Learning recommender models** (KMeans, Nearest Neighbors Model).

- **Filtering Books Model** by Popularity.

- Interactive **dashboard** built in dash and plotly with category-based filters and trend insights

- Deployed **web app** (using Render) with a user-friendly interface

- **Modular architecture** for scalability and testing

## 📦 Dataset:
I found this dataset on github, the dataset was very dirty (most of the values were objects and lists of objects) because it was obtained by scraping techniques, data cleaning took most of the work.
1. **Original Dataset:** [Amazon_popular_books_dataset.csv](https://github.com/roccofab/Amazon_Books_Data_Analysis/blob/main/Amazon_popular_books_dataset.csv)

2. **Cleaned Dataset:** [cleaned_data.csv](https://github.com/roccofab/Amazon_Books_Data_Analysis/blob/main/src/Data_Cleaning/cleaned_data.csv)

## Metadata Description:

- **asin(Amazon Standard Identification Number):** Univoque identification code used by Amazon to identify products.

- **brand:** the brand of the product.

- **currency:** currency used for product prices (e.g. USD).

- **discount:** amount of the discount applied to the product.

- **final_price:** discounted price.

- **images_count:** number of images in the product.

- **initial_price:** not discounted price.

- **item_weight**

- **rating:** average rating of the product.

- **reviews_count:** total number of reviews for the product.

- **root_bs_rank:** Bestseller Rank of the product in its category.

- **seller_id**

- **seller_name**

- **timestamp:** date and time of product data entry.

- **title**

- **video_count:** number of videos available for the product(Kindle format books often contain videos).

- **categories:** category of books to which the product belongs.

- **number_of_sellers:** number of sellers offering a specific product.

- **main_category:** integer number that identify a specific category.

- **main_rank:** integer value indicating the product's popularity(low rank value = high popularity, high rank value = low popularity)

- **quantity_in_stock**

- **is_in_stock:** 0-not in stock, 1-in stock

- **book_format**

- **discount_pct:** percentage of discount applied to the product.

- **discount_range:** Discount percentage range.

- **price-range:** Final product price range.

- **num_reviews_range:** range of reviews.


## 🔍 Findings and Key Insights:
- **Most Popular Books:** the top 10 most popular books identified by the lowest rank values and highest number of reviews have **high average ratings(4.6-4.9).** The most popular book(lowest rank value, highest number of reviews and average rating of 4.9) is **American Marxism.**

- **Uncommonly high discounts:** there are books having significantly high discounts(>60%) these are indicators of promotional strategies implemented by sellers. Some of the most discounted titles: **Homo Deus: A Brief History of Tomorrow(94.48%), Catching Fire(89.47%), The Missing Sister(87.66%), School Zone- Big First Grade Workbook(68.56%)...**

- **Discount-Book Categories:** The Romance - Historical, Textbooks - Social Sciences and Sports Biographies categories offer an average of over 60% off. Categories Cookbooks Food & Wine - Quick & Easy, History-Europe, Business & money-Industries,Romance-New Adult & College,Romance-Paranormal offer low discounts(less than 15% off).

- **Discount-Book Formats:** The Most Discounted book formats (> 43%) are Spiral-Bounds, Board book and Vinyl Bound while the traditional book formats such as Library Binding,Ring-bound,Hardover,Audiobook are less discounted(< 27%).

- **Discount-Rating:** Books with lower ratings (e.g. 3.9) have higher average discounts, suggesting a possible attempt by sellers to incentivize purchases.

- **Prices-Categories:** Children’s and religious categories have very low average prices (e.g. Children’s Books – Animals ≈ $6), while university medical textbooks average over $60.

- **Best Seller:** Amazon is the seller with the largest number of books in stock, followed by ZBK Books,TheBookkingdom,OnTimeBooks, Vivè Liber Books LLC, gatecitybooks.

## 📊 Statistical Relationship Analysis
### 1. Correlation Between Numerical Variables
Pearson’s correlation coefficient was used to assess linear relationships among key numerical features (e.g. prices, discounts, ratings, review counts):

Initial Price vs Final Price (r = 0.78): Higher initial prices generally correspond to higher final prices.

Initial Price vs Discount (r = 0.84): More expensive books tend to receive larger absolute discounts.

Item Weight vs Price (r = 0.59 for initial price, r = 0.62 for final price): Heavier books are generally more expensive.

### 2. Association Between Categorical Variables
Cramér’s V was computed to evaluate associations between categorical features (e.g., brand, seller name, book format). It ranges from 0 (no association) to 1 (perfect association):

- **Brand vs Seller Name:** Strong association — most brands are linked to a specific seller, often Amazon.

- **Brand vs Book Format:** Moderate association — some brands specialize in specific formats.

### 3. Influence of Categorical Variables on Numerical Variables (ANOVA)
One-way ANOVA tests followed by Tukey HSD post-hoc tests was applied to measure the effect of categorical variables on numerical ones (e.g. price, rating). This method identifies statistically significant group differences.

- **Book Category vs Rating:** Significant differences exist; for example, Children’s Books – Animals vs Mystery, Thriller & Suspense.

- **Format vs Rating:** Kindle books receive significantly higher average ratings than Audiobooks.

- **Format and Seller vs Price:** Vinyl Bound books and some specific sellers show significantly higher average prices than others.

## 📚Book Reccomandation Models
### I' ve implemented three recommendation models based on the numerical and categorical features of the books (content-based filtering), since the dataset does not contain user-book interaction data.

1. **filter_by_category:** This basic filtering model suggest popular books (10 by default) in the same category as a book searched for    by  its asin code. The model find book's category and then filtering,sorting by popularity(low main_rank value, hig reviews count and rating), and returns the most relevant books in that category.

2. **knn_category_recommender:** This content-based filtering model suggests books similar to a given one (identified by asin code) using the Nearest Neighbors algorithm within the same category. Filtering is done by calculating the Euclidean distance between books based on their normalized prices and the number of normalized reviews, returning the closest and therefore most similar books in terms of price and number of reviews to the given one.

3. **kmeans_reccomender:** This content-based model suggests books similar to a given one (identified by its ASIN), based on final price and reviews count, by using the K-Means clustering algorithm within the same category combined with dimensionality reduction via UMAP. The k-means algorithm divides a dataset into k clusters by minimizing the intra-cluster distance.

## 🌐 Web Application & API Documentation
### This project includes a production-ready web application, deployed at https://reccomender.onrender.com, which provides a user-friendly interface for book recommendations. The backend is powered by Flask and exposes a RESTful API for programmatic access to the recommendation engine.

#### Application Overview:

The frontend allows users to input an Amazon ASIN code and receive personalized book recommendations.
The backend processes requests, applies the KMeans-based recommendation model, and returns a list of similar books with relevant details.
Recommendations are computed using normalized features such as price, reviews count, and category, ensuring relevant and different suggestions. The book features are converted back to their original format before being returned to the frontend.

#### API Endpoint:

The Flask backend exposes a RESTful API endpoint (/recommend) that accepts an ASIN as input and returns a list of recommended books based on KMeans-Clustering algorithm.
Endpoint: /recommend

Method: GET

Query Parameter: asin code(string)


## 📊Dashboard
### The dashboard, built with Plotly's Dash library, provides an interactive visualization of data. You can check for the dashboard here: <br>https://amazon-dashboard-ycpv.onrender.com 









