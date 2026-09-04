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

## ตารางเปรียบเทียบผลลัพธ์ Before vs After Context

| ประเด็น | ก่อนมี context (ขั้นที่ 4) | หลังมี context (ขั้นที่ 6) |
|---|---|---|
| **การแยกไฟล์/ความรับผิดชอบ** | เขียนรวมกันทั้งหมดในไฟล์เดียว (`inventory_no_context.py`) | แยกไฟล์ตามหน้าที่ (`models.py`, `notifiers.py`, `service.py`) |
| **Type Hint + Docstring** | ขาด Type hint และไม่มี docstring อธิบาย | มี Type hint ครบถ้วน และมี docstring ภาษาไทยทุก method |
| **การผูกกันของ Service กับ Notifier** | Service เรียกใช้/ตัดสินใจสร้าง Notifier โดยตรง | Service รับ Notifier ผ่าน Constructor (Dependency Injection) |
| **การ Hardcode & Code Design** | Hardcode เงื่อนไขช่องทาง และปน I/O ใน logic | แยก I/O ออกจาก Logic ยึดตามหลัก SOLID (SRP, DIP, OCP) |