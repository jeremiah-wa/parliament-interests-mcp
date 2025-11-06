# Parliament Interests MCP Server

An MCP (Model Context Protocol) server that provides access to the UK Parliament Register of Interests API. This server allows Claude Desktop to query MP financial interests, donations, employment, and other registered interests.

## Features

- **Interest Categories**: Browse all types of interests (employment, donations, gifts, etc.)
- **Member Search**: Find MPs by name or browse all members
- **Interest Records**: Search interests by member, category, date range, or donor
- **Detailed Information**: Get comprehensive details about specific interests including donor information

## Installation

### Prerequisites
- Python 3.11+
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

### `get_interests`
Search and retrieve interest records from the Parliament Register of Interests with comprehensive filtering options.

**Parameters (all optional):**
- `member_id` (int): Filter by specific MP ID
- `category_id` (int): Filter by interest category ID  
- `published_from` (date): Filter interests published from this date (YYYY-MM-DD format)
- `published_to` (date): Filter interests published to this date (YYYY-MM-DD format)
- `sort_order` (string): Sort order - "PublishingDateDescending" or "CategoryAscending"
- `expand_child_interests` (bool): Whether to expand child interests (default: true)
- `skip` (int): Number of records to skip for pagination (default: 0)
- `take` (int): Number of records to return (default: 20, max: 100)

**Returns:** Complete interest records including member details, categories, registration dates, field values, and donor information.

### `get_members`
Search and retrieve MP information with extensive search and filtering capabilities.

**Parameters (all optional):**
- `name` (string): Search members by name (partial matches supported)
- `location` (string): Search by postcode, constituency, or geographical location
- `post_title` (string): Filter by government post or role held
- `party_id` (int): Filter by political party ID
- `house` (int): Filter by House (1=Commons, 2=Lords)
- `constituency_id` (int): Filter by constituency ID
- `name_starts_with` (string): Filter by surname starting with specified letters
- `gender` (string): Filter by gender
- `membership_started_since` (datetime): Members who started on or after date
- `membership_ended_since` (datetime): Members who left on or after date
- `was_member_on_or_after` (datetime): Members active on or after date
- `was_member_on_or_before` (datetime): Members active on or before date
- `is_current_member` (bool): Filter for currently active members
- `is_eligible` (bool): Filter for members eligible to sit
- `policy_interest_id` (int): Filter by policy interest area
- `experience` (string): Filter by professional experience
- `skip` (int): Number of records to skip for pagination (default: 0)
- `take` (int): Number of records to return (default: 20, max: 100)

**Returns:** Complete member profiles including personal details, constituencies, party affiliations, and parliamentary roles.

## Example Usage

Once configured in Claude Desktop, you can ask questions like:

- "Show me all interests registered by [MP Name]"
- "Find all recent donations and gifts to MPs"
- "What employment interests have been declared in the last 6 months?"
- "Search for MPs from [Constituency/Location]"
- "Show me all interests in category [Category ID] published since [Date]"
- "Find MPs who have held the position of [Government Role]"
- "What are the most recent interest registrations?"
- "Search for interests related to [Company/Organization Name]"

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
