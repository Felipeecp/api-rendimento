from collections import namedtuple
from flask import Flask, request
import json
from functions.tesouro_direto import calcular_tesouro

app = Flask(__name__)

@app.route("/<aportInicial>/<aporteMensal>", methods=["GET", 'POST'])
def home(aportInicial, aporteMensal):
    # dados_user = request.form["user_parametros"]
    # dados_user = json.loads(data_selecionadas)
    Investimento = namedtuple('Investimento', ['bruto', 'total', 'imposto', "b3", "liquido"])
    fundo = calcular_tesouro(float(aportInicial), float(aporteMensal), "TESOURO PREFIXADO 2026")
    investimento = Investimento(fundo[0], fundo[1], fundo[2],fundo[3],fundo[4])
    return json.dumps(investimento._asdict())

app.run(debug=True)