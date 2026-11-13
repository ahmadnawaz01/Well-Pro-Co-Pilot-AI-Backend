# WellPro Intelligence Service

<p align="center">
  <strong>AI-Powered Multimodal Wellbeing Intelligence & Personal Assistant</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" />
  <img src="https://img.shields.io/badge/LangGraph-Agentic_AI-orange" />
  <img src="https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb" />
  <img src="https://img.shields.io/badge/Version-0.1.0-informational" />
</p>

---

## 1. Project Overview

**WellPro Intelligence Service** is an AI-powered backend service that acts as the intelligent processing layer of the WellPro Co-Pilot ecosystem.

It connects frontend applications with AI models, Frappe ERPNext, and MongoDB Atlas to provide personalized wellbeing management through natural language, voice, images, and conversational AI.

The service transforms unstructured user information into structured wellbeing records, automatically sends extracted data to the Frappe backend, and recalculates wellbeing scores.

It also provides a persistent AI chatbot that can retrieve historical records, analyze wellbeing trends, configure personalized goals, and perform approved CRUD operations through predefined tools.

### Core Objectives

- Multimodal AI-powered data ingestion.
- Natural language understanding and structured information extraction.
- Automated health, financial, and social record management.
- Personalized AI conversational assistant.
- Secure integration with Frappe ERPNext.
- Persistent conversation history using MongoDB.
- Automated wellbeing score recalculation.
- Personalized wellbeing goals and analytics.

---

## 2. Key Features

### 2.1 Multimodal AI Ingestion

Users can provide information through multiple input formats.

| Input Type | Technology | Function |
|---|---|---|
| Text | LLM | Natural language extraction |
| Audio | Groq Whisper | Speech transcription and translation |
| Images | OpenRouter Vision | OCR and visual information extraction |
| JSON | FastAPI | Direct structured record insertion |

The ingestion pipeline:

1. Receives text, audio, or image input.
2. Authenticates the user through Frappe.
3. Processes the input using the appropriate AI provider.
4. Extracts relevant wellbeing information.
5. Converts the information into structured JSON.
6. Validates extracted records.
7. Classifies records into the appropriate wellbeing domains.
8. Dispatches records to Frappe.
9. Automatically recalculates affected daily wellbeing scores.
10. Logs processing information in MongoDB.

### 2.2 Persistent AI Conversational Assistant

The WellPro AI Copilot uses Gemini, LangGraph, and MongoDB Checkpointer.

The assistant supports:

- Natural language conversations.
- Historical wellbeing record retrieval.
- Health, financial, and social data analysis.
- Dashboard metrics and trend analysis.
- Creating new records.
- Updating existing records.
- Deleting permitted records.
- Configuring personalized scoring goals.
- Recalculating wellbeing scores.
- Persistent conversation memory.

### 2.3 Universal Record Ingestion

The `/records/insert` endpoint supports:

- Multiple DocTypes in one request.
- Single record insertion.
- Batch record insertion.
- Multiple wellbeing domains.
- Automatic score recalculation.

### 2.4 Automatic Wellbeing Score Recalculation

Whenever a record is inserted, updated, or deleted through the supported record operations, the backend triggers score recalculation for affected dates.

The system calculates:

- Health Score (0–100).
- Financial Score (0–100).
- Social Score (0–100).
- Overall Wellbeing Score (0–100).
- Confidence percentages.
- Historical wellbeing trends.

### 2.5 Personalized Goals

Users can configure personalized targets, including:

- Daily steps.
- Financial budget.
- Savings rate.
- Water intake.
- Exercise duration.
- Sleep duration.
- Sleep quality.

Human-friendly values such as `12k`, `$3,500`, `25%`, and `3L` are supported by the goal configuration endpoint.

---

## 3. System Architecture

```text
                 FRONTEND APPLICATION
                   Web / Mobile
                        |
                        | HTTP REST / JSON
                        |
                        v
             WELLPRO INTELLIGENCE SERVICE
                    FastAPI
                        |
              Authentication Middleware
                        |
               Frappe Session Verification
                        |
             +----------+-----------+
             |                      |
             v                      v
       DATA INGESTION          AI CHAT AGENT
             |                      |
      +------+------+          Gemini LLM
      |      |      |               |
     Text  Audio  Image         LangGraph
      |      |      |               |
      |    Groq  OpenRouter      Agent Tools
      |   Whisper   Vision          |
      +------+------+---------------+
             |
      Structured Extraction
             |
       Pydantic Validation
             |
       Frappe API Integration
             |
             v
         FRAPPE ERP
             |
       +-----+-----+------+
       |           |      |
     Health     Finance  Social
       |           |      |
       +-----+-----+------+
             |
       Score Recalculation
             |
       Dashboard Analytics

             MONGODB ATLAS
                    |
          +---------+---------+
          |         |         |
         Users  Conversations Messages
          |
     User Mapping
     Chat History
     Agent Checkpoints

             LANGSMITH
                  |
          LLM Observability
```

### Technology Responsibilities

| Technology | Responsibility |
|---|---|
| FastAPI | Main backend and REST API |
| Frappe ERPNext v15 | Authentication, primary data storage, scoring |
| MongoDB Atlas | Conversation history, user mapping, checkpoints |
| Google Gemini | Conversational AI |
| Groq | Audio transcription and AI processing |
| OpenRouter | Image understanding and OCR |
| LangGraph | Agent workflow orchestration |
| LangChain | LLM integration |
| LangSmith | AI tracing and monitoring |
| Pydantic | Data validation |

---

