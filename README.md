# รายงานแบบฝึกหัด Socket API & Docker (Assignment 1 & 2)

**ข้อมูลผู้จัดทำ**
* ชื่อ-นามสกุล: นันทภพ แสวงพืช
* รหัสนักศึกษา: 6814952018
* กลุ่ม/เซคชัน: 2

---

## แบบฝึกหัดที่ 1: ระบบ Chat ด้วย Docker (2 Clients & 1 Server)

### คำอธิบายการทำงาน
ระบบแชทนี้ประยุกต์ใช้ Socket API แบบ TCP ในการส่งข้อมูลระหว่าง Client 2 ตัว ผ่าน Server กลาง
โดยรันอยู่ในรูปแบบของ Docker Multi-container และจัดการด้วย Docker Compose

- `server.py` รับการเชื่อมต่อจากหลาย Client (ใช้ threading) และกระจายข้อความ (broadcast) ไปยัง Client อื่น
- `client.py` เชื่อมต่อ Server และใช้ thread แยกสำหรับรับข้อความ ทำให้พิมพ์และรับข้อความได้พร้อมกัน

### ขั้นตอนการเริ่มทำงาน (How to run)
1. เปิด Terminal และเข้าไปที่โฟลเดอร์แบบฝึกหัดที่ 1:
   ```bash
   cd exercise-1
   ```
2. สั่งรันคอนเทนเนอร์ทั้งหมดผ่าน Docker Compose:
   ```bash
   docker compose up --build
   ```
3. การเข้าใช้งาน Client (เปิด Terminal ใหม่ 2 หน้าต่าง):
   ```bash
   docker exec -it chat_client1 python client.py
   ```
   ```bash
   docker exec -it chat_client2 python client.py
   ```
   พิมพ์ข้อความใน Client หนึ่ง แล้วอีก Client จะแสดงข้อความที่ได้รับ (`Received: ...`)
4. ปิดการทำงาน:
   ```bash
   docker compose down
   ```

---

## แบบฝึกหัดที่ 2: เว็บแอปพลิเคชัน Flask และ Socket Server

### คำอธิบายการทำงาน
แอปพลิเคชันหน้าเว็บพัฒนาด้วย Flask รับข้อความจากการกดส่งฟอร์ม (POST Method)
จากนั้น Flask จะทำหน้าที่เป็น Client ส่งข้อความนั้นต่อไปยัง Socket Server
เพื่อทำการสะท้อนข้อมูลกลับ (Echo) และแสดงผลบนหน้าเว็บ

- `app.py` – Flask web app (พอร์ต 5000)
- `socket_server.py` – TCP Socket Server (พอร์ต 12345)
- `Dockerfile.app`, `Dockerfile.socket`, `docker-compose.yml`

### ขั้นตอนการเริ่มทำงาน (How to run)
1. เปิด Terminal และเข้าไปที่โฟลเดอร์แบบฝึกหัดที่ 2:
   ```bash
   cd exercise-2
   ```
2. สร้างและรันคอนเทนเนอร์:
   ```bash
   docker compose up --build
   ```
3. เปิดเว็บเบราว์เซอร์ไปที่ <http://localhost:5000> กรอกข้อความแล้วกด **Send**
   จะเห็นผลตอบกลับจาก Socket Server แสดงบนหน้าเว็บ
4. ตรวจสอบ log:
   ```bash
   docker compose logs web_app
   docker compose logs socket_server
   ```
5. ปิดการทำงาน:
   ```bash
   docker compose down
   ```

---

## โครงสร้างโฟลเดอร์
```
my-socket-assignment/
├── .gitignore
├── README.md
├── exercise-1/
│   ├── server.py
│   ├── client.py
│   ├── Dockerfile.server
│   ├── Dockerfile.client
│   └── docker-compose.yml
└── exercise-2/
    ├── app.py
    ├── socket_server.py
    ├── Dockerfile.app
    ├── Dockerfile.socket
    └── docker-compose.yml
```
![alt text](<Screenshot 2026-11-26 102851-1.png>)
![alt text](<Screenshot 2026-11-26 102858-1.png>)
![alt text](<Screenshot 2026-11-26 103612-1.png>)