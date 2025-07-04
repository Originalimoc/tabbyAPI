"""Common types for OAI."""

from pydantic import BaseModel, Field
from typing import Optional, Union

from common.sampling import BaseSamplerRequest, get_default_sampler_value


class UsageStats(BaseModel):
    """Represents usage stats."""

    prompt_tokens: int
    prompt_time: Optional[float] = None
    prompt_tokens_per_sec: Optional[Union[float, str]] = None
    completion_tokens: int
    completion_time: Optional[float] = None
    completion_tokens_per_sec: Optional[Union[float, str]] = None
    total_tokens: int
    total_time: Optional[float] = None


class CompletionResponseFormat(BaseModel):
    type: str = "text"


class ChatCompletionStreamOptions(BaseModel):
    include_usage: Optional[bool] = False


class CommonCompletionRequest(BaseSamplerRequest):
    """Represents a common completion request."""

    # Model information
    # This parameter is not used, the loaded model is used instead
    model: Optional[str] = None

    # Generation info (remainder is in BaseSamplerRequest superclass)
    stream: Optional[bool] = False
    stream_options: Optional[ChatCompletionStreamOptions] = None
    response_format: Optional[CompletionResponseFormat] = Field(
        default_factory=CompletionResponseFormat
    )
    n: Optional[int] = Field(
        default_factory=lambda: get_default_sampler_value("n", 1),
        ge=1,
    )

    # Extra OAI request stuff
    best_of: Optional[int] = Field(
        description="Not parsed. Only used for OAI compliance.", default=None
    )
    echo: Optional[bool] = Field(
        description="Not parsed. Only used for OAI compliance.", default=False
    )
    suffix: Optional[str] = Field(
        description="Not parsed. Only used for OAI compliance.", default=None
    )
    user: Optional[str] = Field(
        description="Not parsed. Only used for OAI compliance.", default=None
    )
