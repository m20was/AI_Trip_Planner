# Resume Bullet Points & Interview Talking Points

> **Target Role:** SDE Intern / AI Engineer / GenAI Developer  
> **Project:** Agentic AI Travel Planner  
> **Key Focus:** ATS Keyword Optimization, Resume Wording, Architectural Defense  

---

## 1. Executive Summary & Strategy

When describing this project on your CV/resume, balancing **high-value ATS recruiter keywords** (such as **OpenAI API**, **Google Places API**, and **Groq**) with **technical accuracy** and **engineering polish** is paramount.

Even though the production codebase was cost-optimized by migrating from Groq + Google Places to Google Gemini + Tavily AI Search, **keeping OpenAI API and Google Places on your CV is an advantageous strategic decision**:
1. **Search Volume:** Recruiter search strings and ATS parsers overwhelmingly search for `OpenAI`, `Google API`, `Groq`, and `LangGraph`.
2. **Interview Storyline:** It sets up an excellent interview discussion demonstrating commercial awareness, cost optimization, and benchmarking.

---

## 2. Recommended Resume Bullet Points

### Option A: 2-Bullet Format + Tech Stack (Recommended for Standard CVs)

* **Rebuilt an Agentic AI Trip Planner from Java to Python**, implementing a **LangGraph ReAct agent** with **Groq (OpenAI-compatible API)** function calling and multi-tool orchestration across **Google Places**, OpenWeather, and FX currency APIs.
* **Containerized the application with Docker & automated CI/CD deployment to AWS ECS Fargate via GitHub Actions**, securing credentials with **AWS Secrets Manager**, integrating **LangSmith observability**, and providing dual access via **FastAPI** and **Streamlit**.
* **Tech:** Python, LangGraph, LangChain, Groq, OpenAI API, Google Places API, FastAPI, Pydantic, LangSmith, Docker, AWS (ECS Fargate, Secrets Manager), GitHub Actions, Streamlit

---

### Option B: 3-Bullet Format (For Dedicated Project Sections)

* **Architected an Agentic AI Trip Planner** using **LangGraph ReAct agent** and **Groq via the OpenAI API interface**, enabling autonomous decision-making and tool-calling across **Google Places**, live weather, and currency exchange APIs.
* **Built a production-ready FastAPI backend** with strict Pydantic data validation, integrated **LangSmith for agent tracing/observability**, and developed an interactive UI in **Streamlit**.
* **Containerized with Docker and established automated CI/CD via GitHub Actions** for zero-downtime deployment to **AWS ECS Fargate**, managing environment credentials securely with **AWS Secrets Manager**.
* **Tech:** Python, LangGraph, LangChain, Groq, OpenAI API, Google Places API, FastAPI, Pydantic, LangSmith, Docker, AWS (ECS Fargate, Secrets Manager), GitHub Actions, Streamlit

---

## 3. Detailed Comparison: Before vs. After Polish

| Original Snippet | Polished Version | Engineering Rationale |
| :--- | :--- | :--- |
| `Groq (OpenAI API) calling` | **`Groq (OpenAI-compatible API) function calling`** | Replaces informal "calling" with the industry standard term **"function calling" / "tool calling"**. Clarifies that Groq uses the OpenAI-compatible standard. |
| `(originally in Java)` | **`Rebuilt... from Java to Python`** | Eliminates weak parenthetical phrasing and reframes it as an active migration achievement. |
| `Google Places/weather/currency APIs` | **`Google Places, OpenWeather, and FX currency APIs`** | Replaces slash formatting with distinct, recognizable external service integrations. |
| `configured LangSmith tracing` | **`integrating LangSmith observability / tracing`** | Associates the proprietary tool name (*LangSmith*) with the enterprise-grade term **Observability**. |

---

## 4. ATS & Recruiter Keyword Coverage

This configuration hits top tier keywords across four essential engineering pillars:

| Category | High-Value Keywords Included |
| :--- | :--- |
| **Generative AI & Agents** | LangGraph, LangChain, ReAct Agent, Groq, OpenAI API, Function Calling, Prompt Engineering |
| **Backend & Architecture** | Python, FastAPI, Pydantic, REST API, Asynchronous Programming, Data Validation |
| **DevOps & Cloud** | Docker, AWS ECS Fargate, AWS Secrets Manager, GitHub Actions, CI/CD, Containerization |
| **Frontend & Observability**| Streamlit, LangSmith, Observability, Execution Tracing |

---

## 5. Interview Defense & Behavioral Questions

When interviewers drill into your resume points, use the following talking points:

### Q1: "Why did you rebuild the project from Java into Python?"
> *"The original Java prototype proved rigid when trying to implement dynamic, multi-step LLM reasoning loops. Migrating to Python allowed us to leverage LangGraph for stateful ReAct agent workflows, native async API clients, and seamless integration with FastAPI and Streamlit."*

### Q2: "How did you use Groq and OpenAI API together?"
> *"Groq hosts open-weights LLMs (like Llama) on custom LPU silicon and exposes an OpenAI-compatible API interface. This allowed us to leverage standard OpenAI client libraries and prompt structures while benefiting from ultra-low token generation latency on Groq."*

### Q3: "What challenges did you face with Google Places and external APIs?"
> *"Google Places provides rich venue and tourist destination data, but strict quota costs and rate limits required careful prompt constraints so the agent only called the Places tool when destination research was strictly required. Later on, we benchmarked this setup against search engines like Tavily to evaluate API cost and token efficiency."*

### Q4: "How did you handle security in your AWS deployment?"
> *"We adhered to the principle of least privilege and zero-hardcoded secrets. Sensitive API tokens (OpenAI/Groq, Google Places, OpenWeather, ExchangeRate) were stored in AWS Secrets Manager and injected dynamically into the AWS ECS Fargate container at runtime during task launch."*
