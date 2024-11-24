from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Base URL of the target server for reverse proxy
TARGET_SERVER = "http://localhost:8080/dagster"

@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def reverse_proxy(path):
    """
    Reverse proxy that forwards requests to the target server.
    """
    target_url = f"{TARGET_SERVER}/{path}"
    print(target_url)
    # Extract query parameters
    query_params = request.args.to_dict()

    # Extract headers from the client request
    headers = {key: value for key, value in request.headers if key.lower() != "host"}
    headers["Authorization"] = "abc23456666"
    # Handle cookies
    cookies = request.cookies

    try:
        # Forward the request based on the HTTP method
        if request.method == "GET":
            proxied_response = requests.get(target_url, headers=headers, params=query_params, cookies=cookies)
        elif request.method == "POST":
            proxied_response = requests.post(target_url, headers=headers, data=request.data, params=query_params, cookies=cookies)
        elif request.method == "PUT":
            proxied_response = requests.put(target_url, headers=headers, data=request.data, params=query_params, cookies=cookies)
        elif request.method == "DELETE":
            proxied_response = requests.delete(target_url, headers=headers, params=query_params, cookies=cookies)
        elif request.method == "PATCH":
            proxied_response = requests.patch(target_url, headers=headers, data=request.data, params=query_params, cookies=cookies)
        elif request.method == "OPTIONS":
            proxied_response = requests.options(target_url, headers=headers, params=query_params, cookies=cookies)
        else:
            return Response("Method Not Allowed", status=405)

        # Create a response object to return to the client
        response = Response(proxied_response.content, status=proxied_response.status_code)
        response.headers.update({key: value for key, value in proxied_response.headers.items() if key.lower() != "content-encoding"})  # Remove content-encoding if necessary
        return response
    except requests.exceptions.RequestException as e:
        return Response(f"Proxy Error: {str(e)}", status=500)

@app.route('/ping/')
def ping():
    return "Working"
@app.route('/')
def home():
    return "Home Working"
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=9000)