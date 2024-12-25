import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to get data from SQLite database
def get_data():
    try:
        conn = sqlite3.connect('covid_vaccine.db')
        query = "SELECT * FROM covid_vaccine_data"
        df = pd.read_sql_query(query, conn)
        conn.close()
        logger.info(f"Data retrieved successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error

# Layout of the dashboard
app.layout = html.Div([
    html.H1("COVID-19 and Vaccination Dashboard", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # First row with two cards showing total cases and total vaccinations
    html.Div([
        html.Div([
            html.H4("Total COVID-19 Cases", style={'textAlign': 'center'}),
            html.Div(id='total-cases', style={'textAlign': 'center', 'fontSize': 24})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)', 'backgroundColor': 'white'}),
        
        html.Div([
            html.H4("Total Vaccinations", style={'textAlign': 'center'}),
            html.Div(id='total-vaccinations', style={'textAlign': 'center', 'fontSize': 24})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)', 'backgroundColor': 'white', 'marginLeft': '4%'})
    ], style={'marginBottom': 30}),
    
    # Second row with two graphs
    html.Div([
        html.Div([
            dcc.Graph(id='cases-vs-vaccinations')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='vaccination-rate-chart')
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
    ], style={'marginBottom': 30}),
    
    # Third row with one graph
    html.Div([
        dcc.Graph(id='net-infection-rate')
    ], style={'marginBottom': 30}),
    
    # Update interval
    dcc.Interval(
        id='interval-component',
        interval=300 * 1000,  # update every 5 minutes
        n_intervals=0
    )
], style={'padding': '20px', 'backgroundColor': '#f0f2f5'})

# Callbacks to update the dashboard
@app.callback(
    [Output('total-cases', 'children'),
     Output('total-vaccinations', 'children'),
     Output('cases-vs-vaccinations', 'figure'),
     Output('vaccination-rate-chart', 'figure'),
     Output('net-infection-rate', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    try:
        df = get_data()
        if df.empty:
            raise ValueError("No data available")
            
        # Calculate totals
        total_cases = f"{int(df['total_cases'].sum()):,}"
        total_vaccinations = f"{int(df['total_vaccinations'].sum()):,}"
        
        # Create cases vs vaccinations scatter plot
        fig1 = px.scatter(df, x='total_cases', y='total_vaccinations', 
                         text='country',  # Add country labels
                         title='COVID-19 Cases vs Vaccinations by Country',
                         labels={'total_cases': 'Total Cases', 
                                'total_vaccinations': 'Total Vaccinations'})
        fig1.update_traces(textposition='top center')
        
        # Create vaccination rate bar chart
        fig2 = px.bar(df, x='country', y='vaccination_rate',
                      title='Vaccination Rate by Country',
                      labels={'vaccination_rate': 'Vaccination Rate (%)', 
                             'country': 'Country'},
                      color='vaccination_rate',
                      color_continuous_scale='Viridis')
        
        # Create infection vs vaccination rate chart
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df['country'],
            y=df['infection_rate'],
            name='Infection Rate',
            marker_color='#ff7f7f'
        ))
        fig3.add_trace(go.Bar(
            x=df['country'],
            y=df['vaccination_rate'],
            name='Vaccination Rate',
            marker_color='#7fb3ff'
        ))
        fig3.update_layout(
            barmode='group',
            title='Infection Rate vs Vaccination Rate by Country',
            yaxis_title='Rate (%)'
        )
        
        return total_cases, total_vaccinations, fig1, fig2, fig3
        
    except Exception as e:
        logger.error(f"Error updating dashboard: {e}")
        # Return empty figures in case of error
        empty_fig = go.Figure()
        return "N/A", "N/A", empty_fig, empty_fig, empty_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)