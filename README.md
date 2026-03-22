# AI Trip Planner
An AI-powered trip planning application that helps users generate travel itineraries using an agentic workflow.  
The project is built with a **Streamlit frontend** and a **FastAPI backend**, where the UI sends user queries to the API and receives structured travel plans in response.

---

## Problem Statement
Travel planning requires manually cross-referencing weather, local attractions, exchange rates, and route logistics. This project automates that "research loop" by creating an autonomous agent that can browse the live web, access specialized location APIs, and reason through constraints to deliver a structured itinerary.

![](screenshots/result.png)

---

## Project Structure

```
AI_Trip_Planner/
├── agent/
│   └── agentic_workflow.py   # LangGraph agent setup
├── config/
│   └── config.yaml           # LLM config
├── prompt_library/
│   └── prompt.py             # System prompt
├── tools/
│   └── tools.py              # All LangChain tools
├── utils/
│   └── model_loader.py       # LLM loader
├── main.py                   # FastAPI backend
├── streamlit_app.py          # Streamlit frontend
├── requirements.txt
└── .env                      # API keys (not committed)
```

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** (see `env.example`):
   ```
   GROQ_API_KEY=...
   OPENWEATHERMAP_API_KEY=...
   GPLACES_API_KEY=...
   TAVILY_API_KEY=...
   EXCHANGE_RATE_API_KEY=...
   ```

3. **Run the backend**
   ```bash
   uvicorn main:app --reload
   ```

4. **Run the frontend** (in a new terminal)
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Tech Stack & Architecture
- **Orchestration** - LangGraph for managing the agent's state and decision-making cycles.
- **Streamlit** – Frontend UI
- **FastAPI** – Backend API

---

## Run the Web App

User enters a query in the Streamlit UI (e.g., “Plan a trip to Goa for 5 days”).

![App](screenshots/app.png)

---

## Results
Streamlit sends the request to the FastAPI backend. The backend runs the agentic workflow to generate a plan. The response is sent back to Streamlit and displayed to the user.

![Result](screenshots/result.png)