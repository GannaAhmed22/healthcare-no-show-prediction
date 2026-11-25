import pandas as pd
import plotly.express as px

from dash import Dash, html, dcc, Input, Output

DARK_BLUE = "#17324D"
BLUE = "#2563EB"
MEDIUM_BLUE = "#3B82F6"
LIGHT_BLUE = "#60A5FA"
PALE_BLUE = "#BFDBFE"

BACKGROUND = "#F0F7FF"

STATUS_COLORS = {
    "Attended": BLUE,
    "No-Show": LIGHT_BLUE
}

AGE_COLORS = [
    DARK_BLUE,
    BLUE,
    MEDIUM_BLUE,
    LIGHT_BLUE,
    "#93C5FD",
    PALE_BLUE
]

reminder_options = [
    {"label": "Sent", "value": 1},
    {"label": "Not Sent", "value": 0}
]


def create_dropdown_list(column):

    dd_values = data[column].unique()

    options = []

    for value in dd_values:
        options.append({
            "label": value,
            "value": value
        })

    return options


def create_card(title, value):

    return html.Div(

        children=[

            html.P(
                title,
                style={
                    "color": "#64748B",
                    "fontSize": "15px",
                    "marginBottom": "10px"
                }
            ),

            html.H2(
                value,
                style={
                    "color": DARK_BLUE,
                    "fontSize": "28px",
                    "margin": "0"
                }
            )

        ],

        style={
            "backgroundColor": "white",
            "padding": "20px",
            "borderRadius": "12px",
            "textAlign": "center",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"
        }

    )

def dropdown_componenet(var_label,var_id):
     html.Div([
    
                        html.Label(
                            var_label,
                            style={"fontWeight": "bold"}
                        ),
    
                        dcc.Dropdown(
                            id=var_id,
                            options=reminder_options,
                            placeholder="All",
                            clearable=True
                        )
    
                    ])
    
app = Dash(__name__)

app.title = "Healthcare Analytics Dashboard"

app.layout = html.Div(

    children=[

        html.H1(
            "Healthcare Appointment Dashboard",
            style={
                "color": DARK_BLUE,
                "textAlign": "center",
                "marginBottom": "5px"
            }
        ),

        html.P(
            "Analyze appointment attendance and no-show patterns",
            style={
                "color": "#64748B",
                "textAlign": "center",
                "marginBottom": "30px"
            }
        ),


        html.Div(

            children=[
                dropdown_componenet("Specialty","specialty-filter"),
                dropdown_componenet("Reminder Channel","channel-filter"),
                dropdown_componenet("Reminder Sent","reminder-filter")
               

            ],

            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(3, 1fr)",
                "gap": "20px",
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "marginBottom": "25px"
            }

        ),



        html.Div(

            id="filter-container",

            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(3, 1fr)",
                "gap": "20px",
                "marginBottom": "30px"
            }

        ),


        html.Div(

            children=[

                dcc.Graph(
                    id="status-pie-chart",
                    config={"displayModeBar": False}
                ),

                dcc.Graph(
                    id="age-pie-chart",
                    config={"displayModeBar": False}
                ),

                dcc.Graph(
                    id="monthly-chart",
                    config={"displayModeBar": False},
                    style={"gridColumn": "span 2"}
                )

            ],

            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
                "gap": "15px",
                "backgroundColor": BACKGROUND,
                "alignItems": "stretch"
            }

        )

    ],

    style={
        "backgroundColor": BACKGROUND,
        "minHeight": "100vh",
        "padding": "30px",
        "fontFamily": "Arial"
    }

)


@app.callback(

    [

        Output("filter-container", "children"),

        Output("status-pie-chart", "figure"),

        Output("age-pie-chart", "figure"),

        Output("monthly-chart", "figure")

    ],

    [

        Input("specialty-filter", "value"),

        Input("channel-filter", "value"),

        Input("reminder-filter", "value")

    ]

)


