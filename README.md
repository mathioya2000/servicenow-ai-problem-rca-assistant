\# ServiceNow AI Problem RCA Assistant



\## Overview

AI-powered ServiceNow Problem Management assistant that analyzes Problem records and generates root cause analysis recommendations.



This project integrates:



\- ServiceNow Problem Management

\- FastAPI backend

\- OpenAI API

\- Render cloud deployment

\- ServiceNow UI Action

\- GlideAjax Script Include



\## Business Use Case

Problem Management teams often spend significant time investigating recurring issues.



This assistant accelerates RCA by providing:



\- probable root cause analysis

\- evidence recommendations

\- workaround suggestions

\- permanent fix recommendations

\- known error recommendations

\- business impact analysis

\- executive summaries



Example:

Repeated EMR login failures → AI identifies authentication timeout issues, impacted services, workaround, and permanent remediation guidance.



\---



\## Architecture



ServiceNow Problem Record

&#x20;       ↓

UI Action (Analyze Problem RCA)

&#x20;       ↓

GlideAjax Script Include

&#x20;       ↓

FastAPI REST API

&#x20;       ↓

OpenAI Analysis Engine

&#x20;       ↓

Structured JSON Response

&#x20;       ↓

ServiceNow Work Notes



\---



\## API Endpoints



\### Health Check

GET /



Returns:



```json

{

&#x20; "message": "ServiceNow AI Problem RCA Assistant is running"

}

```



\### Problem Retrieval

GET /problem/{problem\_number}



Example:



/problem/PRB0000001



\### AI RCA Analysis

GET /ai-problem/{problem\_number}



Example:



/ai-problem/PRB0000001



Returns:



\- root cause

\- workaround

\- permanent fix

\- known error guidance

\- affected services

\- business impact



\---



\## Tech Stack



\- Python

\- FastAPI

\- OpenAI API

\- ServiceNow

\- GlideAjax

\- RESTMessageV2

\- Render

\- GitHub



\---



\## ServiceNow Components



\### UI Action

Problem \[problem]



Button:



Analyze Problem RCA



\### Script Include

AIProblemRCAAssistantAjax



\### Output

Writes structured AI RCA analysis into Problem Work Notes.



\---



\## Deployment



Hosted on Render.



Environment variables:



OPENAI\_API\_KEY

SERVICENOW\_INSTANCE\_URL

SERVICENOW\_USERNAME

SERVICENOW\_PASSWORD



\---



\## Portfolio Value



Demonstrates:



\- ServiceNow development

\- AI integration

\- enterprise workflow automation

\- ITSM Problem Management

\- REST API integration

\- cloud deployment

\- business process intelligence



\---



\## Author



Joseph Mwangi

