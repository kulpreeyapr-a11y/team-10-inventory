from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_document(file_path: str):
    """อ่านไฟล์ PDF ระเบียบการจริง และตัดแบ่งข้อความ (Chunking) เป็นส่วนย่อยๆ"""
    # 1. ใช้ PyPDFLoader โหลดเอกสาร PDF ตาม path ที่ส่งเข้ามา
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    # 2. ตั้งค่าตัวตัดแบ่งข้อความ (Chunking Strategy)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,     # ขนาดความยาวของแต่ละ chunk (ตัวอักษร)
        chunk_overlap=50    # ระยะเวลาเหลื่อมกันระหว่าง chunk เพื่อไม่ให้บริบทขาดหาย
    )
    
    # 3. สไลด์ข้อความจากเอกสาร PDF ทั้งหมดให้เป็นก้อนย่อยๆ พร้อมใช้งาน
    chunks = text_splitter.split_documents(pages)
    return chunks