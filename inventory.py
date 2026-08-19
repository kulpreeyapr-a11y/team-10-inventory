import json
import os

DB_FILE = "inventory.json"

def load_items():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def list_items():
    """US-01: ดูรายการสินค้าทั้งหมด"""
    items = load_items()
    
    # Scenario 2: แจ้งเตือนเมื่อไม่มีข้อมูลสินค้าในระบบ
    if not items:
        print("ยังไม่มีสินค้าในระบบ")
        return
    
    # Scenario 1: แสดงรายการสินค้าทั้งหมดเมื่อมีข้อมูล
    print("\n--- รายการสินค้าคงเหลือ ---")
    for item_id, info in items.items():
        print(f"รหัส: {item_id} | ชื่อ: {info['name']} | จำนวนคงเหลือ: {info['quantity']}")

if __name__ == "__main__":
    list_items()