# Parliament Interests MCP Server

An MCP (Model Context Protocol) server that provides access to the UK Parliament Register of Interests API. This server allows Claude Desktop to query MP financial interests, donations, employment, and other registered interests.

## Features

- **Interest Categories**: Browse all types of interests (employment, donations, gifts, etc.)
- **Member Search**: Find MPs by name or browse all members
- **Interest Records**: Search interests by member, category, date range, or donor
- **Detailed Information**: Get comprehensive details about specific interests including donor information

## Installation

### Prerequisites
- Python 3.9+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Setup

1. Clone or download this repository
2. Install dependencies with uv:

```bash
cd parliament-interests-mcp
uv sync
```

This will create a virtual environment and install all dependencies automatically.

## Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "parliament-interests": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.server"],
      "cwd": "C:\\path\\to\\parliament-interests-mcp"
    }
  }
}
```

### macOS
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "parliament-interests": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.server"],
      "cwd": "/path/to/parliament-interests-mcp"
    }
  }
}
```

### Linux
Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "parliament-interests": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.server"],
      "cwd": "/path/to/parliament-interests-mcp"
    }
  }
}
```

## Available Tools

### `get_interest_categories`
Get all interest categories from the Parliament register.

**Parameters:**
- `skip` (optional): Number of records to skip for pagination
- `take` (optional): Number of records to return (max 100)

### `get_category_details`
Get detailed information about a specific interest category.

**Parameters:**
- `category_id` (required): The ID of the category to retrieve

### `search_members`
Search for MPs by name or get all members.

**Parameters:**
- `name` (optional): Name of the MP to search for
- `skip` (optional): Number of records to skip for pagination
- `take` (optional): Number of records to return (max 100)

### `get_member_details`
Get detailed information about a specific MP.

**Parameters:**
- `member_id` (required): The ID of the member to retrieve

### `search_interests`
Search for interest records with various filters.

**Parameters:**
- `member_id` (optional): Filter by specific MP ID
- `category_id` (optional): Filter by interest category ID
- `from_date` (optional): Filter interests from this date (YYYY-MM-DD format)
- `to_date` (optional): Filter interests to this date (YYYY-MM-DD format)
- `skip` (optional): Number of records to skip for pagination
- `take` (optional): Number of records to return (max 100)

### `get_interest_details`
Get detailed information about a specific interest record.

**Parameters:**
- `interest_id` (required): The ID of the interest record to retrieve

### `search_by_donor`
Search for interests by donor name or company.

**Parameters:**
- `donor_name` (required): Name of the donor to search for
- `skip` (optional): Number of records to skip for pagination
- `take` (optional): Number of records to return (max 100)

## Example Usage

Once configured in Claude Desktop, you can ask questions like:

- "What are the different types of interest categories in Parliament?"
- "Show me all interests registered by [MP Name]"
- "Find all donations from [Company Name]"
- "What employment interests has [MP Name] declared?"
- "Show me all interests in the 'Gifts and benefits' category from the last year"

## API Data

The server accesses the official UK Parliament Register of Interests API at `https://interests-api.parliament.uk/api/v1`. This includes:

- **Categories**: Employment, donations, gifts, visits, shareholdings, etc.
- **Members**: Current MPs with their details
- **Interests**: Detailed records including donor information, amounts, dates, and descriptions

## Development

The project uses `uv` for dependency management. Development dependencies are automatically installed with `uv sync`.

Run tests:
```bash
uv run pytest
```

Format code:
```bash
uv run black src/
uv run ruff check src/
```

Add new dependencies:
```bash
uv add <package-name>
uv add --dev <dev-package-name>  # for dev dependencies
```

## License

This project is open source. The Parliament data is available under the Open Parliament Licence.

## Support

For issues with this MCP server, please check the Parliament API documentation at https://interests-api.parliament.uk/index.html
