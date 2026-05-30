# from flask import Flask, request, render_template, redirect, url_for, session, flash
# import psycopg2

# app = Flask(__name__)
# # A secret_key é obrigatória para usar session e flash
# app.secret_key = 'chave_secreta_para_desenvolvimento'

# def conectar():
#     return psycopg2.connect(
#         host="localhost",
#         database="DB_InkUtopia",
#         user="postgres",
#         password="230369"
#     )

# @app.route('/cadastrar', methods=['POST'])
# def cadastrar():
#     nome = request.form.get('nome')
#     email = request.form.get('email')
#     senha = request.form.get('senha')
#     telefone = request.form.get('telefone')
#     tipo_usuario = request.form.get('tipo_usuario')

#     # Validação simples
#     if not all([nome, email, senha, telefone, tipo_usuario]):
#         return "Erro: Todos os campos são obrigatórios", 400

#     conn = conectar()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO usuario (nome, email, senha, telefone, tipo_usuario) VALUES (%s, %s, %s, %s, %s)",
#             (nome, email, senha, telefone, tipo_usuario)
#         )
#         # conn.commit()
#         # return "Usuário cadastrado com sucesso! Acessar página "
#         conn.commit()
#         flash("Cadastro realizado com sucesso! Faça seu login.")
#         return redirect(url_for('exibir_login'))

#         conn.commit()
#         return "Usuário cadastrado com sucesso!"

#     except Exception as e:
#         return f"Erro ao cadastrar: {e}", 500
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.form.get('email')
#     senha = request.form.get('senha')

#     if not email or not senha:
#         flash("Por favor, preencha todos os campos.")
#         return redirect(url_for('exibir_login')) # Redireciona de volta para a página de login

#     conn = conectar()
#     cursor = conn.cursor()
    
#     # Buscamos o usuário pelo email

#     cursor.execute("SELECT id_usuario, nome, senha, tipo_usuario FROM usuario WHERE email = %s", (email,))

#     cursor.execute("SELECT id_usuario, nome, senha FROM usuario WHERE email = %s", (email,))

#     usuario = cursor.fetchone()
    
#     cursor.close()
#     conn.close()

#     if usuario:
#         # usuario[2] é a senha vinda do banco (SELECT id, nome, senha...)
#         if usuario[2] == senha:
#             # Login Sucesso: Criamos a sessão
#             session['id_usuario'] = usuario[0]
#             session['usuario_nome'] = usuario[1]
#             session['tipo_usuario'] = usuario[3] # Importante: 'cliente' ou 'artista'
#             return redirect(url_for('home'))

#             return f"Bem-vindo, {usuario[1]}! Login realizado com sucesso."

#         else:
#             # Senha incorreta
#             flash("Senha incorreta. Tente novamente.")
#     else:
#         # Email não encontrado
#         flash("Email não cadastrado.")

#     # Se chegou aqui, é porque o login falhou
#     return redirect(url_for('exibir_login'))

# # Rota apenas para exibir a página (HTML)
# @app.route('/')
# def exibir_login():
#     return render_template('login.html') # Certifique-se de que seu HTML de login tenha este nome


# # Rota para a home
# @app.route('/home')
# def home():
#     # Verificamos se o usuário está logado na sessão
#     if 'id_usuario' not in session:
#         flash("Por favor, faça login primeiro.")
#         return redirect(url_for('exibir_login'))
    
#     return render_template('home.html', nome=session.get('usuario_nome'))

# # Rota para o perfil ULTIMA ALTERAÇÃO
# @app.route('/perfil')
# def perfil():
#     if 'id_usuario' not in session:
#         return redirect(url_for('exibir_login'))

#     # Buscamos os dados para exibir na página (nome, email, etc)
#     conn = conectar()
#     cursor = conn.cursor()
#     cursor.execute("SELECT nome, email, telefone, tipo_usuario FROM usuario WHERE id_usuario = %s", (session['id_usuario'],))
#     dados = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     usuario = {'nome': dados[0], 'email': dados[1], 'telefone': dados[2], 'tipo': dados[3]}

