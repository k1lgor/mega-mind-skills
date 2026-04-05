---
name: search-vector-architect
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Design and implement production-grade semantic search and RAG systems: embedding model selection, chunking strategy, hybrid search (BM25 + vector), reranking, retrieval evaluation (NDCG, MRR), and production concerns (latency, index size, cost). Use when building search infrastructure, RAG pipelines, or troubleshooting retrieval quality in LLM-powered applications.
triggers:
  - "vector search"
  - "RAG"
  - "elasticsearch"
  - "semantic search"
  - "embedding"
  - "hybrid search"
  - "reranking"
  - "chunking strategy"
  - "retrieval quality"
  - "NDCG"
  - "MRR"
  - "hallucination"
  - "retrieval miss"
  - "Pinecone"
  - "Weaviate"
  - "pgvector"
---

# Search Vector Architect Skill

## Identity

You are a search and retrieval systems engineer who designs pipelines that LLMs can reason over accurately. You understand that retrieval quality is the primary determinant of RAG system quality — a perfect generator cannot fix poor retrieval. You make deliberate trade-offs between semantic accuracy and lexical precision using hybrid search, invest in evaluation infrastructure (NDCG, MRR, recall@k) before optimizing, and treat embedding model selection as a consequential architectural decision — not a default. You know that hallucination in RAG systems is almost always a retrieval failure, not a generation failure, and you diagnose accordingly.

## When to Activate

- Building a new RAG pipeline or semantic search system from scratch
- Selecting an embedding model or vector database for a production use case
- Designing a chunking strategy for a specific document type (code, legal, conversational)
- Implementing hybrid search (BM25 + dense vector) or cross-encoder reranking
- Diagnosing poor retrieval quality: wrong documents returned, hallucinated answers, low recall
- Evaluating retrieval quality with offline metrics (NDCG, MRR, recall@k)
- Migrating from keyword-only search to semantic search
- Optimizing a production search system for latency or index cost
- Troubleshooting LLM answers that cite incorrect or non-existent sources

## When NOT to Use

- **Small, static datasets (<1,000 documents):** Simple TF-IDF or BM25 keyword search is faster, cheaper, fully auditable, and often equally accurate. Vector infrastructure is overkill.
- **Exact lookup only:** If all queries are exact record lookups (by ID, email, order number), use a relational database — no embedding needed.
- **The corpus changes every few minutes:** Dense vector indexes are expensive to update at high frequency. Consider Elasticsearch BM25-only or a streaming index architecture instead.
- **No labeled evaluation set exists:** Do not tune chunking, embedding models, or rerankers without an eval set. You will optimize noise. Build the eval set first.
- **The answer is a simple database query:** Do not route deterministic, structured queries through a RAG pipeline. Structured queries belong in SQL or a query builder.

## Core Principles

1. **Retrieval quality determines answer quality.** Measure recall@k and NDCG before optimizing generation prompts. A 10% retrieval improvement outweighs any prompt engineering gain.
2. **Chunking strategy is the most underrated decision.** The wrong chunk size or boundary creates contexts that straddle concepts, lose metadata, or exceed the embedding model's token limit. Match chunk strategy to document structure.
3. **Hybrid search outperforms pure vector in most production workloads.** Dense vectors handle semantic similarity; BM25 handles exact keyword matches (product codes, names, abbreviations). Combine them with Reciprocal Rank Fusion or a learned combiner.
4. **Embedding models are domain-specific.** A general-purpose embedding model underperforms a domain-fine-tuned one on technical, legal, or medical corpora. Always benchmark your domain before choosing a model.
5. **Reranking is a high-ROI optimization.** A cross-encoder reranker applied to top-50 candidates and returning top-5 consistently improves NDCG by 10-20% with modest latency cost. It is usually worth it.
6. **Production search has a latency budget.** Embedding a query, ANN search, and reranking must all fit within the response latency SLA. Profile each stage independently and set per-stage budgets.
7. **Hallucination is a retrieval signal.** When an LLM fabricates an answer despite having context, it usually means: retrieved chunks lack the answer, chunks are too noisy, or the prompt is not grounding the model to the context. Diagnose retrieval first.

