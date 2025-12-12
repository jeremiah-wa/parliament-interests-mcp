# Vector Store Population Strategies

This document outlines approaches for populating the ChromaDB vector store used by the `search_debates` MCP tool.

## Current Behavior

The vector store starts empty and is populated on-demand when:
- `get_member_contribution_summary()` is called → triggers background indexing via `asyncio.create_task()`
- `get_debate()` is called → synchronously adds documents

The `search_debates()` tool requires the vector store to be populated first.

---

## Option 1: FastMCP Lifespan (Startup Initialization)

Use the official `lifespan` parameter to initialize the vector store at server startup.

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from mcp.server.fastmcp import Context, FastMCP

@dataclass
class AppContext:
    """Application context with pre-loaded data."""
    vectorstore_initialized: bool = False

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Pre-populate vector store on startup."""
    logger.info("Initializing vector store...")
    # Optionally pre-load specific debates here
    # await _preload_debates(some_member_ids)
    
    try:
        yield AppContext(vectorstore_initialized=True)
    finally:
        logger.info("Shutting down...")

mcp = FastMCP(name="parliament", lifespan=app_lifespan)
```

**Pros:**
- Clean lifecycle management
- Proper startup/shutdown handling
- Type-safe context access in tools

**Cons:**
- Requires knowing which debates to pre-load
- Startup time increases with pre-loading

---

## Option 2: Lazy Initialization with Feedback

Check if the vector store is empty and provide a helpful message:

```python
@mcp.tool()
async def search_debates(
    query: str = Field(description="Search query"),
    k: int = Field(default=5),
    filter: DebateSearchParams | None = None,
    where_document: WhereDocument | None = None,
) -> SearchDebatesResponse:
    # Check if vector store has documents
    collection = vectorstore._collection
    if collection.count() == 0:
        return SearchDebatesResponse(
            results=[],
            query=query,
            count=0,
            message="Vector store is empty. Call get_member_contribution_summary() or get_debate() first."
        )
    # ... rest of search logic
```

**Pros:**
- Simple implementation
- Clear feedback to LLM

**Cons:**
- Requires extra call before searching

---

## Option 3: HTTP Mode with Background Task Wrapper

For HTTP deployments with uvicorn, wrap the lifespan to run continuous background indexing:

```python
from contextlib import asynccontextmanager
import asyncio

async def background_indexer():
    """Continuously index new debates."""
    while True:
        # Poll for new debates or process a queue
        await asyncio.sleep(300)  # Every 5 minutes

def wrap_lifespan_with_background_task(original_lifespan):
    @asynccontextmanager
    async def combined_lifespan(app):
        async with original_lifespan(app):
            app.state.indexer_task = asyncio.create_task(background_indexer())
            logger.info("Background indexer started")
            yield
            app.state.indexer_task.cancel()
            try:
                await asyncio.wait_for(app.state.indexer_task, timeout=5.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
            logger.info("Background indexer stopped")
    return combined_lifespan

def main():
    app = mcp.http_app(path="/mcp")
    original_lifespan = app.router.lifespan_context
    if original_lifespan:
        app.router.lifespan_context = wrap_lifespan_with_background_task(original_lifespan)
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Pros:**
- Continuous background indexing
- Works with existing FastMCP lifespan

**Cons:**
- Only works in HTTP mode
- More complex setup

---

## Option 4: Explicit `populate_debates` Tool

Add a dedicated tool that LLMs can call to explicitly populate the store:

```python
@mcp.tool()
async def populate_debates(
    member_ids: list[int] = Field(description="Member IDs to index debates for")
) -> dict:
    """Explicitly populate vector store with debates for specified members.
    
    Call this before using search_debates() to ensure the vector store
    has relevant debate content indexed.
    
    Args:
        member_ids: List of member IDs to index debates for
    
    Returns:
        Summary of indexed debates
    """
    total_docs = 0
    for member_id in member_ids:
        result = await client.get_member_contribution_summary(member_id)
        debate_ids = [item.value.debate_website_id for item in result.items]
        await _update_vector_store(debate_ids)
        total_docs += len(debate_ids)
    return {"indexed_debates": total_docs, "member_ids": member_ids}
```

**Pros:**
- Explicit control for LLMs
- Clear intent
- Can batch multiple members

**Cons:**
- Extra tool call required

---

## Recommendation

Combine multiple approaches for the best experience:

1. **Lifespan (Option 1)** - Handle startup initialization and load persistent ChromaDB
2. **Explicit tool (Option 4)** - Give LLMs explicit control to populate on-demand
3. **Keep existing `asyncio.create_task()`** - Opportunistic background indexing when fetching contributions

This provides:
- Proper lifecycle management
- Explicit LLM control
- Automatic opportunistic indexing
- Good developer experience

---

## References

- [FastMCP Lifespan Discussion](https://github.com/jlowin/fastmcp/discussions/1763)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
