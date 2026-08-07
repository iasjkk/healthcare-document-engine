from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ModelProvider(str, Enum):
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    VLLM = "vllm"
    HUGGINGFACE = "huggingface"
    CUSTOM = "custom"


class ModelCallStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRY = "RETRY"


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0
    total_tokens: int = 0


class CostInfo(BaseModel):
    prompt_cost: float = 0.0
    completion_cost: float = 0.0
    total_cost: float = 0.0
    currency: str = "USD"


class ModelRequest(BaseModel):
    request_id: str

    provider: ModelProvider

    model_name: str

    agent_name: str

    node_name: str

    system_prompt: str = ""

    user_prompt: str = ""

    parameters: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime


class ModelResponse(BaseModel):
    response_id: str

    content: str = ""

    reasoning: str | None = None

    finish_reason: str | None = None

    latency_ms: float = 0.0

    token_usage: TokenUsage = Field(default_factory=TokenUsage)

    cost: CostInfo = Field(default_factory=CostInfo)

    raw_response: dict[str, Any] = Field(default_factory=dict)


class ModelExecution(BaseModel):
    execution_id: str

    request: ModelRequest

    response: ModelResponse | None = None

    status: ModelCallStatus = ModelCallStatus.PENDING

    retry_count: int = 0

    error_message: str | None = None

    started_at: datetime

    completed_at: datetime | None = None


class ModelState(BaseModel):
    """
    Stores every LLM execution during the workflow.
    """

    executions: list[ModelExecution] = Field(default_factory=list)