#     # O "pulo do gato": decide o template baseado no tipo
#     if usuario['tipo'] == 'artista':
#         return render_template('perfil_artista.html', usuario=usuario)
#     else:
#         return render_template('perfil_cliente.html', usuario=usuario)

# # Função de Logout
# @app.route('/logout')
# def logout():
#     session.clear() # Limpa todos os dados da sessão
#     flash("Você saiu da conta.")
#     return redirect(url_for('exibir_login'))

# # Exibir Cadastro
# @app.route('/cadastrar')
# def exibir_cadastro():
#     return render_template('cadastrar.html')

# # Exibir Home
# @app.route('/home')
# def exibir_home():
#     return render_template('home.html')

# # Exibir Ideias
# @app.route('/ideias')
# def exibir_ideias():
#     return render_template('ideias.html')

# #Exibir Catalogo
# @app.route('/catalogo')
# def exibir_catalogo():
#     return render_template('catalogo.html')

# #Exibir Sobre
# @app.route('/sobre')
# def exibir_sobre():
#     return render_template('sobre.html')

# if __name__ == '__main__':
#     app.run(debug=True)

import os
from werkzeug.utils import secure_filename


from flask import Flask, request, render_template, redirect, url_for, session, flash
import psycopg2


app = Flask(__name__)
app.secret_key = 'chave_secreta_para_desenvolvimento'

# Configurações para o upload de imagens do portfólio
UPLOAD_FOLDER = 'static/imagens/portfolio'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="DB_InkUtopia",
        user="postgres",
        password="230369"
    )

