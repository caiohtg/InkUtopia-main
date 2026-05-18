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
<<<<<<< HEAD
        # conn.commit()
        # return "Usuário cadastrado com sucesso! Acessar página "
        conn.commit()
        flash("Cadastro realizado com sucesso! Faça seu login.")
        return redirect(url_for('exibir_login'))
=======
        conn.commit()
        return "Usuário cadastrado com sucesso!"
>>>>>>> 79b248e03e6f2527e2e3449c3d766c65bfe338e3
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
<<<<<<< HEAD
    cursor.execute("SELECT id_usuario, nome, senha, tipo_usuario FROM usuario WHERE email = %s", (email,))
=======
    cursor.execute("SELECT id_usuario, nome, senha FROM usuario WHERE email = %s", (email,))
>>>>>>> 79b248e03e6f2527e2e3449c3d766c65bfe338e3
    usuario = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if usuario:
        # usuario[2] é a senha vinda do banco (SELECT id, nome, senha...)
        if usuario[2] == senha:
            # Login Sucesso: Criamos a sessão
            session['id_usuario'] = usuario[0]
            session['usuario_nome'] = usuario[1]
<<<<<<< HEAD
            session['tipo_usuario'] = usuario[3] # Importante: 'cliente' ou 'artista'
            return redirect(url_for('home'))
=======
            return f"Bem-vindo, {usuario[1]}! Login realizado com sucesso."
>>>>>>> 79b248e03e6f2527e2e3449c3d766c65bfe338e3
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

<<<<<<< HEAD
# Rota para a home
@app.route('/home')
def home():
    # Verificamos se o usuário está logado na sessão
    if 'id_usuario' not in session:
        flash("Por favor, faça login primeiro.")
        return redirect(url_for('exibir_login'))
    
    return render_template('home.html', nome=session.get('usuario_nome'))

# Rota para o perfil ULTIMA ALTERAÇÃO
@app.route('/perfil')
def perfil():
    if 'id_usuario' not in session:
        return redirect(url_for('exibir_login'))

    # Buscamos os dados para exibir na página (nome, email, etc)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, telefone, tipo_usuario FROM usuario WHERE id_usuario = %s", (session['id_usuario'],))
    dados = cursor.fetchone()
    cursor.close()
    conn.close()

    usuario = {'nome': dados[0], 'email': dados[1], 'telefone': dados[2], 'tipo': dados[3]}

    # O "pulo do gato": decide o template baseado no tipo
    if usuario['tipo'] == 'artista':
        return render_template('perfil_artista.html', usuario=usuario)
    else:
        return render_template('perfil_cliente.html', usuario=usuario)

# Função de Logout
@app.route('/logout')
def logout():
    session.clear() # Limpa todos os dados da sessão
    flash("Você saiu da conta.")
    return redirect(url_for('exibir_login'))

# Exibir Cadastro
@app.route('/cadastrar')
def exibir_cadastro():
    return render_template('cadastrar.html')

# Exibir Home
@app.route('/home')
def exibir_home():
    return render_template('home.html')

# Exibir Ideias
@app.route('/ideias')
def exibir_ideias():
    return render_template('ideias.html')

#Exibir Catalogo
@app.route('/catalogo')
def exibir_catalogo():
    return render_template('catalogo.html')

#Exibir Sobre
@app.route('/sobre')
def exibir_sobre():
    return render_template('sobre.html')

=======
>>>>>>> 79b248e03e6f2527e2e3449c3d766c65bfe338e3
if __name__ == '__main__':
    app.run(debug=True)