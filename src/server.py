import logging
import sys
import asyncio
from pydantic import Field
from mcp.server.fastmcp import FastMCP


from src.parliament.api.client import ParliamentAPIClient
from src.parliament.api.models.interests import (
    InterestsParams,
    PublishedInterestApiLinkedSearchResult,
    PublishedCategoryApiLinkedSearchResult,
)
from src.parliament.api.models.members import (
    MemberSearchParams,
    MemberMembersServiceSearchResult,
    BaseParams,
    DebateContributionMembersServiceSearchResult,
    LordsInterestsRegisterParams,
    LordsInterestsStaffParams,
    MembersInterestsMembersServiceSearchResult,
    MembersStaffMembersServiceSearchResult
)
from src.parliament.api.models.debates import DebateResponse
from src.parliament.rag import (
    vectorstore, 
    loader,
    DebateSearchParams,
    WhereDocument,
    SearchDebatesResponse,
    DocumentAPIModel
)

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

mcp = FastMCP(name="parliament-interests")

client = ParliamentAPIClient()


async def _update_vector_store(debate_ids: list[str]):
    """Background task to update debates in vector store."""
    try:
        for debate_id in debate_ids:
            try:
                documents = await loader.aload(debate_id)
                vectorstore.add_documents(documents)
                logger.info(f"Updated vector store with {len(documents)} documents")
            except Exception as e:
                logger.error(f"Error updating debate {debate_id}: {e}")
    except Exception as e:
        logger.error(f"Error in background update task: {e}")


@mcp.tool()
async def get_interests(
    params: InterestsParams | None = None,
) -> PublishedInterestApiLinkedSearchResult:
    """Get parliamentary interests data from the UK Parliament Register of Interests.
    
    The Register of Interests contains declarations of financial interests, gifts,
    hospitality, and other relevant interests declared by Members of Parliament.
    
    Args:
        params: Optional search parameters (skip, take, filters)
    
    Returns:
        Paginated list of published interests with member details
    
    Example:
        Get first 20 interests: get_interests()
        Search specific interests: get_interests(params={"skip": 0, "take": 10})
    """
    result = await client.get_interests(params)
    return result

@mcp.tool()
async def get_lords_interests(
    params: LordsInterestsRegisterParams | None = None,
) -> MembersInterestsMembersServiceSearchResult:
    """Get parliamentary lords interests data from the UK Parliament Register of Lords Interests.
    
    The Register of Lords Interests contains declarations of financial interests, gifts,
    hospitality, and other relevant interests declared by Lords.
    
    Args:
        params: Optional search parameters
    
    Returns:
        Paginated list of published interests with member details
    
    Example:
        Search specific lords interests: get_lords_interests(params={"searchTerm": "Baroness May of Maidenhead"})
    """
    result = await client.get_lords_interests(params)
    return result

@mcp.tool()
async def get_lords_staff(
    params: LordsInterestsStaffParams | None = None,
) -> MembersStaffMembersServiceSearchResult:
    """Get staff information for members of the House of Lords.
    
    Retrieves details about staff members employed by Lords, including their names,
    titles, and employment details.
    
    Args:
        params: Optional search parameters:
            - search_term: Search for staff by name or details
            - page: Page number for pagination (20 results per page)
    
    Returns:
        Paginated list of Lords and their staff members
    
    Example:
        Search for specific staff: get_lords_staff(params={"searchTerm": "Smith"})
        Get all staff: get_lords_staff()
    """
    result = await client.get_lords_staff(params)
    return result

@mcp.tool()
async def get_members(
    params: MemberSearchParams | None = None,
) -> MemberMembersServiceSearchResult:
    """Get information about UK Parliament members (MPs and Lords).
    
    Search and retrieve member profiles including names, constituencies,
    party affiliations, and current status.
    
    Args:
        params: Optional search parameters:
            - skip: Number of records to skip (pagination)
            - take: Number of records to return (max 20)
            - name: Search by member name
    
    Returns:
        Paginated list of members with profile information
    
    Example:
        Search by name: get_members(params={"name": "May"})
        Get all members: get_members(params={"take": 20})
    """
    result = await client.get_members(params)
    return result

