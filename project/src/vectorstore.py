import os
from chromadb import PersistentClient
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class VectorStoreManager:
    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "course_regulation"):
        # ใช้โมเดล Embedding ของ Google เพื่อแปลงข้อความให้อยู่ในรูป Vector
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=os.environ.get("GEMINI_API_KEY")
        )
        
        # สร้าง Chroma Vector Store แบบบันทึกลงดิสก์ (Persistent)
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

    def add_documents(self, chunks: list):
        """รับ Chunk จาก loader มาเพิ่มลงใน Vector Store"""
        self.vector_store.add_documents(chunks)

    def search(self, query: str, k: int = 3):
        """ค้นหาข้อความใน Vector Store ที่เกี่ยวข้องกับคำถามมากที่สุด k อันดับแรก"""
        results = self.vector_store.similarity_search(query, k=k)
        return results