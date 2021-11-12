import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import gunicorn
import os






covid19= pd.read_csv("C:\python\COVID-19 Activity.csv")

covid19 = covid19.dropna(axis=0)





### ###########################################################################################################################################
# app = dash.Dash()
#
# all_continents = covid19.PROVINCE_STATE_NAME.unique()
#
# # 필터링 걸기
# app.layout = html.Div([
#     dcc.Checklist(id="checklist", options=[{"label": x, "value": x}
#                                            for x in all_continents],
#                   value=all_continents[50:],
#                   labelStyle={'display': 'inline-block'}
#                   ),
#
#     dcc.Graph(id="line-chart"
# ])
#
#
# # input 필터
# # ouput 결과
#
# @app.callback(
#     Output("line-chart", "figure"),
#     [Input("checklist", "value")])
# def update_line_chart(PROVINCE_STATE_NAME):
#     mask = covid19.PROVINCE_STATE_NAME.isin(PROVINCE_STATE_NAME)
#     fig = px.line(covid19[mask], x="REPORT_DATE", y="PEOPLE_POSITIVE_CASES_COUNT", color="COUNTY_NAME", title="주별 확진자수")
#     return fig
#
#
# app.run_server(debug=True, use_reloader=False)
#
################################################################################################################################################
covid19.sort_values(by=["PROVINCE_STATE_NAME","COUNTY_NAME","REPORT_DATE"])
covid19["REPORT_DATE"] = pd.to_datetime(covid19['REPORT_DATE'],format='%Y-%m-%d')
covid19["week"] = covid19["REPORT_DATE"].dt.day_name()
covid19_week = covid19.groupby(["COUNTY_NAME","PROVINCE_STATE_NAME","week"],as_index=False)[["PEOPLE_POSITIVE_CASES_COUNT"]].sum()



app = dash.Dash(__name__)

server=app.server

all_continents = covid19.PROVINCE_STATE_NAME.unique()

# 필터링 걸기
app.layout = html.Div([
    dcc.Checklist(id="checklist", options=[{"label": x, "value": x}
                                           for x in all_continents],
                  value=all_continents[50:],
                  #labelStyle={'display': 'inline-block'}
                  ),

    dcc.Graph(id="line-chart"),
    dcc.Graph(id="bar-chart")
])


# input 필터
# ouput 결과

@app.callback(
    Output("line-chart", "figure"),
    [Input("checklist", "value")])
def update_line_chart(PROVINCE_STATE_NAME):
    mask = covid19.PROVINCE_STATE_NAME.isin(PROVINCE_STATE_NAME)
    fig = px.scatter(covid19[mask], x="REPORT_DATE", y="PEOPLE_POSITIVE_CASES_COUNT", color="COUNTY_NAME", title="주별 확진자수")
    return fig


@app.callback(
    Output("bar-chart", "figure"),
    [Input("checklist", "value")])
def update_bar_chart(PROVINCE_STATE_NAME):
    mask_bar = covid19_week.PROVINCE_STATE_NAME.isin(PROVINCE_STATE_NAME)
    fig_bar = px.bar(covid19_week[mask_bar], x="PEOPLE_POSITIVE_CASES_COUNT", y="week", color="COUNTY_NAME", width=1500,
                     height=800,  orientation='h')
    return fig_bar


app.run_server(debug=True, use_reloader=False)