from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import base64
from dash.dependencies import Input, Output
import requests
import dash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

#Base de datos
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://cagomezj:1234@cluster0.lg8bsx8.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.sensores.sensor_1
result = 0

# Declarar data_dist fuera de la función para evitar el UnboundLocalError
data_dist = []
image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROcgZfPY5uOKR5jnyaCcaOeqQfPP8Ib4X50odGx55UYAtBz8IwzCXIYxVVH2W7CTR0EiE&usqp=CAU'

# Obtener la imagen desde la URL
encoded_image = base64.b64encode(requests.get(image_url).content).decode()

# Establecer el estilo de la imagen
image_style = {'width': '50%', 'height': 'auto'}


# App layout
app.layout = dbc.Container([
    # Primera fila con la gráfica
    dbc.Row([
        dbc.Col(html.Div([
            html.H1("Asentamiento Tuneladora", style={'text-align': 'center'}),
            html.Hr(),

            html.Div([
                html.H4(id='distancia-actual', style={'text-align': 'center', 'font-size': '28px'}),
                dcc.Graph(id='asentamiento'),
                dcc.Interval(
                    id='interval-component',
                    interval=1 * 500,  # en milisegundos, actualiza cada 1 segundo
                    n_intervals=0
                ),
                html.Div(id='alerta-texto', style={'text-align': 'center', 'margin-top': '10px'}),
            ]),

        ]), width=12),
    ]),

    # Segunda fila con el texto y la imagen
    dbc.Row([
        # Columna para el texto
        dbc.Col(html.Div([
            # Texto adicional
            html.P(
                "Un asentamiento se refiere a la deformación vertical que experimenta el suelo o una estructura sobre él debido a la aplicación de cargas. Este fenómeno es crucial en la ingeniería civil y la construcción, ya que afecta la estabilidad y el rendimiento de las estructuras.",
                style={'text-align': 'left', 'font-size': '20px', 'margin': '20px'}),
        ]), width=6),

        # Columna para la imagen
        dbc.Col(html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image), style=image_style),
        ]), width=6),
    ]),
     dbc.Row([
        # Columna para el texto
        dbc.Col(html.Div([
            # Texto adicional
            html.P(
                "Cuando se utiliza una tuneladora para excavar un túnel, la máquina excava el suelo y crea un espacio que luego se reviste con segmentos prefabricados. Durante este proceso, es posible que se produzcan asentamientos geotécnicos en la superficie del suelo, sobre todo si el suelo es susceptible a la compresión debido a la excavación.",
                style={'text-align': 'left', 'font-size': '20px', 'margin': '20px'}),
        ]), width=6),

        # Columna para el GIF
        dbc.Col(html.Div([
            html.Img(src='https://i.makeagif.com/media/6-24-2019/_WdjR3.gif', style={'width': '50%', 'height': 'auto'}),
        ]), width=6),
    ]),
], fluid=True, style={'backgroundColor': '#f0f0f0'})

@app.callback(
    [Output('asentamiento', 'figure'),
     Output('distancia-actual', 'children'),
     Output('alerta-texto', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def consultar(n):
    
    # Utilizar la variable global data_dist
    global data_dist , result , db
    result = db.find_one(sort=[('updated_at', -1)])
    distancia = int(result['distancia'])
    data_dist.append(distancia)
    
    # Crear el objeto de figura de Plotly
    fig = go.Figure(data=[go.Scatter(y=data_dist, mode='lines+markers')])
    
     # Agregar una línea horizontal en y=5
    fig.add_shape(
        type="line",
        x0=0,
        x1=len(data_dist),
        y0=1600,
        y1=1600,
        line=dict(color="red", width=2),
    )
    
    # Agregar un texto según la condición
    if distancia >= 1600:
        alerta_texto = html.Span("ALERTA", style={'color': 'red', 'font-size': '24px'})
    else:
        alerta_texto = html.Span("VAMOS REBIEN!!!!!", style={'color': 'green', 'font-size': '24px'})
    
    
    # Formatear la distancia para mostrarla en el H1
    distancia_texto = f"El asentamiento fue: {distancia} cm"
    
    return fig, distancia_texto,alerta_texto


if __name__ == "__main__":
    app.run_server(debug=True)