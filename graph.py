import plotly.express as px

def get_plotly_fig(df, y_series):
    """
    Return a Plotly figure object that can be displayed in the streamlit app.
    """

    # Sort the data in cronological order so the data appears in the correct order on the graph
    df = df.sort_values(by='DATE', ascending=True, na_position='first')

    # Construct the graph and style it. Further customize your graph by editing this code.
    # See Plotly Documentation for help: https://plotly.com/python/plotly-express/
    fig = px.line(df, x='DATE', y=y_series, color='NAME', line_shape='linear')
    fig.update_layout(
        title=f'{y_series} by Bank', 
        xaxis = dict(
            showgrid=True, 
            rangeslider = dict(
                visible=True, 
                thickness=0.05
            )
        ), 
        yaxis = dict(
            showgrid=True
        ), 
        legend = dict(
            orientation='v'
        ), 
    )

    return fig
