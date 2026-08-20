import json
import os

# ชื่อไฟล์สำหรับเก็บข้อมูลสตร็อกสินค้า
DATA_FILE = "inventory.json"

def load_data():
    """ฟังก์ชันโหลดข้อมูลจากไฟล์ JSON"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """ฟังก์ชันบันทึกข้อมูลลงไฟล์ JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_item(item_id, name, quantity, price):
    """ฟังก์ชันสำหรับเพิ่มสินค้าใหม่เข้าระบบ (US-02)"""
    items = load_data()
    
    # ตรวจสอบว่ารหัสสินค้าซ้ำหรือไม่
    for item in items:
        if item["id"] == item_id:
            print(f"Error: รหัสสินค้า {item_id} มีอยู่ในระบบแล้ว!")
            return False

    # สร้างโครงสร้างข้อมูลสินค้าใหม่
    new_item = {
        "id": item_id,
        "name": name,
        "quantity": int(quantity),
        "price": float(price)
    }
    
    items.append(new_item)
    save_data(items)
    print(f"เพิ่มสินค้า '{name}' เข้าระบบเรียบร้อยแล้ว!")
    return True

# ตัวอย่างการเรียกใช้งาน
if __name__ == "__main__":
    # ทดสอบเพิ่มสินค้า
    add_item("P001", "เสื้อยืด", 10, 199.00)