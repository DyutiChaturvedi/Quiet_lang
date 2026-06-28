import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="The Quiet Languages of Research",
    page_icon="🔍",
    layout="wide"
)

# ----------------------------
# SIDEBAR
# ----------------------------

with st.sidebar:

    st.title("🔍 About this Project")

    st.markdown("""
This interactive demonstration explores how a single research idea is interpreted by different members of the research workforce within the research ecosystem.

Rather than replacing expertise, AI is used here as a tool to explore communication across professional boundaries.
""")

    st.markdown("---")

    st.markdown("### Research Workforce")

    st.markdown("""
👩‍🔬 Researcher

📋 Research Support

💰 Finance

📄 Contracts

⚖️ Ethics

🌍 Public Engagement
""")

    st.markdown("---")

    st.caption(
        "University of Warwick\n\nAI Commons Competition 2026"
    )

# ----------------------------
# TITLE
# ----------------------------

st.title("🔍 The Quiet Languages of Research")

st.subheader("Can AI Translate the Hidden Workforce Behind Research?")

st.markdown(
"""
Research is often associated with academics alone.

This project explores whether AI can help translate one research idea across the different professional languages spoken throughout the research ecosystem.
"""
)

st.divider()

# ----------------------------
# DASHBOARD
# ----------------------------

c1, c2, c3 = st.columns(3)

c1.metric("Research Roles", "6")
c2.metric("Research Ideas", "1")
c3.metric("Shared Goal", "Successful Research")

st.divider()

# ----------------------------
# INPUT
# ----------------------------

idea = st.text_area(
    "💡 Enter a Research Idea",
    placeholder="Example: Developing sustainable battery technology for electric vehicles"
)

if st.button("🚀 Translate Across the Research Ecosystem", use_container_width=True):

    with st.spinner("Translating research idea..."):

        time.sleep(1)

    st.success("Translation complete!")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        with st.expander("👩‍🔬 Researcher", expanded=True):

            st.write(
                f"""
The research focuses on **{idea}**.

Priority:

• Originality

• Methodology

• Evidence

• Research impact
"""
            )

        with st.expander("📋 Research Support", expanded=True):

            st.write(
                f"""
For **{idea}**, the key questions are:

• Is it eligible for funding?

• Does it meet the funder's priorities?

• Are collaborators appropriate?

• Is the application competitive?
"""
            )

        with st.expander("💰 Finance", expanded=True):

            st.write(
                f"""
From a finance perspective, **{idea}** requires consideration of:

• Staffing

• Equipment

• Value for money

• Long-term sustainability
"""
            )

    with col2:

        with st.expander("📄 Contracts", expanded=True):

            st.write(
                f"""
Potential considerations include:

• Intellectual Property

• Collaboration agreements

• Data sharing

• Commercialisation opportunities
"""
            )

        with st.expander("⚖️ Ethics", expanded=True):

            st.write(
                f"""
Ethical considerations include:

• Governance

• Risk

• Participant protection

• Responsible research practices
"""
            )

        with st.expander("🌍 Public Engagement", expanded=True):

            st.write(
                f"""
In everyday language:

**{idea}** aims to create positive benefits for society and improve people's lives through research and innovation.
"""
            )

    st.divider()

    st.header("🔄 Translation Audit")

    st.markdown(
"""
Although every audience is looking at the same research idea, each interprets it through a different professional lens.
"""
)

    comparison = pd.DataFrame({

        "What AI may help with ✅": [

            "Makes research more accessible",

            "Adapts language for different audiences",

            "Supports communication between teams",

            "Speeds up drafting",

            "Highlights audience priorities"

        ],

        "What may be lost ⚠️": [

            "Technical precision",

            "Context and background",

            "Research uncertainty",

            "Professional judgement",

            "Nuance and complexity"

        ]

    })

    st.table(comparison)

    st.divider()

    st.info(
"""
### 💭 Critical Reflection

AI can support communication by translating research ideas into language that is meaningful for different audiences.

However, translation is never neutral.

Every translation involves choices about what to simplify, emphasise or omit. While AI can improve accessibility and efficiency, it should complement—not replace—the expertise, judgement and lived experience of the people who enable research.
"""
    )

    st.divider()

    st.caption(
"""
Created for the University of Warwick AI Commons Competition

*"The Quiet Languages of Research: Can AI Translate the Hidden Workforce Behind Research?"*
"""
    )