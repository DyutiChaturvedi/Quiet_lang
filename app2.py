# ============================================================
# THE QUIET LANGUAGES OF RESEARCH
# University of Warwick AI Commons Competition
# Powered by Groq (free API)
# ============================================================

import streamlit as st
from groq import Groq
import json

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ------------------------------------------------------------
# PAGE SETTINGS
# ------------------------------------------------------------

st.set_page_config(
    page_title="The Quiet Languages of Research",
    layout="wide"
)

# ------------------------------------------------------------
# CUSTOM CSS — iOS / Apple style
# ------------------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global */
html, body, .stApp {
    background-color: #F2F2F7;
    font-family: -apple-system, 'SF Pro Display', 'Inter', BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    color: #1C1C1E;
}

/* Headings */
h1 {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
    color: #1C1C1E;
}

h2 {
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    color: #1C1C1E;
    letter-spacing: -0.3px;
}

h3 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #1C1C1E;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E5EA;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    font-size: 0.9rem;
    color: #3A3A3C;
    line-height: 1.6;
}

/* Buttons — iOS filled style */
.stButton > button {
    width: 100%;
    background: #1C1C1E;
    color: #FFFFFF;
    border: none;
    border-radius: 14px;
    padding: 14px 20px;
    font-size: 16px;
    font-weight: 600;
    font-family: -apple-system, 'SF Pro Display', 'Inter', sans-serif;
    letter-spacing: -0.2px;
    transition: background 0.2s ease, transform 0.1s ease;
}

.stButton > button:hover {
    background: #3A3A3C;
    color: #FFFFFF;
    transform: scale(0.99);
}

.stButton > button:active {
    transform: scale(0.97);
}

/* Text area */
textarea {
    border-radius: 12px !important;
    font-family: -apple-system, 'SF Pro Display', 'Inter', sans-serif !important;
    font-size: 15px !important;
    border: 1px solid #D1D1D6 !important;
    background: #FFFFFF !important;
    padding: 12px !important;
    color: #1C1C1E !important;
}

textarea:focus {
    border-color: #1C1C1E !important;
    box-shadow: 0 0 0 2px rgba(28,28,30,0.12) !important;
}

/* Cards — iOS grouped list style */
.ios-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
}

.ios-card-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #8E8E93;
    margin-bottom: 6px;
}

.ios-card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1C1C1E;
    letter-spacing: -0.3px;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid #F2F2F7;
}

.ios-section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #8E8E93;
    margin-top: 16px;
    margin-bottom: 5px;
}

.ios-section-content {
    font-size: 0.95rem;
    line-height: 1.65;
    color: #1C1C1E;
}

/* Reflection box — iOS dark card */
.reflection-box {
    background: #1C1C1E;
    border-radius: 16px;
    padding: 24px 22px;
    color: #FFFFFF;
    margin-top: 8px;
}

.reflection-box p {
    font-size: 0.95rem;
    line-height: 1.7;
    color: #EBEBF5;
    margin-bottom: 12px;
}

.reflection-box strong {
    color: #FFFFFF;
}

/* Footer */
.footer {
    text-align: center;
    padding: 28px 0 12px 0;
    color: #8E8E93;
    font-size: 0.8rem;
    border-top: 1px solid #E5E5EA;
    margin-top: 48px;
    letter-spacing: 0.1px;
}

/* Selectbox */
[data-testid="stSelectbox"] label {
    font-size: 0.85rem;
    font-weight: 500;
    color: #8E8E93;
}

/* Divider */
hr {
    border-color: #E5E5EA;
}

/* Caption text */
.stCaption {
    color: #8E8E93 !important;
    font-size: 0.8rem !important;
}

/* Info box */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
    background: #F2F2F7 !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:
    st.title("About")
    st.write("""
Research is often viewed through the work of academics alone.

This project explores whether AI can help translate one research idea across the different professional languages spoken throughout the research ecosystem.

Rather than replacing expertise, this prototype encourages reflection on the people whose work often remains invisible.
""")

    st.markdown("---")
    st.subheader("The Research Ecosystem")
    for title in [
        "The Researcher's Language",
        "The Research Support Language",
        "The Finance Language",
        "The Contracts Language",
        "The Ethics Language",
        "The Public Language",
    ]:
        st.write(f"— {title}")

    st.markdown("---")
    st.info("""
**How to use**

1. Enter a research idea.
2. Click Translate.
3. Choose a professional perspective.
4. Reflect on what AI reveals — and what it may overlook.
""")
    st.markdown("---")
    st.caption("AI Commons Competition — University of Warwick")

