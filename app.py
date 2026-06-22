import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
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

    if not nome or not email or not senha or not telefone or not tipo_usuario:
        return redirect(url_for('exibir_cadastro'))

    try:
        senha_criptografada = generate_password_hash(senha)
        
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha, telefone, tipo_usuario) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, senha_criptografada, telefone, tipo_usuario)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash("Cadastro realizado com sucesso! Faça seu login.")
        return redirect(url_for('exibir_login'))
        
    except Exception as e:
        return f"Erro ao cadastrar: {e}", 500
        
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not email or not senha:
        flash("Por favor, preencha todos os campos.")
        return redirect(url_for('exibir_login'))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nome, senha, tipo_usuario FROM usuario WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario:
        if check_password_hash(usuario[2], senha):
            session['id_usuario'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            session['tipo_usuario'] = usuario[3] 
            
            return render_template('login.html', login_sucesso=True)
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

@app.route('/cadastro')
def exibir_cadastro():
    return render_template('cadastro.html')

@app.route('/home')
def home():
    return render_template('home.html', nome=session.get('usuario_nome'))

@app.route('/perfil')
def perfil():
    if 'id_usuario' not in session:
        flash("Por favor, faça login primeiro.")
        return redirect(url_for('exibir_login'))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, telefone, tipo_usuario, foto_perfil FROM usuario WHERE id_usuario = %s", (session['id_usuario'],))
    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        conn.close()
        session.clear()
        return redirect(url_for('exibir_login'))

    # === CORRIGIDO AQUI: Adicionado 'foto_perfil' no dicionário que vai para o HTML ===
    usuario = {
        'nome': dados[0], 
        'email': dados[1], 
        'telefone': dados[2], 
        'tipo': dados[3],
        'foto_perfil': dados[4]  # <-- Agora o HTML consegue ler a foto!
    }

    artes = []
    if usuario['tipo'] == 'artista':
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
                'id': r[0],
                'titulo': r[1],
                'descricao': r[2],
                'preco': r[3],
                'url': r[4]
            })

    cursor.close()
    conn.close()

    if usuario['tipo'] == 'artista':
        return render_template('perfil_artista.html', usuario=usuario, artes=artes)
    else:
        return render_template('perfil_cliente.html', usuario=usuario)

@app.route('/atualizar_foto_perfil', methods=['POST'])
def atualizar_foto_perfil():
    if 'id_usuario' not in session:
        flash('Você precisa estar logado para alterar a foto de perfil.', 'danger')
        return redirect(url_for('login'))
    
    if 'foto_perfil' not in request.files:
        flash('Nenhum arquivo enviado.', 'danger')
        return redirect(url_for('exibir_editar_perfil'))
        
    file = request.files['foto_perfil']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado.', 'danger')
        return redirect(url_for('exibir_editar_perfil'))

    if file and arquivo_permitido(file.filename):
        extensao = file.filename.rsplit('.', 1)[1].lower()
        id_usuario = session['id_usuario']
        nome_arquivo = f"avatar_user_{id_usuario}.{extensao}"
        
        pasta_salvar = os.path.join('static', 'img', 'avatar')
        caminho_salvar = os.path.join(pasta_salvar, nome_arquivo)
        
        os.makedirs(pasta_salvar, exist_ok=True)
        file.save(caminho_salvar)
        
        caminho_banco = f"img/avatar/{nome_arquivo}"
        
        try:
            conn = conectar() 
            cursor = conn.cursor()
            
            print(f"\n[DEBUG] Tentando atualizar o usuario {id_usuario} com o caminho: {caminho_banco}")
            
            cursor.execute(
                "UPDATE usuario SET foto_perfil = %s WHERE id_usuario = %s",
                (caminho_banco, id_usuario)
            )
            conn.commit()
            print("[DEBUG] O comando UPDATE foi executado e o COMMIT foi feito com sucesso!\n")
            
            cursor.close()
            conn.close()
            
            flash('Foto de perfil updated com sucesso!', 'success')
        except Exception as e:
            print(f"\n[DEBUG] ERRO AO SALVAR NO BANCO: {e}\n")
            flash(f'Erro ao salvar no banco de dados: {e}', 'danger')
            
        return redirect(url_for('exibir_editar_perfil'))
        
    flash('Formato de arquivo não permitido. Use PNG, JPG, JPEG, GIF ou WEBP.', 'danger')
    return redirect(url_for('exibir_editar_perfil'))

