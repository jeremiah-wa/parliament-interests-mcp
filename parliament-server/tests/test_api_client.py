"""Simple tests for ParliamentAPIClient - just test basic functionality."""

import httpx
import pytest
from tenacity import RetryError
from src.api.models.interests import (
    InterestsParams,
    PublishedInterestApiLinkedSearchResult,
)
from src.api.models.members import MemberSearchParams, MemberMembersServiceSearchResult
from src.api.client import ParliamentAPIClient


class TestParliamentAPIClient:
    """Simple tests for API client functions."""

    @pytest.fixture
    def api_client(self):
        """Create a ParliamentAPIClient instance for testing."""
        return ParliamentAPIClient()

    def test_init(self, api_client: ParliamentAPIClient):
        """Test initialization of ParliamentAPIClient."""
        assert api_client.interests_url == "https://interests-api.parliament.uk/api/v1"
        assert api_client.members_url == "https://members-api.parliament.uk/api"
        assert api_client.headers == {
            "User-Agent": "parliament-interests-mcp/0.1.0",
            "Accept": "application/json",
        }
        assert api_client.timeout == 30

    @pytest.mark.asyncio
    async def test_make_request_retry_logging_with_timeout(
        self, caplog: pytest.LogCaptureFixture
    ):
        """Test retry logging with httpbin delay endpoint that might timeout."""
        # Use a very short timeout to force timeout on httpbin's delay endpoint
        api_client = ParliamentAPIClient()
        api_client.timeout = 1
        caplog.clear()

        with pytest.raises(RetryError):
            await api_client._make_request("https://httpbin.org/delay/3")

        # Verify retry logging occurred
        retry_warnings = [
            record
            for record in caplog.records
            if "Retrying" in record.message and "Timeout" in record.message
        ]
        assert len(retry_warnings) >= 2  # At least 2 retry attempts

    @pytest.mark.asyncio
    async def test_make_request_http_error_logging(
        self, api_client: ParliamentAPIClient, caplog: pytest.LogCaptureFixture
    ):
        """Test HTTP error logging with invalid parameter."""
        caplog.clear()
        with pytest.raises(httpx.HTTPStatusError):
            await api_client._make_request(
                "https://interests-api.parliament.uk/api/v1/Interests?SortOrder=INVALID"
            )

        for caplog_record in caplog.records:
            if caplog_record.levelname == "ERROR":
                assert "400" in caplog_record.message
                assert "SortOrder" in caplog_record.message

    @pytest.mark.asyncio
    async def test_get_interests_no_params(self, api_client: ParliamentAPIClient):
        """Test get_interests with no parameters."""
        result = await api_client.get_interests(None)

        assert isinstance(result, PublishedInterestApiLinkedSearchResult)

    @pytest.mark.asyncio
    async def test_get_interests_with_params(self, api_client: ParliamentAPIClient):
        """Test get_interests with parameters."""
        params = InterestsParams(skip=0, take=5)
        print(f"Params in test: {params.model_dump(by_alias=True, exclude_none=True)}")
        result = await api_client.get_interests(params)

        assert isinstance(result, PublishedInterestApiLinkedSearchResult)
        assert result.take == 5

    @pytest.mark.asyncio
    async def test_get_members_no_params(self, api_client: ParliamentAPIClient):
        """Test get_members with no parameters."""
        result = await api_client.get_members(None)

        assert isinstance(result, MemberMembersServiceSearchResult)

    @pytest.mark.asyncio
    async def test_get_members_with_params(self, api_client: ParliamentAPIClient):
        """Test get_members with parameters."""
        params = MemberSearchParams(skip=0, take=5)
        result = await api_client.get_members(params)

        assert isinstance(result, MemberMembersServiceSearchResult)
        assert result.take == 5
