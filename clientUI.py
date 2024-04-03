import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from socket import *


def connect_to_server():
    try:
        global client_socket
        servername = '10.234.107.110'  # 你的服务器主机名或IP地址
        serverport = 2525
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((servername, serverport))
    except Exception as e:
        update_chat_box(f"Connection Error: Unable to connect to server: {e}", "system")


def send_id():
    user_id = entry_id.get()
    if user_id:
        update_chat_box(f"Sending ID: {user_id}", "client")
        client_socket.send(user_id.encode())
        response = client_socket.recv(1024).decode()
        update_chat_box(response, "server")
        if response == "500 sp AUTH REQUIRED!":
            entry_id.config(state='disabled')
            button_send_id.config(state='disabled')
            entry_password.config(state='normal')
            button_send_password.config(state='normal')
        else:
            entry_id.config(state='disabled')
            button_send_id.config(state='disabled')


def send_password():
    user_password = entry_password.get()
    if user_password:
        update_chat_box("Sending Password", "client")
        client_socket.sendall(user_password.encode())
        response = client_socket.recv(1024).decode()
        update_chat_box(response, "server")
        if response == "525 OK!":
            entry_password.config(state='disabled')
            button_send_password.config(state='disabled')
            entry_withdraw.config(state='normal')
            button_send_withdraw.config(state='normal')
        else:
            entry_password.config(state='disabled')
            button_send_password.config(state='disabled')


def send_withdraw():
    user_withdraw = entry_withdraw.get()
    if user_withdraw:
        update_chat_box(f"Requesting Withdrawal: {user_withdraw}", "client")
        client_socket.sendall(user_withdraw.encode())
        response = client_socket.recv(1024).decode()
        update_chat_box(response, "server")
        if response <= user_withdraw:
            entry_withdraw.config(state='disabled')
            button_send_withdraw.config(state='disabled')
        else:
            entry_withdraw.config(state='disabled')
            button_send_withdraw.config(state='disabled')
            entry_over.config(state='normal')
            button_send_over.config(state='normal')


def send_over():
    user_over = entry_over.get()
    if user_over:
        update_chat_box(user_over, "client")
        client_socket.sendall(user_over.encode())
        response = client_socket.recv(1024).decode()
        update_chat_box(response, "server")
        entry_over.config(state='disabled')
        button_send_over.config(state='disabled')
        client_socket.close()


def update_chat_box(message, sender):
    chat_box.config(state='normal')
    if sender == "client":
        chat_box.insert(tk.END, "You: " + message + '\n\n', "client")
    elif sender == "server":
        chat_box.insert(tk.END, "Server: " + message + '\n\n', "server")
    else:
        chat_box.insert(tk.END, message + '\n\n', "system")
    chat_box.config(state='disabled')
    chat_box.see(tk.END)


root = tk.Tk()
root.title("ATM Client")

# Set a theme
style = ttk.Style(root)
style.theme_use("clam")

# Create a frame for the content
main_frame = ttk.Frame(root, padding=20)
main_frame.grid(row=0, column=0, sticky="nsew")

# Configure grid to expand with window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

label_id = ttk.Label(main_frame, text="Enter your ID:")
label_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")

entry_id = ttk.Entry(main_frame)
entry_id.grid(row=0, column=1, padx=5, pady=5)

button_send_id = ttk.Button(main_frame, text="Send ID", command=send_id)
button_send_id.grid(row=1, column=1, padx=5, pady=5)

label_password = ttk.Label(main_frame, text="Enter your password:")
label_password.grid(row=2, column=0, padx=5, pady=5, sticky="e")

entry_password = ttk.Entry(main_frame, show="*", state='disabled')
entry_password.grid(row=2, column=1, padx=5, pady=5)

button_send_password = ttk.Button(main_frame, text="Send Password", command=send_password, state='disabled')
button_send_password.grid(row=3, column=1, padx=5, pady=5)

label_withdraw = ttk.Label(main_frame, text="Enter withdraw amount:")
label_withdraw.grid(row=4, column=0, padx=5, pady=5, sticky="e")

entry_withdraw = ttk.Entry(main_frame, state='disabled')
entry_withdraw.grid(row=4, column=1, padx=5, pady=5)

button_send_withdraw = ttk.Button(main_frame, text="Withdraw", command=send_withdraw, state='disabled')
button_send_withdraw.grid(row=5, column=1, padx=5, pady=5)

label_over = ttk.Label(main_frame, text="Confirm or Cancel:")
label_over.grid(row=6, column=0, padx=5, pady=5, sticky="e")

entry_over = ttk.Entry(main_frame, state='disabled')
entry_over.grid(row=6, column=1, padx=5, pady=5)

button_send_over = ttk.Button(main_frame, text="Send", command=send_over, state='disabled')
button_send_over.grid(row=7, column=1, padx=5, pady=5)

chat_box = scrolledtext.ScrolledText(main_frame, state='disabled', width=40, height=10)
chat_box.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# 设置聊天框的标签样式
chat_box.tag_configure("client", background="#d9edf7", foreground="black")
chat_box.tag_configure("server", background="#f0f0f0", foreground="black")
chat_box.tag_configure("system", foreground="red")

connect_to_server()

root.mainloop()
