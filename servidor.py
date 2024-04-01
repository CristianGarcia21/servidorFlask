from flask import Flask, request, render_template
from flask_cors import CORS
import graphviz 
import os

app = Flask(__name__, static_folder='static')
app.static_folder = 'static'
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    print("Entrando a la ruta /")
    if request.method == 'POST':
        regex = request.form['regex']
        print(f"Expresión regular recibida: {regex}")
        try:
            nombre_imagen = graficar_regex(regex)
            return render_template('graph.html', regex=regex, imagen=nombre_imagen)
        except Exception as e:
            print(f"Error al graficar la expresión regular: {e}")
            return render_template('graph.html', regex=regex, imagen="")
    return render_template('index.html')


@app.route('/graph')
def graph():
    print("Entrando a la ruta /graph")  # Agregar esta línea
    regex = request.args.get('regex')
    print(f"Expresión regular recibida: {regex}")  # Agregar esta línea
    nombre_imagen = graficar_regex(regex)
    return render_template('graph.html', regex=regex, imagen=nombre_imagen)

def graficar_regex(regex):
    print("Entrando a la función graficar_regex")  # Agregar esta línea

    # Crear un nuevo grafo
    grafo = graphviz.Digraph()

    # Configurar el diseño del grafo
    grafo.graph_attr['rankdir'] = 'LR'
    grafo.node_attr['shape'] = 'circle'

    # Crear los nodos y las aristas según la expresión regular
    estado_actual = 0
    for c in regex:
        if c == '(':
            estado_actual += 1
            grafo.node(str(estado_actual))
        elif c == ')':
            grafo.edge(str(estado_actual), str(estado_actual - 1))
        elif c == '+':
            estado_actual += 1
            grafo.node(str(estado_actual))
            grafo.edge(str(estado_actual - 1), str(estado_actual), label='+')
            grafo.edge(str(estado_actual), str(estado_actual - 1), label='+')
        elif c == '*':
            grafo.edge(str(estado_actual), str(estado_actual), label='*')
        else:
            estado_actual += 1
            grafo.node(str(estado_actual))
            grafo.edge(str(estado_actual - 1), str(estado_actual), label=c)

    # Generar la imagen en formato PNG
    nombre_imagen = 'grafo'
    ruta_imagen = os.path.join('static', nombre_imagen)
    print(f"Generando la imagen en: {ruta_imagen}")
    grafo.render(ruta_imagen, view=True, format='png', cleanup=True)


    return nombre_imagen



if __name__ == '__main__':
    app.run(debug=True)