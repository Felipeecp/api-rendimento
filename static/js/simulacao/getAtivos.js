function getAtivos(){
    fetch("http://127.0.0.1:5000/titulos", {
      method: "GET",
      credentials: "include",
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    }).then(function (response) {
      if (response.status != 200) {
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(function (data) {
          select = document.getElementById('titulosDisponiveis');
          for (var i = 0; i< data.length; i++){
              var opt = document.createElement('option');
              opt.value = data[i];
              opt.innerHTML = data[i];
              select.appendChild(opt);
          }
      });
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });
}

getAtivos();