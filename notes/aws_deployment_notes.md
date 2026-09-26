# AWS Cloud Deployment & Migration Architecture Notes

> **Target Role:** Entry-Level Business Analyst (BA) / Analytics Consultant  
> **Infrastructure:** AWS ECS Fargate, Amazon ECR, AWS Secrets Manager, GitHub Actions  
> **Region:** `ap-southeast-2` (Sydney) | **Cluster:** `ai-planner-cluster`

---

## 1. Executive Summary & Migration Objective

As part of our product evolution, we migrated the AI Trip Planner's core intelligence layer:
* **From:** Groq LLM + Google Places API *(High cost, complex SDKs, strict rate limits)*
* **To:** **Google Gemini 3.1 Flash Lite + Tavily AI Search** *(Faster response times, rich multi-tool reasoning, lower API cost)*

This document outlines how to execute the cloud deployment update on **AWS ECS Fargate** with **zero downtime** and strict security governance.

---

## 2. Cloud Architecture Diagram

```
[Developer: git push master]
             |
             v
+-----------------------------+
|    GitHub Actions CI/CD     | (.github/workflows/aws.yml)
+--------------+--------------+
               |
        1. Build & Push Image
               |
               v
+-----------------------------+
|     Amazon ECR Registry     | (ai-trip-planner:latest)
+--------------+--------------+
               |
        2. Deploy Task Def
               |
               v
+-----------------------------+         3. Fetch Keys at Runtime
|       AWS ECS Fargate       |<=================================+
|     (ai-planner-service)    |                                  |
+--------------+--------------+                                  |
               |                                                 |
         Spins up tasks                               +--------------------+
               |                                      | AWS Secrets Manager|
               v                                      | (trip-planner-     |
+-----------------------------+                       |  secrets-k0FhkV)   |
|   Unified Docker Container  |                       +--------------------+
|  - Streamlit UI (Port 8501) |
|  - FastAPI REST (Port 8000) |
+-----------------------------+
```

---

## 3. Step-by-Step Migration Guide (Updating AWS Secrets)

### Why AWS Secrets Manager?
In enterprise security, **API keys must never be committed to Git or baked into Docker images**. Instead, AWS Secrets Manager securely stores the keys in an encrypted vault (`kms`), and ECS automatically injects them as environment variables into the container when it boots.

### Step 1: Update Keys in AWS Secrets Manager (AWS Console)
1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).
2. In the top-right navbar, select Region: **Asia Pacific (Sydney) `ap-southeast-2`**.
3. Navigate to **Secrets Manager** $\rightarrow$ Click **`trip-planner-secrets-k0FhkV`**.
4. Scroll to **Secret value** $\rightarrow$ Click **Retrieve secret value** $\rightarrow$ Click **Edit**.
5. Update your key-value pairs:

| Action | Key Name | Value |
| :--- | :--- | :--- |
| ❌ **Delete** | `GROQ_API_KEY` | *(Remove old provider)* |
| ❌ **Delete** | `GOOGLE_MAPS_API_KEY` | *(Remove old provider)* |
| ❌ **Delete** | `OPENAI_API_KEY` | *(Remove if present)* |
| ✅ **Add/Keep** | `GEMINI_API_KEY` | `AIzaSy...` (from your `.env`) |
| ✅ **Add/Keep** | `TAVILY_API_KEY` | `tvly-...` (from your `.env`) |
| ✅ **Add/Keep** | `OPENWEATHERMAP_API_KEY` | `a1b2c3...` (from your `.env`) |
| ✅ **Add/Keep** | `EXCHANGE_RATE_API_KEY` | `d4e5f6...` (from your `.env`) |
| ✅ **Add/Keep** | `LANGCHAIN_API_KEY` | `lsv2_pt_...` (or leave empty) |
| ✅ **Add/Keep** | `LANGCHAIN_TRACING_V2` | `true` (or `false`) |

6. Click **Save**.

---

### Step 2: Trigger Automated CI/CD Deployment via Git

