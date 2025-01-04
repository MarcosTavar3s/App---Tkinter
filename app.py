from tkinter import messagebox
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

    # Conexao do banco de dados
    cursor.execute("INSERT INTO  usuarios (id_cartao, nome) VALUES (?,?)", (id, nome)) 
    
    banco.commit()
    messagebox.showinfo("Sucesso", "Dados inseridos com sucesso no banco!")
    
def cronometro(event):
    print(event.widget.get())
    
    cursor.execute('UPDATE usuarios SET tempo_chegada = ? WHERE id = ?', (time.time(), event.widget.get()))
    banco.commit()
    
    event.widget.delete(0, tk.END)
    
def on_enter(event):
    cronometro(event)
    
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
    
    cursor.execute("SELECT * from usuarios")
    itens = cursor.fetchall()
    
    frame_atual = tk.Frame(root)
    frame_atual.pack(expand=True)
    
    titulo = tk.Label(frame_atual, text="Consulta", font=("Roboto", 16, "bold"))
    titulo.pack(pady=0)

    lista = tk.Listbox(frame_atual, height=10)
    lista.pack(pady=5)
    
    for item in itens:
        lista.insert(tk.END, item[2])

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
