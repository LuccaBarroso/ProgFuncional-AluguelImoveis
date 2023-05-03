import mysql.connector.pooling
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


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



# Create a connection pool with a maximum of 5 connections
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mydb_pool",
    pool_size=5,
    host="localhost",
    user="root",
    password="password",
    database="mydb"
)

# retornar todos os imoveis
@app.route("/imoveis")
def get_imoveis():
    # Get a connection from the pool
    conn = connection_pool.get_connection()

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve data from a table
    cursor.execute("SELECT * FROM Imovel")

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    # Close the cursor and return the connection to the pool
    cursor.close()
    conn.close()
    
    formatedValues = []
    for row in rows:
        formatedValues.append(formatarImovel(row))
    
    return jsonify(formatedValues)


#imovel pelo id
@app.route("/imoveis/<int:id>")
def get_imovel(id):
    # Get a connection from the pool
    conn = connection_pool.get_connection()

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve data from a table
    cursor.execute("SELECT * FROM Imovel WHERE id_imovel = %s", (id,))

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    # Close the cursor and return the connection to the pool
    cursor.close()
    conn.close()

    # Return the rows as a json
    return jsonify(formatarImovel(rows[0]))


# criar imovel
@app.route("/imoveis", methods=["POST"])
def create_imovel():
    # Get data from the request
    data = request.json

    # Get a connection from the pool
    conn = connection_pool.get_connection()

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute an INSERT query to create a new record in the "imovel" table
    query = "INSERT INTO Imovel (usuario_id, endereco, descricao, valor, fotos, curtidas) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data["usuario_id"], data["endereco"], data["descricao"], data["valor"], data["fotos"], data["curtidas"])
    cursor.execute(query, values)

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()

    # Return a success message
    return "Imovel created successfully"

# editar imovel
@app.route("/imoveis/<int:id>", methods=["PUT"])
def update_imovel(id):
    # Get data from the request
    data = request.json

    # Get a connection from the pool
    conn = connection_pool.get_connection()

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute an UPDATE query to update a record in the "imovel" table
    query = "UPDATE Imovel SET usuario_id = %s, endereco = %s, descricao = %s, valor = %s, fotos = %s, curtidas = %s WHERE id_imovel = %s"
    values = (data["usuario_id"], data["endereco"], data["descricao"], data["valor"], data["fotos"], data["curtidas"], id)
    cursor.execute(query, values)

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()

    # Return a success message
    return "Imovel updated successfully"


# deletar imovel
@app.route("/imoveis/<int:id>", methods=["DELETE"])
def delete_imovel(id):
    # Get a connection from the pool
    conn = connection_pool.get_connection()

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a DELETE query to delete a record in the "imovel" table
    cursor.execute("DELETE FROM Imovel WHERE id_imovel = %s", (id,))

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()

    # Return a success message
    return "Imovel deleted successfully"