## 4. Environment Configuration

The application uses environment variables for server settings, external services, AI providers, and database connections.

Create a `.env` file in the project root.

### Complete `.env.example`

```env
# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

PROJECT_NAME="WellPro Intelligence Service"
VERSION="0.1.0"
API_V1_STR="/api/v1"

# ==========================================
# SERVER CONFIGURATION
# ==========================================

PORT=8080
LOG_LEVEL=info

# ==========================================
# FRAPPE BACKEND CONFIGURATION
# ==========================================

FRAPPE_BASE_URL="https://your-frappe-instance.example.com"

# ==========================================
# MONGODB ATLAS CONFIGURATION
# ==========================================

MONGODB_URL="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/"
MONGODB_DB_NAME="wellpro_db"

# ==========================================
# GEMINI LLM CONFIGURATION
# ==========================================

GEMINI_API_KEY="YOUR_DEMO_GEMINI_API_KEY"

# ==========================================
# GROQ AI CONFIGURATION
# ==========================================

GROQ_API_KEY="YOUR_DEMO_GROQ_API_KEY"

# ==========================================
# LANGSMITH OBSERVABILITY
# ==========================================

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="YOUR_DEMO_LANGSMITH_API_KEY"
LANGSMITH_PROJECT="wellpro-co-pilot"

# ==========================================
# OPENROUTER VISION CONFIGURATION
# ==========================================

OPENROUTER_API_KEY="YOUR_DEMO_OPENROUTER_API_KEY"
OPENROUTER_VISION_MODEL="openrouter/free"
```

**Note:** All credentials above are demonstration placeholders. Replace them with your own credentials in the local `.env` file.

### Environment Variable Reference

| Variable | Description |
|---|---|
| PROJECT_NAME | Application name |
| VERSION | Application version |
| API_V1_STR | API version prefix |
| PORT | FastAPI server port |
| LOG_LEVEL | Application logging level |
| FRAPPE_BASE_URL | Frappe backend URL |
| MONGODB_URL | MongoDB Atlas connection string |
| MONGODB_DB_NAME | MongoDB database name |
| GEMINI_API_KEY | Google Gemini API key |
| GROQ_API_KEY | Groq API key |
| LANGSMITH_TRACING | Enable or disable tracing |
| LANGSMITH_ENDPOINT | LangSmith API endpoint |
| LANGSMITH_API_KEY | LangSmith API key |
| LANGSMITH_PROJECT | LangSmith project identifier |
| OPENROUTER_API_KEY | OpenRouter API key |
| OPENROUTER_VISION_MODEL | Vision model identifier |

---

## 5. Installation and Setup

### Prerequisites

- Python 3.11 or newer.
- Git.
- MongoDB Atlas account.
- Frappe ERPNext backend.
- Gemini API key.
- Groq API key.
- OpenRouter API key.
- LangSmith account (optional).

### Step 1: Clone Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd wellpro-intelligence-service
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create your local environment file:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Update the `.env` file with your actual credentials.

### Step 5: Configure MongoDB Atlas

1. Create a MongoDB Atlas cluster.
2. Create a database user.
3. Configure network access.
4. Copy your MongoDB connection string.
5. Add the connection string to `MONGODB_URL`.
6. Set the database name to `wellpro_db`.

### Step 6: Configure Frappe Backend

Update:

```env
FRAPPE_BASE_URL="https://your-frappe-instance.example.com"
```

Ensure that the Frappe backend is running and its API endpoints are accessible.

### Step 7: Start FastAPI Server

Assuming the application entry point is `app.main:app`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Application:

```text
http://localhost:8080
```

Swagger Documentation:

```text
http://localhost:8080/docs
```

ReDoc:

```text
http://localhost:8080/redoc
```

The application entry point and documentation routes must match the actual implementation.

---

# 6. API Documentation

## Base URL

Local development:

```text
http://localhost:8000/api/v1
```

Production:

```text
https://your-domain.com/api/v1
```

The FastAPI service runs on port `8080` according to the current environment configuration. Port `8000` above is the base URL shown in the supplied API integration guide; use the actual deployed port when configuring the frontend.

## 6.1 Authentication and Request Headers

All protected endpoints require Frappe API token authentication.

### Authorization Header

```http
Authorization: token <api_key>:<api_secret>
Content-Type: application/json
```

The signup and login endpoints return API credentials.

Use those credentials for subsequent protected requests.

**Important:** Never expose API secrets in frontend logs, public repositories, or client-side source code. For production, use an appropriate secure authentication architecture.

---

## 7. DocTypes and Data Models

The following DocTypes are used by the WellPro Frappe backend.

| DocType | Primary Date Field | Description |
|---|---|---|
| Health Daily Record | `record_date` | Steps, sleep, water, calories, protein and energy |
| Health Activity | `logged_at` | Running, walking, cycling, gym and workouts |
| Financial Transaction | `transaction_date` | Income, expenses, transfers and investments |
| Financial Snapshot | `snapshot_date` | Balances, savings, emergency funds and debt |
| Social Activity | `logged_at` | Social interactions and relationship quality |
| Subjective Wellbeing Checkin | `date` | Mood, energy, stress and social connection |
| Wellbeing Daily Score | `score_date` | Computed domain and overall scores |
| User Consent Preference | `consent_updated_at` | AI and tracking permissions |
| WellPro Profile | `creation` | User preferences and scoring goals |

---

# 8. Authentication Endpoints

Base path:

```text
/api/v1/auth
```

## 8.1 POST `/auth/signup`

