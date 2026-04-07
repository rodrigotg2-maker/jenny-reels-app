import streamlit as st
from core.generator import generate_reel_output

st.set_page_config(
    page_title="Jenny Reels Agent",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- STATE ----------
if "result" not in st.session_state:
    st.session_state.result = None

if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "script": "",
        "topic": "Ansiedad",
        "objective": "Educar",
        "emotional_tone": "Suave",
        "duration": "1300–1500 caracteres",
        "hook_intensity": "Media",
        "view_mode": "Completo",
    }

# ---------- CONSTANTS ----------
TOPICS = [
    "Ansiedad",
    "Autoestima",
    "Duelo",
    "Vínculos",
    "Vacío emocional",
    "Trauma",
    "Autoexigencia",
    "Herida emocional",
    "Apego",
    "Regulación emocional",
    "Identidad",
    "Propósito",
    "Espiritualidad",
    "Crecimiento personal",
    "Psicodélicos terapéuticos",
    "Otro",
]

OBJECTIVES = [
    "Educar",
    "Generar identificación",
    "Provocar reflexión",
    "Aumentar guardados",
    "Aumentar compartidos",
]

TONES = [
    "Suave",
    "Profundo",
    "Directo",
    "Íntimo",
    "Esperanzador",
    "Espiritual",
    "Contenedor",
]

DURATIONS = [
    "1300–1500 caracteres",
    "1000–1300 caracteres",
    "1500–1800 caracteres",
]

HOOK_LEVELS = [
    "Baja",
    "Media",
    "Alta",
]

VIEW_MODES = [
    "Completo",
    "Solo guion",
]

# ---------- HELPERS ----------
def build_export_text(result, topic, objective, emotional_tone, duration, hook_intensity):
    parts = [
        "JENNY REELS AGENT",
        "=================",
        "",
        "CONFIGURACIÓN",
        f"- Tema: {topic}",
        f"- Objetivo: {objective}",
        f"- Tono: {emotional_tone}",
        f"- Duración: {duration}",
        f"- Intensidad hook: {hook_intensity}",
        "",
        "GUIÓN FINAL OPTIMIZADO",
        "----------------------",
        result.guion_final_optimizado,
        "",
        "5 TÍTULOS SUGERIDOS",
        "-------------------",
    ]

    for i, title in enumerate(result.titulos_sugeridos, 1):
        parts.append(f"{i}. {title}")

    parts.extend([
        "",
        "TOP 5 HOOKS MEJORADOS",
        "---------------------",
    ])

    for i, hook in enumerate(result.hooks_mejorados, 1):
        parts.append(f"{i}. {hook}")

    parts.extend([
        "",
        "5 HASHTAGS",
        "----------",
        " ".join(result.hashtags),
        "",
        "3 FRASES DE CIERRE",
        "------------------",
    ])

    for i, frase in enumerate(result.frases_cierre, 1):
        parts.append(f"{i}. {frase}")

    parts.extend([
        "",
        "DIAGNÓSTICO",
        "-----------",
        "Qué funciona:",
    ])

    for item in result.diagnostico.funciona:
        parts.append(f"- {item}")

    parts.append("")
    parts.append("Qué está frenando el reel:")

    for item in result.diagnostico.frena:
        parts.append(f"- {item}")

    return "\n".join(parts)


def clear_form():
    st.session_state.result = None
    st.session_state.form_data = {
        "script": "",
        "topic": "Ansiedad",
        "objective": "Educar",
        "emotional_tone": "Suave",
        "duration": "1300–1500 caracteres",
        "hook_intensity": "Media",
        "view_mode": "Completo",
    }


def render_result_box(label, content, height=220, key="result_box"):
    st.text_area(
        label,
        value=content,
        height=height,
        key=key,
    )
    st.caption("Puedes mantener presionado para seleccionar y copiar.")


def render_cards_list(items):
    if not items:
        st.markdown('<div class="soft-card">Sin contenido.</div>', unsafe_allow_html=True)
        return

    for i, item in enumerate(items, 1):
        st.markdown(
            f'<div class="soft-card"><strong>{i}.</strong> {item}</div>',
            unsafe_allow_html=True
        )


