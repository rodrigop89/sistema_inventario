import tkinter.font as tkFont
from datetime import datetime
from tkinter import *
from tkinter import StringVar, Tk
from tkinter import filedialog as fd
from tkinter import messagebox, ttk

from PIL import Image, ImageTk
from tkcalendar import DateEntry

from view import inserir_form, atualizar_form, deletar_form, ver_form, ver_item_por_id

# Lista de cores

co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # letra
co5 = "#e06636"  # - profit
co6 = "#038cfc"  # azul
co7 = "#3fbfb9"  # verde
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # + verde


# Criando a janela

janela = Tk()
janela.title("Sistema Inventário")
janela.geometry("900x600")
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")

"""Criando os Frames"""

# Frame na parte superior da janela
frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

# Frame na parte do meio da janela
frameMeio = Frame(janela, width=1043, height=303, bg=co1, relief="flat")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

# Frame na parte direita da janela
frameDireita = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frameDireita.grid(row=2, column=0, pady=0, padx=1, sticky=NSEW)

# Logo do aplicativo
app_img = Image.open(r"E:\projetos\projeto_inventario\imagens\inventario.png")
app_img = app_img.resize((45, 45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text="Inventário", width=900, compound=LEFT,
                 relief=RAISED, anchor=NW, font="Verdana 20 bold", bg=co1, fg=co4)
app_logo.place(x=0, y=0)

"""Criando as entradas do sistema"""

global tree
# Função inserir


def inserir():
    global imagem_string
    descricao = e_descricao.get()
    marca = e_marca.get()
    data = e_data_estoque.get()
    valor = e_valor.get()
    imagem = imagem_string  # Se imagem_string for uma variável global, mantenha-a assim

    lista_inserir = [descricao, marca, data, valor, imagem]

    for i in lista_inserir:
        if i == "":
            messagebox.showerror("Erro", "Preencha todos os campos")
            return

    inserir_form(lista_inserir)

    messagebox.showinfo("Sucesso", "Dados inseridos com sucesso")

    # Limpar os campos de entrada
    e_descricao.delete(0, "end")
    e_marca.delete(0, "end")
    e_data_estoque.delete(0, "end")
    e_valor.delete(0, "end")

    # Limpar os widgets no frameDireita
    for widget in frameDireita.winfo_children():
        widget.destroy()

    mostrar()

# Função Atualizar


def atualizar():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']

        id = int(treev_lista[0])
        e_descricao.delete(0, "end")
        e_marca.delete(0, "end")
        e_data_estoque.delete(0, "end")
        e_valor.delete(0, "end")

        e_descricao.insert(0, treev_lista[1])
        e_marca.insert(0, treev_lista[2])
        e_data_estoque.insert(0, treev_lista[3])
        e_valor.insert(0, treev_lista[4])

        # Botão Atualizar
        def confirmar_atualizacao():
            descricao = e_descricao.get()
            marca = e_marca.get()
            data = e_data_estoque.get()
            valor = e_valor.get()
            imagem = imagem_string  # Atualize isso conforme necessário

            atualizar_form((descricao, marca, data, valor, imagem, id))
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso")

            for widget in frameDireita.winfo_children():
                widget.destroy()

            mostrar()

        # Criar botão para confirmar a atualização
        botao_confirmar = Button(
            frameMeio, text="Confirmar Atualização", command=confirmar_atualizacao)
        botao_confirmar.place(x=130, y=160)

    except Exception as e:
        messagebox.showerror("Erro", "Selecione um item para atualizar")

# Função Deletar


def deletar():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        id = int(treev_dicionario['values'][0])

        deletar_form((id,))
        messagebox.showinfo("Sucesso", "Item deletado com sucesso")

        for widget in frameDireita.winfo_children():
            widget.destroy()

        mostrar()
    except Exception as e:
        messagebox.showerror("Erro", "Selecione um item para deletar")

# Função Ver Imagem


def ver_imagem():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        # Supondo que o caminho da imagem está na coluna 5
        imagem_path = treev_dicionario['values'][5]

        if imagem_path:
            img_window = Toplevel(janela)
            img_window.title("Imagem do Item")
            img_window.geometry("400x400")

            # Carregar e redimensionar a imagem
            img = Image.open(imagem_path)
            img = img.resize((300, 300), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)

            img_label = Label(img_window, image=img_tk)
            img_label.image = img_tk  # Manter uma referência da imagem
            img_label.pack(pady=20)

            img_window.mainloop()
        else:
            messagebox.showwarning(
                "Aviso", "Nenhuma imagem disponível para este item.")
    except Exception as e:
        messagebox.showerror(
            "Erro", "Selecione um item para visualizar a imagem.")

# Função para ver detalhes do item selecionado


def ver_item_por_id(id):
    # Aqui você deve buscar os detalhes do item no seu banco de dados ou lista
    detalhes = ver_form(id)  # Supondo que ver_form retorna os detalhes do item

    # Exibir os detalhes em uma nova janela
    ver_window = Toplevel(janela)
    ver_window.title("Detalhes do Item")
    ver_window.geometry("400x400")

    # Criar Labels para exibir os detalhes
    Label(ver_window, text="Descrição: " + detalhes[0]).pack()
    Label(ver_window, text="Marca: " + detalhes[1]).pack()
    Label(ver_window, text="Data: " + detalhes[2]).pack()
    Label(ver_window, text="Valor: " + detalhes[3]).pack()

    if detalhes[4]:  # Se houver imagem
        img = Image.open(detalhes[4])
        img = img.resize((100, 100), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        img_label = Label(ver_window, image=img_tk)
        img_label.image = img_tk  # Manter uma referência da imagem
        img_label.pack(pady=10)

# Modificar a função ver_imagem para usar ver_item_por_id


def ver_imagem():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        # Supondo que o ID é a primeira coluna
        id = int(treev_dicionario['values'][0])

        ver_item_por_id(id)  # Chama a função para ver o item por ID
    except Exception as e:
        messagebox.showerror(
            "Erro", "Selecione um item para visualizar a imagem.")


# Campo Descrição
l_descricao = Label(frameMeio, text="Descrição", height=1,
                    anchor=NW, font=("Ivy", 10, "bold"), bg=co1, fg=co4)
l_descricao.place(x=10, y=10)
e_descricao = Entry(frameMeio, width=30, justify="left", relief="solid")
e_descricao.place(x=130, y=11)


# Campo Marca
l_marca = Label(frameMeio, text="Marca", height=1,
                anchor=NW, font=("Ivy", 10, "bold"), bg=co1, fg=co4)
l_marca.place(x=10, y=40)
e_marca = Entry(frameMeio, width=30, justify="left", relief="solid")
e_marca.place(x=130, y=41)

# Campo Data do Estoque
l_data_estoque = Label(frameMeio, text="Data do Estoque",
                       height=1, anchor=NW, font=("Ivy", 10, "bold"), bg=co1, fg=co4)
l_data_estoque.place(x=10, y=70)
e_data_estoque = DateEntry(frameMeio, width=15, background="darkblue",
                           foreground="white", borderwidth=2, year=2024,
                           date_pattern="dd/MM/yyyy", locale="pt_BR")
e_data_estoque.place(x=130, y=71)

# Campo Valor
l_valor = Label(frameMeio, text="Valor", height=1, anchor=NW,
                font=("Ivy", 10, "bold"), bg=co1, fg=co4)
l_valor.place(x=10, y=100)
e_valor = Entry(frameMeio, width=30, justify="left", relief="solid")
e_valor.place(x=130, y=101)

# Imagem
l_carregar_imagem = Label(frameMeio, text="Imagem do Item",
                          height=1, anchor=NW, font=("Ivy", 10, "bold"), bg=co1, fg=co4)
l_carregar_imagem.place(x=10, y=130)
botao_carregar = Button(frameMeio, compound=CENTER, anchor=CENTER, text="carregar".upper(),
                        width=30, overrelief=RIDGE, font=('ivy 8'), bg=co1, fg=co0)
botao_carregar.place(x=130, y=131)

"""Botões referentes as funções CRUD"""

# Botão inserir
img_add = Image.open(r"E:\projetos\projeto_inventario\imagens\inserir.png")
img_add = img_add.resize((20, 20))
img_add = ImageTk.PhotoImage(img_add)
botao_inserir = Button(frameMeio, image=img_add, compound=LEFT, anchor=NW,
                       text=" inserir ".upper(), width=95, overrelief=RIDGE,
                       font=("ivy 8"), bg=co1, fg=co0)
botao_inserir.place(x=350, y=10)

# Botao Atualizar
img_atualizar = Image.open(
    r"E:\projetos\projeto_inventario\imagens\atualizar.png")
img_atualizar = img_atualizar.resize((20, 20))
img_atualizar = ImageTk.PhotoImage(img_atualizar)
botao_atualizar = Button(frameMeio, image=img_atualizar, compound=LEFT, anchor=NW,
                         text=" Atualizar ".upper(), width=95, overrelief=RIDGE,
                         font=("ivy 8"), bg=co1, fg=co0)
botao_atualizar.place(x=350, y=50)

# Botal Deletar
img_delete = Image.open(r"E:\projetos\projeto_inventario\imagens\delete.png")
img_delete = img_delete.resize((20, 20))
img_delete = ImageTk.PhotoImage(img_delete)
botao_delete = Button(frameMeio, image=img_delete, compound=LEFT, anchor=NW,
                      text=" Excluir ".upper(), width=95, overrelief=RIDGE,
                      font=("ivy 8"), bg=co1, fg=co0)
botao_delete.place(x=350, y=90)

# Botão Consultar
img_consultar = Image.open(
    r"E:\projetos\projeto_inventario\imagens\consultar.png")
img_consultar = img_consultar.resize((20, 20))
img_consultar = ImageTk.PhotoImage(img_consultar)
botao_consultar = Button(frameMeio, image=img_consultar, compound=LEFT, anchor=NW,
                         text=" Consultar ".upper(), width=95, overrelief=RIDGE,
                         font=("ivy 8"), bg=co1, fg=co0)
botao_consultar.place(x=350, y=129)


"""Ver Quantidade Total de Intes e Valores"""

# Valor total de itens
l_total = Label(frameMeio, width=14, height=2, anchor=CENTER, font=("Ivy 17 bold"),
                bg=co1, fg=co0, relief=FLAT)
l_total.place(x=500, y=16)
l_valor_total = Label(frameMeio, text="Valor total", anchor=NW, font=("Ivy 10 bold"),
                      bg=co1, fg=co0)
l_valor_total.place(x=565, y=14)

# Quantidade total de itens
l_quantidade = Label(frameMeio, width=14, height=2, anchor=CENTER, font=("Ivy 17 bold"),
                     bg=co1, fg=co0, relief=FLAT)
l_quantidade.place(x=500, y=97)
l_quantidade_total = Label(frameMeio, text="Quantidade total", anchor=NW, font=("Ivy 10 bold"),
                           bg=co1, fg=co0)
l_quantidade_total.place(x=545, y=95)


# funcao para mostrar
def mostrar():

    # creating a treeview with dual scrollbars
    tabela_head = ['#Item', 'Nome',  'Sala/Área', 'Descrição',
                   'Marca/Modelo', 'Data da compra', 'Valor da compra', 'Número de série']

    lista_itens = []

    global tree

    tree = ttk.Treeview(frameDireita, selectmode="extended",
                        columns=tabela_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(
        frameDireita, orient="vertical", command=tree.yview)
    # horizontal scrollbar
    hsb = ttk.Scrollbar(
        frameDireita, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    frameDireita.grid_rowconfigure(0, weight=12)

    hd = ["center", "center", "center", "center",
          "center", "center", "center", 'center']
    h = [40, 150, 100, 160, 130, 100, 100, 100]
    n = 0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n], anchor=hd[n])

        n += 1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

    quantidade = []
    for iten in lista_itens:
        quantidade.append(iten[6])

    Total_valor = sum(quantidade)
    Total_itens = len(quantidade)

    l_total['text'] = 'R$ {:,.2f}'.format(Total_valor)
    l_quantidade['text'] = Total_itens


mostrar()


janela.mainloop()
