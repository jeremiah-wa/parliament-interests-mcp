import logging
from typing import TypeVar
from pydantic import ConfigDict, Field, model_validator, create_model
# from langchain_huggingface  import HuggingFaceEmbeddings
# from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma
from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_community.vectorstores.utils import filter_complex_metadata

from src.parliament.api.client import ParliamentAPIClient
from src.parliament.api.models.debates import Debate, DebateOverview, DebateItem
from src.parliament.api.models.base import BaseAPIModel

logger = logging.getLogger(__name__)




class DebateDocumentMetadata(DebateOverview, DebateItem):
    """Metadata for debate document in vector store.
    
    Combines DebateOverview and DebateItem fields.
    """
    
    # Exclude items and child_debates from DebateOverview
    items: None = Field(default=None, exclude=True, description="Ignore this attribute")
    child_debates: None = Field(default=None, exclude=True, description="Ignore this attribute")
    value: None = Field(default=None, exclude=True, description="Ignore this attribute")
    
    @classmethod
    def from_overview_and_item(cls, overview: DebateOverview, item: DebateItem) -> "DebateDocumentMetadata":
        """Create metadata from debate overview and item dictionaries."""
        return cls(**{**overview.model_dump(exclude={"items", "child_debates"}, by_alias=True), **item.model_dump(exclude={"value"}, by_alias=True)})

    def to_dict(self):
        return self.model_dump(mode='json', by_alias=True, exclude_none=True)


class DebateLoader(BaseLoader):

    def __init__(self):
        self.client = ParliamentAPIClient()


    def debate_to_documents(self, debate: Debate) -> list[Document]:
        debate_items = []
        for item in debate.items:
            if item.value and item.member_id:
                metadata = DebateDocumentMetadata.from_overview_and_item(debate.overview, item)
                debate_items.append(Document(
                    id=f"{debate.overview.id}-{item.item_id}",
                    page_content=item.value,
                    metadata=metadata.to_dict()
                ))
        for child_debate in debate.child_debates:
            debate_items.extend(self.debate_to_documents(child_debate))
        filtered_documents = filter_complex_metadata(debate_items)
        return filtered_documents

    async def aload(self, debate_section_ext_id) -> list[Document]:
        """Asynchronous load."""

        debate = await self.client.get_debate(debate_section_ext_id)
        debate_items = self.debate_to_documents(debate)
        return debate_items


vectorstore = Chroma(
    collection_name="debates",
    persist_directory="./chromadb"
)

loader = DebateLoader()


# Request models

class WhereDocument(BaseAPIModel):
    """Pydantic model for where_document filter.
    
    Supports text search operators on document content.
    
    Constraints:
        - Only ONE operator can be used per WhereDocument instance
        - At least one operator must be specified
        - For multiple conditions, use $and or $or with nested WhereDocument instances
    
    Available Operators:
        - $contains: Text must contain the specified substring (case-insensitive)
        - $not_contains: Text must NOT contain the specified substring (case-insensitive)
        - $and: All nested conditions must match (logical AND)
        - $or: At least one nested condition must match (logical OR)
    
    Examples:
        # Contains
        where = WhereDocument(contains="immigration")
        
        # Not contains
        where = WhereDocument(not_contains="question")
        
        # AND condition
        where = WhereDocument(and_=[
            WhereDocument(contains="immigration"),
            WhereDocument(contains="policy")
        ])
        
        # OR condition
        where = WhereDocument(or_=[
            WhereDocument(contains="immigration"),
            WhereDocument(contains="asylum")
        ])
        
        # Complex nested
        where = WhereDocument(and_=[
            WhereDocument(contains="immigration"),
            WhereDocument(or_=[
                WhereDocument(contains="Lords"),
                WhereDocument(contains="Commons")
            ])
        ])
    """
    contains: str | None = Field(
        default=None,
        alias="$contains",
        description="Text must contain this substring (case-insensitive)"
    )
    not_contains: str | None = Field(
        default=None,
        alias="$not_contains",
        description="Text must not contain this substring (case-insensitive)"
    )
    and_: list["WhereDocument"] | None = Field(
        default=None,
        alias="$and",
        description="All conditions must match"
    )
    or_: list["WhereDocument"] | None = Field(
        default=None,
        alias="$or",
        description="At least one condition must match"
    )

    @model_validator(mode="after")
    def validate_single_operator(self):
        """Ensure only one operator is used at a time."""
        operators = [
            self.contains,
            self.not_contains,
            self.and_,
            self.or_
        ]
        non_none = [op for op in operators if op is not None]
        
        if len(non_none) == 0:
            raise ValueError("At least one operator must be specified")
        if len(non_none) > 1:
            raise ValueError("Only one operator can be used per WhereDocument")
        
        return self

    def to_dict(self):
        return self.model_dump(mode='json', by_alias=True, exclude_none=True)


DebateSearchParams = create_model(
    'DebateSearchParams',
    __base__=DebateDocumentMetadata,
    **{
        field: (info.annotation | None, Field(default=None, alias=info.alias, description=info.description)) 
        for field, info in DebateDocumentMetadata.model_fields.items()
    },
)


class DocumentAPIModel(BaseAPIModel):
    """Pydantic model for debate document in search results."""
    id: str | None = Field(default=None, description="Document ID")
    page_content: str = Field(description="The text content of the document")
    metadata: dict = Field(default_factory=dict, description="Document metadata")

    @classmethod
    def from_document(cls, document: Document) -> "DocumentAPIModel":
        """Create model from LangChain Document."""
        return cls(
            id=document.id,
            page_content=document.page_content,
            metadata=document.metadata
        )

class SearchDebatesResponse(BaseAPIModel):
    """Response model for debate search results."""
    results: list[DocumentAPIModel] = Field(description="List of matching debate documents")
    query: str = Field(description="The search query used")
    count: int = Field(description="Number of results returned")