Registers a new user, initializes their WellPro Profile and Consent records, and generates API credentials.

**URL**

```http
POST /api/v1/auth/signup
```

**Authentication:** Not required.

**Request JSON**

```json
{
  "email": "sarah.connor@example.com",
  "password": "SecurePassword123!",
  "first_name": "Sarah",
  "last_name": "Connor"
}
```

| Field | Type | Required |
|---|---|---|
| email | string | Yes |
| password | string | Yes |
| first_name | string | No |
| last_name | string | No |

**Success Response – HTTP 201**

```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": "sarah.connor@example.com",
    "api_key": "<demo_api_key>",
    "api_secret": "<demo_api_secret>"
  }
}
```

## 8.2 POST `/auth/login`

Authenticates an existing user and returns API credentials.

**URL**

```http
POST /api/v1/auth/login
```

**Authentication:** Not required.

**Request JSON**

```json
{
  "usr": "sarah.connor@example.com",
  "pwd": "SecurePassword123!"
}
```

Alternatively:

```json
{
  "email": "sarah.connor@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response – HTTP 200**

```json
{
  "success": true,
  "message": "Authentication successful",
  "data": {
    "user": "sarah.connor@example.com",
    "api_key": "<demo_api_key>",
    "api_secret": "<demo_api_secret>"
  }
}
```

## 8.3 GET / POST `/auth/verify-session`

Validates the current Frappe session and retrieves the user's profile and consent configuration.

**URL**

```http
GET /api/v1/auth/verify-session
```

**Alternative method:** POST.

**Authentication:** Required.

**Request Body:** None.

**Success Response – HTTP 200**

```json
{
  "success": true,
  "message": "Session valid",
  "data": {
    "user": "sarah.connor@example.com",
    "profile": {
      "name": "sarah.connor@example.com",
      "user": "sarah.connor@example.com",
      "preferred_currency": "USD",
      "timezone": "UTC",
      "health_tracking_enabled": 1,
      "financial_tracking_enabled": 1,
      "social_tracking_enabled": 1,
      "custom_scoring_goals": {
        "steps_target": 12000,
        "water_liters_target": 3.0
      }
    },
    "consent": {
      "user": "sarah.connor@example.com",
      "allow_ai_processing": 1,
      "allow_voice_logging": 1,
      "allow_document_ocr": 1,
      "health_tracking_enabled": 1,
      "financial_tracking_enabled": 1,
      "social_tracking_enabled": 1
    }
  }
}
```

---

# 9. Records CRUD and Query Endpoints

Base path:

```text
/api/v1/records
```

These endpoints provide direct access to wellbeing records stored in Frappe.

## 9.1 POST `/records/insert` – Universal Ingestion

The primary record insertion endpoint.

It supports multiple DocTypes, individual records, and batch records in one request.

It also automatically recalculates wellbeing scores for affected dates.

**URL**

```http
POST /api/v1/records/insert
```

**Authentication:** Required.

**Content-Type:** `application/json`

### Format A: Multiple DocTypes (Recommended)

```json
{
  "Health Daily Record": {
    "record_date": "2026-10-30",
    "steps": 9200,
    "sleep_hours": 7.5,
    "sleep_quality": 4,
    "water_liters": 2.5,
    "calories_consumed": 2100,
    "protein_grams": 80,
    "energy_level": 4
  },
  "Financial Transaction": [
    {
      "transaction_date": "2026-10-30",
      "amount": 14.50,
      "category": "Coffee & Snacks",
      "transaction_type": "Expense",
      "payment_method": "Card"
    },
    {
      "transaction_date": "2026-10-30",
      "amount": 45.00,
      "category": "Groceries",
      "transaction_type": "Expense",
      "essentiality": "Essential"
    }
  ],
  "Social Activity": {
    "logged_at": "2026-10-30 13:00:00",
    "interaction_type": "In Person",
    "relationship_type": "Colleague",
    "interaction_quality": 4,
    "connection_level": 4,
    "notes": "Team lunch"
  },
  "Subjective Wellbeing Checkin": {
    "date": "2026-10-30",
    "mood": 4,
    "energy": 4,
    "stress": 2,
    "social_connection": 4
  }
}
```

### Format B: Single Record

```json
{
  "doctype": "Financial Transaction",
  "record_data": {
    "amount": 28.50,
    "category": "Pharmacy",
    "transaction_type": "Expense",
    "transaction_date": "2026-10-30"
  }
}
```

### Format C: Batch Array

```json
[
  {
    "doctype": "Health Activity",
    "record_data": {
      "activity_type": "Running",
      "logged_at": "2026-10-30 07:30:00",
      "duration_minutes": 35,
      "distance_km": 5.2,
      "calories_burned": 340
    }
  }
]
```

### Success Response – HTTP 200

```json
{
  "success": true,
  "message": "Successfully created 5 records",
  "data": {
    "count": 5,
    "affected_dates": [
      "2026-10-30"
    ],
    "created": [
      {
        "index": 0,
        "doctype": "Health Daily Record",
        "name": "HDR-00042",
        "affected_date": "2026-10-30",
        "record": {}
      }
    ],
    "recalculated_scores": {
      "2026-10-30": {
        "name": "SCORE-USER-2026-10-30",
        "score_date": "2026-10-30",
        "health_score": 84.5,
        "health_confidence": 75.0,
        "financial_score": 79.2,
        "financial_confidence": 70.0,
        "social_score": 80.0,
        "social_confidence": 85.0,
        "overall_score": 81.2,
        "scoring_version": "v1.0.0",
        "calculated_at": "2026-10-30 12:45:10"
      }
    }
  }
}
```

*The response is illustrative. Actual record names and calculated values depend on the submitted data.*

## 9.2 POST `/records/store-ai`

Dedicated endpoint for storing AI-extracted domain records.

Automatically injects the AI extraction source and recalculates affected scores.

**URL**

```http
POST /api/v1/records/store-ai
```

**Authentication:** Required.

**Request JSON**

```json
{
  "health": {
    "record_date": "2026-10-30",
    "steps": 10000,
    "sleep_hours": 8.0,
    "water_liters": 2.5
  },
  "financial": [
    {
      "amount": 12.00,
      "category": "Lunch",
      "transaction_type": "Expense",
      "transaction_date": "2026-10-30"
    }
  ],
  "social": {
    "logged_at": "2026-10-30 20:00:00",
    "interaction_type": "In Person",
    "relationship_type": "Family",
    "interaction_quality": 5,
    "notes": "Dinner with family"
  }
}
```

**Success Response**

```json
{
  "success": true,
  "message": "Successfully processed 3 AI domain extractions",
  "data": {
    "count": 3,
    "affected_dates": [
      "2026-10-30"
    ],
    "created": [],
    "recalculated_scores": {
      "2026-10-30": {
        "health_score": 88.0,
        "financial_score": 82.0,
        "social_score": 90.0,
        "overall_score": 86.4
      }
    }
  }
}
```

## 9.3 GET `/records` – Retrieve Records

Retrieves paginated records for the authenticated user.

**URL**

```http
GET /api/v1/records
```

**Authentication:** Required.

### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| doctype | string | Yes | - | Frappe DocType |
| limit | integer | No | 50 | Maximum records (up to 200) |
| offset | integer | No | 0 | Pagination offset |
| order_by | string | No | - | Sorting order |
| from_date | string | No | - | Starting date |
| to_date | string | No | - | Ending date |

**Example**

```http
GET /api/v1/records?doctype=Financial%20Transaction&limit=20&offset=0&order_by=transaction_date%20desc
```

## 9.4 POST `/records/query` – Query Records

Retrieves records using a JSON request instead of query parameters.

**URL**

```http
POST /api/v1/records/query
```

**Request JSON**

```json
{
  "doctype": "Financial Transaction",
  "limit": 20,
  "offset": 0,
  "order_by": "transaction_date desc",
  "from_date": "2026-10-01",
  "to_date": "2026-10-30"
}
```

**Success Response**

```json
{
  "success": true,
  "data": [
    {
      "name": "FT-00110",
      "user": "sarah.connor@example.com",
      "amount": 45.0,
      "category": "Groceries",
      "transaction_type": "Expense",
      "transaction_date": "2026-10-30",
      "payment_method": "Card",
      "essentiality": "Essential"
    }
  ],
  "count": 1,
  "limit": 20,
  "offset": 0
}
```

## 9.5 POST / PUT `/records/update`

Updates an existing record using its DocType and document name.

Automatically recalculates scores for the original date and the updated date when the record date changes.

**URL**

```http
POST /api/v1/records/update
```

**Alternative method:** PUT.

**Authentication:** Required.

**Request JSON**

```json
{
  "doctype": "Health Daily Record",
  "name": "HDR-00042",
  "update_data": {
    "water_liters": 3.2,
    "sleep_quality": 5,
    "steps": 10500
  }
}
```

**Success Response**

```json
{
  "success": true,
  "message": "Health Daily Record updated successfully",
  "data": {
    "name": "HDR-00042",
    "doctype": "Health Daily Record",
    "water_liters": 3.2,
    "sleep_quality": 5,
    "steps": 10500
  }
}
```

## 9.6 POST / DELETE `/records/delete`

Deletes a record owned by the authenticated user.

Triggers recalculation for the affected date.

**URL**

```http
POST /api/v1/records/delete
```

**Alternative method:** DELETE.

**Authentication:** Required.

**Request JSON**

```json
{
  "doctype": "Financial Transaction",
  "name": "FT-00109"
}
```

**Success Response**

```json
{
  "success": true,
  "message": "Financial Transaction deleted successfully",
  "data": {
    "doctype": "Financial Transaction",
    "name": "FT-00109"
  }
}
```

---

# 10. Dashboard and Analytics Endpoints

Base path:

```text
/api/v1/dashboard
```

## 10.1 GET / POST `/dashboard/metrics`

The main dashboard analytics endpoint.

It retrieves current scores, confidence values, historical trends, multi-window wellbeing summaries, and recent user records.

### Supported Analytics

- Current daily scores.
- Health, financial, and social scores.
- Overall wellbeing score.
- Score confidence percentages.
- Seven-day weighted scores.
- Thirty-day weighted scores.
- Ninety-day weighted scores.
- Historical trend timeline.
- Recent health records.
- Recent financial transactions.
- Recent health activities.
- Recent social activities.
- Subjective check-ins.

**GET URL**

```http
GET /api/v1/dashboard/metrics?days=30&as_of_date=2026-10-30
```

### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| days | integer | No | 30 | Timeline period (1–365) |
| as_of_date | string | No | Today | Evaluation date |

**Alternative POST URL**

```http
POST /api/v1/dashboard/metrics
```

**POST Request JSON**

```json
{
  "days": 30,
  "as_of_date": "2026-10-30"
}
```

**Success Response**

```json
{
  "success": true,
  "message": "Dashboard metrics retrieved successfully",
  "data": {
    "as_of_date": "2026-10-30",
    "days": 30,
    "current_scores": {
      "name": "SCORE-SARAH-2026-10-30",
      "score_date": "2026-10-30",
      "health_score": 84.5,
      "health_confidence": 75.0,
      "financial_score": 79.2,
      "financial_confidence": 70.0,
      "social_score": 80.0,
      "social_confidence": 85.0,
      "overall_score": 81.2,
      "scoring_version": "v1.0.0"
    },
    "summary": {
      "health": {
        "today_score": 84.5,
        "current_score": 82.1,
        "confidence": 78.0,
        "seven_day_score": 83.0,
        "thirty_day_score": 82.1,
        "ninety_day_score": 80.5,
        "trend": "improving",
        "trend_change": 2.4
      },
      "financial": {
        "today_score": 79.2,
        "current_score": 77.0,
        "confidence": 72.0,
        "seven_day_score": 78.1,
        "thirty_day_score": 77.0,
        "ninety_day_score": 75.0,
        "trend": "stable",
        "trend_change": 0.5
      },
      "social": {
        "today_score": 80.0,
        "current_score": 79.5,
        "confidence": 80.0,
        "seven_day_score": 80.0,
        "thirty_day_score": 79.5,
        "ninety_day_score": 78.0,
        "trend": "improving",
        "trend_change": 1.2
      },
      "overall": {
        "today_score": 81.2,
        "score": 79.8,
        "seven_day_score": 80.5,
        "thirty_day_score": 79.8,
        "ninety_day_score": 78.1,
        "trend": "improving",
        "trend_change": 1.5
      }
    },
    "historical_trends": [
      {
        "score_date": "2026-10-28",
        "health_score": 80.0,
        "financial_score": 76.0,
        "social_score": 78.0,
        "overall_score": 78.2
      },
      {
        "score_date": "2026-10-29",
        "health_score": 82.0,
        "financial_score": 78.0,
        "social_score": 79.0,
        "overall_score": 79.8
      },
      {
        "score_date": "2026-10-30",
        "health_score": 84.5,
        "financial_score": 79.2,
        "social_score": 80.0,
        "overall_score": 81.2
      }
    ],
    "financial": [],
    "health": [],
    "health_activities": [],
    "social": [],
    "checkins": []
  }
}
```

The empty arrays above represent placeholders for the recent record collections.

## 10.2 POST `/dashboard/recalculate-score`

Explicitly recalculates daily wellbeing scores for a specified date.

**URL**

```http
POST /api/v1/dashboard/recalculate-score
```

**Authentication:** Required.

**Request JSON**

```json
{
  "date": "2026-10-30"
}
```

If the date is omitted, the endpoint defaults to today.

**Success Response**

```json
{
  "success": true,
  "message": "Score recalculated successfully",
  "data": {
    "name": "SCORE-SARAH-2026-10-30",
    "score_date": "2026-10-30",
    "health_score": 84.5,
    "health_confidence": 75.0,
    "financial_score": 79.2,
    "financial_confidence": 70.0,
    "social_score": 80.0,
    "social_confidence": 85.0,
    "overall_score": 81.2
  }
}
```

---

# 11. Scoring Goals Configuration

Base path:

```text
/api/v1/goals
```

## 11.1 POST `/goals/setup`

Configures personalized wellbeing scoring targets.

Supports human-readable values and raw numerical values.

**URL**

```http
POST /api/v1/goals/setup
```

**Authentication:** Required.

### Supported Goal Examples

| Goal | Example |
|---|---|
| Steps | `12k` |
| Financial budget | `$3,500` |
| Savings rate | `25%` |
| Water intake | `3L` |
| Exercise minutes | `45` |
| Sleep duration | `8` |
| Sleep quality | `4` |

**Request JSON**

```json
{
  "goals": {
    "steps": "12k",
    "financial_budget": "$3,500",
    "savings_rate": "25%",
    "water": "3L",
    "exercise_minutes": 45
  },
  "recalculate": true
}
```

**Success Response**

```json
{
  "success": true,
  "message": "Scoring goals updated and converted to config scale successfully",
  "data": {
    "configured_goals": {
      "steps_target": 12000,
      "budget_amount": 3500.0,
      "target_savings_rate": 0.25,
      "water_liters_target": 3.0,
      "exercise_minutes_target": 45
    },
    "recalculated_score": {
      "health_score": 85.0,
      "financial_score": 80.0,
      "social_score": 80.0,
      "overall_score": 81.8
    }
  }
}
```

The `recalculate` field determines whether scoring is recalculated after goal configuration.

## 11.2 GET / POST `/goals`

Retrieves the effective user-specific scoring goals merged with system defaults.

**URL**

```http
GET /api/v1/goals
```

**Alternative method:** POST.

**Authentication:** Required.

**Success Response**

```json
{
  "success": true,
  "data": {
    "steps_target": 12000,
    "budget_amount": 3500.0,
    "target_savings_rate": 0.25,
    "water_liters_target": 3.0,
    "exercise_minutes_target": 45,
    "sleep_hours_target": 8.0,
    "sleep_quality_target": 4
  }
}
```

---

# 12. AI Multimodal Ingestion Endpoints

Base path:

```text
/api/v1/ingest
```

These endpoints process unstructured user input and automatically dispatch extracted records to Frappe.

## 12.1 POST `/ingest/process-text`

Extracts structured wellbeing information from natural language using Gemini and the configured extraction pipeline.

**URL**

```http
POST /api/v1/ingest/process-text
```

**Authentication:** Required.

**Content-Type:** `application/json`

### Request JSON

```json
{
  "raw_text": "Slept 7.5 hours last night with great sleep quality. Walked 8500 steps today, drank 2.5 liters of water. Bought a $12 salad for lunch, and had a 45 minute video call with my sister."
}
```

### Success Response

```json
{
  "status": "success",
  "user_email": "sarah.connor@example.com",
  "extracted_count": 3,
  "extracted_records": [
    {
      "doctype": "Health Daily Record",
      "domain": "health",
      "record_data": {
        "record_date": "2026-10-30",
        "sleep_hours": 7.5,
        "sleep_quality": 4,
        "steps": 8500,
        "water_liters": 2.5,
        "source": "AI Extraction"
      }
    },
    {
      "doctype": "Financial Transaction",
      "domain": "financial",
      "record_data": {
        "amount": 3336.0,
        "category": "Dining & Lunch",
        "transaction_type": "Expense",
        "transaction_date": "2026-10-30",
        "source": "AI Extraction"
      }
    },
    {
      "doctype": "Social Activity",
      "domain": "social",
      "record_data": {
        "logged_at": "2026-10-30 14:00:00",
        "interaction_type": "Video Call",
        "relationship_type": "Family",
        "duration_minutes": 45.0,
        "interaction_quality": 5,
        "notes": "Video call with sister",
        "source": "AI Extraction"
      }
    }
  ],
  "frappe_dispatch_results": [],
  "recalculated_scores": {},
  "mongo_log_id": "67220cf01a4e98f45a19bb01",
  "validation_error": null
}
```

The response values are illustrative. The actual currency conversion and extracted fields depend on the input, user preferences, and backend implementation.

## 12.2 POST `/ingest/process-audio`

Accepts audio files in different languages.

Uses Groq Whisper (`whisper-large-v3`) for speech transcription and English translation before extracting wellbeing records.

**URL**

```http
POST /api/v1/ingest/process-audio
```

**Authentication:** Required.

**Content-Type:** `multipart/form-data`

### Supported Formats

- WAV
- MP3
- M4A
- OGG
- FLAC

### Form Data

| Field | Type | Required |
|---|---|---|
| file | Audio binary | Yes |

### Example cURL

```bash
curl -X POST \
  "http://localhost:8080/api/v1/ingest/process-audio" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -F "file=@voice.mp3"
