from dataclasses import asdict, dataclass
from typing import Literal


SceneKind = Literal["walking", "talking", "soccer"]


@dataclass(frozen=True)
class ScenePlan:
    kind: SceneKind
    duration: int
    aspect: str
    description: str


SUPPORTED_SCENE_KEYWORDS = {
    "walking": ("caminhando", "walk", "andando"),
    "talking": ("conversando", "conversa", "talking"),
    "soccer": ("futebol", "jogando bola", "soccer"),
}


def validate_request(description: str, duration: str, aspect: str) -> dict:
    description = description.strip()
    if not description:
        return {"ok": False, "error": "Por favor, descreva a animação desejada."}

    try:
        duration_seconds = int(duration)
    except (TypeError, ValueError):
        return {"ok": False, "error": "Duração inválida."}

    if duration_seconds not in (5, 10, 15):
        return {"ok": False, "error": "Duração deve ser 5, 10 ou 15 segundos."}

    if aspect not in ("16:9", "9:16"):
        return {"ok": False, "error": "Proporção deve ser 16:9 ou 9:16."}

    return {"ok": True}


def classify_scene(description: str) -> SceneKind | None:
    normalized = description.lower()
    for kind, keywords in SUPPORTED_SCENE_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return kind  # type: ignore[return-value]
    return None


def create_scene_plan(description: str, duration: int, aspect: str) -> ScenePlan:
    kind = classify_scene(description)
    if kind is None:
        raise ValueError(
            "Cena não suportada pelo gerador local. Use caminhando, conversando ou jogando futebol."
        )
    return ScenePlan(kind=kind, duration=duration, aspect=aspect, description=description)


def scene_plan_as_dict(plan: ScenePlan) -> dict:
    return asdict(plan)
