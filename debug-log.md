# Code Review & Debugging Log

## 1. AI-Generated Code Review (Lab 5)
- **Component:** Inventory Item Management / Product Add Form
- **AI Suggestion:** ใช้โค้ดรับค่าฟอร์มโดยตรงผ่าน Request โดยไม่ตรวจสอบประเภทข้อมูล
- **Root Cause & Fix:** ได้ตรวจสอบและพบว่าเสี่ยงต่อข้อมูลผิดพลาด จึงเพิ่มการตรวจสอบ Validation (Data Type Validation) ด้วยตนเองเพื่อความปลอดภัย