```

### Success Response

```json
{
  "status": "success",
  "user_email": "sarah.connor@example.com",
  "transcribed_english_text": "I went for a 5 kilometer morning jog in 28 minutes, then spent 500 rupees on breakfast.",
  "is_relevant": true,
  "relevance_reason": "Contains health activity and financial transaction data.",
  "extracted_count": 2,
  "extracted_records": [
    {
      "doctype": "Health Activity",
      "domain": "activity",
      "record_data": {
        "activity_type": "Running",
        "logged_at": "2026-10-30 08:00:00",
        "distance_km": 5.0,
        "duration_minutes": 28.0
      }
    },
    {
      "doctype": "Financial Transaction",
      "domain": "financial",
      "record_data": {
        "amount": 500.0,
        "category": "Breakfast & Food",
        "transaction_type": "Expense",
        "transaction_date": "2026-10-30"
      }
    }
  ],
  "frappe_dispatch_results": [],
  "recalculated_scores": {},
  "mongo_log_id": "67220d1a1a4e98f45a19bb02"
}
```

## 12.3 POST `/ingest/process-image`

Accepts images such as:

- Shopping receipts.
- Medical reports.
- Activity photographs.
- Other relevant wellbeing documents.

Uses OpenRouter Vision for image understanding and OCR.

**URL**

```http
POST /api/v1/ingest/process-image
```

**Authentication:** Required.

**Content-Type:** `multipart/form-data`

### Supported Formats

- JPEG
- PNG
- WEBP

### Form Data

| Field | Type | Required |
|---|---|---|
| file | Image binary | Yes |

### Example cURL

```bash
curl -X POST \
  "http://localhost:8080/api/v1/ingest/process-image" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -F "file=@receipt.jpg"
