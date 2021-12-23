import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def getTitulos():
    url = 'https://apiapex.tesouro.gov.br/aria/v1/sistd/custom/ultimaRentabilidadeCSV'
    titulos = pd.read_csv(url, sep=";", encoding="latin1")
    titulos[['Últ. 30 dias','Mêsanterior','No ano','12 meses','Compra','Venda']] = titulos[['Últ. 30 dias','Mêsanterior','No ano','12 meses','Compra','Venda']].apply(lambda x: x.str.replace(',','.'))

    titulos.query("Compra != '-'",inplace=True)
    titulos['Vencimento'] = pd.to_datetime(titulos['Vencimento'],format="%d/%m/%Y")
    titulos.reset_index(drop=True,inplace=True)
    for i in range(len(titulos)):
        titulos['Títulos'][i] = f"{titulos['Títulos'][i]} {titulos['Vencimento'][i].year}"

    return titulos


def calcular_tesouro(inicial, aporte_mensal, nome_do_titulo, dataset=getTitulos()):
    df = dataset[dataset["Títulos"] == nome_do_titulo]

    # Pegando a quantidade de meses
    startdt=pd.to_datetime(datetime.now().date())
    enddt = df["Vencimento"].iloc[0]
    len(pd.date_range(start=startdt,end=enddt,freq='M'))

    tempo = int(len(pd.date_range(start=startdt,end=enddt,freq='M')) - 1)

    # Calculo da taxa equivalente
    temp_t_equivalente = 1
    taxa_compra = df[df["Títulos"] == nome_do_titulo]['Compra']
    taxa_juros = float(taxa_compra)/100
    temp_t_atual = 12
    taxa_equivalente = (1 + taxa_juros) ** (temp_t_equivalente / temp_t_atual) - 1
    taxa_equivalente

    # Taxa da B3
    taxa = 0.25/100

    # definindo o juro mensal
    juros = taxa_equivalente

    # calculando os valores
    total = inicial + (aporte_mensal * tempo)
    valor_futuro = (aporte_mensal * (((1+juros)**(tempo))-1)) / juros
    bruto = round(((inicial * (1 + juros) ** tempo) + round(valor_futuro, 2)), 2)
    rendimento = bruto - total

    # fAZENDO UMA PREPARAÇÃO PRA FICAR MELHOR
    b3 = total * (1+(taxa/12)) ** tempo - total

    qt_dias = tempo * 30

    #Fazendo o calculo do imposto de renda
    if qt_dias <= 180:
        imposto = rendimento * 22.5 / 100
    elif qt_dias <= 360:
        imposto = rendimento * 20 / 100
    elif qt_dias <= 720:
        imposto = rendimento * 17.5 / 100
    else:
        imposto = rendimento * 15 / 100

    liquido = bruto - imposto - b3

    return bruto, total, round(imposto, 2), round(b3, 2), round(liquido, 2)
