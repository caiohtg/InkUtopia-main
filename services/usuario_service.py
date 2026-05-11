from db.connection import get_connection

def criar_usuario(nome, email, senha, telefone, tipo_usuario):
    conn = get_connection()

    if not conn:
        return "Erro na conexão"

    cursor = conn.cursor()

    query = """
    INSERT INTO usuario (nome, email, senha, telefone, tipo_usuario)
    VALUES (%s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(query, (nome, email, senha, telefone, tipo_usuario))
        conn.commit()
        return "Usuário cadastrado com sucesso!"

    except Exception as e:
        conn.rollback()
        return f"Erro: {e}"

    finally:
        conn.close()