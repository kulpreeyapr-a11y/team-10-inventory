from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Course & Regulation RAG Assistant", version="1.0.0")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    source: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Course & Regulation RAG Assistant API"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="คำถามต้องไม่ว่างเปล่า")
    
    # จำลองการตอบคำถามจากระบบ RAG (ในขั้นต่อๆไปจะเชื่อมกับ Vector DB และ Gemini API)
    sample_answer = f"ได้รับคำถามของคุณแล้ว: '{request.question}' - อ้างอิงจากระเบียบภาควิชา ฉบับปี 2568"
    return QueryResponse(answer=sample_answer, source="ระเบียบการศึกษาหมวดวิชาคอมพิวเตอร์ ข้อ 5")