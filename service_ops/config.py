from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = REPOSITORY_ROOT / ".env"


@dataclass(frozen=True)
class Settings:
    foundry_project_endpoint: str = ""
    foundry_model: str = ""
    foundry_agent_name: str = ""
    foundry_iq_mcp_endpoint: str = ""
    local_mcp_endpoint: str = "http://127.0.0.1:8000/mcp"
    foundry_agent_version: str = ""

    @classmethod
    def from_environment(
        cls,
        *,
        env: Mapping[str, str] | None = None,
        env_file: Path = DEFAULT_ENV_FILE,
    ) -> Settings:
        if env is None:
            load_dotenv(env_file, override=False)
            env = os.environ
        return cls(
            foundry_project_endpoint=env.get("FOUNDRY_PROJECT_ENDPOINT", "").strip(),
            foundry_model=env.get("FOUNDRY_MODEL", "").strip(),
            foundry_agent_name=env.get("FOUNDRY_AGENT_NAME", "").strip(),
            foundry_iq_mcp_endpoint=env.get("FOUNDRY_IQ_MCP_ENDPOINT", "").strip(),
            local_mcp_endpoint=env.get("LOCAL_MCP_ENDPOINT", "http://127.0.0.1:8000/mcp").strip(),
            foundry_agent_version=env.get("FOUNDRY_AGENT_VERSION", "").strip(),
        )

    def missing_for_chat_agent(self) -> tuple[str, ...]:
        missing: list[str] = []
        if not self.foundry_project_endpoint or "YOUR-" in self.foundry_project_endpoint:
            missing.append("FOUNDRY_PROJECT_ENDPOINT")
        if not self.foundry_model or self.foundry_model == "MODEL-DEPLOYMENT-NAME":
            missing.append("FOUNDRY_MODEL")
        return tuple(missing)

    def require_chat_agent(self) -> None:
        missing = self.missing_for_chat_agent()
        if missing:
            joined = ", ".join(missing)
            raise ValueError(f"Set {joined} in .env before running the agent.")
