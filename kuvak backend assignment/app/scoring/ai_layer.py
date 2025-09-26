# app/scoring/ai_layer.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

# Initialize OpenRouter client with new API
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def ai_score(lead: dict, offer: dict) -> dict:
    """
    Calls OpenRouter (via OpenAI SDK >=1.0.0) to classify buying intent.
    Falls back gracefully if API fails.
    """
    try:
        prompt = f"""
        Prospect details: {lead}
        Product/Offer details: {offer}

        Task: Classify buying intent as High, Medium, or Low.
        Also, explain reasoning in 1–2 sentences.
        """

        response = client.chat.completions.create(
            model="tngtech/deepseek-r1t2-chimera:free",  # or another OpenRouter model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )

        result_text = response.choices[0].message.content.strip()

        # Extract intent
        if "High" in result_text:
            intent, points = "High", 50
        elif "Medium" in result_text:
            intent, points = "Medium", 30
        else:
            intent, points = "Low", 10

        return {
            "intent": intent,
            "points": points,
            "reasoning": result_text,
        }

    except Exception as e:
        # fallback
        return {
            "intent": "Medium",
            "points": 30,
            "reasoning": f"[Fallback due to error] {str(e)}",
        }
