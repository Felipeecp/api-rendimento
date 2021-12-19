from collections import namedtuple
from flask import Flask, request, jsonify, make_response
import json


from flask.templating import render_template
from functions.tesouro_direto import calcular_tesouro

app = Flask(__name__)

@app.route("/tesouros", methods=["POST"])
def tesouro():
    req = request.get_json()
    Investimento = namedtuple('Investimento', ['bruto', 'total', 'imposto', "b3", "liquido"])
    fundo = calcular_tesouro(float(req["aporteInicial"]), float(req["aporteMensal"]), "TESOURO PREFIXADO 2026")
    investimento = Investimento(fundo[0], fundo[1], fundo[2],fundo[3],fundo[4])
    res = make_response(jsonify(investimento._asdict()), 200)
    return res


@app.route("/")
def index():
    return render_template("index.html")
app.run(debug=True)