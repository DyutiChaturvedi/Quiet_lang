# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 16:21:38 2026

@author: u4123978
"""

import streamlit as st
from openai import OpenAI

# ---------------------------
# API CLIENT
# ---------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="The Quiet Languages of Research",
    layout="wide"
)

# ---------------------------
# TITLE SECTION (UNCHANGED)
# ---------------------------
st.title("The Quiet Languages of Research")
st.subheader("Can AI Translate the Hidden Workforce Behind Research?")

st.markdown("""
Enter a research idea below and explore how different members of the research workforce might view it.
""")

# ---------------------------
# INPUT
# ---------------------------
idea = st.text_area(
    "Research Idea",
    placeholder="Example: Developing sustainable battery technology for electric vehicles"
)

# ---------------------------
# SIDEBAR (AI TOGGLE)
# ---------------------------
st.sidebar.header("Controls")
use_ai = st.sidebar.toggle("Enable AI interpretation", value=True)

# ---------------------------
# AI FUNCTION
# ---------------------------
def ai_view(role, idea_text):
    if not use_ai:
        return None

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a specialist in {role}. Translate the research idea into that perspective clearly and concisely."
            },
            {
                "role": "user",
                "content": idea_text
            }
        ]
    )
    return response.choices[0].message.content

# ---------------------------
# MAIN LOGIC
# ---------------------------
if st.button("Translate"):

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("👩‍🔬 Researcher")

        res = ai_view("academic research", idea)
        if res:
            st.info(res)
        else:
            st.write(
                f"This project explores new knowledge and methods related to: **{idea}**. "
                "The focus is on originality, evidence and research impact."
            )

        st.subheader("📋 Research Support")

        res = ai_view("research administration and funding", idea)
        if res:
            st.warning(res)
        else:
            st.write(
                f"For this project ({idea}), key considerations include funder eligibility, "
                "partnerships, timelines and submission requirements."
            )

        st.subheader("💰 Finance")

        res = ai_view("research finance and budgeting", idea)
        if res:
            st.success(res)
        else:
            st.write(
                "This project requires consideration of resources, staffing, equipment and "
                "overall value for money."
            )

    with col2:

        st.subheader("📄 Contracts")

        res = ai_view("research contracts and intellectual property", idea)
        if res:
            st.info(res)
        else:
            st.write(
                "This project may involve intellectual property, collaboration agreements "
                "and data-sharing arrangements."
            )

        st.subheader("⚖️ Ethics")

        res = ai_view("research ethics and governance", idea)
        if res:
            st.warning(res)
        else:
            st.write(
                "This project requires consideration of ethical implications, governance "
                "requirements and potential risks."
            )

        st.subheader("🌍 Public")

        res = ai_view("science communication for general public", idea)
        if res:
            st.success(res)
        else:
            st.write(
                f"In simple terms, this project aims to create benefits for society through: "
                f"**{idea}**."
            )

    st.divider()

    # ---------------------------
    # AUDIT SECTION (UNCHANGED STRUCTURE, ENHANCED TEXT OPTIONAL)
    # ---------------------------
    st.header("🔄 Translation Audit")

    st.success("""
    What AI may help with:
    - Accessibility
    - Communication
    - Clarity
    - Cross-team understanding
    """)

    st.warning("""
    What may be lost:
    - Technical nuance
    - Context
    - Uncertainty
    - Professional judgement
    """)

    st.info("""
    Key Reflection:
    AI can help bridge communication gaps across the research ecosystem,
    but translation is never neutral. What becomes clearer may also become
    simplified.
    """
