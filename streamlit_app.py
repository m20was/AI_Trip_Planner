import streamlit as st
import datetime
from dotenv import load_dotenv
from agent.agentic_workflow import GraphBuilder

load_dotenv()

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon=":material/travel:",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("🌍 AI Marketing Campaign Planner")
st.caption("Plan your next adventure with state-of-the-art AI workflows. Developed by Manish Biswas.")

st.sidebar.markdown("### 🌍 AI Travel Planner")
st.sidebar.markdown("""
This assistant plans your trip using tools for:
- :material/cloud: Real-time Weather
- :material/search: Place Search (Google Places)
- :material/calculate: Currency & Expense Calculation
""")
st.sidebar.caption("App version 1.1.0")

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
            agent = GraphBuilder(model_provider="groq")()
            output = agent.invoke({"messages": [user_input]})
            answer = output["messages"][-1].content

        markdown_content = f"""# 🌍 Your Travel Itinerary

**Generated on:** {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}
**Powered by:** Groq (llama-3.3-70b-versatile)
**Developed by:** Manish Biswas

---

{answer}

---

*:material/info: Please verify all timings, flight details, and local weather forecasts prior to departures.*"""
        
        st.markdown(markdown_content)
        
    except Exception as e:
        error_msg = str(e)
        st.error(f"Error: {error_msg}")
        
        if "403" in error_msg or "Access denied" in error_msg:
            st.warning(
                "### :material/vpn_lock: Network Block / VPN Issue Detected\n"
                "The Groq API is blocking your network connection or VPN address.\n\n"
                "**Steps to fix:**\n"
                "1. **Disable VPN:** If you are using a VPN or proxy, disable it and refresh the page."
            )
        elif "429" in error_msg or "quota" in error_msg or "limit" in error_msg:
            st.warning(
                "### :material/hourglass_empty: API Quota Exceeded\n"
                "The default Groq API key has reached its usage limits or has run out of credits."
            )
