import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Load_Data import Loader
from src.Analysis import BookDataAnalysis

#get current directory path and build the path to the cleaned_data.csv file
current_directory = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_directory, '..', 'src', 'Data_Cleaning', 'cleaned_data.csv')
df = Loader.load_dataset(path)

# create dash app
app = dash.Dash(__name__)

# set application components layout
app.layout = html.Div([
    #First section: the main title of the page
    html.H1("Amazon Book Analysis Dashboard", 
             style={'textAlign': 'center', 'color': "#0d0d0d", 'marginBottom': 30}),
    
    # Plot 1: Top 10 Most Discounted Titles
    html.Div([
        html.H2("Top 10 Most Discounted Titles",  #title and style section 2
                style={'textAlign': 'center', 'color': '#34495e'}),
        dcc.Graph(id='discounted-titles-graph')
    ], style={'marginBottom': 40}),
    
    # Plot 2: Top 10 Most Popular Titles(lower rank values) vs Top 10 Less Popular Titles(higher rank values)
    html.Div([
        html.H2("Titles Popularity by Rank", #title and style section 3
                style={'textAlign': 'center', 'color': '#34495e'}),
        dcc.Graph(id='rank-titles-graph')
    ], style={'marginBottom': 40}),
    
    # Plot 3: Rating per Category and Rating per Format with Dropdown to choose between Rating Count per Category bar chart or Rating Count per Format bar chart
    html.Div([
        html.H2("Rating Count per Category/Format",  #title and style section 4
                style={'textAlign': 'center', 'color': '#34495e'}),
        html.Div([
            html.Label("Select Plot:",  #set label and its style for the Dropdown
                      style={'fontSize': 16, 'marginRight': 10}),
            dcc.Dropdown(  #set id,options and style for the Dropdown
                id='rating-type-dropdown',
                options=[
                    {'label': 'Categories-Rating', 'value': 'categories'},
                    {'label': 'Format-Rating', 'value': 'format'}
                ],
                value='categories',
                style={'width': 200, 'display': 'inline-block'}
            )
        ], style={'textAlign': 'center', 'marginBottom': 20}), 
        dcc.Graph(id='rating-graph')
    ], style={'marginBottom': 40}),
    
    #Plot 4: Reviews/Ratings/Prices Histogram with Dropdowm 
    html.Div([
        html.H2("Distribution Reviews/Ratings/Prices", style={'textAlign': 'center', 'color': '#34495e'}), #section title style
        html.Div([
            html.Label("Select Distribution:", style={'fontSize': 16, 'marginRight': 10}), #set label and its style for the dropdowm
            dcc.Dropdown(  #set id,options and style for the Dropdowm
                id='histogram-type-dropdown',
                options=[
                    {'label': 'Number of Reviews', 'value': 'reviews'},
                    {'label': 'Rating', 'value': 'rating'},
                    {'label': 'Prices', 'value': 'prices'}
                ],
                value='reviews',
                style={'width': 250, 'display': 'inline-block'}
            )
        ], style={'textAlign': 'center', 'marginBottom': 20}),  #section style
        dcc.Graph(id='histogram-graph')
    ], style={'marginBottom': 40}),
    
    # Plot 5: Books Availability with dropdown to choose between pie chart and bar chart
    html.Div([
        html.H2("Books Availability",   #section title style
                style={'textAlign': 'center', 'color': '#34495e'}), 
        html.Div([
            html.Label("Select Chart Type:", #set label and its style for the dropdown of this section
                      style={'fontSize': 16, 'marginRight': 10}),
            dcc.Dropdown(  #set id, style and options for the Dropdown of this section
                id='availability-type-dropdown',
                options=[
                    {'label': 'Availability Pie Chart', 'value': 'pie'},
                    {'label': 'Not Available Titles', 'value': 'bar'}
                ],
                value='pie',
                style={'width': 250, 'display': 'inline-block'}
            )
        ], style={'textAlign': 'center', 'marginBottom': 20}),  #section style  
        dcc.Graph(id='availability-graph')
    ], style={'marginBottom': 40})
], style={'padding': 20, 'backgroundColor': '#f8f9fa'})


