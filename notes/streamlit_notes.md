# Streamlit Frontend (`streamlit_app.py`) Architecture Notes

> **Target Role:** Entry-Level Business Analyst (BA) / Analytics Consultant  
> **Module:** `streamlit_app.py`  
> **Key Architecture:** Interactive Consumer Interface & Rapid Prototyping

---

## 1. Executive Summary & Business Purpose

In product management and analytics consulting, **rapid prototyping and consumer feedback loops are essential**. 

While `main.py` provides the backend REST API for system-to-system integrations, **`streamlit_app.py`** provides the **human-facing interactive experience**. It enables non-technical business stakeholders, executives, and travelers to test and experience the AI Travel Concierge directly in a modern web browser.

---

## 2. Refactoring Summary: What Was Simplified

### What Was Removed:
1. **Removed Manual `importlib.reload(...)` Boilerplate:** Purged 8 lines of development-only hot-reload calls from the top of the file, returning to clean standard Python imports.
2. **Simplified Template Selection:** Removed manual session state management in favor of Streamlit's native `st.pills`, automatically populating the input form with sample queries.
3. **Consolidated Error Messaging:** Cleaned up rate-limit notifications into a concise alert without overwhelming the user.

---

## 3. The Clean Implementation (~65 Lines)

```python
import streamlit as st
import datetime
from dotenv import load_dotenv
from agent.agentic_workflow import GraphBuilder

load_dotenv()

st.set_page_config(page_title="AI Travel Concierge", page_icon="✈️", layout="centered")

st.title("✈️ AI Travel Concierge & Trip Planner")
st.caption("Curating bespoke travel itineraries powered by Google Gemini. Developed by Manish Biswas.")

# Sidebar overview
with st.sidebar:
    st.markdown("### ✈️ AI Travel Concierge")
    st.markdown("""
    Curating journeys with:
    - ⛅ **Real-time Weather Forecasts**
    - 🗺️ **Tavily AI Web Discovery**
    - 💱 **Live Currency & Expense Est.**
    """)
    st.caption("App version 1.2.0")

# Example prompt templates
templates = [
    "Plan a trip to Goa for 5 days",
    "3-day weekend itinerary in Tokyo",
    "Budget trip to Paris for a couple"
]
selected = st.pills("Choose an itinerary template:", templates, selection_mode="single")

# Input form
with st.form("query_form"):
    user_input = st.text_input(
        "Where would you like to travel?",
        value=selected if selected else "",
        placeholder="e.g., 5-day cultural trip to Kyoto on a $2,000 budget"
    )
    submitted = st.form_submit_button("Generate Plan", type="primary", use_container_width=True)

if submitted and user_input.strip():
    try:
        with st.spinner("Our AI concierge is researching weather, places, and currency..."):
            agent = GraphBuilder(model_provider="gemini")()
            output = agent.invoke({"messages": [user_input]})
            raw = output["messages"][-1].content
            answer = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in raw) if isinstance(raw, list) else str(raw)

        # Display Itinerary
        itinerary = f"""# 🌍 Your Travel Itinerary

**Generated on:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | **Model:** Gemini 3.1 Flash Lite  
**Created by:** Manish Biswas

---

{answer}

---
*:material/info: Please verify flight details and attraction timings prior to departure.*"""

        st.markdown(itinerary)
        st.download_button(
            label="📥 Download Itinerary (.md)",
            data=itinerary,
            file_name=f"itinerary_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    except Exception as e:
        error_msg = str(e)
        st.error(f"Error: {error_msg}")
        if "429" in error_msg or "quota" in error_msg.lower():
            st.warning("Gemini rate limit momentarily reached. Please wait 30 seconds and try again.")
```

---

## 4. Key UI Components & Business Value

| UI Component | Streamlit Function | Business & User Experience Purpose |
| :--- | :--- | :--- |
| **Interactive Templates** | `st.pills(...)` | Lowers onboarding friction by letting first-time users test popular destinations with a single click. |
| **Bespoke Input Form** | `st.form(...)` | Prevents unnecessary page re-renders until the traveler explicitly clicks "Generate Plan". |
| **Activity Indicator** | `st.spinner(...)` | Provides transparent visual feedback while the agent executes its multi-tool research loop. |
| **Direct Export** | `st.download_button(...)` | Allows travelers to save their personalized markdown itinerary locally for offline viewing. |
| **Fallback Alerts** | `st.warning(...)` | Soft error handling informing the user if free-tier LLM rate limits are temporarily met. |

---

## 5. Interview Talking Points (Business Analyst Perspective)

### Q: "Why choose Streamlit for the user interface?"
> *"From a Business Analyst perspective, Streamlit is the premier tool for **rapid prototyping, stakeholder demos, and interactive validation**. Building traditional React frontends takes weeks of development. With Streamlit, we created a clean, production-ready travel concierge UI in ~65 lines of Python, allowing our product team to gather immediate user feedback and validate product-market fit."*

### Q: "How did you design the user experience to minimize friction?"
> *"Travelers often experience 'blank canvas paralysis' when facing a blank text box. To solve this, I added **template pills (`st.pills`)** with sample itineraries (e.g. Goa, Tokyo, Paris). Users can either pick a pre-set journey or customize their own budget and destination. Furthermore, the **native download button** gives users tangible ownership of their generated itinerary for offline travel."*

### Q: "How does the Streamlit frontend interact with the AI agent?"
> *"When the user submits their request, Streamlit calls our `GraphBuilder` agent. The agent autonomously queries weather, attractions, currency rates, and budget calculations in the background. Streamlit captures the final synthesized answer, wraps it in timestamped metadata, and renders it as rich, readable markdown."*
