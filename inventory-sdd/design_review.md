# SOLID Design Review (`design_review.md`)

| หลัก SOLID | ละเมิดหรือไม่ | จุดที่เกี่ยวข้อง (class/method) | อธิบาย/ผลกระทบ | ข้อเสนอปรับปรุง |
|---|:---:|---|---|---|
| **S (SRP)** | ไม่ละเมิด | `InventoryService` และ `notifiers.py` | แยกหน้าที่ชัดเจน `models.py` เก็บข้อมูล, `notifiers.py` ส่งข้อความ และ `service.py` จัดการเฉพาะ Business Logic | รักษาโครงสร้างเดิมไว้ |
| **O (OCP)** | ไม่ละเมิด | `InventoryService` / `notifiers.py` | เพิ่มช่องทางแจ้งเตือนใหม่ (เช่น Line, Webhook) ได้โดยไม่ต้องแก้ไขโค้ดเดิมใน `InventoryService` | - |
| **L (LSP)** | ไม่ละเมิด | `EmailNotifier`, `SMSNotifier` | Class ย่อยทุกตัวอิมพลิเมนต์ตาม `Notifier` Protocol สมบูรณ์ สามารถเรียกใช้งานทดแทนกันได้ทันทีโดยไม่เกิด Error | - |
| **I (ISP)** | ไม่ละเมิด | `Notifier` Protocol | กำหนดเฉพาะ Method ที่จำเป็น (`send`) ไม่บังคับให้ Class ลูกต้องอิมพลิเมนต์ Method ที่ไม่ได้ใช้งาน | - |
| **D (DIP)** | ไม่ละเมิด | `InventoryService.__init__` | `InventoryService` รับ `Notifier` ผ่าน Constructor Injection ไม่ได้ Import หรือ Instantiate `EmailNotifier`/`SMSNotifier` ตรงๆ | - |