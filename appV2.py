"""
Algorithm for Resonator Parameter Extraction from
Symmetrical and Asymmetrical Transmission Responses

Authors:
    Patrick Krkotic
    Queralt Gallardo
    Nikki Tagdulang
    Montse Pont
    Joan M. O'Callaghan

Contributors:
    Agustin Gomez Mansilla
    Martin Herold
    Tamas Madarasz

Contact:
    arpe-edu@outlook.de

Original Publication:
    2021

Version History:
    v1.0.0  – Initial release (Python 3.7.7) - 2021
    v2.0.0  – New interface and updated to Python 3.11.9 - 2023
    v2.1.0  – Novel routine for over and undercoupling, refactoring and clean-up, and update to Python 3.12.10 - 2026

Citation:
    Please cite the original 2021 publication when using this code.    
"""


import dash
from dash import dcc
from dash import html
from dash import State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import flask
from flask import Flask, send_from_directory, send_file
import algorithm.TheQ_multicore as q_mh
import base64
import os
from urllib.parse import quote as urlquote
import uuid
import conf as conf
from dash import dash_table
from dash.exceptions import PreventUpdate

"""  This part is for the File Upload """
UPLOAD_DIRECTORY = conf.dashapp["uploaddir"]
if not os.path.exists(UPLOAD_DIRECTORY):
   os.makedirs(UPLOAD_DIRECTORY)
server = Flask(__name__)


"""  This is the Frontent Part  """


server = flask.Flask(__name__) # define flask app.server

