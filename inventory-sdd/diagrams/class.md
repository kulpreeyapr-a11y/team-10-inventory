# Class Diagram (Refactored)

```mermaid
classDiagram
    class Category {
        +str name
    }
    
    class Product {
        +str name
        +Category category
        +int quantity
        +float unit_price
        +int threshold
    }
    
    class Notifier {
        <<interface>>
        +send(message: str) None
    }
    
    class EmailNotifier {
        +str email
        +send(message: str) None
    }
    
    class SMSNotifier {
        +str phone_number
        +send(message: str) None
    }

    class NotifierFactory {
        +create(channel: str) Notifier
    }
    
    class InventoryService {
        +dict products
        -list _observers
        +attach_observer(notifier: Notifier) None
        +detach_observer(notifier: Notifier) None
        -_notify_observers(message: str) None
        +add_product(product: Product) None
        +record_stock_in(product_name: str, quantity: int) None
        +record_stock_out(product_name: str, quantity: int) None
        +generate_value_report() dict
    }

    Product --> Category
    Notifier <|.. EmailNotifier : realization
    Notifier <|.. SMSNotifier : realization
    NotifierFactory ..> Notifier : creates
    InventoryService o-- Notifier : observers (Observer Pattern)
    InventoryService o-- Product : aggregation