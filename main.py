#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# ### 图1：世界地图可视化
# 
# 使用plotly 画出。

# In[2]:


df1 = pd.read_excel('数据_已处理图1、2.xlsx', sheet_name="教育投入与可视化地图")


# In[3]:


df1.columns


# In[4]:


df1.教育投入占GDP比例.describe()


# In[5]:


import plotly.express as px
fig1_1 = px.choropleth(df1, locations="Country Code", 
                    color="教育投入占GDP比例",
                    hover_name="Country Name",
                    #title = '地图可视化: %s' %('教育投入占GDP比例'),
                    range_color=[0,max(df1.教育投入占GDP比例)])
fig1_1.show()


# In[6]:


import plotly.express as px
fig1_2 = px.choropleth(df1, locations="Country Code", 
                    color="初等教育投入比例",
                    hover_name="Country Name",
                    # title = '地图可视化: %s' %("初等教育投入比例"),
                    range_color=[0,max(df1.初等教育投入比例)])
fig1_2.update_layout()
fig1_2.show()


# In[7]:


import plotly.express as px
fig1_3 = px.choropleth(df1, locations="Country Code", 
                    color="中等教育投入比例",
                    hover_name="Country Name",
                    # title = '地图可视化: %s' %('中等教育投入比例'),
                    range_color=[0,max(df1.中等教育投入比例)])

fig1_3.show()


# In[8]:


fig1_4 = px.choropleth(df1, locations="Country Code", 
                    color="高等教育投入比例",
                    hover_name="Country Name",
                    # title = '地图可视化: %s' %('高等教育投入比例'),
                    range_color=[0,max(df1.高等教育投入比例)])

fig1_4.show()


# ### 图2：气泡图
# 
# 使用 plotly 套件画出。

# In[9]:


df2 = pd.read_excel('数据_已处理图1、2.xlsx', sheet_name="人均GDP_受教育程度")


# In[10]:


df2.columns


# In[11]:


# bubble chart
# https://plotly.com/python/bubble-charts/?utm_source=mailchimp-jan-2015&utm_medium=email&utm_campaign=generalemail-jan2015&utm_term=bubble-chart
## hover text
# https://plotly.com/r/hover-text-and-formatting/
# https://plotly.com/python/hover-text-and-formatting/
import plotly.express as px
fig2 = px.scatter(df2, x='人均GDP（美元)',y='高中及以上受教育人口比例',
                size='人口',color='Region',
                hover_name="Country Name",log_x =True,size_max=60,)
fig2.show()


# ### 图3：变化条形图
# 
# 使用 matplotlib 画出。

# In[12]:


# 导入库文件
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
import matplotlib
#防止动漫内存太大，报错
matplotlib.rcParams['animation.embed_limit'] = 2**128


#pandas读取数据，且去列名分别为name,group,year和value的值；,usecols=['countryname', 'group', 'year', 'value']
df = pd.read_csv('data_plot3.csv',engine='python',header=1,names=['name', 'group', 'year', 'value'])
df.head()

#导入random函数，randomcolor用于生成颜色代码
# randomcolor生成颜色代码原理，
# 【1-9/A-F】15个数字随机组合成6位字符串前面再加上一个“#”号键

'''import random
def randomcolor():
    colorlist = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color =''
    for i in range(6):
        color += random.choice(colorlist)
    return '#'+ color

#对地区列表进行去重，分类；
area_list1 = set(df['Country Name'])

# color_list用于存放随机生成颜色代码个数
# 因为后面区域个数 要与颜色个数保持一致，这里用了len函数；
color_list =[]
for i in range(len(area_list1)):
    str_1 = randomcolor()

    color_list.append(str_1)
    str_1 = randomcolor()
    
print(color_list)
#area_list转化为列表
area_list_1 = [i for i in area_list1]
print(area_list_1)

#colors表示 所在城市：颜色 一一对应字典形式；
colors =dict(zip(area_list_1,color_list))
print(colors)'''

#group_lk为 城市：所在区域 --对应字典形式；
group_lk = df.set_index('name')['group'].to_dict()
print(group_lk)

colors = dict(zip(
     ["East Asia & Pacific", "Europe & Central Asia", "Latin America & Caribbean", "Middle East & North Africa", "North America", "South Asia", "Sub-Saharan Africa"],
     ["#adb0ff", "#ffb3ff", "#90d595", "#e48381", "#aafbff", "#f7bb5f", "#eafb50","#edab10"]
 ))
# group_lk = df.set_index('name')['group'].to_dict()

# 用plt加理图表，figsize表示图标长宽，ax表示标签
fig, ax = plt.subplots(figsize=(15, 8))

