import sys
import os

# เพิ่ม Path ปัจจุบันให้ Python มองเห็นโฟลเดอร์ src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_chain import RAGChain

app = FastAPI(
    title="Course & Regulation RAG Assistant API",
    description="API สำหรับระบบค้นหาและตอบคำถามระเบียบการศึกษาและหลักสูตร",
    version="1.0.0"
)

try:
    rag_chain = RAGChain()
except Exception as e:
    # ปริ้นท์ Error ตัวจริงออกดูที่ Terminal ชัดๆ
    print("❌ ERROR ตอนสร้าง RAGChain:", str(e))
    raise e  # ให้พ่น Error ออกมาตรงๆ เลย

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str

@app.get("/")
def read_root():
    return {"status": "success", "message": "Course & Regulation RAG Assistant API is running!"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    if not rag_chain:
        raise HTTPException(status_code=500, detail="RAG Chain ไม่ได้ถูกเริ่มต้นอย่างถูกต้อง")
    
    try:
        answer = rag_chain.answer_query(request.question)
        return {
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        # พิมพ์ตัว Error จริงๆ ออกมาดูที่ Terminal แบบละเอียด
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)