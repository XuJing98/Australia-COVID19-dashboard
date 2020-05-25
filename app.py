import pandas as pd
from datetime import datetime, timedelta,date
import math
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_table
from dash_table.Format import Format
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


input_list = [
    Input('datatable-interact-location', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location', 'selected_row_ids'),
]

def scraping_data():
    """
    Scraping the data from Johns Hopkins CSSE

    """

    # get the date of yesterday and the day before yesterday and convert them to the m-d-Y format
    yesterday = (date.today() + timedelta(days = -1)).strftime("%m-%d-%Y")
    before_yesterday = (date.today() + timedelta(days = -2)).strftime("%m-%d-%Y")

    #the url of global daily reports provided by Johns Hopkins University
    address = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
    url1 = address + yesterday + ".csv"
    url2 = address + before_yesterday + ".csv"

    # load the csv data into pandas.DataFrame
    # and test whether yesterday data has been update yet
    try:
        p_td = pd.read_csv(url1)
    except:
        p_td = pd.read_csv(url2)
    # Only show the data about Australia
    # get the summary data for each state in Australia
    data_td = p_td[p_td['Country_Region'] == 'Australia']
    data_td = data_td.drop(["FIPS", "Admin2"], axis=1)
    data_td = data_td.reset_index(drop=True)
    data_td.drop(columns=['Combined_Key'], inplace=True)
    data_td['Population'] = [412576, 7544000, 211945, 5071000, 1677000, 515000, 6359000, 2589000]
    data_td = data_td.astype({'Last_Update': 'datetime64'})
    data_td['Death Rate'] = data_td['Deaths'] / data_td['Confirmed']
    data_td['Confirmed/100k'] = ((data_td['Confirmed'] / data_td['Population'])*100000).round()
    data_td.drop(columns = 'Population', inplace=True)
    data_td = data_td[['Province_State', 'Country_Region','Active', 'Confirmed', 'Recovered','Deaths','Death Rate', 'Confirmed/100k','Last_Update', 'Lat', 'Long_']]

    # url of the time series data of global confirmed cases
    url_hc= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    # url of the time series data of global death cases
    url_hd= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    # url of the time series data of global recovered cases
    url_hr= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    p_hc = pd.read_csv(url_hc)
    p_hd = pd.read_csv(url_hd)
    p_hr = pd.read_csv(url_hr)

    # Time series data of Australia Confrimed cases
    data_hc = p_hc[p_hc['Country/Region'] == 'Australia']
    data_hc = data_hc.reset_index(drop=True)
    data_hc  = data_hc.drop(columns = ['Country/Region', 'Lat', 'Long'])
    df0 = pd.DataFrame(data_hc.stack()[0], columns= ['Australian Capital Territory']).drop('Province/State')
    df1 = pd.DataFrame(data_hc.stack()[1], columns= ['NSW']).drop('Province/State')
    df2 = pd.DataFrame(data_hc.stack()[2], columns= ['Northern Territory']).drop('Province/State')
    df3 = pd.DataFrame(data_hc.stack()[3], columns= ['Queensland']).drop('Province/State')
    df4 = pd.DataFrame(data_hc.stack()[4], columns= ['South Australia']).drop('Province/State')
    df5 = pd.DataFrame(data_hc.stack()[5], columns= ['Tasmania']).drop('Province/State')
    df6 = pd.DataFrame(data_hc.stack()[6], columns= ['Victoria']).drop('Province/State')
    df7 = pd.DataFrame(data_hc.stack()[7], columns= ['Western Australia']).drop('Province/State')
    df_confirmed = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7], axis =1)
    list1 = []
    list2 = []
    for i in range(len(df_confirmed)):
        list1.append(df_confirmed.index[i])
        list2.append(df_confirmed.iloc[i].sum())
    df_confirmed = pd.DataFrame({'Date':list1, 'Total':list2})


    # Time series data of Australia Deaths
    data_hd = p_hd[p_hd['Country/Region'] == 'Australia']
    data_hd = data_hd.reset_index(drop=True)
    data_hd  = data_hd.drop(columns = ['Country/Region', 'Lat', 'Long'])
    df0 = pd.DataFrame(data_hd.stack()[0], columns= ['Australian Capital Territory']).drop('Province/State')
    df1 = pd.DataFrame(data_hd.stack()[1], columns= ['NSW']).drop('Province/State')
    df2 = pd.DataFrame(data_hd.stack()[2], columns= ['Northern Territory']).drop('Province/State')
    df3 = pd.DataFrame(data_hd.stack()[3], columns= ['Queensland']).drop('Province/State')
    df4 = pd.DataFrame(data_hd.stack()[4], columns= ['South Australia']).drop('Province/State')
    df5 = pd.DataFrame(data_hd.stack()[5], columns= ['Tasmania']).drop('Province/State')
    df6 = pd.DataFrame(data_hd.stack()[6], columns= ['Victoria']).drop('Province/State')
    df7 = pd.DataFrame(data_hd.stack()[7], columns= ['Western Australia']).drop('Province/State')
    df_death = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7], axis =1)
    list1 = []
    list2 = []
    for i in range(len(df_death)):
        list1.append(df_death.index[i])
        list2.append(df_death.iloc[i].sum())
    df_death = pd.DataFrame({'Date':list1, 'Total':list2})

    # Times series data of Australia recovered cases
    data_hr = p_hr[p_hr['Country/Region'] == 'Australia']
    data_hr = data_hr.reset_index(drop=True)
    data_hr  = data_hr.drop(columns = ['Country/Region', 'Lat', 'Long'])
    df0 = pd.DataFrame(data_hr.stack()[0], columns= ['Australian Capital Territory']).drop('Province/State')
    df1 = pd.DataFrame(data_hr.stack()[1], columns= ['NSW']).drop('Province/State')
    df2 = pd.DataFrame(data_hr.stack()[2], columns= ['Northern Territory']).drop('Province/State')
    df3 = pd.DataFrame(data_hr.stack()[3], columns= ['Queensland']).drop('Province/State')
    df4 = pd.DataFrame(data_hr.stack()[4], columns= ['South Australia']).drop('Province/State')
    df5 = pd.DataFrame(data_hr.stack()[5], columns= ['Tasmania']).drop('Province/State')
    df6 = pd.DataFrame(data_hr.stack()[6], columns= ['Victoria']).drop('Province/State')
    df7 = pd.DataFrame(data_hr.stack()[7], columns= ['Western Australia']).drop('Province/State')
    df_recovered = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7], axis =1)
    list1 = []
    list2 = []
    for i in range(len(df_recovered)):
        list1.append(df_recovered.index[i])
        list2.append(df_recovered.iloc[i].sum())
    df_recovered = pd.DataFrame({'Date':list1, 'Total':list2})

    return data_td, df_confirmed, df_death, df_recovered





