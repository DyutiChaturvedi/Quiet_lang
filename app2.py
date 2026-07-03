# ============================================================
# THE QUIET LANGUAGES OF RESEARCH
# University of Warwick AI Commons Competition
# Powered by Groq (free API)
# ============================================================

import streamlit as st
from groq import Groq
import json
import re

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ------------------------------------------------------------
# PAGE SETTINGS
# ------------------------------------------------------------

st.set_page_config(
    page_title="The Quiet Languages of Research",
    layout="wide"
)

# ------------------------------------------------------------
# CUSTOM CSS — iOS style, dark mode safe
# ------------------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    background-color: #F2F2F7;
    font-family: -apple-system, 'SF Pro Display', 'Inter', BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    color: #1C1C1E;
}

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

p { color: #3A3A3C; }

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

.stButton > button {
    width: 100%;
    background: #5856D6;
    color: #FFFFFF;
    border: none;
    border-radius: 14px;
    padding: 14px 20px;
    font-size: 16px;
    font-weight: 600;
    font-family: -apple-system, 'Inter', sans-serif;
    letter-spacing: -0.2px;
    transition: background 0.2s ease, transform 0.1s ease;
}

.stButton > button:hover {
    background: #4341C2;
    color: #FFFFFF;
    transform: scale(0.99);
}

textarea {
    border-radius: 12px !important;
    font-family: -apple-system, 'Inter', sans-serif !important;
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

.ios-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    color: #1C1C1E;
    font-size: 0.95rem;
    line-height: 1.65;
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

.bullet-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 0.95rem;
    line-height: 1.6;
    color: #1C1C1E;
}

.bullet-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #1C1C1E;
    margin-top: 8px;
    flex-shrink: 0;
}

/* --- AI Gains/Misses table --- */
.ai-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.92rem;
    border-radius: 16px;
    overflow: hidden;
    background: #FFFFFF;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-bottom: 12px;
}

.ai-table th {
    padding: 13px 16px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    border-bottom: 1px solid #F2F2F7;
}

.ai-table th.gains-header {
    background: #F0FFF4;
    color: #1A6B3A;
    text-align: left;
}

.ai-table th.misses-header {
    background: #FFF5F5;
    color: #C0392B;
    text-align: left;
    border-left: 1px solid #F2F2F7;
}

.ai-table td {
    padding: 12px 16px;
    vertical-align: top;
    line-height: 1.6;
    color: #1C1C1E;
    border-bottom: 1px solid #F2F2F7;
}

.ai-table td.gains-cell {
    background: #FAFFFE;
    border-left: none;
}

.ai-table td.misses-cell {
    background: #FFFAFA;
    border-left: 1px solid #F2F2F7;
}

.ai-table tr:last-child td {
    border-bottom: none;
}

.row-dot-green {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #34C759;
    margin-right: 8px;
    vertical-align: middle;
    margin-top: -2px;
}

.row-dot-red {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #FF3B30;
    margin-right: 8px;
    vertical-align: middle;
    margin-top: -2px;
}

/* --- Reflection box --- */
.reflection-box {
    background: #1C1C1E;
    border-radius: 16px;
    padding: 24px 22px;
    margin-top: 8px;
}

.reflection-box p {
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    color: #EBEBF5 !important;
    margin-bottom: 12px !important;
}

.reflection-box strong {
    color: #FFFFFF !important;
}

.reflection-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #8E8E93;
    margin-bottom: 10px;
}

.footer {
    text-align: center;
    padding: 28px 0 12px 0;
    color: #8E8E93;
    font-size: 0.8rem;
    border-top: 1px solid #E5E5EA;
    margin-top: 48px;
}

