import os
from dotenv import load_dotenv  # <-- เพิ่มบรรทัดนี้
import google.generativeai as genai
from src.vectorstore import VectorStoreManager

# โหลดตัวแปรจากไฟล์ .env เข้าสู่ระบบ
load_dotenv()  # <-- เพิ่มบรรทัดนี้

class RAGChain:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("ไม่พบ GEMINI_API_KEY ในไฟล์ .env กรุณาตรวจสอบอีกครั้ง")
            
        genai.configure(api_key=api_key)
        self.vector_store_manager = VectorStoreManager()
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def answer_query(self, query: str) -> str:
        relevant_docs = self.vector_store_manager.search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        if not context:
            return "ขออภัยครับ ไม่พบข้อมูลระเบียบการที่เกี่ยวข้องกับคำถามนี้ในระบบ"

        prompt = f"""
คุณเป็นผู้ช่วยอัจฉริยะสำหรับตอบคำถามระเบียบการศึกษาและหลักสูตร
โปรดตอบคำถามโดยอ้างอิงจากข้อมูลที่กำหนดให้ด้านล่างเท่านั้น ห้ามแต่งเติมเอง หากไม่มีข้อมูลให้บอกว่าไม่ทราบ

ข้อมูลอ้างอิง:
{context}

คำถามจากผู้ใช้: {query}
คำตอบ:
"""
        response = self.model.generate_content(prompt)
        return response.text