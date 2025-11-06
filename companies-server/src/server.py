import logging
import sys
from mcp.server.fastmcp import FastMCP
from src.api.client import CompanyApiClient
from src.api.models.search import (
    CompanySearchParams,
    CompanySearchResponse,
    AdvancedSearchParams,
    AdvancedSearchResponse,
    OfficerSearchParams,
    OfficerSearchResponse,
)

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

mcp = FastMCP(name="companies-house")

client = CompanyApiClient()


@mcp.tool()
async def search_companies(
    params: CompanySearchParams
) -> CompanySearchResponse:
    """Search for companies by name or number.
    
    This is the primary search tool for finding companies. It provides fuzzy matching,
    relevance ranking, and highlighted snippets showing why results matched.
    
    Args:
        params: Search parameters including:
            - q: The search term (company name or number)
            - items_per_page: Number of results to return (1-100, default 20)
            - start_index: Starting index for pagination (default 0)
            - restrictions: Optional filters like 'active-companies' or 'legally-equivalent-company-name'
    
    Returns:
        Search results with company details, addresses, and match highlights
    
    Example:
        Search for active companies: search_companies(q="Tesla", restrictions="active-companies")
        Search by number: search_companies(q="00000006")
    """
    result = await client.search_companies(params)
    return result


@mcp.tool()
async def advanced_search_companies(
    params: AdvancedSearchParams | None = None
) -> AdvancedSearchResponse:
    """Advanced search for companies with detailed filters.
    
    Use this for complex queries requiring precise filtering by status, type,
    date ranges, location, or SIC codes. For simple name searches, use search_companies instead.
    
    Args:
        params: Advanced search parameters including:
            - company_name_includes/excludes: Filter by name
            - company_status: Filter by status (active, dissolved, etc.)
            - company_type: Filter by type (ltd, plc, llp, etc.)
            - dissolved_from/to: Date range for dissolution
            - incorporated_from/to: Date range for incorporation
            - location: Filter by location
            - sic_codes: Filter by industry codes
            - size: Results per page (1-5000)
            - start_index: Pagination offset
    
    Returns:
        Search results with company details and registered office addresses
    
    Example:
        Find dissolved companies: advanced_search_companies(params={
            "company_status": ["dissolved"],
            "dissolved_from": "2020-01-01",
            "location": "Wales"
        })
    """
    result = await client.advanced_search_companies(params)
    return result


@mcp.tool()
async def search_officers(
    params: OfficerSearchParams
) -> OfficerSearchResponse:
    """Search for company officers by name.
    
    Find directors, secretaries, and other company officers. Results include
    appointment counts, partial date of birth, and address information.
    
    Args:
        params: Search parameters including:
            - q: The search term (officer name)
            - items_per_page: Number of results to return (1-100, default 20)
            - start_index: Starting index for pagination (default 0)
    
    Returns:
        Search results with officer details, appointment counts, and addresses
    
    Example:
        Search for officers: search_officers(q="John Smith")
        Paginate results: search_officers(q="Smith", items_per_page=50, start_index=50)
    """
    result = await client.search_officers(params)
    return result


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
