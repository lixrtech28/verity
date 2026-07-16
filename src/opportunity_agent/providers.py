from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from typing import Any

import httpx

from .prompts import SYSTEM_PROMPT, build_user_prompt


class ProviderError(RuntimeError):
    pass


class LLMProvider(ABC):
    name: str
    model: str

    @abstractmethod
    def generate_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self, model: str, api_key: str | None = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ProviderError("OPENAI_API_KEY is not set")

    def generate_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = {
            "model": self.model,
            "input": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(json.dumps(payload))},
            ],
            "text": {"format": {"type": "json_object"}},
        }
        with httpx.Client(timeout=120) as client:
            response = client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=body,
            )
        if response.is_error:
            raise ProviderError(f"OpenAI request failed: {response.status_code} {response.text}")
        data = response.json()
        text = data.get("output_text")
        if not text:
            for item in data.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        text = content.get("text")
                        break
        if not text:
            raise ProviderError("OpenAI response contained no output text")
        return json.loads(text.replace("PROVIDER_NAME", self.name).replace("MODEL_NAME", self.model))


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, model: str, api_key: str | None = None):
        self.model = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ProviderError("ANTHROPIC_API_KEY is not set")

    def generate_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = {
            "model": self.model,
            "max_tokens": 5000,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": build_user_prompt(json.dumps(payload))}],
        }
        with httpx.Client(timeout=120) as client:
            response = client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json=body,
            )
        if response.is_error:
            raise ProviderError(f"Anthropic request failed: {response.status_code} {response.text}")
        blocks = response.json().get("content", [])
        text = "".join(block.get("text", "") for block in blocks if block.get("type") == "text")
        return json.loads(text.replace("PROVIDER_NAME", self.name).replace("MODEL_NAME", self.model))


class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(json.dumps(payload))},
            ],
        }
        with httpx.Client(timeout=180) as client:
            response = client.post(f"{self.base_url}/api/chat", json=body)
        if response.is_error:
            raise ProviderError(f"Ollama request failed: {response.status_code} {response.text}")
        text = response.json()["message"]["content"]
        return json.loads(text.replace("PROVIDER_NAME", self.name).replace("MODEL_NAME", self.model))


class MockProvider(LLMProvider):
    """Deterministic provider for learning, tests, and zero-cost demos."""

    name = "mock"
    model = "deterministic-v1"

    def generate_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        company = payload["company"]
        role = payload["buyer_role"]
        focus = payload["problem_focus"]
        claims = []
        for source in payload["sources"][:3]:
            sentence = source["text"].strip().split(".")[0].strip()
            if sentence:
                claims.append({
                    "text": sentence,
                    "claim_type": "fact",
                    "source_ids": [source["source_id"]],
                    "confidence": 0.9,
                })
        return {
            "company": company,
            "buyer_role": role,
            "problem_focus": focus,
            "claims": claims,
            "workflow_hypothesis": [f"The {role} may own or influence {focus}."],
            "unresolved_questions": [
                "What happened in the most recent real exception?",
                "Which systems and people touched that case?",
                "What measurable consequence did the failure create?",
            ],
            "outreach_draft": (
                f"Hi — I am mapping how {focus} operates at companies like {company}. "
                "I found a few public signals, but I do not want to mistake them for internal truth. "
                "Could I ask about the last real exception? I will share the anonymized map afterward."
            ),
            "discovery_questions": [
                "Walk me through the last case from trigger to resolution.",
                "Where did ownership change hands?",
                "Which information was missing or conflicting?",
                "How was the outcome verified?",
            ],
            "human_approval_required": True,
            "approved_by": None,
            "provider": self.name,
            "model": self.model,
        }


def get_provider(name: str, model: str | None = None) -> LLMProvider:
    normalized = name.lower()
    if normalized == "mock":
        return MockProvider()
    if normalized == "openai":
        if not model:
            raise ProviderError("Pass --model with a model available in your OpenAI account")
        return OpenAIProvider(model=model)
    if normalized == "anthropic":
        if not model:
            raise ProviderError("Pass --model with a model available in your Anthropic account")
        return AnthropicProvider(model=model)
    if normalized == "ollama":
        return OllamaProvider(model=model or "qwen3:8b")
    raise ProviderError(f"Unknown provider: {name}")
