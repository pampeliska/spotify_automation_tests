# --- HELPERS ---

from urllib.parse import urlencode

from constants import *

def spotify_request(api_context, token, method, path, params=None, data=None, json_body=None, form=None, headers=None):
    """Helper function for making Spotify API calls (GET/POST/PUT/DELETE...)."""
    url = f"{BASE_URL}{path}"

    if params:
        query = urlencode({k: v for k, v in params.items() if v is not None})
        if query:
            url = f"{url}?{query}"

    all_headers = {"Authorization": f"Bearer {token}"}
    if headers:
        all_headers.update(headers)

    method_lower = method.lower()
    fn = getattr(api_context, method_lower)

    kwargs = {"headers": all_headers}
    if method_lower in ("post", "put", "patch", "delete"):
        if data is not None:
            kwargs["data"] = data
        if json_body is not None:
            kwargs["json"] = json_body
        if form is not None:
            kwargs["form"] = form

    response = fn(url, **kwargs)

    print(f"\n[{method}] {url}")
    print(f"Status: {response.status}")
    print(f"Body: {response.text()}")

    return response


def spotify_get(api_context, token, path, params=None, headers=None):
    return spotify_request(api_context, token, "GET", path, params=params, headers=headers)


def spotify_post(api_context, token, path, *, data=None, json_body=None, form=None, headers=None):
    return spotify_request(api_context, token, "POST", path, data=data, json_body=json_body, form=form, headers=headers)
