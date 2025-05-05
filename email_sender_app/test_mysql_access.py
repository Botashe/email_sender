import socket

def test_mysql_server(host='localhost', port=3306):
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            print(f"Conexión exitosa al servidor MySQL en {host}:{port}")
    except Exception as e:
        print(f"No se pudo conectar al servidor MySQL en {host}:{port}")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_mysql_server()