@app.route('/perfil/novo-portfolio', methods=['POST'])
def novo_portfolio():
    if 'id_usuario' not in session or session.get('tipo_usuario') != 'artista':
        flash("Acesso restrito.")
        return redirect(url_for('exibir_login'))

    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco_estimado')
    file = request.files.get('imagem')

    if not preco:
        preco = None

    if not titulo or not file:
        flash("O título e a imagem são obrigatórios para a publicação.")
        return redirect(url_for('perfil'))

    if file and arquivo_permitido(file.filename):
        filename = secure_filename(file.filename)
        filename = f"artista_{session['id_usuario']}_{filename}"
        
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(caminho_completo)
        
        caminho_banco = f"imagens/portfolio/{filename}"

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO postagem (titulo, descricao, preco_estimado, tipo_post, id_artista) 
                   VALUES (%s, %s, %s, 'artista', %s) RETURNING id_postagem""",
                (titulo, descricao, preco, session['id_usuario'])
            )
            id_nova_postagem = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO midia_postagem (id_postagem, url, tipo) VALUES (%s, %s, 'imagem')",
                (id_nova_postagem, caminho_banco)
            )
            
            conn.commit()
            flash("Arte publicada com sucesso no seu portfólio!")
            
        except Exception as e:
            conn.rollback()
            flash(f"Erro ao salvar no banco: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Formato de imagem inválido. Use PNG, JPG, JPEG ou GIF.")

    return redirect(url_for('perfil'))

@app.route('/ideias')
def exibir_ideias():
    return render_template('ideias.html')

@app.route('/catalogo')
def exibir_catalogo():
    conn = conectar()
    cursor = conn.cursor()
    
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
        
    return render_template('catalogo.html', artes=feed_artes)

@app.route('/perfil/editar', methods=['GET'])
def exibir_editar_perfil():
    if 'id_usuario' not in session:
        flash("Por favor, faça login primeiro.")
        return redirect(url_for('exibir_login'))
    
    id_usuario = session['id_usuario']
    
    conn = conectar()
    cursor = conn.cursor()
    # === CORRIGIDO AQUI TAMBÉM: Trazendo a foto_perfil para a tela de edição ===
    cursor.execute("SELECT nome, email, telefone, tipo_usuario, foto_perfil FROM usuario WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not usuario:
        flash("Usuário não encontrado.")
        return redirect(url_for('home'))
    
    dados_usuario = {
        'nome': usuario[0],
        'email': usuario[1],
        'telefone': usuario[2],
        'tipo': usuario[3],
        'foto_perfil': usuario[4] # <-- Adicionado aqui
    }
    
    return render_template('editar_perfil.html', usuario=dados_usuario)

@app.route('/perfil/editar', methods=['POST'])
def editar_perfil():
    if 'id_usuario' not in session:
        return redirect(url_for('exibir_login'))
    
    id_usuario = session['id_usuario']
    
    novo_nome = request.form.get('nome')
    novo_email = request.form.get('email')
    novo_telefone = request.form.get('telefone')
    
    if not novo_nome or not novo_email:
        flash("Nome e E-mail são campos obrigatórios.")
        return redirect(url_for('exibir_editar_perfil'))
    
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE usuario SET nome = %s, email = %s, telefone = %s WHERE id_usuario = %s",
            (novo_nome, novo_email, novo_telefone, id_usuario)
        )
        conn.commit()
        
        session['usuario_nome'] = novo_nome
        flash("Dados updated com sucesso!")
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar perfil: {e}")
        flash("Erro ao atualizar os dados. Verifique se o e-mail já está em uso.")
        return redirect(url_for('exibir_editar_perfil'))
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('home'))

@app.route('/postagem/deletar/<int:id_postagem>', methods=['POST'])
def deletar_postagem(id_postagem):
    if 'id_usuario' not in session:
        return redirect(url_for('exibir_login'))
    
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM midia_postagem WHERE id_postagem = %s", (id_postagem,))
        cursor.execute("DELETE FROM postagem WHERE id_postagem = %s AND id_artista = %s", 
                       (id_postagem, session['id_usuario']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao deletar: {e}")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('perfil'))

@app.route('/postagem/editar/<int:id_postagem>', methods=['POST'])
def editar_postagem(id_postagem):
    if 'id_usuario' not in session:
        return redirect(url_for('exibir_login'))
        
    novo_titulo = request.form.get('titulo')
    nova_descricao = request.form.get('descricao')
    novo_preco = request.form.get('preco')
    
    if not novo_preco:
        novo_preco = None

    conn = conectar()
    cursor = conn.cursor()
    
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
    
    # === CORRIGIDO: Adicionado foto_perfil no SELECT ===
    cursor.execute("""
        SELECT nome, email, telefone, foto_perfil 
        FROM usuario 
        WHERE id_usuario = %s AND tipo_usuario = 'artista'
    """, (id_artista,))
    dados_artista = cursor.fetchone()
    
    if not dados_artista:
        cursor.close()
        conn.close()
        flash("Artista não encontrado.")
        return redirect(url_for('exibir_catalogo'))
        
    # === CORRIGIDO: Mapeado 'foto_perfil' para o dicionário (posição dados_artista[3]) ===
    artista = {
        'id': id_artista,
        'nome': dados_artista[0],
        'email': dados_artista[1],
        'telefone': dados_artista[2],
        'foto_perfil': dados_artista[3]  # <-- Puxa o caminho do banco de dados
    }
    
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