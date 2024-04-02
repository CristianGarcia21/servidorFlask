from flask import Flask, request, render_template
from flask_cors import CORS
from direct_dfa import DDFA
from reader import Reader
from parsing import Parser
from nfa import NFA
from dfa import DFA


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
            automaton_type = request.form['automaton_type']
            reader = Reader(regex)
            tokens = reader.CreateTokens()
            parser = Parser(tokens)
            tree = parser.Parse()
            if automaton_type == "DirectDFA":
                ddfa = DDFA(tree, reader.GetSymbols(), regex)
                ddfa.GraphDFA()

                return render_template('graph.html', regex=regex, imagen="grafo.png")
            elif automaton_type == "NFA":
                nfa = NFA(tree, reader.GetSymbols(), regex)
                nfa.WriteNFADiagram()
                return render_template('graph.html', regex=regex, imagen="grafo.png")
            elif automaton_type == "DFA":
                nfa = NFA(tree, reader.GetSymbols(), regex)
                dfa = DFA(nfa.trans_func, nfa.symbols,nfa.curr_state, nfa.accepting_states, regex)
                dfa.TransformNFAToDFA()
                dfa.GraphDFA()
                return render_template('graph.html', regex=regex, imagen="grafo.png")
            else:
                print("¡Opción no válida! Por favor, ingrese 'NFA', 'DFA' o 'DirectDFA'.")
                return render_template('index.html')
        except Exception as e:
            print(f"Error: {e}")
            return render_template('graph.html', regex=regex, imagen="")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
