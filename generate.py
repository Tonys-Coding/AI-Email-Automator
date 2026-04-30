import os
from dotenv import load_dotenv
from google import genai

#Loading API Key from the .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_email(topic, audience, tone):
    prompt = f"""
    Write a {tone} email newsletter.and
    
    Topic: {topic}
    Audience: {audience}

    Format with:
    - Subject Line (label it "Subject:")
    - Greeting
    - Body (2-3 paragraphs)
    - Clear Call to Action
    

    Keep it slighly concise but engaging, and make sure to include a detailed overview/description of the topic, and a clear call to action for the audience.
    """

    try:

        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API Failed: {e}")

if __name__ == "__main__":

    email = generate_email(
        topic="The latest AI tools for productivity",
        audience="Tech enthusiasts and professionals",
        tone="Informative and engaging"
     )
    
    print(email)