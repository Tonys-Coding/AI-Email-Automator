import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

#Loading API Key from the .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_email(topic, audience, tone):
    prompt = f"""
    You are an expert email newsletter writer
    Write a {tone} email newsletter in clearn HTML format(body content only, no <html> or <body> tags)

    
    Topic: {topic}
    Audience: {audience}

    Use the Google Search Tool to find the most recent, up to date information on the topic before writing


   Format the email using rich HTML including:
    - A subject line as: <p><strong>Subject:</strong> Your subject here</p>
    - A greeting
    - Sections with <h3> subheadings
    - Bullet points using <ul> and <li> tags where appropriate
    - Bold key terms using <strong>
    - Working hyperlinks using <a href="..."> for any sources or tools mentioned
    - A clear call to action button styled like: <a href="#" style="background:#2c3e50;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">Learn More</a>


    Only return the HTML content, nothing else

    Keep it slighly concise but engaging, and make sure to include a detailed overview/description of the topic, and a clear call to action for the audience.
    """

    try:

        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API Failed: {e}")

if __name__ == "__main__":

    email = generate_email(
        topic="The latest, most recent AI tools for productivity, search the web and look for AI tools/updates within the last week",
        audience="Tech enthusiasts and professionals",
        tone="Informative and engaging"
     )
    
    print(email)