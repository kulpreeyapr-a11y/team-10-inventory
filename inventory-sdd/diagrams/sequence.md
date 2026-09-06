---

```markdown
# Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Staff as พนักงานคลังสินค้า
    participant Service as InventoryService
    participant Prod as Product
    participant Notifier as Notifier (Email/SMS)

    Staff->>Service: record_stock_out("สายไฟ", 8)
    Service->>Prod: ตรวจสอบจำนวนสต็อกคงเหลือ
    alt สต็อกพอจ่าย
        Service->>Prod: ตัดสต็อก (quantity - 8)
        opt สต็อกหลังจ่าย < threshold
            Service->>Service: _notify_managers(product)
            loop ทุก Notifier ในรายการ
                Service->>Notifier: send(message)
                Notifier-->>Staff: print("[Email/SMS]...")
            end
        end
    else สต็อกไม่พอ
        Service-->>Staff: Raise ValueError("สต็อกไม่พอ")
    end