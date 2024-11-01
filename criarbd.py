import sqlite3 as lite

# Criando conexão com o banco
con = lite.connect("dados.db")

# Criando tabela
with con:
    cursor = con.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Inventario(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "descricao TEXT, marca TEXT, data_do_estoque DATE, valor DECIMAL, imagem TEXT)"
    )
