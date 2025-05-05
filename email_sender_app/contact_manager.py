import tkinter as tk
from tkinter import messagebox
import pymysql
from pymysql import err as pymysql_err
import re  # Importar el módulo de expresiones regulares

from assets.contact_manager_ui import ContactManagerUI

class ContactManager:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        master.title("Gestión de Contactos")

        self.ui = ContactManagerUI(master, user_id, self.load_contacts)

        self.load_contacts()

    def load_contacts(self):
        self.ui.contact_listbox.delete(0, tk.END)  # Limpiar la lista
        db = connect_db()
        if db is None:
            return
        cursor = db.cursor()
        cursor.execute("SELECT name, email FROM contacts WHERE user_id = %s", (self.user_id,))
        contacts = cursor.fetchall()
        for contact in contacts:
            self.ui.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['email']}")
        cursor.close()
        db.close()

    def is_valid_email(self, email):
        # Expresión regular para validar el formato del correo electrónico
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def center_window(self, window):
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
                db = connect_db()
                if db is None:
                    return
                cursor = db.cursor()
                cursor.execute("INSERT INTO contacts (user_id, name, email) VALUES (%s, %s, %s)", (self.user_id, name, email))
                db.commit()
                cursor.close()
                db.close()
                self.load_contacts()
                add_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Por favor ingrese nombre y correo")

        add_window = tk.Toplevel(self.master)
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

    def edit_contact(self):
        selected_contact = self.ui.contact_listbox.curselection()
        if not selected_contact:
            messagebox.showwarning("Advertencia", "Seleccione un contacto para editar")
            return

        contact_info = self.ui.contact_listbox.get(selected_contact)
        old_name, old_email = contact_info.split(" - ")

        def update_contact():
            new_name = name_entry.get()
            new_email = email_entry.get()
            if new_name and new_email:
                if not self.is_valid_email(new_email):
                    messagebox.showwarning("Advertencia", "Por favor ingrese un correo electrónico válido")
                    return
                db = connect_db()
                if db is None:
                    return
                cursor = db.cursor()
                cursor.execute("UPDATE contacts SET name = %s, email = %s WHERE name = %s AND user_id = %s", 
                             (new_name, new_email, old_name, self.user_id))
                db.commit()
                cursor.close()
                db.close()
                self.load_contacts()
                edit_window.destroy()
            else:
                messagebox.showwarning("Advertencia", "Por favor ingrese nombre y correo")

        edit_window = tk.Toplevel(self.master)
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
        selected_contact = self.ui.contact_listbox.curselection()
        if selected_contact:
            contact_info = self.ui.contact_listbox.get(selected_contact)
            contact_name = contact_info.split(" - ")[0]
            
            # Pedir confirmación antes de eliminar
            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está seguro que desea eliminar el contacto: {contact_name}?",
                icon='warning'
            )
            
            if confirm:
                db = connect_db()
                if db is None:
                    return
                cursor = db.cursor()
                cursor.execute("DELETE FROM contacts WHERE name = %s", (contact_name,))
                db.commit()
                cursor.close()
                db.close()
                self.load_contacts()
                messagebox.showinfo("Éxito", "Contacto eliminado correctamente")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un contacto para eliminar")

def connect_db():
    try:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="email_sender",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql_err.MySQLError as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

def show_contact_manager(master, user_id):
    # Crear ventana Toplevel independiente para gestión de contactos
    contact_window = tk.Toplevel()
    contact_manager = ContactManager(contact_window, user_id)
