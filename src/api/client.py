"""HTTP client for Parliament Interests API."""

import httpx
import logging
import sys
from typing import Any
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential, 
    retry_if_exception_type,
    before_sleep_log,
)
from .models.interests import (
    InterestsParams,
    PublishedInterestApiLinkedSearchResult,
)
from .models.members import (
    MemberMembersServiceSearchResult,
    MemberSearchParams,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger(__name__)

class ParliamentAPIClient:
    """Client for the UK Parliament Register of Interests API."""

    def __init__(self):
        self.interests_url = "https://interests-api.parliament.uk/api/v1"
        self.members_url = "https://members-api.parliament.uk/api"
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

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=self.headers, params=params)

            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                logger.error(e.response.json())
                raise
            return response.json()


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
