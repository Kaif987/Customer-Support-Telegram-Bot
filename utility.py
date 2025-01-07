import httpx
from pydantic import BaseModel, Field
from typing import Literal, TypedDict, Any, NotRequired
import asyncio

class ToolCall(TypedDict):
    """Represents a request to call a tool."""

    name: str
    """The name of the tool to be called."""
    args: dict[str, Any]
    """The arguments to the tool call."""
    id: str | None
    """An identifier associated with the tool call."""
    type: NotRequired[Literal["tool_call"]]

class AgenticClientError(Exception):
    pass

class ChatMessage(BaseModel):
    """Message in a chat."""

    type: Literal["human", "ai", "tool", "custom", "interrupt"] = Field(
        description="Role of the message.",
        examples=["human", "ai", "tool", "custom", "interrupt"],
    )
    content: str = Field(
        description="Content of the message.",
        examples=["Hello, world!"],
    )
    tool_calls: list[ToolCall] = Field(
        description="Tool calls in the message.",
        default=[],
    )
    tool_call_id: str | None = Field(
        description="Tool call that this message is responding to.",
        default=None,
        examples=["call_Jja7J89XsjrOLA5r!MEOW!SL"],
    )
    run_id: str | None = Field(
        description="Run ID of the message.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    response_metadata: dict[str, Any] = Field(
        description="Response metadata. For example: response headers, logprobs, token counts.",
        default={},
    )
    custom_data: dict[str, Any] = Field(
        description="Custom message data.",
        default={},
    )

class ChatMessages(BaseModel):
    messages: list[ChatMessage]

async def call_agent(msg: str, thread_id: str) -> ChatMessages:
    base_url = "http://c960ga0jlt8f924pn0p0ff34ao.ingress.hurricane.akash.pub"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{base_url}/customer-support-agent/invoke',json={
                "type": "user",
                "message": msg,
                "thread_id": thread_id,
            }, timeout=None)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise AgenticClientError("An error occured ", e)
            
    return ChatMessages.model_validate(response.json())