"""

Load the data and assign them to the variables

"""

df_latest, df_confirmed, df_death, df_recovered = scraping_data()

df_latest = df_latest.astype({'Last_Update': 'datetime64'})
latestDate = datetime.strftime(df_latest['Last_Update'][0], '%b %d, %Y %H:%M GMT+10')
daysOutbreak = (df_latest['Last_Update'][0] - datetime.strptime('12/31/2019', '%m/%d/%Y')).days

countryTable = df_latest
countryTable = countryTable.sort_values(by=['Active', 'Confirmed'], ascending=False).reset_index(drop=True)
countryTable['id'] = countryTable['Province_State']
countryTable.set_index('id', inplace=True, drop=False)

# df_confirmed = pd.read_csv('./data/confirmed.csv')
ConfirmedCases = df_confirmed['Total'].values[-1]
PlusConfirmed = df_confirmed['Total'].values[-1] - df_confirmed['Total'].values[-2]
PlusConfirmed_per = PlusConfirmed / df_confirmed['Total'].values[-2]

# df_death = pd.read_csv('./data/death.csv')
DeathCases = df_death['Total'].values[-1]
PlusDeath = df_death['Total'].values[-1] - df_death['Total'].values[-2]
PlusDeath_per = PlusDeath / df_death['Total'].values[-2]

