import bcrypt
from email_templates import connect_db

def get_user_configuration(user_id):
    db = connect_db()
    if db is None:
        return None
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT username, email, phone, address, signature, language
            FROM users
            WHERE id = %s
        """, (user_id,))
        row = cursor.fetchone()
        print(f"DEBUG: get_user_configuration row: {row}")  # Debug print
        cursor.close()
        if row:
            return {
                "username": row.get("username"),
                "email": row.get("email"),
                "phone": row.get("phone"),
                "address": row.get("address"),
                "signature": row.get("signature"),
                "language": row.get("language")
            }
        else:
            return None
    finally:
        db.close()

def update_user_configuration(user_id, username, email, phone, address, signature, language):
    db = connect_db()
    if db is None:
        return False
    try:
        cursor = db.cursor()
        cursor.execute("""
            UPDATE users
            SET username = %s,
                email = %s,
                phone = %s,
                address = %s,
                signature = %s,
                language = %s
            WHERE id = %s
        """, (username, email, phone, address, signature, language, user_id))
        db.commit()
        cursor.close()
        return True
    except Exception:
        return False
    finally:
        db.close()

def change_user_password(user_id, current_password, new_password):
    db = connect_db()
    if db is None:
        return False, "No se pudo conectar a la base de datos"
    try:
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            return False, "Usuario no encontrado"
        stored_password = row[0]
        # Verificar contraseña actual con bcrypt
        if not bcrypt.checkpw(current_password.encode('utf-8'), stored_password.encode('utf-8')):
            cursor.close()
            return False, "Contraseña actual incorrecta"
        # Hashear nueva contraseña con bcrypt
        new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hashed.decode('utf-8'), user_id))
        db.commit()
        cursor.close()
        return True, "Contraseña actualizada correctamente"
    except Exception as e:
        return False, f"Error al cambiar la contraseña: {e}"
    finally:
        db.close()
