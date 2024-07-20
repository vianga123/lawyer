const loaderOut = document.querySelector("#loader-out");
function fadeOut(element) {
  let opacity = 1;
  const timer = setInterval(function () {
    if (opacity <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = opacity;
    opacity -= opacity * 0.1;
  }, 50);
}
fadeOut(loaderOut);

//finalizar proceso de un cliente
function eliminarProcesoU(id_proceso) {
  if (confirm("¿Estas seguro que desea finalizar el proceso?")){
      let url = `/borrar-proceso/${id_proceso}`;
      if (url) {
        window.location.href = url;
        window.alert("Proceso Finalizado con exito")
      }
  }
}

//consultar cliente ya existente   
$("#id").on("keyup", function() {
  var id = $("#id").val(); //CAPTURANDO EL VALOR DE INPUT CON ID CEDULA
  //var longitudCedula = $("#id").val().length; //CUENTO LONGITUD
  //if(longitudCedula >= 4){
  var dataString = 'cedula=' + id;
     $.ajax({
          url: `/buscando-cli/${id}`,
          type: "POST",
          data: dataString,
          dataType: "JSON",
          success: function(data){
            var html = "";
                for (var count = 0; count < data.length; count++) {
                    html += data[count].id;
                }
                if (html==id){
                  if(html==id){
                        alert("El documento "+html+" ya existe por favor verificar en lista de clientes.");
                        document.getElementById("id").value = "";
                        document.getElementById('id').focus();
                      }else{
                        document.getElementById('nombre_empleado').focus();
                      }
                  }
          }
          
      });
   // }
  });

//comprobar solo numeros en input
$('#id').on('keydown keypress',function(e){
    if(e.key.length === 1){ // Evaluar si es un solo caracter
        if($(this).val().length < 10 && !isNaN(parseFloat(e.key))){ /* Comprobar que
                                                                     * son menos de 10
                                                                     * catacteres y que
                                                                     * es un número */
            $(this).val($(this).val() + e.key); // Muestra el valor en el input
            //document.getElementById("id").value = "";
        }
        return false;
    }
});

$('#proceso_numero').on('keydown keypress',function(e){
  if(e.key.length === 1){ // Evaluar si es un solo caracter
      if($(this).val().length < 23 && !isNaN(parseFloat(e.key))){ /* Comprobar que
                                                                   * son menos de 10
                                                                   * catacteres y que
                                                                   * es un número */
          $(this).val($(this).val() + e.key); // Muestra el valor en el input
          //document.getElementById("id").value = "";
      }
      return false;
  }
});

//evitar contro c pegar
$("#id").on("paste", function(e) {
  var pastedData = e.originalEvent.clipboardData.getData('id');
  const globalRegex = new RegExp('^[0-9]*$', 'g');
  if (!globalRegex.test(pastedData)) {
    alert('Cadena incorrecta! ' + pastedData);
    e.preventDefault();
  }
});

//Terminar de guardar un proceso de un cliente
function terminarActualizar() {
  //var id = $("#id_cliente").val();
  if (confirm("¿Estas seguro que desea actualizar el proceso?")){
     var url = `/lista-de-clientes`;
        if (url){
          window.location.href = url ;
          window.alert("Proceso Finalizado con exito"+window.location.href+url);
        }    
     
  }
}


//inactivar delitos de un proceso ya guardado esto en el formulario de editar o actualizar proceso
function inacDel(id_delagra) {
  if (confirm("¿Estas seguro que desea borrar el delito con su agravante?"+id_delagra)){
      let url = `/borrar-delito/${id_delagra}`;
      if (url) {
        window.location.href = url;
        window.alert("Proceso Finalizado con exito");
      }
  }
}

// evitar doble click al actualizar cliente
function enviI() {
  $("envi").prop("disabled", true);
  if (confirm("¿Estas seguro que desea actualizar el cliente?")){
    $("envi").prop("disabled", true);
  }
}

//eviar doble click al registrar cliente
function enviII() {
  $("envicli").prop("disabled", true);
  if (confirm("¿Estas seguro que desea registrar el cliente?")){
    $("envicli").prop("disabled", true);
  }
}

//evidar doble click al cargar un documento del cliente
function carD() {
  $("car").prop("disabled", true);
  if (confirm("¿Estas seguro que desea cargar el documento del cliente?")){
    $("car").prop("disabled", true);
  }
}

//evidar doble click al registrar una etapa de un proceso
function etaC() {
  $("eta").prop("disabled", true);
  if (confirm("¿Estas seguro que desea registrar la etapa?")){
    $("eta").prop("disabled", true);
  }
}

//evidar doble click al actualizar un usaurio
function actUC() {
  $("act").prop("disabled", true);
  if (confirm("¿Estas seguro que desea actualizar la informacion del usuario?")){
    $("act").prop("disabled", true);
  }
}

//evidar doble click al registrar un usuario
function creaCu() {
  $("creacu").prop("disabled", true);
  if (confirm("¿Estas seguro que desea registrar el usuario?")){
    $("creacu").prop("disabled", true);
  }
}

