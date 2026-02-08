import cohere
from typing import Dict, Any, List, Optional
from ..config import settings
from ..schemas.chat_schemas import ToolCall, ToolCallResult
from .mock_client import mock_cohere_client


class CohereClient:
    def __init__(self):
        try:
            # Try to initialize with the actual API key
            if settings.cohere_api_key:
                self.client = cohere.Client(settings.cohere_api_key)
                self.is_mock = False
            else:
                # Fall back to mock client if no API key is provided
                self.is_mock = True
        except Exception as e:
            print(f"Warning: Failed to initialize Cohere client: {e}. Falling back to mock client.")
            self.is_mock = True
        
    def chat_with_tools(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Send a chat request to Cohere with tool calling capability
        """
        if self.is_mock:
            # Use the mock client if the real client is not available
            return mock_cohere_client.chat_with_tools(
                message=message,
                conversation_history=conversation_history,
                tools=tools
            )
        
        try:
            # Prepare the chat history
            formatted_history = []
            if conversation_history:
                for item in conversation_history:
                    # Convert our internal format to Cohere's format
                    role = "USER" if item["role"] == "user" else "CHATBOT"
                    formatted_history.append({
                        "role": role,
                        "message": item["message"]
                    })

            # Prepare the tools if provided
            if tools:
                response = self.client.chat(
                    message=message,
                    chat_history=formatted_history,
                    tools=tools,
                    force_single_step=True  # Force the model to use tools if needed
                )
            else:
                response = self.client.chat(
                    message=message,
                    chat_history=formatted_history
                )

            # Extract the response
            result = {
                "text": response.text,
                "tool_calls": []
            }

            # Process tool calls if any
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    result["tool_calls"].append({
                        "name": tool_call.name,
                        "parameters": tool_call.parameters
                    })

            return result

        except Exception as e:
            # Handle any errors from the Cohere API
            print(f"Warning: Cohere API error: {str(e)}. Falling back to mock client.")
            return mock_cohere_client.chat_with_tools(
                message=message,
                conversation_history=conversation_history,
                tools=tools
            )
    
    def process_tool_results(
        self,
        original_message: str,
        conversation_history: List[Dict[str, str]],
        tool_results: List[Dict[str, Any]]
    ) -> str:
        """
        Process the results from tool executions and generate a final response
        """
        if self.is_mock:
            # Use the mock client if the real client is not available
            return mock_cohere_client.process_tool_results(
                original_message=original_message,
                conversation_history=conversation_history,
                tool_results=tool_results
            )
        
        try:
            # Add the tool results to the conversation history
            updated_history = conversation_history.copy()
            for result in tool_results:
                updated_history.append({
                    "role": "tool",
                    "message": f"Tool {result['name']} returned: {result['result']}"
                })

            # Format history for Cohere
            formatted_history = []
            for item in updated_history:
                role = "USER" if item["role"] == "user" else "CHATBOT"
                if item["role"] == "tool":
                    role = "SYSTEM"  # Use SYSTEM role for tool responses
                formatted_history.append({
                    "role": role,
                    "message": item["message"]
                })

            # Get the final response from the model
            response = self.client.chat(
                message=original_message,
                chat_history=formatted_history
            )

            return response.text

        except Exception as e:
            # Handle any errors from the Cohere API
            print(f"Warning: Cohere API error while processing tool results: {str(e)}. Falling back to mock client.")
            return mock_cohere_client.process_tool_results(
                original_message=original_message,
                conversation_history=conversation_history,
                tool_results=tool_results
            )


# Global instance of the Cohere client
cohere_client = CohereClient()