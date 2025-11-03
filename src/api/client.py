"""HTTP client for Parliament Interests API."""

import httpx
import logging
from typing import Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
from src.api.models.base import BaseParams
from src.api.models.interests import (
    InterestsParams,
    PublishedInterestApiLinkedSearchResult,
    PublishedCategoryApiLinkedSearchResult,
)
from src.api.models.members import (
    MemberMembersServiceSearchResult,
    MemberSearchParams,
    DebateContributionMembersServiceSearchResult,
    MembersInterestsMembersServiceSearchResult,
    LordsInterestsRegisterParams,
)
from src.api.models.debates import Debate

# Note: Logging configuration is handled in server.py to avoid conflicts
logger = logging.getLogger(__name__)


class ParliamentAPIClient:
    """Client for the UK Parliament Register of Interests API."""

    def __init__(self):
        self.interests_url = "https://interests-api.parliament.uk/api/v1"
        self.members_url = "https://members-api.parliament.uk/api"
        self.hansard_url = "https://hansard-api.parliament.uk"
        self.headers = {
            "User-Agent": "parliament-interests-mcp/0.1.0",
            "Accept": "application/json",
        }
        self.timeout = 30

    @retry(
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _make_request(
        self, url: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make HTTP request with retry logic."""
        logger.debug(f"Making request to {url} with params: {params}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=self.headers, params=params)
            try:
                response.raise_for_status()
                result = response.json()
                return result
            except httpx.HTTPStatusError as e:
                error_detail = "Unknown error"
                try:
                    error_detail = e.response.json()
                except Exception:
                    error_detail = e.response.text
                logger.error(
                    f"HTTP error {e.response.status_code} for {response.request.url}: {error_detail}"
                )
                raise

    async def get_interests(
        self, params: InterestsParams | None = None
    ) -> PublishedInterestApiLinkedSearchResult:
        response = await self._make_request(
            f"{self.interests_url}/Interests",
            params=(
                params.model_dump(by_alias=True, exclude_none=True) if params else None
            ),
        )
        return PublishedInterestApiLinkedSearchResult.model_validate(response)

    async def get_lords_interests(self, params: LordsInterestsRegisterParams | None = None):
        response = await self._make_request(
            f"{self.members_url}/LordsInterests/Register",
            params=params.model_dump(by_alias=True, exclude_none=True) if params else None
        )
        return MembersInterestsMembersServiceSearchResult.model_validate(response)

    async def get_categories(
        self, params: BaseParams | None = None
    ) -> PublishedCategoryApiLinkedSearchResult:
        response = await self._make_request(
            f"{self.interests_url}/Categories",
            params=(
                params.model_dump(by_alias=True, exclude_none=True) if params else None
            ),
        )
        return PublishedCategoryApiLinkedSearchResult.model_validate(response)

    async def get_members(
        self, params: MemberSearchParams | None = None
    ) -> MemberMembersServiceSearchResult:
        response = await self._make_request(
            f"{self.members_url}/Members/Search",
            params=(
                params.model_dump(by_alias=True, exclude_none=True) if params else None
            ),
        )
        return MemberMembersServiceSearchResult.model_validate(response)

    async def get_member_contribution_summary(
        self, member_id: int, page: int | None = None
    ) -> DebateContributionMembersServiceSearchResult:
        response = await self._make_request(
            f"{self.members_url}/Members/{member_id}/ContributionSummary",
            params=dict(page=page) if page else None,
        )
        return DebateContributionMembersServiceSearchResult.model_validate(response)
            
    async def get_debate(self, debate_section_ext_id: str) -> Debate:
        response = await self._make_request(f"{self.hansard_url}/Debates/Debate/{debate_section_ext_id}.json")
        return Debate.model_validate(response)


async def main():
    # from src.api.rag import loader, vectorstore
    # from langchain_community.vectorstores.utils import filter_complex_metadata
    client = ParliamentAPIClient()
    params = LordsInterestsRegisterParams(searchTerm="May")
    result = await client.get_lords_interests(params)
    # result = await client.get_debate("F2CE6BA1-3CA1-4032-9398-E07D35A35F95")
    # documents = loader.debate_to_documents(result)
    # filtered_documents = filter_complex_metadata(documents)
    # vectorstore.add_documents(filtered_documents)
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())