```

### Success Response

```json
{
  "status": "success",
  "user_email": "sarah.connor@example.com",
  "extracted_ocr_text": "Walmart Supercenter\nDate: 2026-10-30\nTotal: $64.30",
  "is_relevant": true,
  "relevance_reason": "Valid store receipt containing expense transaction.",
  "extracted_count": 1,
  "extracted_records": [
    {
      "doctype": "Financial Transaction",
      "domain": "financial",
      "record_data": {
        "amount": 17875.4,
        "category": "Groceries",
        "transaction_type": "Expense",
        "transaction_date": "2026-10-30",
        "payment_method": "Card",
        "merchant_or_source": "Walmart Supercenter"
      }
    }
  ],
  "frappe_dispatch_results": [],
  "recalculated_scores": {},
  "mongo_log_id": "67220d3f1a4e98f45a19bb03"
}
```

## 12.4 POST `/ingest/insert-record`

Direct JSON shortcut for universal record insertion.

Accepts the same payload formats as:

```http
POST /api/v1/records/insert
```

## 12.5 POST `/ingest/store-ai-record`

Direct JSON shortcut for AI domain-based record insertion.

Accepts the same payload as:

```http
POST /api/v1/records/store-ai
```

Both shortcut endpoints require authentication.

---

# 13. Interactive AI Chatbot Endpoints

Base path:

```text
/api/v1/chat
```

The WellPro AI chatbot is a persistent, tool-enabled ReAct agent powered by Gemini and LangGraph with MongoDB Checkpointer.

It can query historical records, create and update documents, retrieve dashboard trends, recalculate scores, and configure goals.

## 13.1 POST `/chat/message`

Sends a user message to the AI Copilot.

**URL**

```http
POST /api/v1/chat/message
```

**Authentication:** Required.

### Request JSON

```json
{
  "message": "How many steps have I logged this week, and what is my current overall wellbeing score?",
  "session_id": "default"
}
```

### Request Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| message | string | Yes | User's conversational message |
| session_id | string | No | Conversation thread identifier; defaults to `default` |

### Success Response

```json
{
  "status": "success",
  "user_email": "sarah.connor@example.com",
  "session_id": "default",
  "response": "You have logged an average of 9,800 steps daily over the past 7 days! Your current overall wellbeing score is 81.2 (Health: 84.5, Financial: 79.2, Social: 80.0), which is currently trending upwards by 1.5 points."
}
```

## 13.2 GET `/chat/history`

Retrieves historical user and assistant messages for a conversation session.

Useful for restoring the chat interface after a page reload.

**URL**

```http
GET /api/v1/chat/history?session_id=default
```

**Authentication:** Required.

### Query Parameters

| Parameter | Type | Required | Default |
|---|---|---|---|
| session_id | string | No | default |

### Success Response

```json
{
  "status": "success",
  "user_email": "sarah.connor@example.com",
  "session_id": "default",
  "count": 2,
  "messages": [
    {
      "role": "user",
      "content": "How many steps have I logged this week?"
    },
    {
      "role": "assistant",
      "content": "You have logged an average of 9,800 steps daily over the past 7 days!"
    }
  ]
}
```

## 13.3 DELETE `/chat/clear`

Clears chat memory checkpoints for a given session thread.

**URL**

```http
DELETE /api/v1/chat/clear?session_id=default
```

**Authentication:** Required.

### Query Parameters

| Parameter | Type | Required | Default |
|---|---|---|---|
| session_id | string | No | default |

### Success Response

```json
{
  "status": "success",
  "message": "Chat history cleared for session 'default'.",
  "user_email": "sarah.connor@example.com"
}
```

---

# 14. System Endpoints

## 14.1 GET `/health`

Checks the availability of the WellPro Intelligence Service.

**URL**

```http
GET /health
```

**Authentication:** Not required.

### Success Response

```json
{
  "status": "online",
  "project": "WellPro Intelligence Service"
}
```

This endpoint can be used by monitoring systems, load balancers, and deployment platforms.

---

# 15. Complete API Endpoint Reference

The following table provides a quick reference for frontend developers.

| # | Method | Endpoint | Authentication |
|---|---|---|---|
| 1 | POST | `/api/v1/auth/signup` | Public |
| 2 | POST | `/api/v1/auth/login` | Public |
| 3 | GET / POST | `/api/v1/auth/verify-session` | Required |
| 4 | POST | `/api/v1/records/insert` | Required |
| 5 | POST | `/api/v1/records/store-ai` | Required |
| 6 | GET | `/api/v1/records` | Required |
| 7 | POST | `/api/v1/records/query` | Required |
| 8 | POST / PUT | `/api/v1/records/update` | Required |
| 9 | POST / DELETE | `/api/v1/records/delete` | Required |
| 10 | GET / POST | `/api/v1/dashboard/metrics` | Required |
| 11 | POST | `/api/v1/dashboard/recalculate-score` | Required |
| 12 | POST | `/api/v1/goals/setup` | Required |
| 13 | GET / POST | `/api/v1/goals` | Required |
| 14 | POST | `/api/v1/ingest/process-text` | Required |
| 15 | POST | `/api/v1/ingest/process-audio` | Required |
| 16 | POST | `/api/v1/ingest/process-image` | Required |
| 17 | POST | `/api/v1/ingest/insert-record` | Required |
| 18 | POST | `/api/v1/ingest/store-ai-record` | Required |
| 19 | POST | `/api/v1/chat/message` | Required |
| 20 | GET | `/api/v1/chat/history` | Required |
| 21 | DELETE | `/api/v1/chat/clear` | Required |
| 22 | GET | `/health` | Public |

---

# 16. Frontend Integration – TypeScript / Axios

The following example demonstrates how a frontend application can communicate with the WellPro backend.

### Install Axios

```bash
npm install axios
```

### API Client

```typescript
import axios, { AxiosInstance } from "axios";

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data: T;
  recalculated_scores?: Record<string, any>;
}

