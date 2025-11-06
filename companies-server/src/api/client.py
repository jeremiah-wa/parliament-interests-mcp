import httpx
import logging
import os
from typing import Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
from src.api.models.search import (
    CompanySearchParams,
    CompanySearchResponse,
    AdvancedSearchParams,
    AdvancedSearchResponse,
    OfficerSearchParams,
    OfficerSearchResponse,
)

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

COMPANY_API_KEY = os.getenv("COMPANY_API_KEY")

class CompanyApiClient:
    def __init__(self):
        if not COMPANY_API_KEY:
            raise ValueError(
                "COMPANY_API_KEY environment variable is required. "
                "Get your API key from: https://developer.company-information.service.gov.uk/"
            )
        
        self.base_url = "https://api.company-information.service.gov.uk"
        self.auth = httpx.BasicAuth(username=COMPANY_API_KEY, password="")
        self.headers = {
            "User-Agent": "company-api-client/0.1.0",
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
            response = await client.get(url, headers=self.headers, params=params, auth=self.auth)
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

    async def search_companies(self, params: CompanySearchParams) -> CompanySearchResponse:
        """Search for companies by name or number (simple search)."""
        url = f"{self.base_url}/search/companies"
        response = await self._make_request(
            url, 
            params.model_dump(by_alias=True, exclude_none=True)
        )
        return CompanySearchResponse.model_validate(response)
    
    async def advanced_search_companies(self, params: AdvancedSearchParams | None = None) -> AdvancedSearchResponse:
        """Search for companies using advanced search with detailed filters."""
        url = f"{self.base_url}/advanced-search/companies"
        response = await self._make_request(
            url, 
            params.model_dump(by_alias=True, exclude_none=True) if params else None
        )
        return AdvancedSearchResponse.model_validate(response)
    
    async def search_officers(self, params: OfficerSearchParams) -> OfficerSearchResponse:
        """Search for company officers by name."""
        url = f"{self.base_url}/search/officers"
        response = await self._make_request(
            url,
            params.model_dump(by_alias=True, exclude_none=True)
        )
        return OfficerSearchResponse.model_validate(response)