@mcp.tool()
async def get_categories(
    params: BaseParams | None = None
) -> PublishedCategoryApiLinkedSearchResult:
    """Get categories used in the UK Parliament Register of Interests.
    
    Categories classify different types of interests such as employment,
    donations, gifts, property, shareholdings, etc.
    
    Args:
        params: Optional pagination parameters (skip, take)
    
    Returns:
        List of interest categories with descriptions
    
    Example:
        Get all categories: get_categories()
    """
    result = await client.get_categories(params)
    return result

@mcp.tool()
async def get_member_contribution_summary(
    member_id: int = Field(description="Contribution summary of Member by ID specified"),
    page: int | None = Field(default=None, description="Page number")
) -> DebateContributionMembersServiceSearchResult:
    """Get a summary of a member's contributions to parliamentary debates.
    
    Returns a list of debates where the specified member has spoken or contributed.
    This tool automatically indexes the debates in the background for semantic search.
    
    IMPORTANT: This tool populates the vector store for search_debates()
    
    Args:
        member_id: The unique ID of the member (use get_members to find IDs)
        page: Optional page number for pagination
    
    Returns:
        Paginated list of debate contributions with titles, dates, and debate IDs
    
    Side Effects:
        Automatically indexes debates into the vector store in the background
        for semantic search via search_debates()
    
    Example:
        Get contributions for member ID 8: get_member_contribution_summary(member_id=8)
    """
    result = await client.get_member_contribution_summary(member_id, page)
    
    # Extract debate IDs and start background indexing
    debate_ids = [item.value.debate_website_id for item in result.items]
    asyncio.create_task(_update_vector_store(debate_ids))
    
    return result



@mcp.tool()
async def get_debate(
    debate_id: str = Field(description="Debate section external ID specified"),
) -> DebateResponse:
    """Get the full content and details of a specific parliamentary debate.
    
    Retrieves the complete debate record including all speeches, interventions,
    member attributions, timestamps, and navigation structure.
    
    Args:
        debate_id: The external ID of the debate section
            (debateWebsiteId from get_member_contribution_summary)
    
    Returns:
        Debate: Complete debate record with:
            - Overview (title, date, location, house)
            - Navigator (section tree structure)
            - Items (all speeches and contributions)
            - Child debates (nested debate sections)
    
    Example:
        Get specific debate: get_debate(debate_id="F2CE6BA1-3CA1-4032-9398-E07D35A35F95")
    """
    # Debate.model_rebuild()
    result = await client.get_debate(debate_id)
    documents = loader.debate_to_documents(result)
    vectorstore.add_documents(documents)
    return DebateResponse(
        debate=result
    )

@mcp.tool()
async def search_debates(
    query: str = Field(description="Search query"),
    k: int = Field(default=5, description="Number of results to return"),
    filter: DebateSearchParams | None = Field(default=None, description="Filter to apply to search results metadata"),
    where_document: WhereDocument | None = Field(default=None, description="Filter to apply to search results document content"),
) -> SearchDebatesResponse:
    """Search parliamentary debates using semantic similarity.
    
    IMPORTANT: Before searching, you must first call get_member_contribution_summary()
    or get_debate() to populate the vector store with debate documents. The vector store starts empty 
    and is populated on-demand when member contributions or debates are fetched.
    
    Workflow:
        1. Call get_member_contribution_summary(member_id) or get_debate(debate_website_id) to update vector store
        2. Wait a moment for background update to complete
        3. Call search_debates(query) to find relevant content
    
    Args:
        query: Natural language search query
        k: Number of results to return (default: 5)
        filter: Filter by metadata fields (member_id, house, date, etc.)
        where_document: Filter by document content ($contains, $not_contains, $and, $or)
    
    Returns:
        SearchDebatesResponse with matching documents, query, and count
    
    Example:
        search_debates(
            query="immigration policy",
            k=5,
            filter={"member_id": 8},
            where_document={"$contains": "immigration"}
        )
    """

    _documents = vectorstore.similarity_search(
        query, 
        k=k, 
        filter=filter.model_dump(mode='json', exclude_none=True) if filter else None,
        where_document=where_document.model_dump(exclude_none=True) if where_document else None
    )
    
    # Convert LangChain Documents to Pydantic DebateDocuments
    documents = [DocumentAPIModel.from_document(doc) for doc in _documents]
    
    return SearchDebatesResponse(
        results=documents,
        query=query,
        count=len(documents)
    )


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
