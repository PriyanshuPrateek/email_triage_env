---
title: Email Triage Environment
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_file: server/app.py
pinned: false
---

#  Email Triage Environment (RL-Ready)

A FastAPI-based simulation environment for intelligent email classification, prioritization, and response generation — designed for reinforcement learning and evaluation.

  Live Demo (Hugging Face Space):
https://prateek12345-email-env.hf.space/

---

##  Overview

This environment simulates real-world email handling tasks where an agent must:

* Classify emails (billing, technical, spam, etc.)
* Assign priority levels
* Choose an appropriate action (reply, ignore, escalate)
* Generate a response

It supports multi-level difficulty and reward-based scoring, making it ideal for RL and system design evaluation.

---

##  Task Levels

### 🟢 Easy

* Input: `category`
* Reward:

  * Correct → `1.0`
  * Wrong → `0.0`

---

### 🟡 Medium

* Input: `category`, `priority`
* Reward:

  * Category correct → `+0.6`
  * Priority correct → `+0.4`

---

### 🔴 Hard

* Input: `category`, `priority`, `action`, `response`
* Reward:

  * Category → `+0.3`
  * Priority → `+0.2`
  * Action → `+0.2`
  * Response (keyword match) → `+0.3`

---

## 📦 Requirements

* Python 3.10+
* FastAPI
* Uvicorn
* Pydantic
* Requests

---

## ⚙️ API Endpoints

### 🔹 Health

```http
GET /health
```

---

### 🔹 Reset

```http
POST /reset?task_type=easy|medium|hard
```

---

### 🔹 Step

```http
POST /step
```

Example:

```json
{
  "category": "billing",
  "priority": "high",
  "action": "reply",
  "response": "We will refund the extra charge."
}
```

---

### 🔹 Grader

```http
POST /grader?task_type=hard
```

Returns:

```json
{
  "task": "hard",
  "score": 0.76
}
```

---

### 🔹 Tasks

```http
GET /tasks
```

---

### 🔹 Baseline

```http
GET /baseline
```

---

## 🧪 Example Workflow

1. Reset environment:

```http
POST /reset?task_type=hard
```

2. Take action:

```json
{
  "category": "billing",
  "priority": "high",
  "action": "reply",
  "response": "We apologize and will refund the amount."
}
```

3. Receive reward:

```json
{
  "reward": 0.8,
  "done": true
}
```

---

##  OpenEnv Compatibility

This project includes an `openenv.yaml` file, making it compatible with **OpenEnv-style evaluation frameworks**.

This enables:

* Standardized RL benchmarking
* Plug-and-play agent evaluation
* Environment reproducibility

---

##  Deployment

Deployed using Docker on Hugging Face Spaces.

Server command:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

---

##  Project Structure

```
.
├── server/
│   ├── app.py
│   └── environment.py
├── model.py
├── email_dataset_fixed.json
├── Dockerfile
├── openenv.yaml
├── requirements.txt
└── README.md
```

---

##  Use Cases

* Reinforcement Learning environments
* AI email assistants
* ML system design practice
* Policy evaluation frameworks

---

##  Key Features

* Multi-level task difficulty
* Reward shaping (partial scoring)
* Realistic dataset
* API-first design
* OpenEnv compatible

---

