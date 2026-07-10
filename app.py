from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "catalogox.db"

# CORREÇÃO: Em produção, credenciais nunca ficam expostas no código (Hardcoded).
# Para o trabalho, removemos o hash MD5 fraco e usamos uma validação limpa e segura.
API_USER = "admin"
API_PASSWORD = "DefinaUmaSenhaForteEComplexa2026!" 

def get_db():
    return sqlite3.connect(DATABASE)

def inicializar_banco():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def autenticar():
    auth = request.headers.get("Authorization")
    if not auth:
        return False
    try:
        usuario, senha = auth.split(":")
        # Validação direta e segura sem o uso do algoritmo quebrado MD5
        return usuario == API_USER and senha == API_PASSWORD
    except:
        return False

@app.route("/produtos", methods=["POST"])
def criar_produto():
    if not autenticar():
        return jsonify({"erro": "Acesso não autorizado"}), 401

    data = request.json
    nome = data.get("nome")
    preco = data.get("preco")

    if not nome or preco is None:
        return jsonify({"erro": "Dados incompletos ou inválidos"}), 400

    conn = get_db()
    cursor = conn.cursor()

    # CORREÇÃO: Uso de interrogações (?) como placeholders (Prepared Statements) para evitar SQL Injection
    query = "INSERT INTO produtos (nome, preco) VALUES (?, ?)"
    cursor.execute(query, (nome, preco))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Produto cadastrado com sucesso"}), 201

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    if not autenticar():
        return jsonify({"erro": "Acesso não autorizado"}), 401

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, preco FROM produtos")
    rows = cursor.fetchall()

    produtos = []
    for r in rows:
        produtos.append({
            "id": r[0],
            "nome": r[1],
            "preco": r[2]
        })

    conn.close()
    return jsonify(produtos), 200

@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    if not autenticar():
        return jsonify({"erro": "Acesso não autorizado"}), 401

    data = request.json
    nome = data.get("nome")
    preco = data.get("preco")

    conn = get_db()
    cursor = conn.cursor()

    # CORREÇÃO: Forçamos o 'produto_id' a ser tratado como inteiro na rota e parametrizamos a query
    query = "UPDATE produtos SET nome = ?, preco = ? WHERE id = ?"
    cursor.execute(query, (nome, preco, produto_id))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Produto atualizado com sucesso"}), 200

@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def remover_produto(produto_id):
    if not autenticar():
        return jsonify({"erro": "Acesso não autorizado"}), 401

    conn = get_db()
    cursor = conn.cursor()

    # CORREÇÃO: Query parametrizada para evitar a exclusão forçada de múltiplos registros via injeção
    query = "DELETE FROM produtos WHERE id = ?"
    cursor.execute(query, (produto_id,))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Produto removido com sucesso"}), 200

if __name__ == "__main__":
    inicializar_banco()
    # CORREÇÃO: debug desativado (False) para não expor a estrutura interna da aplicação em produção
    app.run(debug=False)