# Callback for discount_titles_graph (Top 10 Most Discounted Titles)
@app.callback(
    Output('discounted-titles-graph', 'figure'), #the output of the function is an object figure for the component having id 'discounted-titles-graph'
    Input('discounted-titles-graph', 'id')  # input 'discounted-titles-graph' works as trigger for the callback function
)
def update_discounted_titles_graph(id):
    # calculate discount percentage column, sort values in descending order and get the first 10 rows of the dataframe
    df['discount_pct'] = (df['discount'] / df['initial_price']) * 100
    top10 = df.sort_values('discount_pct', ascending=False).head(10)
    top10 = top10.sort_values('discount_pct')
    
    # truncate titles having more than 50 characters
    top10['title_short'] = top10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
    
    fig = go.Figure()  #initialize a new empty Plotly plot
    fig.add_trace(go.Bar(  #add a bar plot with horizontal bars
        x=top10['discount_pct'],  #values
        y=top10['title_short'], #labels
        orientation='h',  #bars horizontal orientation
        marker_color='lightblue',  
        text=[f'{val:.2f}%' for val in top10['discount_pct']], #calculate values of discount percentage
        textposition='auto'   #Plotly automatically choose if show discount percentage values inside or on the top of the bars 
    ))
    
    # Plot layout personalization
    fig.update_layout(
        title='Top 10 Most Discounted Titles', #plot title
        xaxis_title='Discount (%)',  #x-axes title
        yaxis_title='Title',  #y-axes title
        height=500,  
        showlegend=False,  #
        plot_bgcolor='white'  #background color
    )
    
    return fig

