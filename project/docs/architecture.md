# System Architecture: Course & Regulation RAG Assistant

## 1. C4 Model - System Architecture

### 1.1 Context Diagram (System Context)
* **Users:** นักศึกษา และอาจารย์ สามารถพิมพ์คำถามเกี่ยวกับระเบียบผ่าน User Interface (Frontend)
* **System:** ระบบ RAG Assistant ทำหน้าที่รับคำค้นหา ค้นหาเอกสารที่เกี่ยวข้อง และส่งให้ LLM ประมวลผลคำตอบ
* **External Services:** Google Gemini API (สำหรับสร้าง Embedding และ Generate คำตอบ)

### 1.2 Container Diagram
* **Frontend:** Web Interface (Streamlit / HTML-CSS) สำหรับให้ผู้ใช้งานพิมพ์แชทและอัปโหลด PDF
* **Backend Application:** FastAPI (Python) ทำหน้าที่ควบคุม Business Logic, จัดการ REST API และประสานงานกับ RAG Pipeline
* **Vector Database:** ChromaDB เก็บ Vector Embeddings ของเอกสารระเบียบภาควิชา
* **Relational Database (Optional/Mock):** เก็บประวัติการใช้งานและ Audit Log พื้นฐาน

### 1.3 Component Diagram (Backend Core)
* `API Router (main.py)`: รับ Request จาก Frontend
* `Document Processor`: ตัดแบ่งข้อความเอกสาร PDF เป็น Chunks ย่อย
* `Retrieval Engine`: ค้นหา Chunk ที่มีความหมายใกล้เคียงกับคำถามที่สุดจาก ChromaDB
* `LLM Generator`: ส่ง Context ที่ค้นหาได้ไปให้ Gemini API เพื่อสรุปคำตอบและอ้างอิง Citation

---

## 2. Decision Tree: LLM vs Classical ML vs Rule-Based
* **คำถามทั่วไปเกี่ยวกับระเบียบ/ข้อบังคับ (Semantic Search / Q&A):** เลือกใช้ **LLM + RAG** เนื่องจากข้อมูลมีความซับซ้อนและต้องอาศัยความเข้าใจภาษาธรรมชาติ
* **การตรวจสอบประเภทไฟล์ PDF หรือขนาดไฟล์:** เลือกใช้ **Rule-Based** (เขียนโค้ดตรวจสอบเงื่อนไขตรงๆ) เพราะมีความแม่นยำสูงและไม่ต้องเปลืองต้นทุน AI