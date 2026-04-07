import json
import re

from core.llm_client import get_client, get_model_name
from core.prompts import SYSTEM_PROMPT, build_user_prompt
from core.schemas import ReelOutput


def extract_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0).strip()
    return text.strip()


def normalize_output(parsed: dict) -> dict:
    if "diagnostico" not in parsed or not isinstance(parsed.get("diagnostico"), dict):
        parsed["diagnostico"] = {}

    parsed["diagnostico"].setdefault("funciona", [])
    parsed["diagnostico"].setdefault("frena", [])

    parsed.setdefault("guion_final_optimizado", "")
    parsed.setdefault("titulos_sugeridos", [])
    parsed.setdefault("hooks_mejorados", [])
    parsed.setdefault("hashtags", [])
    parsed.setdefault("frases_cierre", [])

    parsed["titulos_sugeridos"] = parsed["titulos_sugeridos"][:5]
    parsed["hooks_mejorados"] = parsed["hooks_mejorados"][:5]
    parsed["hashtags"] = parsed["hashtags"][:5]
    parsed["frases_cierre"] = parsed["frases_cierre"][:3]

    return parsed


def force_valid_json(raw_text: str) -> dict:
    client = get_client()
    model = get_model_name()

    repair_prompt = f"""
Convierte el siguiente contenido en JSON válido.

Devuelve solo JSON válido.
No agregues explicación.
No resumas.
No cambies el sentido del contenido.
Corrige comillas, saltos de línea, comas o escapes si es necesario.

La estructura final debe ser:
{{
  "diagnostico": {{
    "funciona": [],
    "frena": []
  }},
  "guion_final_optimizado": "",
  "titulos_sugeridos": [],
  "hooks_mejorados": [],
  "hashtags": [],
  "frases_cierre": []
}}

Contenido a reparar:
{raw_text}
"""

    response = client.responses.create(
        model=model,
        input=repair_prompt,
    )

    repaired_text = response.output_text.strip()
    repaired_json = extract_json(repaired_text)
    return json.loads(repaired_json)


def generate_reel_output(
    script: str,
    topic: str,
    objective: str,
    emotional_tone: str,
    duration: str,
    hook_intensity: str,
) -> ReelOutput:
    client = get_client()
    model = get_model_name()

    user_prompt = build_user_prompt(
        script=script,
        topic=topic,
        objective=objective,
        emotional_tone=emotional_tone,
        duration=duration,
        hook_intensity=hook_intensity,
    )

    raw_text = ""

    try:
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        raw_text = response.output_text.strip()
        clean_json = extract_json(raw_text)

        try:
            parsed = json.loads(clean_json)
        except json.JSONDecodeError:
            parsed = force_valid_json(clean_json)

        parsed = normalize_output(parsed)

        return ReelOutput.model_validate(parsed)

    except Exception as e:
        raise Exception(f"Error en generación: {e}\n\nRespuesta original:\n{raw_text}")