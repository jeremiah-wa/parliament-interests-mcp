"""Tests for the MCP server tools."""

import pytest
from typing import Sequence
from mcp.types import TextContent, Tool
from mcp.server.fastmcp.exceptions import ToolError

from src.server import mcp
from src.api.models.base import BaseAPIModel
from src.api.models import (
    InterestsParams,
    PublishedInterestApiLinkedSearchResult,
    MemberSearchParams,
    MemberMembersServiceSearchResult,
)


class TestMCPServer:
    """Test MCP server tool definitions and functionality."""

    def test_server_initialization(self):
        """Test that MCP server is properly initialized."""
        assert mcp.name == "parliament-interests"

    @classmethod
    def get_result(cls, model: BaseAPIModel, result) -> BaseAPIModel | None:
        if isinstance(result, Sequence):
            for item in result:
                if isinstance(item, TextContent):
                    resultant_model = model.model_validate_json(item.text)
                    assert resultant_model
                    return resultant_model
                elif isinstance(item, Sequence):
                    return cls.get_result(model, item)
                else:
                    return None
        else:
            assert isinstance(result, TextContent)
            resultant_model = model.model_validate_json(result.text)
            assert resultant_model
            return resultant_model
        return None

    @pytest.mark.asyncio
    async def test_tools_registered(self):
        """Test that tools are properly registered."""
        tools = await mcp.list_tools()
        tool_names = [tool.name for tool in tools]

        assert "get_interests" in tool_names
        assert "get_members" in tool_names

    @pytest.mark.asyncio
    async def test_get_interests_tool_definition(self):
        """Test get_interests tool definition."""
        tools = await mcp.list_tools()
        get_interests_tool = next((t for t in tools if t.name == "get_interests"), None)

        assert get_interests_tool is not None
        assert isinstance(get_interests_tool, Tool)
        assert get_interests_tool.description is not None

    @pytest.mark.asyncio
    async def test_get_members_tool_definition(self):
        """Test get_members tool definition."""
        tools = await mcp.list_tools()
        get_members_tool = next((t for t in tools if t.name == "get_members"), None)

        assert get_members_tool is not None
        assert isinstance(get_members_tool, Tool)
        assert get_members_tool.description is not None

    @pytest.mark.asyncio
    async def test_get_interests_tool_execution_no_params(self):
        """Test executing get_interests tool without parameters."""
        result = await mcp.call_tool("get_interests", {})

        assert self.get_result(PublishedInterestApiLinkedSearchResult, result)

    @pytest.mark.asyncio
    async def test_get_interests_tool_execution_with_params(self):
        """Test executing get_interests tool with parameters."""
        params = dict(params=InterestsParams(skip=0, take=5))
        result = await mcp.call_tool("get_interests", params)

        # Should return a valid result
        resultant_model = self.get_result(
            PublishedInterestApiLinkedSearchResult, result
        )
        assert isinstance(resultant_model, PublishedInterestApiLinkedSearchResult)
        assert resultant_model.skip == 0
        assert resultant_model.take == 5

    @pytest.mark.asyncio
    async def test_get_members_tool_execution_no_params(self):
        """Test executing get_members tool without parameters."""
        result = await mcp.call_tool("get_members", {})
        assert self.get_result(MemberMembersServiceSearchResult, result)

    @pytest.mark.asyncio
    async def test_get_members_tool_execution_with_params(self):
        """Test executing get_members tool with parameters."""
        params = dict(params=MemberSearchParams(skip=0, take=5))
        result = await mcp.call_tool("get_members", params)

        resultant_model = self.get_result(MemberMembersServiceSearchResult, result)
        assert isinstance(resultant_model, MemberMembersServiceSearchResult)
        assert resultant_model.skip == 0
        assert resultant_model.take == 5

    @pytest.mark.asyncio
    async def test_invalid_tool_name(self):
        """Test calling non-existent tool."""
        with pytest.raises(ToolError):
            await mcp.call_tool("non_existent_tool", {})
