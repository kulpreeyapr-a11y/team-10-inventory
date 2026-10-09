# รายงานช่องว่างของ Test สำหรับเมธอด sell (Test Gap Analysis)

| กรณีที่ AI ให้มา (Happy Path พื้นฐาน) | กรณีที่ขาด (Edge Cases / Error Paths) | Test ที่เราเขียนเสริม |
|---|---|---|
| ขายสินค้าในจำนวนปกติที่พอกับสต็อก | ขายเท่ากับจำนวนคงเหลือทั้งหมดพอดี (Boundary) | `test_sell_exact_all()` |
| - | ขายจำนวนติดลบหรือขาย 0 (Invalid Input) | `test_sell_zero_or_negative()` |
| - | ขายเกินจำนวนสินค้าคงเหลือในคลัง (Error Path) | `test_sell_exceed_stock()` |
| - | ขายสินค้าที่ไม่มีอยู่ในระบบ (KeyError) | `test_sell_item_not_found()` |
| - | ส่งค่าจำนวนหรือข้อมูลที่ไม่ใช่ตัวเลขที่ถูกต้อง (Data Type) | `test_sell_invalid_type()` |