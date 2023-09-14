import pika
import tkinter as tk
import random

# Lista para armazenar as senhas
senhas_geradas = []

# Função para gerar senhas
def gerar_senha_preferencial():
    senha = f"Senha-P{random.randint(1, 100)}"
    senhas_geradas.append(senha)
    return senha

def gerar_senha_normal():
    senha = f"Senha-N{random.randint(1, 100)}"
    senhas_geradas.append(senha)
    return senha

# Função para enviar senha para a fila
def enviar_senha_para_fila(senha):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('ads', 'ads')))
    channel = connection.channel()
    
    if senha.startswith("Senha-P"):
        fila = 'fila_senhas_pref'
    else:
        fila = 'fila_senhas'

    channel.queue_declare(queue=fila, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=fila,
                          body=senha,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

    connection.close()

# Função para gerar senha e enviá-la para a fila
def gerar_e_enviar_senha():
    senha = gerar_senha_preferencial() if preferencial.get() else gerar_senha_normal()
    enviar_senha_para_fila(senha)
    senhas_geradas_text.config(state=tk.NORMAL)
    senhas_geradas_text.insert(tk.END, senha + '\n')
    senhas_geradas_text.config(state=tk.DISABLED)

# Interface gráfica
root = tk.Tk()
root.title("Geração de Senhas")
root.geometry("400x500")

preferencial = tk.BooleanVar()

senhas_geradas_text = tk.Text(root, state=tk.DISABLED)
senhas_geradas_text.pack()

preferencial_checkbox = tk.Checkbutton(root, text="Preferencial", variable=preferencial)
preferencial_checkbox.pack()

gerar_senha_button = tk.Button(root, text="Gerar Senha", command=gerar_e_enviar_senha)
gerar_senha_button.pack()

root.mainloop()