Your local [`.aws/task-definition.json`](file:///d:/Workspace/workspace/Analytics/apps/AI_Trip_Planner/.aws/task-definition.json) and [`.github/workflows/aws.yml`](file:///d:/Workspace/workspace/Analytics/apps/AI_Trip_Planner/.github/workflows/aws.yml) are already pre-configured with the new keys.

Run in your terminal:
```bash
git add .
git commit -m "Deploy updated Gemini 3.1 Flash-Lite architecture to AWS ECS"
git push origin master
```

---

### Step 3: Access the Live Application on AWS ECS

Once the deployment finishes and the ECS Fargate task enters `RUNNING` status:

1. **Locate the Running Task:**
   - In AWS Console $\rightarrow$ **Amazon ECS** $\rightarrow$ **Clusters** $\rightarrow$ **`ai-planner-cluster`**.
   - Click the **Services** tab $\rightarrow$ select **`ai-planner-service`**.
   - Click the **Tasks** tab and select the active running task.

2. **Step 2: Copy the Public IP & Add `:8501`:**
   - On the task page, look under the **Networking** section for **Public IP**.
   - Copy the IP address (for example, if it is `16.176.147.145` or `13.236.80.218`).
   - Open a new tab in your web browser and enter:
     ```text
     http://<YOUR_PUBLIC_IP>:8501
     ```
     *(For example: `http://16.176.147.145:8501`)*

> [!NOTE]
> Make sure to type `http://` (not `https://`), followed by `:8501`.

### Visual Verification & Deployment Proof

| AWS ECS Fargate Task Configuration (`RUNNING`) | Live Application Deployed on AWS ECS |
| :---: | :---: |
| ![AWS ECS Fargate Task Configuration](../docs/AWS%20ECS.png) | ![Live Deployed Application on AWS](../docs/AWS%20Final%20Deploy.png) |

---



## 4. How the CI/CD Pipeline Works (`.github/workflows/aws.yml`)

1. **Authentication:** Authenticates to AWS using GitHub repository secrets (`AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`).
2. **ECR Login:** Logs into Amazon Elastic Container Registry (`566167302601.dkr.ecr.ap-southeast-2.amazonaws.com`).
3. **Docker Build & Push:** Builds the multi-stage cached container image and tags it with the commit SHA (`git-sha`).
4. **Task Definition Registration:** Updates `.aws/task-definition.json` with the new ECR image URI.
5. **Zero-Downtime Rolling Update:** AWS ECS starts the new container task, verifies its health, routes traffic to it, and gracefully terminates the old task.

---

## 5. ECS Fargate Resource Sizing & Cost Optimization

| Metric | Allocated Value | Business Rationale |
| :--- | :--- | :--- |
| **Compute Engine** | AWS Fargate (Serverless) | Eliminates EC2 server management, OS patching, and idle capacity costs. |
| **CPU Allocation** | `256` (0.25 vCPU) | Perfectly sized for I/O-bound web processes and external API calls. |
| **Memory Allocation** | `512` (512 MB RAM) | Low memory footprint enabled by our lean 12-dependency Python environment. |
| **Estimated Cost** | ~$0.012 per hour | Highly cost-effective for portfolio hosting, small teams, and beta testing. |

---

## 6. Interview Talking Points (Business Analyst Perspective)

### Q: "How did you manage the cloud migration from Groq to Google Gemini on AWS?"
> *"I coordinated the migration using **AWS Secrets Manager, Amazon ECS Fargate, and GitHub Actions CI/CD**.  
> From a security and governance perspective, we decoupled credentials from the application code. In AWS Secrets Manager, we rotated out the legacy Groq and Google Places keys in favor of the new Gemini and Tavily credentials. Our CI/CD pipeline then executed a **zero-downtime rolling deployment**, replacing the old container task with the new Gemini engine without impacting active users."*

### Q: "Why choose AWS Fargate instead of a traditional EC2 virtual machine?"
> *"As a Business Analyst, I evaluate technology based on **Total Cost of Ownership (TCO) and operational overhead**. With traditional EC2, engineering teams spend hours patching Linux operating systems and configuring auto-scaling groups. Fargate is serverless container compute—AWS handles underlying hardware management, and we only pay for the exact CPU and memory consumed while our container runs."*

### Q: "How does the architecture comply with enterprise security standards?"
> *"We follow the **Principle of Least Privilege and Zero Secret Leaks**:  
> 1. No API keys or passwords are ever stored in GitHub or container images.  
> 2. The container's IAM execution role (`ecsTaskExecutionRole`) is strictly scoped to read only our specific secret ARN (`trip-planner-secrets-k0FhkV`).  
> 3. Secrets are injected into container memory only at boot time, preventing unauthorized external access."*
