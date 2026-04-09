import dash_design_kit as ddk
import numpy as np
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc

app = Dash(__name__)
server = app.server


df = px.data.gapminder()

app.layout = ddk.App(
    [
        ddk.Header(
            [
                ddk.Logo(src=app.get_asset_url("logo.png")),
                ddk.Title("GoPro Test 2"),
            ]
        ),
        ddk.ControlCard(
            [
                ddk.ControlItem(
                    dcc.Dropdown(
                        df["country"].unique(),
                        ["Canada", "Panama", "Norway", "France"],
                        multi=True,
                        id="dropdown-country",
                    ),
                    label="Country",
                ),
                ddk.ControlItem(
                    dcc.RangeSlider(
                        min=df["year"].min(),
                        max=df["year"].max(),
                        marks={
                            int(year): str(year) for year in sorted(df["year"].unique())
                        },
                        value=[df["year"].min(), df["year"].max()],
                        step=None,
                        id="slider",
                    ),
                    label="Year Range",
                ),
                ddk.ControlItem(
                    dcc.Dropdown(
                        options={
                            "lifeExp": "Life Expectancy",
                            "pop": "Population",
                            "gdpPercap": "GDP per Capita",
                        },
                        value="pop",
                        id="dropdown-y-axis",
                    ),
                    label="Y-axis Variable",
                ),
            ],
            orientation="horizontal",
        ),
        ddk.Card(
            children=ddk.Graph(id="graph"),
        ),
    ],
    show_editor=True,
)


@callback(
    Output("graph", "figure"),
    Input("dropdown-country", "value"),
    Input("slider", "value"),
    Input("dropdown-y-axis", "value"),
)
def update_graph(country, year_range, y_axis):
    df = px.data.gapminder()
    filtered_df = df[df["country"].isin(country)]
    filtered_df = filtered_df[
        (filtered_df["year"] >= year_range[0]) & (filtered_df["year"] <= year_range[1])
    ]
    figure = px.line(
        filtered_df, x="year", y=y_axis, color="country", title=f"{y_axis} by Country"
    )
    return figure


if __name__ == "__main__":
    app.run(debug=True, port=8050)
