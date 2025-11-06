# UK Parliament & Companies House MCP Servers

Monorepo containing two Model Context Protocol (MCP) servers for UK government data:

## Servers

### 🏛️ [Parliament Server](./parliament-server/)
Access UK Parliament data including:
- MP and Lords interests
- Member profiles and staff
- Parliamentary debates with semantic search (RAG)

**No API key required**

### 🏢 [Companies House Server](./companies-server/)
Search UK company data:
- Simple company search by name/number
- Advanced search with filters
- Company profiles and registered addresses

**Requires Companies House API key**

## Quick Start

### Installation

```bash
# Install both servers
cd parliament-server && uv sync && cd ..
cd companies-server && uv sync && cd ..
```

### Configuration

#### Parliament Server
No configuration needed - APIs are public.

#### Companies House Server
Create `companies-server/src/.env`:
```bash
COMPANY_API_KEY=your_api_key_here
```

Get your key from: https://developer.company-information.service.gov.uk/

### Claude Desktop Setup

Add both servers to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "parliament": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/parliament-interests-mcp/parliament-server",
        "mcp",
        "run",
        "src/server.py"
      ]
    },
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

## Development

### Running Servers

```bash
# Parliament server
cd parliament-server
uv run mcp dev src/server.py

# Companies House server
cd companies-server
uv run mcp dev src/server.py
```

### Testing

```bash
# Parliament server
cd parliament-server
uv run pytest

# Companies House server
cd companies-server
uv run pytest
```

## Project Structure

```
parliament-interests-mcp/
├── parliament-server/          # Parliament MCP server
│   ├── src/
│   │   ├── api/               # Parliament API client & models
│   │   ├── rag.py             # Vector store for debate search
│   │   └── server.py          # MCP server
│   ├── tests/
│   └── README.md
├── companies-server/           # Companies House MCP server
│   ├── src/
│   │   ├── api/               # Companies House API client & models
│   │   └── server.py          # MCP server
│   └── README.md
├── pyproject.toml             # Shared dependencies
└── README.md                  # This file
```

## Features

### Parliament Server
- ✅ Get MP/Lords interests and staff
- ✅ Search members by name
- ✅ Get debate contributions
- ✅ Semantic debate search with ChromaDB
- ✅ No authentication required

### Companies House Server
- ✅ Simple company search (fuzzy matching)
- ✅ Advanced search (13 filter options)
- ✅ Match highlighting
- ✅ Pagination support

## API Documentation

- [UK Parliament APIs](https://developer.parliament.uk/)
- [Companies House API](https://developer-specs.company-information.service.gov.uk/)
- [MCP Protocol](https://modelcontextprotocol.io/)

## License

MIT
