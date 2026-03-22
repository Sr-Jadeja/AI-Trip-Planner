import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Trip Planner", page_icon="🌍", layout="centered")
st.title("🌍 AI Trip Planner")
st.write("Tell me where you want to go and I'll plan your trip!")

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("Where do you want to travel?", placeholder="e.g. Plan a 5 day trip to Goa")
    submitted = st.form_submit_button("Plan My Trip")

if submitted and user_input.strip():
    with st.spinner("Planning your trip..."):
        try:
            res = requests.post(f"{BASE_URL}/query", json={"question": user_input})
            if res.status_code == 200:
                answer = res.json().get("answer", "No answer returned.")
                st.markdown(f"**Generated on:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
                st.markdown("---")
                st.markdown(answer)
            else:
                st.error("Failed to get a response: " + res.text)
        except Exception as e:
            st.error(f"Error: {e}")
