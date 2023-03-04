from dash import html

def make_table(df):
    return  html.Table(
        style={
            "font-size":"14px",
            "margin-right":"50px",
        },
        children=[
            html.Thead(
                children=[
                    html.Tr(
                        style={
                            "display":"grid",
                            "grid-template-columns":"repeat(4,1fr)",
                            "font-weight":"bold",
                            "font-size":"14px",
                            "margin":"12px",
                            },
                        children=[
                            html.Th(column_name.replace("_", " ")
                                    ,style={
                                        "text-align":"center",
                                    })
                            for column_name in df.columns
                        ],
                    )
                ]
            )
            ,html.Tbody(
                style={
                    "max-height":"50vh",
                    "display":"block",
                    "overflow":"scroll",
                    },
                children=[
                    html.Tr(
                        style={
                            "display":"grid",
                            "grid-template-columns":"repeat(4,1fr)",
                            "border-top":"1px solid white",
                            "padding": "15px 0px",
                            },
                        children=[
                            html.Td(row_column
                                    ,
                                    style={
                                        "text-align":"center",
                                    })
                            for row_column in row
                        ]
                    ) for row in df.values
                ],
                
            )
        ],
    )

    