# ---------- CSS ----------
st.markdown("""
<style>
.block-container {
    max-width: 760px;
    padding-top: 1.4rem !important;
    padding-bottom: 2rem;
    padding-left: 0.85rem;
    padding-right: 0.85rem;
}

.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #f3f4f6 100%);
}

.hero {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 20px 18px;
    margin-bottom: 16px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

.main-title {
    font-size: 1.9rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 0.35rem 0;
    color: #0f172a;
    letter-spacing: -0.02em;
}

.subtitle {
    font-size: 1rem;
    color: #64748b;
    line-height: 1.45;
    margin: 0;
}

.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
}

.soft-card {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 12px 14px;
    margin-bottom: 10px;
    line-height: 1.5;
    color: #111827;
}

.metric-wrap {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 12px 14px;
}

.metric-label {
    font-size: 0.75rem;
    color: #64748b;
    margin-bottom: 4px;
}

.metric-value {
    font-size: 0.95rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
}

.hashtag-chip-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 6px;
}

.hashtag-chip {
    background: #eef2ff;
    color: #1e3a8a;
    border: 1px solid #c7d2fe;
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 0.92rem;
    font-weight: 600;
}

label, .stSelectbox label, .stTextArea label {
    font-weight: 700 !important;
    color: #111827 !important;
    font-size: 1rem !important;
}

.stTextArea textarea {
    background: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    opacity: 1 !important;
    font-size: 17px !important;
    line-height: 1.6 !important;
    border-radius: 16px !important;
    border: 1px solid #d1d5db !important;
    padding: 14px !important;
}

.stTextArea textarea::placeholder {
    color: #9ca3af !important;
    -webkit-text-fill-color: #9ca3af !important;
    opacity: 1 !important;
    font-size: 17px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #111827 !important;
    border-radius: 14px !important;
    min-height: 50px !important;
    border: 1px solid #d1d5db !important;
}

.stDownloadButton button,
.stButton button,
.stFormSubmitButton button {
    border-radius: 14px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: 1px solid #d1d5db !important;
    box-shadow: none !important;
}

.stFormSubmitButton button[kind="primary"] {
    background: #111827 !important;
    color: white !important;
}

[data-testid="stAlert"] {
    border-radius: 16px;
}

div[data-testid="stExpander"] {
    border: 1px solid #e5e7eb !important;
    border-radius: 16px !important;
    background: #ffffff !important;
    margin-bottom: 12px !important;
}

@media (max-width: 640px) {
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }

    .hero {
        padding: 18px 16px;
        border-radius: 20px;
    }

    .main-title {
        font-size: 1.65rem;
    }

    .subtitle {
        font-size: 0.95rem;
    }

    .card {
        padding: 14px;
        border-radius: 18px;
    }

    .soft-card {
        padding: 12px;
    }

    .metric-card {
        padding: 10px 12px;
    }

    .stTextArea textarea {
        font-size: 18px !important;
        line-height: 1.65 !important;
    }

    .stTextArea textarea::placeholder {
        font-size: 18px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <div class="main-title">Jenny Reels Agent</div>
    <div class="subtitle">
        Optimiza guiones para Reels con foco en hook, claridad, ritmo y conexión emocional.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- FORM ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

with st.form("reel_form"):
    script = st.text_area(
        "Guion base",
        height=210,
        placeholder="Pega aquí el guion que quieres optimizar...",
        value=st.session_state.form_data["script"],
    )

    topic = st.selectbox(
        "Tema principal",
        TOPICS,
        index=TOPICS.index(st.session_state.form_data["topic"]),
    )

    objective = st.selectbox(
        "Objetivo del reel",
        OBJECTIVES,
        index=OBJECTIVES.index(st.session_state.form_data["objective"]),
    )

    emotional_tone = st.selectbox(
        "Tono emocional",
        TONES,
        index=TONES.index(st.session_state.form_data["emotional_tone"]),
    )

    duration = st.selectbox(
        "Duración deseada",
        DURATIONS,
        index=DURATIONS.index(st.session_state.form_data["duration"]),
    )

    hook_intensity = st.selectbox(
        "Intensidad del hook",
        HOOK_LEVELS,
        index=HOOK_LEVELS.index(st.session_state.form_data["hook_intensity"]),
    )

    view_mode = st.selectbox(
        "Modo de visualización",
        VIEW_MODES,
        index=VIEW_MODES.index(st.session_state.form_data["view_mode"]),
    )

    c1, c2 = st.columns(2)
    with c1:
        submitted = st.form_submit_button("Generar optimización", use_container_width=True)
    with c2:
        clear_clicked = st.form_submit_button("Limpiar formulario", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if clear_clicked:
    clear_form()
    st.rerun()

# ---------- GENERATE ----------
if submitted:
    if not script.strip():
        st.warning("Pega un guion para continuar.")
        st.stop()

    st.session_state.form_data = {
        "script": script,
        "topic": topic,
        "objective": objective,
        "emotional_tone": emotional_tone,
        "duration": duration,
        "hook_intensity": hook_intensity,
        "view_mode": view_mode,
    }

    with st.spinner("Optimizando guion... esto puede tardar unos segundos."):
        try:
            result = generate_reel_output(
                script=script,
                topic=topic,
                objective=objective,
                emotional_tone=emotional_tone,
                duration=duration,
                hook_intensity=hook_intensity,
            )
            st.session_state.result = result
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
            st.stop()

# ---------- RENDER RESULT ----------
if st.session_state.result is not None:
    result = st.session_state.result
    topic = st.session_state.form_data["topic"]
    objective = st.session_state.form_data["objective"]
    emotional_tone = st.session_state.form_data["emotional_tone"]
    duration = st.session_state.form_data["duration"]
    hook_intensity = st.session_state.form_data["hook_intensity"]
    view_mode = st.session_state.form_data["view_mode"]

    export_text = build_export_text(
        result=result,
        topic=topic,
        objective=objective,
        emotional_tone=emotional_tone,
        duration=duration,
        hook_intensity=hook_intensity,
    )

    # SIEMPRE PRIMERO EL GUIÓN
    st.markdown("## Guion final optimizado")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    render_result_box(
        "Listo para copiar y pegar",
        result.guion_final_optimizado,
        height=340,
        key="guion_final_box",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if view_mode == "Solo guion":
        st.download_button(
            label="Descargar resultado (.txt)",
            data=export_text,
            file_name="jenny_reels_resultado.txt",
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.markdown("## Resumen")
        st.markdown(
            f"""
            <div class="metric-wrap">
                <div class="metric-card">
                    <div class="metric-label">Tema</div>
                    <div class="metric-value">{topic}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Objetivo</div>
                    <div class="metric-value">{objective}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Tono</div>
                    <div class="metric-value">{emotional_tone}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Duración</div>
                    <div class="metric-value">{duration}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Hook</div>
                    <div class="metric-value">{hook_intensity}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Caracteres</div>
                    <div class="metric-value">{len(result.guion_final_optimizado)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            label="Descargar resultado (.txt)",
            data=export_text,
            file_name="jenny_reels_resultado.txt",
            mime="text/plain",
            use_container_width=True,
        )

        with st.expander("5 títulos sugeridos", expanded=False):
            render_cards_list(result.titulos_sugeridos)
            render_result_box(
                "Títulos listos para copiar",
                "\n".join([f"{i}. {t}" for i, t in enumerate(result.titulos_sugeridos, 1)]),
                height=180,
                key="titulos_box",
            )

        with st.expander("Top 5 hooks mejorados", expanded=False):
            render_cards_list(result.hooks_mejorados)
            render_result_box(
                "Hooks listos para copiar",
                "\n".join([f"{i}. {h}" for i, h in enumerate(result.hooks_mejorados, 1)]),
                height=200,
                key="hooks_box",
            )

        with st.expander("5 hashtags", expanded=False):
            st.markdown('<div class="hashtag-chip-wrap">', unsafe_allow_html=True)
            for tag in result.hashtags:
                st.markdown(
                    f'<span class="hashtag-chip">{tag}</span>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
            render_result_box(
                "Hashtags listos para copiar",
                " ".join(result.hashtags),
                height=100,
                key="hashtags_box",
            )

        with st.expander("3 frases de cierre", expanded=False):
            render_cards_list(result.frases_cierre)
            render_result_box(
                "Frases de cierre listas para copiar",
                "\n".join([f"{i}. {f}" for i, f in enumerate(result.frases_cierre, 1)]),
                height=150,
                key="cierres_box",
            )

        with st.expander("Diagnóstico", expanded=False):
            st.markdown("**Qué funciona**")
            if result.diagnostico.funciona:
                for item in result.diagnostico.funciona:
                    st.markdown(f"- {item}")
            else:
                st.markdown("- Sin observaciones.")

            st.markdown("")
            st.markdown("**Qué está frenando el reel**")
            if result.diagnostico.frena:
                for item in result.diagnostico.frena:
                    st.markdown(f"- {item}")
            else:
                st.markdown("- Sin observaciones.")

            render_result_box(
                "Diagnóstico listo para copiar",
                "Qué funciona:\n"
                + "\n".join([f"- {x}" for x in result.diagnostico.funciona])
                + "\n\nQué está frenando el reel:\n"
                + "\n".join([f"- {x}" for x in result.diagnostico.frena]),
                height=220,
                key="diagnostico_box",
            )