# ============================================================
# THE QUIET LANGUAGES OF RESEARCH
# University of Warwick AI Commons Competition
# Powered by Google Gemini (free API)
# ============================================================

import streamlit as st
from groq import Groq
import json
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ------------------------------------------------------------
# PAGE SETTINGS
# -----------------------------------------------------------

st.set_page_config(
    page_title="The Quiet Languages of Research",
    page_icon="🔍",
    layout="wide"
)

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

.stApp {
    background-color: #F7F5F9;
    font-family: 'Inter', sans-serif;
}

h1 {
    color: #4B1E78;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 2.4rem !important;
    letter-spacing: -0.5px;
}

h2, h3 {
    color: #4B1E78;
    font-family: 'Playfair Display', serif;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E8E0F0;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4B1E78, #7B3FA8);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-size: 17px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #69439E, #9B5FC8);
    color: white;
    box-shadow: 0 4px 15px rgba(75, 30, 120, 0.3);
}

textarea {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    border: 1.5px solid #D0C0E8 !important;
}

.perspective-card {
    background: white;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(75, 30, 120, 0.08);
    border-left: 5px solid;
    font-family: 'Inter', sans-serif;
}

.card-role-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    opacity: 0.65;
    margin-bottom: 4px;
}

.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 18px;
}

.card-section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    opacity: 0.5;
    margin-top: 18px;
    margin-bottom: 6px;
}

.card-content {
    font-size: 1rem;
    line-height: 1.7;
    color: #1A1A2E;
}

.audit-card {
    background: white;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(75, 30, 120, 0.08);
    font-family: 'Inter', sans-serif;
}

.audit-card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
}

