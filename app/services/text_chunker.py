from app.models import DocumentChunk, DocumentPage

"""
text_chunker.py

Splits extracted document pages into smaller overlapping text sections.

The chunks will later be converted into embeddings and used for
semantic retrieval.
"""
# Split document pages into overlapping word-based chunks.
# Returns a list of DocumentChunk objects.
def create_chunks(
    pages: list[DocumentPage],                                 # Pages extracted from the uploaded PDF
    chunk_size: int = 180,                                     # Maximum number of words in each chunk
    overlap: int = 30                                          # Number of words shared by two consecutive chunks
):                                                             # list[DocumentChunk]
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    chunks: list[DocumentChunk] = []

    for page in pages:
        words = page.text.split()                              # Split the page text into individual words
        start = 0
        chunk_index = 1                                        # Keep track of the chunk number for each page to create unique chunk IDs

        while start < len(words):
            end = min(start + chunk_size, len(words))

            chunk_text = " ".join(words[start:end])

            chunks.append(
                DocumentChunk(
                    # Unique chunk ID based on the page number and chunk index
                    chunk_id=f"page-{page.page_number}-chunk-{chunk_index}",        
                    page_number=page.page_number,
                    text=chunk_text,
                )
            )

            # Stop when the final words of the page have been processed.
            if end == len(words):
                break

            # Move forward while preserving context from the previous chunk.
            start = end - overlap
            chunk_index += 1
    # Return the list of DocumentChunk objects representing the smaller overlapping text sections
    return chunks          