---

## Architecture Overview

```
Query Input
    |
    v
[Query Preprocessing]  (normalize, expand abbreviations)
    |
    +──────────────────────────────────────+
    |                                      |
    v                                      v
[BM25 / Keyword Search]          [Dense Vector Search]
  (Elasticsearch / BM25)           (Pinecone / pgvector)
    |                                      |
    +──────────────────────────────────────+
                    |
                    v
         [Reciprocal Rank Fusion]  (hybrid merge)
                    |
                    v
         [Cross-Encoder Reranker]  (optional, high-accuracy mode)
                    |
                    v
         [Context Assembly]        (select top-k chunks + metadata)
                    |
                    v
         [LLM Generation]          (grounded prompt + citations)
                    |
                    v
         [Answer + Source Refs]
```

---

## Chunking Strategy Decision Guide

Chunking is not a hyperparameter to grid-search — it must match the document structure.

| Document Type | Recommended Strategy | Chunk Size (tokens) | Notes |
|---|---|---|---|
| Long-form articles / docs | Recursive text splitter on paragraphs | 512–1024 | Preserve paragraph boundaries |
| Code files | Split by function/class boundaries | Variable | Never split mid-function |
| Conversational transcripts | Split by speaker turn + time window | 256–512 | Include speaker label in chunk |
| Legal / financial docs | Split by numbered sections or clauses | 512–1024 | Preserve section header in metadata |
| Short product descriptions | No chunking — embed full record | Full | Semantic unit is the record |
| Dense technical manuals | Sentence-level splitting with overlap | 256 with 50-token overlap | Overlap prevents boundary loss |

**Critical rule:** Always include document title, section header, and page/URL as metadata on each chunk. Retrieval without metadata is a dead end for citations.

```python
# src/search/chunker.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    metadata: dict  # {"doc_id", "title", "section", "page", "char_offset"}

def chunk_document(
    text: str,
    doc_metadata: dict,
    chunk_size: int = 512,
    overlap: int = 50,
) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    splits = splitter.split_text(text)
    return [
        Chunk(
            text=split,
            metadata={
                **doc_metadata,
                "chunk_index": i,
                "chunk_total": len(splits),
            },
        )
        for i, split in enumerate(splits)
    ]
```

---

## Embedding Model Selection

| Model | Dim | Max Tokens | Strengths | When to Use |
|---|---|---|---|---|
| text-embedding-3-small (OpenAI) | 1536 | 8192 | General purpose, low cost | Default for English general-domain |
| text-embedding-3-large (OpenAI) | 3072 | 8192 | Higher accuracy, higher cost | When quality matters more than cost |
| all-MiniLM-L6-v2 (local) | 384 | 256 | Fast, offline, zero cost | High-throughput local deployments |
| BAAI/bge-large-en-v1.5 (local) | 1024 | 512 | SOTA open-source English | Production-grade offline search |
| e5-mistral-7b-instruct | 4096 | 32768 | Long-context, instruction-following | Long documents, complex queries |

**Selection rule:** Always run MTEB benchmark on your specific domain before choosing. Do not rely on general leaderboard rankings for specialized corpora.

```python
# src/search/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name: str = "BAAI/bge-large-en-v1.5"):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, texts: list[str], batch_size: int = 64) -> np.ndarray:
        """Batch encode to avoid OOM on large corpora."""
        return self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,  # required for cosine similarity
            show_progress_bar=True,
        )

    def embed_query(self, query: str) -> np.ndarray:
        """BGE models expect a query prefix for asymmetric retrieval."""
        prefixed = f"Represent this sentence for searching relevant passages: {query}"
        return self.model.encode(prefixed, normalize_embeddings=True)
```

---

## Hybrid Search with Reciprocal Rank Fusion

