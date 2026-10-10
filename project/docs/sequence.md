sequenceDiagram
    autonumber
    actor User as User
    participant API as FastAPI
    participant Chain as RAGChain
    participant VS as ChromaDB
    participant LLM as GeminiAPI

    User->>API: POST /ask {"question": "ระเบียบการ"}
    API->>Chain: invoke(question)
    Chain->>VS: retrieve context
    VS-->>Chain: return chunks
    Chain->>LLM: generate answer
    LLM-->>Chain: return response
    Chain-->>API: format result
    API-->>User: HTTP 200 OK