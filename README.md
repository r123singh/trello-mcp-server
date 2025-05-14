# Trello MCP Server

This is a Model Context Protocol (MCP) server for interacting with Trello API.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/r123singh/trello-mcp-server.git
```
2. cd trello-mcp-server
3. Create a virtual environment:  
```bash
python -m venv venv
```
4. Activate the virtual environment:
```bash
source venv/bin/activate
```
5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Configure your environment variables:
Create a `.env` file with:
```
TRELLO_API_KEY=your_trello_api_key
TRELLO_API_TOKEN=your_trello_token
```

7. Configure MCP JSON:
Create a `mcp.json` file with:
```json
{
  "mcpServers": {
    "trello": {
      "command": "{PATH_TO_DIRECTORY}\\trello-mcp-server\\venv\\Scripts\\python.exe", 
      "args": [
        "{PATH_TO_DIRECTORY}\\trello-mcp-server\\server.py"
      ],
      "env": {
        "TRELLO_API_KEY": "your_trello_api_key",
        "TRELLO_API_TOKEN": "your_trello_token"
      }
    }
  }
}
```

Replace:
- `{{PATH_TO_DIRECTORY}}` with the absolute path to this directory (use `pwd` command)
- Add your API keys and tokens

To get Trello credentials:
  - Go to https://trello.com/app-key
  - Copy the API Key
  - Generate a token by visiting: https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Server%20Token&key=YOUR_API_KEY
  - (replace YOUR_API_KEY with your actual API key)
  - Replace your_trello_api_key and your_trello_token in the config with these value

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

## Usage

Once configured, the MCP server can be started using the standard MCP client configuration. The server provides a natural language interface to interact with Trello through the available tools such as Cursor, Claude Desktop

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.



