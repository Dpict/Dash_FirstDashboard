from dash import Dash,html,dcc,dash_table,callback
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import seaborn as sns

iris = sns.load_dataset('iris')

def header(title,app):
    title = html.H2(title, className= 'title')
    app = html.Img(src = app.get_asset_url('dash-logo.png'), className= 'app')
    return dbc.Row([dbc.Col(title, md = 9,className="d-flex align-items-center"), dbc.Col(app, md =3,className="d-flex justify-content-end align-items-center")],className="flex-nowrap")

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP,'styles.css'])
app.layout = dbc.Container([
    header('Iris Analysis Dataset', app)
    ,html.Hr(className ='Line1')
]),dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H4('Sepal Rankings',style={'textAlign': 'center'})
                ,html.H6('Top 5', style={'textAlign': 'center'})
                ,dash_table.DataTable(id='table'
                                     ,columns=[{"name": i
                                                ,"id": i} for i in iris[['sepal_length'
                                                                                   , 'sepal_width'
                                                                                   ,'species']].columns]
                                     ,data=[]
                                     ,style_table={
                                         'width': '100%',  # Ensure the table takes full width of the card
                                         'overflowX': 'auto',  # Add horizontal scrolling if content overflows
                                         'maxWidth': '100%',  # Prevent it from stretching beyond the card's width
                                         }
                                         ,style_cell={
                                             'textAlign': 'center',  # Center text inside each cell
                                             #'padding': '10px',  # Add some padding for readability
                                             }
                                    )
                                    ],body=True
                                    ,color="light")
                                    ,md = 4
        ),
        dbc.Col(
            dbc.Card([
                html.H4('Species Average', style={'textAlign':'center'})
                ,dash_table.DataTable(id = 'table3'
                              ,columns = [{'name': i, 'id': i,} for i in ['Species'
                                                                         , 'Sepal Length'
                                                                         , 'Sepal Width'
                                                                         , 'Petal Length'
                                                                         , 'Petal Width']]
                              ,data=[]
                              ,style_table={'overflowY': 'scroll'}
                              ,style_header={'backgroundColor': '#343a40', 'color': 'white'}
                              ,style_cell={'backgroundColor': '#2f3436', 'color': 'white', 'textAlign': 'center'}
                              ,style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#383d41'}]
                             )
            ]
            ,body=True
            ,color="dark"
            ,inverse=True
            )
            ,md = 4
        )
        ,dbc.Col(
            dbc.Card([
                html.H4('Petals Ranking',style={'textAlign': 'center'})
                ,html.H6('Top5',style={'textAlign': 'center'})
                ,dash_table.DataTable(id = 'table2'
                                      ,columns = [{'name':i
                                                   ,'id':i} for i in iris[['petal_length'
                                                                           ,'petal_width'
                                                                           ,'species']].columns]
                                                                           ,data=[]
                                                                           ,style_header={'backgroundColor': "#0c7ff2", 'color': 'white'}
                                                                           ,style_cell={'backgroundColor': "#0c7ff2", 'color': 'white', 'textAlign': 'center'}
                                                                           ,style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': "#0c7ff2"}]
                                                                           ,style_table={
                                         'width': '100%',  # Ensure the table takes full width of the card
                                         'overflowX': 'auto',  # Add horizontal scrolling if content overflows
                                         'maxWidth': '100%',  # Prevent it from stretching beyond the card's width
                                         }
                                        )
            ]
            ,body=True
            ,color="primary"
            ,inverse=True
            )
            ,md = 4
        )
        ])
    ,html.Br()
    ,dbc.Row([
        dbc.Col(
            dcc.Dropdown(
            id = 'Dp1'
            ,options = iris['species'].unique()
            ,multi = True
        )
        , md =6)
        ,dbc.Col(dcc.Dropdown(
            id = 'Dp2'
            ,options = iris['species'].unique()
            ,multi = True
        )
        ,md =6)
    ]
    ,justify = 'center'
    )
    ,dbc.Row([
        dbc.Col(dcc.Graph(id = 'graph1')
                ,md=6) #For Mobile 
        ,dbc.Col(dcc.Graph(id='graph2')
                 ,md=6) #For Mobile 
],justify = 'center')
    ,dbc.Row([
        dbc.Col([
            html.Div(children='Iris Dataset')
            ,dash_table.DataTable(data=iris.to_dict('records')
                                  ,page_size = 10
                                  , style_table={
                'width': '100%',  # Make the table width 100% of its container
                'overflowX': 'auto',  # Enable horizontal scrolling if content overflows
                'maxWidth': '100%'  # Ensure it doesn't stretch beyond the container
            },
            style_cell={
                'textAlign': 'center'}
                )
        ]
        ,md = {'size':8
               ,'offset':2})
    ])
])

