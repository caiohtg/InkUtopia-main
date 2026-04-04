from flask import Flask, request, render_template, redirect, url_for, session, flash
import psycopg2

app = Flask(__name__)
# A secret_key é obrigatória para usar session e flash
app.secret_key = 'chave_secreta_para_desenvolvimento'

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="DB_InkUtopia",
        user="postgres",
        password="230369"
    )

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')
    tipo_usuario = request.form.get('tipo_usuario')

    # Validação simples
    if not all([nome, email, senha, telefone, tipo_usuario]):
        return "Erro: Todos os campos são obrigatórios", 400

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha, telefone, tipo_usuario) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, senha, telefone, tipo_usuario)
        )
        conn.commit()
        return "Usuário cadastrado com sucesso!"
    except Exception as e:
        return f"Erro ao cadastrar: {e}", 500
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not email or not senha:
        flash("Por favor, preencha todos os campos.")
        return redirect(url_for('exibir_login')) # Redireciona de volta para a página de login

    conn = conectar()
    cursor = conn.cursor()
    
    # Buscamos o usuário pelo email
    cursor.execute("SELECT id_usuario, nome, senha FROM usuario WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if usuario:
        # usuario[2] é a senha vinda do banco (SELECT id, nome, senha...)
        if usuario[2] == senha:
            # Login Sucesso: Criamos a sessão
            session['id_usuario'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            return f"Bem-vindo, {usuario[1]}! Login realizado com sucesso."
        else:
            # Senha incorreta
            flash("Senha incorreta. Tente novamente.")
    else:
        # Email não encontrado
        flash("Email não cadastrado.")

    # Se chegou aqui, é porque o login falhou
    return redirect(url_for('exibir_login'))

# Rota apenas para exibir a página (HTML)
@app.route('/')
def exibir_login():
    return render_template('login.html') # Certifique-se de que seu HTML de login tenha este nome

if __name__ == '__main__':
    app.run(debug=True)