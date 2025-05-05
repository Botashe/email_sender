import tkinter as tk
from tkinter import messagebox
from configuration import get_user_configuration, update_user_configuration

class ConfigurationUI:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        self.window = tk.Toplevel(parent)
        self.window.title("Configuración de Cuenta")
        self.window.geometry("500x500")
        self.window.minsize(400, 400)
        self.window.configure(bg="#f5f5f5")
        self.window.grab_set()

        self.center_window()

        self.create_widgets()
        self.load_configuration()

        # Configurar grid para responsividad
        for i in range(10):
            self.window.grid_rowconfigure(i, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=2)

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        label_style = {"bg": "#f5f5f5", "font": ("Helvetica", 11)}
        entry_style = {"font": ("Helvetica", 11)}

        # Campos para username y email
        tk.Label(self.window, text="Usuario:", **label_style).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.username_entry = tk.Entry(self.window, **entry_style)
        self.username_entry.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=10)

        tk.Label(self.window, text="Correo:", **label_style).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.email_entry = tk.Entry(self.window, **entry_style)
        self.email_entry.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=10)

        # Campos para cambio de contraseña
        tk.Label(self.window, text="Contraseña actual:", **label_style).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.current_password_entry = tk.Entry(self.window, show="*", **entry_style)
        self.current_password_entry.grid(row=2, column=1, sticky=tk.EW, padx=10, pady=10)

        tk.Label(self.window, text="Nueva contraseña:", **label_style).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.new_password_entry = tk.Entry(self.window, show="*", **entry_style)
        self.new_password_entry.grid(row=3, column=1, sticky=tk.EW, padx=10, pady=10)

        tk.Label(self.window, text="Confirmar nueva contraseña:", **label_style).grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        self.confirm_password_entry = tk.Entry(self.window, show="*", **entry_style)
        self.confirm_password_entry.grid(row=4, column=1, sticky=tk.EW, padx=10, pady=10)

        tk.Label(self.window, text="Teléfono:", **label_style).grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        self.phone_entry = tk.Entry(self.window, **entry_style)
        self.phone_entry.grid(row=5, column=1, sticky=tk.EW, padx=10, pady=10)

        tk.Label(self.window, text="Dirección:", **label_style).grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
        self.address_entry = tk.Entry(self.window, **entry_style)
        self.address_entry.grid(row=6, column=1, sticky=tk.EW, padx=10, pady=10)

        tk.Label(self.window, text="Firma:", **label_style).grid(row=7, column=0, sticky=tk.NW, padx=10, pady=10)
        self.signature_text = tk.Text(self.window, height=5, width=30, font=("Helvetica", 11))
        self.signature_text.grid(row=7, column=1, sticky=tk.EW, padx=10, pady=10)

        tk.Label(self.window, text="Idioma:", **label_style).grid(row=8, column=0, sticky=tk.W, padx=10, pady=10)
        self.language_entry = tk.Entry(self.window, **entry_style)
        self.language_entry.grid(row=8, column=1, sticky=tk.EW, padx=10, pady=10)

        self.save_button = tk.Button(self.window, text="Guardar", command=self.save_configuration, bg="#3498db", fg="#ffffff", font=("Helvetica", 12, "bold"), bd=0, relief="flat", activebackground="#2980b9", activeforeground="#ffffff")
        self.save_button.grid(row=9, column=0, columnspan=2, pady=20, sticky="ew")

    def load_configuration(self):
        config = get_user_configuration(self.user_id)
        if config:
            self.username_entry.delete(0, tk.END)
            if config.get("username"):
                self.username_entry.insert(0, config["username"])
            self.email_entry.delete(0, tk.END)
            if config.get("email"):
                self.email_entry.insert(0, config["email"])
            self.current_password_entry.delete(0, tk.END)
            self.new_password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            if config.get("phone"):
                self.phone_entry.insert(0, config["phone"])
            self.address_entry.delete(0, tk.END)
            if config.get("address"):
                self.address_entry.insert(0, config["address"])
            self.signature_text.delete("1.0", tk.END)
            if config.get("signature"):
                self.signature_text.insert(tk.END, config["signature"])
            self.language_entry.delete(0, tk.END)
            if config.get("language"):
                self.language_entry.insert(0, config["language"])

    def save_configuration(self):
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        signature = self.signature_text.get("1.0", tk.END).strip()
        language = self.language_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validar cambio de contraseña
        current_password = self.current_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if new_password or confirm_password or current_password:
            if not current_password:
                messagebox.showerror("Error", "Debe ingresar la contraseña actual para cambiarla.")
                return
            if new_password != confirm_password:
                messagebox.showerror("Error", "La nueva contraseña y su confirmación no coinciden.")
                return
            from configuration import change_user_password
            success, msg = change_user_password(self.user_id, current_password, new_password)
            if not success:
                messagebox.showerror("Error", msg)
                return
            else:
                messagebox.showinfo("Éxito", msg)

        success = update_user_configuration(self.user_id, username, email, phone, address, signature, language)
        if success:
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la configuración.")
