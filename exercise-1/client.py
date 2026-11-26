import socket
import threading
import os
import sys

# ใน Docker ใช้ชื่อ service "server" เป็น hostname
HOST = os.environ.get('SERVER_HOST', 'server')
PORT = int(os.environ.get('SERVER_PORT', '65432'))


def receive_messages(sock):
    """Thread สำหรับรับข้อความจาก Server"""
    while True:
        try:
            data = sock.recv(1024).decode('utf-8', errors='replace')
            if not data:
                print("Disconnected from server.")
                break
            print(f"Received: {data}")
        except OSError:
            break


def main():
    # กัน error จากตัวอักษรที่ Terminal ส่งมาไม่ใช่ UTF-8 (เช่น พิมพ์ภาษาไทยบน Windows)
    sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("Connected to server.", flush=True)

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    try:
        while True:
            message = input("Enter message: ")
            if message.lower() in ('quit', 'exit'):
                break
            sock.send(message.encode('utf-8', errors='replace'))
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        sock.close()


if __name__ == '__main__':
    main()