import json
import mimetypes
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    from .processing import (
        create_scene_plan,
        scene_plan_as_dict,
        validate_request,
    )
    from .blender_render import BlenderUnavailableError, render_scene
except ImportError:
    from processing import (
        create_scene_plan,
        scene_plan_as_dict,
        validate_request,
    )
    from blender_render import BlenderUnavailableError, render_scene


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIRECTORY = ROOT / "output"


class Simple3DHandler(BaseHTTPRequestHandler):
    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/health":
            self.send_json(200, {"status": "ok"})
            return

        if parsed.path.startswith("/output/"):
            relative = urllib.parse.unquote(parsed.path.removeprefix("/output/"))
            file_path = (OUTPUT_DIRECTORY / relative).resolve()
            if OUTPUT_DIRECTORY.resolve() not in file_path.parents:
                self.send_error(403)
                return
            if not file_path.is_file():
                self.send_error(404)
                return

            content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(file_path.stat().st_size))
            self.end_headers()
            with file_path.open("rb") as file:
                self.wfile.write(file.read())
            return

        relative_path = "index.html" if parsed.path in ("", "/") else parsed.path.lstrip("/")
        file_path = (ROOT / relative_path).resolve()
        if ROOT.resolve() not in file_path.parents and file_path != ROOT.resolve():
            self.send_error(403)
            return
        if not file_path.is_file():
            self.send_error(404)
            return

        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(file_path.stat().st_size))
        self.end_headers()
        with file_path.open("rb") as file:
            self.wfile.write(file.read())

    def do_POST(self) -> None:
        if urllib.parse.urlparse(self.path).path != "/api/generate":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json(400, {"error": "JSON inválido."})
            return

        validation = validate_request(
            payload.get("description", ""),
            payload.get("duration", ""),
            payload.get("format", ""),
        )
        if not validation["ok"]:
            self.send_json(400, {"error": validation["error"]})
            return

        try:
            plan = create_scene_plan(
                payload["description"].strip(),
                int(payload["duration"]),
                payload["format"],
            )
        except ValueError as error:
            self.send_json(422, {"error": str(error)})
            return

        try:
            output = render_scene(plan, OUTPUT_DIRECTORY)
        except BlenderUnavailableError as error:
            self.send_json(503, {"error": str(error), "plan": scene_plan_as_dict(plan)})
            return
        except (RuntimeError, TimeoutError) as error:
            self.send_json(502, {"error": str(error), "plan": scene_plan_as_dict(plan)})
            return

        self.send_json(
            200,
            {
                "status": "completed",
                "plan": scene_plan_as_dict(plan),
                "downloadUrl": "/output/simple3d-preview.mp4",
            },
        )

    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Simple3DHandler)
    print("Simple3D AI running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
