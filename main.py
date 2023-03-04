from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from data_processing import countries_df, totals_df, dropdown_options, make_final_df
from table_maker import make_table
stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css",
               'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600&display=swap',]

app = Dash(__name__, external_stylesheets=stylesheets)

server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

fig = px.scatter_geo(countries_df, 
                     locations="Country_Region", locationmode="country names", 
                     color="Confirmed", size="Confirmed", size_max=50,
                     color_continuous_scale=px.colors.sequential.Oryel,
                     projection="natural earth", template="plotly_dark",
                     hover_name="Country_Region", 
                     hover_data={
                         "Country_Region":False,
                         "Confirmed":True,
                         "Deaths":True},
                    )
fig.update_layout(
    geo=dict(
        bgcolor="black",
        landcolor="black",
        countrycolor="white",
        framecolor="#404040",
    ),
    paper_bgcolor="black",
)

bar = px.bar(totals_df, x="condition", y="count")
bar.update_layout(
    font_color="white",
    title=dict(
        font_color="white",
        font_size=24,
        text="Global Total Cases",
    ),
    xaxis=dict(title="Condition"),
    yaxis=dict(title="Count"),
    plot_bgcolor="black",
    paper_bgcolor="black",
    grid_domain_x=[0,0]
)
bar.update_traces(
    marker=dict(color=["#f8885a","#a6363f"],),
    hoverlabel=dict(
        bordercolor="white",
        font=dict(color="white")
    )
)


app.layout = html.Div(
    style={
        "font-family":"Open Sans, sans-serif",
        "max-width":"100vw",
        "min-height":"100vh",
        "background-color":"black",
    },
    children=[
        html.Header(
            style={"color":"white","text-align":"center","padding":"24px 0px",},
            children=[
                html.H1("Corona Dashboard",style={"font-size":"32px",}),
            ],
        ),
        # upper
        html.Div(
            style={
                "display":"grid",
                "grid-template-columns":"repeat(6,1fr)",
                "gap":"50px",
                "margin-bottom":"100px",
            },
            children=[
                dcc.Graph(
                    style={"grid-column":"span 4","background-color":"black"},
                    figure=fig
                    ),
                html.Div(
                    style={"grid-column":"span 2","color":"white"},
                    children=[make_table(countries_df)]
                    ),
                ],
            ),
        # lower
        html.Div(
            style={
                "display":"grid",
                "grid-template-columns":"repeat(6,1fr)",
                "gap":"50px",
                },
            children=[
                dcc.Graph(
                    style={"min-height":"50vh", "grid-column":"span 2"},
                    figure=bar
                    ),
                html.Div(
                    style = {"grid-column":" 3 / -1", "margin-right":"50px",},
                    children=[
                        dcc.Dropdown(
                            id="countries",
                            style={"width":"320px", "margin":"0 auto"},
                            options=[
                                {"label":country,"value":country}
                                for country in dropdown_options["Country_Region"] 
                            ]
                        ),
                        dcc.Graph(id="country-graph")
                        ]
                    ) 
                ]
            )
        ]
    )

@app.callback(Output("country-graph", "figure"), Input("countries", "value"))
def update_graph(country):
    df = make_final_df(country)
    line = px.line(df, x="date", y=["confirmed","deaths","recovered"],
              labels={"value":"Cases", "date":"Date", "variable":"Condition"},
               hover_data={
                   "value":":,",
                   "variable":False,
                   "date":False,
               },
               template="plotly_dark",
              )
    line.update_layout(
    title=dict(
        font_size=24,
        text="Number of Cases by Country",
    ),
    plot_bgcolor="black",
    paper_bgcolor="black",
    )
    line.update_xaxes(
    rangeslider_visible=True,
    showgrid=False,
    tickangle=-45,
    ticklabelstep=2
    )
    line.update_traces(
        hoverlabel=dict(
            bordercolor="white",
            font=dict(color="white")
            )
    )
    return line