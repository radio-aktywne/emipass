from emipass.api.routes.ping.models import PingResponse


class Service:
    """Service for the ping endpoint."""

    async def ping(self) -> PingResponse:
        """Do nothing."""

        return None
