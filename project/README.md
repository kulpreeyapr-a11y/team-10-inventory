# Course & Regulation RAG Assistant (ระบบผู้ช่วยตอบคำถามเอกสารหลักสูตรและระเบียบภาควิชา)

## 1. ภาพรวมโครงการ (Problem & Goal)
นักศึกษาและผู้รับบริการ มักมีคำถามเกี่ยวกับระเบียบการลงทะเบียนเรียน, มคอ.3, และเงื่อนไขการสำเร็จการศึกษา ซึ่งต้องใช้เวลาในการค้นหาจากเอกสาร PDF หลายฉบับ และสร้างภาระงานแก่เจ้าหน้าที่ภาควิชาในการตอบคำถามเดิมซ้ำๆ 

โครงการนี้จึงสร้างขึ้นเพื่อพัฒนาระบบผู้ช่วยฉลาด (RAG Assistant) ที่สามารถค้นหาและตอบคำถามจากเอกสารหลักสูตรและระเบียบภาควิชาด้วยภาษาธรรมชาติได้อย่างถูกต้อง รวดเร็ว และมีการอ้างอิงแหล่งที่มา (Citation) ที่ตรวจสอบได้

## 2. กลุ่มผู้ใช้หลัก (Stakeholders)
* **ผู้ใช้งานหลัก (End User):** นักศึกษา และอาจารย์ที่ปรึกษา
* **ผู้ดูแลข้อมูล (Data Manager):** เจ้าหน้าที่ภาควิชา และ Admin

## 3. ขอบเขตของระบบ (Scope)
* **In Scope:**
  * การสืบค้นคำถาม-คำตอบผ่าน RAG (Retrieval-Augmented Generation) จากเอกสาร PDF ระเบียบภาควิชา
  * การแสดง Citation อ้างอิงชื่อเอกสารและหน้า/ข้อความที่เกี่ยวข้อง
  * ระบบหลังบ้านสำหรับเจ้าหน้าที่ในการอัปโหลด/จัดการไฟล์ PDF
  * ระบบประเมินผลความแม่นยำ (AI Regression Eval Suite) และ Audit Log
* **Out of Scope:**
  * การลงทะเบียนเรียนหรือยื่นคำร้องเปลี่ยนเกรดจริงในระบบทะเบียน
  * ระบบชำระเงินค่าธรรมเนียมการศึกษา

## 4. วิธีการติดตั้งและรันระบบ (Setup Guide)
```bash
# 1. Clone repository
git clone [https://github.com/](https://github.com/)<username>/swe-inventory-67332310152-9.git
cd project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run FastAPI Backend
python -m uvicorn src.main:app --reload

# 4. Run Tests & Evals
pytest tests/ -v
python evals/eval_runner.py