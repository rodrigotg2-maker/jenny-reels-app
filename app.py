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
    }

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


def render_list_card(title, items):
    st.markdown(f"### {title}")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if items:
        for i, item in enumerate(items, 1):
            st.markdown(
                f'<div class="soft-card"><strong>{i}.</strong> {item}</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="soft-card">Sin contenido.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_copy_code(label, content, language="markdown"):
    st.markdown(f"**{label}**")
    st.code(content, language=language)
    st.caption("Usa el ícono de copiar en la esquina superior derecha del bloque.")


def clear_form():
    st.session_state.result = None
    st.session_state.form_data = {
        "script": "",
        "topic": "Ansiedad",
        "objective": "Educar",
        "emotional_tone": "Suave",
        "duration": "1300–1500 caracteres",
        "hook_intensity": "Media",
    }


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

# ---------- CSS MOBILE SAFE ----------
st.markdown("""
<style>
.block-container {
    max-width: 780px;
    padding-top: 1.8rem !important;
    padding-bottom: 2rem;
    padding-left: 0.9rem;
    padding-right: 0.9rem;
}

.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #f3f4f6 100%);
}

/* Header */
.hero {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 20px 18px;
    margin-bottom: 18px;
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

/* Cards */
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
    margin-bottom: 16px;
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

/* Labels */
label, .stSelectbox label, .stTextArea label {
    font-weight: 700 !important;
    color: #111827 !important;
    font-size: 1rem !important;
}

/* TEXTAREA - CRÍTICO */
.stTextArea textarea {
    background: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    opacity: 1 !important;
    font-size: 18px !important;
    line-height: 1.6 !important;
    border-radius: 16px !important;
    border: 1px solid #d1d5db !important;
    padding: 14px !important;
}

.stTextArea textarea::placeholder {
    color: #9ca3af !important;
    -webkit-text-fill-color: #9ca3af !important;
    opacity: 1 !important;
    font-size: 18px !important;
}

/* Selects */
.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #111827 !important;
    border-radius: 14px !important;
    min-height: 50px !important;
    border: 1px solid #d1d5db !important;
}

/* Buttons */
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

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 16px;
}

/* Code blocks */
pre, code {
    font-size: 0.95rem !important;
}

/* Mobile */
@media (max-width: 640px) {
    .block-container {
        padding-top: 1.1rem !important;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
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
        height=220,
        placeholder="Pega aquí el guion base...",
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

    c1, c2 = st.columns(2)
    with c1:
        submitted = st.form_submit_button("Generar optimización", use_container_width=True)
    with c2:
        clear_clicked = st.form_submit_button("Limpiar formulario", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if clear_clicked:
    clear_form()
    st.rerun()

# ---------- RESULTS ----------
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

    export_text = build_export_text(
        result=result,
        topic=topic,
        objective=objective,
        emotional_tone=emotional_tone,
        duration=duration,
        hook_intensity=hook_intensity,
    )

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

    st.markdown("## Guion final optimizado")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.text_area(
        "Listo para copiar y pegar",
        value=result.guion_final_optimizado,
        height=380,
        key="guion_final_mobile",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    render_copy_code("Copiar guion final", result.guion_final_optimizado)

    render_list_card("5 títulos sugeridos", result.titulos_sugeridos)
    render_copy_code(
        "Copiar títulos",
        "\n".join([f"{i}. {t}" for i, t in enumerate(result.titulos_sugeridos, 1)])
    )

    render_list_card("Top 5 hooks mejorados", result.hooks_mejorados)
    render_copy_code(
        "Copiar hooks",
        "\n".join([f"{i}. {h}" for i, h in enumerate(result.hooks_mejorados, 1)])
    )

    st.markdown("## 5 hashtags")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if result.hashtags:
        chips = "".join([f'<span class="hashtag-chip">{tag}</span>' for tag in result.hashtags])
        st.markdown(f'<div class="hashtag-chip-wrap">{chips}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="soft-card">No se generaron hashtags.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    render_copy_code("Copiar hashtags", " ".join(result.hashtags))

    render_list_card("3 frases de cierre", result.frases_cierre)
    render_copy_code(
        "Copiar frases de cierre",
        "\n".join([f"{i}. {f}" for i, f in enumerate(result.frases_cierre, 1)])
    )

    st.markdown("## Diagnóstico")
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

    render_copy_code(
        "Copiar diagnóstico",
        "Qué funciona:\n"
        + "\n".join([f"- {x}" for x in result.diagnostico.funciona])
        + "\n\nQué está frenando el reel:\n"
        + "\n".join([f"- {x}" for x in result.diagnostico.frena])
    )