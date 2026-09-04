from typing import Protocol


class Notifier(Protocol):
    """Protocol สำหรับช่องทางการแจ้งเตือน (DIP)"""
    def send(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือน"""
        ...


class EmailNotifier:
    """ส่งแจ้งเตือนผ่าน Email (ใช้ print แทนส่งจริง)"""
    def __init__(self, email: str) -> None:
        self.email = email

    def send(self, message: str) -> None:
        print(f"[Email Notification] ถึง {self.email}: {message}")


class SMSNotifier:
    """ส่งแจ้งเตือนผ่าน SMS (ใช้ print แทนส่งจริง)"""
    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def send(self, message: str) -> None:
        print(f"[SMS Notification] ถึง {self.phone_number}: {message}")