# 🚀 WellPro FastAPI Backend - Comprehensive Endpoints & Integration Guide

> **Version**: 2.0.0  
> **Base URL**: `http://localhost:8000/api/v1` (or your production deployment domain)  
> **Status**: Verified & Active  
> **Target Audience**: Frontend Engineers, Mobile Developers, AI Integration Engineers, Full-Stack Developers

---

## Table of Contents
1. [Architecture Overview & Core Concepts](#1-architecture-overview--core-concepts)
2. [Authentication & Request Headers](#2-authentication--request-headers)
3. [DocTypes & Data Models Reference](#3-doctypes--data-models-reference)
4. [Authentication Endpoints (`/auth`)](#4-authentication-endpoints-auth)
   - [4.1 POST `/auth/signup`](#41-post-authsignup)
   - [4.2 POST `/auth/login`](#42-post-authlogin)
   - [4.3 GET & POST `/auth/verify-session`](#43-get--post-authverify-session)
5. [Records CRUD & Query Endpoints (`/records`)](#5-records-crud--query-endpoints-records)
   - [5.1 POST `/records/insert` (Universal Ingestion)](#51-post-recordsinsert-universal-ingestion)
   - [5.2 POST `/records/store-ai`](#52-post-recordsstore-ai)
   - [5.3 GET `/records` & POST `/records/query`](#53-get-records--post-recordsquery)
   - [5.4 POST & PUT `/records/update`](#54-post--put-recordsupdate)
   - [5.5 POST & DELETE `/records/delete`](#55-post--delete-recordsdelete)
6. [Dashboard & Analytics Endpoints (`/dashboard`)](#6-dashboard--analytics-endpoints-dashboard)
   - [6.1 GET & POST `/dashboard/metrics`](#61-get--post-dashboardmetrics)
   - [6.2 POST `/dashboard/recalculate-score`](#62-post-dashboardrecalculate-score)
7. [Scoring Goals Configuration Endpoints (`/goals`)](#7-scoring-goals-configuration-endpoints-goals)
   - [7.1 POST `/goals/setup`](#71-post-goalssetup)
   - [7.2 GET & POST `/goals`](#72-get--post-goals)
8. [AI Multimodal Ingestion Endpoints (`/ingest`)](#8-ai-multimodal-ingestion-endpoints-ingest)
   - [8.1 POST `/ingest/process-text`](#81-post-ingestprocess-text)
   - [8.2 POST `/ingest/process-audio`](#82-post-ingestprocess-audio)
   - [8.3 POST `/ingest/process-image`](#83-post-ingestprocess-image)
   - [8.4 POST `/ingest/insert-record` & `/ingest/store-ai-record`](#84-post-ingestinsert-record--ingeststore-ai-record)
9. [Interactive Chatbot Endpoints (`/chat`)](#9-interactive-chatbot-endpoints-chat)
   - [9.1 POST `/chat/message`](#91-post-chatmessage)
   - [9.2 GET `/chat/history`](#92-get-chathistory)
   - [9.3 DELETE `/chat/clear`](#93-delete-chatclear)
10. [System Endpoints](#10-system-endpoints)
   - [10.1 GET `/health`](#101-get-health)
11. [Client Integration Examples (TypeScript / Axios)](#11-client-integration-examples-typescript--axios)

---

## 1. Architecture Overview & Core Concepts

The **WellPro FastAPI Co-Pilot Backend** serves as the intelligence layer and high-performance API gateway bridging frontend applications (Web, iOS, Android), AI models (Gemini, Groq Whisper, OpenRouter Vision), Frappe v15 ERP, and MongoDB Atlas.

```
┌────────────────────────────────────────────────────────┐
│            Frontend (Web / Mobile / Wearables)         │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP REST / JSON
                           ▼
┌────────────────────────────────────────────────────────┐
│               WellPro FastAPI Backend                  │
│                                                        │
│  ├─ /auth       -> User Registration, Login & Session  │
│  ├─ /records    -> CRUD, Queries, Universal Ingestion  │
│  ├─ /dashboard  -> Multi-Window Metrics & Analytics   │
│  ├─ /goals      -> Goal Targets Setup & Retrieval      │
│  ├─ /ingest     -> Multimodal AI (Text, Audio, Vision) │
│  └─ /chat       -> Persistent ReAct Agentic Chatbot    │
└────────────┬─────────────────────────────┬─────────────┘
             │ RPC calls                   │ Checkpoints / Logs
             ▼                             ▼
┌─────────────────────────┐   ┌──────────────────────────┐
│   Frappe ERP Backend    │   │      MongoDB Atlas       │
│  (MariaDB + Scoring)    │   │  (Audit & Chat History)  │
└─────────────────────────┘   └──────────────────────────┘
```

### Key Capabilities:
- **Instant Score Recalculation**: Any record insertion, update, or deletion automatically triggers daily wellbeing score calculations and returns recalculated scores directly.
- **Multimodal AI Ingestion**: Accepts raw conversational text, voice audio (auto-translated to English via Groq Whisper), and OCR receipt images (via OpenRouter Vision) and extracts structured records.
- **Multi-DocType Ingestion**: Submit records across multiple domains (Health, Finance, Social, Check-in) in a single unified HTTP call.
- **Agentic CRUD Chatbot**: A stateful conversational agent capable of querying history, creating records, configuring goals, and recalculating scores with persistent memory in MongoDB.

---

## 2. Authentication & Request Headers

All protected endpoints require Frappe API token authentication passed in the standard `Authorization` header:

```http
Authorization: token <api_key>:<api_secret>
Content-Type: application/json
```

- When registering via `POST /api/v1/auth/signup` or logging in via `POST /api/v1/auth/login`, the response returns `api_key` and `api_secret`.
- Combine them with a colon (`:`) prefixed with `token `:  
  `Authorization: token 4c9e88bf91a13b2:9a7f34bc0281ef5`

---

## 3. DocTypes & Data Models Reference

| DocType | Scope | Primary Date Field | Description |
|---|---|---|---|
| **Health Daily Record** | User | `record_date` | Daily steps, sleep, water, calories, protein, energy |
| **Health Activity** | User | `logged_at` | Workout sessions (walking, running, cycling, gym, sports) |
| **Financial Transaction** | User | `transaction_date` | Ledger entries (income, expense, transfer, investment, debt) |
| **Financial Snapshot** | User | `snapshot_date` | Monthly balances, savings, emergency fund, investments |
| **Social Activity** | User | `logged_at` | Social interactions, relationship types, quality ratings |
| **Subjective Wellbeing Checkin** | User | `date` | Self-reported mood, energy, stress, loneliness ratings |
| **Wellbeing Daily Score** | User | `score_date` | System-computed scores (0-100) and confidence percentages |
| **User Consent Preference** | User | `consent_updated_at` | AI processing and domain tracking permissions |
| **WellPro Profile** | User | `creation` | User preferences, currency, and scoring goals |

---

## 4. Authentication Endpoints (`/auth`)

### 4.1 POST `/auth/signup`
Registers a new user in the system, initializes Profile and Consent records, and generates API credentials.

- **URL**: `/api/v1/auth/signup`
- **Method**: `POST`
- **Auth**: None (Public)
- **Headers**: `Content-Type: application/json`

#### Input JSON
```json
{
  "email": "sarah.connor@example.com",
  "password": "SecurePassword123!",
  "first_name": "Sarah",
  "last_name": "Connor"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Valid email address |
| `password` | string | Yes | Minimum 6 characters |
| `first_name` | string | No | User's first name |
| `last_name` | string | No | User's last name |

#### Output JSON (HTTP 201 Created)
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": "sarah.connor@example.com",
    "api_key": "4c9e88bf91a13b2",
    "api_secret": "9a7f34bc0281ef5"
  }
}
```

---

### 4.2 POST `/auth/login`
Authenticates existing credentials and returns API key and secret. Supports both `usr`/`pwd` and `email`/`password` keys.

- **URL**: `/api/v1/auth/login`
- **Method**: `POST`
- **Auth**: None (Public)
- **Headers**: `Content-Type: application/json`

#### Input JSON
```json
{
  "usr": "sarah.connor@example.com",
  "pwd": "SecurePassword123!"
}
```
*(Or alternatively: `{"email": "...", "password": "..."}`)*

#### Output JSON (HTTP 200 OK)
```json
{
  "success": true,
  "message": "Authentication successful",
  "data": {
    "user": "sarah.connor@example.com",
    "api_key": "4c9e88bf91a13b2",
    "api_secret": "9a7f34bc0281ef5"
  }
}
```

---

### 4.3 GET & POST `/auth/verify-session`
Validates session credentials in the `Authorization` header and returns user profile and consent configurations.

- **URL**: `/api/v1/auth/verify-session`
- **Method**: `GET` or `POST`
- **Auth**: `Authorization: token <api_key>:<api_secret>`
- **Input JSON**: None

#### Output JSON (HTTP 200 OK)
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

## 5. Records CRUD & Query Endpoints (`/records`)

### 5.1 POST `/records/insert` (Universal Ingestion)
The primary ingestion endpoint supporting multiple ingestion formats in a single API call. Immediately recalculates and returns wellbeing scores for the affected dates.

- **URL**: `/api/v1/records/insert`
- **Method**: `POST`
- **Auth**: Required (`Authorization: token <key>:<secret>`)
- **Headers**: `Content-Type: application/json`

#### Ingestion Format A: Multi-DocType on Single Request (Recommended)
Submit records across multiple DocTypes in one combined payload:

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

#### Ingestion Format B: Single Record Insert
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

#### Ingestion Format C: Batch Array
```json
[
  {
    "doctype": "Health Activity",
    "record_data": {
      "activity_type": "Running",
      "logged_at": "2026-10-30 07:30:00",
      "duration_minutes": 35.0,
      "distance_km": 5.2,
      "calories_burned": 340
    }
  }
]
```

#### Output JSON (HTTP 200 OK)
```json
{
  "success": true,
  "message": "Successfully created 5 records",
  "data": {
    "count": 5,
    "affected_dates": ["2026-10-30"],
    "created": [
      {
        "index": 0,
        "doctype": "Health Daily Record",
        "name": "HDR-00042",
        "affected_date": "2026-10-30",
        "record": { ... }
      },
      {
        "index": 1,
        "doctype": "Financial Transaction",
        "name": "FT-00109",
        "affected_date": "2026-10-30",
        "record": { ... }
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

---

### 5.2 POST `/records/store-ai`
Dedicated endpoint for domain-keyed extractions. Automatically injects `source: "AI Extraction"` and recalculates scores.

- **URL**: `/api/v1/records/store-ai`
- **Method**: `POST`
- **Auth**: Required

#### Input JSON
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

#### Output JSON (HTTP 200 OK)
```json
{
  "success": true,
  "message": "Successfully processed 3 AI domain extractions",
  "data": {
    "count": 3,
    "affected_dates": ["2026-10-30"],
    "created": [ ... ],
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

---

### 5.3 GET `/records` & POST `/records/query`
Retrieves paginated user records for a specific DocType.

#### GET `/records`
- **URL**: `/api/v1/records`
- **Method**: `GET`
- **Auth**: Required
- **Query Parameters**:
  - `doctype` (string, required): e.g. `Financial Transaction`, `Health Daily Record`
  - `limit` (integer, default `50`, max `200`): Max records
  - `offset` (integer, default `0`): Pagination offset
  - `order_by` (string, optional): e.g. `transaction_date desc`
  - `from_date` (string, optional): Filter YYYY-MM-DD
  - `to_date` (string, optional): Filter YYYY-MM-DD

#### POST `/records/query`
- **URL**: `/api/v1/records/query`
- **Method**: `POST`
- **Auth**: Required
- **Input JSON**:
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

#### Output JSON (HTTP 200 OK)
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

---

### 5.4 POST & PUT `/records/update`
Updates an existing document by DocType and document name (`name`). Recalculates scores for both the original date and new date if the date changed.

- **URL**: `/api/v1/records/update`
- **Method**: `POST` or `PUT`
- **Auth**: Required

#### Input JSON
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

#### Output JSON (HTTP 200 OK)
```json
{
  "success": true,
  "message": "Health Daily Record updated successfully",
  "data": {
    "name": "HDR-00042",
    "water_liters": 3.2,
    "sleep_quality": 5,
    "steps": 10500
  }
}
```

---

### 5.5 POST & DELETE `/records/delete`
Safely removes a document owned by the authenticated caller and triggers score recalculation for the affected date.

- **URL**: `/api/v1/records/delete`
- **Method**: `POST` or `DELETE`
- **Auth**: Required

#### Input JSON
```json
{
  "doctype": "Financial Transaction",
  "name": "FT-00109"
}
```

#### Output JSON (HTTP 200 OK)
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

## 6. Dashboard & Analytics Endpoints (`/dashboard`)

### 6.1 GET & POST `/dashboard/metrics`
The primary analytics endpoint for the application dashboard. Computes:
1. Current daily score (`0.0` - `100.0`) and confidence values across all 3 domains.
2. Multi-window recency-weighted scores (`7-day`, `30-day`, `90-day`) with exponential decay ($\lambda = 0.05$).
3. Historical trend timeline array.
4. Recent 10 entries across Health, Financial, Social, and Checkins.

- **URL**: `/api/v1/dashboard/metrics`
- **Method**: `GET` or `POST`
- **Auth**: Required
- **GET Query Parameters**:
  - `days` (integer, default `30`, min `1`, max `365`): Timeline lookback window
  - `as_of_date` (string, optional): Evaluation target date (YYYY-MM-DD, defaults to today)
- **POST Input JSON**:
```json
{
  "days": 30,
  "as_of_date": "2026-10-30"
}
```

#### Output JSON (HTTP 200 OK)
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
    "financial": [ ... recent 10 transactions ... ],
    "health": [ ... recent 10 daily records ... ],
    "health_activities": [ ... recent 10 activities ... ],
    "social": [ ... recent 10 social logs ... ],
    "checkins": [ ... recent 10 checkins ... ]
  }
}
```

---

### 6.2 POST `/dashboard/recalculate-score`
Explicitly recalculates daily score and confidence metrics for a specific date.

- **URL**: `/api/v1/dashboard/recalculate-score`
- **Method**: `POST`
- **Auth**: Required

#### Input JSON
```json
{
  "date": "2026-10-30"
}
```
*(If `date` is omitted, defaults to today)*

#### Output JSON (HTTP 200 OK)
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

## 7. Scoring Goals Configuration Endpoints (`/goals`)

### 7.1 POST `/goals/setup`
Configures user-specific scoring thresholds. Accepts human-friendly string formats (`"12k"`, `"$3,500"`, `"25%"`, `"3L"`) or raw numbers.

- **URL**: `/api/v1/goals/setup`
- **Method**: `POST`
- **Auth**: Required

#### Input JSON
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

#### Output JSON (HTTP 200 OK)
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

---

### 7.2 GET & POST `/goals`
Retrieves effective scoring goals merged with system defaults.

- **URL**: `/api/v1/goals`
- **Method**: `GET` or `POST`
- **Auth**: Required

#### Output JSON (HTTP 200 OK)
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

## 8. AI Multimodal Ingestion Endpoints (`/ingest`)

### 8.1 POST `/ingest/process-text`
Extracts structured personal records from natural language text using Gemini and automatically dispatches them to Frappe.

- **URL**: `/api/v1/ingest/process-text`
- **Method**: `POST`
- **Auth**: Required

#### Input JSON
```json
{
  "raw_text": "Slept 7.5 hours last night with great sleep quality. Walked 8,500 steps today, drank 2.5 liters of water. Bought a $12 salad for lunch, and had a 45 minute video call with my sister."
}
```

#### Output JSON (HTTP 200 OK)
```json
{
  "status": "success",
  "user_email": "sarah.connor@example.com",
  "extracted_count": 4,
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
        "description": "Converted from 12.0 USD to PKR",
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
  "frappe_dispatch_results": [
    {
      "type": "store_ai_record",
      "status": "success",
      "message": "Successfully processed 3 AI domain extractions",
      "recalculated_scores": {
        "2026-10-30": {
          "health_score": 86.0,
          "financial_score": 79.5,
          "social_score": 88.0,
          "overall_score": 84.5
        }
      }
    }
  ],
  "recalculated_scores": {
    "2026-10-30": {
      "health_score": 86.0,
      "financial_score": 79.5,
      "social_score": 88.0,
      "overall_score": 84.5
    }
  },
  "mongo_log_id": "67220cf01a4e98f45a19bb01",
  "validation_error": null
}
```

---

### 8.2 POST `/ingest/process-audio`
Accepts multipart audio files (WAV, MP3, M4A, OGG, FLAC) in **any language**, translates to English via Groq Whisper (`whisper-large-v3`), extracts structured records, and inserts them into Frappe.

- **URL**: `/api/v1/ingest/process-audio`
- **Method**: `POST`
- **Auth**: Required
- **Content-Type**: `multipart/form-data`

#### Form Data:
- `file`: Audio binary file

#### Output JSON (HTTP 200 OK)
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
  "frappe_dispatch_results": [ ... ],
  "recalculated_scores": { ... },
  "mongo_log_id": "67220d1a1a4e98f45a19bb02"
}
```

---

### 8.3 POST `/ingest/process-image`
Accepts receipts, medical reports, or activity photos. Runs OCR using OpenRouter Vision, structures the data, and persists records into Frappe.

- **URL**: `/api/v1/ingest/process-image`
- **Method**: `POST`
- **Auth**: Required
- **Content-Type**: `multipart/form-data`

#### Form Data:
- `file`: Image binary file (JPEG, PNG, WEBP)

#### Output JSON (HTTP 200 OK)
```json
{
  "status": "success",
  "user_email": "sarah.connor@example.com",
  "extracted_ocr_text": "Walmart Supercenter\nDate: 2026-10-30\nTotal: $64.30\nPayment: Visa ending in 4112",
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
  "frappe_dispatch_results": [ ... ],
  "recalculated_scores": { ... },
  "mongo_log_id": "67220d3f1a4e98f45a19bb03"
}
```

---

### 8.4 POST `/ingest/insert-record` & `/ingest/store-ai-record`
Direct JSON proxy shortcuts under the `/ingest` router for convenience. Accept identical payloads as `/records/insert` and `/records/store-ai`.

---

## 9. Interactive Chatbot Endpoints (`/chat`)

A persistent, tool-enabled ReAct agent powered by Gemini and MongoDB Checkpointer. The agent can query history, create records, modify documents, inspect dashboard trends, recalculate scores, and set goals.

### 9.1 POST `/chat/message`
Sends a user message to the AI copilot.

- **URL**: `/api/v1/chat/message`
- **Method**: `POST`
- **Auth**: Required

#### Input JSON
```json
{
  "message": "How many steps have I logged this week, and what is my current overall wellbeing score?",
  "session_id": "default"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | User conversational prompt |
| `session_id` | string | No | Thread session identifier (default `"default"`) |

#### Output JSON (HTTP 200 OK)
```json
{
  "status": "success",
  "user_email": "sarah.connor@example.com",
  "session_id": "default",
  "response": "You have logged an average of 9,800 steps daily over the past 7 days! Your current overall wellbeing score is 81.2 (Health: 84.5, Financial: 79.2, Social: 80.0), which is currently trending upwards by 1.5 points."
}
```

---

### 9.2 GET `/chat/history`
Retrieves past user and assistant messages for a session to rehydrate frontend UI on page reload.

- **URL**: `/api/v1/chat/history?session_id=default`
- **Method**: `GET`
- **Auth**: Required

#### Output JSON (HTTP 200 OK)
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

---

### 9.3 DELETE `/chat/clear`
Clears chat memory checkpoints for a given session thread.

- **URL**: `/api/v1/chat/clear?session_id=default`
- **Method**: `DELETE`
- **Auth**: Required

#### Output JSON (HTTP 200 OK)
```json
{
  "status": "success",
  "message": "Chat history cleared for session 'default'.",
  "user_email": "sarah.connor@example.com"
}
```

---

## 10. System Endpoints

### 10.1 GET `/health`
Health check endpoint for container orchestrators and uptime monitoring.

- **URL**: `/health`
- **Method**: `GET`
- **Auth**: None (Public)

#### Output JSON (HTTP 200 OK)
```json
{
  "status": "online",
  "project": "WellPro Intelligence Service"
}
```

---

## 11. Client Integration Examples (TypeScript / Axios)

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

  constructor(baseURL: string, apiKey?: string, apiSecret?: string) {
    this.client = axios.create({
      baseURL: `${baseURL}/api/v1`,
      headers: {
        "Content-Type": "application/json",
        ...(apiKey && apiSecret ? { Authorization: `token ${apiKey}:${apiSecret}` } : {})
      }
    });

    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        const detail = error.response?.data?.detail || error.message;
        return Promise.reject(new Error(detail));
      }
    );
  }

  // 1. Auth: Sign up
  async signup(email: string, password: string, firstName?: string, lastName?: string) {
    return this.client.post("/auth/signup", { email, password, first_name: firstName, last_name: lastName });
  }

  // 2. Auth: Login
  async login(email: string, password: string) {
    return this.client.post("/auth/login", { usr: email, pwd: password });
  }

  // 3. Ingestion: Universal Multi-DocType Log
  async insertRecords(payload: Record<string, any>) {
    return this.client.post("/records/insert", payload);
  }

  // 4. Ingestion: Natural Language Text
  async processText(rawText: string) {
    return this.client.post("/ingest/process-text", { raw_text: rawText });
  }

  // 5. Ingestion: Voice Audio (Multilingual)
  async processAudio(audioBlob: Blob, filename = "voice.mp3") {
    const formData = new FormData();
    formData.append("file", audioBlob, filename);
    return this.client.post("/ingest/process-audio", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });
  }

  // 6. Analytics: Dashboard Metrics & Timeline
  async getDashboardMetrics(days = 30, asOfDate?: string) {
    return this.client.get("/dashboard/metrics", { params: { days, as_of_date: asOfDate } });
  }

  // 7. Goals: Set Custom Wellbeing Targets
  async setGoals(goals: Record<string, any>, recalculate = true) {
    return this.client.post("/goals/setup", { goals, recalculate });
  }

  // 8. Chatbot: Send Message
  async sendChatMessage(message: string, sessionId = "default") {
    return this.client.post("/chat/message", { message, session_id: sessionId });
  }
}
```

