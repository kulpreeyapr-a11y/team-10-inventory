# AI Iteration Log

## สรุปปัญหาจากโค้ดที่เจนแบบไม่มี Context (`src/inventory_no_context.py`)

จากการให้ AI เจนโค้ดจาก `specs/spec.md` โดยตรงโดยยังไม่ได้ใส่กฎโปรเจกต์ (Context Rules) พบปัญหาและจุดอ่อนของโค้ดดังนี้:

1. **โครงสร้างโค้ดไม่ตรงตามหลัก Modular:**
   - รวมทุกความรับผิดชอบไว้ใน class `InventorySystem` เพียง class เดียว ทั้ง Data Model, Business Logic, การคำนวณรายงาน และการส่งแจ้งเตือน (ขัดกับหลัก Single Responsibility Principle - SRP)
2. **ขาดการใช้ Type Hint และ Docstring:**
   - ไม่มี Parameter/Return Type Annotation ชัดเจน ทำให้ตรวจสอบ Data Type ได้ยาก
   - ขาด Docstring ภาษาไทยอธิบายการทำงานของแต่ละ Method
3. **การผูกแน่นของ Logic และ Notifier (High Coupling):**
   - Class `InventorySystem` รู้จักเงื่อนไขการพิมพ์แจ้งเตือน `Email` และ `SMS` โดยตรง (ไม่ได้ใช้ Dependency Injection)
   - หากต้องการเพิ่มช่องทางแจ้งเตือนใหม่ (เช่น LINE) จะต้องกลับมาแก้ไขโค้ดใน `InventorySystem` (ขัดกับหลัก Open/Closed Principle - OCP)
4. **Hardcode และ I/O ปะปนกับ Business Logic:**
   - มีการ Hardcode ชื่อช่องทางแจ้งเตือน และการสั่ง `print()` แสดงผลลัพธ์ปะปนอยู่ภายใน Method ตัดสต็อกโดยตรง

---

## ตารางเปรียบเทียบ Before vs After Context (ขั้นที่ 4 vs ขั้นที่ 6)

| ประเด็น | ก่อนมี context (ขั้นที่ 4) | หลังมี context (ขั้นที่ 6) |
|---|---|---|
| **แยกไฟล์/ความรับผิดชอบ** | รวมทุกอย่างอยู่ในไฟล์เดียว (`inventory_no_context.py`) ขัดต่อหลัก SRP | แยกไฟล์ตามความรับผิดชอบชัดเจน (`src/models.py`, `src/notifiers.py`, `src/service.py`) |
| **type hint + docstring** | ไม่มี Type Hint ใน Function Signature และไม่มี Docstring | มี Type Hint ครบถ้วนทุก Method และมี Docstring ภาษาไทยอธิบาย Public Method |
| **service ผูกกับ notifier ตรง ๆ หรือไม่** | ผูกตรง (High Coupling) โดย Service สร้างและเรียกใช้ Email/SMS เอง | ไม่ผูกตรง โดย Service รับ `Notifier` Protocol ผ่าน Constructor Injection (DIP) |
| **hardcode config หรือไม่** | Hardcode ช่องทางแจ้งเตือนและข้อความใน Business Logic | ไม่ Hardcode โดยรับ Notifier ที่ตั้งค่าเสร็จแล้วเข้ามาจากภายนอก |