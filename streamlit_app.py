import streamlit as st
import datetime
from dotenv import load_dotenv
import importlib
import prompt_library.prompt
importlib.reload(prompt_library.prompt)
import agent.agentic_workflow
importlib.reload(agent.agentic_workflow)
from agent.agentic_workflow import GraphBuilder

load_dotenv()

st.set_page_config(
    page_title="AI Travel Concierge",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("✈️ AI Travel Concierge & Trip Planner")
st.caption("Curating bespoke, real-time travel itineraries powered by Google Gemini. Developed by Manish Biswas.")

st.sidebar.markdown("### ✈️ AI Travel Concierge")
st.sidebar.markdown("""
This assistant curates your journey using:
- ⛅ **Real-time Weather Forecasts**
- 🗺️ **Tavily AI Web Discovery**
- 💱 **Live Currency & Expense Est.**
""")
st.sidebar.caption("App version 1.2.0")

examples = [
    "Plan a trip to Goa for 5 days",
    "3-day weekend itinerary in Tokyo",
    "Budget trip to Paris for a couple"
]

if "example_query" not in st.session_state:
    st.session_state.example_query = ""

st.markdown("### :material/map: Where would you like to travel?")
selected_example = st.pills("Or select an example itinerary template:", examples, selection_mode="single")

if selected_example:
    st.session_state.example_query = selected_example

with st.form(key="query_form", border=True):
    user_input = st.text_input(
        "Enter your query",
        value=st.session_state.example_query,
        placeholder="e.g., Plan a trip to Goa for 5 days"
    )
    submit_button = st.form_submit_button("Generate Plan", icon=":material/send:", type="primary")

if submit_button and user_input.strip():
    try:
        with st.spinner("Our AI travel agent is researching and planning your trip..."):
            agent = GraphBuilder(model_provider="gemini")()
            output = agent.invoke({"messages": [user_input]})
            raw_content = output["messages"][-1].content
            if isinstance(raw_content, list):
                answer = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in raw_content])
            else:
                answer = str(raw_content)

        markdown_content = f"""# 🌍 Your Travel Itinerary

**Generated on:** {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}
**Powered by:** Google Gemini (gemini-3.1-flash-lite)
**Developed by:** Manish Biswas

---

{answer}

---

*:material/info: Please verify all timings, flight details, and local weather forecasts prior to departures.*"""
        
        st.markdown(markdown_content)
        st.download_button(
            label="📥 Download Itinerary (.md)",
            data=markdown_content,
            file_name=f"itinerary_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
        
    except Exception as e:
        error_msg = str(e)
        st.error(f"Error: {error_msg}")
        
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            st.warning(
                "### :material/hourglass_empty: Gemini Free-Tier Rate Limit Reached\n"
                "Google's free-tier rate limit was momentarily exceeded. Please wait 30–60 seconds and submit your query again."
            )
