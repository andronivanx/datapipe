from aiohttp import web
import aiohttp

TARGET_SERVER = "http://localhost:8080"


async def reverse_proxy(request):
    """
    Reverse proxy implementation using aiohttp with added custom headers.
    """
    path = request.match_info.get("path", "")
    target_url = f"{TARGET_SERVER}/{path}"

    # Prepare headers for the target server request
    headers = dict(request.headers)  # Copy original headers
    headers.pop("Host", None)  # Remove 'Host' to avoid conflicts
    headers["X-Custom-Header"] = "abc23456666"  # Add a custom header
    headers["Authorization"] = "abc23456666"  # Add a custom header
    headers["X-Forwarded-For"] = request.remote  # Add the client's IP address

    async with aiohttp.ClientSession() as session:
        async with session.request(
                method=request.method,
                url=target_url,
                params=request.query,
                headers=headers,
                data=await request.read()
        ) as proxied_response:
            # Prepare response headers for the client
            response_headers = {
                key: value
                for key, value in proxied_response.headers.items()
                if key.lower() not in ["content-length", "transfer-encoding", "content-encoding"]
            }

            # Add a custom header to the response if needed
            response_headers["X-Proxy-Custom-Header"] = "ResponseCustomValue"
            response_headers["Authorization"] = "abc23456666"

            body = await proxied_response.read()
            return web.Response(body=body, status=proxied_response.status, headers=response_headers)


# Create aiohttp application
app = web.Application()
app.router.add_route("*", "/{path:.*}", reverse_proxy)

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=9000)