#dras_barchart生成current_year这一年各城市人口基本情况；
def draw_barchart(current_year):
    
    #dff对year==current_year的行，以value从升序方式排序，取后十名也就是最大值；
    dff = df[df['year'].eq(current_year)].sort_values(by='value',ascending = True).tail(12)
    # 所有坐标、标签清除
    ax.clear()
    #显示颜色、城市名字
    ax.barh(dff['name'],dff['value'],color = [colors[x] for x in dff['group']])
    
    dx = dff['value'].max()/200
    
    #ax.text(x,y,name,font,va,ha)
    # x,y表示位置；
    # name表示显示文本；
    # va,ba分别表示水平位置，垂直放置位置；
    for i ,(value,name) in enumerate(zip(dff['value'], dff['name'])):
        ax.text(value-dx,i,name,size=14,weight=600,ha ='right',va = 'bottom')
        ax.text(value-dx,i-.25,group_lk[name],size = 10,color ='#444444',ha ='right',va = 'baseline')
        ax.text(value+dx,i ,f'{value:,.0f}',size = 14,ha = 'left',va ='center')
    
    #ax.transAxes表示轴坐标系，(1,0.4)表示放置位置
    ax.text(1,0.4,current_year,transform = ax.transAxes,color ='#777777',size = 46,ha ='right',weight=800) 
    ax.text(0,1.06,'Per capita investment in education(dollars)',transform = ax.transAxes,size=12,color='#777777')
    
    #set_major_formatter表示刻度尺格式；
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x',colors='#777777',labelsize=12)
    ax.set_yticks([])
    #margins表示自动缩放余额；
    ax.margins(0,0.01)
    # 设置后面的网格
    ax.grid(which='major',axis='x',linestyle='-')
    #刻度线和网格线是在图标上方还是下方，True为下方
    ax.set_axisbelow(True)
    ax.text(0,1.15,'Per capita investment in education from 1970 to 2018',
           transform=ax.transAxes,size=24,weight=600,ha='left',va='top')
    #取消图表周围的方框显示
    plt.box(False)

#绘制2018年各城市人口情况
draw_barchart(2018)

#将原来的静态图拼接成动画
fig, ax = plt.subplots(figsize=(15, 8))
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(1970, 2018))


# In[13]:


df4 = pd.read_csv('data_plot3.csv')
fig4 = px.bar(df4,x="name",y="value",color='group',
             animation_frame='year',range_y=[0,350000])
fig4.show()


# In[14]:


df4.columns


# ### 利用Dash 形成网页

# ### Reference
# 
# Dash App
# - https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-opioid-epidemic/app.py#L107
# 
# Dash Core Components
# - https://dash.plotly.com/dash-core-components
# 
# Video Addition
# - https://community.plotly.com/t/adding-video-player/5303
# - https://dash.plotly.com/dash-html-components/video

# In[ ]:


import os
import pathlib
import re
import flask

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ])

colors = {
    'background':'#3d5a80',
    'text':'#355070'
}

app.layout = html.Div(
    id = "root",
    style = {},
    children = [
        html.Div(
            id="header",
            children = [
                html.H1(
                    children="各国教育可视化",
                    style = {'color':colors["text"],
                             'textAlign':'center',
                             'font-family':'Microsoft JhengHei',
                            },
                       ),
                html.P(
                    id="description",
                    children = "|| 利用世界银行的世界发展指标，来观察各国教育发展情形。 ||",
                    style = {'color':'#495057',
                             'font-family':'Microsoft JhengHei', 
                             'font-size': "2",
                             'textAlign':'center',
                            },
                       ),
                    ],
                ),
        html.Div(
            id = "app-container",
            children = [
                html.Div(
                    id = "left-column",
                    style={'width': '49%','display': 'inline-block'},
                    children = [
                        html.P(
                          id = "plot-selector",
                          children = "Select:"),
                        dcc.Dropdown(
                          options = [
                              {"label":"教育投入占GDP比例",
                               "value": "教育投入占GDP比例",},
                              {"label":"初等教育投入比例",
                               "value": "初等教育投入比例",},
                              {"label":"中等教育投入比例",
                               "value": "中等教育投入比例",},
                              {"label":"高等教育投入比例",
                               "value": "高等教育投入比例",},
                          ],
                          value = "教育投入占GDP比例",
                          id="chart-dropdown",
                        ),
                        dcc.Graph(
                            id = "selected-data",
                            figure = fig1_1,
                                      
                        ),
                    ],
                ),
                html.Div(
                    id = "right-column",
                    style={'width': '49%',
                           'float':'right', 
                           'display': 'inline-block'},
                    children=[
                        html.H4(
                            children = "气泡图",
                            style = {
                            'font-family':'Microsoft JhengHei'
                                    },
                        ),
                        dcc.Graph(
                            id = "bubble-plot",
                            figure = fig2,
                        ),    
                    ],
                ),
                html.Div(
                    id = "bottom",
                     style={'width': '49%',
                           'float':'left', 
                           'display': 'inline-block'},
                    children=[
                        html.H4(
                            children = "条形变化图",
                            style = {
                            'font-family':'Microsoft JhengHei'
                                    },
                                ),
                        html.Video(
                            controls=True,
                            style = {
                              'Align':'center',  
                            },
                            height = "400",
                            width = "600",
                            id = "histrogram",
                            src = "/static/plot3.mp4",
                        ),    
                    ],
                ),
                html.Div(
                    id = "right-bottom",
                     style={'width': '49%',
                           'float':'right', 
                           'display': 'inline-block'},
                    children=[
                        dcc.Graph(
                            id = "bar-plot",
                            figure = fig4,
                        ),      
                    ],
                ),
            ],
        ),
    ],
)

server = app.server

@app.callback(
    Output("selected-data","figure"),
    [
      Input("chart-dropdown","value")  
    ],
)
def display_selected_data(chart_dropdown):
    if chart_dropdown == "教育投入占GDP比例":
        return fig1_1
    if chart_dropdown == "初等教育投入比例":
        return fig1_2
    if chart_dropdown == "中等教育投入比例":
        return fig1_3
    if chart_dropdown == "高等教育投入比例":
        return fig1_4

@server.route('/plot3.mp4')
def server_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir,"static"),path)


if __name__ == "__main__":
    app.run_server(debug=True,thread= True) # Turn off reloader if inside Jupyter


# In[ ]:




