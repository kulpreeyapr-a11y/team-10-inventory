# Code Review Log: inventory_service.py

## Review Checklist & Method Analysis

### 1. เมธอด `sell_batch` - Partial Failure Leaves Dirty State & Concurrency
- **Location:** เมธอด `sell_batch` บรรทัดที่ 18-24
- **Why it is wrong:** 
  1. **State / Partial Failure:** มีการวนลูปขายสินค้าทีละรายการ หากการขายรายการที่ 2 เกิด Exception/Error สินค้าในรายการแรกจะถูกขายไปแล้วโดยไม่มีการ Rollback ทำให้ State ค้าง
  2. **Concurrency:** ไม่ได้ใช้ `self._lock` ครอบ ทำให้หากมี 2 Thread สั่งขายพร้อมกัน ข้อมูลการตัดสต็อกจะขัดแย้งกัน
- **Broken Example:** สั่งขาย `orders = {"apple": 5, "unknown_item": 10}`
  - Expected: ถ้ามีสินค้าที่ไม่มีในคลัง การขายทั้งหมดควรล้มเหลว (Atomic) และสต็อก `apple` ควรเหลือเท่าเดิม
  - Actual: `apple` ถูกหักออกไปแล้ว 5 ชิ้น ก่อนที่ระบบจะ Crash เมื่อเจอ `unknown_item`
- **Proposed Fix:** ทำ Validate รายการสินค้าและจำนวนสต็อกทั้งหมดก่อนทำการตัดจริง หรือใช้ Transaction/Rollback Mechanism
- **Category:** correctness
- **Severity:** high

---

### 2. เมธอด `reserve` - Access Private Attribute & KeyError Edge Case
- **Location:** เมธอด `reserve` บรรทัดที่ 27-32
- **Why it is wrong:** 
  1. เข้าถึง `self._inv._items` โดยตรงซึ่งเป็น Private Attribute 
  2. หากส่งชื่อสินค้าที่ไม่มีในคลังเข้ามาจะเกิด `KeyError` 
  3. ไม่ได้ใช้ `self._lock` เพื่อป้องกัน Race Condition ในการจองสินค้า
- **Broken Example:** เรียก `reserve("non_exist_item", 2)`
  - Expected: ควรคืนค่า 0 หรือ Raise Exception ที่จัดการแล้ว
  - Actual: โปรแกรม Crash ด้วย `KeyError: 'non_exist_item'`
- **Proposed Fix:** เรียกผ่าน Public Method ของ `Inventory` และใช้ Lock ครอบการตรวจสอบและบันทึกการจอง
- **Category:** correctness
- **Severity:** medium

---

### 3. เมธอด `items_in_price_range` - Boundary Condition Bug (คำว่า หรือเท่ากับ)
- **Location:** เมธอด `items_in_price_range` บรรทัดที่ 38
- **Why it is wrong:** Docstring ระบุว่าคืนสินค้าที่ราคาอยู่ในช่วง `[low, high]` (รวมขอบเขตช่วงปิด) แต่โค้ดใช้ `if low < item.price < high:` ซึ่งไม่รวมค่าที่เท่ากับ `low` หรือ `high`
- **Broken Example:** เรียก `items_in_price_range(100.0, 500.0)` โดยมีสินค้าที่ราคา 100.0 บาทพอดี
  - Expected: สินค้าที่ราคา 100.0 บาท ต้องอยู่ในรายชื่อที่คืนกลับมา
  - Actual: สินค้าถูกข้ามไปเนื่องจาก 100.0 ไม่มากกว่า 100.0 (`100.0 < 100.0` เป็น False)
- **Proposed Fix:** แก้ไขเงื่อนไขเป็น `if low <= item.price <= high:`
- **Category:** correctness
- **Severity:** medium

---

### 4. เมธอด `low_stock_report` - Boundary Condition Bug (คำว่า ต่ำกว่าหรือเท่ากับ)
- **Location:** เมธอด `low_stock_report` บรรทัดที่ 46
- **Why it is wrong:** Docstring ระบุว่า คืนรายชื่อสินค้าที่ stock "ต่ำกว่าหรือเท่ากับ" เกณฑ์ (`LOW_STOCK_THRESHOLD = 5`) แต่โค้ดใช้ `if item.quantity < self.LOW_STOCK_THRESHOLD:` (ขาดกรณีเท่ากับ)
- **Broken Example:** มีสินค้าที่มีสต็อกเหลืออยู่ 5 ชิ้นพอดี
  - Expected: สินค้านี้ต้องติดอยู่ในรายงานสินค้าใกล้หมด
  - Actual: สินค้าไม่ถูกใส่ในรายงาน เพราะ 5 ไม่ได้น้อยกว่า 5 (`5 < 5` เป็น False)
- **Proposed Fix:** แก้ไขเงื่อนไขเป็น `if item.quantity <= self.LOW_STOCK_THRESHOLD:`
- **Category:** correctness
- **Severity:** medium

---

### 5. เมธอด `concurrent_restock` - Race Condition Outside Lock
- **Location:** เมธอด `concurrent_restock` บรรทัดที่ 52-54
- **Why it is wrong:** อ่านค่า `current = self._inv._items[name].quantity` **ก่อน** เข้าบล็อก `with self._lock:` ทำให้หากมี 2 Thread อ่านค่าพร้อมกัน ค่า `current` ที่ได้จะเป็นค่าเก่าก่อนเติมทั้งคู่ (Race Condition)
- **Broken Example:** สต็อกเดิมมี 10 ชิ้น, Thread A และ Thread B เรียกเติมสต็อกคนละ 5 ชิ้นพร้อมกัน
  - Expected: สต็อกรวมต้องเป็น 20 ชิ้น
  - Actual: ทั้งสอง Thread อ่าน `current = 10` ออกไปพร้อมกัน แล้วเขียนทับได้ผลลัพธ์เป็น 15 ชิ้น
- **Proposed Fix:** ย้ายการอ่านค่า `current` เข้าไปอยู่ **ภายใน** บล็อก `with self._lock:`
- **Category:** concurrency
- **Severity:** high

---

### 6. เมธอด `average_unit_value` - Zero Division Error & Incorrect Item Count
- **Location:** เมธอด `average_unit_value` บรรทัดที่ 62-63
- **Why it is wrong:** 
  1. หากคลังสินค้าไม่มีสินค้าเลย (`_items` เป็น dict ว่าง) จะเกิด `ZeroDivisionError`
  2. โค้ดใช้นับชนิดสินค้า `len(self._inv._items)` เป็นตัวหาร แทนที่จะหารด้วย **จำนวนชิ้นสินค้าทั้งหมด** (Total Quantity) ตามความหมาย "มูลค่าเฉลี่ยต่อชิ้น"
- **Broken Example:** คลังสินค้าว่างเปล่า เรียก `average_unit_value()`
  - Expected: คืนค่า `0.0`
  - Actual: โปรแกรม Crash ด้วย `ZeroDivisionError: division by zero`
- **Proposed Fix:** คำนวณจำนวนชิ้นสินค้ารวมทั้งหมด (`total_quantity`) เช็คถ้าเป็น 0 ให้คืนค่า 0.0 ไม่เช่นนั้นคืนค่า `total_value / total_quantity`
- **Category:** correctness
- **Severity:** medium

---

## สรุปตารางจัดหมวดและระดับความรุนแรง (Summary Table)

| # | เมธอด | หมวด | ระดับ | สรุปปัญหา | กรณีที่ทำให้พัง |
|---|---|---|---|---|---|
| 1 | `sell_batch` | correctness | high | เกิด Partial Failure เมื่อมีรายการใดรายการหนึ่งขายไม่สำเร็จ | สั่งขายหลายชิ้น รายการแรกผ่าน แต่วายป่วงที่รายการถัดมา |
| 2 | `reserve` | correctness | medium | เข้าถึง Private Attribute และเกิด KeyError เมื่อไม่เจอสินค้า | เรียก `reserve("unknown", 1)` แล้วเกิด KeyError |
| 3 | `items_in_price_range` | correctness | medium | ขาดการเช็คเงื่อนไขขอบเขต "หรือเท่ากับ" ตาม Docstring | สินค้าราคาเท่ากับ `low` หรือ `high` พอดีถูกข้ามไป |
| 4 | `low_stock_report` | correctness | medium | ใช้ `<` แทนที่จะเป็น `<=` ตาม Docstring "ต่ำกว่าหรือเท่ากับ" | สต็อกเหลือ 5 ชิ้นพอดี แต่ไม่ติดในรายงาน |
| 5 | `concurrent_restock` | concurrency | high | อ่านค่าสต็อกนอก Lock ทำให้เกิด Race Condition | 2 Threads อ่านค่าสต็อกเดิมพร้อมกันแล้วเซฟทับ |
| 6 | `average_unit_value` | correctness | medium | เกิด ZeroDivisionError เมื่อไม่มีสินค้าในคลัง | เรียกใช้งานตอนคลังสินค้าว่างเปล่า `_items = {}` |