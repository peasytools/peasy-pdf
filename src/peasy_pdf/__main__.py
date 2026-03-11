"""Allow running ``python -m peasy_pdf`` to start the MCP server."""

from peasy_pdf.mcp_server import mcp

if __name__ == "__main__":
    mcp.run()
