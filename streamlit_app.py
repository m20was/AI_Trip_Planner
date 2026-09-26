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
