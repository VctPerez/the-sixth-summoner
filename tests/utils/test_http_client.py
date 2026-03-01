import unittest
from datetime import datetime
from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock, MagicMock

from httpcore import TimeoutException
from httpx import Response, HTTPStatusError, Request

from utils.http.http_client import HttpClient
from utils.http.http_method import HttpMethod


class TestHttpClient(IsolatedAsyncioTestCase):
    def setUp(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.default_headers = {"Content-Type": "application/json"}
        self.http_client = HttpClient(base_url=self.base_url, default_headers=self.default_headers)

    async def test_http_client(self):
        # Test GET request
        response = await self.http_client.request(
            method=HttpMethod.GET,
            path="/posts/1"
        )
        self.assertIsInstance(response, dict)
        self.assertEqual(response["id"], 1)

        # Test POST request
        new_post = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        response = await self.http_client.request(
            method=HttpMethod.POST,
            path="/posts",
            body=new_post
        )
        self.assertIsInstance(response, dict)
        self.assertEqual(response["title"], new_post["title"])
        self.assertEqual(response["body"], new_post["body"])
        self.assertEqual(response["userId"], new_post["userId"])

    async def asyncTearDown(self):
        await self.http_client.close()

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_request_path_params_interpolation(self, mock_request):
        # Configuramos un mock exitoso
        mock_request.return_value = Response(200, json={"status": "ok"}, request=Request("GET", "https://test.com"))
        mock_request.return_value._elapsed = MagicMock()

        await self.http_client.request(
            method=HttpMethod.GET,
            path="/riot/account/v1/{name}/{tag}",
            path_params={"name": "vlad", "tag": "euw"}
        )

        # Verificamos que la URL se construyó bien
        expected_url = f"{self.base_url}/riot/account/v1/vlad/euw"
        mock_request.assert_called_once()
        self.assertEqual(mock_request.call_args.kwargs["url"], expected_url)

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_request_http_error_403(self, mock_request):
        mock_request.return_value = Response(403, text="Forbidden", request=Request("GET", "https://test.com"))
        mock_request.return_value._elapsed = MagicMock()

        with self.assertRaises(HTTPStatusError):
            await self.http_client.request(
                method=HttpMethod.GET,
                path="/test"
            )

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    @patch("httpx._models.Response.raise_for_status")
    async def test_headers_merging(self, raise_for_status, mock_request):
        mock_request.return_value = Response(
            status_code=200,
            json={"message": "success"}
        )
        mock_request.return_value._elapsed = MagicMock()

        custom_headers = {"X-Custom": "temp", "X-Default": "true"}
        await self.http_client.request(
            method=HttpMethod.GET,
            path="/test",
            headers=custom_headers
        )


        sent_headers = mock_request.call_args.kwargs["headers"]
        self.assertEqual(sent_headers["X-Default"], "true")
        self.assertEqual(sent_headers["X-Custom"], "temp")

    @patch("httpx.AsyncClient.request", side_effect=TimeoutException("Timeout"))
    async def test_request_timeout(self, mock_request):
        mock_request.return_value._elapsed = MagicMock()

        with self.assertRaises(Exception):
            await self.http_client.request(
                method=HttpMethod.GET,
                path="/test"
            )

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    @patch("httpx._models.Response.raise_for_status")
    async def test_query_params_passing(self, raise_for_status ,mock_request):
        mock_request.return_value = Response(200, json={})
        mock_request.return_value._elapsed = MagicMock()

        params = {"start": 0, "count": 20}

        await self.http_client.request(
            method=HttpMethod.GET,
            path="/test",
            query_params=params
        )

        # Verificamos que los query params llegaron al cliente de httpx
        self.assertEqual(mock_request.call_args.kwargs["params"], params)