def serve_layout():
    session_id = str(uuid.uuid4())
    print(session_id)

    ### We are counting the amount of visitors of the webpage by counting the amount of session IDs
    ### created per day without tracking any information

    visitor = open(str(UPLOAD_DIRECTORY) + "/" + str(session_id) + ".txt", "wb")

    # the style arguments for the sidebar.
    SIDEBAR_STYLE = {
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '20%',
        'padding': '20px 10px',
        # 'background-color': '#f8f9fa'
        'background-color': '#293e6b'
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
        'color': '#293e6b'
        # 'color':'#ffffff'
    }

    TEXT_STYLE2 = {
        'textAlign': 'center',
        # 'color': '#191970'
        'color':'#ffffff'
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
                dcc.Graph(id='theq-chart',
                          config = {
                                'displayModeBar': True,  # Show the mode bar
                                # 'modeBarButtonsToRemove': ['toImage'],  # Remove the 'Download' button from the toolbar
                                'scrollZoom': True,  # Enable zooming with scroll
                                'displaylogo': False,  # Hide the Plotly logo
                                'toImageButtonOptions': {
                                    'format': 'svg', 
                                    'filename': 'ARPE_Transmission',
                                    'height': 500,
                                    'width': 700,
                                    'scale': 1
                                }
                          }
                          ), md=12,
            )
        ]
    )

    content_second_row = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='refl-chart',
                          config = {
                                'displayModeBar': True,  # Show the mode bar
                                # 'modeBarButtonsToRemove': ['toImage'],  # Remove the 'Download' button from the toolbar
                                'scrollZoom': True,  # Enable zooming with scroll
                                'displaylogo': False,  # Hide the Plotly logo
                                'toImageButtonOptions': {
                                    'format': 'svg', 
                                    'filename': 'ARPE_Reflection',
                                    'height': 500,
                                    'width': 700,
                                    'scale': 1
                                }
                          }
                          ), md=6
            ),
            dbc.Col(
                dcc.Graph(id='S21-chart',
                          config = {
                                'displayModeBar': True,  # Show the mode bar
                                # 'modeBarButtonsToRemove': ['toImage'],  # Remove the 'Download' button from the toolbar
                                'scrollZoom': True,  # Enable zooming with scroll
                                'displaylogo': False,  # Hide the Plotly logo
                                'toImageButtonOptions': {
                                    'format': 'svg', 
                                    'filename': 'ARPE_SParameter',
                                    'height': 500,
                                    'width': 700,
                                    'scale': 1
                                }
                          }
                          ), md=6
            ),
        ]
    )

    content_first_row = dbc.Row([
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [  html.H5("Abstract"),
                            html.P(id='card_text_1', children=[
                                'We describe an algorithm capable of extracting the unloaded quality factor '
                                'and the resonant frequency of microwave resonators from vector S-parameters. Both '
                                'symmetrical (Lorentzian) and asymmetrical (Fano) transmission responses are supported. '
                                'The algorithm performs an adaptive outlier removal to discard measurement points '
                                'affected by noise or distortion. It removes the effects caused by imperfections in '
                                'the device (such as modes with close resonance frequencies or stray coupling between '
                                'the resonator ports) or the experimental setup (such as lack of isolation or '
                                'dispersion in the test-set and cables). We present an extensive assessment of the '
                                'algorithm performance based on a numerical perturbation analysis and on the evaluation '
                                'of S-parameter fitting results obtained from network analyzer measurements and '
                                'resonator equivalent circuits. Our results suggest that uncertainty is mainly caused '
                                'by factors that distort the frequency dependence of the S-parameters, such as cabling '
                                'and coupling networks and is highly dependent on the device measured. Our perturbation '
                                'analysis shows improved results with respect to those of previous publications. Our '
                                'source code is written in Python using open source packages and is publicly available '
                                'under a freeware license.'
                           ], ),
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
            html.H5(["Published in: IEEE Transactions on Microwave Theory and Techniques (Volume: 69, Issue: 8, August 2021)  DOI:",html.A('10.1109/TMTT.2021.3081730', href='https://doi.org/10.1109/TMTT.2021.3081730')]),
            html.H5(["Manuscript available at ",html.A('UPCCommons', href='https://upcommons.upc.edu/urlFiles?idDrac=31808583')]),
            html.Div(session_id, id='session-id', style={'display': 'none'}),
            html.Hr(),
            content_first_row,
            content_second_row,
            content_third_row,
            content_fourth_row,
            dcc.ConfirmDialog(
                id='confirm',
                message='Some files could not be processed!', )
        ],
        style=CONTENT_STYLE
    )

    controls = dbc.Form(
        [
            html.Br(),
            html.H3("Upload", style={'textAlign': 'center','color':'#ffffff'}),
            # html.Div('Upload your data in .s2p Touchstone format.'),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    [
                        "Drag and Drop or Select .s2p Files", 
                        html.Img(
                            src='assets/upload.png', style={'height':'20px', 'marginLeft':'10px'}
                        )
                        ]
                ),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    'color':'#ffffff'
                    # 'background': 'linear-gradient(45deg, #ffcccb 5%, transparent 5%, transparent 95%, #ffcccb 95%, #ffcccb 100%, transparent 100%, transparent)'
                    # 'padding' : '20px'
                },
                multiple=True,
            ),
            dcc.Store(id='total-uploaded', data =0),
            dcc.Store(id='uploaded-filenames', data=[]),  # Store for already uploaded filenames
            html.Div([
                html.Div(id='numberoffiles', style={'color': 'white'}),  # For the number of files uploaded
                html.Div(id='errorfile', style={'color': 'red'}),  # For error messages
                html.Div(id='duplicatefile', style={'color': 'lightblue'})  # For duplicate messages
            ]),
            html.Ul(id="Dictionary"),
            html.Div(id="code-finished"),
            html.Div(
                [
                    dbc.Button(
                        id='button-calculate',
                        n_clicks=0,
                        children='Calculate',
                        color='primary',
                        #class_name = "w-100"
                    ),
                    dbc.Spinner(html.Div(id='loading'), color='primary', show_initially=False),
                ]),
            html.Br(),
            html.H3('File to Plot', style={
                'textAlign': 'center', 'color':'#ffffff'
            }),
            dcc.Dropdown(
                id='name-dropdown',
                options=[
                ],
            ),
            html.Br(),
            html.H3('Source Code', style={
                'textAlign': 'center','color':'#ffffff'
            }),
            html.Label(['The source code is available in the Git repository: ', html.A('ARPE-edu', href='https://github.com/ARPE-edu/arpe')],style={'color':'#ffffff'}),
            html.Br(),
            html.Img(
                src="/assets/CommSense.png",
                style={
                    'height': '20%',
                    'width': '20%',
                    'float': 'center',
                    'position': 'relative',
                    'margin-right': '20px',
                    'margin-left': '60px',
                    'margin-top': '230px'
                },
            ),

            html.Img(
                src="/assets/ALBA.svg",
                style={
                    'height': '30%',
                    'width': '30%',
                    'float': 'center',
                    'position': 'relative',
                    # 'backgroundColor': '#293e6b',
                    'margin-left': '40px',
                    'margin-top': '230px'
                },
            ),

            html.Img(
                src="/assets/UPC.png",
                style={
                    'height': '80%',
                    'width': '80%',
                    'float': 'center',
                    'position': 'relative',
                    'margin-left': '30px',
                    'margin-top': '20px'
                },
            ),

        ]
    )

    sidebar = html.Div(
        [
            html.H1('ARPE', style=TEXT_STYLE2),
            html.Hr(style={'backgroundColor': '#ffffff', 'height': '2px', 'border': 'none'}),
            controls
        ],
        style=SIDEBAR_STYLE,
    )

    stores = html.Div([
        dcc.Store(id='tdict', storage_type='session'),
        dcc.Store(id='Corrupt', storage_type='session'),
    ])

    layout = html.Div([sidebar, content, stores])

    return layout


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)
app.title = 'ARPE'
app.config['suppress_callback_exceptions'] = True
app.layout = serve_layout
app._favicon = ("favicon.png")


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
        ### We count the amount of files uploaded to be able to estimate the computing power needed ###
        filestats = open(str(UPLOAD_DIRECTORY) + "/" + str(session_id) + ".txt", "w")
        filestats.write(str(len(files)))
        filestats.close()
    return files