# df_recovered = pd.read_csv('./data/recovered.csv')
RecoveredCases = df_recovered['Total'].values[-1]
PlusRecovered = df_recovered['Total'].values[-1] - df_recovered['Total'].values[-2]
PlusRecovered_per = PlusRecovered / df_recovered['Total'].values[-2]

ActativeCases = ConfirmedCases - DeathCases - RecoveredCases

CountryTable = df_latest
CountryTable = CountryTable.sort_values(by=['Active', 'Confirmed'], ascending=False).reset_index(drop=True)
countryTable['id'] = countryTable['Province_State']
countryTable.set_index('id', inplace=True, drop=False)

AustraliaTable = CountryTable

active = df_confirmed['Total']-df_death['Total']-df_recovered['Total']
df_active = pd.DataFrame({'Date': df_confirmed['Date'].values, 'Total': active.values})

df_death['Date'] = df_death['Date']+'20'
df_confirmed['Date'] = df_confirmed['Date'] + '20'
df_recovered['Date'] = df_recovered['Date'] + '20'
df_active['Date'] = df_active['Date'] + '20'
df_death = df_death.astype({'Date': 'datetime64'})
df_confirmed = df_confirmed.astype({'Date': 'datetime64'})
df_recovered = df_recovered.astype({'Date': 'datetime64'})
df_active = df_active.astype({'Date': 'datetime64'})


# create pie chart of Australian State Infection Rate
fig_pie = px.pie(df_latest, values='Active', names='Province_State')

# Create empty figure canvas
fig_combine = go.Figure()
# Add trace to the figure

fig_combine.add_trace(go.Scatter(x=df_active['Date'], y=df_active['Total'],
                                 mode='lines+markers',
                                 line_shape='spline',
                                 name='Active',
                                 line=dict(color='#ffff00', width=2),
                                 marker=dict(size=2, color='#ffff00',
                                             line=dict(width=.5, color='#ffff00')),
                                 text=[datetime.strftime(
                                     d, '%b %d %Y GMT+10') for d in df_death['Date']],
                                 hovertext=['Total active<br>{:,d} cases<br>'.format(
                                     i) for i in df_active['Total']],
                                 hovertemplate='%{hovertext}' +
                                               '<extra></extra>'))
fig_combine.add_trace(go.Scatter(x=df_confirmed['Date'], y=df_confirmed['Total'],
                                 mode='lines+markers',
                                 line_shape='spline',
                                 name='Confirmed',
                                 line=dict(color='#ff0000', width=2),
                                 marker=dict(size=2, color='#ff0000',
                                             line=dict(width=.5, color='#ff0000')),
                                 text=[datetime.strftime(
                                     d, '%b %d %Y GMT+10') for d in df_confirmed['Date']],
                                 hovertext=['Total confirmed<br>{:,d} cases<br>'.format(
                                     i) for i in df_confirmed['Total']],
                                 hovertemplate='%{hovertext}' +
                                               '<extra></extra>'))
fig_combine.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Total'],
                                 mode='lines+markers',
                                 line_shape='spline',
                                 name='Recovered',
                                 line=dict(color='#168038', width=2),
                                 marker=dict(size=2, color='#168038',
                                             line=dict(width=.5, color='#168038')),
                                 text=[datetime.strftime(
                                     d, '%b %d %Y GMT+10') for d in df_recovered['Date']],
                                 hovertext=['Total recovered<br>{:,d} cases<br>'.format(
                                     i) for i in df_recovered['Total']],
                                 hovertemplate='%{hovertext}' +
                                               '<extra></extra>'))
