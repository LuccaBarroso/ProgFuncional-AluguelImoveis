from flask import jsonify, request
from ...app import app, connection_pool
#from flask import current_app as app
def formatarUsuario(data):
    # Implemente a função para formatar os dados do usuário conforme necessário
    return {
        "id_usuario": data[0],
        "nome_completo": data[1],
        "idade": data[2],
        "dono": data[3],
        "cpf": data[4],
    }

@app.route("/usuarios")
def get_usuarios():
    # Get a connection from the pool
    conn = connection_pool.get_connection()

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve data from a table
    cursor.execute("SELECT * FROM Usuario")

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    # Close the cursor and return the connection to the pool
    cursor.close()
    conn.close()

    # Format and return the users as JSON
    formatedValues = []
    for row in rows:
        formatedValues.append(formatarUsuario(row))

    return jsonify(formatedValues)
