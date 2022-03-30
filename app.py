import datetime
from main import do_zip, close_tmp_file

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


header = html.Div([
    html.Span(className='helper'),
    html.Div(html.Img(src=f'assets/sedmax.png', className='logo'),
             style={'width': '20%', 'opacity': 0.95, 'align-self': 'center'}),
    html.Div(html.B("Преобразование отчетов XML 80040", style={'textAlign': 'center', 'color': 'rgba(241,241,241,0.9)', 'font-size': 22}),
             style={'width': '60%', 'text-align': 'center', 'vertical-align': 'middle', 'align-self': 'center'}),
    html.Div(style={'width': '20%', 'opacity': 0.9})
], className='header')


upload_block = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Перетащите или ',
            html.A('выберите файлы')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin-top': '20px',
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output'),
])

download_button = dbc.Button("Загрузить", id="dbutton", n_clicks=0, className="ant-electro-btn-primary",
            style={'margin-right': '3px', 'font-size': '14px'}
           )


app.layout  = html.Div([
    dcc.Store(id='memory'),
    header,
    html.Div([
        upload_block,
        dcc.Download(id="download-zip"),
        #download_button,
        html.Div(id='files_list'),
    ], style={'width': '80%', 'margin-left': '10%'})
])


def parse_contents(i, filename):

    return html.P(f'{i+1}. ' + filename)


@app.callback(Output("files_list", "children"),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename')
              )
def update_output(list_of_contents, list_of_names):

    if list_of_contents is not None:
        children = [parse_contents(i, n) for (i, n) in enumerate([n for n in list_of_names if n.endswith('.xml')])]

        content = html.Div([
            html.Div(html.H6('Список обработанных файлов:'), className='file_list'),
            html.Div(children=children, className='file_list',
                style={'overflow': 'scroll', 'borderWidth': '1px', 'margin-bottom': '10px',
                       'borderRadius': '5px', 'border-style': 'dotted', 'padding': '5px'}),
            html.Div(download_button, className='file_list')
        ])
        return content


@app.callback(Output("download-zip", "data"),
              Input('dbutton', 'n_clicks'),
              State('upload-image', 'filename'),
              State('upload-image', 'contents'),
              prevent_initial_call=True
              )
def update_output(n, list_of_names, list_of_contents):

    if n:
        if list_of_names is not None:
            data = [(n, c) for (n, c) in zip(list_of_names, list_of_contents) if n.endswith('.xml')]
            zip_file = do_zip(data)
            zip_file.flush()
            zip_file.seek(0)
            #close_tmp_file(zip_file)

        return dcc.send_file(zip_file.name, filename="XML_reports.zip")

if __name__ == '__main__':
    app.run_server(debug=True)