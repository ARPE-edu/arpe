"""
Novel Algorithm for Resonator Parameter Extraction with Outlier Removal
by Patrick Krkotic, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O'Callaghan, 2020

Code written by Patrick Krkotic and Queralt Gallardo
patrickkrkotic@outlook.de

Developed on Python 3.7.7
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import flask
from flask import Flask, send_from_directory, send_file
import algorithm.QNoGUI as q_mh
import base64
import os
from urllib.parse import quote as urlquote
import uuid
import conf as conf
import dash_table
from dash.exceptions import PreventUpdate

"""  This part is for the File Upload """
UPLOAD_DIRECTORY = conf.dashapp["uploaddir"]
if not os.path.exists(UPLOAD_DIRECTORY):
   os.makedirs(UPLOAD_DIRECTORY)
# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
# app = dash.Dash(server=server)

"""  This is the Frontent Part  """
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__) # define flask app.server
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server) # call flask server

TDict = {}
TDictRefl = {}
amountoffiles = []


def serve_layout():
    session_id = str(uuid.uuid4())
    print(session_id)
    ### We are counting the amount of visitors on the page without tracking any information ###
    visitor = open(str(UPLOAD_DIRECTORY) + "/" + str(session_id) + ".txt", "wb")

    # the style arguments for the sidebar.
    SIDEBAR_STYLE = {
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '20%',
        'padding': '20px 10px',
        'background-color': '#f8f9fa'
    }

    # the style arguments for the main content page.
    CONTENT_STYLE = {
        'margin-left': '25%',
        'margin-right': '5%',
        'top': 0,
        'padding': '20px 10px'
    }

    TEXT_STYLE = {
        'textAlign': 'center',
        'color': '#191970'
    }

    CARD_TEXT_STYLE = {
        'textAlign': 'center',
        'color': '#0074D9'
    }

    content_fourth_row = dbc.Row(
        [
            dbc.Col(
                html.Div(
                    id='final-results'
                ), md=12,
            )
        ]
    )

    content_third_row = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='theq-chart'), md=12,
            )
        ]
    )

    content_second_row = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='refl-chart'), md=6
            ),
            dbc.Col(
                dcc.Graph(id='S21-chart'), md=6
            ),
        ]
    )

    content_first_row = dbc.Row([
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            # html.H4(id='card_title_1', children=['Abstract'], className='card-title',
                            #        style=CARD_TEXT_STYLE),
                            html.P(id='card_text_1', children=[
                                'The algorithm is based on Moore-Penrose pseudo-inverse routines for rapid and efficient numerical performance, which are used to fit the reflection and transmission responses. It is capable of extracting the unloaded quality factor and resonant frequency of microwave resonators from two-port S-parameters in any Touchstone format. The algorithm performs an adaptive outlier removal to discard measurement points affected by distortion caused by defects in the device or in the experimental setup. An extensive error analysis relating network analyzer capabilities with errors in the extracted parameters showed that errors below 1% in the unloaded quality factor are feasible with this algorithm. The source code is written in Python 3.7.7 using open source packages and can be downloaded using the download button for offline usage. For more information and a more detailed explanation of the algorithm we refer to the publication accesible over the DOI link. Please cite the publication if using this web application or the source code.'], ),
                        ]
                    )
                ]
            ),
            md=12
        ),
    ])

    content = html.Div(
        [
            html.H1(
                'Algorithm for Resonator Parameter Extraction from Symmetrical and Asymmetrical Transmission Responses',
                style=TEXT_STYLE),
            html.H4("by Patrick Krkotic, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O'Callaghan"),
            html.H5("Publication submitted to IEEE Transactions on Microwave Theory and Techniques"),
            # html.Div('your SessionID is: {}'.format(session_id)),
            html.Div(session_id, id='session-id', style={'display': 'none'}),
            html.Hr(),
            content_first_row,
            content_second_row,
            content_third_row,
            content_fourth_row,
            dcc.ConfirmDialog(
                id='confirm',
                message='The webpage is still being under development.', )
        ],
        style=CONTENT_STYLE
    )

    controls = dbc.FormGroup(
        [
            html.Br(),
            html.H3("Upload", style={'textAlign': 'center'}),
            # html.Div('Upload your data in .s2p Touchstone format.'),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Drag and drop or click to upload .s2p files."]
                ),
                style={
                    "width": "98%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    # "margin": "10px",
                },
                multiple=True,
            ),
            html.Div(id="numberoffiles"),
            html.Ul(id="Dictionary"),
            html.Div(id="code-finished"),
            html.Div(
                [
                    dbc.Button(
                        id='button-calculate',
                        n_clicks=0,
                        children='Calculate',
                        color='primary',
                        block=True
                    ),
                    dbc.Spinner(html.Div(id='loading'), color='primary'),
                ]),
            html.Br(),
            html.H3('List of Files', style={
                'textAlign': 'center'
            }),
            dcc.Dropdown(
                id='name-dropdown',
                options=[
                ],
                # value=['value1'],  # default value
                # multi=False
            ),
            # html.Br(),
            # html.P(id='',children=['Comment: The source code and results buttons will be available after the decision of the reviewers have been taken.']),
            html.Br(),
            html.H3('Source Code', style={
                'textAlign': 'center'
            }),
            html.Label(['The code can be downloaded from ', html.A('GitHub', href='https://github.com/ARPE-edu/arpe')]),
            html.Br(),
            html.Img(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Logo_UPC.svg/110px-Logo_UPC.svg.png",
                style={
                    'height': '25%',
                    'width': '25%',
                    'float': 'center',
                    'position': 'relative'
                    # 'textAlign':'center'
                },
            ),

            html.Img(
                src="https://www.cells.es/logo.png",
                style={
                    'height': '50%',
                    'width': '50%',
                    'float': 'center',
                    # 'textAlign':'right'
                    'position': 'relative'
                },
            ),
        ]
    )

    sidebar = html.Div(
        [
            html.H1('ARPE', style=TEXT_STYLE),
            html.Hr(),
            controls
        ],
        style=SIDEBAR_STYLE,
    )

    layout = html.Div([sidebar, content, dcc.Store(id='memory')])

    return layout


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)
app.title = 'ARPE'
app.config['suppress_callback_exceptions'] = True
app.layout = serve_layout



@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    print(path)
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


def uploaded_files(session_id):
    """List the files in the upload directory."""
    print("Showing uploaded Files")
    files = []
    if os.path.exists(os.path.join(UPLOAD_DIRECTORY, session_id)):
        for filename in os.listdir(os.path.join(UPLOAD_DIRECTORY, session_id)):
            if filename.endswith('.s2p') or filename.endswith('.S2P'):
                files.append(filename)
                print('These are the files' + str(files))
        ### We count the amount of files uploaded to be able to estimate the computing power needed ###
        filestats = open(str(UPLOAD_DIRECTORY) + "/" + str(session_id) + ".txt", "w")
        filestats.write(str(len(files)))
        filestats.close()
    return files


def file_download_link(filename, session_id):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}/{}".format(urlquote(session_id), urlquote(filename))
    return html.A(filename, href=location)

suppress_callback_exceptions=True
@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents"), Input("session-id", "children")],
)
def update_output(uploaded_filenames, uploaded_file_contents,session_id):
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            data = data.encode("utf8").split(b";base64,")[1]
            with open(os.path.join(UPLOAD_DIRECTORY, session_id, name), "wb") as fp:
                fp.write(base64.decodebytes(data))
    files=uploaded_files(session_id)
    print(files)
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        print("Si")
        return [html.Li(file_download_link(filename,session_id)) for filename in files]

# @app.callback(
#     Output("file-list", "children"),
#     [Input("upload-data", "filename"), Input("upload-data", "contents"), Input("session-id", "children")])
# def update_output(uploaded_filenames, uploaded_file_contents, session_id):
#     """Save uploaded files and regenerate the file list."""
#     if uploaded_filenames is not None and uploaded_file_contents is not None:
#         for name, data in zip(uploaded_filenames, uploaded_file_contents):
#             #print("Saving file")
#             data = data.encode("utf8").split(b";base64,")[1]
#             if not os.path.exists(os.path.join(UPLOAD_DIRECTORY, session_id)):
#                 os.mkdir(os.path.join(UPLOAD_DIRECTORY, session_id))
#             with open(os.path.join(UPLOAD_DIRECTORY, session_id, name), "wb") as fp:
#                 fp.write(base64.decodebytes(data))
#
#     files = uploaded_files(session_id)
#     print(files)
#     if len(files) == 0:
#         return [html.Li("No files yet!")]
#     else:
#         return [html.Div(filename) for filename in files]


@app.callback([Output('name-dropdown', 'options'), Output('numberoffiles', 'children')],
              [Input("upload-data", "filename"), Input("upload-data", "contents"), Input("session-id", "children")])
def parse_uploads(uploaded_filenames, uploaded_file_contents, session_id):

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            #print("Saving file")
            data = data.encode("utf8").split(b";base64,")[1]
            if not os.path.exists(os.path.join(UPLOAD_DIRECTORY, session_id)):
                os.mkdir(os.path.join(UPLOAD_DIRECTORY, session_id))
            with open(os.path.join(UPLOAD_DIRECTORY, session_id, name), "wb") as fp:
                fp.write(base64.decodebytes(data))

    files=uploaded_files(session_id)
    amountoffiles = 'Upload of {} file successfull'.format(len(files))
    if len(files) == 0:
        return [{'label': i, 'value': i } for i in files],''
    else:
        #print([{'label': i, 'value': i } for i in files])
        return [{'label': i, 'value': i } for i in files],amountoffiles


# @app.callback(Output("loading-output-2", "children"), [Input('button-calculate', 'n_clicks')])
# def input_triggers_nested(n_clicks):
#     time.sleep(1)
#     return n_clicks

@app.callback([dash.dependencies.Output('Dictionary', 'children'),dash.dependencies.Output('loading', 'children'),dash.dependencies.Output("final-results", "children")],
    [dash.dependencies.Input('button-calculate', 'n_clicks'),Input("session-id", "children")])

def update_output(click,session_id):
    print(click)
    codedone = ''
    DataToSave = None

    if isinstance(click, int):
        if click > 0:
            if os.path.exists(os.path.join(conf.dashapp["uploaddir"], session_id)):
                (ListofFiles, WCCFXList, PlotDataList, QUnloaded, DataToSave) = q_mh.TheQFuntion(
                    os.path.join(conf.dashapp["uploaddir"], session_id))
                print(ListofFiles)
                codedone = 'The calculations are finished'
                ### We count the amount of executions per visit ###
                executionstats = open(str(UPLOAD_DIRECTORY) + "/" + str(session_id) + ".txt", "a")
                executionstats.write('\t' + str(click))
                executionstats.close()

                for k in range(len(ListofFiles)):
                    TDict[ListofFiles[k]] = [WCCFXList[k], PlotDataList[k]]
                return TDict, codedone, html.Div(
                    [
                        dash_table.DataTable(
                            data=DataToSave.to_dict("rows"),
                            columns=[{"id": x, "name": x} for x in DataToSave.columns],
                            export_format="xlsx",
                        )
                    ]
                )
        else:
            return [None,None,None]


@app.callback(
    Output("theq-chart", "figure"),
    [Input("session-id", "children"),Input('Dictionary', 'children'),Input('name-dropdown', 'value'),]
)
def update_theq_chart(session_id,TDict,selector):
    """ This is the part where the Data is prepared and calculated for the chart """
    # filelocation = "C:/Users/Maddi/PycharmProjects/theq/data/devdata"
    # if not selector is None:
    #print("Dictionary")
    #print(TDict)
    if selector == None:
        raise PreventUpdate
    Entry = TDict[selector]
    #print("Entry")
    #print(Entry)
    # plotdata = []
    # for Entry in selector:
    #     plotdata.append(TDict[Entry])
    # print("plotdata[0]")
    # print(plotdata[0][1][1])
    # print("plotdata[1]")
    # print(plotdata[1])
    # RedFreq = Entry[0][0]
    # Qloaded = Entry[0][1]
    # RS21 = plotdata[0][1][0]
    # IS21 = plotdata[0][1][1]
    # WRS21 = plotdata[0][1][2]
    # WIS21 = plotdata[0][1][3]
    RS21 = Entry[1][0]
    IS21 = Entry[1][1]
    WRS21 = Entry[1][2]
    WIS21 = Entry[1][3]
    return {
        'data': [
            {
                'x': RS21,
                'y': IS21,
                'name': 'S21 input data',
                'mode': 'markers',
                'marker': {'size': 7, "color": 'green'},
                'color': 'firebrick'
            },
            {
                'x': WRS21,
                'y': WIS21,
                'name': 'S21 fit',
                'mode': 'line',
                'marker': {'size': 7, "color": 'red'},
            },
        ],
        'layout': {'title': 'Transmission Circle Fit',
                   'clickmode': 'event+select',
                   'xaxis': dict(
                       title='Re(S21)'
                   ),
                   'yaxis': dict(
                       scaleanchor="x",
                       scaleratio=1,
                       title='Im(S21)'
                   )
                   }
    }


@app.callback(
    Output("refl-chart", "figure"),
    [Input("session-id", "children"),Input('Dictionary', 'children'),Input('name-dropdown', 'value'),]
)
def update_theq_reflchart(session_id,TDictRef,selector):
    """ This is the part where the Data is prepared and calculated for the chart """
    # filelocation = "C:/Users/Maddi/PycharmProjects/theq/data/devdata"
    # if not selector is None:
    #print("Dictionary")
    #print(TDict)
    if selector == None:
        raise PreventUpdate
    Entry = TDictRef[selector]
    # print("Entry")
    #print(Entry)
    # plotdata = []
    # for Entry in selector:
    #     plotdata.append(TDict[Entry])
    # print("plotdata[0]")
    # print(plotdata[0][1][1])
    # print("plotdata[1]")
    # print(plotdata[1])
    # RedFreq = Entry[0][0]
    # Qloaded = Entry[0][1]
    # RS21 = plotdata[0][1][0]
    # IS21 = plotdata[0][1][1]
    # WRS21 = plotdata[0][1][2]
    # WIS21 = plotdata[0][1][3]
    RS11 = Entry[1][4]
    IS11 = Entry[1][5]
    WRS11 = Entry[1][6]
    WIS11 = Entry[1][7]
    WRS11c = Entry[1][8]
    WIS11c = Entry[1][9]
    RS22 = Entry[1][10]
    IS22 = Entry[1][11]
    WRS22 = Entry[1][12]
    WIS22 = Entry[1][13]
    WRS22c = Entry[1][14]
    WIS22c = Entry[1][15]
    return {
        'data': [
            {
                'x': RS11,
                'y': IS11,
                'name': 'S11 input data',
                'mode': 'markers',
                'marker': {'size': 7, "color": 'green'},
                'color': 'firebrick'
            },
            {
                'x': WRS11,
                'y': WIS11,
                'name': 'S11 fit',
                'mode': 'line',
                'marker': {'size': 7, "color": 'red'},
            },
            {
                'x': WRS11c,
                'y': WIS11c,
                'name': 'S11 fit center',
                'mode': 'markers',
                'marker': {'size': 7, "color": 'blue'},
            },
            {
                'x': RS22,
                'y': IS22,
                'name': 'S22 input data',
                'mode': 'markers',
                'marker': {'size': 7, "color": 'green'},
                'color': 'firebrick'
            },
            {
                'x': WRS22,
                'y': WIS22,
                'name': 'S22 fit',
                'mode': 'line',
                'marker': {'size': 7, "color": 'red'},
            },
            {
                'x': WRS22c,
                'y': WIS22c,
                'name': 'S22 fit center',
                'mode': 'markers',
                'marker': {'size': 7, "color": 'blue'},
            },
        ],
        'layout': {'title': 'Reflection Circle Fit',
                   'clickmode': 'event+select',
                   'xaxis': dict(
                       title='Re(S)'
                   ),
                   'yaxis': dict(
                       scaleanchor="x",
                       scaleratio=1,
                       title='Im(S)'
                   )
                   }
    }


@app.callback(
    Output("S21-chart", "figure"),
    [Input("session-id", "children"),Input('Dictionary', 'children'),Input('name-dropdown', 'value'),]
)
def update_theq_chart(session_id,TDicttran,selector):
    """ This is the part where the Data is prepared and calculated for the chart """
    # filelocation = "C:/Users/Maddi/PycharmProjects/theq/data/devdata"
    # if not selector is None:
    #print("Dictionary")
    #print(TDict)
    if selector == None:
        raise PreventUpdate
    Entry = TDicttran[selector]
    #print("Entry")
    #print(Entry)
    # plotdata = []
    # for Entry in selector:
    #     plotdata.append(TDict[Entry])
    # print("plotdata[0]")
    # print(plotdata[0][1][1])
    # print("plotdata[1]")
    # print(plotdata[1])
    # RedFreq = Entry[0][0]
    # Qloaded = Entry[0][1]
    # RS21 = plotdata[0][1][0]
    # IS21 = plotdata[0][1][1]
    # WRS21 = plotdata[0][1][2]
    # WIS21 = plotdata[0][1][3]
    ftr = Entry[1][16]
    RS11tr = Entry[1][17]
    IS22tr = Entry[1][18]
    WRS21tr = Entry[1][19]
    return {
        'data': [
            {
                'x': ftr,
                'y': RS11tr,
                'name': 'S11 input data',
                'mode': 'line',
                'marker': {'size': 7, "color": 'blue'},
                'yaxis': 'y2',
                'color': 'firebrick'
            },
            {
                'x': ftr,
                'y': IS22tr,
                'name': 'S22 input data',
                'mode': 'line',
                'yaxis': 'y2',
                'marker': {'size': 7, "color": 'green'},
            },
            {
                'x': ftr,
                'y': WRS21tr,
                'name': 'S21 input data',
                'mode': 'line',
                'marker': {'size': 7, "color": 'red'},
            },
        ],
        'layout': {
            'title': 'S-Parameter',
            'clickmode': 'event+select',
            'xaxis': dict(
                title='Frequency [Hz]'
            ),
            'yaxis': dict(
                title=' Transmission [dB]'
            ),
            'yaxis2': dict(
                title='Reflection [dB]',
                overlaying='y',
                side='right'
            )
        }
    }

# @app.callback(Output('confirm', 'displayed'),
#               [Input("session-id", "children")])
# def display_confirm(value):
#     return True

""" Run it """
if __name__ == '__main__':
    ####### global environment
    app.run_server(port=8050,debug=False,host='0.0.0.0')
    ####### local environment
    #app.run_server(port=8050, debug=False)