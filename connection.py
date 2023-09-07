import hashlib
import socket
import threading
import time
from tkinter import Tk, Frame, Text, Entry, Button, Scrollbar, INSERT, END

from encryption import encrypt_message, decrypt_message
from key_exchange import generate_key_pair, derive_shared_key


def key_update(client_socket, shared_key, role):
    while True:
        time.sleep(600)  # Update key every 10 minutes
        # Derive a new shared key using the existing shared key
        new_shared_key = hashlib.sha256(shared_key[0]).digest()

        shared_key[0] = new_shared_key
        #print(f"{role}: new shared_key: ", shared_key[0])


def on_send_click(entry, text_widget, client_socket, shared_key):
    message = entry.get()
    entry.delete(0, END)
    encrypted_message = encrypt_message(message, shared_key[0])
    #print("encrypted sent: ", encrypted_message)
    client_socket.send(encrypted_message)

    text_widget.configure(state="normal")
    text_widget.insert(INSERT, f"You: {message}\n")
    text_widget.configure(state="disabled")


def receive_messages(client_socket, shared_key, text_widget):
    while True:
        data = client_socket.recv(4096)
        #print("encrypted received: ", data)
        if not data: break
        decrypted_message = decrypt_message(data, shared_key[0])
        #print("decrypted message: ", decrypted_message)
        text_widget.configure(state="normal")
        text_widget.insert(INSERT, f"Received: {decrypted_message}\n")
        text_widget.configure(state="disabled")


def create_gui(title, shared_key, client_socket):
    root = Tk()
    root.title(title)

    frame = Frame(root)
    scrollbar = Scrollbar(frame)
    text_widget = Text(frame, wrap="word", yscrollcommand=scrollbar.set, state="disabled")
    scrollbar.config(command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")
    text_widget.pack(side="left", fill="both", expand=True)
    frame.pack(fill="both", expand=True)

    entry = Entry(root)
    entry.pack(fill="x", expand=True)

    send_button = Button(root, text="Send", command=lambda: on_send_click(entry, text_widget, client_socket, shared_key))
    send_button.pack(side="right")

    return root, text_widget


def server(ip_address, port_num):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port_num))
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()
    print("Connection from:", addr)

    # Key exchange
    server_key_pair = generate_key_pair()
    server_pubkey = server_key_pair.gen_public_key()
    client_socket.send(server_pubkey.to_bytes(4096, 'big'))
    client_pubkey_bytes = client_socket.recv(4096)
    client_pubkey = int.from_bytes(client_pubkey_bytes, 'big')

    shared_key = [derive_shared_key(server_key_pair, client_pubkey)]

    root, text_widget = create_gui("Server", shared_key, client_socket)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, shared_key, text_widget))
    key_update_thread = threading.Thread(target=key_update, args=(client_socket, shared_key, "Server"))

    receive_thread.start()
    key_update_thread.start()

    root.mainloop()

    receive_thread.join()
    key_update_thread.join()

    client_socket.close()


def client(ip_address, port_num):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port_num))

    # Key exchange
    client_key_pair = generate_key_pair()
    client_pubkey = client_key_pair.gen_public_key()
    server_pubkey_bytes = client_socket.recv(4096)
    server_pubkey = int.from_bytes(server_pubkey_bytes, 'big')
    client_socket.send(client_pubkey.to_bytes(4096, 'big'))

    shared_key = [derive_shared_key(client_key_pair, server_pubkey)]

    root, text_widget = create_gui("Client", shared_key, client_socket)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, shared_key, text_widget))
    key_update_thread = threading.Thread(target=key_update, args=(client_socket, shared_key, "Client"))

    receive_thread.start()
    key_update_thread.start()

    root.mainloop()

    receive_thread.join()
    key_update_thread.join()

    client_socket.close()

