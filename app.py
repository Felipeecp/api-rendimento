from collections import namedtuple
from flask import Flask, request, jsonify, make_response
import json
from flask.json import dumps


from flask.templating import render_template
from flask_cors import CORS, cross_origin
from numpy import invert
from functions.tesouro_direto import calcular_tesouro, getTitulos, calcular_poupanca

app = Flask(__name__)
CORS(app)

@app.route("/tesouros", methods=["POST"])
def tesouro():
    investimento =  ['bruto', 'total', 'imposto', "b3", "liquido"]
    try:
        req = request.get_json()

        ap_inicial, ap_mensal = float(req["aporteInicial"]), float(req["aporteMensal"])
        nome = req["nomeTitulo"]

        fundo = calcular_tesouro(ap_inicial, ap_mensal, nome)
        res = make_response(jsonify(dict(zip(investimento, fundo))), 200)
        
        return res
    except:
        return make_response(jsonify({}),500)

@app.route("/poupanca", methods=["GET"])
def poupanca():
    ap_inicial = 1000
    ap_mensal = 50 
    nome = 'Tesouro Selic 2024'
    try:
        fundo = calcular_poupanca(ap_inicial, ap_mensal, nome)
        return make_response(jsonify(fundo), 200)
    
    except:
        return make_response(jsonify({}),500)

@app.route("/titulos", methods=['GET'])
def titulos():
    try:
        titulos = getTitulos()['Títulos']
        titulos_json = []
        for titulo in titulos:
            titulos_json.append(titulo)
        return make_response(jsonify(titulos_json), 200)
    except:
        return make_response(jsonify({}),500)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)