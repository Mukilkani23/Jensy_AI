import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Mocks
class MockCollection:
    def add(self, **kwargs): pass
    def query(self, **kwargs): return {"documents": [["Mock context from PDF"]]}


load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

# Setup ChromaDB persistent client
chroma_client = None
collection = MockCollection()


async def extract_and_store_pdf(file_bytes: bytes, file_id: str, metadata: dict):
    text = "Mock PDF Content"

        
    # Simple chunking (approx 500 tokens = ~2000 characters)
    chunk_size = 2000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    if not chunks:
        return
        
    # Get embeddings
    # Using async openai client to get embeddings
    response = await client.embeddings.create(
        input=chunks,
        model="text-embedding-3-small"
    )
    embeddings = [data.embedding for data in response.data]
    
    # Store in ChromaDB
    ids = [f"{file_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [metadata for _ in chunks]
    
    collection.add(
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )

async def ask_rag(question: str, subject_code: str = None) -> str:
    # Embed question
    response = await client.embeddings.create(
        input=[question],
        model="text-embedding-3-small"
    )
    q_embedding = response.data[0].embedding
    
    # Query ChromaDB
    where_clause = {"subject_code": subject_code} if subject_code else None
    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=3,
        where=where_clause
    )
    
    context = ""
    if results and results['documents'] and results['documents'][0]:
        context = "\n\n".join(results['documents'][0])
        
    if not context:
        return "I couldn't find any relevant information in the uploaded resources."
        
    # Generate answer
    prompt = f"""Use the following context from the course materials to answer the question.
If the answer is not in the context, say "I don't know based on the uploaded materials."

Context:
{context}

Question: {question}
Answer:"""

    chat_response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3
    )
    
    return chat_response.choices[0].message.content
