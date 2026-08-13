from __future__ import annotations

import json
from typing import Any

from openai import OpenAI
from pydantic import BaseModel

from email_agent.config import settings
from email_agent.exceptions import LLMProviderError


class LLMResponse:
    """Normalized response object."""
    def __init__(self, content: str, tool_calls: list[dict[str, Any]] | None = None):
        self.content = content
        self.tool_calls = tool_calls or []
    
    def __repr__(self):
        return f"LLMResponse(content={self.content!r}, tool_cals={self.tool_calls!r})"
    
class LLMClient:
    """provider-agnostic LLM client (OpenAI-compatible API)."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.cerebras_api_key
        self.base_url = base_url or settings.cerebras_base_url
        self.model = model or settings.cerebras_model

        if not self.api_key:
            raise LLMProviderError("Cerebras API key is missing.")
        
        self._client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.0,
        max_tokens: int = 1000,
        tools: list[dict[str, Any]] | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> LLMResponse:
        """Send a chat completion request and return a normalized response."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if tools:
            kwargs["tools"] = tools
        
        if response_format:
            kwargs["response_format"] = response_format
        
        try:
            completion = self._client.chat.completions.create(**kwargs)
        except Exception as e:
            raise LLMProviderError(f"Cerebras API Call failed: {e}") from e

        choice = completion.choices[0]
        message = choice.message

        tool_calls = None
        if message.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                }
                for tc in message.tool_calls
            ]
        
        return LLMResponse(
            content=message.content or "",
            tool_calls=tool_calls,
        )
    
    def chat_structured(
        self,
        messages: list[dict[str, str]],
        output_schema: type[BaseModel],
        *,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> BaseModel:
        """Request structured output as Pydantic model"""

        function_spec = {
            "type": "function",
            "function": {
                "name": "generate_structured_output",
                "description": "Return a structured output matching the given schema",
                "parameters": output_schema.model_json_schema(),
            },
        }

        response = self.chat(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=[function_spec],
        )

        if not response.tool_calls:
            try:
                return output_schema.model_validate_json(response.content)
            except Exception as e:
                raise LLMProviderError(f"No tool call and content not valid JSON. {response.content}") from e

        tool_call = response.tool_calls[0]
        if tool_call["function"]["name"] != "generate_structured_output":
            raise LLMProviderError(f"Unexpected tool call: {tool_call['function']['name']}")

        try:
            arguments = json.loads(tool_call["function"]["arguments"])
            return output_schema.model_validate(arguments)
        except (json.JSONDecodeError, Exception) as e:
            raise LLMProviderError(f"failed to validate schema from arguments: {e}") from e



    

