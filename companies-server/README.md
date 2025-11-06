# Companies House MCP Server

MCP server for searching UK Companies House data.

## Features

- **Simple Company Search** - Search by name or number with fuzzy matching
- **Advanced Company Search** - Filter by status, type, dates, location, SIC codes

## Installation

```bash
# From the monorepo root
cd companies-server
uv sync
```

## Configuration

Set your Companies House API key in `.env`:

```bash
COMPANY_API_KEY=your_api_key_here
```

Get your API key from: https://developer.company-information.service.gov.uk/

## Usage

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "companies-house": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/parliament-interests-mcp/companies-server",
        "mcp",
        "run",
        "src/server.py"
      ],
      "env": {
        "COMPANY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Development

```bash
# Run the server
uv run mcp dev src/server.py

# Run tests
uv run pytest
```

## Available Tools

### `search_companies`
Search for companies by name or number.

**Parameters:**
- `q` (required) - Search term
- `items_per_page` - Results per page (1-100, default 20)
- `start_index` - Pagination offset (default 0)
- `restrictions` - Filters like "active-companies"

**Example:**
```python
search_companies(q="Tesla", restrictions="active-companies")
```

### `advanced_search_companies`
Advanced search with detailed filters.

**Parameters:**
- `company_name_includes/excludes` - Name filters
- `company_status` - Status filter (active, dissolved, etc.)
- `company_type` - Type filter (ltd, plc, llp, etc.)
- `dissolved_from/to` - Dissolution date range
- `incorporated_from/to` - Incorporation date range
- `location` - Location filter
- `sic_codes` - Industry code filters
- `size` - Results per page (1-5000)
- `start_index` - Pagination offset

**Example:**
```python
advanced_search_companies(params={
    "company_status": ["dissolved"],
    "dissolved_from": "2020-01-01",
    "location": "Wales"
})
```

### `search_officers`
Search for company officers (directors, secretaries) by name.

**Parameters:**
- `q` (required) - Search term (officer name)
- `items_per_page` - Results per page (1-100, default 20)
- `start_index` - Pagination offset (default 0)

**Returns:**
- Officer name and address
- Appointment count (total companies)
- Partial date of birth (month/year)
- Match highlighting

**Example:**
```python
search_officers(q="John Smith")
```

## API Documentation

- [Companies House API Docs](https://developer-specs.company-information.service.gov.uk/)
- [Search API Reference](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search)

## License

MIT
