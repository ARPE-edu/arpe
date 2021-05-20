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
from flask import Flask, send_from_directory
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

"""  This is the Frontent Part  """
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__) # define flask app.server
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server) # call flask server

amountoffiles = []


def serve_layout():
    session_id = str(uuid.uuid4())
    print(session_id)

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
                            html.P(id='card_text_1', children=[
                                'The algorithm is based on Moore-Penrose pseudo-inverse routines for rapid and '
                                'efficient numerical performance, which are used to fit the reflection and transmission'
                                ' responses. It is capable of extracting the unloaded quality factor and resonant '
                                'frequency of microwave resonators from two-port S-parameters in any Touchstone format.'
                                ' The algorithm performs an adaptive outlier removal to discard measurement points '
                                'affected by distortion caused by defects in the device or in the experimental setup. '
                                'An extensive error analysis relating network analyzer capabilities with errors in the '
                                'extracted parameters showed that errors below 1% in the unloaded quality factor are '
                                'feasible with this algorithm. The source code is written in Python 3.7.7 using open '
                                'source packages and can be downloaded using the download button for offline usage. '
                                'For more information and a more detailed explanation of the algorithm we refer to the '
                                'publication accesible over the DOI link. Please cite the publication if using this '
                                'web application or the source code.'], ),
                        ]
                    )
                ]
            ),
            md=12
        ),
    ])

    content = html.Div(
        [
            html.H1('Algorithm for Resonator Parameter Extraction with Outlier Removal', className="text"),
            html.H4(
                "by Patrick Krkoti" + u"\u0107" + ", Queralt Gallardo, Nikki Tagdulang, "
                                                  "Montse Pont and Joan M. O'Callaghan"),
            html.H5("Publication submitted to IEEE Transactions on Microwave Theory and Techniques"),
            # html.Div('your SessionID is: {}'.format(session_id)),
            html.Div(session_id, id='session-id', style={'display': 'none'}),
            html.Hr(),
            content_first_row,
            content_second_row,
            content_third_row,
            content_fourth_row
        ],
        className="content"
    )

    controls = dbc.FormGroup(
        [
            html.Br(),
            html.H3("Upload", style={'textAlign': 'center'}),
            html.Div('We recommend the uploaded data to include only one single maximum in the magnitude of S21.'),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Drag and drop or click to upload .s2p files."]
                ),
                className="upload",
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
                searchable=True,
                placeholder='Select your results',  # default value
                multi=False
            ),
            dbc.Button(
                id='',
                n_clicks=0,
                children='Download Results',
                color='primary',
                block=True
            ),
            html.Br(),
            html.P(id='', children=[
                'Comment: The source code and results buttons will be available after the decision of the reviewers have been taken.']),
            html.Br(),
            html.H3('Source Code', style={
                'textAlign': 'center'
            }),
            dbc.Button(
                id='',
                n_clicks=0,
                children='Download Source Code',
                color='primary',
                block=True
            ),
            html.Br(),
            html.Img(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Logo_UPC.svg/110px-Logo_UPC.svg.png",
                className='upc-logo',
            ),

            html.Img(
                src="https://www.cells.es/logo.png",
                className='alba-logo',
            ),
        ]
    )

    sidebar = html.Div(
        [
            html.H1('ARPE', className="text"),
            html.Hr(),
            controls
        ],
        className="sidebar",
    )

    stores = html.Div([
        dcc.Store(id='tdict', storage_type='session'),
        dcc.Store(id='stats', storage_type='memory')
    ])

    layout = html.Div([sidebar, content, stores])

    return layout


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/styles.css'], server=server)
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
            path = os.path.join(UPLOAD_DIRECTORY, session_id, filename)
            if os.path.isfile(path):
                files.append(filename)
                print(filename)
    return files


def file_download_link(filename, session_id):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}/{}".format(urlquote(session_id), urlquote(filename))
    return html.A(filename, href=location)


