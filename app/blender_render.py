import shutil
import subprocess
import tempfile
from pathlib import Path

try:
    from .processing import ScenePlan
except ImportError:
    from processing import ScenePlan


class BlenderUnavailableError(RuntimeError):
    pass


def find_blender() -> str | None:
    return shutil.which("blender")


def render_scene(plan: ScenePlan, output_directory: Path) -> Path:
    blender = find_blender()
    if not blender:
        raise BlenderUnavailableError(
            "Blender não encontrado. Instale o Blender, adicione-o ao PATH e tente novamente."
        )

    output_directory.mkdir(parents=True, exist_ok=True)
    output = output_directory / "simple3d-preview.mp4"
    script = Path(__file__).resolve().parent.parent / "blender" / "render_scene.py"

    if not script.exists():
        raise RuntimeError("Script de renderização do Blender não encontrado.")

    width, height = (1280, 720) if plan.aspect == "16:9" else (720, 1280)
    command = [
        blender,
        "--background",
        "--factory-startup",
        "--python",
        str(script),
        "--",
        plan.kind,
        str(plan.duration),
        str(width),
        str(height),
        str(output),
    ]

    with tempfile.TemporaryDirectory(prefix="simple3d-") as temp_directory:
        environment = subprocess.os.environ.copy()
        environment["TEMP"] = temp_directory
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
            env=environment,
        )

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "Falha desconhecida"
        raise RuntimeError(f"Renderização do Blender falhou: {detail[-1200:]}")

    if not output.exists():
        raise RuntimeError("O Blender terminou sem gerar o arquivo MP4.")

    return output