.reflection-box {
    background: linear-gradient(135deg, #4B1E78 0%, #7B3FA8 100%);
    border-radius: 16px;
    padding: 32px;
    color: white;
    font-family: 'Inter', sans-serif;
    margin-top: 10px;
}

.reflection-box h3 {
    color: white !important;
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
}

.footer {
    text-align: center;
    padding: 32px 0 16px 0;
    color: #888;
    font-size: 0.85rem;
    font-family: 'Inter', sans-serif;
    border-top: 1px solid #E0D8ED;
    margin-top: 48px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# GEMINI SETUP — key entered once via sidebar
# ------------------------------------------------------------

with st.sidebar:
    st.title("🔍 About")
    st.write("""
Research is often viewed through the work of academics alone.

This project explores whether AI can help translate one research idea across the different professional languages spoken throughout the research ecosystem.

Rather than replacing expertise, this prototype encourages reflection on the people whose work often remains invisible.
""")

    st.markdown("---")

    st.subheader("The Research Ecosystem")
    for emoji, title in [
        ("👩‍🔬", "The Researcher's Language"),
        ("📋", "The Research Support Language"),
        ("💰", "The Finance Language"),
        ("📄", "The Contracts Language"),
        ("⚖️", "The Ethics Language"),
        ("🌍", "The Public Language"),
    ]:
        st.write(f"{emoji} {title}")

    st.markdown("---")
    st.info("""
💡 **How to use**

1. Enter a research idea.
2. Click **Translate**.
3. Choose a professional perspective.
4. Try the **Translation Audit** for a full comparison.
""")
    st.markdown("---")
    st.caption("Submitted to the [AI Commons Competition](https://warwick.ac.uk/research/research-culture-at-warwick/aicommons/competition/) — University of Warwick")

# ------------------------------------------------------------
# PERSPECTIVE CONFIG
# ------------------------------------------------------------

PERSPECTIVES = {
    "👩‍🔬 Researcher": {
        "emoji": "👩‍🔬",
        "title": "The Researcher's Language",
        "color": "#4B1E78",
        "prompt_role": "an academic researcher at a research-intensive university",
        "what_matters": "intellectual contribution, novelty, methodology, and impact on the field",
        "quiet_reason": "Researchers are often the most visible voice — yet even they can feel unheard when institutional processes overshadow the science itself.",
    },
    "📋 Research Support": {
        "emoji": "📋",
        "title": "The Research Support Language",
        "color": "#1A6B5A",
        "prompt_role": "a research support professional (project manager / research administrator) at a university",
        "what_matters": "timelines, deliverables, reporting requirements, stakeholder coordination, and making the project actually work",
        "quiet_reason": "Research support professionals keep projects alive but rarely appear in acknowledgements, publications, or public narratives about research.",
    },
    "💰 Finance": {
        "emoji": "💰",
        "title": "The Finance Language",
        "color": "#B45309",
        "prompt_role": "a university research finance officer responsible for grants and budgets",
        "what_matters": "eligible costs, funder rules, budget forecasting, audit compliance, and value for money",
        "quiet_reason": "Finance teams are often only heard when something goes wrong — their expertise is invisible until a project runs into trouble.",
    },
    "📄 Contracts": {
        "emoji": "📄",
        "title": "The Contracts Language",
        "color": "#1E4FA0",
        "prompt_role": "a university contracts and legal officer handling research agreements",
        "what_matters": "IP ownership, data rights, liability clauses, funder terms, and institutional risk",
        "quiet_reason": "Contracts professionals are seen as gatekeepers, rarely as enablers — their protective work is invisible when it succeeds.",
    },
    "⚖️ Ethics": {
        "emoji": "⚖️",
        "title": "The Ethics Language",
        "color": "#8B1A1A",
        "prompt_role": "a university research ethics officer or committee member",
        "what_matters": "participant welfare, informed consent, data privacy, risk, and the responsible conduct of research",
        "quiet_reason": "Ethics review is often experienced as a hurdle rather than a partnership — the values this role protects rarely get named in final outputs.",
    },
    "🌍 Public Engagement": {
        "emoji": "🌍",
        "title": "The Public Language",
        "color": "#065F46",
        "prompt_role": "a public engagement and communications professional at a university",
        "what_matters": "public benefit, accessibility, real-world relevance, narrative clarity, and who benefits from this research",
        "quiet_reason": "Public engagement is often treated as an afterthought — a box to tick rather than a lens that reshapes how research is designed and shared.",
    },
}

# ------------------------------------------------------------
# AI GENERATION (Gemini)
# ------------------------------------------------------------

def call_gemini(prompt: str, api_key: str = None) -> str:
    """Call Groq and return raw text response."""
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()


def parse_json(raw: str) -> dict:
    """Strip markdown fences and parse JSON robustly."""
    import re

    # Remove markdown fences if present
    if "```" in raw:
        parts = raw.split("```")
        raw = parts[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    # Extract just the JSON object
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        raw = raw[start:end]

    # Fix unquoted bullet point blocks — the main culprit
    # Find first_questions value that isn't in quotes and wrap it
    def fix_bullet_field(text):
        # Match a key followed by unquoted multiline bullet content
        pattern = r'("first_questions"\s*:\s*)([\s\S]*?)(\n\s*"[a-z])'
        def replacer(m):
            key = m.group(1)
            bullets = m.group(2).strip()
            next_key = m.group(3)
            # Clean up and wrap bullets in a single quoted string
            bullets_clean = bullets.replace('"', "'").replace('\n', ' ').strip()
            # Remove trailing comma if present
            bullets_clean = bullets_clean.rstrip(',').strip()
            return f'{key}"{bullets_clean}",{next_key}'
        return re.sub(pattern, replacer, text)

    raw = fix_bullet_field(raw)

    try:
        return json.loads(raw)
    except Exception:
        # Last resort: manually extract each field
        result = {}
        for field in ["priorities", "first_questions", "ai_interpretation", "hidden_contribution"]:
            pattern = rf'"{field}"\s*:\s*"([\s\S]*?)"(?:\s*,|\s*}})'
            match = re.search(pattern, raw)
            if match:
                result[field] = match.group(1)
            else:
                # Try unquoted multiline (like the bullet block)
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
    raw = call_gemini(prompt)
    return parse_json(raw)


def generate_audit(idea: str) -> dict:
    roles_list = "\n".join([f"- {k}" for k in PERSPECTIVES.keys()])
    prompt = f"""You are analysing how different professional groups in a university research ecosystem interpret the same research idea.

Research idea: {idea}

For each role below, identify:
1. Their PRIMARY concern in one short phrase (max 8 words)
2. A word or short phrase describing their TONE when discussing research

Roles:
{roles_list}

Respond ONLY in this exact JSON format (no markdown, no preamble):
{{
  "rows": [
    {{"role": "role name here", "primary_concern": "...", "tone": "..."}}
  ],
  "shared_goal": "One sentence describing the single goal ALL these roles share despite their different languages.",
  "translation_risk": "One sentence about what is most at risk of being lost when AI translates between these professional languages."
}}"""
    raw = call_gemini(prompt)
    return parse_json(raw)


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

st.title("🔍 The Quiet Languages of Research")
st.subheader("Can AI Translate the Hidden Workforce Behind Research?")
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
    "💡 Enter a Research Idea",
    placeholder="Example: Developing sustainable battery technology for electric vehicles",
    height=100
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    translate_clicked = st.button("🚀 Translate Across the Research Ecosystem")

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

for key, default in [
    ("translated", False),
    ("current_idea", ""),
    ("perspective_cache", {}),
    ("audit_cache", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# Handle translate click
if translate_clicked:
    if not idea.strip():
        st.warning("Please enter a research idea first.")
    else:
        if idea.strip() != st.session_state.current_idea:
            st.session_state.perspective_cache = {}
            st.session_state.audit_cache = None
        st.session_state.current_idea = idea.strip()
        st.session_state.translated = True

# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------

if st.session_state.translated and st.session_state.current_idea:

    st.divider()
    st.markdown("## 🧭 Whose language would you like AI to translate?")
    st.caption("Each perspective shows how a different professional group interprets the same research idea.")

    perspective = st.selectbox(
        "Select a professional perspective",
        list(PERSPECTIVES.keys()),
        label_visibility="collapsed"
    )

    cfg = PERSPECTIVES[perspective]

    # Generate or load from cache
    if perspective not in st.session_state.perspective_cache:
        with st.spinner(f"Translating into {cfg['title']}..."):
            try:
                result = generate_perspective(
    st.session_state.current_idea, perspective
)
                st.session_state.perspective_cache[perspective] = result
            except Exception as e:
                st.error(f"Translation failed: {e}")
                result = None
    else:
        result = st.session_state.perspective_cache[perspective]

    # Render perspective card
    if result:
        color = cfg["color"]

        def clean(text):
            return str(text).replace('"', '&quot;')

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

        # Render using native Streamlit inside a container
        with st.container():
            st.markdown(f"### {cfg['emoji']} {cfg['title']}")
            st.caption("PROFESSIONAL PERSPECTIVE")
            st.divider()

            st.markdown("**🎯 What matters most to them**")
            st.write(result.get("priorities", ""))

            st.markdown("**❓ Questions they ask first**")
            st.write(bullet_text)

            st.markdown("**🤖 How AI interprets this role**")
            st.write(result.get("ai_interpretation", ""))

            st.markdown("**💭 Why this voice is often quiet**")
            st.write(cfg["quiet_reason"])

            st.markdown("**🌱 Hidden contribution**")
            st.write(result.get("hidden_contribution", ""))


    # ---- Translation Audit ----
    st.markdown("---")
    st.markdown("## 📊 Translation Audit")
    st.caption("A comparative view of how all professional groups interpret the same idea — and what this reveals about communication across the ecosystem.")

    if st.button("🔎 Generate Full Translation Audit"):
        with st.spinner("Comparing all professional languages..."):
            try:
                audit = generate_audit(st.session_state.current_idea)
                st.session_state.audit_cache = audit
            except Exception as e:
                st.error(f"Audit failed: {e}")

    if st.session_state.audit_cache:
        audit = st.session_state.audit_cache
        rows = audit.get("rows", [])

        # Emoji map for table rows
        emoji_map = {k.split(" ")[1].lower(): cfg["emoji"] for k, cfg in PERSPECTIVES.items()}

        table_html = """
<div class="audit-card">
<h3>🗂️ Across the Ecosystem</h3>
<table style="width:100%; border-collapse:collapse; font-family:'Inter',sans-serif; font-size:0.93rem;">
<thead>
<tr style="border-bottom: 2px solid #E0D8ED;">
  <th style="text-align:left; padding:10px 8px; color:#4B1E78; font-weight:700;">Role</th>
  <th style="text-align:left; padding:10px 8px; color:#4B1E78; font-weight:700;">Primary Concern</th>
  <th style="text-align:left; padding:10px 8px; color:#4B1E78; font-weight:700;">Typical Tone</th>
</tr>
</thead>
<tbody>
"""
        for i, row in enumerate(rows):
            bg = "#F9F6FF" if i % 2 == 0 else "#FFFFFF"
            role_name = row.get("role", "")
            # Try to find matching emoji
            emoji = ""
            for k, c in PERSPECTIVES.items():
                if any(word in role_name.lower() for word in k.lower().split()[1:]):
                    emoji = c["emoji"]
                    break
            table_html += f"""
<tr style="background:{bg}; border-bottom: 1px solid #F0EAF8;">
  <td style="padding:10px 8px; font-weight:600;">{emoji} {role_name}</td>
  <td style="padding:10px 8px;">{row.get('primary_concern','')}</td>
  <td style="padding:10px 8px; font-style:italic; color:#666;">{row.get('tone','')}</td>
</tr>"""
        table_html += "</tbody></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
<div class="audit-card" style="border-top: 4px solid #4B1E78;">
<h3>🤝 Shared Goal</h3>
<p style="font-size:1rem; line-height:1.7; color:#1A1A2E;">{audit.get('shared_goal','')}</p>
</div>
""", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
<div class="audit-card" style="border-top: 4px solid #B45309;">
<h3>⚠️ Translation Risk</h3>
<p style="font-size:1rem; line-height:1.7; color:#1A1A2E;">{audit.get('translation_risk','')}</p>
</div>
""", unsafe_allow_html=True)

    # ---- Critical Reflection ----
    st.markdown("---")
    st.markdown("""
<div class="reflection-box">
<h3>🧠 A Note on What AI May Overlook</h3>
<p style="font-size:1rem; line-height:1.8; margin-top:12px;">
AI translates language — but professional expertise is more than language.
The concerns, instincts, and institutional knowledge of a finance officer,
a contracts professional, or an ethics reviewer are built from years of experience
that cannot be captured in a text prompt.
</p>
<p style="font-size:1rem; line-height:1.8;">
This app demonstrates both the promise and the limits of AI as a mediator.
It can surface the vocabulary of different roles. It cannot replicate
the judgement behind them — or the relationships, trust, and unwritten rules
that make research ecosystems function.
</p>
<p style="font-size:1rem; line-height:1.8; margin-bottom:0;">
<strong>The quiet languages of research are not quiet because they have nothing to say.
They are quiet because the systems we work within rarely ask them to speak.</strong>
</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown("""
<div class="footer">
    🔍 <strong>The Quiet Languages of Research</strong><br>
    Submitted to the AI Commons Competition — University of Warwick · 2026<br>
    <em>Powered by Google Gemini · AI use disclosed: Gemini generates all perspective translations in response to user input.</em>
</div>
""", unsafe_allow_html=True)