def file_download_link(filename, session_id):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}/{}".format(urlquote(session_id), urlquote(filename))
    return html.A(filename, href=location)


suppress_callback_exceptions = True


@app.callback(
    [Output("file-list", "children")],
    [Input("upload-data", "filename"), Input("upload-data", "contents"), Input("session-id", "children")],
)
def update_output(uploaded_filenames, uploaded_file_contents, session_id):
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            data = data.encode("utf8").split(b";base64,")[1]
            with open(os.path.join(UPLOAD_DIRECTORY, session_id, name), "wb") as fp:
                fp.write(base64.decodebytes(data))

    files = uploaded_files(session_id)
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename, session_id)) for filename in files]

@app.callback(
    Output('numberoffiles', 'children'),
    Output('errorfile', 'children'),
    Output('duplicatefile', 'children'),  # Output for duplicates
    Output('total-uploaded', 'data'),  # Output for the updated total count
    Output('uploaded-filenames', 'data'),  # Output for the list of uploaded filenames
    Input("upload-data", "filename"),
    Input("upload-data", "contents"),
    Input('total-uploaded', 'data'),  # Input for the current total count
    Input('uploaded-filenames', 'data'),  # Input for already uploaded filenames
    State("session-id", "children")  # Assuming this is part of your layout
)
def handle_uploads(uploaded_filenames, uploaded_file_contents, current_total, uploaded_filenames_list, session_id):
    # Initialize output variables
    if uploaded_filenames is None or uploaded_file_contents is None:
        return "No files uploaded.", "", "", current_total, uploaded_filenames_list  # No files uploaded case

    # Create a directory for session uploads if it doesn't exist
    session_dir = os.path.join(UPLOAD_DIRECTORY, session_id)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)  # Use makedirs to create intermediate directories

    total_files = len(uploaded_filenames)
    invalid_filenames = []  # List to store invalid filenames
    new_uploads = []  # List to track newly uploaded valid filenames
    duplicate_filenames = []  # List for duplicates
    unique_uploaded_filenames = set(uploaded_filenames_list)  # Convert to set for faster lookup

    # Iterate through uploaded files
    for name, content in zip(uploaded_filenames, uploaded_file_contents):
        # Decode the base64 content
        data = content.encode("utf8").split(b";base64,")[1]
        if name.endswith('.s2p') or name.endswith('.S2P'):
            if name not in unique_uploaded_filenames:  # Check for duplicates
                # Write the valid file to the session directory
                with open(os.path.join(session_dir, name), "wb") as fp:
                    fp.write(base64.decodebytes(data))
                new_uploads.append(name)  # Add valid file to the list of new uploads
                unique_uploaded_filenames.add(name)  # Add to the set of uploaded filenames
            else:
                duplicate_filenames.append(name)  # File is a duplicate
        else:
            invalid_filenames.append(name)  # Collect invalid filenames

    # Prepare output messages
    successful_uploads = len(new_uploads)
    total_successful_uploads = current_total + successful_uploads  # Update total count
    amount_of_files = f"{total_successful_uploads} out of {total_files - len(duplicate_filenames) + current_total} files uploaded successfully!" if total_files > 0 else "No files uploaded."
    
    # Format error message for duplicates if there are any
    duplicate_message = ""
    if duplicate_filenames:
        duplicate_files_string = ", ".join(duplicate_filenames)
        if len(duplicate_filenames) == 1:
            duplicate_message = f"{duplicate_files_string} already exists."
        else:
            duplicate_message = f"{duplicate_files_string} already exist."

    # Format error message if there are any invalid filenames
    if invalid_filenames:
        invalid_files_string = ", ".join(invalid_filenames)
        if len(invalid_filenames) == 1:
            error_message = f"{invalid_files_string} is not a .s2p file."
        else:
            error_message = f"{invalid_files_string} are not .s2p files."
    else:
        error_message = ""

    return amount_of_files, error_message, duplicate_message, total_successful_uploads, list(unique_uploaded_filenames)  # Return the updated total count and list of uploaded files


