# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px


color_pln = ['#f7e82e','#4ca8e0','#e72a2b']

promotion = pd.read_csv('data_input/promotion.csv')
promotion = promotion.dropna()

promotion['KPIs_met >80%'] = promotion['KPIs_met >80%'].map({0: 'No', 1: 'Yes'})
promotion['awards_won?'] = promotion['awards_won?'].map({0: 'No', 1: 'Yes'})
promotion['is_promoted'] = promotion['is_promoted'].map({0: 'No', 1: 'Yes'})
promotion['gender'] = promotion['gender'].map({'m': 'Male', 'f': 'Female'})

promotion[['department','region','education',
           'gender','recruitment_channel',
           'KPIs_met >80%','awards_won?',
           'is_promoted']] = promotion[['department','region',
                                        'education','gender',
                                        'recruitment_channel',
                                        'KPIs_met >80%','awards_won?',
                                        'is_promoted']].astype('category')


# # higest_promotion_rate
# promoted = promotion[promotion['is_promoted'] == 'Yes']
# aspect_promoted = promoted['department'].value_counts(normalize=True).round(2).reset_index()

# previous_rating_&_education
dept_hr = promotion[promotion['department'] == 'HR']


# First card content - Information
card_information = [
    dbc.CardHeader('Information'),
    dbc.CardBody(
        [
            html.P(
                "This is the information of employeed in our Start-Up. help to identify who is a potential candidate for promotion",
                className="card-text",
            ),
        ]
    ),
]


sum_promoted = promotion[promotion['is_promoted']=='Yes'].shape[0]

card_promoted = [
    dbc.CardHeader("Who is Promoted?"),
    dbc.CardBody(
        [
            html.H2(sum_promoted, className="card-title"),
        ]
    ),
]

list_category = [
    {
        'label': 'Department',
        'value': 'department'
    },
    {
        'label': 'Region',
        'value': 'region'
    },
    {
        'label': 'Gender',
        'value': 'gender'
    },
    {
        'label': 'Recruitment Channel',
        'value': 'recruitment_channel'
    },
    {
        'label': 'KPIs met > 80%?',
        'value': 'KPIs_met >80%'
    },
    {
        'label': 'Awards won?',
        'value': 'awards_won?'
    },
]

# 2. Create a Dash app instance
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    html.Br(),
    html.H1(children='Employee Promotion Analysis'),
    html.Br(),

    # Here for cards
    dbc.Row(
            [
                dbc.Col(dbc.Card(card_information, color="primary", outline=True), width=6),
                dbc.Col(dbc.Card(card_promoted, color="warning", inverse=True), width=2),
                dbc.Col(dbc.Card(card_promoted, color="info", inverse=True), width=2),
                dbc.Col(dbc.Card(card_promoted, color="danger", inverse=True), width=2),
            ],
            className="mb-4",
        ),
    html.Hr(), html.Br(),

    # Here for the first row
    dbc.Row(
        dcc.Dropdown(id='category_promotion_picker',
                    options=list_category,
                    value='department')
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(
                id='higest_promotion_rate',

            )),
        ],
    className="mb-4"
    ), html.Br(),

    # Here for the second row
    dbc.Row(
        [
            dbc.Col(dcc.Graph(
                id='previous_rating_education',
                figure=px.density_heatmap(
                                        dept_hr,
                                        x = 'previous_year_rating',
                                        y = 'education',
                                        title = 'Number of Employee by Previous Rating and Education',
                                        labels={
                                            'education': 'Education',
                                            'previous_year_rating': 'Previous Year Rating'
                                        },
                                        template = 'ggplot2',
                                        color_continuous_scale=color_pln
                                        )

            )),
            dbc.Col(dcc.Graph(
                id='relation_length_service',
                figure=px.scatter(
                                dept_hr,
                                x = 'length_of_service',
                                y = 'avg_training_score',
                                title = 'The Relation of Length of Service and Average Training Score',
                                color = 'KPIs_met >80%',
                                facet_col = 'is_promoted',
                                size = 'no_of_trainings',
                                color_discrete_sequence=color_pln,
                                labels = {
                                        'length_of_service' : 'Length of Service',
                                        'avg_training_score' : 'Score',
                                        'KPIs_met >80%': 'KPIs met >80%?',
                                        'no_of_trainings': 'No. of Trainings',
                                        'is_promoted': 'Promoted Status'
                                        }
                                )

            ))
        ],
    className="mb-4"
    ),
])

@app.callback(
    Output('higest_promotion_rate', 'figure'), # Output from graphic
    Input('category_promotion_picker', 'value') # Input from dropdown
)

def update_figure(value):
    # higest_promotion_rate
    promoted = promotion[promotion['is_promoted'] == 'Yes']
    aspect_promoted = promoted[value].value_counts(normalize=True).round(2).reset_index()

    bar_graph = px.bar(aspect_promoted,
                                x = 'index',
                                y = value,
                                title = 'Which aspect have the highest promotion rate?',
                                color_discrete_sequence = ['#4ca8e0'],
                                labels = {
                                    'index':str(value.title()),
                                    str(value):'Percentage'
                                        }
                                )

    return bar_graph



# 5. Start the Dash server
if __name__ == "__main__":
    app.run_server()