export class WellProClient {
  private client: AxiosInstance;

  constructor(
    baseURL: string,
    apiKey?: string,
    apiSecret?: string
  ) {
    this.client = axios.create({
      baseURL: `${baseURL}/api/v1`,
      headers: {
        "Content-Type": "application/json",
        ...(apiKey && apiSecret
          ? {
              Authorization: `token ${apiKey}:${apiSecret}`
            }
          : {})
      }
    });

    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        const detail =
          error.response?.data?.detail || error.message;

        return Promise.reject(new Error(detail));
      }
    );
  }

  // Authentication
  async signup(
    email: string,
    password: string,
    firstName?: string,
    lastName?: string
  ) {
    return this.client.post("/auth/signup", {
      email,
      password,
      first_name: firstName,
      last_name: lastName
    });
  }

  async login(email: string, password: string) {
    return this.client.post("/auth/login", {
      usr: email,
      pwd: password
    });
  }

  // Universal Record Ingestion
  async insertRecords(payload: Record<string, any>) {
    return this.client.post("/records/insert", payload);
  }

  // Text Ingestion
  async processText(rawText: string) {
    return this.client.post("/ingest/process-text", {
      raw_text: rawText
    });
  }

  // Audio Ingestion
  async processAudio(
    audioBlob: Blob,
    filename = "voice.mp3"
  ) {
    const formData = new FormData();

    formData.append("file", audioBlob, filename);

    return this.client.post(
      "/ingest/process-audio",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
    );
  }

  // Dashboard Analytics
  async getDashboardMetrics(
    days = 30,
    asOfDate?: string
  ) {
    return this.client.get("/dashboard/metrics", {
      params: {
        days,
        as_of_date: asOfDate
      }
    });
  }

  // Personalized Goals
  async setGoals(
    goals: Record<string, any>,
    recalculate = true
  ) {
    return this.client.post("/goals/setup", {
      goals,
      recalculate
    });
  }

  // AI Chatbot
  async sendChatMessage(
    message: string,
    sessionId = "default"
  ) {
    return this.client.post("/chat/message", {
      message,
      session_id: sessionId
    });
  }
}
```

### Initialize Client

```typescript
const wellPro = new WellProClient(
  "http://localhost:8080",
  "YOUR_API_KEY",
  "YOUR_API_SECRET"
);
```

**Production security:** The API key and secret must not be embedded in a public frontend bundle. Use a secure backend session or another protected credential exchange mechanism.

---

# 17. MongoDB Atlas Database

MongoDB Atlas provides the persistence layer for conversational AI and application-related metadata.

### Main Responsibilities

- User-to-Frappe identity mapping.
- Conversation metadata.
- Chat message history.
- LangGraph checkpoints.
- AI processing logs.

### Recommended Collections

| Collection | Purpose |
|---|---|
| users | Verified Frappe user mappings |
| conversations | Conversation metadata |
| messages | User and assistant messages |
| checkpoints | LangGraph conversation state |
| ingestion_logs | Processing and ingestion logs, if implemented |

### Recommended Indexes

```text
users:
  Unique index on frappe_user