suppress_callback_exceptions = True


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents"), Input("session-id", "children")],
)
def update_output(uploaded_filenames, uploaded_file_contents, session_id):
    print('calling update_output')
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            data = data.encode("utf8").split(b";base64,")[1]
            with open(os.path.join(UPLOAD_DIRECTORY, session_id, name), "wb") as fp:
                fp.write(base64.decodebytes(data))
    files = uploaded_files(session_id)
    print(files)
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        print("Si")
        return [html.Li(file_download_link(filename, session_id)) for filename in files]


@app.callback([Output('name-dropdown', 'options'), Output('numberoffiles', 'children')],
              [Input("upload-data", "filename"), Input("upload-data", "contents"), Input("session-id", "children")])
def parse_uploads(uploaded_filenames, uploaded_file_contents, session_id):
    print('calling update_output')

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            # print("Saving file")
            data = data.encode("utf8").split(b";base64,")[1]
            if not os.path.exists(os.path.join(UPLOAD_DIRECTORY, session_id)):
                os.mkdir(os.path.join(UPLOAD_DIRECTORY, session_id))
            with open(os.path.join(UPLOAD_DIRECTORY, session_id, name), "wb") as fp:
                fp.write(base64.decodebytes(data))

    files = uploaded_files(session_id)

    amount_of_files = 'Upload of {} file successful'.format(len(files))
    if len(files) == 0:
        return [{'label': i, 'value': i} for i in files], ''
    else:
        # print([{'label': i, 'value': i } for i in files])
        return [{'label': i, 'value': i} for i in files], amount_of_files


@app.callback([Output('tdict', 'data'), Output('loading', 'children'),
               Output("final-results", "children")],
              [Input('button-calculate', 'n_clicks'), Input("session-id", "children"), Input('tdict', 'data')])
def update_output(click, session_id, tdict):
    print(click)
    tdict = tdict or {}
    if isinstance(click, int):
        if click > 0:
            if os.path.exists(os.path.join(conf.dashapp["uploaddir"], session_id)):
                (ListofFiles, WCCFXList, PlotDataList, QUnloaded, DataToSave) = q_mh.TheQFuntion(
                    os.path.join(conf.dashapp["uploaddir"], session_id))

                code_done = 'The calculations are finished'
                f = open("TheQ-Results", "w")
                f.write(str(DataToSave))
                f.close()

                print("Data Saved")
                for k in range(len(ListofFiles)):
                    tdict[ListofFiles[k]] = [WCCFXList[k], PlotDataList[k]]
                return tdict, code_done, html.Div(
                    [
                        dash_table.DataTable(
                            data=DataToSave.to_dict("rows"),
                            columns=[{"id": x, "name": x} for x in DataToSave.columns],
                            export_format="xlsx",
                        )
                    ]
                )
        else:
            return [None, None, None]


@app.callback(
    Output("theq-chart", "figure"),
    [Input('tdict', 'data'), Input('name-dropdown', 'value'), ]
)
def update_theq_chart(t_dict, selector):
    """ This is the part where the Data is prepared and calculated for the chart """

    if selector == None:
        raise PreventUpdate
    Entry = t_dict[selector]

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
        'layout': {
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
    [Input('tdict', 'data'), Input('name-dropdown', 'value'), ]
)
def update_theq_reflchart(t_dict_ref, selector):
    """ This is the part where the Data is prepared and calculated for the chart """

    if selector == None:
        raise PreventUpdate
    Entry = t_dict_ref[selector]

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
        'layout': {
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
    [Input('tdict', 'data'), Input('name-dropdown', 'value'), ]
)
def update_theq_chart(t_dict_tran, selector):
    """ This is the part where the Data is prepared and calculated for the chart """

    if selector == None:
        raise PreventUpdate
    Entry = t_dict_tran[selector]

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
                'color': 'firebrick'
            },
            {
                'x': ftr,
                'y': IS22tr,
                'name': 'S22 input data',
                'mode': 'line',
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
            'clickmode': 'event+select',
            'xaxis': dict(
                title='frequency [Hz]'
            ),
            'yaxis': dict(
                title='S-Paramter [dB]'
            )
        }
    }


""" Run it """
if __name__ == '__main__':
    ####### global environment
    app.run_server(port=8050,debug=False,host='0.0.0.0')
    ####### local environment
    #app.run_server(port=8050, debug=False)