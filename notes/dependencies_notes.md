# Dependencies & Packaging Architecture Notes

> **Target Role:** Entry-Level Business Analyst (BA) / Analytics Consultant  
> **Files:** `pyproject.toml` & `requirements.txt`  
> **Standards:** PEP 621 (Modern Python Packaging Specification)

---

## 1. Executive Summary & Business Importance

In enterprise software products, **dependency management is a critical risk and cost factor**. Bloated dependencies introduce:
* **Security Vulnerabilities:** Every unvetted third-party package increases the attack surface (CVE risks).
* **Infrastructure Costs:** Heavier packages increase Docker image size, cloud bandwidth, and deployment times.
* **Maintenance Debt:** Redundant libraries create version conflicts and dependency hell.

Our application maintains a **lean, production-ready manifest of exactly 12 essential packages**, with `pyproject.toml` serving as the single source of truth.

---

## 2. The 12 Core Dependencies Matrix

| # | Package | Layer | Business Capability | Where Used |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **`langchain`** | AI Framework | Tool interfaces (`@tool`) and message typing | `tools/`, `streamlit_app.py` |
| **2** | **`langchain-google-genai`** | LLM Provider | Connects to Google Gemini 3.1 Flash Lite API | `utils/model_loader.py` |
| **3** | **`langchain_tavily`** | Tool / Search | AI-optimized live web discovery (Attractions, Food) | `tools/place_search_tool.py` |
| **4** | **`langgraph`** | Agent Workflow | ReAct agent state machine and decision loop | `agent/agentic_workflow.py` |
| **5** | **`fastapi`** | Backend API | High-performance REST endpoints (`POST /query`) | `main.py` |
| **6** | **`uvicorn`** | Server Host | Lightning-fast ASGI production web server | `entrypoint.sh` |
| **7** | **`streamlit`** | Frontend UI | Interactive, responsive web application for travelers | `streamlit_app.py` |
| **8** | **`pydantic`** | Data Governance | Request validation contracts and strict schema types | `main.py`, `utils/model_loader.py` |
| **9** | **`python-dotenv`** | Security | Secure environment variable management (`.env`) | Throughout project |
| **10** | **`pyyaml`** | Config Management| Secure parsing of external `config/config.yaml` | `utils/config_loader.py` |
| **11** | **`requests`** | REST Clients | Direct HTTP calls to OpenWeather and ExchangeRate | `tools/weather_info_tool.py`, `tools/currency_conversion_tool.py` |
| **12** | **`pytest`** | Quality Assurance | Automated unit testing suite | `tests/unit/test_calculator.py` |

---

## 3. `pyproject.toml` vs. `requirements.txt`: Modern Standards

### `pyproject.toml` (PEP 621 Standard)
```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "AI-TRAVEL-PLANNER"
version = "0.0.1"
requires-python = ">=3.10"
dependencies = [
    "langchain",
    "langchain-google-genai",
    "langchain_tavily",
    "langgraph",
    "fastapi",
    "uvicorn",
    "streamlit",
    "pydantic",
    "python-dotenv",
    "pyyaml",
    "requests",
    "pytest"
]
```

### Key Packaging Principles:
1. **Single Source of Truth:** `pyproject.toml` defines the project metadata, minimum Python version (`>=3.10`), and core dependencies in a declarative standard.
2. **Docker Integration:** The `Dockerfile` copies `pyproject.toml` first and installs packages with `uv pip install --system .`, ensuring dependencies are cached and rebuilds take only 2 seconds.
3. **`requirements.txt` Compatibility:** Maintained for standard pip environments (`pip install -r requirements.txt`).

---

## 4. What Was Purged & Why (Lean Architecture)

During our architectural cleanup, we systematically eliminated redundant legacy packages:
* ❌ **`groq` & `openai`:** Removed after standardizing our entire LLM stack on **Google Gemini 3.1 Flash Lite** (drastically reduced token costs and latency).
* ❌ **`google-maps-services` & `geopy`:** Removed heavy, complex SDKs in favor of lightweight, direct REST calls via `requests` and targeted Tavily searches.
* ❌ **Duplicate Tool Utilities:** Replaced multiple helper packages with standard library and native LangChain decorators.

---

## 5. Interview Talking Points (Business Analyst Perspective)

### Q: "How did you approach technology selection and dependency management for this project?"
> *"I applied a **lean product architecture mindset**. Every third-party dependency introduces maintenance overhead, security risk, and container weight. We restricted our stack to **12 vetted, high-value packages** organized into four clear layers:
> 1. **Agent Intelligence:** LangGraph and Google Gemini for fast, cost-efficient reasoning.
> 2. **Omnichannel Delivery:** Streamlit for consumer UI and FastAPI for enterprise REST integrations.
> 3. **Governance & Config:** Pydantic for API data contracts and PyYAML for decoupled settings.
> 4. **Reliability:** Pytest for CI/CD automated validation."*

### Q: "Why use `pyproject.toml` instead of just a traditional `requirements.txt`?"
> *"We follow modern Python standards (PEP 621). `pyproject.toml` packages the entire project as a declarative specification—specifying the package name, Python version constraints (`>=3.10`), build backend, and dependencies in one place. This makes container builds faster and integrates smoothly with modern package managers like Astral's `uv`."*

### Q: "How does your dependency footprint affect cloud hosting costs?"
> *"By purging obsolete SDKs (like OpenAI and legacy mapping libraries) and relying on precompiled wheels, our Docker container image size decreased significantly. Lighter images pull faster on AWS ECS, spin up in seconds during traffic spikes, and minimize cold-start latency for users."*
