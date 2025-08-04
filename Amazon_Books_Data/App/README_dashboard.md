# Dashboard Amazon Books Data

This Dashboard built in Dash and Plotply makes visualization of data stored in cleaned_dataset.csv simple and interactive.

## Charts, Functionalities and Features

Dashboard includes 8 Plots:

### 1. **Top 10 Most Discounted Books**
- Show 10 books having the biggest discount percentage in a horizontal barplot.

### 2. **Titles Popularity by Rank**
- Show 10 books with highest rank value(low popularity) and 10 books with lowest rank value(high popularity) in a horizontal barplot.
- The main rank value is a value that amazon uses for popularity of a product(low rank value = high popularity, high rank value = low popularity).

### 3. **Rating per Category/Format**
- This section includes two barplots: Rating per Category and Rating per Format, you can choose the chart to display by using the Dropdown.

### 4. **Distribution of Reviews/Rating/Prices**
- This section includes three histograms: Distribution Reviews,Distribution Rating, Distribution Prices, you can choose the chart to display by using the Dropdowm. 
- The histograms shows how Reviews/Rating/Prices are distributed across the books in the dataset.

### 5. **Books Availability**
- This section includes two charts: pie chart to show the percentage of available and not available books and an horizontal bar chart to show the titles not available, you can choose the chart to display by using the Dropdowm.

### **Responsive Charts**: Automatically adapt to the screen size.

###  **Tooltip**: Show detailed values on mouseover.


## Local Setup:

1. 
   ```
   git clone https://github.com/roccofab/Amazon_Books_Data_Analysis.git
   ```

2. 
   ```
   cd Amazon_Books_Data_Analysis/App
   ```

3. 
   ```
   pip install -r requirements.txt
   ```

4. ```
   python Dashboard.py
   ```


## Technologies used

- **Framework**: Dash (based on Flask)
- **Visualization**: Plotly Graph Objects
- **Style**: CSS 
- **Data**: Pandas DataFrame
- **Connection**: Dynamic Port(assigned by Render hosting platform)