@app.callback(
        [
            Output('tdict', 'data'), 
            Output('loading', 'children'), 
            Output("final-results", "children"), 
            Output('Corrupt', 'data'),
            Output('name-dropdown', 'options')
        ],
        [
            Input('button-calculate', 'n_clicks'), 
            Input("session-id", "children"), 
            Input('tdict', 'data')
        ],
        prevent_initial_call=True
)
def update_output(click,session_id, tdict):
    codedone = ''
    DataToSave = None
    tdict = tdict or {}
    ListofFiles = None or []

    print("Calculate clicked:", click)


    if isinstance(click, int):
        print("Inside click is int")
        if click > 0:
            if os.path.exists(os.path.join(conf.dashapp["uploaddir"], session_id)):
                (ListofFiles, WCCFXList, PlotDataList, QUnloaded, DataToSave, Corrupt) = q_mh.TheQFunction(
                    os.path.join(conf.dashapp["uploaddir"], session_id))
                codedone = html.Div('The calculations are finished',style={'color': 'white'})


                rounding_specs = {
                    'Resonant Frequency [Hz]': 0,  # Replace 'column2' with your actual column name and desired decimals
                    'Loaded Quality Factor': 2,
                    'Coupling Factor S11': 5,
                    'Coupling Factor S22': 5,
                    'Unloaded Quality Factor': 2,
                    'Percentage of Data Removed': 2,  # Add more columns as needed
                }
                
                DataToExport = DataToSave

                # Apply rounding to each specified column
                for column, decimals in rounding_specs.items():
                    if column in DataToSave.columns:  # Ensure the column exists
                        DataToSave[column] = DataToSave[column].round(decimals)

                # DataToSave = DataToSave.round(2)

                ### We count the amount of executions per visit without tracking information ###
                executionstats = open(str(UPLOAD_DIRECTORY) + "/" + str(session_id) + ".txt", "a")
                executionstats.write('\t' + str(click))
                executionstats.close()

                for k in range(len(ListofFiles)):
                    tdict[ListofFiles[k]] = [WCCFXList[k], PlotDataList[k]]

                return tdict, codedone, html.Div(
                    [
                        dash_table.DataTable(
                            data=DataToSave.to_dict("records"),
                            columns=[{"id": x, "name": x} for x in DataToSave.columns],
                            export_format="xlsx",
                            style_header={
                            # 'backgroundColor': '#293e6b',
                            'fontWeight': 'bold',
                            # 'color': 'white'
                            },
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': 'Filenames'},  # Use 'column_id' instead of 'id'
                                    'textAlign': 'left'
                                }
                            ],
                            style_cell={'textAlign': 'right'},  # Default alignment for other cells
                            # style_as_list_view=True,
                        )
                    ]
                ), Corrupt, [{'label': i, 'value': i} for i in ListofFiles]
            else:
                return [None, None, None, None, [{'label': i, 'value': i} for i in ListofFiles]]
        else:
            print("Click is zero or negative")
            return [None, None, None, None, [{'label': i, 'value': i} for i in ListofFiles]]
    else:
        return [None, None, None, None, [{'label': i, 'value': i} for i in ListofFiles]]