def update_graphs(specialty, channel, reminder):


    filtered_data = data

    if specialty is not None:

        filtered_data = filtered_data[
            filtered_data["specialty_group"] == specialty
        ]

    if channel is not None:

        filtered_data = filtered_data[
            filtered_data["reminder_channel"] == channel
        ]

    if reminder is not None:

        filtered_data = filtered_data[
            filtered_data["reminder_sent_flag"] == reminder
        ]


    

    no_show_appointments = (
        filtered_data["no_show_flag"] == 1
    ).sum()

    attended_appointments = (
        filtered_data["no_show_flag"] == 0
    ).sum()

    if len(filtered_data) > 0:

        no_show_rate = (
            no_show_appointments / len(filtered_data)
        ) * 100

    else:

        no_show_rate = 0


    kpi_cards = [

        create_card(
            "Total Appointments",
            f"{len(filtered_data):,}"
        ),

        create_card(
            "No-Show Rate",
            f"{no_show_rate:.2f}%"
        ),

        create_card(
            "Attended Appointments",
            f"{attended_appointments:,}"
        )

    ]


   
    if filtered_data.empty:

        empty_status = px.pie(
            title="No Appointment Data Available"
        )

        empty_age = px.pie(
            title="No Age Data Available"
        )

        empty_monthly = px.line(
            title="No Monthly Data Available"
        )

        return (
            kpi_cards,
            empty_status,
            empty_age,
            empty_monthly
        )



    status_data = (

        filtered_data["no_show_flag"]

        .map({
            0: "Attended",
            1: "No-Show"
        })

        .value_counts()

        .reindex(
            ["Attended", "No-Show"],
            fill_value=0
        )

        .reset_index()

    )

    status_data.columns = [
        "status",
        "appointments"
    ]



    status_chart = px.pie(

        status_data,

        names="status",

        values="appointments",

        hole=0.4,

        color="status",

        color_discrete_map=STATUS_COLORS,

        title="Appointment Status Distribution"

    )

    status_chart.update_traces(
        textinfo="percent+label",
        textposition="inside"
    )


    age_data = (

        filtered_data.groupby("age_group", observed=True).size().reset_index(name="appointments")

    )

    age_chart = px.pie(

        age_data,

        names="age_group",

        values="appointments",

        hole=0.4,

        color="age_group",

        color_discrete_sequence=AGE_COLORS,

        title="Appointments by Age Group"

    )

    age_chart.update_traces(
        textinfo="percent+label",
        textposition="inside"
    )

    monthly_data = (

        filtered_data

        .groupby(["month_num", "no_show_flag"])

        .size()

        .reset_index(name="appointments")

    )

    monthly_data["status"] = (

        monthly_data["no_show_flag"]

        .map({
            0: "Attended",
            1: "No-Show"
        })

    )


    monthly_chart = px.line(

        monthly_data,

        x="month_num",

        y="appointments",

        color="status",

        markers=True,

        color_discrete_map=STATUS_COLORS,

        title="Attended vs No-Show Appointments per Month",

        labels={
            "month_num": "Month",
            "appointments": "Number of Appointments",
            "status": "Appointment Status"
        }

    )

    monthly_chart.update_traces(
        marker={"size": 9},
        line={"width": 3}
    )

    charts = [
        status_chart,
        age_chart,
        monthly_chart
    ]

    for figure in charts:

        figure.update_layout(

            plot_bgcolor="white",

            paper_bgcolor="white",

            font={
                "family": "Arial",
                "color": DARK_BLUE
            },

            title={
                "font": {
                    "size": 17,
                    "color": DARK_BLUE
                },
                "x": 0.5,
                "xanchor": "center"
            },

            margin={
                "l": 25,
                "r": 25,
                "t": 65,
                "b": 25
            },

            legend={
                "orientation": "h",
                "y": -0.15
            }

        )


    monthly_chart.update_xaxes(
        dtick=1,
        gridcolor=PALE_BLUE
    )

    monthly_chart.update_yaxes(
        gridcolor=PALE_BLUE
    )


    return (

        kpi_cards,

        status_chart,

        age_chart,

        monthly_chart

    )


if __name__ == "__main__":

    app.run(debug=True)
