import mysql.connector.pooling
from flask import Flask, jsonify, request   
#from src.routes.usuarios import *
#from src.routes.imoveis import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.run(debug=True)
app.config["JWT_SECRET_KEY"] = "your-secret-key"  
jwt = JWTManager(app)

@app.route("/")
def hello():
    return "Hello World!"

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mydb_pool",
    pool_size=5,
    host="localhost",
    user="root",
    password="12345678",
    database="airbndb"
)

######################################################################################################


def formatarImovel(data):
    return {
        "id_imovel": data[0],
        "usuario_id": data[1],
        "endereco": data[2],
        "descricao": data[3],
        "valor": data[4],
        "fotos": data[5],
        "curtidas": data[6]
    }
@app.route("/imoveis")
def get_imoveis():
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Imovel")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    
    formatedValues = []
    for row in rows:
        formatedValues.append(formatarImovel(row))
    
    return jsonify(formatedValues)


@app.route("/imovel/<int:id>")
def get_imovel(id):
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Imovel WHERE id_imovel = %s", (id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return jsonify({"message": "Imóvel não encontrado"}), 404

    return jsonify(formatarImovel(row))


@app.route("/imoveis/<int:valor_maximo>")
def get_imoveis_valor(valor_maximo):
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Imovel WHERE valor < %s", (valor_maximo,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    formatedValues = []
    for row in rows:
        formatedValues.append(formatarImovel(row))

    return jsonify(formatedValues)




@app.route("/imoveis", methods=["POST"])
def create_imovel():
    data = request.json

    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE id_usuario = %s", (data["usuario_id"],))
    user_row = cursor.fetchone()

    if user_row is None:
        return jsonify({"message": "Usuário não encontrado"}), 404

    query = "INSERT INTO Imovel (usuario_id, endereco, descricao, valor, fotos, curtidas) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data["usuario_id"], data["endereco"], data["descricao"], data["valor"], data["fotos"], data["curtidas"])
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

    return "Imóvel criado com sucesso"



@app.route("/imoveis/<int:id>", methods=["PUT"])
def update_imovel(id):
    data = request.json

    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    query = "UPDATE Imovel SET usuario_id = %s, endereco = %s, descricao = %s, valor = %s, fotos = %s, curtidas = %s WHERE id_imovel = %s"
    values = (data["usuario_id"], data["endereco"], data["descricao"], data["valor"], data["fotos"], data["curtidas"], id)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

    return "Imovel updated successfully"


@app.route("/imoveis/<int:id>", methods=["DELETE"])
def delete_imovel(id):
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM Imovel WHERE id_imovel = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return "Imovel deleted successfully"

###########################################################################################

def formatarUsuario(data):
    return {
        "id_usuario": data[0],
        "nome_completo": data[1],
        "idade": data[2],
        "dono": data[3],
        "cpf": data[4],
        "username": data[5],
        "password": data[6]
    }

@app.route("/usuarios")
#@jwt_required()
def get_usuarios():
    #current_user = get_jwt_identity()
    conn = connection_pool.get_connection()
    
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    formatedValues = []
    for row in rows:
        formatedValues.append(formatarUsuario(row))

    return jsonify(formatedValues)

@app.route("/usuarios/<int:dono>")
#@jwt_required()
def get_usuarios_donos(dono):
    #current_user = get_jwt_identity()
    conn = connection_pool.get_connection()
    
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE dono  = %s", (dono,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    formatedValues = []
    for row in rows:
        formatedValues.append(formatarUsuario(row))

    return jsonify(formatedValues)

@app.route("/usuario/<int:id>")
def get_usuario(id):
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE id_usuario = %s", (id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return jsonify({"message": "Usuário não encontrado"}), 404

    return jsonify(formatarUsuario(row))


@app.route("/usuarios", methods=["POST"])
def create_usuario():
    data = request.json
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    query = "INSERT INTO Usuario (nome_completo, idade, dono, cpf, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
    password = data["password"]
    hashed_password = generate_password_hash(password)
    values = (data["nome_completo"], data["idade"], data["dono"], data["cpf"], data["username"], hashed_password)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

    return "Usuário created successfully"

@app.route("/usuario/<int:id>", methods=["PUT"])
def update_usuario(id):
    data = request.json

    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    query = "UPDATE Usuario SET nome_completo = %s, idade = %s, dono = %s, cpf = %s, username = %s, password = %s, WHERE id_usuario = %s"
    values = (data["nome_completo"], data["idade"], data["dono"], data["cpf"], data["username"], data["password"], id)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

    
    return "Usuário updated successfully"