# Callback for rank-titles-graph(Top 10 Most Popular Books vs Top 10 Less Popular Books)
@app.callback(
    Output('rank-titles-graph', 'figure'),
    Input('rank-titles-graph', 'id')
)
def update_rank_titles_graph(id):
    # exclude rows having not valid main_rank value 
    ranks = df[df['main_rank'].notna()]
    
    # Calculate top 10 most popular books(lower rank values)
    top10 = ranks.sort_values('main_rank').head(10).copy()
    top10['title_short'] = top10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
    
    # calculate top 10 less popular books(higher rank values)
    bottom10 = ranks.sort_values('main_rank', ascending=False).head(10).copy()
    bottom10['title_short'] = bottom10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
    
    fig = go.Figure()
    
    # Top 10 Most popular books plot
    fig.add_trace(go.Bar(
        x=top10['main_rank'],
        y=top10['title_short'],
        orientation='h',
        marker_color='seagreen',
        name='Most Popular',
        text=[f'{val:.3f}' for val in top10['main_rank']],
        textposition='auto'
    ))
    
    # Top 10 less popular books plot
    fig.add_trace(go.Bar(
        x=bottom10['main_rank'],
        y=bottom10['title_short'],
        orientation='h',
        marker_color='salmon',
        name='Less Popular',
        text=[f'{val:.3f}' for val in bottom10['main_rank']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Top 10 Most Popular Books vs Top 10 Less Popular Books (Lower Rank Value = More Popularity)',
        xaxis_title='Main Rank',
        yaxis_title='Titles',
        height=600,
        barmode='group',
        plot_bgcolor='white'
    )
    
    return fig

# Callback for rating-type-dropdown and rating-graph and (Rating per Category, Rating per Book Formats)
@app.callback(
    Output('rating-graph', 'figure'),
    Input('rating-type-dropdown', 'value')
)
def update_rating_graph(selected_type):
    if selected_type == 'categories':
        # extract category value from column categories and calculate the top 10 best rated categories and the top 10 lowest rated categories
        df['categories'] = df['categories'].apply(
            lambda x: eval(x)[0] if isinstance(x, str) and x.startswith('[') else str(x)
        )
        categories_rating = df.groupby('categories')['rating'].mean().sort_values(ascending=False)
        top10 = categories_rating.head(10)
        bottom10 = categories_rating.tail(10)
        
        fig = go.Figure()
        
        # Top 10 best rated categories
        fig.add_trace(go.Bar(
            x=top10.values,
            y=top10.index,
            orientation='h',
            marker_color='seagreen',
            name='Top 10 Categories',
            text=[f'{val:.2f}' for val in top10.values],
            textposition='auto'
        ))
        
        # Top 10 less rated categories
        fig.add_trace(go.Bar(
            x=bottom10.values,
            y=bottom10.index,
            orientation='h',
            marker_color='salmon',
            name='Bottom 10 Categories',
            text=[f'{val:.2f}' for val in bottom10.values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Rating per Category',
            xaxis_title='Rating',
            yaxis_title='Category',
            height=600,
            barmode='group',
            plot_bgcolor='white'
        )
    #show rating-graph(Rating per Book Formats)    
    else:
        # get all the books format, group by average rating, sort values in descending orders and show the result in a barplot having vertical bars
        format_rating = df.groupby('book_format')['rating'].mean().sort_values(ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=format_rating.index,
            y=format_rating.values,
            marker_color='lightblue',
            text=[f'{val:.2f}' for val in format_rating.values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Rating per Book Formats',
            xaxis_title='Formato',
            yaxis_title='Rating',
            height=500,
            plot_bgcolor='white'
        )
    
    return fig

# Callback for histogram-graph
@app.callback(
    Output('histogram-graph', 'figure'),
    Input('histogram-type-dropdown', 'value')
)
def update_histogram_graph(selected_type):
    fig = go.Figure()
    if selected_type == 'reviews':
        fig.add_trace(go.Histogram(
            x=df['reviews_count'].dropna(),
            nbinsx=30,
            marker_color='skyblue',
            marker_line_color='black',
            marker_line_width=1
        ))
        fig.update_layout(
            title='Distribution of the Number of Reviews across all Books',
            xaxis_title='Number of Reviews',
            yaxis_title='Number of Books',
            height=500,
            plot_bgcolor='white'
        )
    elif selected_type == 'rating':
        fig.add_trace(go.Histogram(
            x=df['rating'].dropna(),
            xbins=dict(start=1, end=5, size=0.8),  
            marker_color='skyblue',
            marker_line_color='black',
            marker_line_width=1
        ))
        fig.update_layout(
            title='Distribution of Ratings Value across all Books',
            xaxis_title='Rating',
            yaxis_title='Number of Books',
            height=500,
            plot_bgcolor='white'
        )
    elif selected_type == 'prices':
        fig.add_trace(go.Histogram(
            x=df['final_price'],
            nbinsx=15,
            marker_color='skyblue',
            marker_line_color='black',
            marker_line_width=1
        ))
        fig.update_layout(
            title='Distribution of Prices across all Books',
            xaxis_title='Final Price',
            yaxis_title='Number of Books',
            height=500,
            plot_bgcolor='white'
        )
    return fig

# Callback for availability-graph (Books Availability)
@app.callback(
    Output('availability-graph', 'figure'),
    Input('availability-type-dropdown', 'value')
)
def update_availability_graph(selected_type):
    if selected_type == 'pie':
        # Pie chart for books availability
        availability_counts = df['is_in_stock'].value_counts(normalize=True)
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=['Available', 'Not Available'],
            values=availability_counts.values,
            textinfo='percent',
            textposition='inside',
            marker=dict(colors=['lightblue', 'salmon'])
        ))
        
        fig.update_layout(
            title='Books Availability',
            height=500,
            showlegend=True
        )
        
    else:
        # Bar chart for not available titles
        not_available = df[df['is_in_stock'] == 0]
        not_available_titles = not_available['title'].value_counts()
        
        # Truncate long titles
        not_available_titles.index = not_available_titles.index.to_series().apply(
            lambda x: x[:50] + '...' if len(x) > 50 else x
        )
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=not_available_titles.values[::-1],
            y=not_available_titles.index[::-1],
            orientation='h',
            marker_color='lightblue',
            text=not_available_titles.values[::-1],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Titles Not Available',
            xaxis_title='Count',
            yaxis_title='Title',
            height=600,
            plot_bgcolor='white'
        )
    
    return fig

# For production deployment
server = app.server

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port)
