import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import openpyxl
from dash import html
import warnings
warnings.filterwarnings(action="ignore")



covid19= pd.read_csv("C:/python/PycharmProjects/data/COVID19Activity.csv")
covid19 = covid19.dropna(axis=0)
covid19.sort_values(by=["PROVINCE_STATE_NAME","COUNTY_NAME","REPORT_DATE"])
covid19["REPORT_DATE"] = pd.to_datetime(covid19['REPORT_DATE'],format='%Y-%m-%d')
covid19["week"] = covid19["REPORT_DATE"].dt.day_name()
covid19_week = covid19.groupby(["COUNTY_NAME","PROVINCE_STATE_NAME","week"],as_index=False)[["PEOPLE_POSITIVE_CASES_COUNT"]].sum()


###### 주소 데이터 #########

juso= pd.read_csv("C:/python/PycharmProjects/data/build_incheon.txt",encoding="cp949",sep="|", header=None)
juso = juso.rename(columns={1:"시도",2:"시군구",3:"읍면동",9:"도로명"})
juso = juso[["시도","시군구","읍면동","도로명"]]
juso["도로명"] = juso["도로명"].str.replace(pat=r'([가-힇]+)[0-9]+.*',repl=r'\1',regex=True)
juso["count"] = 0
for i in range(0, len(juso["count"])):
    if juso["시군구"][i] == "중구":
        juso["count"][i] = "0"
    elif juso["시군구"][i] == "동구":
        juso["count"][i] = "1"
    elif juso["시군구"][i] == "미추홀구":
        juso["count"][i] = "2"
    elif juso["시군구"][i] == "연수구":
        juso["count"][i] = "3"
    elif juso["시군구"][i] == "남동구":
        juso["count"][i] = "4"
    elif juso["시군구"][i] == "부평구":
        juso["count"][i] = "5"
    elif juso["시군구"][i] == "계양구":
        juso["count"][i] = "6"
    elif juso["시군구"][i] == "서구":
        juso["count"][i] = "7"
    elif juso["시군구"][i] == "강화군":
        juso["count"][i] = "8"
    elif juso["시군구"][i] == "옹진군":
        juso["count"][i] = "9"
juso=juso.drop_duplicates(["시도","시군구","읍면동","도로명"])
juso = juso[["도로명","읍면동","시군구","시도","count"]]

fig1= px.sunburst(juso, path=["시도", "시군구", "읍면동", "도로명"],
                   values="count",
                   width=750, height=750, maxdepth=2)

###### 지하철 데이터 #########

subway = pd.read_excel("subway_test.xlsx", engine='openpyxl')

subway = subway.drop_duplicates(["주소"])
#px.set_mapbox_access_token(open("mapbox_token.ipynb").read())

fig2= px.scatter_mapbox(subway, lat="Y", lon="X", color="호선", hover_name="주소", hover_data=["주소", "호선"],
                         width=1000, height=1000, size_max=15, zoom=7)
fig2.update_mapboxes(
    accesstoken="pk.eyJ1Ijoid2pzcXVkZG4iLCJhIjoiY2t3MncyamNjMGg1NjJ2bW03MHZnamZleCJ9.nppVkhhyF-hQdlh4LQgMqw")
fig2.update_layout(mapbox=dict(style="light"))


######## 결혼 이혼 ############
ex = pd.read_csv("C:/python/PycharmProjects/data/report.txt", encoding="utf-8", sep="\t", header=1)
for i in range(0, len(ex["월별"])):
    if ex["월별"][i] == "계":
        ex["월별"][i] = None
    elif ex["자치구"][i] == "합계":
        ex["자치구"][i] = None
ex = ex.dropna(axis=0)
ex["혼인"] = ex["혼인"].str.replace(pat=r',',repl=r'',regex=True)
ex["이혼"] = ex["이혼"].str.replace(pat=r',',repl=r'',regex=True)
ex = ex.astype({"혼인":"int64","이혼":"int64"})
fig3= px.scatter(ex, x="혼인", y="이혼", animation_frame="월별", animation_group="자치구",
                  size="이혼", color="자치구", hover_name="자치구",
                  log_x=True, size_max=55, range_x=[10, 400], range_y=[10, 120])




#### 대시보드 ####

#dash.Dash(external_stylesheets=[dbc.themes.GRID])
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.GRID])

all_continents = covid19.PROVINCE_STATE_NAME.unique()
# 필터링 걸기
app.layout = html.Div([
    dcc.Checklist(id="checklist", options=[{"label": x, "value": x}
                                           for x in all_continents],
                  value=all_continents[50:],
                  labelStyle={'display': 'inline-block'}
                  ),
    dcc.Graph(id="line-chart"),
    dcc.Graph(id="bar-chart"),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3)
])

row = html.Div(
    [
    dbc.Row(
            [
               dbc.Col(html.Div(id="line-chart"), width=2),
                dbc.Col(html.Div(id="bar-chart"), width=2)
            ],
           justify="start"),
html.Br(),
    dbc.Row(
            [
               dbc.Col(html.Div("fig1"), width=2),
                dbc.Col(html.Div("fig2"), width=2)
            ],
            justify="center"),
html.Br(),
    dbc.Row(
        [
                dbc.Col(html.Div("fig3"), width=1)
        ],
            justify="end")

            ]
        )



# input 필터
# ouput 결과

@app.callback(
    Output("line-chart", "figure"),
    [Input("checklist", "value")])
def update_line_chart(PROVINCE_STATE_NAME):
    mask = covid19.PROVINCE_STATE_NAME.isin(PROVINCE_STATE_NAME)
    fig_line = px.scatter(covid19[mask], x="REPORT_DATE", y="PEOPLE_POSITIVE_CASES_COUNT", color="COUNTY_NAME", title="주별 확진자수", width=600, height=750)
    return fig_line


@app.callback(
    Output("bar-chart", "figure"),
    [Input("checklist", "value")])
def update_bar_char(PROVINCE_STATE_NAME):
    mask_bar = covid19_week.PROVINCE_STATE_NAME.isin(PROVINCE_STATE_NAME)
    fig_bar = px.bar(covid19_week[mask_bar], x="week", y="PEOPLE_POSITIVE_CASES_COUNT", color="COUNTY_NAME", width=600,
                     height=750)
    return fig_bar


fig1 = px.sunburst(juso, path=["시도", "시군구", "읍면동", "도로명"],
                   values="count",
                   width=750, height=750, maxdepth=2)


fig2= px.scatter_mapbox(subway, lat="Y", lon="X", color="호선", hover_name="주소", hover_data=["주소", "호선"],
                         width=1000, height=1000, size_max=15, zoom=7)
fig2.update_mapboxes(
    accesstoken="pk.eyJ1Ijoid2pzcXVkZG4iLCJhIjoiY2t3MncyamNjMGg1NjJ2bW03MHZnamZleCJ9.nppVkhhyF-hQdlh4LQgMqw")
fig2.update_layout(mapbox=dict(style="light"))

fig3= px.scatter(ex, x="혼인", y="이혼", animation_frame="월별", animation_group="자치구",
                  size="이혼", color="자치구", hover_name="자치구",
                  log_x=True, size_max=55, range_x=[10, 400], range_y=[10, 120])







app.run_server(debug=True, use_reloader=False)























