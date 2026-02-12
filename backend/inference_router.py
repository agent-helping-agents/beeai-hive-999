"""
Inference Router - Decentralized AI Inference Platform Connector

This module provides a unified interface for accessing multiple decentralized AI inference platforms
with support for platform selection, fallback mechanisms, and consistent API responses.
"""

import os
from enum import Enum
from typing import Optional, Dict, Any
from beeai_framework.backend.message import Message
from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.types import ChatModelOutput
from beeai_framework.tools import StringToolOutput, tool


class InferencePlatform(Enum):
    """Supported decentralized AI inference platforms"""

    OPENROUTER = "openrouter"
    CHUTES = "chutes"
    RENDER = "render"
    FORTYTWO = "fortytwo"
    OLLAMA = "ollama"


class InferenceRouter:
    """
    A router for accessing decentralized AI inference platforms with fallback support.

    This class provides a unified interface to interact with multiple AI inference platforms
    while handling platform selection, API key management, and fallback mechanisms.
    """

    def __init__(
        self, default_platform: InferencePlatform = InferencePlatform.OPENROUTER
    ):
        """
        Initialize the inference router.

        Args:
            default_platform: Default platform to use if not specified
        """
        self.default_platform = default_platform
        self.platform_configs = self._load_platform_configs()

    def _load_platform_configs(self) -> Dict[InferencePlatform, Dict[str, Any]]:
        """Load platform configurations from environment variables."""
        return {
            InferencePlatform.OPENROUTER: {
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "base_url": "https://openrouter.ai/api/v1",
                "models": [
                    "meta-llama/llama-3.2-3b-instruct:free",
                    "anthropic/claude-3-haiku:free",
                ],
            },
            InferencePlatform.CHUTES: {
                "api_key": os.getenv("CHUTES_API_KEY"),
                "base_url": "https://api.chutes.ai/v1",
                "models": ["llama-3.2:3b"],
            },
            InferencePlatform.RENDER: {
                "api_key": os.getenv("RENDER_API_KEY"),
                "base_url": "https://api.render.com/v1",
                "models": ["llama-3.2"],
            },
            InferencePlatform.FORTYTWO: {
                "api_key": os.getenv("FORTYTWO_API_KEY"),
                "base_url": "https://api.fortytwo.ai/v1",
                "models": ["llama-3.2-3b"],
            },
            InferencePlatform.OLLAMA: {
                "base_url": "http://localhost:11434",
                "models": ["llama3.2:3b"],
            },
        }

    def is_platform_available(self, platform: InferencePlatform) -> bool:
        """
        Check if a platform is available for use.

        Args:
            platform: Platform to check

        Returns:
            True if platform is available, False otherwise
        """
        config = self.platform_configs[platform]

        # Ollama is available if running locally
        if platform == InferencePlatform.OLLAMA:
            try:
                import requests

                response = requests.get(f"{config['base_url']}/api/tags")
                return response.status_code == 200
            except:
                return False

        # Other platforms require API keys
        return config.get("api_key") is not None

    def get_available_platforms(self) -> list[InferencePlatform]:
        """Get list of available platforms."""
        return [
            platform
            for platform in InferencePlatform
            if self.is_platform_available(platform)
        ]

    async def chat(
        self,
        model: str,
        messages: list[Message],
        platform: Optional[InferencePlatform] = None,
        **kwargs,
    ) -> ChatModelOutput:
        """
        Send chat messages to an AI model using the specified or default platform.

        Args:
            model: Model to use for inference
            messages: List of chat messages
            platform: Platform to use for inference (defaults to self.default_platform)
            **kwargs: Additional parameters for model interaction

        Returns:
            LLMOutput containing the response

        Raises:
            Exception: If no available platforms or all attempts fail
        """
        if platform is None:
            platform = self.default_platform

        # Try specified platform first
        if self.is_platform_available(platform):
            try:
                return await self._call_platform(platform, model, messages, **kwargs)
            except Exception as e:
                print(f"Platform {platform.value} failed: {e}")

        # Try fallback platforms
        fallback_platforms = self.get_available_platforms()
        if platform in fallback_platforms:
            fallback_platforms.remove(platform)

        for fallback in fallback_platforms:
            try:
                return await self._call_platform(fallback, model, messages, **kwargs)
            except Exception as e:
                print(f"Fallback platform {fallback.value} failed: {e}")

        raise Exception("No available platforms for AI inference")

    async def _call_platform(
        self, platform: InferencePlatform, model: str, messages: list[Message], **kwargs
    ) -> ChatModelOutput:
        """
        Call a specific inference platform.

        Args:
            platform: Platform to use
            model: Model to use
            messages: List of chat messages
            **kwargs: Additional parameters

        Returns:
            LLMOutput with the response

        Raises:
            Exception: If platform call fails
        """
        config = self.platform_configs[platform]

        if platform == InferencePlatform.OLLAMA:
            return await self._call_ollama(model, messages, config, **kwargs)
        elif platform == InferencePlatform.OPENROUTER:
            return await self._call_openrouter(model, messages, config, **kwargs)
        elif platform == InferencePlatform.CHUTES:
            return await self._call_chutes(model, messages, config, **kwargs)
        elif platform == InferencePlatform.RENDER:
            return await self._call_render(model, messages, config, **kwargs)
        elif platform == InferencePlatform.FORTYTWO:
            return await self._call_fortytwo(model, messages, config, **kwargs)
        else:
            raise Exception(f"Unsupported platform: {platform.value}")

    async def _call_ollama(
        self, model: str, messages: list[Message], config: Dict[str, Any], **kwargs
    ) -> ChatModelOutput:
        """Call Ollama platform."""
        from beeai_framework.models import OllamaChatModel

        llm = OllamaChatModel.from_name(f"ollama:{model}")
        response = await llm.messages_async(messages, **kwargs)
        return response

    async def _call_openrouter(
        self, model: str, messages: list[Message], config: Dict[str, Any], **kwargs
    ) -> ChatModelOutput:
        """Call OpenRouter platform."""
        from beeai_framework.models import OpenAIChatModel

        # If model starts with "openrouter:", extract just the model name
        if model.startswith("openrouter:"):
            model = model[len("openrouter:") :]

        llm = OpenAIChatModel.from_name(model)
        llm.api_key = config["api_key"]
        llm.base_url = config["base_url"]

        response = await llm.messages_async(messages, **kwargs)
        return response

    async def _call_chutes(
        self, model: str, messages: list[Message], config: Dict[str, Any], **kwargs
    ) -> ChatModelOutput:
        """Call Chutes.ai platform."""
        from beeai_framework.models import OpenAIChatModel

        llm = OpenAIChatModel.from_name(model)
        llm.api_key = config["api_key"]
        llm.base_url = config["base_url"]

        response = await llm.messages_async(messages, **kwargs)
        return response

    async def _call_render(
        self, model: str, messages: list[Message], config: Dict[str, Any], **kwargs
    ) -> ChatModelOutput:
        """Call Render Network platform."""
        # Render Network API integration
        import requests

        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": [
                {"role": msg.role, "content": msg.content} for msg in messages
            ],
            **kwargs,
        }

        response = requests.post(
            f"{config['base_url']}/inference", headers=headers, json=data
        )
        response.raise_for_status()

        result = response.json()
        return LLMOutput(
            result=result["choices"][0]["message"]["content"], tool_calls=[]
        )

    async def _call_fortytwo(
        self, model: str, messages: list[Message], config: Dict[str, Any], **kwargs
    ) -> ChatModelOutput:
        """Call Fortytwo platform."""
        # Fortytwo API integration
        import requests

        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": [
                {"role": msg.role, "content": msg.content} for msg in messages
            ],
            **kwargs,
        }

        response = requests.post(
            f"{config['base_url']}/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()

        result = response.json()
        return LLMOutput(
            result=result["choices"][0]["message"]["content"], tool_calls=[]
        )


# Global router instance
_router: Optional[InferenceRouter] = None


def get_router(platform: Optional[InferencePlatform] = None) -> InferenceRouter:
    """
    Get or create the global inference router instance.

    Args:
        platform: Default platform to use

    Returns:
        InferenceRouter instance
    """
    # If platform is specified, always create a new router instance
    if platform is not None:
        return InferenceRouter(platform)

    # Otherwise, use a global singleton instance
    global _router
    if _router is None:
        # Try to get default platform from environment variables
        default_platform = os.getenv("INFERENCE_PLATFORM", "openrouter").lower()
        try:
            _router = InferenceRouter(InferencePlatform(default_platform))
        except ValueError:
            _router = InferenceRouter(InferencePlatform.OPENROUTER)
    return _router


@tool
def list_inference_platforms() -> StringToolOutput:
    """
    List available inference platforms with status.

    Returns:
        StringToolOutput with list of platforms and their availability
    """
    router = get_router()
    platforms = []

    for platform in InferencePlatform:
        status = "✓" if router.is_platform_available(platform) else "✗"
        platforms.append(f"{status} {platform.value}")

    return StringToolOutput(result="\n".join(platforms))


@tool
def get_default_inference_platform() -> StringToolOutput:
    """
    Get the current default inference platform.

    Returns:
        StringToolOutput with default platform
    """
    router = get_router()
    return StringToolOutput(result=router.default_platform.value)


@tool
def set_inference_platform(platform: str) -> StringToolOutput:
    """
    Set the default inference platform.

    Args:
        platform: Platform name to set as default

    Returns:
        StringToolOutput confirming the change
    """
    try:
        platform_enum = InferencePlatform(platform.lower())
        global _router
        _router = InferenceRouter(platform_enum)
        return StringToolOutput(result=f"Default platform set to {platform_enum.value}")
    except ValueError:
        return StringToolOutput(result=f"Invalid platform: {platform}")