hr { border-color: #E5E5EA; }

/* ---- Dark mode ---- */
@media (prefers-color-scheme: dark) {

    html, body, .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    h1, h2, h3 { color: #FFFFFF !important; }
    p { color: #EBEBF5 !important; }

    [data-testid="stSidebar"] {
        background-color: #1C1C1E !important;
        border-right: 1px solid #38383A !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li { color: #EBEBF5 !important; }

    textarea {
        background: #1C1C1E !important;
        border-color: #38383A !important;
        color: #FFFFFF !important;
    }

    .ios-card {
        background: #1C1C1E !important;
        box-shadow: none !important;
        border: 1px solid #2C2C2E !important;
        color: #EBEBF5 !important;
    }

    .bullet-row { color: #EBEBF5 !important; }
    .bullet-dot { background: #FFFFFF !important; }

    .ai-table {
        background: #1C1C1E !important;
        border: 1px solid #2C2C2E !important;
    }

    .ai-table th.gains-header {
        background: #0D2B18 !important;
        color: #34C759 !important;
    }

    .ai-table th.misses-header {
        background: #2B0D0D !important;
        color: #FF6B6B !important;
        border-left: 1px solid #38383A !important;
    }

    .ai-table td {
        color: #EBEBF5 !important;
        border-bottom: 1px solid #2C2C2E !important;
    }

    .ai-table td.gains-cell { background: #0D1F12 !important; }
    .ai-table td.misses-cell {
        background: #1F0D0D !important;
        border-left: 1px solid #38383A !important;
    }

    .reflection-box {
        background: #2C2C2E !important;
        border: 1px solid #38383A !important;
    }

    .footer {
        border-top: 1px solid #38383A !important;
        color: #636366 !important;
    }

    hr { border-color: #38383A !important; }

    .stAlert {
        background: #1C1C1E !important;
        border: 1px solid #2C2C2E !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# PERSPECTIVE CONFIG
# ------------------------------------------------------------

PERSPECTIVES = {
    "Researcher": {
        "title": "The Researcher's Language",
        "prompt_role": "an academic researcher at a research-intensive university",
        "what_matters": "novelty, methodology, and impact on the field",
    },
    "Research Support": {
        "title": "The Research Support Language",
        "prompt_role": "a research support officer or research development officer responsible for submission of the grant application and processing the awarded grant",
        "what_matters": "timelines, funder requirements, stakeholder coordination, eligibility for the researcher and eligible costs",
    },
    "Finance": {
        "title": "The Finance Language",
        "prompt_role": "a university research finance officer responsible for invoicing of the budgets to the collaborators and the researcher if the grant is awarded",
        "what_matters": "eligible costs, budget forecasting and optimisation, audit compliance, and value for money",
    },
    "Contracts": {
        "title": "The Contracts Language",
        "prompt_role": "a university contracts and legal officer handling research agreements",
        "what_matters": "IP ownership, data rights, liability clauses, funder terms, and institutional risk",
    },
    "Ethics": {
        "title": "The Ethics Language",
        "prompt_role": "a university research ethics officer",
        "what_matters": "participant welfare, informed consent, data privacy, risk, and the responsible conduct of research",
    },
}

# Static AI gains/misses per role — consistent, no AI call needed
AI_GAINS_MISSES = {
    "Researcher": [
        ("Surfaces relevant literature and methodology gaps quickly", "Cannot evaluate whether a research question is truly novel or significant"),
        ("Suggests interdisciplinary connections across fields", "Misses the tacit knowledge built through years of lab or fieldwork"),
        ("Drafts structured summaries of complex ideas", "Cannot replicate the creative intuition behind a research breakthrough"),
        ("Helps identify potential journals or conferences", "Overlooks the informal networks that shape what gets published"),
    ],
    "Research Support": [
        ("Summarises funder eligibility rules and deadlines", "Cannot judge which funders are realistically likely to fund Universities"),
        ("Drafts project timelines and milestone structures", "Misses the informal negotiation that keeps stakeholders aligned"),
        ("Checks application text against funder criteria", "Cannot anticipate how a funder panel will read between the lines"),
        ("Formats budgets and cost breakdowns quickly", "Overlooks the institutional history that shapes what gets approved"),
    ],
    "Finance": [
        ("Categorises expenditure against funder cost headings", "Cannot interpret ambiguous funder rules the way an experienced officer can"),
        ("Flags budget variances and forecasting gaps", "Misses the relationship context that allows renegotiation with funders"),
        ("Generates audit-ready financial summaries", "Cannot account for mid-project scope changes and their financial knock-ons"),
        ("Cross-checks invoices against approved budgets", "Overlooks the institutional memory of what auditors have accepted before"),
    ],
    "Contracts": [
        ("Identifies standard IP and liability clauses quickly", "Cannot weigh institutional risk in the way an experienced legal officer can"),
        ("Compares contract terms against funder templates", "Misses the negotiating precedents built up over years of agreements"),
        ("Summarises long agreements into plain language", "Cannot judge which clauses are dealbreakers vs. acceptable compromises"),
        ("Flags missing or unusual terms for review", "Overlooks the relationship dynamics that shape what is actually negotiable"),
    ],
    "Ethics": [
        ("Checks protocols against standard ethical frameworks", "Cannot assess the lived experience of research participants"),
        ("Summarises consent form requirements by jurisdiction", "Misses the power dynamics between researchers and vulnerable groups"),
        ("Flags common risks in study design early", "Cannot weigh context-dependent harms that fall outside standard categories"),
        ("Drafts ethics committee application sections", "Overlooks emerging ethical questions that no framework has yet named"),
    ],
}

# ------------------------------------------------------------
# AI GENERATION
# ------------------------------------------------------------

def call_groq(prompt: str) -> str:
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1200,
    )
    return response.choices[0].message.content.strip()


def parse_json(raw: str) -> dict:
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
    try:
        return json.loads(raw)
    except Exception:
        result = {}
        for field in ["priorities", "first_questions", "ai_interpretation", "quiet_contribution"]:
            pattern = rf'"{field}"\s*:\s*"([\s\S]*?)"(?=\s*[,}}])'
            match = re.search(pattern, raw)
            if match:
                result[field] = match.group(1).replace("\\n", "\n").replace('\\"', '"')
            else:
                arr_pattern = rf'"{field}"\s*:\s*(\[[\s\S]*?\])(?=\s*[,}}])'
                arr_match = re.search(arr_pattern, raw)
                if arr_match:
                    try:
                        result[field] = json.loads(arr_match.group(1))
                    except Exception:
                        result[field] = arr_match.group(1)
        return result


def format_bullets(raw) -> list:
    if isinstance(raw, list):
        return [str(q).strip().lstrip("•-0123456789.) ").strip() for q in raw if str(q).strip()]
    text = str(raw)
    if "•" in text:
        items = text.split("•")
    elif "\n" in text:
        items = text.split("\n")
    else:
        items = [text]
    cleaned = [i.strip().lstrip("-•0123456789.) ").strip() for i in items if i.strip()]
    return [c for c in cleaned if len(c) > 5]


def generate_perspective(idea: str, perspective_key: str) -> dict:
    cfg = PERSPECTIVES[perspective_key]
    prompt = f"""You are helping a user understand how different professional groups within a university research ecosystem interpret the same research idea.

Translate this research idea through the professional lens of {cfg["prompt_role"]}.
For this role, what matters most is: {cfg["what_matters"]}.

Research idea: {idea}

You MUST respond ONLY with a valid JSON object. No markdown, no explanation, no text before or after the JSON.

{{
  "priorities": "2-3 sentences on what this professional immediately focuses on",
  "first_questions": ["question 1", "question 2", "question 3", "question 4"],
  "ai_interpretation": "2-3 sentences on how AI might help this professional and where it might fall short",
  "quiet_contribution": "1-2 sentences on a contribution this role makes that rarely gets credited in research outputs"
}}

Rules:
- first_questions must be a valid JSON array of 4 plain strings
- Do not use bullet points or special characters inside the strings
- All four fields are required — do not omit quiet_contribution"""

    raw = call_groq(prompt)
    return parse_json(raw)


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
    ]:
        st.write(f"— {title}")

    st.markdown("---")
    st.info("""
**How to use**

1. Enter a research idea.
2. Click Translate.
3. Choose a professional perspective.
4. Explore what AI gains and misses for that role.
5. Reflect on what AI reveals — and what it may overlook.
""")
    st.markdown("---")

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

st.title("The Quiet Languages of Research")
st.subheader("Can AI translate the work of the hidden workforce behind research?")
st.markdown("""
Research succeeds because many different professional groups contribute their expertise.
Although everyone is working towards the same goal, they often communicate through different priorities, responsibilities, and professional languages.

This interactive prototype explores whether AI can help translate these perspectives while encouraging reflection on what may be gained, and lost, in the process.
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
        with st.container():
            st.markdown(f"### {cfg['title']}")
            st.caption("Professional Perspective")
            st.divider()

            # What matters most
            st.markdown("<div class='ios-section-label'>What matters most</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='ios-card'>{result.get('priorities', '')}</div>", unsafe_allow_html=True)

            # Questions
            st.markdown("<div class='ios-section-label'>Questions they ask first</div>", unsafe_allow_html=True)
            questions = format_bullets(result.get("first_questions", []))
            if questions:
                bullets_html = "".join(
                    f"<div class='bullet-row'><div class='bullet-dot'></div><div>{q}</div></div>"
                    for q in questions
                )
                st.markdown(f"<div class='ios-card'>{bullets_html}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ios-card'>{result.get('first_questions', '')}</div>", unsafe_allow_html=True)

            # How AI interprets this role
            st.markdown("<div class='ios-section-label'>How AI interprets this role</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='ios-card'>{result.get('ai_interpretation', '')}</div>", unsafe_allow_html=True)

            # Quiet contribution
            hidden = result.get("quiet_contribution", "").strip()
            if not hidden:
                try:
                    retry = generate_perspective(st.session_state.current_idea, perspective)
                    hidden = retry.get("quiet_contribution", "").strip()
                    result["quiet_contribution"] = hidden
                    st.session_state.perspective_cache[perspective] = result
                except Exception:
                    hidden = ""

            st.markdown("<div class='ios-section-label'>Quiet contribution</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='ios-card'>{hidden if hidden else 'Not available — please try translating again.'}</div>",
                unsafe_allow_html=True
            )

        # ---- What AI Gains vs Misses ----
        st.markdown("---")
        st.markdown("<div class='ios-section-label'>What AI gains and misses for this role</div>", unsafe_allow_html=True)
        st.caption("A role-specific comparison of where AI adds value and where professional judgement cannot be replaced.")

        rows = AI_GAINS_MISSES.get(perspective, [])
        rows_html = "".join(
            f"""<tr>
  <td class='gains-cell'><span class='row-dot-green'></span>{g}</td>
  <td class='misses-cell'><span class='row-dot-red'></span>{m}</td>
</tr>"""
            for g, m in rows
        )

        table_html = f"""
<table class='ai-table'>
  <thead>
    <tr>
      <th class='gains-header'>What AI gains</th>
      <th class='misses-header'>What AI misses</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
"""
        st.markdown(table_html, unsafe_allow_html=True)

    # ---- Critical Reflection ----
    st.markdown("---")
    st.markdown("""
<div class="reflection-box">
<div class="reflection-label">A note on what AI may overlook</div>
<p>
AI helps in translating different languages of the research workforce but professional expertise cannot be replaced.
The concerns, instincts, and institutional knowledge of a finance officer, a contracts professional, or an ethics
reviewer are built from years of experience that no prompt can fully capture.
</p>
<p>
The table above makes this visible. AI can process, summarise, and surface patterns. What it cannot do is sit in a
room, read the atmosphere, draw on institutional memory, or carry the professional responsibility that comes
with each of these roles.
</p>
<p style="margin-bottom:0;">
<strong>The Quiet Languages of Research are the intricate nuances which go unnoticed sometimes.
This prototype asks: Can the hidden languages of the research workforce be replaced with AI? </strong>
</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown("""
<div class="footer">
    <strong>The Quiet Languages of Research</strong><br>
    Submitted by Dyuti Chaturvedi &nbsp;&middot;&nbsp; AI Commons Competition, University of Warwick &nbsp;&middot;&nbsp; 2026<br>
    <span style="color:#C7C7CC;">Powered by Groq &nbsp;&middot;&nbsp; AI use disclosed: all perspective translations are AI-generated in response to user input.</span>
</div>
""", unsafe_allow_html=True)