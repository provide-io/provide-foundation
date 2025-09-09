"""OpenObserve integration configuration."""

from attrs import define

from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.base import field


@define(slots=True, repr=False)
class OpenObserveConfig(RuntimeConfig):
    """Configuration for OpenObserve integration."""

    url: str | None = field(
        default=None,
        env_var="OPENOBSERVE_URL",
        description="OpenObserve URL endpoint",
    )
    org: str | None = field(
        default=None,
        env_var="OPENOBSERVE_ORG",
        description="OpenObserve organization",
    )
    user: str | None = field(
        default=None,
        env_var="OPENOBSERVE_USER",
        description="OpenObserve username",
    )
    password: str | None = field(
        default=None,
        env_var="OPENOBSERVE_PASSWORD",
        description="OpenObserve password",
    )
    stream: str | None = field(
        default=None,
        env_var="OPENOBSERVE_STREAM",
        description="OpenObserve stream name",
    )