@callback(
Output('graph1', 'figure')
,Input('Dp1','value')
)
def graph1(lin):
    if not lin:
        raise PreventUpdate
    figure = px.scatter(
        iris.query(f'species in {lin}')
        ,x = 'sepal_width'
        ,y = 'sepal_length'
        ,color = 'species'
        ,render_mode = 'webgl'
        ,template = "simple_white"
    )
    #figure.update_xaxes(showgrid=True) #showing x-grid lines
    figure.update_yaxes(showgrid=True) #showing y-grid lines
    figure.update_layout(
    xaxis_title='Width of Sepal (cm)',
    yaxis_title='Length of Sepal (cm)'
)
    return figure

@callback(
Output('graph2', 'figure')
,Input('Dp2','value')
)
def graph2(lin):
    if not lin:
        raise PreventUpdate
    figure = px.scatter(
        iris.query(f'species in {lin}')
        ,x = 'petal_width'
        ,y = 'petal_length'
        ,color = 'species'
        ,render_mode = 'webgl'
        ,template = "simple_white"
    )
    #figure.update_xaxes(showgrid=True) #showing x-grid lines
    figure.update_yaxes(showgrid=True) #showing y-grid lines
    figure.update_layout(
    xaxis_title='Width of Petal (cm)',
    yaxis_title='Length of Petal (cm)'
)
    return figure    
# end def

# In your callback
@callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('Dp1', 'value')
)

#Top 5 Sepal
def cb1(selector):
    if not selector:
        raise PreventUpdate
    
    filtered_iris = iris[iris['species'].isin(selector)] if isinstance(selector, list) else iris[iris['species'] == selector]
    
    top_i = filtered_iris.nlargest(5, 'sepal_length')
    sepal_values = top_i[['sepal_length', 'sepal_width', 'species']]
    
    columns = [{"name": i, "id": i} for i in sepal_values.columns]
    data = sepal_values.to_dict('records')
    
    return data, columns
# end def
@callback(
Output('table2','data')
,Output('table2','columns')
,Input('Dp2','value')
)

#Top 5 Petal 
def cb2(picker):
    if not picker:
        raise PreventUpdate
    
    filtered_petal = iris[iris['species'].isin(picker)] if isinstance(picker, list) else iris[iris['species'=='species']]
    
    top_i = filtered_petal.nlargest(5, 'petal_length')
    petal_values = top_i[['petal_length','petal_width','species']]

    columns = [{'name': i, 'id':i} for i in petal_values.columns]
    data = petal_values.to_dict('records')

    return data,columns
# end def

#Average table Update
@callback(
    [Output('table3', 'data'),
     Output('table3', 'columns')],
    Input('Dp1', 'value'),
    prevent_initial_update=True
)
def update_table(selector):
    if not selector:
        return [], [{'name': i, 'id': i} for i in ['Species'
                                                   , 'Sepal Length'
                                                   , 'Sepal Width'
                                                   , 'Petal Length'
                                                   , 'Petal Width']]
    
    selector = selector if isinstance(selector, list) else [selector]
    filtered_iris = iris[iris['species'].isin(selector)]
    
    average_measurements = filtered_iris.groupby('species')[['sepal_length'
                                                             ,'sepal_width'
                                                             ,'petal_length'
                                                             ,'petal_width']].mean().reset_index()
    
    average_measurements = average_measurements.rename(columns={
        'sepal_length': 'Sepal Length',
        'sepal_width': 'Sepal Width',
        'petal_length': 'Petal Length',
        'petal_width': 'Petal Width',
        'species': 'Species'
    })
    
    columns = [{'name': i, 'id': i, 'type': 'numeric', 'format': {'specifier': '.2f'}} if i != 'Species' else {'name': i, 'id': i} for i in average_measurements.columns]
    
    return average_measurements.to_dict('records'), columns

if __name__ == '__main__':
    app.run()