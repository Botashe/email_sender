import tkinter as tk
from tkinter import messagebox

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_register_window(register_user_callback):
    register_window = tk.Toplevel()
    register_window.title("Registro de Usuario")
    register_window.geometry("400x500")
    register_window.configure(bg="#f5f5f5")

    # Fuente y colores
    font_label = ("Helvetica", 12)
    font_entry = ("Helvetica", 12)
    font_button = ("Helvetica", 12, "bold")
    color_bg = "#f5f5f5"
    color_fg = "#333333"
    color_error = "#e74c3c"
    color_button_bg = "#3498db"
    color_button_fg = "#ffffff"

    # Layout grid configuración
    register_window.grid_rowconfigure(0, weight=1)
    register_window.grid_rowconfigure(15, weight=1)
    register_window.grid_columnconfigure(0, weight=1)
    register_window.grid_columnconfigure(2, weight=1)

    # Nombre de usuario
    label_user = tk.Label(register_window, text="Nombre de usuario:", font=font_label, bg=color_bg, fg=color_fg)
    label_user.grid(row=1, column=1, sticky="w", padx=20, pady=(10, 3))

    username_entry = tk.Entry(register_window, font=font_entry, bd=1, relief="solid")
    username_entry.grid(row=2, column=1, sticky="ew", padx=20)

    username_error = tk.Label(register_window, text="", fg=color_error, bg=color_bg, font=("Helvetica", 10))
    username_error.grid(row=3, column=1, sticky="w", padx=20, pady=(1, 5))

    # Email
    label_email = tk.Label(register_window, text="Email:", font=font_label, bg=color_bg, fg=color_fg)
    label_email.grid(row=4, column=1, sticky="w", padx=20, pady=(8, 3))

    email_entry = tk.Entry(register_window, font=font_entry, bd=1, relief="solid")
    email_entry.grid(row=5, column=1, sticky="ew", padx=20)

    email_error = tk.Label(register_window, text="", fg=color_error, bg=color_bg, font=("Helvetica", 10))
    email_error.grid(row=6, column=1, sticky="w", padx=20, pady=(1, 5))

    # Contraseña
    label_pass = tk.Label(register_window, text="Contraseña:", font=font_label, bg=color_bg, fg=color_fg)
    label_pass.grid(row=7, column=1, sticky="w", padx=20, pady=(8, 3))

    password_entry = tk.Entry(register_window, font=font_entry, bd=1, relief="solid", show="*")
    password_entry.grid(row=8, column=1, sticky="ew", padx=20)

    password_error = tk.Label(register_window, text="", fg=color_error, bg=color_bg, font=("Helvetica", 10))
    password_error.grid(row=9, column=1, sticky="w", padx=20, pady=(1, 5))

    # Confirmar contraseña
    label_confirm = tk.Label(register_window, text="Confirmar Contraseña:", font=font_label, bg=color_bg, fg=color_fg)
    label_confirm.grid(row=10, column=1, sticky="w", padx=20, pady=(8, 3))

    confirm_entry = tk.Entry(register_window, font=font_entry, bd=1, relief="solid", show="*")
    confirm_entry.grid(row=11, column=1, sticky="ew", padx=20)

    confirm_error = tk.Label(register_window, text="", fg=color_error, bg=color_bg, font=("Helvetica", 10))
    confirm_error.grid(row=12, column=1, sticky="w", padx=20, pady=(1, 5))

    # Fortaleza de contraseña
    strength_frame = tk.Frame(register_window, bg=color_bg)
    strength_frame.grid(row=13, column=1, sticky="w", padx=20, pady=(10, 5))
    tk.Label(strength_frame, text="Fortaleza:", bg=color_bg, fg=color_fg, font=font_label).pack(side=tk.LEFT)
    strength_bar = tk.Label(strength_frame, text="    ", bg="red", width=10)
    strength_bar.pack(side=tk.LEFT, padx=5)
    strength_text = tk.Label(strength_frame, text="Débil", bg=color_bg, fg=color_fg, font=("Helvetica", 10))
    strength_text.pack(side=tk.LEFT)

    def update_strength(event):
        password = password_entry.get()
        strength = 0
        
        if len(password) >= 8: strength += 1
        if any(c.isdigit() for c in password): strength += 1
        if any(c.isupper() for c in password): strength += 1
        if any(c in "!@#$%^&*" for c in password): strength += 1
        
        if strength == 0:
            strength_bar.config(bg="red")
            strength_text.config(text="Débil")
        elif strength <= 2:
            strength_bar.config(bg="orange")
            strength_text.config(text="Media")
        else:
            strength_bar.config(bg="green")
            strength_text.config(text="Fuerte")

    password_entry.bind("<KeyRelease>", update_strength)

    def validate_username(event):
        if not username_entry.get():
            username_error.config(text="El nombre de usuario es obligatorio")
        else:
            username_error.config(text="")

    def validate_email(event):
        email = email_entry.get()
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            email_error.config(text="El email es obligatorio")
        elif not re.match(pattern, email):
            email_error.config(text="Email inválido")
        else:
            email_error.config(text="")

    def validate_password(event):
        pwd = password_entry.get()
        if not pwd:
            password_error.config(text="La contraseña es obligatoria")
        elif len(pwd) < 8:
            password_error.config(text="La contraseña debe tener al menos 8 caracteres")
        else:
            password_error.config(text="")

    def validate_confirm(event):
        if confirm_entry.get() != password_entry.get():
            confirm_error.config(text="Las contraseñas no coinciden")
        else:
            confirm_error.config(text="")

    username_entry.bind("<KeyRelease>", validate_username)
    email_entry.bind("<KeyRelease>", validate_email)
    password_entry.bind("<KeyRelease>", validate_password)
    confirm_entry.bind("<KeyRelease>", validate_confirm)

    def on_register():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_entry.get()
        if not username or not email or not password or not confirm_password:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
            return
        if username_error.cget("text") or email_error.cget("text") or password_error.cget("text") or confirm_error.cget("text"):
            messagebox.showwarning("Advertencia", "Por favor corrija los errores antes de continuar")
            return
        register_user_callback(username, email, password, confirm_password, register_window)

    register_button = tk.Button(register_window, text="Registrar", font=font_button, bg=color_button_bg, fg=color_button_fg, bd=0, relief="flat", command=on_register)
    register_button.grid(row=14, column=1, sticky="ew", padx=20, pady=20)

    center_window(register_window)
    register_window.mainloop()
