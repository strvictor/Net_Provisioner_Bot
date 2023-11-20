import psycopg2
import mysql.connector
from datetime import datetime
import log


def Apresentacao(usuario):
    msg_apresentacao = f'''
Olá {usuario},

Seja bem vindo(a) ao *PRO-BETA-bot*

Fase de Desenvolvimento: `Beta`
'''
    return msg_apresentacao

def Verifica_Nome(nome_informado):
    usuarios = []
    try:
        # Estabelece a conexão com o banco de dados PostgreSQL
        conn = psycopg2.connect(
                dbname='dbemp00543',
                user='cliente_s',
                password='pRT0iWohci7#!3WT',
                host='177.104.253.232',
                port='5432'
            )
        print('Conexão bem-sucedida ao banco de dados PostgreSQL!')

        # Cria um cursor para executar operações no banco de dados
        cursor = conn.cursor()

        # Executa uma consulta SQL para recuperar todos os registros de uma tabela
        cursor.execute('SELECT name, login, email, profile_id, active FROM erp.v_users') 

        # Recupera todos os registros retornados pela consulta
        colunas = cursor.fetchall()
        
        # esvaziando a lista pra ser atualizada
        usuarios.clear()
        for coluna in colunas:
            dados = list(coluna)
            # adiciona na lista os dados pra consulta
            usuarios.append(dados)

    except psycopg2.Error as e:
        print('Erro ao conectar ao banco de dados PostgreSQL:', e)

    finally:
        # Certifica-se de fechar o cursor e a conexão após o uso
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    # faz a busca pra ver se tem o nome no banco da voalle 
    for usuario in usuarios:
        print(usuario)
        
        nome_bd = str(usuario[0]).upper()
        usuario_login = usuario[1]
        email = usuario[2]
        permissao = usuario[3]
        if permissao == 20 or nome_bd == 'PAULO VICTOR SILVA E SILVA':
            permissao = 'tecnico'
        else:
            permissao = 'consulta'
        status = usuario[-1]
        
        # verifica se tem o nome no banco da voalle e se o status ta ativo
        if nome_informado == nome_bd and status:
            #achou o nome no bd
            return nome_bd, usuario_login, email, permissao
        
    return 'nome não encontrado'


def Cadastro_No_Mysql(id_usuario_telegram, usuario_telegram, nome_completo, usuario, email, senha, permissao,):
    # Conectando ao banco de dados
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Str12345!@",
        database="dados_usuarios",
    )

    # Capturando data e hora atualizada
    data_hora_atual = datetime.now()
    data_e_hora_atual = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
    
    print(data_e_hora_atual)
    
    # Criando um objeto cursor para executar comandos SQL
    cursor = conexao.cursor()
    # Comando SQL para criar uma tabela chamada "clientes"
    comando_sql = f"""
    INSERT INTO usuarios_cadastrados 
        (`id_usuario_telegram`, `usuario_telegram`, `nome_completo`, `usuario`, `email`, `senha`, `permissao`, `data_criacao`, `ultimo_login`)
        VALUES ('{id_usuario_telegram}', '{usuario_telegram}', '{nome_completo}', '{usuario}', '{email}', '{senha}', '{permissao}', '{data_e_hora_atual}', '{data_e_hora_atual}');
    """

    # Executando o comando SQL para criar a tabela
    cursor.execute(comando_sql)

    # Finalizando a transação e fechando a conexão
    conexao.commit()
    cursor.close()
    conexao.close()
    
    return f'✅ Usuário _{usuario}_ *Cadastrado com sucesso* ✅'


def Consulta_Id(id_usuario):
    config = {
    'user': 'root',
    'password': 'Str12345!@',
    'host': 'localhost',
    'database': 'dados_usuarios',
}

    # Conectando ao banco de dados
    conexao = mysql.connector.connect(**config)

    # Criando um cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    # Exemplo de execução de uma consulta SELECT
    cursor.execute("SELECT id_usuario_telegram FROM usuarios_cadastrados")

    # Recuperando os resultados da consulta
    resultados = cursor.fetchall()

    # Imprimindo os resultados
    for resultado in resultados:
        if id_usuario == list(resultado)[0]:
            
            return 'usuario ja cadastrado'
        
    # Fechando o cursor e a conexão
    cursor.close()
    conexao.close()
    
    return 'usuario ainda não tem cadastro'


