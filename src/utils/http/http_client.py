import logging
from typing import Any

import httpx
from httpx import HTTPStatusError

from utils.http.http_method import HttpMethod

http_logger = logging.getLogger("http_client")
http_logger.setLevel(logging.DEBUG)

class HttpClient:
    def __init__(self, base_url: str, default_headers: dict=None, timeout: int=10):
        self.base_url = base_url
        self.default_headers = default_headers
        self.timeout = timeout
        self.client = httpx.AsyncClient(headers=self.default_headers, timeout=self.timeout)

    async def request(
            self,
            method: HttpMethod,
            path: str,
            path_params: dict[str, Any] | None = None,
            query_params: dict[str, Any] | None = None,
            body: dict[str, Any] | None = None,
            headers: dict[str, str] | None = None,
            **kwargs
    ) -> dict | list:

        url = f"{self.base_url}{path.format(**path_params)}" if path_params else f"{self.base_url}{path}"

        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        logging.info(f"Request: {method} {url}| Headers: {request_headers} | Params: {query_params} | Body: {body}")

        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=query_params,
                json=body,
                headers=request_headers,
                **kwargs
            )
            response.raise_for_status()
            logging.info(
                f"Response: {response.status_code} {method.upper()} {url} "
                f"| Duration: {response.elapsed.total_seconds()}s"
                f"| Response Body: {response.json()}..."
            )
            return response.json()

        except HTTPStatusError as e:
            logging.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            logging.error(f"Unexpected Error: {repr(e)}")
            raise

    async def close(self):
        await self.client.aclose()