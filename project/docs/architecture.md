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