def Consulta_Permissao(id_usuario):
    
    config = {
    'user': 'root',
    'password': 'Str12345!@',
    'host': 'localhost',
    'database': 'dados_usuarios',
}

    # Conectando ao banco de dados
    conexao = mysql.connector.connect(**config)

    # Criando um cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    # Exemplo de execução de uma consulta SELECT
    cursor.execute(f"SELECT permissao FROM usuarios_cadastrados WHERE id_usuario_telegram = {id_usuario}")

    # Recuperando os resultados da consulta
    resultados = cursor.fetchall()

    # Imprimindo os resultados
    for resultado in resultados:
        
        permissao = list(resultado)[0]
        
    # Fechando o cursor e a conexão
    cursor.close()
    conexao.close()
    
    return permissao


def Timeout(id_usuario):
    config = {
        'user': 'root',
        'password': 'Str12345!@',
        'host': 'localhost',
        'database': 'dados_usuarios',
    }

    # Conectando ao banco de dados
    conexao = mysql.connector.connect(**config)

    # Criando um cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    # Exemplo de execução de uma consulta SELECT
    cursor.execute(f"SELECT ultimo_login FROM usuarios_cadastrados WHERE id_usuario_telegram = {id_usuario}")

    # Recuperando os resultados da consulta
    resultados = cursor.fetchall()

    data_hora_atual = datetime.now()
    data_e_hora_atual = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")

    # Imprimindo os resultados
    for resultado in resultados:

        ultimo_login = list(resultado)[0]
        
        # Converter as strings para objetos datetime
        data1 = datetime.strptime(ultimo_login, '%d/%m/%Y %H:%M:%S')
        data2 = datetime.strptime(data_e_hora_atual, '%d/%m/%Y %H:%M:%S')
        
        timeout = (data2 - data1).total_seconds()
        
    # Fechando o cursor e a conexão
    cursor.close()
    conexao.close()
        
    if timeout >= 43200.0:
        return 'timeout'
    
    else:
        return 'ok'
        

def Valida_Senha(id_usuario):
    config = {
        'user': 'root',
        'password': 'Str12345!@',
        'host': 'localhost',
        'database': 'dados_usuarios',
    }

    # Conectando ao banco de dados
    conexao = mysql.connector.connect(**config)

    # Criando um cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    # Exemplo de execução de uma consulta SELECT
    cursor.execute(f"SELECT senha FROM usuarios_cadastrados WHERE id_usuario_telegram = {id_usuario}")

    # Recuperando os resultados da consulta
    resultados = cursor.fetchall()

    data_hora_atual = datetime.now()
    data_e_hora_atual = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")

    # Imprimindo os resultados
    for resultado in resultados:

        senha_cadastrada = list(resultado)[0]
        
    # Fechando o cursor e a conexão
    cursor.close()
    conexao.close()
    
    return senha_cadastrada


def Atualiza_Timeout(id_usuario):
    config = {
        'user': 'root',
        'password': 'Str12345!@',
        'host': 'localhost',
        'database': 'dados_usuarios',
    }

    # Conectando ao banco de dados
    conexao = mysql.connector.connect(**config)

    # Criando um cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    data_hora_atual = datetime.now()
    data_e_hora_atual = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")

    # Exemplo de execução de uma consulta UPDATE
    cursor.execute(f"UPDATE `usuarios_cadastrados` SET `ultimo_login` = '{data_e_hora_atual}' WHERE `id_usuario_telegram` = '{id_usuario}'")

    # Confirmando a transação (importante para efetivar as mudanças no banco)
    conexao.commit()
    #print('timeout atualizado com sucesso')
    log.info(f'timeout atualizado com sucesso para o user {id_usuario}')
    

    # Fechando o cursor
    cursor.close()