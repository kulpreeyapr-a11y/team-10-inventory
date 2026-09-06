# Class Diagram

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
    
    class InventoryService {
        +dict products
        +list notifiers
        +add_product(product: Product) None
        +record_stock_in(product_name: str, quantity: int) None
        +record_stock_out(product_name: str, quantity: int) None
        +generate_value_report() dict
        -_notify_managers(product: Product) None
    }

    Product --> Category
    Notifier <|.. EmailNotifier : realization
    Notifier <|.. SMSNotifier : realization
    InventoryService o-- Notifier : dependency
    InventoryService o-- Product : aggregation