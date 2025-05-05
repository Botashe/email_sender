import tkinter as tk
from tkinter import messagebox
from register import show_register_window

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_login_window(login_user_callback):
    root = tk.Tk()
    root.title("Email Sender - Login")
    root.geometry("400x400")
    root.configure(bg="#f5f5f5")

    # Fuente y colores
    font_label = ("Helvetica", 12)
    font_entry = ("Helvetica", 12)
    font_button = ("Helvetica", 12, "bold")
    color_bg = "#f5f5f5"
    color_fg = "#333333"
    color_error = "#e74c3c"
    color_button_bg = "#3498db"
    color_button_fg = "#ffffff"

    # Configurar grid para responsividad
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(9, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)

    # Frame central para contenido
    content_frame = tk.Frame(root, bg=color_bg)
    content_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
    content_frame.grid_columnconfigure(0, weight=1)

    # Etiqueta Usuario o Email
    label_user = tk.Label(content_frame, text="Usuario o Email:", font=font_label, bg=color_bg, fg=color_fg)
    label_user.grid(row=0, column=0, sticky="w", pady=(0, 5))

    username_entry = tk.Entry(content_frame, font=font_entry, bd=1, relief="solid")
    username_entry.grid(row=1, column=0, sticky="ew")

    username_error = tk.Label(content_frame, text="", fg=color_error, bg=color_bg, font=("Helvetica", 10))
    username_error.grid(row=2, column=0, sticky="w", pady=(2, 10))

    # Etiqueta Contraseña
    label_pass = tk.Label(content_frame, text="Contraseña:", font=font_label, bg=color_bg, fg=color_fg)
    label_pass.grid(row=3, column=0, sticky="w", pady=(0, 5))

    password_entry = tk.Entry(content_frame, font=font_entry, bd=1, relief="solid", show="*")
    password_entry.grid(row=4, column=0, sticky="ew")

    password_error = tk.Label(content_frame, text="", fg=color_error, bg=color_bg, font=("Helvetica", 10))
    password_error.grid(row=5, column=0, sticky="w", pady=(2, 10))

    def validate_username(event):
        if not username_entry.get():
            username_error.config(text="El usuario o email es obligatorio")
        else:
            username_error.config(text="")

    def validate_password(event):
        pwd = password_entry.get()
        if not pwd:
            password_error.config(text="La contraseña es obligatoria")
        elif len(pwd) < 8:
            password_error.config(text="La contraseña debe tener al menos 8 caracteres")
        else:
            password_error.config(text="")

    username_entry.bind("<KeyRelease>", validate_username)
    password_entry.bind("<KeyRelease>", validate_password)

    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
            return
        login_user_callback(username, password, root)

    login_button = tk.Button(content_frame, text="Iniciar Sesión", font=font_button, bg=color_button_bg, fg=color_button_fg, bd=0, relief="flat", command=on_login)
    login_button.grid(row=6, column=0, sticky="ew", pady=(10, 5))

    register_button = tk.Button(content_frame, text="Registrarse", font=font_button, bg="#95a5a6", fg=color_button_fg, bd=0, relief="flat", command=show_register_window)
    register_button.grid(row=7, column=0, sticky="ew")

    # Set focus on username entry
    username_entry.focus_set()

    center_window(root)
    root.mainloop()