# --- ROTAS DE AUTENTICAÇÃO (MÉTODOS POST) ---

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')
    tipo_usuario = request.form.get('tipo_usuario')

    if not all([nome, email, senha, telefone, tipo_usuario]):
        flash("Erro: Todos os campos são obrigatórios")
        return redirect(url_for('exibir_cadastro'))

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha, telefone, tipo_usuario) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, senha, telefone, tipo_usuario)
        )
        conn.commit()
        flash("Cadastro realizado com sucesso! Faça seu login.")
        return redirect(url_for('exibir_login'))
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
        return redirect(url_for('exibir_login'))

    conn = conectar()
    cursor = conn.cursor()
    
    # CORRIGIDO: Agora trazemos o tipo_usuario corretamente em uma única consulta
    cursor.execute("SELECT id_usuario, nome, senha, tipo_usuario FROM usuario WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if usuario:
        # usuario[2] é a senha vinda do banco
        if usuario[2] == senha:
            session['id_usuario'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            session['tipo_usuario'] = usuario[3] # Agora o índice 3 existe!
            return redirect(url_for('home'))
        else:
            flash("Senha incorreta. Tente novamente.")
    else:
        flash("Email não cadastrado.")

    return redirect(url_for('exibir_login'))

@app.route('/logout')
def logout():
    session.clear() 
    flash("Você saiu da conta.")
    return redirect(url_for('exibir_login'))


# --- ROTAS DE RENDERIZAÇÃO DE PÁGINAS (VISUALIZAÇÃO) ---

@app.route('/')
def exibir_login():
    return render_template('login.html')

@app.route('/cadastro') # Mudado o endpoint para não chocar com a rota POST
def exibir_cadastro():
    return render_template('cadastro.html')

@app.route('/home')
def home():
    # Deixamos a home pública visualmente, mas integrada com o Jinja se logado
    return render_template('home.html', nome=session.get('usuario_nome'))

@app.route('/perfil')
def perfil():
    if 'id_usuario' not in session:
        flash("Por favor, faça login primeiro.")
        return redirect(url_for('exibir_login'))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, telefone, tipo_usuario FROM usuario WHERE id_usuario = %s", (session['id_usuario'],))
    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        conn.close()
        session.clear()
        return redirect(url_for('exibir_login'))

    usuario = {'nome': dados[0], 'email': dados[1], 'telefone': dados[2], 'tipo': dados[3]}

    # SE FOR ARTISTA, BUSCAMOS O PORTFÓLIO DELE
    artes = []
    if usuario['tipo'] == 'artista':
        # ADICIONADO: p.id_postagem no SELECT para podermos editar/excluir
        cursor.execute("""
            SELECT p.id_postagem, p.titulo, p.descricao, p.preco_estimado, m.url 
            FROM postagem p
            JOIN midia_postagem m ON p.id_postagem = m.id_postagem
            WHERE p.id_artista = %s
            ORDER BY p.data_postagem DESC
        """, (session['id_usuario'],))
        
        resultados = cursor.fetchall()
        for r in resultados:
            artes.append({
                'id': r[0],           # <-- Guardando o ID da postagem aqui
                'titulo': r[1],
                'descricao': r[2],
                'preco': r[3],
                'url': r[4]
            })

    cursor.close()
    conn.close()

    if usuario['tipo'] == 'artista':
        # Passamos a lista 'artes' atualizada para o template do artista
        return render_template('perfil_artista.html', usuario=usuario, artes=artes)
    else:
        return render_template('perfil_cliente.html', usuario=usuario)

@app.route('/perfil/novo-portfolio', methods=['POST'])
def novo_portfolio():
    # Segurança: Verifica se o usuário está logado e se é realmente um artista
    if 'id_usuario' not in session or session.get('tipo_usuario') != 'artista':
        flash("Acesso restrito.")
        return redirect(url_for('exibir_login'))

    # Coleta os dados que vieram do formulário HTML
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco_estimado')
    file = request.files.get('imagem')

    # Se o preço veio vazio do formulário, transformamos em None (NULL no banco)
    if not preco:
        preco = None

    # Validação: A imagem e o título são obrigatórios
    if not titulo or not file:
        flash("O título e a imagem são obrigatórios para a publicação.")
        return redirect(url_for('perfil'))

    # Processamento do arquivo de imagem
    if file and arquivo_permitido(file.filename):
        # Limpa o nome do arquivo para evitar bugs com espaços ou acentos
        filename = secure_filename(file.filename)
        # Deixa o nome único adicionando o ID do artista no começo
        filename = f"artista_{session['id_usuario']}_{filename}"
        
        # Salva o arquivo fisicamente na pasta static/imagens/portfolio
        # 1. Garante que a pasta destino realmente exista antes de salvar
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # 2. Cria o caminho completo de forma segura para o sistema operacional
        caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 3. Salva o arquivo fisicamente
        file.save(caminho_completo)
        
        # 4. Força o caminho do banco a usar barras normais '/' para o HTML não quebrar
        caminho_banco = f"imagens/portfolio/{filename}"

        # Inserindo os dados no Banco de Dados
        conn = conectar()
        cursor = conn.cursor()
        try:
            # 1º INSERT: Salva as informações de texto na tabela 'postagem'
            # O RETURNING id_postagem traz de volta o ID que o banco acabou de gerar automaticamente
            cursor.execute(
                """INSERT INTO postagem (titulo, descricao, preco_estimado, tipo_post, id_artista) 
                   VALUES (%s, %s, %s, 'artista', %s) RETURNING id_postagem""",
                (titulo, descricao, preco, session['id_usuario'])
            )
            id_nova_postagem = cursor.fetchone()[0]

            # 2º INSERT: Usa o ID gerado acima para vincular a imagem na tabela 'midia_postagem'
            cursor.execute(
                "INSERT INTO midia_postagem (id_postagem, url, tipo) VALUES (%s, %s, 'imagem')",
                (id_nova_postagem, caminho_banco)
            )
            
            conn.commit() # Se os dois inserts derem certo, salva permanentemente
            flash("Arte publicada com sucesso no seu portfólio!")
            
        except Exception as e:
            conn.rollback() # Se der qualquer erro em um dos passos, cancela tudo para não quebrar os dados
            flash(f"Erro ao salvar no banco: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Formato de imagem inválido. Use PNG, JPG, JPEG ou GIF.")

    # Redireciona de volta para a página do perfil do artista
    return redirect(url_for('perfil'))

@app.route('/ideias')
def exibir_ideias():
    return render_template('ideias.html')

@app.route('/catalogo')
def exibir_catalogo():
    conn = conectar()
    cursor = conn.cursor()
    
    # Buscamos as fotos de todos os artistas, trazendo junto o nome do tatuador
    cursor.execute("""
        SELECT p.titulo, p.descricao, p.preco_estimado, m.url, u.nome, p.id_postagem, u.telefone, u.id_usuario
        FROM postagem p
        JOIN midia_postagem m ON p.id_postagem = m.id_postagem
        JOIN usuario u ON p.id_artista = u.id_usuario
        WHERE p.tipo_post = 'artista'
        ORDER BY p.data_postagem DESC
    """)
    
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Organiza os dados em uma lista de dicionários
    feed_artes = []
    for r in resultados:
        feed_artes.append({
            'titulo': r[0],
            'descricao': r[1],
            'preco': r[2],
            'url': r[3],
            'artista_nome': r[4],
            'id_postagem': r[5],
            'artista_telefone': r[6],
            'artista_id': r[7]
        })
        
    # Passamos a lista de artes globais para o template do catálogo
    return render_template('catalogo.html', artes=feed_artes)


@app.route('/postagem/deletar/<int:id_postagem>', methods=['POST'])
def deletar_postagem(id_postagem):
    # Verificar se o usuário está logado
    if 'id_usuario' not in session:
        return redirect(url_for('exibir_login'))
    
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # 1. Primeiro, deletamos o registro na tabela midia_postagem (chave estrangeira)
        cursor.execute("DELETE FROM midia_postagem WHERE id_postagem = %s", (id_postagem,))
        
        # 2. Depois, deletamos a postagem em si, garantindo que ela pertence ao artista logado
        cursor.execute("DELETE FROM postagem WHERE id_postagem = %s AND id_artista = %s", 
                       (id_postagem, session['id_usuario']))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao deletar: {e}")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('perfil')) # Redireciona de volta para o perfil do artista


@app.route('/postagem/editar/<int:id_postagem>', methods=['POST'])
def editar_postagem(id_postagem):
    if 'id_usuario' not in session:
        return redirect(url_for('exibir_login'))
        
    # Pega os novos dados digitados no formulário de edição
    novo_titulo = request.form.get('titulo')
    nova_descricao = request.form.get('descricao')
    novo_preco = request.form.get('preco')
    
    # Se o preço vier vazio, definimos como None para o banco
    if not novo_preco:
        novo_preco = None

    conn = conectar()
    cursor = conn.cursor()
    
    # Atualiza a postagem apenas se ela pertencer ao artista logado
    cursor.execute("""
        UPDATE postagem 
        SET titulo = %s, descricao = %s, preco_estimado = %s
        WHERE id_postagem = %s AND id_artista = %s
    """, (novo_titulo, nova_descricao, novo_preco, id_postagem, session['id_usuario']))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('perfil'))

@app.route('/artista/<int:id_artista>')
def perfil_publico(id_artista):
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Busca os dados públicos do artista
    cursor.execute("""
        SELECT nome, email, telefone 
        FROM usuario 
        WHERE id_usuario = %s AND tipo_usuario = 'artista'
    """, (id_artista,))
    dados_artista = cursor.fetchone()
    
    # Se o artista não existir, redireciona para o catálogo
    if not dados_artista:
        cursor.close()
        conn.close()
        flash("Artista não encontrado.")
        return redirect(url_for('exibir_catalogo'))
        
    artista = {
        'id': id_artista,
        'nome': dados_artista[0],
        'email': dados_artista[1],
        'telefone': dados_artista[2]
    }
    
    # 2. Busca todas as artes postadas por esse artista específico
    cursor.execute("""
        SELECT p.id_postagem, p.titulo, p.descricao, p.preco_estimado, m.url 
        FROM postagem p
        JOIN midia_postagem m ON p.id_postagem = m.id_postagem
        WHERE p.id_artista = %s
        ORDER BY p.data_postagem DESC
    """, (id_artista,))
    
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    
    artes_artista = []
    for r in resultados:
        artes_artista.append({
            'id': r[0],
            'titulo': r[1],
            'descricao': r[2],
            'preco': r[3],
            'url': r[4]
        })
        
    return render_template('perfil_publico.html', artista=artista, artes=artes_artista)


@app.route('/sobre')
def exibir_sobre():
    return render_template('sobre.html')


if __name__ == '__main__':
    app.run(debug=True)