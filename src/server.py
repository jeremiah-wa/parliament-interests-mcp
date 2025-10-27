import logging
import sys
from mcp.server.fastmcp import FastMCP
from src.api.client import ParliamentAPIClient
from src.api.models import (
    InterestsParams,
    PublishedInterestApiLinkedSearchResult,
    MemberSearchParams,
    MemberMembersServiceSearchResult,
)

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

mcp = FastMCP(name="parliament-interests")

client = ParliamentAPIClient()


@mcp.tool()
async def get_interests(
    params: InterestsParams | None = None,
) -> PublishedInterestApiLinkedSearchResult:
    """Get parliamentary interests data."""
    result = await client.get_interests(params)
    return result



@mcp.tool()
async def get_members(
    params: MemberSearchParams | None = None,
) -> MemberMembersServiceSearchResult:
    """Get parliamentary members data."""
    result = await client.get_members(params)
    return result


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
