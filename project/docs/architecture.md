# System Architecture & Diagrams

## Class Diagram
```mermaid
classDiagram
    class DocumentLoader {
        +str file_path
        +load_pdf() list
    }
    class VectorStoreManager {
        +str db_path
        +add_documents(chunks) void
        +get_retriever() retriever
    }
    class RAGChain {
        +retriever retriever
        +llm model
        +invoke(question: str) dict
    }
    class APIRouter {
        +ask_question(query: QueryModel) dict
    }
    RAGChain --> VectorStoreManager : uses retriever
    APIRouter --> RAGChain : calls invoke
    VectorStoreManager --> DocumentLoader : loads data

    sequenceDiagram
    autonumber
    actor User as ผู้ใช้งาน
    participant API as FastAPI (main.py)
    participant Chain as RAGChain
    participant VS as ChromaDB (VectorStore)
    participant LLM as Google Gemini API

    User->>API: POST /ask {"question": "คำถามระเบียบการ"}
    API->>Chain: invoke(question)
    Chain->>VS: ค้นหาเอกสารที่เกี่ยวข้อง (Retrieval)
    VS-->>Chain: ส่งคืนข้อมูลข้อความระเบียบการ
    Chain->>LLM: ส่ง Prompt + Context + คำถามไปยัง Gemini
    LLM-->>Chain: สังเคราะห์คำตอบ
    Chain-->>API: ส่งผลลัพธ์คำตอบกลับ
    API-->>User: ตอบกลับ JSON (Status 200 OK)