@app.callback(
    Output("theq-chart", "figure"),
    [Input("session-id", "children"), Input('tdict', 'data'), Input('name-dropdown', 'value'), ]
)
def update_theq_chart(session_id, TDict, selector):
    """ This is the part where the Data is prepared and calculated for the chart """
    if selector == None:
        raise PreventUpdate
    Entry = TDict[selector]
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
                'marker': {'size': 10, 
                    "color": '1f77b4',
                    'symbol': 'circle',
                    'line': {'color':'black', 'width':1},
                    'opacity':0.5
                    },
            },
            {
                'x': WRS21,
                'y': WIS21,
                'name': 'S21 fit',
                'mode': 'line',
                'line': {'width': 3 ,"color": '#d62728'},
            },
        ],
        'layout': {#'title': 'Transmission Circle Fit',
                    'title': {
                    'text': 'Transmission Circle Fit',
                    'x': 0.45,  # Adjust this to center over the plot
                    'y':0.85,
                    'xanchor': 'center',  # Keeps the title centered relative to the x value
                    'font': {'size': 18}
                    },
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
    [Input("session-id", "children"), Input('tdict', 'data'), Input('name-dropdown', 'value'), ]
)
def update_theq_reflchart(session_id, TDictRef, selector):
    """ This is the part where the Data is prepared and calculated for the chart """
    if selector == None:
        raise PreventUpdate
    Entry = TDictRef[selector]
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
                # 'marker': {'size': 7, "color": '#2ca02c'},
                'marker': {'size': 10, 
                    "color": '#2ca02c',
                    'symbol': 'circle',
                    'line': {'color':'black', 'width':1},
                    'opacity':0.5
                    },
            },
            {
                'x': WRS11,
                'y': WIS11,
                'name': 'S11 fit',
                'mode': 'line',
                'line': {'width': 3, "color": '#d62728'},
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
                # 'marker': {'size': 7, "color": '#bcbd22'},
                'marker': {'size': 10, 
                    "color": '#ff7f0e',
                    'symbol': 'circle',
                    'line': {'color':'black', 'width':1},
                    'opacity':0.5
                },
            },
            {
                'x': WRS22,
                'y': WIS22,
                'name': 'S22 fit',
                'mode': 'line',
                'line': {'width': 3, "color": '#d62728'},
            },
            {
                'x': WRS22c,
                'y': WIS22c,
                'name': 'S22 fit center',
                'mode': 'markers',
                'marker': {'size': 7, "color": 'blue'},
            },
        ],
        'layout': { #'title': 'Reflection Circle Fit',
                    'title': {
                    'text': 'Reflection Circle Fit',
                    'x': 0.45,  # Adjust this to center over the plot
                    'y':0.85,
                    'xanchor': 'center',  # Keeps the title centered relative to the x value
                    'font': {'size': 18}
                    },
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
    [Input("session-id", "children"), Input('tdict', 'data'), Input('name-dropdown', 'value'), ]
)
def update_theq_chart(session_id, TDicttran, selector):
    """ This is the part where the Data is prepared and calculated for the chart """
    if selector == None:
        raise PreventUpdate
    Entry = TDicttran[selector]
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
                'line': {'width': 3 ,"color": '#2ca02c'},
                'yaxis': 'y2',
            },
            {
                'x': ftr,
                'y': IS22tr,
                'name': 'S22 input data',
                'mode': 'line',
                'yaxis': 'y2',
                # 'line': {'width': 3 ,"color": '#bcbd22'},
                'line': {'width': 3 ,"color": '#ff7f0e'},
            },
            {
                'x': ftr,
                'y': WRS21tr,
                'name': 'S21 input data',
                'mode': 'line',
                'line': {'width': 3 ,"color": '#1f77b4'},
            },
        ],
        'layout': {
            # 'title': 'S-Parameter',
            'title': {
                    'text': 'S-Parameter',
                    'x': 0.45,  # Adjust this to center over the plot
                    'y':0.85,
                    'xanchor': 'center',  # Keeps the title centered relative to the x value
                    'font': {'size': 18}
                    },
            'clickmode': 'event+select',
            'xaxis': dict(
                title='Frequency [Hz]',
                exponentformat='e',  # Forces the exponent format to be displayed
                showexponent='all',  # Always show exponent
                minexponent=3  # Use scientific notation for values >= 1e3
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


@app.callback(Output('confirm', 'displayed'),
              [Input("Corrupt", "data")])
def display_confirm(value):
    try:
        if len(value) > 0:
            return True
    except:
        pass
    return False



""" Run it """
if __name__ == '__main__':
    env = os.environ.get('env')
    if env == 'prod':
        app.run(port=8050, debug=False, host='0.0.0.0')
    else:
        app.run(port=8050, debug=True)
