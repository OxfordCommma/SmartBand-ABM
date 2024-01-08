from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def conectar_bd():
    return sqlite3.connect('sampledb.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ver_administradores', methods=['GET'])
def ver_administradores():
    con = conectar_bd()
    mi_cursor = con.cursor()
    mi_cursor.execute("SELECT * FROM EMPLEADOS")
    resultado = mi_cursor.fetchall()
    con.close()

    if request.method == 'GET':
        return jsonify(resultado)
    
@app.route('/ver_usuarios', methods=['GET'])
def ver_usuarios():
    con = conectar_bd()
    mi_cursor = con.cursor()
    mi_cursor.execute("SELECT * FROM CLIENTES")
    resultado = mi_cursor.fetchall()
    con.close()

    if request.method == 'GET':
        return jsonify(resultado)
    
@app.route('/ver_proveedores', methods=['GET'])
def ver_proveedores():
    con = conectar_bd()
    mi_cursor = con.cursor()
    mi_cursor.execute("SELECT * FROM PROVEEDORES")
    resultado = mi_cursor.fetchall()
    con.close()

    if request.method == 'GET':
        return jsonify(resultado)
    
@app.route('/ver_stock', methods=['GET'])
def ver_stock():
    con = conectar_bd()
    mi_cursor = con.cursor()
    mi_cursor.execute("SELECT * FROM PRODUCTOS")
    resultado = mi_cursor.fetchall()
    con.close()

    if request.method == 'GET':
        return jsonify(resultado)
    
@app.route('/ver_OrdenesCompra', methods=['GET'])
def ver_OrdenesCompra():
    con = conectar_bd()
    mi_cursor = con.cursor()
    mi_cursor.execute("SELECT DP.idDetallePedido, P.nombreproducto, CP.modelo, DP.cantidad, DP.precioTotal, PE.fechaentrega FROM DETALLESPEDIDOS DP JOIN CARACTERISTICASPRODUCTO CP ON DP.idCaracteristicaproducto = CP.idCaracteristicaproducto JOIN PRODUCTOS P ON CP.idProducto = P.idProducto JOIN PEDIDOS PE ON DP.idPedido = PE.idPedido;")
    resultado = mi_cursor.fetchall()
    con.close()

    if request.method == 'GET':
        return jsonify(resultado)
    
@app.route('/guardar_administrador', methods=['POST'])
def guardar_administrador():
    if request.method == 'POST':
        # Obtén los datos del cuerpo de la solicitud
        datos = request.json

        # Inserta los datos en la base de datos (asegúrate de validar y sanitizar los datos)
        con = conectar_bd()
        mi_cursor = con.cursor()
        mi_cursor.execute("""
            INSERT INTO EMPLEADOS (nombre, apellido, fechacontratacion, direccion, ciudad, pais, jefe, sueldobasico)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datos['nombre'],
            datos['apellido'],
            datos['fechaContratacion'],
            datos['direccion'],
            datos['ciudad'],
            datos['pais'],
            datos['jefe'],
            datos['sueldoBasico'],
        ))
        con.commit()
        con.close()

        return jsonify({'mensaje': 'Administrador guardado exitosamente'})

@app.route('/borrar_usuario', methods=['POST'])
def borrar_usuario():
    if request.method == 'POST':
        data = request.json
        numero_cliente = data.get('numeroCliente')

        con = conectar_bd()
        mi_cursor = con.cursor()

        # Realiza la operación de borrado en la base de datos
        mi_cursor.execute("DELETE FROM CLIENTES WHERE idCliente = ?", (numero_cliente,))
        con.commit()

        con.close()

        return jsonify({'message': 'Usuario borrado exitosamente'})
    
@app.route('/guardar_proveedor', methods=['POST'])
def guardar_proveedor():
    if request.method == 'POST':
        # Obtén los datos del cuerpo de la solicitud
        datos = request.json

        # Inserta los datos en la base de datos (asegúrate de validar y sanitizar los datos)
        con = conectar_bd()
        mi_cursor = con.cursor()
        mi_cursor.execute("""
            INSERT INTO PROVEEDORES (nombrecompañia, direccion, ciudad, codpostal, pais, telefono)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datos['nombreCompania'],
            datos['direccion'],
            datos['ciudad'],
            datos['codigoPostal'],
            datos['pais'],
            datos['telefono'],
        ))
        con.commit()
        con.close()

        return jsonify({'mensaje': 'Proveedor guardado exitosamente'})

@app.route('/borrar_proveedor', methods=['POST'])
def borrar_proveedor():
    if request.method == 'POST':
        data = request.json
        numero_proveedor = data.get('numeroProveedor')

        con = conectar_bd()
        mi_cursor = con.cursor()

        # Realiza la operación de borrado en la base de datos
        mi_cursor.execute("DELETE FROM PROVEEDORES WHERE idProveedor = ?", (numero_proveedor,))
        con.commit()

        con.close()

        return jsonify({'message': 'Proveedor borrado exitosamente'})

@app.route('/alta_baja_stock', methods=['POST'])
def alta_baja_stock():
    if request.method == 'POST':
        data = request.json
        opcion_stock = data.get('opcionStock')
        cantidad = data.get('cantidad')

        con = conectar_bd()
        mi_cursor = con.cursor()

        # Realiza la operación de Alta/Baja en la base de datos
        if opcion_stock == 'alta':
            mi_cursor.execute("UPDATE PRODUCTOS SET Stock = Stock + ? WHERE idProducto = 1", (cantidad,))
        elif opcion_stock == 'baja':
            mi_cursor.execute("UPDATE PRODUCTOS SET Stock = Stock - ? WHERE idProducto = 1", (cantidad,))
        
        con.commit()
        con.close()

        return jsonify({'message': 'Operación de Stock realizada exitosamente'})

@app.route('/modificar_usuario', methods=['POST'])
def modificar_usuario():
    if request.method == 'POST':
        data = request.json
        id_cliente = data.get('idCliente')
        nuevo_nombre = data.get('nuevoNombre')
        nuevo_apellido = data.get('nuevoApellido')

        con = conectar_bd()
        mi_cursor = con.cursor()

        # Realiza la operación de modificación en la base de datos
        mi_cursor.execute("UPDATE CLIENTES SET nombrecliente = ?, apellidocliente = ? WHERE idCliente = ?", (nuevo_nombre, nuevo_apellido, id_cliente))
        con.commit()
        con.close()

        return jsonify({'message': 'Usuario modificado exitosamente'})


if __name__ == '__main__':
    app.run(debug=True)