fig_combine.add_trace(go.Scatter(x=df_death['Date'], y=df_death['Total'],
                                 mode='lines+markers',
                                 line_shape='spline',
                                 name='Death',
                                 line=dict(color='#000000', width=2),
                                 marker=dict(size=2, color='#000000',
                                             line=dict(width=.5, color='#000000')),
                                 text=[datetime.strftime(
                                     d, '%b %d %Y GMT+10') for d in df_death['Date']],
                                 hovertext=['Total death<br>{:,d} cases<br>'.format(
                                     i) for i in df_death['Total']],
                                 hovertemplate='%{hovertext}' +
                                               '<extra></extra>'))
# Customise layout
fig_combine.update_layout(
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis_type='linear',
    yaxis=dict(
        showline=False, linecolor='#272e3e',
        zeroline=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
    ),
    xaxis=dict(
        showline=False, linecolor='#272e3e',
        showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode='x unified',
    legend_orientation="h",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)



"""
The Framework of the Dash App
"""

external_stylesheets = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

app = dash.Dash(__name__,
                assets_folder='./assets/',
                external_stylesheets= [external_stylesheets]
      )

app.title = 'Australian COVID-19 Dashboard'

server = app.server

# This is to prevent app crash when loading since we have plot that only render when user clicks.
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div(
    style={'backgroundColor': '#fafbfd'},
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(
                    id='herder-title',
                    children=" Australian Coronavirus(COVID-19) Dashboard" ),
                html.P(
                    id="description",
                    children=dcc.Markdown(
                        children=
                        '''
                        This dashboard is developed to visualize and track the spread of recent outbreak coronavirus (COVID-19) in Australia.
                        Also, this website and its contents, including all data, mapping, and analysis, is provided to the public strictly 
                        for general information purposes only. All the data was collected from Johns Hopkins CSSE
                        (https://github.com/CSSEGISandData/COVID-19).  
                        ''',
                    )
                ),
                html.P(
                    className='time-stamp',
                    children="Last update: {}.".format(latestDate)
                ),
                html.Hr(style={'marginTop': '.5%'},
                        ),
            ]
        ),
        html.Div(
            className="number-plate",
            children=[
                html.Div(
                    className='number-plate-single',
                    style={'border-top': '#2674f6 solid .2rem',},
                    children=[
                        html.H3(style={'color': '#2674f6'},
                                children=[
                                    html.P(
                                        style={'color': '#ffffff',},
                                        children='xxxx xx xxx xxxx xxx xxxxx'
                                    ),
                                    '{}'.format(daysOutbreak),
                                ]
                                ),
                        html.H5(
                            style={'color': '#2674f6',},
                            children="days since outbreak"
                        )
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-active',
                    style={'border-top': '#e36209 solid .2rem',},
                    children=[
                        html.H3(
                            style={'color': '#e36209'},
                            children=[
                                html.P(
                                    style={'color': '#ffffff',},
                                    children='xxxx xx xxx xxxx xxx xxxxx'
                                ),
                                '{:,d}'.format(ActativeCases)
                            ]
                        ),
                        html.H5(
                            style={'color': '#e36209'},
                            children="Active Cases"
                        )
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-confirm',
                    style={'border-top': '#d7191c solid .2rem',},
                    children=[
                        html.H3(
                            style={'color': '#d7191c'},
                            children=[
                                html.P(
                                    children='+ {:,d} in the past 24h ({:.1%})'.format(PlusConfirmed, PlusConfirmed_per)
                                ),
                                '{:,d}'.format(ConfirmedCases)
                            ]
                        ),
                        html.H5(
                            style={'color': '#d7191c'},
                            children="Confirmed Cases"
                        )
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-recover',
                    style={'border-top': '#1a9622 solid .2rem',},
                    children=[
                        html.H3(
                            style={'color': '#1a9622'},
                            children=[
                                html.P(
                                    children='+ {:,d} in the past 24h ({:.1%})'.format(PlusRecovered, PlusRecovered_per)
                                ),
                                '{:,d}'.format(RecoveredCases),
                            ]
                        ),
                        html.H5(
                            style={'color': '#1a9622'},
                            children="Recovered Cases"
                        )
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-death',
                    style={'border-top': '#6c6c6c solid .2rem',},
                    children=[
                        html.H3(
                            style={'color': '#6c6c6c'},
                            children=[
                                html.P(
                                    children='+ {:,d} in the past 24h ({:.1%})'.format(PlusDeath, PlusDeath_per)
                                ),
                                '{:,d}'.format(DeathCases)
                            ]
                        ),
                        html.H5(
                            style={'color': '#6c6c6c'},
                            children="Death Cases"
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='row dcc-plot',
            children=[
                html.Div(
                    className='dcc-sub-plot',
                    children=[
                        html.H5(
                            children='Australian Cases Timeline'
                        ),
                        dcc.Graph(
                            style={'height': '400px'},
                            figure=fig_combine,
                            config={"displayModeBar": False, "scrollZoom": False},
                        ),
                    ]
                ),
                html.Div(
                    className='dcc-sub-plot',
                    children=[
                        html.H5(
                            children='Australian States Infection Rate'
                        ),
                        dcc.Graph(
                            style={'height': '400px'},
                            figure= fig_pie,
                            config={"displayModeBar": False, "scrollZoom": False},
                        )

                    ]
                )

            ]

        ),
        html.Div(
            className='table',
            children=[
                html.H5(
                    children='Latest Coronavirus Outbreak Map',
                    style = {'textAlign': 'center',
                             'fontWeight': 'bold'}
                ),
                dcc.Graph(
                    id='datatable-interact-map',
                    style={'height': '400px'},
                    config={"displayModeBar": False, "scrollZoom": True},
                ),
            ]
        ),
        html.Div(
            className='table',
            children=[
                html.H5(
                    id='dcc-table-header',
                    children='Australian COVID-19 Cases Summary',
                    style =  {'textAlign': 'center',
                              'fontWeight': 'bold'}
                ),

                dash_table.DataTable(
                    id='datatable-interact-location',
                    columns=[{"name": 'Province_State', "id": 'Province_State'}
                             if i == 'Province_State' else {"name": 'Country_Region', "id": 'Country_Region'}
                             for i in CountryTable.columns[0:1]] +
                            [{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                             if i == 'Death Rate' else {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                             for i in CountryTable.columns[1:]],
                    # But still store coordinates in the table for interactivity
                    data= CountryTable.to_dict("rows"),
                    row_selectable="single",
                    sort_action="native",
                    style_as_list_view=True,
                    style_cell={'font_family': 'Roboto',
                                'backgroundColor': '#ffffff',
                                },
                    fixed_rows={'headers': True, 'data': 0},
                    style_table={'minHeight': '400px',
                                 'height': '400px',
                                 'maxHeight': '400px',
                                 'overflowX': 'auto',
                                 },
                    style_header={'backgroundColor': '#ffffff',
                                  'fontWeight': 'bold'},
                    style_cell_conditional=[{'if': {'column_id': 'Province_State'}, 'width': '18%'},
                                            {'if': {'column_id': 'Country_Regions'}, 'width': '12%'},
                                            {'if': {'column_id': 'Active'}, 'width': '8%'},
                                            {'if': {'column_id': 'Confirmed'}, 'width': '8%'},
                                            {'if': {'column_id': 'Recovered'}, 'width': '8%'},
                                            {'if': {'column_id': 'Deaths'}, 'width': '8%'},
                                            {'if': {'column_id': 'Death rate'}, 'width': '12%'},
                                            {'if': {'column_id': 'Confirmed/100k'}, 'width': '12%'},
                                            {'if': {'column_id': 'Active'}, 'color':'#e36209'},
                                            {'if': {'column_id': 'Confirmed'}, 'color': '#d7191c'},
                                            {'if': {'column_id': 'Recovered'}, 'color': '#1a9622'},
                                            {'if': {'column_id': 'Deaths'}, 'color': '#6c6c6c'},
                                            {'textAlign': 'center'}
                                            ],
                ),

            ]
        ),
        html.Div(
            className='footer-container',
            id='my-footer',
            children=[
                html.Hr(),
                html.P(
                   style={'textAlign': 'center', 'margin': 'auto'},
                   children=[
                       html.A(
                           'UTS Project',
                           href='https://handbook.uts.edu.au/subjects/48001.html',
                           target='_blank'
                       ),
                       ' | ',
                       html.A(
                           'Project Owner: Chris Wong',
                           href='https://www.uts.edu.au/staff/chris.wong',
                           target='_blank'
                       ),
                       ' | ',
                       html.A(
                           'Developed by: Xu Jing',
                           href='https://github.com/XuJing98',
                           target='_blank'

                       ),
                       ' , ',
                       html.A(
                           'Zeyu Li',
                           href='https://github.com/lizeyujack',
                           target='_blank'
                       ),
                       ' , Peifeng Xing & Ziheng Wang | ',
                       html.A(
                            'About this dashboard',
                            href='https://github.com/XuJing98/Australia-COVID19-dashboard',
                            target='_blank'
                        ),
                   ]
                ),
            ]
        )


    ]

)



@app.callback(
    Output('datatable-interact-map', 'figure'),
    input_list
)
def update_figures(
        derived_virtual_selected_rows, selected_row_ids,
):



    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = AustraliaTable
    latitude = -25.931850 if len(derived_virtual_selected_rows) == 0 else dff.iloc[derived_virtual_selected_rows].Lat.values.item()
    longitude = 134.024931 if len(derived_virtual_selected_rows) == 0 else dff.iloc[derived_virtual_selected_rows].Long_.values.item()
    zoom = 3 if len(derived_virtual_selected_rows) == 0 else 5

    hovertext_value = [
        'Active: {:,d}<br>Confirmed: {:,d}<br>Recovered: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(
            h, i, j, k, t, q)
        for h, i, j, k, t, q in zip(
            df_latest['Active'],
            df_latest['Confirmed'], df_latest['Recovered'],
            df_latest['Deaths'], df_latest['Death Rate'],
            df_latest['Confirmed/100k']
        )
    ]

    mapbox_access_token = "pk.eyJ1IjoieHVqaW5nOTgiLCJhIjoiY2s5Z2ljdnViMG55djNmcDl6bXJhenhrNSJ9.88lfe_EfVWTMjzROPq9UIA"

    # Generate a list for hover text display
    textList = []
    for area, region in zip(df_latest['Province_State'], df_latest['Country_Region']):

        if type(area) is str:

            textList.append(area + ', ' + region)
        else:
            textList.append(region)

    # Generate a list for color gradient display
    colorList = []
    for comfirmed, recovered, deaths in zip(df_latest['Confirmed'], df_latest['Recovered'], df_latest['Deaths']):
        remaining = comfirmed - deaths - recovered
        colorList.append(remaining)

    fig2 = go.Figure(go.Scattermapbox(
        lat=df_latest['Lat'],
        lon=df_latest['Long_'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color=['#d7191c' if i > 0 else '#1a9622' for i in colorList],
            size=[i ** (1 / 3) for i in df_latest['Confirmed']],
            sizemin=1,
            sizemode='area',
            sizeref=2. * max([math.sqrt(i)
                              for i in df_latest['Confirmed']]) / (100. ** 2),
        ),
        text=textList,
        hovertext=hovertext_value,
        hovertemplate="<b>%{text}</b><br><br>" +
                      "%{hovertext}<br>" +
                      "<extra></extra>")
    )
    fig2.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        margin=go.layout.Margin(l=10, r=10, b=10, t=0, pad=40),
        hovermode='closest',
        transition={'duration': 500},
        annotations=[
            dict(x=.5,
                 y=-.0,
                 align='center',
                 showarrow=False,
                 text="Points are placed based on data geolocation levels.<br>Province/State level - Australia",
                 xref="paper",
                 yref="paper",
                 font=dict(size=10, color='#292929'),
                 )
        ],
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            style="light",
            # The direction you're facing, measured clockwise as an angle from true north on a compass
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=latitude,
                lon=longitude
            ),
            pitch=0,
            zoom=zoom
        )
    )

    return fig2


if __name__ == "__main__":
    app.run_server(debug=True)