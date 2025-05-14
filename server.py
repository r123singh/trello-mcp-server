import httpx
from mcp.server.fastmcp import FastMCP, Context
import os

# Create a Trello MCP server
mcp = FastMCP(
    "Trello API", 
    instructions="""
    # Trello API Server
    
    This server provides access to Trello boards, lists, and cards through various tools.
    
    ## Available Tools
    - `get_boards()` - Get all boards accessible to the user
    - `get_board_details(board_id)` - Get detailed information about a specific board
    - `get_lists(board_id)` - Get all lists in a board
    - `get_cards(list_id)` - Get all cards in a list
    - `get_card_details(card_id)` - Get detailed information about a specific card
    - `create_card(list_id, name, desc)` - Create a new card in a list
    - `update_card(card_id, name=None, desc=None, due=None, labels=None)` - Update an existing card
    - `move_card(card_id, list_id)` - Move a card to a different list
    - `add_comment(card_id, text)` - Add a comment to a card
    - `get_board_members(board_id)` - Get all members of a board
    
    ## When to use what
    - For viewing boards: Use `get_boards()` 
    - For board details: Use `get_board_details(board_id)`
    - For viewing lists: Use `get_lists(board_id)`
    - For viewing cards: Use `get_cards(list_id)`
    - For card details: Use `get_card_details(card_id)`
    - For creating new cards: Use `create_card(list_id, name, desc)`
    - For updating cards: Use `update_card(card_id, ...)`
    - For moving cards: Use `move_card(card_id, list_id)`
    - For adding comments: Use `add_comment(card_id, text)`
    - For viewing board members: Use `get_board_members(board_id)`
    
    ## Notes
    - Ensure you have valid Trello API credentials set in environment variables:
      - `TRELLO_API_KEY`
      - `TRELLO_API_TOKEN`
    - The API key and token can be obtained from Trello's developer portal
    - These credentials should be kept secret and not shared publicly
    """
)

# Constants
BASE_URL = "https://api.trello.com/1"
API_KEY = os.getenv("TRELLO_API_KEY")
API_TOKEN = os.getenv("TRELLO_API_TOKEN")

