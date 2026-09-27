# Debugging Log - discount.py

## Point 1: Test `test_calculate_discount_boundary_1000` ไม่ผ่าน

### 1. Reproduce
- **คำสั่งรัน:** `py -m pytest tests/ -v -o pythonpath=.`
- **Assertion Failure:** `assert 0.0 == 50.0` (Expected 50.0, got 0.0)

### 2. Traceback
```text
tests/test_discount.py:15: in test_calculate_discount_boundary_1000
    assert calculate_discount(1000) == 50.0
discount.py:17: in calculate_discount
    elif amount > 1000:
E   assert 0.0 == 50.0

```
### 3. สมมติฐาน
เงื่อนไขตรวจสอบยอดซื้อใช้เครื่องหมายมากกว่าอย่างเดียว (amount > 1000) ทำให้เมื่อยอดซื้อเท่ากับ 1,000 บาทพอดี โค้ดมองว่าข้ามเงื่อนไขนี้ไป และส่งค่าส่วนลดคืนกลับมาเป็น 0.0

### 4. การยืนยัน
ทดลองรันเงื่อนไข 1000 > 1000 ใน Python Shell ได้ผลลัพธ์เป็น False ยืนยันว่าค่าตรงขอบเขตจะไม่เข้าเงื่อนไขนี้

### 5. Root cause และการแก้
Root cause: การเลือกใช้ Relational Operator ผิดประเภท (> แทนที่จะเป็น >=) ทำให้ไม่ครอบคลุมค่าตรงขอบเขตพอดี

การแก้: แก้ไขเงื่อนไขใน discount.py จาก amount > 1000 เป็น amount >= 1000 และ amount > 5000 เป็น amount >= 5000 เพื่อให้รวมยอดซื้อ 1,000 และ 5,000 บาทเข้าเงื่อนไขส่วนลด






---

## Point 2: Test `test_apply_coupon_valid_SAVE10` ไม่ผ่าน

### 1. Reproduce
- **คำสั่งที่รัน:** `py -m pytest tests/ -v -o pythonpath=.`
- **Assertion ที่ fail:** `AssertionError: assert 100.0 == 145.0`

### 2. Traceback
```text
tests/test_discount.py:57: in test_apply_coupon_valid_SAVE10
    assert apply_coupon(1000, "SAVE10") == 145.0
E   AssertionError: assert 100.0 == 145.0

```
### 3. สมมติฐาน
ฟังก์ชัน apply_coupon มีการเรียกใช้ calculate_discount(1000) เพื่อคำนวณราคาส่วนลดตั้งต้น เมื่อ calculate_discount ทำงานผิดพลาด ณ จุดขอบเขต 1,000 บาท จึงทำให้ส่วนลดคูปองคำนวณผิดพลาดตามไปด้วย

### 4. การยืนยัน
ตรวจสอบการทำงานของ apply_coupon พบว่า Logic คำนวณคูปองถูกต้องแล้ว แต่ผลลัพธ์ของ base_discount ที่ส่งมาจาก calculate_discount(1000) ได้ค่าเป็น 0.0 ซึ่งไม่ถูกต้อง

### 5. Root cause และการแก้
Root cause: เกิดผลกระทบสืบเนื่อง (Side Effect) จาก Bug ขอบเขตในฟังก์ชัน calculate_discount
การแก้: เมื่อทำการแก้ไข Bug ขอบเขตที่ calculate_discount เรียบร้อยแล้ว ฟังก์ชัน apply_coupon ก็กลับมาทำงานถูกต้องและทดสอบผ่านทั้งหมดโดยไม่ต้องแก้โค้ดภายในตัวมันเอง