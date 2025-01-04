from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3
import time

banco = sqlite3.connect('meu_banco.db')
cursor = banco.cursor()   

def cadastro_dados(nome, id):
    global frame_atual
    global banco
    global cursor
    
    if not nome or not id:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    cursor.execute('SELECT * FROM usuarios WHERE id_cartao = ?', (id))
    if len(cursor.fetchall()):
        messagebox.showwarning("Erro", "Identificador já cadastradado no banco de dados!")
        return
    
    # Conexao do banco de dados
    cursor.execute("INSERT INTO  usuarios (id_cartao, nome) VALUES (?,?)", (id, nome)) 
    
    banco.commit()
    messagebox.showinfo("Sucesso", "Dados inseridos com sucesso no banco!")
 
def deleta_dados(id):
    global frame_atual
    global banco
    global cursor
    
    resposta = messagebox.askokcancel("Confirmação", "Deseja realmente deletar?")
    
    if resposta:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        banco.commit()
    else:
        print("Não deletado")
       
def cronometro(event):
    print(event.widget.get())
    
    cursor.execute('UPDATE usuarios SET tempo_chegada = ? WHERE id = ?', (time.time(), event.widget.get()))
    banco.commit()
    
    event.widget.delete(0, tk.END)
    
def on_enter(event):
    cronometro(event)

def consulta_geral():
    global banco
    global cursor
    
    cursor.execute("SELECT * from usuarios")
    itens = cursor.fetchall()

    return itens

def consulta_linha(event):
    global frame_atual
    
    dados =  event.widget.item(event.widget.selection())['values']
    id = dados[0]
    
    delete = lambda: deleta_dados(id)
    
    botao_delete = tk.Button(frame_atual, text="Deletar", command=delete)
    botao_delete.pack(pady=10)
    
 
def limpa_frame():
    global frame_atual
    
    # Se houver um frame ativo, destrua-o
    if frame_atual:
        frame_atual.destroy()
      
def tela_inicial():
    global frame_atual
    limpa_frame()

    # Cria o frame para a janela 1
    frame_atual = tk.Frame(root)
    frame_atual.pack(expand=True)

    # Adiciona widgets da Janela 1
    titulo = tk.Label(frame_atual, text="Trekking App", font=("Roboto", 25, "bold"))
    titulo.pack(pady=0)

    botao_tela_cadastro = tk.Button(frame_atual, text="Cadastro", command=tela_cadastro, font=("Roboto", 15))
    botao_tela_corrida = tk.Button(frame_atual, text="Corrida", command=tela_corrida, font=("Roboto", 15))
    botao_tela_consulta = tk.Button(frame_atual, text="Consultar", command=tela_consulta, font=("Roboto", 15))
    
    botao_tela_cadastro.pack(pady=5)
    botao_tela_corrida.pack(pady=5)
    botao_tela_consulta.pack(pady=5)

# Função para mudar para a Janela 2
def tela_cadastro():
    global frame_atual    
    limpa_frame()

    # Cria o frame para a janela 2
    frame_atual = tk.Frame(root)
    frame_atual.pack(expand=True)

    # Adiciona widgets da Janela 2
    titulo = tk.Label(frame_atual, text="Cadastro", font=("Roboto", 16, "bold"))
    titulo.pack(pady=0)

    label_nome = tk.Label(frame_atual, text="Nome do atleta:", font=("Roboto", 14))
    label_nome.pack(pady=5)
    
    caixa_nome = tk.Entry(frame_atual, font=("Roboto", 14))
    caixa_nome.pack(pady=0)
    
    label_id = tk.Label(frame_atual, text="Identificador do atleta:", font=("Roboto", 14))
    label_id.pack(pady=5)
    
    caixa_id = tk.Entry(frame_atual, font=("Roboto", 14))
    caixa_id.pack(pady=0)
        
   
    envia_dados = lambda: [cadastro_dados(nome=caixa_nome.get(), id=caixa_id.get()), caixa_id.delete(0,tk.END), caixa_nome.delete(0,tk.END)]
    
    botao_enviar = tk.Button(frame_atual, text="Enviar dados", command=envia_dados)
    botao_enviar.pack(pady=20)
    
    botao_voltar = tk.Button(frame_atual, text="Voltar para Janela 1", command=tela_inicial)
    botao_voltar.pack(pady=20)

def tela_corrida():
    global frame_atual
    limpa_frame()

    frame_atual = tk.Frame(root)
    frame_atual.pack(expand=True)
    
    titulo = tk.Label(frame_atual, text="Corrida", font=("Roboto", 16, "bold"))
    titulo.pack(pady=0)

    label_id = tk.Label(frame_atual, text="Identificador do atleta:", font=("Roboto", 14))
    label_id.pack(pady=5)
    
    caixa_id = tk.Entry(frame_atual, font=("Roboto", 14))
    caixa_id.bind("<Return>", cronometro)
    caixa_id.pack(pady=0)

    botao_voltar = tk.Button(frame_atual, text="Voltar para Janela 1", command=tela_inicial)
    botao_voltar.pack(pady=20)

def tela_consulta():
    global frame_atual
    global banco
    global cursor
    limpa_frame()
    
    itens = consulta_geral()
    
    frame_atual = tk.Frame(root)
    frame_atual.pack(expand=True)
    
    # Título da página de consulta
    titulo = tk.Label(frame_atual, text="Consulta", font=("Roboto", 16, "bold"))
    titulo.pack(pady=0)

    # Criação da tabela
    tabela = ttk.Treeview(frame_atual, columns=("Id_Cartao", "Nome", "Tempo_Partida", "Tempo_Chegada", "Tempo_Total"), show="headings")
    tabela.pack(pady=10)

    # Nome dos cabeçalhos
    tabela.heading("Nome", text="Nome")
    tabela.heading("Id_Cartao", text="Identificador")
    tabela.heading("Tempo_Partida", text="Partida")
    tabela.heading("Tempo_Chegada", text="Chegada")
    tabela.heading("Tempo_Total", text="Tempo entre os pontos")

    # Alinhamento das colunas    
    tabela.column("Nome", anchor=tk.CENTER, width=200) 
    tabela.column("Id_Cartao", anchor=tk.CENTER, width=85)  
    tabela.column("Tempo_Partida", anchor=tk.CENTER, width=100)  
    tabela.column("Tempo_Chegada", anchor=tk.CENTER, width=100)  
    tabela.column("Tempo_Total", anchor=tk.CENTER, width=150)  

    # Insere itens na lista
    for item in itens:
        tabela.insert("", tk.END, values=item[1:])
    
    tabela.bind("<ButtonRelease-1>", consulta_linha)
    
    # Botão de voltar
    botao_voltar = tk.Button(frame_atual, text="Voltar para Janela 1", command=tela_inicial)
    botao_voltar.pack(pady=20)
    
    
# Inicializa a janela principal (root)
root = tk.Tk()
root.title("Aplicação com Frames")
root.geometry("640x480")

# Variável global para controlar o frame atual
frame_atual = None

# Inicializa a Janela 1
tela_inicial()

# Inicia o loop principal
root.mainloop()
