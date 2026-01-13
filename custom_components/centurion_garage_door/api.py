"""Sample API Client for Centurion Garage Door."""

import aiohttp
import async_timeout


class CenturionGarageApiClientError(Exception):
    """Base exception for Centurion Garage API client errors."""


class CenturionGarageApiClientCommunicationError(CenturionGarageApiClientError):
    """Exception for communication errors with Centurion Garage API client."""


class CenturionGarageApiClientAuthenticationError(CenturionGarageApiClientError):
    """Exception for authentication errors with Centurion Garage API client."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Raise for HTTP errors or authentication failures."""
    if response.status in (401, 403):
        raise CenturionGarageApiClientAuthenticationError("Invalid credentials")
    response.raise_for_status()


class CenturionGarageApiClient:
    """API client for Centurion Garage Door device."""

    def __init__(self, ip_address: str, api_key: str, session: aiohttp.ClientSession):
        """
        Initialize the CenturionGarageApiClient.

        Args:
            ip_address: IP address of the garage door device.
            api_key: API key for authentication.
            session: aiohttp ClientSession for HTTP requests.
        """
        self.ip_address = ip_address
        self.api_key = api_key
        self._session = session

    def _base_url(self) -> str:
        """Return the base URL for API requests."""
        return f"http://{self.ip_address}/api?key={self.api_key}"

    async def async_get_data(self) -> dict:
        """Get device status as a dictionary."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&status=json") as response:
                _verify_response_or_raise(response)
                return await response.json()

    async def get_door_state(self) -> str:
        """Get the current state of the garage door."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&status=json") as response:
                _verify_response_or_raise(response)
                data = await response.json()
                return data.get("door", "unknown").lower()

    async def wifi_dbm(self) -> str:
        """Get the current state of the garage door wifi signal."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&status=json") as response:
                _verify_response_or_raise(response)
                data = await response.json()
                return data.get("wdBm", "unknown").lower()

    async def lamp_status(self) -> str:
        """Get the current state of the garage door lamp status."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&status=json") as response:
                _verify_response_or_raise(response)
                data = await response.json()
                return data.get("lamp", "unknown").lower()

    async def vacation_status(self) -> str:
        """Get the current state of the garage door vacation status."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&status=json") as response:
                _verify_response_or_raise(response)
                data = await response.json()
                return data.get("vacation", "unknown").lower()

    async def open_door(self) -> None:
        """Send command to open the garage door."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&door=open") as response:
                _verify_response_or_raise(response)

    async def close_door(self) -> None:
        """Send command to close the garage door."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&door=close") as response:
                _verify_response_or_raise(response)

    async def stop_door(self) -> None:
        """Send command to stop the garage door."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&door=stop") as response:
                _verify_response_or_raise(response)

    async def lamp_on(self) -> None:
        """Turn the garage lamp on."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&lamp=on") as response:
                _verify_response_or_raise(response)

    async def lamp_off(self) -> None:
        """Turn the garage lamp off."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&lamp=off") as response:
                _verify_response_or_raise(response)

    async def vacation_on(self) -> None:
        """Enable vacation mode."""
        async with async_timeout.timeout(10):
            async with self._session.get(f"{self._base_url()}&vacation=on") as response:
                _verify_response_or_raise(response)

    async def vacation_off(self) -> None:
        """Disable vacation mode."""
        async with async_timeout.timeout(10):
            async with self._session.get(
                f"{self._base_url()}&vacation=off"
            ) as response:
                _verify_response_or_raise(response)

    async def get_camera_image(self) -> bytes | None:
        """Fetch a snapshot image from the camera, if supported."""
        async with async_timeout.timeout(10):
            async with self._session.get(
                f"{self._base_url()}&camera=snapshot"
            ) as response:
                _verify_response_or_raise(response)
                return await response.read()
