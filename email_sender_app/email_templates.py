import tkinter as tk
from tkinter import simpledialog, messagebox
import pymysql
import tkinter as tk
from tkinter import simpledialog, messagebox
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
    except pymysql.MySQLError as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

def list_templates(user_id):
    db = connect_db()
    if db is None:
        return []
    cursor = db.cursor()
    try:
        cursor.execute("SELECT name, subject, created_at FROM templates WHERE user_id = %s", (user_id,))
        templates = [(row['name'], row['subject'], row['created_at']) for row in cursor.fetchall()]
        return templates
    except pymysql_err.MySQLError as e:
        messagebox.showerror("Error", f"Error al obtener plantillas: {e}")
        return []
    finally:
        cursor.close()
        db.close()

def list_all_templates():
    db = connect_db()
    if db is None:
        return []
    cursor = db.cursor()
    try:
        cursor.execute("SELECT name, subject, created_at FROM templates")
        templates = [(row['name'], row['subject'], row['created_at']) for row in cursor.fetchall()]
        return templates
    except pymysql_err.MySQLError as e:
        messagebox.showerror("Error", f"Error al obtener todas las plantillas: {e}")
        return []
    finally:
        cursor.close()
        db.close()

def get_template(user_id, name):
    db = connect_db()
    if db is None:
        return "", ""
    cursor = db.cursor()
    try:
        cursor.execute("SELECT subject, content FROM templates WHERE user_id = %s AND name = %s", (user_id, name))
        row = cursor.fetchone()
        return (row['subject'], row['content']) if row else ("", "")
    except pymysql_err.MySQLError as e:
        messagebox.showerror("Error", f"Error al obtener plantilla: {e}")
        return "", ""
    finally:
        cursor.close()
        db.close()

def add_template(user_id, name, subject, content):
    db = connect_db()
    if db is None:
        return False
    cursor = db.cursor()
    try:
        # Verificar si la plantilla ya existe para el usuario
        cursor.execute("SELECT COUNT(*) FROM templates WHERE user_id = %s AND name = %s", (user_id, name))
        count = cursor.fetchone()['COUNT(*)']
        if count > 0:
            messagebox.showerror("Error", "La plantilla ya existe")
            return False
        cursor.execute("INSERT INTO templates (user_id, name, subject, content) VALUES (%s, %s, %s, %s)", (user_id, name, subject, content))
        db.commit()
        return True
    except pymysql.MySQLError as e:
        messagebox.showerror("Error al agregar plantilla", f"No se pudo agregar la plantilla debido a un error inesperado. Detalles: {e}")
        return False
    finally:
        cursor.close()
        db.close()

def edit_template(user_id, name, subject, content):
    db = connect_db()
    if db is None:
        return False
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE templates SET subject = %s, content = %s WHERE user_id = %s AND name = %s", (subject, content, user_id, name))
        db.commit()
        return True
    except pymysql_err.MySQLError as e:
        messagebox.showerror("Error", f"Error al actualizar plantilla: {e}")
        return False
    finally:
        cursor.close()
        db.close()

def delete_template(user_id, name):
    db = connect_db()
    if db is None:
        return False
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM templates WHERE user_id = %s AND name = %s", (user_id, name))
        db.commit()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar plantilla: {e}")
        return False
    finally:
        cursor.close()
        db.close()