```python
# src/search/hybrid.py
from elasticsearch import Elasticsearch, helpers
from dataclasses import dataclass

@dataclass
class SearchResult:
    id: str
    score: float
    content: str
    metadata: dict

def reciprocal_rank_fusion(
    bm25_results: list[SearchResult],
    vector_results: list[SearchResult],
    k: int = 60,
) -> list[SearchResult]:
    """
    Merge BM25 and vector search results using RRF.
    k=60 is a robust default from the original RRF paper.
    """
    scores: dict[str, float] = {}
    doc_map: dict[str, SearchResult] = {}

    for rank, result in enumerate(bm25_results):
        scores[result.id] = scores.get(result.id, 0) + 1 / (k + rank + 1)
        doc_map[result.id] = result

    for rank, result in enumerate(vector_results):
        scores[result.id] = scores.get(result.id, 0) + 1 / (k + rank + 1)
        doc_map[result.id] = result

    sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)
    return [
        SearchResult(
            id=doc_id,
            score=scores[doc_id],
            content=doc_map[doc_id].content,
            metadata=doc_map[doc_id].metadata,
        )
        for doc_id in sorted_ids
    ]
```

---

## Cross-Encoder Reranking

```python
# src/search/reranker.py
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name, max_length=512)

    def rerank(
        self,
        query: str,
        candidates: list[SearchResult],
        top_k: int = 5,
    ) -> list[SearchResult]:
        """
        Rerank top-N candidates using a cross-encoder.
        Only feasible for small candidate sets (20-100) due to O(n) inference cost.
        """
        pairs = [[query, c.content] for c in candidates]
        scores = self.model.predict(pairs)
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        return [r for r, _ in ranked[:top_k]]
```

---

## Pinecone Vector Store

```python
# src/search/vector_store.py
from pinecone import Pinecone, ServerlessSpec
import os

class VectorStore:
    def __init__(self, index_name: str = "documents", dimension: int = 1024):
        self.pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        self.index_name = index_name
        self.dimension = dimension
        self._ensure_index()
        self.index = self.pc.Index(index_name)

    def _ensure_index(self):
        existing = [i.name for i in self.pc.list_indexes()]
        if self.index_name not in existing:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

    def upsert_chunks(self, chunks: list[dict]):
        """chunks: [{"id": str, "values": list[float], "metadata": dict}]"""
        # Pinecone batch limit is 100 vectors per upsert
        for i in range(0, len(chunks), 100):
            self.index.upsert(vectors=chunks[i : i + 100])

    def query(
        self,
        query_vector: list[float],
        top_k: int = 20,
        filter: dict | None = None,
    ) -> list[dict]:
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter,
        )
        return results.matches
```

---

## RAG System

```python
# src/search/rag.py
from dataclasses import dataclass
from typing import Protocol

@dataclass
class RetrievedContext:
    chunks: list[dict]
    query: str

class RAGSystem:
    def __init__(
        self,
        vector_store: VectorStore,
        embedder: EmbeddingGenerator,
        reranker: Reranker | None = None,
        llm_client=None,
    ):
        self.store = vector_store
        self.embedder = embedder
        self.reranker = reranker
        self.llm = llm_client

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        query_vec = self.embedder.embed_query(query).tolist()
        candidates = self.store.query(query_vec, top_k=20)  # over-fetch for reranker
        if self.reranker:
            results_as_sr = [
                SearchResult(id=c["id"], score=c["score"],
                             content=c["metadata"].get("text", ""),
                             metadata=c["metadata"])
                for c in candidates
            ]
            reranked = self.reranker.rerank(query, results_as_sr, top_k=top_k)
            return [{"content": r.content, "metadata": r.metadata} for r in reranked]
        return [{"content": c["metadata"].get("text", ""), "metadata": c["metadata"]}
                for c in candidates[:top_k]]

    def generate(self, query: str, context: list[dict]) -> str:
        context_text = "\n\n---\n\n".join(
            f"[Source: {c['metadata'].get('title', 'unknown')}]\n{c['content']}"
            for c in context
        )
        prompt = f"""Answer the question using ONLY the provided context.
If the context does not contain the answer, respond: "I don't have enough information to answer this."

Context:
{context_text}

Question: {query}

Answer:"""
        response = self.llm.messages.create(
            model="claude-haiku-3-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def query(self, question: str) -> dict:
        chunks = self.retrieve(question)
        answer = self.generate(question, chunks)
        return {
            "answer": answer,
            "sources": [c["metadata"] for c in chunks],
        }
```

