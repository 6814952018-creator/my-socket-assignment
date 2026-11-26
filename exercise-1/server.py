import socket
import threading

# กำหนดค่าการเชื่อมต่อ
HOST = '0.0.0.0'
PORT = 65432

clients = []
clients_lock = threading.Lock()


def broadcast(message, sender_conn):
    """ส่งข้อความไปยังทุก Client ยกเว้นผู้ส่ง"""
    with clients_lock:
        targets = [c for c in clients if c != sender_conn]
    for client in targets:
        try:
            client.send(message.encode('utf-8'))
        except OSError:
            pass


def handle_client(conn, addr):
    print(f"Client {addr} connected.")
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8', errors='replace')
            if not msg:
                break
            print(f"Message from {addr}: {msg}")
            broadcast(msg, conn)
        except OSError:
            break
    print(f"Client {addr} disconnected.")
    with clients_lock:
        if conn in clients:
            clients.remove(conn)
    conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server is listening on {HOST}:{PORT}...", flush=True)

    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == '__main__':
    main()