import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `trilha`;")

cursor.execute("CREATE DATABASE `trilha`;")

cursor.execute("USE `trilha`;")

# criando tabelas
TABLES = {}
TABLES['Cursos'] = ('''
      CREATE TABLE `cursos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `curso` varchar(50) NOT NULL,
      `descricao` varchar(200) NOT NULL,
      `escola` varchar(20) NOT NULL,
      `duracao` int(200) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nome`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, senha) VALUES (%s, %s)'
usuarios = [
      ("Paula", generate_password_hash("alloha").decode('utf-8')),
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from trilha.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[0])

# inserindo cursos
cursos_sql = 'INSERT INTO cursos (curso, descricao, escola, duracao) VALUES (%s, %s, %s, %s)'
cursos = [
      ('Python', 'Começando com a Linguagem', 'Alura', 12),
      ('Python', 'Avançando na Linguagem', 'Alura', 12),
]
cursor.executemany(cursos_sql, cursos)

cursor.execute('select * from trilha.cursos')
print(' -------------  Cursos:  -------------')
for curso in cursor.fetchall():
    print(curso[1], '-', curso[2])


# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()