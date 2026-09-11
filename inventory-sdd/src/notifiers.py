from typing import Protocol


class Notifier(Protocol):
    """Protocol สำหรับการส่งข้อความแจ้งเตือน"""
    def send(self, message: str) -> None:
        ...


class EmailNotifier:
    """ส่งการแจ้งเตือนผ่าน Email"""
    def __init__(self, email: str = "manager@example.com") -> None:
        self.email = email

    def send(self, message: str) -> None:
        print(f"[Email to {self.email}] {message}")


class SMSNotifier:
    """ส่งการแจ้งเตือนผ่าน SMS"""
    def __init__(self, phone_number: str = "081-234-5678") -> None:
        self.phone_number = phone_number

    def send(self, message: str) -> None:
        print(f"[SMS to {self.phone_number}] {message}")


class NotifierFactory:
    """Factory Pattern สำหรับสร้าง Notifier ตามช่องทางที่กำหนด"""
    @staticmethod
    def create(channel: str, **kwargs) -> Notifier:
        channel_clean = channel.lower().strip()
        if channel_clean == "email":
            return EmailNotifier(**kwargs)
        elif channel_clean == "sms":
            return SMSNotifier(**kwargs)
        else:
            raise ValueError(f"ไม่รองรับช่องทางแจ้งเตือน: {channel}")