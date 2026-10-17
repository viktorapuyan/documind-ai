
import pytest
from sqlalchemy import select

from app.models import Document, DocumentChunk 
from sqlalchemy.exc import IntegrityError

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


def test_duplicate_chunk_index(db_session):
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
        chunk_index=0  # Duplicate chunk_index
    )

    document.chunks.append(chunk1)
    document.chunks.append(chunk2)

    db_session.add(document)

    with pytest.raises(IntegrityError):
        db_session.commit()

def test_invalid_document_reference(db_session):
    chunk = DocumentChunk(
        content="Introduction to machine learning",
        page_number=1,
        chunk_index=0,
        document_id=9999  # Assuming this document ID does not exist
    )

    db_session.add(chunk)

    with pytest.raises(IntegrityError):
        db_session.commit()