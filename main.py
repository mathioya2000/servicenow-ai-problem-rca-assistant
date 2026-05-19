from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import json

load_dotenv()

app = FastAPI(title="ServiceNow AI Problem RCA Assistant")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def home():
    return {"message": "ServiceNow AI Problem RCA Assistant is running"}


@app.get("/check-env")
def check_env():
    return {
        "openai_key_loaded": bool(os.getenv("OPENAI_API_KEY")),
        "servicenow_url_loaded": bool(os.getenv("SERVICENOW_INSTANCE_URL")),
        "servicenow_username_loaded": bool(os.getenv("SERVICENOW_USERNAME")),
        "servicenow_password_loaded": bool(os.getenv("SERVICENOW_PASSWORD")),
    }


@app.get("/problem/{problem_number}")
def get_problem(problem_number: str):
    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = (
        f"{instance_url}/api/now/table/problem"
        f"?sysparm_query=number={problem_number}"
        "&sysparm_limit=1"
        "&sysparm_fields=number,short_description,description,category,priority,state,impact,urgency,workaround,cause_notes,fix_notes,opened_at"
    )

    response = requests.get(
        url,
        auth=(username, password),
        headers={"Accept": "application/json"},
        timeout=30,
    )

    data = response.json()

    if not data.get("result"):
        return {"error": f"Problem {problem_number} not found"}

    return data["result"][0]


@app.get("/ai-problem/{problem_number}")
def analyze_problem(problem_number: str):
    problem = get_problem(problem_number)

    if "error" in problem:
        return problem

    return analyze_problem_with_ai(problem)


def analyze_problem_with_ai(problem: dict):
    prompt = f"""
You are a ServiceNow Problem Management RCA Assistant.

Analyze this ServiceNow Problem record.

Problem:
Number: {problem.get("number")}
Short Description: {problem.get("short_description")}
Description: {problem.get("description")}
Category: {problem.get("category")}
Priority: {problem.get("priority")}
Impact: {problem.get("impact")}
Urgency: {problem.get("urgency")}
State: {problem.get("state")}
Workaround: {problem.get("workaround")}
Cause Notes: {problem.get("cause_notes")}
Fix Notes: {problem.get("fix_notes")}
Opened: {problem.get("opened_at")}

Return STRICT JSON only:
{{
  "problem_summary": "...",
  "probable_root_cause": "...",
  "evidence_needed": ["...", "..."],
  "workaround_recommendation": "...",
  "permanent_fix_recommendation": "...",
  "known_error_recommendation": "...",
  "affected_services": ["...", "..."],
  "business_impact": "...",
  "executive_summary": "..."
}}

Rules:
- If cause notes are missing, recommend evidence needed for RCA.
- If workaround is missing, suggest a safe temporary workaround.
- If fix notes are missing, suggest a permanent fix direction.
- Recommend creating a known error if the issue is recurring or has a workaround.
- Return JSON only, no markdown.
"""

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert ServiceNow Problem Management analyst. Always return valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    ai_text = ai_response.choices[0].message.content

    try:
        parsed = json.loads(ai_text)
    except Exception:
        parsed = {
            "problem_summary": ai_text,
            "probable_root_cause": "",
            "evidence_needed": [],
            "workaround_recommendation": "",
            "permanent_fix_recommendation": "",
            "known_error_recommendation": "",
            "affected_services": [],
            "business_impact": "",
            "executive_summary": "",
        }

    return {
        "problem": problem,
        "structured_ai": parsed,
    }
