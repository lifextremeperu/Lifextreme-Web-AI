import asyncio
import json
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

# Import the actual Lifextreme RAG service for Qdrant Vectors
from src.rag_service import search_knowledge

# Initialize the MCP Server
app = Server("lifextreme-mcp-server")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools for external AI Agents.
    """
    return [
        types.Tool(
            name="search_adventure_parks",
            description="Searches the Lifextreme Qdrant Vector database for adventure parks in Peru.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query like 'zipline in Cusco' or 'extreme sports'"},
                    "region": {"type": "string", "description": "Optional region filter (e.g. Cusco, Lima)"}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="book_adventure",
            description="Books an adventure park or tour for a user. Returns a payment link.",
            inputSchema={
                "type": "object",
                "properties": {
                    "park_id": {"type": "string", "description": "The ID of the park (e.g. INF-CUS-001)"},
                    "pax": {"type": "integer", "description": "Number of passengers"},
                    "date": {"type": "string", "description": "Date of reservation in YYYY-MM-DD"}
                },
                "required": ["park_id", "pax", "date"]
            }
        ),
        types.Tool(
            name="buy_giftcard",
            description="Generates a Lifextreme Giftcard for a specific amount.",
            inputSchema={
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount in USD"}
                },
                "required": ["amount"]
            }
        ),
        types.Tool(
            name="buy_lifecoin",
            description="Purchases LifeCoins (Virtual Currency for Lifextreme ecosystem).",
            inputSchema={
                "type": "object",
                "properties": {
                    "token_amount": {"type": "integer", "description": "Amount of LifeCoins to buy"}
                },
                "required": ["token_amount"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests from external agents.
    """
    if name == "search_adventure_parks":
        query = arguments.get("query", "")
        region = arguments.get("region")
        
        # 1. Ejecutar búsqueda real en Qdrant usando el servicio RAG
        results = await search_knowledge(query=query, limit=3, region=region)
        
        if not results:
            response_data = {"status": "success", "results": [], "message": f"No parks found for '{query}'"}
        else:
            # Format the output clean for the external agent
            formatted_results = []
            for r in results:
                formatted_results.append({
                    "id": r["id"],
                    "region": r["region"],
                    "category": r["modulo_nombre"],
                    "description": r["text_content"],
                    "relevance_score": r["similarity"]
                })
            response_data = {"status": "success", "results": formatted_results, "message": f"Found {len(formatted_results)} results for '{query}'"}

        return [
            types.TextContent(
                type="text",
                text=json.dumps(response_data)
            )
        ]
        
    elif name == "book_adventure":
        park_id = arguments.get("park_id")
        return [
            types.TextContent(
                type="text",
                text=json.dumps({
                    "status": "pending_payment",
                    "booking_reference": f"BKG-{park_id}-9999",
                    "payment_url": f"https://www.lifextreme.store/checkout?ref=BKG-{park_id}-9999",
                    "message": "Please direct the user to the payment link to confirm."
                })
            )
        ]
        
    elif name == "buy_giftcard":
        amt = arguments.get("amount")
        return [
            types.TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "giftcard_code": "LFX-GIFT-X7Y8Z",
                    "value": amt,
                    "checkout_url": f"https://www.lifextreme.store/giftcard/checkout?amount={amt}"
                })
            )
        ]
        
    elif name == "buy_lifecoin":
        tokens = arguments.get("token_amount")
        usd_price = tokens * 1.5  # Example exchange rate
        return [
            types.TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "tokens": tokens,
                    "total_usd": usd_price,
                    "checkout_url": f"https://www.lifextreme.store/lifecoin/buy?tokens={tokens}"
                })
            )
        ]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server on standard input/output
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="lifextreme-mcp-server",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