conversations:
  Compound index on user_id and updated_at

messages:
  Compound index on conversation_id and created_at

checkpoints:
  Index according to LangGraph checkpoint requirements
```

Ensure that every conversation and message query enforces authenticated user ownership.

---

# 18. LangSmith Monitoring

LangSmith provides observability for AI and LangGraph workflows.

### Capabilities

- Track LLM calls.
- Inspect agent execution.
- Debug LangGraph workflows.
- Monitor tool invocations.
- Inspect extraction failures.
- Evaluate model outputs.

### Configuration

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_PROJECT="wellpro-co-pilot"
```

The LangSmith API key must be configured separately.

Avoid sending unnecessary personal, health, financial, or authentication information to external tracing services.

---

# 19. Security Guidelines

WellPro processes sensitive personal and financial information. Security must be enforced throughout the application.

### Authentication

- Verify all protected requests through Frappe.
- Never trust a frontend-provided user identity without verification.
- Enforce user ownership for records and conversations.
- Never expose API secrets in frontend source code.

### API Security

- Validate incoming request payloads.
- Restrict accessible DocTypes.
- Use Pydantic schemas.
- Restrict AI tools to approved operations.
- Apply appropriate request size limits.
- Use HTTPS in production.

### Database Security

- Use MongoDB Atlas credentials stored in environment variables.
- Restrict database network access.
- Enforce conversation ownership.
- Avoid storing unnecessary sensitive information.

