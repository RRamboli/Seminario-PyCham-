from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

produtos = []
proximo_id = 1

@app.route("/")
def index():
    return render_template("index.html")

# Listar todos os produtos
@app.route("/api/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos), 200

# Cadastrar novo produto
@app.route("/api/produtos", methods=["POST"])
def cadastrar_produto():
    global proximo_id

    dados = request.get_json()

    # Validação básica
    if not dados or not dados.get("nome") or dados.get("preco") is None:
        return jsonify({"erro": "Os campos 'nome' e 'preco' são obrigatórios."}), 400
    try:
        preco = float(dados["preco"])
    except (ValueError, TypeError):
        return jsonify({"erro": "O preço deve ser um número válido."}), 400

    produto = {
        "id": proximo_id,
        "nome": dados["nome"].strip(),
        "preco": preco,
        "descricao": dados.get("descricao", "").strip()
    }
    produtos.append(produto)
    proximo_id += 1
    return jsonify(produto), 201

# Buscar produto por ID
@app.route("/api/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    produto = next((p for p in produtos if p["id"] == produto_id), None)

    if not produto:
        return jsonify({"erro": "Produto não encontrado."}), 404

    return jsonify(produto), 200

# Deletar produto
@app.route("/api/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    global produtos

    produto = next((p for p in produtos if p["id"] == produto_id), None)

    if not produto:
        return jsonify({"erro": "Produto não encontrado."}), 404

    produtos = [p for p in produtos if p["id"] != produto_id]
    return jsonify({"mensagem": "Produto removido com sucesso."}), 200


if __name__ == "__main__":
    app.run(debug=True)