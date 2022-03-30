import datetime
from main import do_zip

from dash import Dash, dcc, html
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
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])

app.layout  = html.Div([
    header,
    upload_block,
    dcc.Download(id="download-zip"),
])


def parse_contents(contents, filename, date):

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(Output("download-zip", "data"),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        do_zip(list_of_contents, list_of_names)

        return dcc.send_file('reports.zip', filename="reports.zip")

if __name__ == '__main__':
    app.run_server(debug=True)