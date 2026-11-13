"""S2-only routes installed exclusively in the private S1 host when enabled."""
import asyncio
import json
import re

from fastapi import Request
from fastapi.responses import JSONResponse

from backend.app.local_product_web import AuthError, LOGIN, PREFIX
from backend.app.services.product_web_bridge import BODY_LIMIT, REVIEW_LIMIT, BridgeError, admit, require

SELECTOR = r"[0-9a-f]{32}"
BASE = PREFIX + "/documents"


class PublicationFence:
    """Recheck live authority at actual ASGI publication, after S1 middleware.

    Already-transmitted bytes cannot be recalled. No custody lock is taken.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not scope.get("path", "").startswith(BASE):
            return await self.app(scope, receive, send)
        start, parts, size = None, [], 0
        async def buffered(message):
            nonlocal start, size
            if message["type"] == "http.response.start":
                start = message
                return
            if message["type"] != "http.response.body":
                return
            size += len(message.get("body", b""))
            require(size <= REVIEW_LIMIT, 503, "response_limit")
            parts.append(message.get("body", b""))
            if not message.get("more_body", False):
                fence = scope.get("state", {}).get("s2_fence")
                try:
                    if fence:
                        fence()
                except (BridgeError, AuthError):
                    response = JSONResponse({"error": {"code": "authority_revoked"}}, status_code=401,
                                            headers={"Cache-Control": "no-store"})
                    await response(scope, receive, send)
                    return
                await send(start)
                # Check immediately before body publication as well.
                if fence:
                    fence()
                await send({"type": "http.response.body", "body": b"".join(parts)})
        await self.app(scope, receive, buffered)


async def body(request):
    headers = request.state.s1_headers
    length = headers.get("content-length", "")
    require(re.fullmatch(r"0|[1-9][0-9]{0,3}", length) is not None, 400, "invalid_framing")
    require("transfer-encoding" not in headers and "content-encoding" not in headers, 400, "invalid_framing")
    require(int(length) <= BODY_LIMIT, 413, "body_limit")
    data = bytearray()
    async with asyncio.timeout(5):
        async for part in request.stream():
            require(len(data) + len(part) <= BODY_LIMIT, 413, "body_limit")
            data.extend(part)
    require(len(data) == int(length), 400, "invalid_framing")
    return bytes(data)


def install_routes(app, sessions, bridge):
    app.add_middleware(PublicationFence)
    @app.api_route(BASE, methods=["POST"])
    @app.api_route(BASE + "/{selector}", methods=["DELETE"])
    @app.api_route(BASE + "/{selector}/{action}", methods=["GET", "POST"])
    @app.get(BASE + "/{selector}/revisions/{revision}/artifacts/{filename}")
    async def document(request: Request, selector: str = "", action: str = "", revision: str = "", filename: str = ""):
        try:
            require(request.scope.get("raw_path") == request.url.path.encode(), 404)
            headers = request.state.s1_headers
            token = request.state.s1_cookies.get(LOGIN)
            sessions.authority(token, headers.get("x-aiip-csrf"), mutation=request.method != "GET")
            if selector:
                require(re.fullmatch(SELECTOR, selector), 404)
            if request.method == "GET":
                require(headers.get("content-length", "0") == "0"
                        and "transfer-encoding" not in headers and "content-encoding" not in headers, 400)
            if filename:
                require(request.method == "GET" and re.fullmatch(r"[1-9][0-9]{0,8}", revision), 404)
                data = {"revision": int(revision), "filename": filename}
                action = "download"
            elif request.method == "GET":
                require(action == "review", 404)
                data = {}
            else:
                raw = await body(request)
                if not selector:
                    require(request.method == "POST", 404)
                    source = (headers.get("x-aiip-filename"), headers.get("content-type"), raw)
                    admit(*source)
                    result, fence = await bridge.execute(token, "", "intake", {}, source=source)
                    request.state.s2_fence = fence
                    return result
                def unique(pairs):
                    result = {}
                    for key, value in pairs:
                        require(key not in result, 400)
                        result[key] = value
                    return result
                data = json.loads(raw, object_pairs_hook=unique)
                require(type(data) is dict, 400)
                if request.method == "DELETE":
                    require(data == {}, 400)
                    bridge.cancel(token, selector)
                    return JSONResponse({"state": "cancelled"})
                require(action in {"ack-content", "ack-claims", "render"}, 404)
            result, fence = await bridge.execute(token, selector, action, data)
            request.state.s2_fence = fence
            return result
        except (BridgeError, AuthError) as exc:
            return JSONResponse({"error": {"code": exc.code}}, status_code=exc.status)
        except (ValueError, UnicodeError, TimeoutError):
            return JSONResponse({"error": {"code": "request_rejected"}}, status_code=400)
