import tkinter as tk
from tkinter import messagebox

class ContactManagerUI:
    def __init__(self, parent, user_id, load_contacts_callback):
        self.parent = parent
        self.user_id = user_id
        self.load_contacts_callback = load_contacts_callback
        self.contacts = []  # Initialize contacts list to avoid attribute error
        self.sort_mode = "asc"  # Initialize sort_mode to default

        self.window = parent  # Use the passed parent window directly
        self.window.title("Gestión de Contactos")
        self.window.geometry("400x400")

        self.center_window()

        self.label = tk.Label(self.window, text="Lista de Contactos")
        self.label.pack(pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_filter)
        self.search_entry = tk.Entry(self.window, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=5, pady=(5, 5))

        self.sort_var = tk.StringVar(value="Ordenar A-Z")
        self.sort_menu_btn = tk.Menubutton(self.window, text="🔽 Ordenar", relief=tk.RAISED)
        self.sort_menu = tk.Menu(self.sort_menu_btn, tearoff=0)
        self.sort_menu.add_radiobutton(label="Ordenar A-Z", variable=self.sort_var, command=lambda: self.set_sort("asc"))
        self.sort_menu.add_radiobutton(label="Ordenar Z-A", variable=self.sort_var, command=lambda: self.set_sort("desc"))
        self.sort_menu.add_separator()
        self.sort_menu.add_radiobutton(label="Ordenar por Nombre A-Z", variable=self.sort_var, command=lambda: self.set_sort("name_asc"))
        self.sort_menu.add_radiobutton(label="Ordenar por Nombre Z-A", variable=self.sort_var, command=lambda: self.set_sort("name_desc"))
        self.sort_menu.add_separator()
        self.sort_menu.add_radiobutton(label="Ordenar por Email A-Z", variable=self.sort_var, command=lambda: self.set_sort("email_asc"))
        self.sort_menu.add_radiobutton(label="Ordenar por Email Z-A", variable=self.sort_var, command=lambda: self.set_sort("email_desc"))
        self.sort_menu.add_separator()
        self.sort_menu.add_radiobutton(label="Ordenar por Fecha Reciente", variable=self.sort_var, command=lambda: self.set_sort("date_desc"))
        self.sort_menu.add_radiobutton(label="Ordenar por Fecha Más Antigua", variable=self.sort_var, command=lambda: self.set_sort("date_asc"))
        self.sort_menu_btn.config(menu=self.sort_menu)
        self.sort_menu_btn.pack(fill=tk.X, padx=5, pady=(5, 5))

        self.contact_listbox = tk.Listbox(self.window)
        self.contact_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=5, fill=tk.X)

        self.add_button = tk.Button(btn_frame, text="Agregar Contacto", command=self.add_contact)
        self.add_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.edit_button = tk.Button(btn_frame, text="Editar Contacto", command=self.edit_contact)
        self.edit_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.delete_button = tk.Button(btn_frame, text="Eliminar Contacto", command=self.delete_contact)
        self.delete_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.load_contacts()

    def center_window(self, window=None):
        if window is None:
            window = self.window
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def add_contact(self):
        def save_contact():
            name = name_entry.get()
            email = email_entry.get()
            if name and email:
                if not self.is_valid_email(email):
                    messagebox.showwarning("Advertencia", "Por favor ingrese un correo electrónico válido")
                    return
                if self.save_contact_to_db(name, email):
                    self.load_contacts_callback()
                    add_window.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo agregar el contacto.")
            else:
                messagebox.showwarning("Advertencia", "Por favor ingrese nombre y correo")

        add_window = tk.Toplevel(self.window)
        add_window.title("Agregar Contacto")

        tk.Label(add_window, text="Nombre:").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Correo:").pack(pady=5)
        email_entry = tk.Entry(add_window)
        email_entry.pack(pady=5)

        save_button = tk.Button(add_window, text="Guardar", command=save_contact)
        save_button.pack(pady=10)

        self.center_window(add_window)
        add_window.update()
        add_window.deiconify()

    def set_sort(self, mode):
        self.sort_mode = mode
        self.sort_var.set({
            "asc": "Ordenar A-Z",
            "desc": "Ordenar Z-A",
            "name_asc": "Ordenar por Nombre A-Z",
            "name_desc": "Ordenar por Nombre Z-A",
            "email_asc": "Ordenar por Email A-Z",
            "email_desc": "Ordenar por Email Z-A",
            "date_asc": "Ordenar por Fecha Más Antigua",
            "date_desc": "Ordenar por Fecha Reciente"
        }.get(mode, "Ordenar A-Z"))
        self.update_filter()

    def update_filter(self, *args):
        filter_text = self.search_var.get().lower()
        if not self.contacts:
            self.display_contacts([])
            return
        # Filtrar por nombre o correo
        filtered = [contact for contact in self.contacts if filter_text in (contact.get('name', '') or '').lower() or filter_text in (contact.get('email', '') or '').lower()]
        if self.sort_mode == "asc" or self.sort_mode == "name_asc":
            filtered.sort(key=lambda x: (x.get('name', '') or '').lower())
        elif self.sort_mode == "desc" or self.sort_mode == "name_desc":
            filtered.sort(key=lambda x: (x.get('name', '') or '').lower(), reverse=True)
        elif self.sort_mode == "email_asc":
            filtered.sort(key=lambda x: (x.get('email', '') or '').lower())
        elif self.sort_mode == "email_desc":
            filtered.sort(key=lambda x: (x.get('email', '') or '').lower(), reverse=True)
        elif self.sort_mode == "date_asc":
            filtered.sort(key=lambda x: x.get('created_at'))
        elif self.sort_mode == "date_desc":
            filtered.sort(key=lambda x: x.get('created_at'), reverse=True)
        self.display_contacts(filtered)

    def display_contacts(self, contacts):
        self.contact_listbox.delete(0, tk.END)
        for contact in contacts:
            # Display name and email only, ignore created_at in display
            self.contact_listbox.insert(tk.END, f"{contact.get('name', '')} - {contact.get('email', '')}")

    def load_contacts(self):
        import pymysql
        from pymysql import err as pymysql_err
        self.contact_listbox.delete(0, tk.END)
        try:
            db = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="email_sender",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = db.cursor()
            cursor.execute("SELECT name, email, created_at FROM contacts WHERE user_id = %s", (self.user_id,))
            self.contacts = cursor.fetchall()
            cursor.close()
            db.close()
            self.update_filter()
        except pymysql_err.MySQLError as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")

    def edit_contact(self):
        selected_contact = self.contact_listbox.curselection()
        if not selected_contact:
            messagebox.showwarning("Advertencia", "Seleccione un contacto para editar")
            return

        contact_info = self.contact_listbox.get(selected_contact)
        old_name, old_email = contact_info.split(" - ")

        def update_contact():
            new_name = name_entry.get()
            new_email = email_entry.get()
            if new_name and new_email:
                if not self.is_valid_email(new_email):
                    messagebox.showwarning("Advertencia", "Por favor ingrese un correo electrónico válido")
                    return
                if self.update_contact_in_db(old_name, new_name, new_email):
                    self.load_contacts_callback()
                    edit_window.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el contacto.")
            else:
                messagebox.showwarning("Advertencia", "Por favor ingrese nombre y correo")

        edit_window = tk.Toplevel(self.window)
        edit_window.title("Editar Contacto")

        tk.Label(edit_window, text="Nombre:").pack(pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, old_name)
        name_entry.pack(pady=5)

        tk.Label(edit_window, text="Correo:").pack(pady=5)
        email_entry = tk.Entry(edit_window)
        email_entry.insert(0, old_email)
        email_entry.pack(pady=5)

        update_button = tk.Button(edit_window, text="Actualizar", command=update_contact)
        update_button.pack(pady=10)

        self.center_window(edit_window)
        edit_window.update()
        edit_window.deiconify()

    def delete_contact(self):
        selected_contact = self.contact_listbox.curselection()
        if selected_contact:
            contact_info = self.contact_listbox.get(selected_contact)
            contact_name = contact_info.split(" - ")[0]

            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está seguro que desea eliminar el contacto: {contact_name}?",
                icon='warning'
            )

            if confirm:
                if self.delete_contact_from_db(contact_name):
                    self.load_contacts_callback()
                    messagebox.showinfo("Éxito", "Contacto eliminado correctamente")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el contacto.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un contacto para eliminar")

    def is_valid_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def save_contact_to_db(self, name, email):
        import pymysql
        from pymysql import err as pymysql_err
        try:
            db = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="email_sender",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = db.cursor()
            cursor.execute("INSERT INTO contacts (user_id, name, email) VALUES (%s, %s, %s)", (self.user_id, name, email))
            db.commit()
            cursor.close()
            db.close()
            return True
        except pymysql_err.MySQLError as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return False

    def update_contact_in_db(self, old_name, new_name, new_email):
        import pymysql
        from pymysql import err as pymysql_err
        try:
            db = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="email_sender",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = db.cursor()
            cursor.execute("UPDATE contacts SET name = %s, email = %s WHERE name = %s AND user_id = %s", 
                           (new_name, new_email, old_name, self.user_id))
            db.commit()
            cursor.close()
            db.close()
            return True
        except pymysql_err.MySQLError as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return False

    def delete_contact_from_db(self, contact_name):
        import pymysql
        from pymysql import err as pymysql_err
        try:
            db = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="email_sender",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = db.cursor()
            cursor.execute("DELETE FROM contacts WHERE name = %s AND user_id = %s", (contact_name, self.user_id))
            db.commit()
            cursor.close()
            db.close()
            return True
        except pymysql_err.MySQLError as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return False
