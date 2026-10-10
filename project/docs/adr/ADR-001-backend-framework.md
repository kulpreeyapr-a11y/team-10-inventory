# ADR-001: เลือกใช้ FastAPI เป็น Backend Framework

## Status
Accepted (อนุมัติใช้งาน)

## Context (บริบทของปัญหา)
ระบบ RAG Assistant จำเป็นต้องมี Backend ที่สามารถสร้าง REST API เพื่อรับคำถามจากผู้ใช้ ส่งต่อไปประมวลผลใน RAG Pipeline และส่งคำตอบกลับได้อย่างรวดเร็ว รวมถึงต้องรองรับการทำงานร่วมกับระบบทดสอบ (Pytest) ได้ดี

## Decision (การตัดสินใจ)
เลือกใช้ **FastAPI (Python)** เป็น Backend Framework หลักของโครงการ

## Consequences (ผลกระทบและข้อดี-ข้อเสีย)
* **ข้อดี:** 
  * มีความเร็วสูง (High Performance) เทียบเท่า NodeJS/Go เนื่องจากสร้างบน Starlette และ Pydantic
  * รองรับการทำ Type Hint สมบูรณ์แบบ ช่วยลด Bug ตั้งแต่ขั้นตอนเขียนโค้ด
  * มีระบบสร้าง Interactive API Documentation (Swagger UI) อัตโนมัติ ช่วยให้การทดสอบและทำ Demo สะดวกมาก
* **ข้อเสีย/ความท้าทาย:** 
  * ทีมต้องทำความเข้าใจการใช้งาน Asynchronous programming ในบางจุด (แม้ว่าจะใช้งานแบบ Synchronous พื้นฐานได้)