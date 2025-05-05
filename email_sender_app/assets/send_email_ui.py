import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from send_email import send_email_logic
from email_templates import list_templates, get_template
import os

class SendEmailUI:
    def __init__(self, master, user_id, contacts, user_email):
        self.master = master
        self.user_id = user_id
        self.user_email = user_email
        self.contacts = contacts  # List of tuples (name, email)
        self.selected_files = []
        self.selected_template = None

        self.window = tk.Toplevel(master)
        self.window.title("Enviar Correo")
        self.window.geometry("700x700")

        # Centrar ventana
        # Comentamos el centrado para evitar que la ventana se recorte en pantallas pequeñas
        self.center_window(700, 700)

        # Configurar grid para responsividad
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(11, weight=1)  # preview_text row

        # Mostrar correo del usuario
        tk.Label(self.window, text=f"Correo remitente: {self.user_email}").grid(row=0, column=0, sticky="w", padx=10, pady=(10,0))

        # Campo para ingresar contraseña
        tk.Label(self.window, text="Contraseña del correo:").grid(row=1, column=0, sticky="w", padx=10, pady=(10,0))
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Contactos
        tk.Label(self.window, text="Selecciona contactos:").grid(row=3, column=0, sticky="w", padx=10, pady=(10,0))
        self.contact_listbox = tk.Listbox(self.window, selectmode=tk.MULTIPLE)
        self.contact_listbox.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, f"{contact.get('name', '')} - {contact.get('email', '')}")

        # Archivos adjuntos
        tk.Label(self.window, text="Archivos adjuntos:").grid(row=5, column=0, sticky="w", padx=10, pady=(10,0))
        self.attach_button = tk.Button(self.window, text="Seleccionar archivos", command=self.select_files)
        self.attach_button.grid(row=6, column=0, sticky="ew", padx=10, pady=5)
        self.attach_label = tk.Label(self.window, text="No hay archivos seleccionados")
        self.attach_label.grid(row=7, column=0, sticky="w", padx=10)

        # Plantillas
        tk.Label(self.window, text="Selecciona plantilla:").grid(row=8, column=0, sticky="w", padx=10, pady=(10,0))
        self.templates = list_templates(self.user_id)
        self.template_var = tk.StringVar()
        if self.templates:
            self.template_var.set(self.templates[0][0])  # Set default to first template name
        self.template_menu = tk.OptionMenu(self.window, self.template_var, *[tpl[0] for tpl in self.templates], command=self.update_preview)
        self.template_menu.grid(row=9, column=0, sticky="ew", padx=10, pady=5)

        # Vista previa
        tk.Label(self.window, text="Vista previa del correo:").grid(row=10, column=0, sticky="w", padx=10, pady=(10,0))
        self.preview_text = scrolledtext.ScrolledText(self.window, height=15)
        self.preview_text.grid(row=11, column=0, sticky="nsew", padx=10, pady=5)
        self.preview_text.config(state=tk.DISABLED)

        # Barra de progreso
        self.progress = ttk.Progressbar(self.window, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=12, column=0, sticky="ew", padx=10, pady=(0,10))

        # Botón enviar
        self.send_button = tk.Button(self.window, text="Enviar", command=self.send_email)
        self.send_button.grid(row=13, column=0, sticky="ew", padx=10, pady=10)

    def center_window(self, width, height):
        # Obtener dimensiones de la pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        # Calcular posición x, y para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def select_files(self):
        files = filedialog.askopenfilenames(title="Seleccionar archivos")
        if files:
            self.selected_files = list(files)
            filenames = [os.path.basename(f) for f in self.selected_files]
            self.attach_label.config(text=", ".join(filenames))
        else:
            self.selected_files = []
            self.attach_label.config(text="No hay archivos seleccionados")

    def show_variables_help(self):
        help_window = tk.Toplevel(self.window)
        help_window.title("Variables disponibles")
        help_window.geometry("300x250")
        help_window.transient(self.window)
        help_window.grab_set()

        help_text = (
            "Variables disponibles para plantillas:\n\n"
            "[Nombre contacto] - Nombre del contacto seleccionado\n"
            "[Email contacto] - Email del contacto seleccionado\n"
            "[Documento1], [Documento2], ... - Nombres de archivos adjuntos\n"
            "[Saludo] - Saludo según la hora del día (buenos días, buenas tardes, buenas noches)\n"
            "\nUsa estas variables entre corchetes en tus plantillas para personalizar los correos."
        )

        label = tk.Label(help_window, text=help_text, justify="left", padx=10, pady=10)
        label.pack(fill=tk.BOTH, expand=True)

        close_button = tk.Button(help_window, text="Cerrar", command=help_window.destroy)
        close_button.pack(pady=10)

    def update_preview(self, selected_template_name):
        import re
        from email_templates import get_template

        if not selected_template_name:
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert(tk.END, "No hay plantilla seleccionada")
            self.preview_text.config(state=tk.DISABLED)
            return

        # Obtener contenido de la plantilla real
        subject, template_content = get_template(self.user_id, selected_template_name)

        # Obtener primer contacto seleccionado para vista previa
        selected_indices = self.contact_listbox.curselection()
        if not selected_indices:
            preview_text = "Seleccione al menos un contacto para vista previa."
        else:
            first_contact = self.contacts[selected_indices[0]]

            # Diccionario de variables para reemplazo
            variables = {
                "Nombre contacto": first_contact.get("name", ""),
                "Email contacto": first_contact.get("email", ""),
                "Saludo": self.saludo()
            }

            # Agregar nombres de archivos adjuntos si hay
            if self.selected_files:
                for i, filepath in enumerate(self.selected_files, start=1):
                    filename = os.path.basename(filepath)
                    filename_no_ext = os.path.splitext(filename)[0]
                    variables[f"Documento{i}"] = filename_no_ext
            else:
                variables["Documento1"] = "[Sin archivos adjuntos]"

            # Función para reemplazar variables en formato [Variable]
            def replace_var(match):
                var_name = match.group(1)
                var_name_key = var_name.strip().capitalize()
                value = variables.get(var_name_key, f"[{var_name}]")
                if var_name_key == "Saludo":
                    value = value.lower()
                if value == f"[{var_name}]":
                    value = variables.get(var_name.strip().lower(), value)
                return value

            # Reemplazar variables en el contenido
            preview_text = re.sub(r"\[([^\]]+)\]", replace_var, template_content)

        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, preview_text)
        self.preview_text.config(state=tk.DISABLED)

    def send_email(self):
        from email_templates import get_template

        selected_indices = self.contact_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Advertencia", "Seleccione al menos un contacto para enviar el correo.")
            return
        selected_contacts = [self.contacts[i] for i in selected_indices]

        template_name = self.template_var.get()
        if not template_name:
            messagebox.showwarning("Advertencia", "Seleccione una plantilla para enviar el correo.")
            return

        # Obtener contenido real de la plantilla
        subject, template_content = get_template(self.user_id, template_name)

        # Preparar datos para enviar
        recipients = [c.get("email", "") for c in selected_contacts]

        # Obtener contraseña ingresada
        sender_password = self.password_entry.get()
        if not sender_password:
            messagebox.showwarning("Advertencia", "Ingrese la contraseña del correo remitente.")
            return

        # Reemplazar variables en el contenido de la plantilla para cada contacto
        personalized_contents = []
        for contact in selected_contacts:
            content = template_content
            variables = {
                "Nombre contacto": contact.get("name", ""),
                "Email contacto": contact.get("email", ""),
                "Saludo": self.saludo()  # Lowercase greeting
            }
            if self.selected_files:
                for i, filepath in enumerate(self.selected_files, start=1):
                    filename = os.path.basename(filepath)
                    filename_no_ext = os.path.splitext(filename)[0]
                    variables[f"Documento{i}"] = filename_no_ext
            else:
                variables["Documento1"] = "[Sin archivos adjuntos]"

            import re
            def replace_var(match):
                var_name = match.group(1)
                var_name_clean = var_name.strip()
                var_name_key = var_name_clean.capitalize()
                value = variables.get(var_name_key, f"[{var_name}]")
                if var_name_key == "Saludo":
                    value = value.lower()
                if value == f"[{var_name}]":
                    value = variables.get(var_name_clean.lower(), value)
                return value

            personalized_content = re.sub(r"\[([^\]]+)\]", replace_var, content)
            personalized_contents.append(personalized_content)

        # Enviar correos personalizados uno por uno
        all_success = True
        errors = []
        for i, (recipient, content) in enumerate(zip(recipients, personalized_contents), start=1):
            self.progress['value'] = i
            self.window.update_idletasks()
            success, error = send_email_logic([recipient], content, self.selected_files, sender_email=self.user_email, sender_password=sender_password)
            if not success:
                all_success = False
                errors.append(f"{recipient}: {error}")

        if all_success:
            messagebox.showinfo("Éxito", "Correos enviados correctamente.")
            self.window.destroy()
        else:
            import traceback
            detailed_error = traceback.format_exc()
            messagebox.showerror("Error", f"No se pudieron enviar algunos correos:\n{chr(10).join(errors)}\nDetalles: {detailed_error}")

    def edit_template(self):
        messagebox.showinfo("Editar plantilla", "Funcionalidad de editar plantilla no implementada aún.")

    def delete_template(self):
        messagebox.showinfo("Borrar plantilla", "Funcionalidad de borrar plantilla no implementada aún.")
