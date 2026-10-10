# Tech Stack Specifications

## 1. Selected Technologies
* **Programming Language:** Python 3.11+
* **Backend Framework:** FastAPI (สำหรับสร้าง REST API)
* **Vector Database:** ChromaDB (Local / Embedded Vector Store)
* **LLM & Embedding Provider:** Google Gemini API / Gemini Embedding (ผ่าน Google AI Studio Free Tier)
* **Document Processing:** PyPDF2 / LangChain TextSplitter
* **Testing:** Pytest

## 2. Alternatives Considered & Decision Rationale
* **Vector DB (Pinecone vs ChromaDB):** เลือก ChromaDB เพราะสามารถรันแบบ Local ได้ทันที ไม่มีค่าใช้จ่าย และจัดการขอบเขตข้อมูลเอกสารภาควิชาได้สะดวกรวดเร็ว
* **LLM Provider (OpenAI vs Gemini):** เลือก Gemini เนื่องจากมี Free Tier ช่วยควบคุมค่าใช้จ่ายไม่ให้เกินงบตาม NFR ที่ตั้งไว้

# System Specification (Spec ของระบบ)
## Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **AI Model & Embedding:** Google Generative AI (`models/gemini-embedding-001` และ Gemini Model สำหรับสร้างคำตอบ)
* **Environment Management:** `python-dotenv`