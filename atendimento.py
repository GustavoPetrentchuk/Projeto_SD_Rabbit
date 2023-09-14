import pika
import tkinter as tk
from threading import Thread
import time

#Tags
called_tickets_label = None
preferred_called_tickets_label = None

def callback_normal(ch, method, properties, body):
    senha = body.decode()
    
    if not senha.startswith("Senha-P"):
        print(f"Atendimento: Chamando cliente: {senha}")
        update_gui_normal(senha)
    else:
        print(f"Atendimento: Chamando cliente (Preferencial): {senha}")
        update_gui_preferred(senha)
    
    time.sleep(5)  # Atraso de 5 segundos entre senhas
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_preferred(ch, method, properties, body):
    senha = body.decode()
    
    if senha.startswith("Senha-P"):
        print(f"Atendimento: Chamando cliente (Preferencial): {senha}")
        update_gui_preferred(senha)
        time.sleep(5)
    
def update_gui_normal(senha):
    called_tickets_label.config(text=f"Chamando: {senha}")

def update_gui_preferred(senha):
    preferred_called_tickets_label.config(text=f"Chamando (Preferencial): {senha}")

def consume_messages():
    time.sleep(5)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('ads', 'ads')))
    channel = connection.channel()

    channel.queue_declare(queue='fila_senhas', durable=True)
    channel.queue_declare(queue='fila_senhas_pref', durable=True)

    #Verifica a fila pref
    while True:
        method_frame, header_frame, body = channel.basic_get(queue='fila_senhas_pref')
        if body:
            senha = body.decode('utf-8')
            print(f"Atendimento: Chamando cliente (Preferencial): {senha}")
            update_gui_preferred(senha)
            time.sleep(5)
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        else:
            method_frame, header_frame, body = channel.basic_get(queue='fila_senhas')
            if body:
                senha = body.decode('utf-8')
                print(f"Atendimento: Chamando cliente: {senha}")
                update_gui_normal(senha)
                time.sleep(5)
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            else:
                print("Atendimento: Sem senhas para atender")
                time.sleep(5)

def main():
    root = tk.Tk()
    root.title("Atendimento")
    root.geometry("600x320")

    global called_tickets_label, preferred_called_tickets_label
    called_tickets_label = tk.Label(root, text="Chamando:")
    called_tickets_label.pack()

    preferred_called_tickets_label = tk.Label(root, text="Chamando (Preferencial):")
    preferred_called_tickets_label.pack()

    message_thread = Thread(target=consume_messages)
    message_thread.daemon = True
    message_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()