
from sqlalchemy import select

from app.models import Document, DocumentChunk 

def test_create_document(db_session):
    document = Document(
        filename="machine_learning.pdf",
    )

    db_session.add(document)
    db_session.commit()

    selected_document = db_session.scalars(select(Document).where(Document.id == document.id)).one()
    
    assert selected_document.filename == "machine_learning.pdf"
    assert selected_document.status == "pending"
    assert selected_document.id is not None



def test_document_chunks_relationship(db_session):
    document = Document(
        filename="machine_learning.pdf"
    )

    chunk1 = DocumentChunk(
        content="Introduction to machine learning",
        page_number=1,
        chunk_index=0
    )

    chunk2 = DocumentChunk(
        content="Supervised learning uses labeled data",
        page_number=1,
        chunk_index=1
    )

    document.chunks.append(chunk1)
    document.chunks.append(chunk2)

    db_session.add(document)
    db_session.commit()

    selected_document = db_session.scalars(select(Document).where(Document.id == document.id)).one()

    assert len(selected_document.chunks) == 2
