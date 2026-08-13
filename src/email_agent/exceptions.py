class EmailAgentError(Exception):
    """Base exception for all email-agent errors"""

class LLMProviderError(EmailAgentError):
    """Raised when the LLM provider fails."""

class TriageError(EmailAgentError):
    """Raised when  triage classification fails or returns invalid output"""

class ToolExecutionError(EmailAgentError):
    """Raised when a tool fails during execution"""

class MemoryStoreError(EmailAgentError):
    """Raised when the long-term memory store cannot be read/writtern."""

class HumanInterruptError(EmailAgentError):
    """Raised when a human interrupt is not resolved in time."""

class ConfigurationError(EmailAgentError):
    """Raised when the agent is misconfigured"""
