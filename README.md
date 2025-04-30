# Trello MCP Server

This is a Model Context Protocol (MCP) server for interacting with Trello API.

## Setup

1. Install dependencies using `uv`:
```bash
uv pip install -r uv.lock
```

2. Configure your environment variables:
Create a `.env` file with:
```
TRELLO_API_KEY=your_trello_api_key
TRELLO_API_TOKEN=your_trello_token
NOTION_API_KEY=your_notion_api_key  # Optional, only if using Notion integration
NOTION_PARENT_PAGE_ID=your_notion_page_id  # Optional, only if using Notion integration
```

3. Configure MCP JSON:
Create a `mcp.json` file with:
```json
{
  "mcpServers": {
    "trello": {
      "command": "{{PATH_TO_UV}}", 
      "args": [
        "--directory",
        "{{PATH_TO_SRC}}", 
        "run",
        "server.py"
      ],
      "env": {
        "TRELLO_API_KEY": "your_trello_api_key",
        "TRELLO_API_TOKEN": "your_trello_token",
        "NOTION_API_KEY": "your_notion_api_key",  // Optional
        "NOTION_PARENT_PAGE_ID": "your_notion_page_id"  // Optional
      }
    }
  }
}
```

Replace:
- `{{PATH_TO_UV}}` with the output of `which uv` (e.g., `/usr/local/bin/uv`)
- `{{PATH_TO_SRC}}` with the absolute path to this directory (use `pwd` command)
- Add your API keys and tokens

## Available Tools

The server provides the following tools for interacting with Trello:

- Get all boards
- Get board details
- Get lists in a board
- Get cards in a list
- Get card details
- Create new cards
- Update existing cards
- Move cards between lists
- Add comments to cards
- Get board members
- Publish to Notion (optional integration)

## Usage

Once configured, the MCP server can be started using the standard MCP client configuration. The server provides a natural language interface to interact with Trello through the available tools. 