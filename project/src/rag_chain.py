import os
from google import genai
from src.vectorstore import VectorStoreManager

class RAGChain:
    def __init__(self):
        # เรียกใช้งาน Gemini API SDK ล่าสุด
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.vector_store_manager = VectorStoreManager()

    def answer_query(self, query: str) -> str:
        """ค้นหาข้อมูลและให้ Gemini สร้างคำตอบจากระเบียบการ"""
        # 1. ค้นหาเอกสารที่เกี่ยวข้องจาก ChromaDB
        relevant_docs = self.vector_store_manager.search(query, k=3)
        
        # 2. รวมข้อความ Context จากเอกสารที่เจอ
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # ถ้าไม่เจอข้อมูลที่เกี่ยวข้อง
        if not context:
            return "ขออภัยครับ ไม่พบข้อมูลระเบียบการที่เกี่ยวข้องกับคำถามนี้ในระบบ"

        # 3. กำหนด Prompt และส่งให้ Gemini สังเคราะห์คำตอบ
        prompt = f"""
คุณเป็นผู้ช่วยอัจฉริยะสำหรับตอบคำถามระเบียบการศึกษาและหลักสูตร
โปรดตอบคำถามโดยอ้างอิงจากข้อมูลที่กำหนดให้ด้านล่างเท่านั้น ห้ามแต่งเติมเอง หากไม่มีข้อมูลให้บอกว่าไม่ทราบ

ข้อมูลอ้างอิง:
{context}

คำถามจากผู้ใช้: {query}
คำตอบ:
"""
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text