import httpx
from typing import Dict, Any, Optional
from ..config import settings
from .mock_mcp_client import mock_mcp_client


class MCPClient:
    def __init__(self):
        self.base_url = settings.mcp_server_url
        self.timeout = 30  # seconds
        # Check if the MCP server is available
        self.is_available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """
        Check if the MCP server is available
        """
        try:
            import urllib.request
            import urllib.error
            import socket
            
            # Parse the URL to get host and port
            from urllib.parse import urlparse
            parsed_url = urlparse(self.base_url)
            host = parsed_url.hostname
            port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
            
            # Try to connect to the host and port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 second timeout
            result = sock.connect_ex((host, port))
            sock.close()
            
            return result == 0
        except Exception:
            return False  # If any error occurs, assume it's not available
        
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool with the given parameters
        """
        # If the real server is not available, use the mock client
        if not self.is_available:
            return await mock_mcp_client.call_tool(tool_name, params)
        
        url = f"{self.base_url}/{tool_name}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=params)

                if response.status_code == 200:
                    return {
                        "success": True,
                        "data": response.json()
                    }
                else:
                    return {
                        "success": False,
                        "error": response.json() if response.content else {"message": "Unknown error"}
                    }

        except httpx.TimeoutException:
            return {
                "success": False,
                "error": {"code": "TIMEOUT", "message": "Request timed out"}
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": {"code": "REQUEST_ERROR", "message": str(e)}
            }
        except Exception as e:
            return {
                "success": False,
                "error": {"code": "UNKNOWN_ERROR", "message": str(e)}
            }
    
    # Specific tool methods for better organization
    async def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        params = {
            "user_id": user_id,
            "title": title,
            "description": description or ""
        }
        return await self.call_tool("add_task", params)
    
    async def list_tasks(self, user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        params = {
            "user_id": user_id,
            "status": status or "all"
        }
        return await self.call_tool("list_tasks", params)
    
    async def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        params = {
            "user_id": user_id,
            "task_id": task_id
        }
        return await self.call_tool("complete_task", params)
    
    async def update_task(self, user_id: str, task_id: str, **kwargs) -> Dict[str, Any]:
        params = {
            "user_id": user_id,
            "task_id": task_id
        }
        params.update(kwargs)
        return await self.call_tool("update_task", params)
    
    async def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        params = {
            "user_id": user_id,
            "task_id": task_id
        }
        return await self.call_tool("delete_task", params)


# Global instance of the MCP client
mcp_client = MCPClient()