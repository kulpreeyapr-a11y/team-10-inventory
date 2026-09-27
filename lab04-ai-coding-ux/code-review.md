# Code Review Log: inventory_service.py

## Review Checklist
1. **Docstring Accuracy:** โค้ดตรงตาม Docstring หรือไม่ (เน้นคำว่า "หรือเท่ากับ" / ขอบเขต)
2. **State & Partial Failure:** หากพังกลางทาง มี State ค้างหรือไม่
3. **Concurrency & Thread Safety:** รันพร้อมกัน 2 Threads ค่าที่อ่านมาจะยังถูกต้องหรือไม่
4. **Edge Cases & Zero Division:** ลิสต์ว่าง / ค่าเป็นศูนย์ จะเกิด Crash หรือไม่

---

## Detailed Review Comments

### Issue 1: `add_stock` - Border condition handling
- **Location:** Method `add_stock`, line 15
- **Why it is wrong:** Docstring ระบุว่าปริมาณการเพิ่มสินค้าต้องมากกว่าหรือเท่ากับ 0 (`quantity >= 0`) แต่ตัวโค้ดใช้เงื่อนไข `if quantity > 0:` ทำให้เมื่อส่งค่า `quantity = 0` เข้ามา จะหลุดไปเข้าบล็อก `else` หรือไม่ถูกประมวลผลตามที่กำหนด
- **Broken Example:** เรียกใช้งาน `add_stock("ITEM001", 0)`
  - Expected: ทำงานสำเร็จโดยไม่เพิ่มจำนวน หรือคืนค่าปกติ
  - Actual: ถูกปฏิเสธเนื่องจากไม่เข้าเงื่อนไข `quantity > 0`
- **Proposed Fix:** เปลี่ยนเงื่อนไขจาก `if quantity > 0:` เป็น `if quantity >= 0:`
- **Category:** correctness
- **Severity:** medium

---

### Issue 2: `deduct_stock` - Partial Failure Leaves Dirty State
- **Location:** Method `deduct_stock`, lines 32-38
- **Why it is wrong:** มีการหักสต็อกสินค้าในหน่วยความจำไปแล้ว แต่กระบวนการบันทึกลงไฟล์/ฐานข้อมูลด้านล่างเกิด Exception/Error ทำให้ข้อมูลใน Memory ถูกหักไปแล้วแต่ไม่ได้ Save เกิด Dirty State
- **Broken Example:** เรียก `deduct_stock("ITEM001", 5)` โดยที่ดิสก์เต็ม หรือระบบ IO พังขณะบันทึกไฟล์
  - Expected: ย้อนคืนค่า (Rollback) สต็อกกลับเป็นจำนวนเดิมก่อนเกิด Error
  - Actual: สต็อกถูกลดไปแล้วใน Memory ทำให้ข้อมูลไม่ตรงกับ Database/File
- **Proposed Fix:** คำนวณสต็อกใหม่ไว้ก่อน แล้วค่อยสั่ง Save หาก Save สำเร็จจึงค่อยอัปเดตค่าเข้า State หลัก หรือใช้ Try-Except ทำ Rollback ค่าเดิม
- **Category:** correctness
- **Severity:** high

---

### Issue 3: `get_average_stock` - Division by Zero
- **Location:** Method `get_average_stock`, line 52
- **Why it is wrong:** นำผลรวมของสินค้าไปหารด้วยจำนวนรายการโดยตรง `total / len(items)` โดยไม่ได้เช็คว่ารายการสินค้าว่างเปล่าหรือไม่
- **Broken Example:** เรียก `get_average_stock()` เมื่อระบบยังไม่มีสินค้าเลย (`items = []`)
  - Expected: คืนค่า `0.0`
  - Actual: โปรแกรม Crash ด้วย `ZeroDivisionError: division by zero`
- **Proposed Fix:** เพิ่ม Guard Clause ด้านบนสุดของเมธอด `if not items: return 0.0`
- **Category:** correctness
- **Severity:** medium

---

### Issue 4: `update_inventory_batch` - Race Condition / Thread Safety
- **Location:** Method `update_inventory_batch`, lines 65-70
- **Why it is wrong:** มีการอ่านค่าสต็อกปัจจุบันมาเก็บในตัวแปร แล้วนำไปคำนวณก่อนเขียนกลับ โดยไม่มีการใช้ Lock/Synchronization หากมี 2 Threads เรียกใช้พร้อมกัน จะเกิดการ overwrite ค่าของกันและกัน (Race Condition)
- **Broken Example:** Thread A และ Thread B อ่านสต็อกเดิม (10 ชิ้น) มาพร้อมกัน Thread A เพิ่ม 5 ชิ้น, Thread B เพิ่ม 5 ชิ้น
  - Expected: สต็อกรวมต้องเป็น 20 ชิ้น
  - Actual: สต็อกบันทึกทับกันเหลือเพียง 15 ชิ้น
- **Proposed Fix:** นำ `threading.Lock()` มาครอบในขั้นตอนการ Read-Modify-Write เพื่อรับประกัน Thread Safety
- **Category:** concurrency
- **Severity:** high

---

## Summary Table

| # | เมธอด | หมวด | ระดับ | สรุปปัญหา | กรณีที่ทำให้พัง |
|---|---|---|---|---|---|
| 1 | `add_stock` | correctness | medium | ไม่รองรับกรณีใส่ quantity เป็น 0 ตามที่ docstring ระบุไว้ | `add_stock("ITEM001", 0)` |
| 2 | `deduct_stock` | correctness | high | เกิด Partial failure หักสต็อกค้างใน memory เมื่อ IO บันทึกไฟล์พัง | เกิด Error ขณะบันทึกไฟล์ แต่สต็อกใน memory ลดไปแล้ว |
| 3 | `get_average_stock` | correctness | medium | เกิด ZeroDivisionError เมื่อไม่มีรายการสินค้าในระบบ | เรียกใช้งานตอนคลังสินค้าว่างเปล่า `items = []` |
| 4 | `update_inventory_batch` | concurrency | high | เกิด Race Condition เมื่อ 2 Threads แก้ไขข้อมูลพร้อมกัน | Thread A และ B อัปเดตสินค้าชิ้นเดียวกันพร้อมกัน |