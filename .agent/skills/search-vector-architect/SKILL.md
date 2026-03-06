---
name: search-vector-architect
description: Vector search (RAG) and Elasticsearch. Use for search and vector database tasks.
triggers:
  - "vector search"
  - "RAG"
  - "elasticsearch"
  - "semantic search"
---

# Search Vector Architect Skill

## Identity

You are a search and vector database specialist focused on implementing semantic search and RAG systems.

## When to Use

- Building search functionality
- Implementing RAG systems
- Setting up vector databases
- Semantic search implementations

## Vector Search Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Query     │────▶│  Embedding  │────▶│   Vector    │
│   Input     │     │   Model     │     │   Search    │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Result    │◀────│   Score &   │◀────│   Vector    │
│   Output    │     │   Rank      │     │   Store     │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Embedding Generation

```python
# embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class EmbeddingGenerator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # for all-MiniLM-L6-v2

    def generate(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

    def generate_single(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        return self.model.encode([text])[0]

# Usage
generator = EmbeddingGenerator()
embeddings = generator.generate([
    "The quick brown fox jumps over the lazy dog.",
    "A fast animal leaped across a sleeping canine."
])

# Compare similarity
similarity = np.dot(embeddings[0], embeddings[1])
print(f"Similarity: {similarity:.3f}")
```

## Pinecone Implementation

```python
# vector_store.py
from pinecone import Pinecone, ServerlessSpec
import os

class VectorStore:
    def __init__(self, index_name: str = "documents"):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = index_name
        self.dimension = 384
        self._ensure_index()
        self.index = self.pc.Index(index_name)

    def _ensure_index(self):
        """Create index if it doesn't exist"""
        if self.index_name not in [i.name for i in self.pc.list_indexes()]:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

    def upsert(self, vectors: list[dict]):
        """Insert vectors into the index"""
        # vectors format: [{"id": "1", "values": [...], "metadata": {...}}, ...]
        self.index.upsert(vectors=vectors)

    def query(self, query_vector: list, top_k: int = 10, filter: dict = None):
        """Search for similar vectors"""
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter
        )
        return results.matches

    def delete(self, ids: list[str]):
        """Delete vectors by ID"""
        self.index.delete(ids=ids)

# Usage
store = VectorStore()

# Insert documents
vectors = [
    {"id": "doc1", "values": embedding1.tolist(), "metadata": {"title": "Document 1"}},
    {"id": "doc2", "values": embedding2.tolist(), "metadata": {"title": "Document 2"}}
]
store.upsert(vectors)

# Search
results = store.query(query_embedding.tolist(), top_k=5)
```

## RAG Implementation

```python
# rag.py
from typing import List
from dataclasses import dataclass

@dataclass
class Document:
    id: str
    content: str
    metadata: dict

class RAGSystem:
    def __init__(self, vector_store, embedding_generator, llm_client):
        self.vector_store = vector_store
        self.embedder = embedding_generator
        self.llm = llm_client

    def index_documents(self, documents: List[Document]):
        """Index documents into vector store"""
        vectors = []
        for doc in documents:
            embedding = self.embedder.generate_single(doc.content)
            vectors.append({
                "id": doc.id,
                "values": embedding.tolist(),
                "metadata": {**doc.metadata, "content": doc.content}
            })
        self.vector_store.upsert(vectors)

    def retrieve(self, query: str, top_k: int = 5) -> List[Document]:
        """Retrieve relevant documents for a query"""
        query_embedding = self.embedder.generate_single(query)
        results = self.vector_store.query(query_embedding.tolist(), top_k)

        return [
            Document(
                id=r.id,
                content=r.metadata.get("content", ""),
                metadata={k: v for k, v in r.metadata.items() if k != "content"}
            )
            for r in results
        ]

    def generate_answer(self, query: str, context_docs: List[Document]) -> str:
        """Generate answer using retrieved context"""
        context = "\n\n".join([doc.content for doc in context_docs])

        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""

        response = self.llm.generate(prompt)
        return response

    def query(self, question: str, top_k: int = 5) -> dict:
        """Full RAG query pipeline"""
        docs = self.retrieve(question, top_k)
        answer = self.generate_answer(question, docs)

        return {
            "answer": answer,
            "sources": [{"id": d.id, "metadata": d.metadata} for d in docs]
        }
```

## Elasticsearch Setup

```python
# elasticsearch_store.py
from elasticsearch import Elasticsearch, helpers

class ElasticsearchStore:
    def __init__(self, hosts: list[str], index_name: str = "documents"):
        self.es = Elasticsearch(hosts)
        self.index_name = index_name
        self._ensure_index()

    def _ensure_index(self):
        """Create index with proper mappings"""
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(
                index=self.index_name,
                body={
                    "mappings": {
                        "properties": {
                            "content": {"type": "text"},
                            "title": {"type": "text"},
                            "embedding": {
                                "type": "dense_vector",
                                "dims": 384,
                                "index": True,
                                "similarity": "cosine"
                            }
                        }
                    }
                }
            )

    def search_hybrid(self, query: str, query_embedding: list, k: int = 10):
        """Hybrid search combining text and vector search"""
        response = self.es.search(
            index=self.index_name,
            body={
                "size": k,
                "query": {
                    "script_score": {
                        "query": {
                            "match": {"content": query}
                        },
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'embedding') + _score",
                            "params": {"query_vector": query_embedding}
                        }
                    }
                }
            }
        )
        return response["hits"]["hits"]
```

## Tips

- Choose appropriate embedding models for your domain
- Implement chunking for long documents
- Use hybrid search for better results
- Monitor and optimize retrieval quality
- Cache frequently accessed embeddings