# Helper functions
async def fetch_from_api(path: str, params: dict = None) -> dict:
    """Helper function to fetch data from Trello API"""
    if params is None:
        params = {}
    params.update({"key": API_KEY, "token": API_TOKEN})
    
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}{path}"
        response = await client.get(url, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()

async def post_to_api(path: str, data: dict = None, params: dict = None) -> dict:
    """Helper function to post data to Trello API"""
    if params is None:
        params = {}
    if data is None:
        data = {}
    params.update({"key": API_KEY, "token": API_TOKEN})
    
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}{path}"
        response = await client.post(url, json=data, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()

async def put_to_api(path: str, data: dict = None, params: dict = None) -> dict:
    """Helper function to update data on Trello API"""
    if params is None:
        params = {}
    if data is None:
        data = {}
    params.update({"key": API_KEY, "token": API_TOKEN})
    
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}{path}"
        response = await client.put(url, json=data, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()

# Tools

@mcp.tool()
async def get_boards() -> str:
    """Get all boards accessible to the user"""
    boards = await fetch_from_api("/members/me/boards")
    return format_boards(boards)

@mcp.tool()
async def get_board_details(board_id: str) -> str:
    """Get detailed information about a specific board"""
    board = await fetch_from_api(f"/boards/{board_id}")
    return format_board_details(board)

@mcp.tool()
async def get_lists(board_id: str) -> str:
    """Get all lists in a board"""
    lists = await fetch_from_api(f"/boards/{board_id}/lists")
    return format_lists(lists)

@mcp.tool()
async def get_cards(list_id: str) -> str:
    """Get all cards in a list"""
    cards = await fetch_from_api(f"/lists/{list_id}/cards")
    return format_cards(cards)

@mcp.tool()
async def get_card_details(card_id: str) -> str:
    """Get detailed information about a specific card"""
    card = await fetch_from_api(f"/cards/{card_id}")
    return format_card_details(card)

@mcp.tool()
async def create_card(list_id: str, name: str, desc: str = "") -> str:
    """Create a new card in a list"""
    data = {
        "name": name,
        "desc": desc,
        "idList": list_id
    }
    card = await post_to_api("/cards", data=data)
    return f"Card created successfully:\n{format_card_details(card)}"

@mcp.tool()
async def update_card(card_id: str, name: str = None, desc: str = None, 
                     due: str = None, labels: list = None) -> str:
    """Update an existing card"""
    data = {}
    if name is not None:
        data["name"] = name
    if desc is not None:
        data["desc"] = desc
    if due is not None:
        data["due"] = due
    if labels is not None:
        data["idLabels"] = ",".join(labels)
    
    card = await put_to_api(f"/cards/{card_id}", data=data)
    return f"Card updated successfully:\n{format_card_details(card)}"

@mcp.tool()
async def move_card(card_id: str, list_id: str) -> str:
    """Move a card to a different list"""
    data = {"idList": list_id}
    card = await put_to_api(f"/cards/{card_id}", data=data)
    return f"Card moved successfully:\n{format_card_details(card)}"

@mcp.tool()
async def add_comment(card_id: str, text: str) -> str:
    """Add a comment to a card"""
    data = {"text": text}
    comment = await post_to_api(f"/cards/{card_id}/actions/comments", data=data)
    return f"Comment added successfully:\n{comment['data']['text']}"

@mcp.tool()
async def get_board_members(board_id: str) -> str:
    """Get all members of a board"""
    members = await fetch_from_api(f"/boards/{board_id}/members")
    return format_members(members)

# Helper formatting functions

def format_boards(boards: list) -> str:
    """Format a list of boards for display"""
    if not boards:
        return "No boards found."
    
    result = "# Trello Boards\n\n"
    for board in boards:
        result += f"## {board['name']}\n"
        result += f"ID: {board['id']}\n"
        result += f"URL: {board['url']}\n"
        result += f"Last Activity: {board['dateLastActivity']}\n\n"
    
    return result

def format_board_details(board: dict) -> str:
    """Format board details for display"""
    result = f"# {board['name']}\n\n"
    result += f"ID: {board['id']}\n"
    result += f"URL: {board['url']}\n"
    result += f"Description: {board.get('desc', 'No description')}\n"
    result += f"Last Activity: {board['dateLastActivity']}\n"
    result += f"Members: {board['memberships']}\n"
    return result

def format_lists(lists: list) -> str:
    """Format a list of lists for display"""
    if not lists:
        return "No lists found."
    
    result = "# Lists\n\n"
    for list_item in lists:
        result += f"## {list_item['name']}\n"
        result += f"ID: {list_item['id']}\n"
        result += f"Cards: {list_item.get('cards', [])}\n\n"
    
    return result

def format_cards(cards: list) -> str:
    """Format a list of cards for display"""
    if not cards:
        return "No cards found."
    
    result = "# Cards\n\n"
    for card in cards:
        result += f"## {card['name']}\n"
        result += f"ID: {card['id']}\n"
        result += f"Description: {card.get('desc', 'No description')}\n"
        result += f"Due Date: {card.get('due', 'No due date')}\n"
        result += f"Labels: {', '.join(label['name'] for label in card.get('labels', []))}\n\n"
    
    return result

def format_card_details(card: dict) -> str:
    """Format card details for display"""
    result = f"# {card['name']}\n\n"
    result += f"ID: {card['id']}\n"
    result += f"Description: {card.get('desc', 'No description')}\n"
    result += f"Due Date: {card.get('due', 'No due date')}\n"
    result += f"Labels: {', '.join(label['name'] for label in card.get('labels', []))}\n"
    result += f"URL: {card['url']}\n"
    result += f"Last Activity: {card['dateLastActivity']}\n"
    return result

def format_members(members: list) -> str:
    """Format a list of members for display"""
    if not members:
        return "No members found."
    
    result = "# Board Members\n\n"
    for member in members:
        result += f"## {member['fullName']}\n"
        result += f"Username: {member['username']}\n"
        result += f"Role: {member['memberType']}\n\n"
    
    return result

if __name__ == "__main__":
    print("Starting Trello MCP server...")
    mcp.run(transport = "stdio") 