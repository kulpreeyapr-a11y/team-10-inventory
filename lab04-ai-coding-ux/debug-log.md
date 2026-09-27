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


---

# Debugging Log - Step 8 (New Test Suite)

## Point 3: Test `test_apply_discount_basic` & `test_bulk_total` ไม่ผ่าน

### 1. Reproduce
- **คำสั่งรัน:** `& "C:\Users\ployk\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pytest`
- **Assertion Failure:** `assert 99.9 == 90.0` และ `assert 299.9 == 270.0`

### 2. Traceback
```text
tests\test_discount.py:10: in test_apply_discount_basic
    assert apply_discount(100.0, 10) == 90.0
E   assert 99.9 == 90.0
```

### 3. สมมติฐาน
สูตรคำนวณส่วนลดเปอร์เซ็นต์ในฟังก์ชัน apply_discount มีการหารตัวเลขผิดพลาด ทำให้ค่าส่วนลดที่ออกมาน้อยกว่าความเป็นจริงมาก

### 4. การยืนยัน
ตรวจสอบโค้ดใน apply_discount พบว่ามีการนำ discount_percent ไปหารด้วย 1000 แทนที่จะเป็น 100

### 5. Root cause และการแก้
Root cause: ตัวหารในสูตรคำนวณส่วนลดผิดพลาด (ใช้ 1000.0 แทนที่จะเป็น 100.0)
การแก้: แก้ไขใน discount.py ให้เป็น return price * (1 - discount_percent / 100.0)



## Point 4: Test 
`test_average_price_empty` ไม่ผ่าน

### 1. Reproduce
- **คำสั่งรัน:** `& "C:\Users\ployk\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pytest`
- **Error:** `ZeroDivisionError: division by zero`

### 2. Traceback
```text
discount.py:20: in average_price
    return sum(prices) / len(prices)
E   ZeroDivisionError: division by zero
```

### 3. สมมติฐาน
ฟังก์ชัน average_price ไม่ได้รองรับกรณีส่งลิสต์ว่าง [] เข้ามา ทำให้เกิดการนำ sum ไปหารด้วย len([]) ซึ่งมีค่าเป็น 0

### 4. การยืนยัน
ทดลองส่ง prices = [] เข้าฟังก์ชัน เกิด ZeroDivisionError ทันที

### 5. Root cause และการแก้
Root cause: ขาด Guard Clause สำหรับเช็คกรณีลิสต์ว่าง
การแก้: เพิ่มเงื่อนไข if not prices: return 0.0 ไว้ตอนต้นฟังก์ชัน average_price



## Point 5: Test 
`test_cheapest_n ไม่ผ่าน

### 1. Reproduce
- **คำสั่งรัน:** `& "C:\Users\ployk\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pytest`
- **Assertion Failure:** `assert [20.0] == [10.0, 20.0]`

### 2. Traceback
```text
tests\test_discount.py:35: in test_cheapest_n
    assert cheapest_n([50.0, 10.0, 30.0, 20.0], 2) == [10.0, 20.0]
E   assert [20.0] == [10.0, 20.0]
```

### 3. สมมติฐาน
ฟังก์ชัน cheapest_n ไม่ได้ทำการเรียงลำดับราคาจากน้อยไปมากก่อนทำการ Slice ดึงข้อมูล หรือมี Logic การ Slice ที่ผิดพลาด

### 4. การยืนยัน
ตรวจสอบโค้ดพบว่าไม่มีการสั่ง sorted() ข้อมูลก่อน คืนค่ากลับไปแบบผิดลำดับ

### 5. Root cause และการแก้
Root cause: ขาดขั้นตอนการเรียงลำดับราคาสินค้า (Sorting)
การแก้: แก้ไขฟังก์ชันให้เรียงลำดับด้วย sorted_prices = sorted(prices) แล้วคืนค่า sorted_prices[:n]