@app.route("/usuario/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return "Usuário deleted successfully"

###########################################################################################################

def formatarReserva(data):
    return {
        "id_reserva": data[0],
        "entrada": data[1],
        "saida": data[2],
        "Usuario_id_usuario": data[3],
        "Imovel_id_imovel": data[4],
    }

@app.route("/reserva")
def get_reservas():
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Reserva")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    formatedValues = []
    for row in rows:
        formatedValues.append(formatarReserva(row))

    return jsonify(formatedValues)

@app.route("/reserva/<int:id>")
def get_reserva(id):
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Reserva WHERE id_reserva = %s", (id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return jsonify({"message": "Reserva não encontrada"}), 404

    return jsonify(formatarReserva(row))


@app.route("/reserva", methods=["POST"])
def create_reserva():
    data = request.json

    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE id_usuario = %s", (data["Usuario_id_usuario"],))
    user_row = cursor.fetchone()

    if user_row is None:
        return jsonify({"message": "Usuário não encontrado"}), 404

    cursor.execute("SELECT * FROM Imovel WHERE id_imovel = %s", (data["Imovel_id_imovel"],))
    imovel_row = cursor.fetchone()

    if imovel_row is None:
        return jsonify({"message": "Imóvel não encontrado"}), 404

    query = "INSERT INTO Reserva (entrada, saida, Usuario_id_usuario, Imovel_id_imovel) VALUES (%s, %s, %s, %s)"
    values = (data["entrada"], data["saida"], data["Usuario_id_usuario"], data["Imovel_id_imovel"])
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

    return "Reserva criada com sucesso"


@app.route("/reserva/<int:id>", methods=["PUT"])
def update_reserva(id):
    data = request.json

    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    query = "UPDATE Reserva SET entrada = %s, saida = %s, Usuario_id_usuario = %s, Imovel_id_imovel = %s WHERE id_reserva = %s"
    values = (data["entrada"], data["saida"], data["Usuario_id_usuario"], data["Imovel_id_imovel"], id)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

    return "Reserva updated successfully"

@app.route("/reserva/<int:id>", methods=["DELETE"])
def delete_reserva(id):
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM Reserva WHERE id_reserva = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return "Reserva deleted successfully"


#####################################################################################################



@app.route("/login", methods=["POST"])
def login():
    
    data = request.json
    username = data["username"]
    password = data["password"]

    
    
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario  WHERE username = %s", (username,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    
    if rows:
        hashed_password = rows[0][6]
        
        
        if check_password_hash(hashed_password, password):
        
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
        
            return jsonify(message="Invalid username or password"), 401
    else:
        return "Usuário não encontrado"
    
    
    
    
    
@app.route("/reset", methods=["PUT"])
def reset():
    
    data = request.json
    username = data["username"]
    cpf = data["cpf"]
    password = data["novo_password"]

    
    
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario  WHERE username = %s", (username,))

    rows = cursor.fetchall()
    if rows:
        if rows[0][4] == cpf:
            hashed_password = generate_password_hash(password)

            query = "UPDATE Usuario SET password = %s WHERE username = %s"
            values = (hashed_password, username)

            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()

            return "Senha atualizada com sucesso"
        else:
            cursor.close()
            conn.close()
            return "Não verificado"
    else:
        cursor.close()
        conn.close()
        return "Usuário não encontrado"
    

##########################################################################################
def formatarAluguel(data):
    return {
        "id_alugar": data[0],
        "Reserva_id_reserva": data[1]
    }
    
@app.route("/aluguel")
def get_alugueis():
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Aluguel")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    
    formatedValues = []
    for row in rows:
        formatedValues.append(formatarAluguel(row))
    
    return jsonify(formatedValues)


@app.route("/aluguel/<int:id>")
def get_aluguel(id):
    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Aluguel WHERE id_alugar = %s", (id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return jsonify({"message": "Aluguel não encontrado"}), 404

    return jsonify(formatarAluguel(row))



@app.route("/aluguel", methods=["POST"])
def create_aluguel():
    data = request.json

    conn = connection_pool.get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Reserva WHERE id_reserva = %s", (data["Reserva_id_reserva"],))
    reserva_row = cursor.fetchone()

    if reserva_row is None:
        return jsonify({"message": "Reserva não encontrada"}), 404

    query = "INSERT INTO Aluguel (Reserva_id_reserva) VALUES (%s)"
    values = (data["Reserva_id_reserva"],)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

    return "Aluguel criado com sucesso"

