function simularTesouro(vl_Inicial, vl_Mensal, nome) {
    var entry = {
        aporteInicial: vl_Inicial,
        aporteMensal: vl_Mensal,
        nomeTitulo: nome
    };
    console.log(entry)

    fetch("https://api-rendimento.herokuapp.com/tesouros", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
        .then(function (response) {
            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return;
            }
            response.json().then(function (data) {
                document.getElementById("iT").textContent = `Investimento total: R$ ${data['total']}`;
                document.getElementById("rB").textContent = `Retorno Bruto: R$ ${data["bruto"]}`;
                document.getElementById("custo").textContent = `Custo: R$ ${data["b3"]}`;
                document.getElementById("iR").textContent = `Imposto de Renda: R$ ${data["imposto"]}`;
                document.getElementById("rL").textContent = `Retorno Líquido: R$ ${data["liquido"]}`;
            });
        })
        .catch(function (error) {
            console.log("Fetch error: " + error);
        });

}

function submit_message() {
          
    var aporteInicial = document.getElementById("aporteInicial").value;
    var aporteMensal = document.getElementById("aporteMensal").value;
    
    var nome_titulo = document.getElementById("titulosDisponiveis").value;

    if (aporteInicial != "" && aporteMensal != "" && nome_titulo != 0) {
        simularTesouro(aporteInicial, aporteMensal, nome_titulo);
    }
  }