### Environment Security

Never commit the following files:

```text
.env
.env.local
.env.production
```

Use `.env.example` for demonstration configuration.

### Recommended `.gitignore`

```gitignore
# Environment
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]

# Virtual environments
venv/
.venv/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

---

# 20. Deployment

The service can be deployed independently from the Frappe backend.

### Production Deployment Requirements

1. Configure production environment variables.
2. Use a production MongoDB Atlas connection.
3. Configure the production Frappe backend URL.
4. Configure all required AI provider credentials.
5. Run FastAPI using a production ASGI server configuration.
6. Enable HTTPS.
7. Configure CORS for trusted frontend domains.
8. Configure logging and monitoring.
9. Validate authentication and user ownership.
10. Test all API endpoints before release.

### Example Production Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

The actual module path must match the project entry point.

---

# 21. Development Workflow

### Recommended Branch Structure

```text
main
 |
 +--- develop
        |
        +--- feature/multimodal-ingestion
        |
        +--- feature/chat-agent
        |
        +--- feature/frappe-integration
        |
        +--- feature/dashboard-analytics
        |
        +--- bugfix/authentication
```

### Commit Convention

```text
feat: add multimodal ingestion
feat: implement Gemini conversational agent
feat: integrate Frappe authentication
feat: add persistent chat history
fix: resolve MongoDB ownership validation
fix: improve score recalculation
refactor: improve ingestion validation
docs: update API documentation
```

---

# 22. Future Enhancements

- Real-time AI response streaming.
- Advanced multimodal processing.
- Personalized wellbeing recommendations.
- More advanced agentic workflows.
- Predictive wellbeing analytics.
- Improved AI memory management.
- Automated wellbeing reports.
- Advanced financial insights.
- AI-powered health trend analysis.
- Production monitoring and evaluation.

---

# 23. License

Add the appropriate project license before distributing or publishing the repository.

---

<p align="center">
  <strong>WellPro Intelligence Service</strong>
  <br/>
  Intelligent Data Processing. Personalized Wellbeing. Secure AI Integration.
  <br/><br/>
  Built for the WellPro Co-Pilot Ecosystem.
</p>
