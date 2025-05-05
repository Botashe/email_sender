import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from email_templates import list_templates, get_template, add_template, edit_template, delete_template, connect_db
import re
import datetime

class TemplateManagerUI:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        self.window = tk.Toplevel(parent)
        self.window.title("Gestor de Plantillas")
        self.window.geometry("600x400")

        self.center_window()

        # Cambiar layout principal a grid
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=2)
        self.window.grid_columnconfigure(1, weight=3)
        self.window.minsize(800, 500)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=2)
        self.window.columnconfigure(1, weight=3)

        # Frame para lista de plantillas y botón Nuevo
        left_frame = tk.Frame(self.window)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.grid_rowconfigure(4, weight=1)  # Hacer que la fila 4 (listbox) crezca verticalmente
        left_frame.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_filter)
        self.search_entry = tk.Entry(left_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))

        self.sort_var = tk.StringVar(value="Ordenar A-Z")
        self.sort_menu_btn = tk.Menubutton(left_frame, text="🔽 Ordenar", relief=tk.RAISED)
        self.sort_menu = tk.Menu(self.sort_menu_btn, tearoff=0)
        self.sort_menu.add_radiobutton(label="Ordenar A-Z", variable=self.sort_var, command=lambda: self.set_sort("asc"))
        self.sort_menu.add_radiobutton(label="Ordenar Z-A", variable=self.sort_var, command=lambda: self.set_sort("desc"))
        self.sort_menu.add_separator()
        self.sort_menu.add_radiobutton(label="Ordenar por Asunto A-Z", variable=self.sort_var, command=lambda: self.set_sort("subject_asc"))
        self.sort_menu.add_radiobutton(label="Ordenar por Asunto Z-A", variable=self.sort_var, command=lambda: self.set_sort("subject_desc"))
        self.sort_menu.add_separator()
        self.sort_menu.add_radiobutton(label="Ordenar por Fecha Reciente", variable=self.sort_var, command=lambda: self.set_sort("date_desc"))
        self.sort_menu.add_radiobutton(label="Ordenar por Fecha Más Antigua", variable=self.sort_var, command=lambda: self.set_sort("date_asc"))
        self.sort_menu_btn.config(menu=self.sort_menu)
        self.sort_menu_btn.grid(row=1, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))

        # Añadir botón variables disponibles debajo de ordenar
        self.help_button = tk.Button(left_frame, text="Variables disponibles", command=self.show_variables_help)
        self.help_button.config(width=30)
        self.help_button.grid(row=2, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))

        self.new_btn = tk.Button(left_frame, text="Nuevo", command=self.new_template)
        self.new_btn.grid(row=3, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))

        self.listbox = tk.Listbox(left_frame)
        self.listbox.grid(row=4, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        form_frame = tk.Frame(self.window)
        form_frame.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)

        tk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW)

        tk.Label(form_frame, text="Asunto:").grid(row=1, column=0, sticky=tk.W)
        self.subject_entry = tk.Entry(form_frame)
        self.subject_entry.grid(row=1, column=1, sticky=tk.EW)

        tk.Label(form_frame, text="Contenido:").grid(row=2, column=0, sticky=tk.NW)
        self.content_text = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, height=10)
        self.content_text.grid(row=2, column=1, sticky=tk.EW)
        self.content_text.bind("<KeyRelease>", self.on_content_keyrelease)

        tk.Label(form_frame, text="Previsualización:").grid(row=4, column=0, sticky=tk.NW)
        self.preview_text = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, height=10, state=tk.DISABLED, bg="#f0f0f0")
        self.preview_text.grid(row=4, column=1, sticky=tk.EW, pady=(10, 0))

        # Botones agregar, editar y borrar plantilla en horizontal debajo de la vista previa
        buttons_frame = tk.Frame(form_frame)
        buttons_frame.grid(row=5, column=1, sticky="ew", pady=(10, 0))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)

        # Set a minimum width for buttons to avoid being cut off
        min_button_width = 20

        self.add_button = tk.Button(buttons_frame, text="Guardar", command=self.add_template)
        self.add_button.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.edit_button = tk.Button(buttons_frame, text="Editar", command=self.edit_template)
        self.edit_button.grid(row=0, column=1, sticky="nsew", padx=5)

        self.delete_button = tk.Button(buttons_frame, text="Borrar", command=self.delete_template)
        self.delete_button.grid(row=0, column=2, sticky="nsew", padx=(5, 0))

        # Add padding inside buttons to prevent text clipping
        for btn in [self.add_button, self.edit_button, self.delete_button]:
            btn.config(padx=10, pady=5)

        # Ensure buttons_frame expands horizontally
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)

        # Ensure form_frame expands horizontally
        parent_form = buttons_frame.master
        parent_form.grid_columnconfigure(1, weight=1)

        # Variables para autocompletado
        self.variables = [
            "Nombre contacto",
            "Email contacto",
            "Documento1",
            "Documento2",
            "Correo",
            "Fecha actual",
            "Hora actual",
            "Día actual",
            "Saludo"
        ]

        # Lista desplegable para autocompletado
        self.autocomplete_listbox = None

        self.load_templates()

        # Variables para autocompletado
        self.variables = [
            "Nombre contacto",
            "Email contacto",
            "Documento1",
            "Documento2",
            "Correo",
            "Fecha actual",
            "Hora actual",
            "Día actual",
            "Saludo"
        ]

        # Lista desplegable para autocompletado
        self.autocomplete_listbox = None

        self.load_templates()

    def highlight_invalid_variables(self):
        print("DEBUG: Highlighting invalid variables")  # Debug print
        # Eliminar resaltado previo
        self.clear_invalid_variable_highlight()
        content = self.content_text.get('1.0', tk.END)
        pattern = r'\[([^\]]+)\]'
        for match in re.finditer(pattern, content):
            var_name = match.group(1)
            if var_name not in self.variables:
                start_index = f"1.0 + {match.start()} chars"
                end_index = f"1.0 + {match.end()} chars"
                self.content_text.tag_add("invalid_var", start_index, end_index)
            else:
                # Remove highlight if variable is valid (in case it was previously highlighted)
                start_index = f"1.0 + {match.start()} chars"
                end_index = f"1.0 + {match.end()} chars"
                self.content_text.tag_remove("invalid_var", start_index, end_index)

        self.content_text.tag_config("invalid_var", background="red", foreground="white")

    def clear_invalid_variable_highlight(self):
        print("DEBUG: Clearing invalid variable highlights")  # Debug print
        self.content_text.tag_remove("invalid_var", '1.0', tk.END)

    def update_preview(self):
        content = self.content_text.get('1.0', tk.END)
        now = datetime.datetime.now()
        day_name_en = now.strftime("%A")
        day_name_es_map = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        day_name_es = day_name_es_map.get(day_name_en, day_name_en)
        variables = {
            "Nombre contacto": "Juan Pérez",
            "Email contacto": "juan.perez@example.com",
            "Documento1": "informe.pdf",
            "Documento2": "contrato.docx",
            "Correo": "correo@example.com",
            "Fecha actual": now.strftime("%m/%d/%Y"),
            "Hora actual": now.strftime("%H:%M"),
            "Día actual": day_name_es,
            "Saludo": self.get_greeting()
        }
        def replace_var(match):
            var_name = match.group(1)
            return variables.get(var_name, f"[{var_name}]")
        preview_content = re.sub(r"\[([^\]]+)\]", replace_var, content)

        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert(tk.END, preview_content)
        self.preview_text.config(state=tk.DISABLED)

    def on_content_keyrelease(self, event):
        print("DEBUG: on_content_keyrelease called")  # Debug print
        # Obtener la posición del cursor
        cursor_index = self.content_text.index(tk.INSERT)
        line, col = map(int, cursor_index.split('.'))
        # Obtener el texto de la línea actual hasta el cursor
        line_text = self.content_text.get(f"{line}.0", f"{line}.{col}")
        # Buscar el último corchete abierto y el último corchete cerrado
        last_open_bracket_pos = line_text.rfind('[')
        last_close_bracket_pos = line_text.rfind(']')
        # Verificar si el cursor está dentro de corchetes abiertos y no cerrados
        if last_open_bracket_pos == -1 or (last_close_bracket_pos > last_open_bracket_pos):
            print("DEBUG: Cursor not inside brackets, hiding autocomplete")  # Debug print
            self.hide_autocomplete()
            # No limpiar resaltado aquí para que no desaparezca al seguir escribiendo fuera de corchetes
            # self.clear_invalid_variable_highlight()
            self.update_preview()
            return
        # Obtener el texto después del último corchete abierto
        prefix = line_text[last_open_bracket_pos+1:]
        # Filtrar variables que coincidan con el prefijo
        matches = [var for var in self.variables if var.lower().startswith(prefix.lower())]
        if matches:
            self.show_autocomplete(matches, line, last_open_bracket_pos)
        else:
            print("DEBUG: No matches found, hiding autocomplete")  # Debug print
            self.hide_autocomplete()
        self.highlight_invalid_variables()
        self.update_preview()

    def show_autocomplete(self, matches, line, bracket_pos):
        print(f"DEBUG: show_autocomplete called with matches: {matches}")  # Debug print
        if self.autocomplete_listbox:
            self.autocomplete_listbox.destroy()
        # Calcular posición para mostrar la lista
        bbox = self.content_text.bbox(f"{line}.{bracket_pos+1}")
        print(f"DEBUG: bbox for autocomplete: {bbox}")  # Debug print
        if not bbox:
            print("DEBUG: bbox not found, hiding autocomplete")  # Debug print
            self.hide_autocomplete()
            return
        x, y, width, height = bbox
        x_root = self.content_text.winfo_rootx() + x
        y_root = self.content_text.winfo_rooty() + y + height
        print(f"DEBUG: autocomplete position: x={x_root}, y={y_root}")  # Debug print

        # Usar Toplevel para la lista de autocompletado para mejor control de posición y visibilidad
        if hasattr(self, 'autocomplete_window') and self.autocomplete_window:
            self.autocomplete_window.destroy()
        self.autocomplete_window = tk.Toplevel(self.window)
        self.autocomplete_window.wm_overrideredirect(True)
        self.autocomplete_window.wm_geometry(f"+{x_root}+{y_root}")

        self.autocomplete_listbox = tk.Listbox(self.autocomplete_window, height=min(5, len(matches)), bg="white", fg="black", bd=1, relief="solid")
        for match in matches:
            self.autocomplete_listbox.insert(tk.END, match)
        self.autocomplete_listbox.pack()
        self.autocomplete_listbox.bind("<ButtonRelease-1>", self.on_autocomplete_select)
        self.autocomplete_listbox.bind("<Return>", self.on_autocomplete_select)
        self.autocomplete_listbox.focus_set()

    def hide_autocomplete(self):
        if hasattr(self, 'autocomplete_window') and self.autocomplete_window:
            self.autocomplete_window.destroy()
            self.autocomplete_window = None
        self.autocomplete_listbox = None

    def on_autocomplete_select(self, event):
        if not self.autocomplete_listbox:
            return
        selection = self.autocomplete_listbox.curselection()
        if not selection:
            return
        selected_text = self.autocomplete_listbox.get(selection[0])
        # Insertar la variable seleccionada en el texto
        cursor_index = self.content_text.index(tk.INSERT)
        line, col = map(int, cursor_index.split('.'))
        line_start = f"{line}.0"
        line_text = self.content_text.get(line_start, f"{line}.{col}")
        last_bracket_pos = line_text.rfind('[')
        if last_bracket_pos == -1:
            self.hide_autocomplete()
            return
        # Reemplazar el texto desde el último corchete hasta el cursor con la variable seleccionada + cierre de corchete
        self.content_text.delete(f"{line}.{last_bracket_pos+1}", f"{line}.{col}")
        self.content_text.insert(f"{line}.{last_bracket_pos+1}", selected_text + "]")
        self.hide_autocomplete()
        # Mover cursor al final de la variable insertada + corchete
        self.content_text.mark_set(tk.INSERT, f"{line}.{last_bracket_pos+2 + len(selected_text)}")
        self.hide_autocomplete()

    def show_variables_help(self):
        help_window = tk.Toplevel(self.window)
        help_window.title("Variables disponibles")
        help_window.geometry("400x350")
        help_window.resizable(True, True)
        help_window.transient(self.window)
        help_window.grab_set()

        help_text = (
            "Variables disponibles para plantillas:\n\n"
            "[Nombre contacto] - Nombre del contacto seleccionado\n"
            "[Email contacto] - Email del contacto seleccionado\n"
            "[Documento1], [Documento2], ... - Nombres de archivos adjuntos\n"
            "[Correo] - Correo electrónico\n"
            "[Fecha actual] - Fecha actual en formato MM/DD/AAAA\n"
            "[Hora actual] - Hora actual en formato hh:mm\n"
            "[Día actual] - Día actual de la semana\n"
            "[Saludo] - Saludo según la hora del día (Buenos días, Buenas tardes, Buenas noches)\n"
            "\nUsa estas variables entre corchetes en tus plantillas para personalizar los correos."
        )

        text_widget = tk.scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        close_button = tk.Button(help_window, text="Cerrar", command=help_window.destroy)
        close_button.pack(pady=10)

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def load_templates(self):
        self.listbox.delete(0, tk.END)
        print(f"DEBUG: Loading templates for user_id: {self.user_id}")  # Debug print user_id
        # Update list_templates to also fetch created_at datetime
        try:
            self.templates = list_templates(self.user_id)  # Should return list of tuples (name, subject, created_at)
            print(f"DEBUG: Templates loaded: {self.templates}")  # Debug print
        except Exception as e:
            self.templates = []
            messagebox.showerror("Error", f"No se pudieron cargar las plantillas: {e}")
        self.sort_mode = "asc"
        self.display_templates(self.templates)

    def display_templates(self, templates):
        print(f"DEBUG: Displaying templates: {templates}")  # Debug print
        self.listbox.delete(0, tk.END)
        for tpl in templates:
            name = tpl[0]
            subject = tpl[1]
            created_at = tpl[2]
            display_text = f"{name} - {subject} - {created_at.strftime('%Y-%m-%d') if hasattr(created_at, 'strftime') else created_at}"
            self.listbox.insert(tk.END, display_text)

    def update_filter(self, *args):
        if not hasattr(self, 'templates'):
            self.templates = []
        if not hasattr(self, 'sort_mode'):
            self.sort_mode = "asc"
        filter_text = self.search_var.get().lower()
        filtered = [tpl for tpl in self.templates if filter_text in tpl[0].lower()]
        if self.sort_mode == "asc":
            filtered.sort(key=lambda x: x[0].lower())
        elif self.sort_mode == "desc":
            filtered.sort(key=lambda x: x[0].lower(), reverse=True)
        elif self.sort_mode == "subject_asc":
            filtered.sort(key=lambda x: x[1].lower())
        elif self.sort_mode == "subject_desc":
            filtered.sort(key=lambda x: x[1].lower(), reverse=True)
        elif self.sort_mode == "date_desc":
            filtered.sort(key=lambda x: x[2], reverse=True)
        elif self.sort_mode == "date_asc":
            filtered.sort(key=lambda x: x[2])
        self.display_templates(filtered)

    def on_select(self, event):
        print("DEBUG: on_select called")  # Debug print
        # Evitar que la selección se pierda al seleccionar texto en el contenido
        # Comprobar si el evento proviene del widget content_text para evitar deselección
        if event.widget == self.content_text:
            return "break"
        try:
            # Comprobar si hay selección de texto en el widget content_text
            if self.content_text.tag_ranges(tk.SEL):
                return "break"
        except tk.TclError:
            pass
        # Evitar que on_select se ejecute si el foco no está en el listbox
        if self.window.focus_get() != self.listbox:
            print("DEBUG: Focus not in listbox, ignoring on_select")  # Debug print
            return "break"
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        item_text = self.listbox.get(index)
        # Extract name from "name - subject"
        name = item_text.split(" - ")[0]
        subject, content = get_template(self.user_id, name)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.subject_entry.delete(0, tk.END)
        self.subject_entry.insert(0, subject)
        self.content_text.delete('1.0', tk.END)
        self.content_text.insert(tk.END, content)

        # Reemplazo de variables dinámicas para previsualización con valores de ejemplo
        variables = {
            "Nombre contacto": "Juan Pérez",
            "Email contacto": "juan.perez@example.com",
            "Documento1": "informe.pdf",
            "Documento2": "contrato.docx"
        }
        def replace_var(match):
            var_name = match.group(1)
            # Strip any trailing or leading whitespace from var_name
            var_name_clean = var_name.strip()
            # Make variable name case-insensitive for matching
            var_name_key = var_name_clean.capitalize()
            value = variables.get(var_name_key, f"[{var_name}]")
            if var_name_key == "Saludo":
                value = value.lower()
            # If the value is still the placeholder, try lowercase key
            if value == f"[{var_name}]":
                value = variables.get(var_name_clean.lower(), value)
            return value
        preview_content = re.sub(r"\[([^\]]+)\]", replace_var, content)

        # Actualizar previsualización
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert(tk.END, preview_content)
        self.preview_text.config(state=tk.DISABLED)
        # Mantener la selección activa para permitir edición continua
        self.listbox.selection_set(index)

    def toggle_sort(self):
        self.sorted_asc = not getattr(self, 'sorted_asc', True)
        if self.sorted_asc:
            self.sort_btn.config(text="Ordenar A-Z")
        else:
            self.sort_btn.config(text="Ordenar Z-A")
        self.update_filter()

    def set_sort(self, mode):
        self.sort_mode = mode
        self.sort_var.set({
            "asc": "Ordenar A-Z",
            "desc": "Ordenar Z-A",
            "subject_asc": "Ordenar por Asunto A-Z",
            "subject_desc": "Ordenar por Asunto Z-A",
            "date_asc": "Ordenar por Fecha Más Antigua",
            "date_desc": "Ordenar por Fecha Reciente"
        }[mode])
        self.update_filter()

    def new_template(self):
        # Deseleccionar plantilla y limpiar campos para nueva plantilla
        self.listbox.selection_clear(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.content_text.delete('1.0', tk.END)

    def add_template(self):
        name = self.name_entry.get().strip()
        subject = self.subject_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        if not name or not content:
            messagebox.showwarning("Advertencia", "El nombre y contenido son obligatorios.")
            return
        if add_template(self.user_id, name, subject, content):
            messagebox.showinfo("Éxito", "Plantilla agregada correctamente.")
            self.load_templates()
        else:
            messagebox.showerror("Error", "No se pudo agregar la plantilla.")

    def edit_template(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una plantilla para editar.")
            return
        old_item_text = self.listbox.get(selection[0])
        old_name = old_item_text.split(" - ")[0]

        new_name = self.name_entry.get().strip()
        new_subject = self.subject_entry.get().strip()
        new_content = self.content_text.get('1.0', tk.END).strip()

        if not new_name or not new_content:
            messagebox.showwarning("Advertencia", "El nombre y contenido son obligatorios.")
            return

        # Check if name changed and if new name exists
        if new_name != old_name:
            db = connect_db()
            if db is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM templates WHERE user_id = %s AND name = %s", (self.user_id, new_name))
            count = cursor.fetchone()[0]
            cursor.close()
            db.close()
            if count > 0:
                messagebox.showerror("Error", "El nombre de plantilla ya existe")
                return

        # Update content and subject
        if edit_template(self.user_id, old_name, new_subject, new_content):
            # If name changed, update it in DB
            if new_name != old_name:
                db = connect_db()
                if db is None:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    return
                cursor = db.cursor()
                try:
                    cursor.execute("UPDATE templates SET name = %s WHERE user_id = %s AND name = %s", (new_name, self.user_id, old_name))
                    db.commit()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar nombre de plantilla: {e}")
                finally:
                    cursor.close()
                    db.close()
            messagebox.showinfo("Éxito", "Plantilla actualizada")
            self.load_templates()
        else:
            messagebox.showerror("Error", "Error al actualizar la plantilla")

    def delete_template(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una plantilla para eliminar.")
            return
        item_text = self.listbox.get(selection[0])
        name = item_text.split(" - ")[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar plantilla '{name}'?"):
            if delete_template(self.user_id, name):
                messagebox.showinfo("Éxito", "Plantilla eliminada")
                self.load_templates()
            else:
                messagebox.showerror("Error", "Error al eliminar la plantilla")

    def get_greeting(self):
        import datetime
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            return "buenos días"
        elif 12 <= hour < 20:
            return "buenas tardes"
        else:
            return "buenas noches"
