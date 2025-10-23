"""HTTP client for Parliament Interests API."""

import httpx
import logging
from typing import Any
from tenacity import retry, stop_after_attempt, wait_exponential
from .models import (
    InterestsParams,
    PublishedInterestApiLinkedSearchResult,
    MemberMembersServiceSearchResult,
    MemberSearchParams,
)


class ParliamentAPIClient:
    """Client for the UK Parliament Register of Interests API."""

    def __init__(self):
        self.interests_url = "https://interests-api.parliament.uk/api/v1"
        self.members_url = "https://members-api.parliament.uk/api"
        self.timeout = 30

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _make_request(
        self, url: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make HTTP request with retry logic."""
        try:
            logging.info(f"Making request to: {url}")
            logging.info(f"With parameters: {params}")
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                logging.info(f"Response status: {response.status_code}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            raise

    async def get_interests(
        self, params: InterestsParams | None = None
    ) -> PublishedInterestApiLinkedSearchResult:
        response = await self._make_request(
            f"{self.interests_url}/Interests",
            params=params.model_dump(by_alias=True) if params else None,
        )
        return PublishedInterestApiLinkedSearchResult(**response)

    async def get_members(
        self, params: MemberSearchParams | None = None
    ) -> MemberMembersServiceSearchResult:
        response = await self._make_request(
            f"{self.members_url}/Members/Search",
            params=params.model_dump(by_alias=True) if params else None,
        )
        return MemberMembersServiceSearchResult(**response)
