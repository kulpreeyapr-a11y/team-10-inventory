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