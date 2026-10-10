```markdown
# Requirements Specification

## 1. User Stories & Acceptance Criteria (Given-When-Then)

### US-01: ค้นหาคำตอบจากระเบียบภาควิชา
* **User Story:** As a นักศึกษา, I want สอบถามข้อสงสัยเกี่ยวกับระเบียบหลักสูตรด้วยภาษาธรรมชาติ, so that ได้รับคำตอบที่ถูกต้องรวดเร็วโดยไม่ต้องอ่านเอกสารทั้งหมด
* **Acceptance Criteria:**
  * **Given** มีเอกสารระเบียบอยู่ในระบบอย่างน้อย 1 ฉบับ
  * **When** นักศึกษาพิมพ์ถามว่า "ถ้ารายวิชาบังคับถอนได้ถึงสัปดาห์ไหน"
  * **Then** ระบบตอบคำตอบที่ถูกต้องพร้อมระบุชื่อเอกสารระเบียบและข้อที่อ้างอิง

### US-02: การรับมือเมื่อไม่มีข้อมูลในระบบ
* **User Story:** As a นักศึกษา, I want ระบบแจ้งชัดเจนเมื่อไม่พบข้อมูลในระเบียบ, so that ไม่เข้าใจผิดจากคำตอบที่มั่วขึ้นมา
* **Acceptance Criteria:**
  * **Given** คำถามของผู้ใช้ไม่มีเนื้อหาเกี่ยวข้องในคลังเอกสาร
  * **When** นักศึกษาพิมพ์ถามคำถามที่ไม่มีในระเบียบ
  * **Then** ระบบตอบว่า "ไม่พบข้อมูลในระเบียบที่เกี่ยวข้อง" และไม่สร้างคำตอบเท็จ (Hallucination)

### US-03: อัปโหลดเอกสารระเบียบใหม่
* **User Story:** As a เจ้าหน้าที่ภาควิชา, I want อัปโหลดเอกสาร PDF ระเบียบฉบับปรับปรุง, so that ข้อมูลในระบบเป็นปัจจุบันเสมอ
* **Acceptance Criteria:**
  * **Given** เจ้าหน้าที่ล็อกอินเข้าสู่ระบบหลังบ้าน
  * **When** อัปโหลดไฟล์ PDF ระเบียบใหม่สำเร็จ
  * **Then** ระบบทำ Document Chunking และ Update Vector Store พร้อมใช้งานภายใน 1 นาที

## 2. FURPS+ Classification
* **Functionality:** ค้นหาด้วย Semantic Search, สรุปเนื้อหาด้วย LLM, อัปโหลด PDF, แสดง Citation
* **Usability:** รองรับภาษาไทย สื่อสารเข้าใจง่าย มีข้อความเตือนเมื่อหาไม่เจอ
* **Reliability:** มี Fallback behavior เมื่อ LLM Provider ล่ม
* **Performance:** ตอบคำถามคำค้นหาเสร็จสิ้นภายในเวลาที่กำหนด
* **Supportability:** โครงสร้างโค้ดแบบ Modular แยกส่วน RAG Service และ API ชัดเจน

## 3. Non-Functional Requirements (NFRs for AI Feature)
* **NFR-01 (Latency):** Response time (p95) ของการตอบคำถาม RAG ต้องไม่เกิน 3.0 วินาที
* **NFR-02 (Hallucination Tolerance / Faithfulness):** Faithfulness Score จากการประเมินต้อง $\ge 90\%$ และต้องอ้างอิง Citation ทุกครั้ง
* **NFR-03 (Cost Ceiling):** ควบคุมค่าใช้จ่าย API ของ LLM ไม่ให้เกิน $5 (ประมาณ 175 บาท) ต่อเดือน
* **NFR-04 (Fallback Behavior):** หาก LLM API ขัดข้อง ระบบต้องเปลี่ยนไปแสดงข้อความแนะนำช่องทางติดต่อเจ้าหน้าที่ภาควิชาโดยตรง