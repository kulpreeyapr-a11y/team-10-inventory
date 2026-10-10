import pytest
from unittest.mock import MagicMock, patch
from src.loader import load_and_split_document
from src.rag_chain import RAGChain

def test_load_and_split_document_mock():
    """ทดสอบฟังก์ชัน Loader ด้วยการ Mock ข้อมูล PDF"""
    with patch("src.loader.PyPDFLoader") as mock_loader:
        # จำลองหน้าเอกสาร PDF
        mock_page = MagicMock()
        mock_page.page_content = "นี่คือเนื้อหาทดสอบระเบียบการลงทะเบียนเรียนของมหาวิทยาลัย"
        mock_loader.return_value.load.return_value = [mock_page]

        chunks = load_and_split_document("dummy_path.pdf")
        assert len(chunks) > 0
        assert "ระเบียบการลงทะเบียน" in chunks[0].page_content

@patch("src.rag_chain.VectorStoreManager")
@patch("src.rag_chain.genai.Client")
def test_rag_chain_answer(mock_genai_client, mock_vector_store):
    """ทดสอบระบบ RAG Chain ว่าสามารถเรียกใช้งานและตอบกลับได้"""
    # จำลองผลการค้นหาจาก Vector Store
    mock_doc = MagicMock()
    mock_doc.page_content = "การลงทะเบียนล่าช้าทำได้ถึงสัปดาห์ที่ 3"
    mock_vector_store.return_value.search.return_value = [mock_doc]

    # จำลองผลลัพธ์จาก Gemini API
    mock_response = MagicMock()
    mock_response.text = "สามารถลงทะเบียนล่าช้าได้ถึงสัปดาห์ที่ 3 ครับ"
    mock_genai_client.return_value.models.generate_content.return_value = mock_response

    rag = RAGChain()
    answer = rag.answer_query("ลงทะเบียนล่าช้าได้ถึงเมื่อไหร่?")
    
    assert "สัปดาห์ที่ 3" in answer