# ------------------------------------------------------------
# PERSPECTIVE CONFIG
# ------------------------------------------------------------

PERSPECTIVES = {
    "Researcher": {
        "title": "The Researcher's Language",
        "color": "#1C1C1E",
        "prompt_role": "an academic researcher at a research-intensive university",
        "what_matters": "novelty, methodology, and impact on the field",
        
    },
    "Research Support": {
        "title": "The Research Support Language",
        "color": "#2C2C2E",
        "prompt_role": "a research support officer or research development officer responsible for submission of the grant application and processing the awarded grant",
        "what_matters": "timelines, funder requirements, stakeholder coordination, and eligible costs",
    },
    "Finance": {
        "title": "The Finance Language",
        "color": "#2C2C2E",
        "prompt_role": "a university research finance officer responsible for invoicing of the budgets to the collaborators and the researcher if the grant is awarded",
        "what_matters": "eligible costs, budget forecasting/ optimisation, audit compliance, and value for money",
    },
    "Contracts": {
        "title": "The Contracts Language",
        "color": "#2C2C2E",
        "prompt_role": "a university contracts and legal officer handling research agreements",
        "what_matters": "IP ownership, data rights, liability clauses, funder terms, and institutional risk",
    },
    "Ethics": {
        "title": "The Ethics Language",
        "color": "#2C2C2E",
        "prompt_role": "a university research ethics officer",
        "what_matters": "participant welfare, informed consent, data privacy, risk, and the responsible conduct of research",
    },
   }

# ------------------------------------------------------------
# AI GENERATION
# ------------------------------------------------------------

def call_groq(prompt: str) -> str:
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()


