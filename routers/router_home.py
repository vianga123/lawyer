from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
from conexion.conexionBD import connectionBD  # Conexión a BD
#from controllers.funciones_home import model_dropdown

#main = Blueprint('dropdown_bp', __name__)

# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/clientes"

#lanzar formulario para crear un nuevo cliente
@app.route('/registrar-cliente', methods=['GET'])
def viewFormCliente():
    depto = comboDepto()
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_cliente.html', depto=depto)
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Guardar cliente nuevo
@app.route('/form-registrar-cliente', methods=['POST'])
def formCliente():
    if 'conectado' in session:
        if 'foto_empleado' in request.files:
            foto_perfil = request.files['foto_empleado']
            resultado = procesar_form_cliente(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_clientes'))
            else:
                flash('El empleado NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_cliente.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
# guardar nuevo proceso de un cliente
@app.route('/form-registrar-proceso', methods=['POST', 'GET'])
def formProceso():
    if 'conectado' in session:
        #if 'foto_empleado' in request.files:
            resultado = procesar_form_proceso(request.form)
            r2 = resul_Proceso(request.form)
            res = procesar_form_proceso_delito(request.form, r2)
            if resultado:
                return redirect(url_for('lista_clientes'))
            else:
                flash('El proceso NO fue registrado.', 'error')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# guardar delitos de un proceso de un cliente
@app.route('/form-registrar-delitos', methods=['POST', 'GET'])
def formDelitos():
    if 'conectado' in session:
        #if 'foto_empleado' in request.files:
            r2 = resul_Proceso(request.form)
            resultado = procesar_form_delito(request.form, r2)
            resultado2 = procesar_form_delito_update(request.form, r2)
            if resultado:
                 print("", resultado2)
                 return redirect(url_for('lista_clientes'))
            else:
                 flash('El proceso NO fue registrado.', 'error')
                 return render_template(f'{PATH_URL}/form_new_procesos.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# guardar etapa de un proceso
@app.route('/form-registrar-etapa', methods=['POST', 'GET'])
def formEtapa():
    if 'conectado' in session:
            resultado = procesar_form_etapa(request.form)
            if resultado:
                return redirect(url_for('lista_clientes'))
            else:
                flash('La etapa no fue guardada.', 'error')
                return render_template(f'{PATH_URL}/form_new_etapa.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
# guardar documentacion de un proceso especifico
@app.route('/form-registrar-documentos', methods=['POST', 'GET'])
def formCargaDocu():
    if 'conectado' in session:
        if 'document' in request.files:
            document = request.files['document']
            tipo = request.form['id_etapa_etapa']
            tproceso = request.form['id_tipo_proceso']
            resultado = procesar_form_carga(request.form, document, tipo, tproceso)
            if resultado:
                return redirect(url_for('lista_clientes()'))
            else:
                flash('La etapa no fue guardada.', 'error')
                return render_template(f'{PATH_URL}/form_new_etapa.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# listando los clientes
@app.route('/lista-de-clientes', methods=['GET','POST'])
def lista_clientes():
    if 'conectado' in session:
        return  render_template(f'{PATH_URL}/lista_clientes.html', clientes=sql_lista_clientesBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# listando los procesos por cliente
@app.route('/lista-de-procesos', methods=['GET'])
@app.route("/lista-de-procesos/<int:idCliente>", methods=['GET'])
def lista_procesos(idCliente=None):
    respuestaCliente = buscarProcesoBus(idCliente)
    if 'conectado' in session:
            return render_template(f'{PATH_URL}/lista_procesos.html', procesos=sql_lista_procesosBD(idCliente), respuestaCliente=respuestaCliente)
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# listando las etapas por proceso
@app.route('/lista-de-etapas', methods=['GET'])
@app.route("/lista-de-etapas/<int:idEtapa>", methods=['GET'])
def lista_etapas(idEtapa=None):
    if 'conectado' in session:
            return render_template(f'{PATH_URL}/form_new_etapa.html', etapas=sql_lista_etapasBD(idEtapa))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# formulario que muestra todos los datos del un cliente
@app.route("/detalles-cliente/", methods=['GET'])
@app.route("/detalles-cliente/<int:idCliente>", methods=['GET'])
def detalleCliente(idCliente=None):
    if 'conectado' in session:
        if idCliente is None:
            return redirect(url_for('inicio'))
        else:
            detalle_cliente = sql_detalles_clientesBD(idCliente) or []
            return render_template(f'{PATH_URL}/detalles_cliente.html', detalle_cliente=detalle_cliente)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
#listar procesos de cada cliente
@app.route("/procesos-cliente/", methods=['GET'])
@app.route("/procesos-cliente/<int:idCliente>", methods=['GET'])
def procesoCliente(idCliente=None):
    if 'conectado' in session:
        if idCliente is None:
            return redirect(url_for('inicio'))
        else:
            proceso_cliente = sql_detalles_clientesBD(idCliente) or []
            return render_template(f'{PATH_URL}/lista_procesos.html', proceso_cliente=proceso_cliente)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Buscador de Clientes
@app.route("/buscando-cliente", methods=['POST'])   
def viewBuscarClienteBDd():
    resultadoBusqueda = buscarClienteBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_cliente.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})
    
# Buscador de Procesos
@app.route("/buscando-proceso/<int:id>", methods=['POST'])
def viewBuscarProcesoBD(id):
    resultadoBusqueda = buscarProcesoBD(request.json['busqueda'], id)
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_proceso.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

# Buscador de etapas
@app.route("/buscando-etapa", methods=['POST'])
def viewBuscarEtapaBD():
    resultadoBusqueda = buscarEtapaBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_etapa.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


# modificar cliente *********************************************
@app.route("/editar-cliente/<int:id>", methods=['GET'])
def viewEditarCliente(id):
    if 'conectado' in session:
        respuestaCliente = buscarClienteUnico(id)
        depto = comboDepto()
        if respuestaCliente:
            return render_template(f'{PATH_URL}/form_cliente_update.html', respuestaCliente=respuestaCliente, depto=depto)
        else:
            flash('El cliente no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
# lanzar formulario para modificar proceso *
@app.route("/editar-proceso/<int:id>/<int:ti>", methods=["POST","GET"])
def viewEditarProceso(id:int, ti:int):
    tipoproceso = comboTipoProceso()
    combodelito= comboDelitos()
    depto = comboDepto()
    agrav = agraVantes(ti)
    if 'conectado' in session:
        respuestaProceso = buscarProUnico(ti)
        if respuestaProceso:
            return render_template(f'{PATH_URL}/form_update_proceso.html', respuestaProceso=respuestaProceso, tipoproceso=tipoproceso, depto=depto, agrav=agrav, combodelito=combodelito)
        else:
            flash('El proceso no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#Lanzar formulario para crear nuevo proceso de un cliente
@app.route("/new-proceso/<int:id>", methods=['GET','POST'])
def viewNewProceso(id):
    if 'conectado' in session:
        respuestaCliente = buscarClienteUnico(id)
        combodelito= comboDelitos()
        tipoproceso = comboTipoProceso()
        depto = comboDepto()
        if respuestaCliente:
            return render_template(f'{PATH_URL}/form_new_proceso.html', respuestaCliente=respuestaCliente, combodelito=combodelito, tipoproceso=tipoproceso, depto=depto)
        else:
            flash('El cliente no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


#lanzar formulario para crear nueva etapa de un proceso
@app.route('/new-etapa/<int:id>/<int:ti>', methods=['GET'])
def viewNewEtapa(id:int, ti:int):
    if 'conectado' in session:
        respuestaCliente = buscarProcesoUnico(id)
        listaEtapa = cargaListaEtapa(id)
        comboetapa = comboEtapa(ti)
        dato = datoCli(id)
        if respuestaCliente:
            return render_template(f'{PATH_URL}/form_new_etapa.html', respuestaCliente=respuestaCliente, dato=dato, comboetapa=comboetapa, listaEtapa=listaEtapa)
        else:
            flash('El cliente no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#lanzar formulario para cargar documentacion de un proceso
@app.route("/carga-documentos/<int:id>/<int:ti>", methods=['GET'])
def cargaDocumentos(id:int, ti:int):
    if 'conectado' in session:
        respuestaCliente = buscarProcesoUnicoDocu(id)
        comboetapa = comboEtapa(ti)
        dato = datoCli(id)
        cdocument = cargaDocument(id)
        if respuestaCliente:
            return render_template(f'{PATH_URL}/form_carga_documentos.html', respuestaCliente=respuestaCliente, dato=dato, comboetapa=comboetapa, cdocument=cdocument)
        else:
            flash('El cliente no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Recibir formuactualizarlario para actualizar informacion de cliente
@app.route('/actualizar-cliente', methods=['POST', 'GET'])
def actualizarCliente():
    foto_perfil = request.files['foto_empleado']
    resultData = procesar_actualizacion_form(request.form, foto_perfil)
    if resultData:
        return redirect(url_for('lista_clientes'))

# Recibir formulario para actualizar informacion de un proceso
@app.route('/form-actualizar-proceso', methods=['POST', 'GET'])
def actualizarProceso():
    resultData = procesar_actualizacion_proceso(request.form)
    if resultData == '1':
        return redirect(url_for('lista_clientes'))
   
#Lista de usuario que manejan el sistema
@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))

#eliminar usuario que manejan el sistema
@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))

#inactivar etapa 
@app.route('/borrar-etapa/<string:id>', methods=['GET'])
def eliminarEtapa(id):
    resp = borrarEtapa(id)
    if resp:
        flash('La etapa fue eliminda con exito', 'success')
        return redirect(url_for('lista_clientes'))
    
#inactivar proceso
@app.route('/borrar-proceso/<string:id>', methods=['GET'])
def eliminarProceso(id):
    resp = borrarProceso(id)
    if resp:
        flash('el proceso fue eliminado con Exito', 'success')
        return redirect(url_for('lista_clientes'))

#inactivar delito que se encuentra listado en el formulario de editar o actualizar
@app.route('/borrar-delito/<string:id>', methods=['GET'])
def eliminarDelito(id):
    resp = borrarDelito(id)
    if resp:
        flash('el delito fue eliminado con Exito', 'success')
        return redirect(url_for('lista_clientes'))

@app.route("/descargar-informe-clientes/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#cargando combo de area dependiendo del tipo de proceso
@app.route("/areas",methods=["POST","GET"])
def area():  
    if request.method == 'POST':
        try:    
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    id_tipo_area = request.form['id_tipo_area'] 
                    cursor.execute("SELECT * FROM tbl_tipo_area WHERE id_tip_area = 5 OR id_area_tip = %s ORDER BY nombre_area ASC", [id_tipo_area] )
                    areamodel = cursor.fetchall()  
                    OutputArray = []
                    for row in areamodel:
                        outputObj = {
                            'id_tip_area': row['id_tip_area'],
                            'nombre_area': row['nombre_area']}
                        OutputArray.append(outputObj)
                return jsonify(OutputArray)
        except Exception as e:
            return f'Se produjo un error al consultar el tipo proceso del area segunda consulta segundo combo: {str(e)}'

# Buscador de Clientes que por si ya estan en el sistema
@app.route("/buscando-cli/<int:id>", methods=["GET","POST"])  
def buscandoCli(id):
   if (request.method ):
        try:    
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT id FROM tbl_empleados WHERE id = %s ", [id] )
                    areamodel = cursor.fetchall()  
                    OutputArray = []
                    for row in areamodel:
                        outputObj = { 'id': row['id']}
                        OutputArray.append(outputObj)
                return jsonify(OutputArray)
        except Exception as e:
            return f' Se  presento un error al buscar el cliente ya existente: {str(e)}'

# Buscador de proceso que por si ya estan en el sistema
@app.route("/buscando-pro/<int:id>", methods=["GET","POST"])  
def buscandoPro(id):
   if (request.method ):
        try:    
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT proceso_numero FROM tbl_procesos WHERE proceso_numero = %s ", [id] )
                    areamodel = cursor.fetchall()  
                    OutputArray = []
                    for row in areamodel:
                        outputObj = { 'proceso_numero': row['proceso_numero']}
                        OutputArray.append(outputObj)
                return jsonify(OutputArray)
        except Exception as e:
            return f' Se  presento un error al buscar el proceso ya existente: {str(e)}'

#cargando combo de juzgados dependiendo del municipio
@app.route("/depto",methods=["POST"])
def depto():  
    if 'conectado' in session:
        try:    
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cod_municipio = request.form['cod_municipio'] 
                    cursor.execute("SELECT * FROM tbl_juzgados WHERE id_municipio = %s ORDER BY id_municipio ASC", [cod_municipio] )
                    areamodel = cursor.fetchall()  
                    OutputArray = []
                    for row in areamodel:
                        outputObj = {
                            'id_juzgado': row['id_juzgado'],
                            'nombre_juzgado': row['nombre_juzgado'],
                            'id_municipio': row['id_municipio']}
                        OutputArray.append(outputObj)
                return jsonify(OutputArray)
        except Exception as e:
            return f'Se produjo un error al consultar los jugados pertenecientes a un munipio: {str(e)}'

#cargando combo de agravantes dependiendo del delito
@app.route("/agravante",methods=["POST","GET"])
def agravante():  
    if request.method == 'POST':
        id_delito_agravante = request.form['id_delito']
        res = buscarAgra(id_delito_agravante)
        if(res==[]):
            id_delito_agravante = '287'
        else:
            id_delito_agravante = request.form['id_delito'] 
        try:    
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM tbl_agravantes WHERE id_delito_agravante = %s ORDER BY descripcion ASC", [id_delito_agravante] )
                    areamodel = cursor.fetchall()  
                    OutputArray = []
                    for row in areamodel:
                        outputObj = {
                            'id_agravante': row['id_agravante'],
                            'id_delito_agravante': row['id_delito_agravante'],
                            'descripcion': row['descripcion']}
                        OutputArray.append(outputObj)
                return jsonify(OutputArray)
        except Exception as e:
            return f'Se produjo un error al consultar los agravantes del delito seleccionado: {str(e)}'

#Listar delitos de un proceso guardado
@app.route("/listarde",methods=["POST","GET"])
def listarde():  
    p_numero = request.form['radicado'] 
    r2 = resul_Proceso2(p_numero)
    if request.method == 'POST':
        try:    
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                    querySQL = (""" SELECT d.delitos_nombre, d.id_delito, a.id_agravante, a.id_delito_agravante, a.descripcion, da.id_agravante, da.id_cliente, da.id_proceso_delagra, da.id_delagra
                                     FROM tbl_agravantes AS a, tbl_delitos AS d, tbl_delitos_agravantes AS da 
                                     WHERE da.id_proceso_delagra = %s AND d.id_delito = da.id_delito AND a.id_agravante = da.id_agravante """
                                )
                    mycursor.execute(querySQL,(r2,))
                    areamodel = mycursor.fetchall()  
                    OutputArray = []
                    for row in areamodel:
                        outputObj = {
                            'delitos_nombre': row['delitos_nombre'],
                            'descripcion': row['descripcion']}
                        OutputArray.append(outputObj)
                return jsonify(OutputArray)
        except Exception as e:
            return f'Se produjo un error al consultar los delitos de un proceso guardado: {str(e)}'

#Retornar a la lista de clientes
@app.route('/volver-cliente', methods=["POST","GET"])
def volverCli():
    clientes=sql_lista_clientesBD()
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_clientes.html', clientes=clientes )
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#lanzar informacion acerca del sistema y su creador
@app.route('/acerca-de', methods=['GET'])
def acercaDe():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/acerca_de.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))





