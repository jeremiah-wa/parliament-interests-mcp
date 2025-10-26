from mcp.server.fastmcp import FastMCP
from src.api.client import ParliamentAPIClient
from src.api.models import (
    InterestsParams,
    PublishedInterestApiLinkedSearchResult,
    MemberSearchParams,
    MemberMembersServiceSearchResult,
)

mcp = FastMCP(name="parliament-interests")

client = ParliamentAPIClient()


@mcp.tool()
async def get_interests(
    params: InterestsParams | None = None,
) -> PublishedInterestApiLinkedSearchResult:
    return await client.get_interests(params)


@mcp.tool()
async def get_members(
    params: MemberSearchParams | None = None,
) -> MemberMembersServiceSearchResult:
    return await client.get_members(params)


if __name__ == "__main__":
    mcp.run()
