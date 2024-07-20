// buscador de clientes::::::::::::::::::::::::::::::::::::::::::::::::::::::
async function buscadorTableC(tableId) {
 
  let input, busqueda, url;
  url = "/buscando-cliente";
  
  input = document.getElementById("search");
  busqueda = input.value.toUpperCase();
  const dataPeticion = { busqueda };
  
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    
  };
  
  try {
    const response = await axios.post(url, dataPeticion, { headers });
    
    if (!response.status) {
      
      console.log(`HTTP error! status: ${response.status} 😭`);
      
    }
    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}

//buscador de procesos
async function buscadorTableP(tableId, id) {
 // window.alert(tableId)
  //window.alert(id)
  
  
  let  input, busqueda, url;
 
  
  //url =  `/buscando-proceso`;
  url =  `/buscando-proceso/${id} `;
 
  input = document.getElementById("search");
  
  busqueda = input.value.toUpperCase();
  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}


//buscador de etapas
async function buscadorTableE(tableId) {
  
  let input, busqueda, url;
  url = "/buscando-etapa";

  input = document.getElementById("search");
  busqueda = input.value.toUpperCase();

  const dataPeticion = { busqueda };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}



