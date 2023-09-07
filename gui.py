import tkinter as tk
from tkinter import scrolledtext

class ChatGUI:
    def __init__(self, role, send_callback):
        self.window = tk.Tk()
        self.window.title(role)
        self.send_callback = send_callback

        self.chat_box = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=50, height=15)
        self.chat_box.pack(pady=10)
        self.chat_box.config(state=tk.DISABLED)

        self.entry = tk.Entry(self.window, width=50)
        self.entry.pack(pady=10)

        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

    def run(self):
        self.window.mainloop()

    def send_message(self):
        message = self.entry.get()
        self.entry.delete(0, tk.END)
        self.send_callback(message)

    def display_received_message(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, message + '\n')
        self.chat_box.config(state=tk.DISABLED)