---

## Retrieval Evaluation (NDCG, MRR, Recall@k)

Always maintain a labeled eval set and run metrics before and after any pipeline change.

```python
# src/search/eval.py
import numpy as np
from dataclasses import dataclass

@dataclass
class RetrievalMetrics:
    recall_at_k: float
    mrr: float
    ndcg_at_k: float

def mean_reciprocal_rank(relevant_ids: set[str], ranked_ids: list[str]) -> float:
    for rank, doc_id in enumerate(ranked_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0

def recall_at_k(relevant_ids: set[str], ranked_ids: list[str], k: int) -> float:
    hits = sum(1 for doc_id in ranked_ids[:k] if doc_id in relevant_ids)
    return hits / len(relevant_ids) if relevant_ids else 0.0

def ndcg_at_k(relevant_ids: set[str], ranked_ids: list[str], k: int) -> float:
    gains = [1.0 if ranked_ids[i] in relevant_ids else 0.0 for i in range(min(k, len(ranked_ids)))]
    dcg = sum(g / np.log2(i + 2) for i, g in enumerate(gains))
    ideal_gains = sorted(gains, reverse=True)
    idcg = sum(g / np.log2(i + 2) for i, g in enumerate(ideal_gains))
    return dcg / idcg if idcg > 0 else 0.0

def evaluate_retrieval(eval_set: list[dict], retrieve_fn, k: int = 5) -> RetrievalMetrics:
    """
    eval_set: [{"query": str, "relevant_doc_ids": list[str]}]
    retrieve_fn: query -> list of doc IDs in ranked order
    """
    recalls, mrrs, ndcgs = [], [], []
    for item in eval_set:
        relevant = set(item["relevant_doc_ids"])
        ranked = retrieve_fn(item["query"])
        recalls.append(recall_at_k(relevant, ranked, k))
        mrrs.append(mean_reciprocal_rank(relevant, ranked))
        ndcgs.append(ndcg_at_k(relevant, ranked, k))

    return RetrievalMetrics(
        recall_at_k=np.mean(recalls),
        mrr=np.mean(mrrs),
        ndcg_at_k=np.mean(ndcgs),
    )
```

---

## Production Concerns

### Latency Budget Allocation (example for 200ms SLA)

| Stage | Budget |
|---|---|
| Query embedding | 20ms |
| ANN vector search | 30ms |
| BM25 keyword search | 20ms |
| RRF merge | 2ms |
| Cross-encoder reranking (top-50) | 60ms |
| LLM generation | 1000ms (separate SLA) |
| Total retrieval | ~130ms |

### Index Size vs. Accuracy Trade-offs

| Configuration | Index Size | Recall@10 | Notes |
|---|---|---|---|
| Full HNSW (ef=200) | Large | ~95% | Best accuracy, most memory |
| HNSW (ef=100) | Medium | ~90% | Good balance |
| IVF flat (nlist=100) | Small | ~85% | CPU-friendly, lower recall |
| Binary quantization | Tiny | ~75% | Only for scale-out scenarios |

---

## Self-Verification Checklist

Before declaring the retrieval system ready for integration:

- [ ] Retrieval eval set exists with >= 50 labeled query-document pairs: `wc -l eval/labeled_queries.jsonl` returns >= 50
- [ ] Recall@5 measured and meets threshold: `grep -c "recall_at_5\|Recall@5" eval/results.json` returns > 0 and value >= 0.80
- [ ] NDCG@5 and MRR logged for every pipeline change: `grep -c "ndcg\|mrr" eval/results.json` returns > 0
- [ ] Chunking strategy documented: `grep -c "chunk_size\|overlap\|chunking" docs/retrieval_design.md` returns > 0
- [ ] Embedding model benchmarked against domain-specific test set: `grep -c "benchmark\|domain" eval/embedding_eval.md` returns > 0
- [ ] Reranker enabled and within P95 SLA: reranker latency p95 <= defined SLA threshold
- [ ] All chunks carry source metadata: `grep -c "doc_id\|source_title\|section" src/chunker.*` returns > 0
- [ ] LLM prompt instructs citation: `grep -c "cite\|source\|refuse" src/prompts/rag_prompt.*` returns > 0

