import streamlit as st
from core.generator import generate_reel_output

st.set_page_config(
    page_title="Jenny Reels Agent",
    layout="centered",
    initial_sidebar_state="collapsed",
)

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


# ---------- CSS ----------
st.markdown("""
<style>
.block-container {
    max-width: 760px;
    padding-top: 2.8rem !important;
    padding-bottom: 2.2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(236, 233, 255, 0.9), transparent 30%),
        linear-gradient(180deg, #f8fafc 0%, #f5f7fb 100%);
}

.hero {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 20px 18px 18px 18px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.main-title {
    font-size: 1.95rem;
    font-weight: 800;
    line-height: 1.12;
    margin: 0 0 0.35rem 0;
    color: #0f172a;
    letter-spacing: -0.02em;
}

.subtitle {
    font-size: 0.96rem;
    color: #64748b;
    margin: 0;
    line-height: 1.45;
}

.card {
    background: rgba(255,255,255,0.96);
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    backdrop-filter: blur(6px);
}

.soft-card {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #edf2f7;
    border-radius: 16px;
    padding: 13px 14px;
    margin-bottom: 10px;
    line-height: 1.45;
    color: #111827;
}

.metric-wrap {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 16px;
}

.metric-card {
    background: rgba(255,255,255,0.96);
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 12px 14px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
}

.metric-label {
    font-size: 0.75rem;
    color: #64748b;
    margin-bottom: 5px;
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
    padding: 7px 11px;
    font-size: 0.9rem;
    font-weight: 600;
}

textarea {
    font-size: 16px !important;
    line-height: 1.55 !important;
    border-radius: 16px !important;
}

.stTextArea textarea {
    background: #fcfdff !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    min-height: 48px !important;
}

.stDownloadButton button,
.stButton button,
.stFormSubmitButton button {
    border-radius: 14px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
    border: 1px solid #dbe4f0 !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
}

.stFormSubmitButton button {
    background: linear-gradient(135deg, #111827 0%, #1f2937 100%) !important;
    color: white !important;
}

label, .stSelectbox label, .stTextArea label {
    font-weight: 650 !important;
    color: #0f172a !important;
}

[data-testid="stAlert"] {
    border-radius: 16px;
}

@media (max-width: 640px) {
    .block-container {
        padding-top: 2.2rem !important;
        padding-left: 0.9rem;
        padding-right: 0.9rem;
    }

    .hero {
        padding: 18px 16px 16px 16px;
        border-radius: 20px;
        margin-bottom: 16px;
    }

    .main-title {
        font-size: 1.7rem;
    }

    .subtitle {
        font-size: 0.92rem;
    }

    .card {
        padding: 14px;
        border-radius: 18px;
    }

    .soft-card {
        padding: 12px;
        border-radius: 14px;
    }

    .metric-wrap {
        gap: 8px;
    }

    .metric-card {
        padding: 10px 12px;
        border-radius: 14px;
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
with st.form("reel_form"):
    script = st.text_area(
        "Guion base",
        height=220,
        placeholder="Pega aquí el guion base...",
    )

    topic = st.selectbox(
        "Tema principal",
        [
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
        ],
    )

    objective = st.selectbox(
        "Objetivo del reel",
        [
            "Educar",
            "Generar identificación",
            "Provocar reflexión",
            "Aumentar guardados",
            "Aumentar compartidos",
        ],
    )

    emotional_tone = st.selectbox(
        "Tono emocional",
        [
            "Suave",
            "Profundo",
            "Directo",
            "Íntimo",
            "Esperanzador",
            "Espiritual",
            "Contenedor",
        ],
    )

    duration = st.selectbox(
        "Duración deseada",
        [
            "1300–1500 caracteres",
            "1000–1300 caracteres",
            "1500–1800 caracteres",
        ],
        index=0,
    )

    hook_intensity = st.selectbox(
        "Intensidad del hook",
        [
            "Baja",
            "Media",
            "Alta",
        ],
        index=1,
    )

    submitted = st.form_submit_button("Generar optimización", use_container_width=True)

# ---------- RESULTS ----------
if submitted:
    if not script.strip():
        st.error("Debes pegar un guion base.")
    else:
        with st.spinner("Optimizando guion..."):
            try:
                result = generate_reel_output(
                    script=script,
                    topic=topic,
                    objective=objective,
                    emotional_tone=emotional_tone,
                    duration=duration,
                    hook_intensity=hook_intensity,
                )

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

                render_list_card("5 títulos sugeridos", result.titulos_sugeridos)
                st.text_area(
                    "Copiar títulos",
                    value="\n".join([f"{i}. {t}" for i, t in enumerate(result.titulos_sugeridos, 1)]),
                    height=150,
                    key="copy_titles_mobile",
                )

                render_list_card("Top 5 hooks mejorados", result.hooks_mejorados)
                st.text_area(
                    "Copiar hooks",
                    value="\n".join([f"{i}. {h}" for i, h in enumerate(result.hooks_mejorados, 1)]),
                    height=150,
                    key="copy_hooks_mobile",
                )

                st.markdown("## 5 hashtags")
                st.markdown('<div class="card">', unsafe_allow_html=True)
                if result.hashtags:
                    chips = "".join([f'<span class="hashtag-chip">{tag}</span>' for tag in result.hashtags])
                    st.markdown(f'<div class="hashtag-chip-wrap">{chips}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="soft-card">No se generaron hashtags.</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.text_area(
                    "Copiar hashtags",
                    value=" ".join(result.hashtags),
                    height=90,
                    key="copy_hashtags_mobile",
                )

                render_list_card("3 frases de cierre", result.frases_cierre)
                st.text_area(
                    "Copiar frases de cierre",
                    value="\n".join([f"{i}. {f}" for i, f in enumerate(result.frases_cierre, 1)]),
                    height=120,
                    key="copy_closings_mobile",
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

                st.text_area(
                    "Copiar diagnóstico",
                    value="Qué funciona:\n"
                    + "\n".join([f"- {x}" for x in result.diagnostico.funciona])
                    + "\n\nQué está frenando el reel:\n"
                    + "\n".join([f"- {x}" for x in result.diagnostico.frena]),
                    height=180,
                    key="copy_diagnosis_mobile",
                )

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")