def parse_json(raw: str) -> dict:
    import re
    if "```" in raw:
        parts = raw.split("```")
        raw = parts[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        raw = raw[start:end]

    def fix_bullet_field(text):
        pattern = r'("first_questions"\s*:\s*)([\s\S]*?)(\n\s*"[a-z])'
        def replacer(m):
            key = m.group(1)
            bullets = m.group(2).strip()
            next_key = m.group(3)
            bullets_clean = bullets.replace('"', "'").replace('\n', ' ').strip().rstrip(',').strip()
            return f'{key}"{bullets_clean}",{next_key}'
        return re.sub(pattern, replacer, text)

    raw = fix_bullet_field(raw)

    try:
        return json.loads(raw)
    except Exception:
        result = {}
        for field in ["priorities", "first_questions", "ai_interpretation", "hidden_contribution"]:
            pattern = rf'"{field}"\s*:\s*"([\s\S]*?)"(?:\s*,|\s*}})'
            match = re.search(pattern, raw)
            if match:
                result[field] = match.group(1)
            else:
                pattern2 = rf'"{field}"\s*:\s*([\s\S]*?)(?=\n\s*"[a-z]|\n\s*}})'
                match2 = re.search(pattern2, raw)
                if match2:
                    result[field] = match2.group(1).strip().rstrip(',')
        return result


def generate_perspective(idea: str, perspective_key: str) -> dict:
    cfg = PERSPECTIVES[perspective_key]
    prompt = f"""You are helping a user understand how different professional groups within a university research ecosystem interpret the same research idea.

Translate this research idea through the professional lens of {cfg["prompt_role"]}.
For this role, what matters most is: {cfg["what_matters"]}.

Research idea: {idea}

Respond ONLY in this exact JSON format (no markdown, no preamble, no explanation):
{{
  "priorities": "2-3 sentences describing what this professional immediately focuses on when they hear this research idea",
  "first_questions": "3-4 bullet points (each starting with a bullet •) listing the first questions they would ask",
  "ai_interpretation": "2-3 sentences describing how AI might interpret or assist this professional with this idea, and where AI might misread or oversimplify their concerns",
  "hidden_contribution": "1-2 sentences naming a specific contribution this role makes that is rarely credited or visible in research outputs"
}}"""
    raw = call_groq(prompt)
    return parse_json(raw)


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

st.title("The Quiet Languages of Research")
st.subheader("Can AI translate the hidden workforce behind research?")
st.markdown("""
Research succeeds because many different professional groups contribute their expertise.
Although everyone is working towards the same goal, they often communicate through different priorities, responsibilities, and professional languages.

This interactive prototype explores whether AI can help translate these perspectives — while encouraging reflection on what may be gained, and lost, in the process.
""")

st.divider()

# ------------------------------------------------------------
# INPUT
# ------------------------------------------------------------

idea = st.text_area(
    "Enter a Research Idea",
    placeholder="Example: Developing sustainable battery technology for electric vehicles",
    height=100
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    translate_clicked = st.button("Translate")

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

for key, default in [
    ("translated", False),
    ("current_idea", ""),
    ("perspective_cache", {}),
]:
    if key not in st.session_state:
        st.session_state[key] = default

if translate_clicked:
    if not idea.strip():
        st.warning("Please enter a research idea first.")
    else:
        if idea.strip() != st.session_state.current_idea:
            st.session_state.perspective_cache = {}
        st.session_state.current_idea = idea.strip()
        st.session_state.translated = True

# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------

if st.session_state.translated and st.session_state.current_idea:

    st.divider()
    st.markdown("Whose language would you like AI to translate?")
    st.caption("Each perspective shows how a different professional group interprets the same research idea.")

    perspective = st.selectbox(
        "Select a professional perspective",
        list(PERSPECTIVES.keys()),
        label_visibility="collapsed"
    )

    cfg = PERSPECTIVES[perspective]

    if perspective not in st.session_state.perspective_cache:
        with st.spinner(f"Translating into {cfg['title']}..."):
            try:
                result = generate_perspective(st.session_state.current_idea, perspective)
                st.session_state.perspective_cache[perspective] = result
            except Exception as e:
                st.error(f"Translation failed: {e}")
                result = None
    else:
        result = st.session_state.perspective_cache[perspective]

    if result:
        # Format bullets
        raw_bullets = result.get("first_questions", "")
        if isinstance(raw_bullets, list):
            bullet_text = "\n".join(f"• {str(b).strip()}" for b in raw_bullets)
        else:
            bullet_text = "\n".join(
                f"• {b.strip()}"
                for b in str(raw_bullets).replace("[","").replace("]","").split("•")
                if b.strip()
            )

        with st.container():
            st.markdown(f"### {cfg['title']}")
            st.caption("Professional Perspective")
            st.divider()

            st.markdown("**What matters most to them**")
            st.write(result.get("priorities", ""))

            st.markdown("**Questions they ask first**")
            st.write(bullet_text)

            st.markdown("**How AI interprets this role**")
            st.write(result.get("ai_interpretation", ""))

            st.markdown("**Hidden contribution**")
            st.write(result.get("hidden_contribution", ""))

    # ---- Critical Reflection ----
    st.markdown("---")
    st.markdown("""
<div class="reflection-box">
<p style="font-size:0.75rem; font-weight:600; letter-spacing:0.8px; text-transform:uppercase; color:#8E8E93; margin-bottom:10px;">A Note on What AI May Overlook</p>
<p>
AI helps in translating different languages of the research workforce but professional expertise cannot be replaced.
The concerns, instincts, and institutional knowledge of a finance officer,
a contracts professional, or an ethics reviewer are built from years of experience
that cannot be captured in a text prompt.
</p>
<p>
This app demonstrates both the promise and the limits of AI as a mediator.
It can simplify the vocabulary of different roles. It cannot replicate
the judgement behind them or the relationships, trust, and unwritten rules
that make research ecosystems function.
</p>
<p style="margin-bottom:0;">
<strong>The Quiet Languages of Research are the intricate nuances which go unnoticed sometimes.</strong>
</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown("""
<div class="footer">
    <strong>The Quiet Languages of Research</strong><br>
    Submitted by Dyuti Chaturvedi &nbsp;·&nbsp; AI Commons Competition, University of Warwick · 2026<br>
    <span style="color:#C7C7CC;">Powered by Groq · AI use disclosed: all perspective translations are AI-generated in response to user input.</span>
</div>
""", unsafe_allow_html=True)