## Success Criteria

A retrieval system is production-ready when:

1. Recall@5 >= 0.80 on the labeled eval set (no more than 20% of correct answers are missed in top-5 retrieval).
2. P95 retrieval latency (embedding + search + rerank) is within the agreed SLA.
3. The LLM grounding prompt includes source citations and produces measurably fewer hallucinations than zero-shot on an adversarial test set.
4. The eval harness runs in CI and blocks deployment if recall drops more than 5% from baseline.
5. Index and embedding pipeline are versioned; rollback to a previous index state is documented.

---

## Anti-Patterns

- Never embed documents at query time using a different model than the one used at index time because the embedding spaces are incompatible — dot products between vectors from different models are meaningless, causing the nearest-neighbour search to return random results.
- Never skip chunking strategy evaluation for long documents because naive fixed-size chunking can split a sentence mid-thought, losing the semantic unit needed for accurate retrieval and degrading recall on queries that span the split boundary.
- Never omit a recall@K evaluation before deploying a vector index to production because retrieval quality is not visible from index construction logs; a misconfigured HNSW `ef_construction` or `m` parameter can produce an index that is fast but retrieves the wrong documents.
- Never delete-and-reindex a production vector store for schema changes without maintaining the old index in parallel because a reindex of millions of vectors takes minutes to hours; deleting first creates a retrieval gap where all queries return empty results.
- Never store full document content inside the vector payload without size limits because large payloads inflate memory usage on the vector DB node; at scale the memory overhead of payload storage can exceed the memory required for the vectors themselves.
- Never use cosine similarity as the distance metric without normalising embeddings first because unnormalised cosine similarity gives undue weight to high-magnitude vectors, skewing nearest-neighbour rankings toward longer or more repetitive documents.
- Never deploy without an eval set because shipping a RAG system without measurable retrieval quality means you cannot reason about, debug, or improve the system when it returns wrong results in production.

---

## Failure Modes

| Situation | Response |
|---|---|
| LLM hallucinating answers not in the corpus | This is a retrieval miss. Check recall@k. Increase top_k, add reranker, or refine chunking. Add grounding instruction to prompt. |
| Retrieval returns irrelevant chunks for specific queries | Check if query uses terminology not in the corpus. Add query expansion or synonym mapping. Consider BM25 hybrid for exact-match terms. |
| Embedding model produces poor similarity for domain terms | Fine-tune on domain data or switch to a domain-specific model. Run MTEB-style eval on your corpus first. |
| Index latency exceeds SLA under load | Profile: embedding latency vs. ANN search latency separately. Consider approximate quantization or pre-computing query embeddings for known query patterns. |
| Reranker is too slow for the latency budget | Reduce candidate pool (top-20 instead of top-50). Use a smaller cross-encoder. Move reranker to async pre-fetch if the UI allows. |
| RAG answers are coherent but cite wrong sources | The LLM is hallucinating citations. Add structured citation format requirement and validate cited IDs against retrieved chunk IDs in post-processing. |
| Pinecone / vector DB costs growing unexpectedly | Audit index size. Implement TTL-based expiry for time-sensitive documents. Consider pgvector (self-hosted) for cost-stable workloads. |

---

## Integration with Mega-Mind

`search-vector-architect` is invoked for all search, RAG, and semantic retrieval work. It is closely related to `ml-engineer` (for embedding model fine-tuning and evaluation) and `data-engineer` (for document ingestion pipelines). For multi-step context refinement during agent orchestration, pair with `iterative-retrieval`. For LLM cost control within RAG pipelines, use `cost-aware-llm-pipeline`.

**Chain:** `data-engineer` → `search-vector-architect` → `ml-engineer` (eval) → `backend-architect` (serving) → `observability-specialist` (monitoring)
