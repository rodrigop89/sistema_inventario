import sqlite3 as lite
from datetime import datetime

# Função para conectar ao banco de dados


def conectar():
    return lite.connect("dados.db")

# Função para inserir um novo item no inventário


def inserir_form(i):
    with conectar() as con:
        cursor = con.cursor()
        query = (
            "INSERT INTO Inventario(descricao, marca, data_do_estoque, valor, imagem) "
            "VALUES(?, ?, ?, ?, ?)"
        )
        cursor.execute(query, i)

# Função para deletar um item do inventário com base no ID


def deletar_form(id):
    with conectar() as con:
        cursor = con.cursor()
        query = "DELETE FROM Inventario WHERE id=?"
        cursor.execute(query, (id,))  # Passa id como tupla

# Função para atualizar um item do inventário com base no ID


def atualizar_form(i):
    with conectar() as con:
        cursor = con.cursor()
        query = (
            "UPDATE Inventario SET descricao=?, marca=?, data_do_estoque=?, valor=?, imagem=? "
            "WHERE id=?"
        )
        cursor.execute(query, i)

# Função para consultar todos os itens do inventário


def ver_form():
    with conectar() as con:
        cursor = con.cursor()
        query = "SELECT * FROM Inventario"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

# Função para ver um item específico no inventário pelo ID


def ver_item_por_id(id):
    with conectar() as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Inventario WHERE id=?", (id,))
        row = cursor.fetchone()  # Usa fetchone para retornar um único item
        return row
