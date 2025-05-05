import tkinter as tk
from tkinter import messagebox
from assets.template_manager_ui import TemplateManagerUI
from email_templates import connect_db
from assets.login_ui import show_login_window

import tkinter as tk
from tkinter import messagebox
from assets.template_manager_ui import TemplateManagerUI
from assets.login_ui import show_login_window
from app import login_user

class MainInterface:
    def __init__(self, master, user_id, user_email, login_user_callback):
        self.master = master
        self.user_id = user_id
        self.user_email = user_email
        self.login_user_callback = login_user_callback
        master.title("Interfaz Principal - Envío de Correos")
        master.geometry("400x400")
        master.minsize(600, 600)
        master.configure(bg="#f5f5f5")

        # Centrar ventana
        self.center_window(master)

        # Configurar grid para responsividad
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(5, weight=1)
        master.grid_rowconfigure(6, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(2, weight=1)

        # Frame central para contenido
        content_frame = tk.Frame(master, bg="#f5f5f5")
        content_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)

        # Obtener username desde la base de datos
        print(f"DEBUG: user_id in main_interface: {self.user_id}")  # Debug print
        username = self.user_email  # Valor por defecto si no se encuentra en DB
        db = connect_db()
        if db is not None:
            try:
                cursor = db.cursor()
                cursor.execute("SELECT username FROM users WHERE id = %s", (self.user_id,))
                row = cursor.fetchone()
                print(f"DEBUG: username query result: {row}")  # Debug print
                if row:
                    username = row[0]
                cursor.close()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo obtener el nombre de usuario: {e}")
            finally:
                db.close()

        label = tk.Label(content_frame, text=f"Bienvenido {username} a la aplicación de envío de correos", bg="#f5f5f5", font=("Helvetica", 12))
        label.grid(row=0, column=0, pady=(0, 20))

        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#3498db",
            "fg": "#ffffff",
            "bd": 0,
            "relief": "flat",
            "activebackground": "#2980b9",
            "activeforeground": "#ffffff",
            "width": 20,
            "height": 2,
        }

        self.contact_button = tk.Button(content_frame, text="Gestionar Contactos", command=self.manage_contacts, **button_style)
        self.contact_button.grid(row=1, column=0, pady=5, sticky="ew")

        self.template_button = tk.Button(content_frame, text="Seleccionar Plantilla", command=self.select_template, **button_style)
        self.template_button.grid(row=2, column=0, pady=5, sticky="ew")

        self.send_button = tk.Button(content_frame, text="Enviar Correo", command=self.send_email, **button_style)
        self.send_button.grid(row=3, column=0, pady=5, sticky="ew")

        self.config_button = tk.Button(content_frame, text="Configurar Cuenta", command=self.configure_account, **button_style)
        self.config_button.grid(row=4, column=0, pady=5, sticky="ew")

        logout_button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#95a5a6",
            "fg": "#ffffff",
            "bd": 0,
            "relief": "flat",
            "activebackground": "#7f8c8d",
            "activeforeground": "#ffffff",
            "width": 20,
            "height": 2,
        }

        self.logout_button = tk.Button(content_frame, text="Cerrar Sesión", command=self.logout, **logout_button_style)
        self.logout_button.grid(row=5, column=0, pady=5, sticky="ew")

    def manage_contacts(self):
        from contact_manager import show_contact_manager
        show_contact_manager(self.master, self.user_id)

    def select_template(self):
        TemplateManagerUI(self.master, self.user_id)

    def send_email(self):
        from assets.send_email_ui import SendEmailUI
        from contact_manager import connect_db

        # Cargar contactos para el usuario
        db = connect_db()
        if db is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos para cargar contactos.")
            return
        cursor = db.cursor()
        cursor.execute("SELECT name, email FROM contacts WHERE user_id = %s", (self.user_id,))
        contacts = cursor.fetchall()
        cursor.close()
        db.close()

        SendEmailUI(self.master, self.user_id, contacts, self.user_email)

    def configure_account(self):
        print(f"DEBUG: configure_account called with user_id: {self.user_id}")  # Debug print
        from assets.configuration_ui import ConfigurationUI
        ConfigurationUI(self.master, self.user_id)

    def logout(self):
        self.master.destroy()
        from assets.login_ui import show_login_window
        from app import login_user
        show_login_window(login_user)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

def show_main_interface(user_id, user_email, login_user_callback):
    root = tk.Tk()
    main_interface = MainInterface(root, user_id, user_email, login_user_callback)
    root.mainloop()