def select_template_ui(parent, user_id):
    def on_select():
        try:
            selected = listbox.get(tk.ACTIVE)
        except tk.TclError:
            selected = None
        if selected:
            messagebox.showinfo("Plantilla Seleccionada", f"Has seleccionado la plantilla: {selected}")
            select_window.destroy()
        else:
            messagebox.showwarning("Advertencia", "Por favor selecciona una plantilla")

    def on_add():
        name = simpledialog.askstring("Nueva Plantilla", "Nombre de la nueva plantilla:", parent=select_window)
        if name:
            subject = simpledialog.askstring("Asunto", "Asunto de la plantilla:", parent=select_window)
            if subject:
                content = simpledialog.askstring("Contenido", "Contenido de la plantilla:", parent=select_window)
                if content:
                    if add_template(user_id, name, subject, content):
                        listbox.insert(tk.END, name)
                    else:
                        messagebox.showerror("Error", "La plantilla ya existe")

    def on_edit():
        selected = listbox.get(tk.ACTIVE)
        if selected:
            new_name = simpledialog.askstring("Editar Plantilla", "Nuevo nombre de la plantilla:", initialvalue=selected, parent=select_window)
            if new_name:
                subject, content = get_template(user_id, selected)
                new_subject = simpledialog.askstring("Editar Asunto", "Nuevo asunto:", initialvalue=subject, parent=select_window)
                if new_subject:
                    new_content = simpledialog.askstring("Editar Plantilla", "Nuevo contenido:", initialvalue=content, parent=select_window)
                    if new_content:
                        if new_name != selected:
                            # Verificar si el nuevo nombre ya existe
                            db = connect_db()
                            if db is None:
                                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                                return
                            cursor = db.cursor()
                            cursor.execute("SELECT COUNT(*) FROM templates WHERE user_id = %s AND name = %s", (user_id, new_name))
                            count = cursor.fetchone()[0]
                            cursor.close()
                            db.close()
                            if count > 0:
                                messagebox.showerror("Error", "El nombre de plantilla ya existe")
                                return
                        # Actualizar nombre, asunto y contenido
                        if edit_template(user_id, selected, new_subject, new_content):
                            # Si el nombre cambió, actualizarlo en la base de datos
                            if new_name != selected:
                                db = connect_db()
                                if db is None:
                                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                                    return
                                cursor = db.cursor()
                                try:
                                    cursor.execute("UPDATE templates SET name = %s WHERE user_id = %s AND name = %s", (new_name, user_id, selected))
                                    db.commit()
                                except pymysql.MySQLError as e:
                                    messagebox.showerror("Error", f"Error al actualizar nombre de plantilla: {e}")
                                finally:
                                    cursor.close()
                                    db.close()
                                messagebox.showinfo("Éxito", "Plantilla actualizada")
                                # Actualizar la lista en la UI
                                listbox.delete(tk.ACTIVE)
                                listbox.insert(tk.ACTIVE, new_name)
                        else:
                            messagebox.showerror("Error", "Error al actualizar la plantilla")
        else:
            messagebox.showwarning("Advertencia", "Por favor selecciona una plantilla")

    def on_delete():
        selected = listbox.get(tk.ACTIVE)
        if selected:
            if messagebox.askyesno("Confirmar", f"¿Eliminar plantilla '{selected}'?"):
                if delete_template(user_id, selected):
                    listbox.delete(tk.ACTIVE)
                else:
                    messagebox.showerror("Error", "Error al eliminar la plantilla")
        else:
            messagebox.showwarning("Advertencia", "Por favor selecciona una plantilla")

    select_window = tk.Toplevel(parent)
    select_window.title("Seleccionar Plantilla")
    select_window.geometry("400x300")

    listbox = tk.Listbox(select_window, exportselection=False)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for tpl in list_templates(user_id):
        listbox.insert(tk.END, tpl)

    # Desactivar selección automática
    listbox.selection_clear(0, tk.END)
    listbox.select_clear(0, tk.END)
    listbox.selection_set(-1)

    btn_frame = tk.Frame(select_window)
    btn_frame.pack(pady=5)

    select_btn = tk.Button(btn_frame, text="Seleccionar", command=on_select)
    select_btn.pack(side=tk.LEFT, padx=5)

    add_btn = tk.Button(btn_frame, text="Agregar", command=on_add)
    add_btn.pack(side=tk.LEFT, padx=5)

    edit_btn = tk.Button(btn_frame, text="Editar", command=on_edit)
    edit_btn.pack(side=tk.LEFT, padx=5)

    delete_btn = tk.Button(btn_frame, text="Eliminar", command=on_delete)
