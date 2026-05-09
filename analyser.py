import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, get_analysis_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def calculate_metrics(property_data: dict) -> dict:
    """
    Calculate core real estate metrics from raw numbers.
    These are hard maths — we do not rely on AI for these.
    """
    try:
        price = float(property_data.get("price", 0))
        monthly_rent = float(property_data.get("rental_income", 0))
        monthly_expenses = float(property_data.get("expenses", 0))

        annual_rent = monthly_rent * 12
        annual_expenses = monthly_expenses * 12
        annual_net = annual_rent - annual_expenses

        rental_yield = (annual_rent / price * 100) if price > 0 else 0
        roi = (annual_net / price * 100) if price > 0 else 0
        payback_years = (price / annual_net) if annual_net > 0 else 0

        return {
            "calculated_rental_yield": round(rental_yield, 2),
            "calculated_roi": round(roi, 2),
            "calculated_payback_years": round(payback_years, 1),
            "annual_net_income": round(annual_net, 2),
        }
    except Exception:
        return {
            "calculated_rental_yield": 0,
            "calculated_roi": 0,
            "calculated_payback_years": 0,
            "annual_net_income": 0,
        }


def analyse_property(property_data: dict) -> dict:
    """
    Send one property to OpenAI and get back an AI analysis.
    Merges AI insights with our own calculated metrics.
    """
    # First calculate our own hard numbers
    metrics = calculate_metrics(property_data)

    # Add metrics to the data we send AI so it has full context
    enriched_data = {**property_data, **metrics}

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": get_analysis_prompt(enriched_data)},
            ],
            temperature=0.3,
            max_tokens=800,
        )

        raw = response.choices[0].message.content.strip()

        # Clean up response in case AI adds markdown formatting
        raw = raw.replace("```json", "").replace("```", "").strip()
        ai_result = json.loads(raw)

        # Merge AI analysis with our calculated metrics
        return {
            "property_name": property_data.get("property_name", "Unknown"),
            "location": property_data.get("location", "Unknown"),
            "price": property_data.get("price", 0),
            **metrics,
            **ai_result,
            "status": "success",
        }

    except json.JSONDecodeError:
        return {
            "property_name": property_data.get("property_name", "Unknown"),
            "location": property_data.get("location", "Unknown"),
            "price": property_data.get("price", 0),
            **metrics,
            "status": "error",
            "error": "AI returned unexpected format",
        }
    except Exception as e:
        return {
            "property_name": property_data.get("property_name", "Unknown"),
            "location": property_data.get("location", "Unknown"),
            "price": property_data.get("price", 0),
            **metrics,
            "status": "error",
            "error": str(e),
        }


def analyse_all(properties: list[dict]) -> list[dict]:
    """
    Analyse a list of properties one by one.
    Returns list of results in the same order.
    """
    results = []
    for prop in properties:
        result = analyse_property(prop)
        results.append(result)
    return results