import os
import openai

# FAQs
faqs = {
    "programs": "Iron Lady offers Leadership Development, Confidence Bootcamps, Public Speaking, and Executive Coaching.",
    "duration": "Most programs run between 8 to 12 weeks, depending on the track.",
    "mode": "Iron Lady programs are conducted both online and offline (hybrid).",
    "certificate": "Yes, certificates are provided upon successful completion.",
    "mentors": "Programs are led by experienced leadership coaches, industry experts, and successful women leaders."
}

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_answer(user_query):
    query = user_query.lower()

    # Step 1: Check FAQs first
    if "program" in query:
        return faqs["programs"]
    elif "duration" in query:
        return faqs["duration"]
    elif "online" in query or "offline" in query or "mode" in query:
        return faqs["mode"]
    elif "certificate" in query:
        return faqs["certificate"]
    elif "mentor" in query or "coach" in query:
        return faqs["mentors"]

    # Step 2: Fallback to GPT if no FAQ matched
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # you can use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are an assistant that answers questions about Iron Lady leadership programs."},
                {"role": "user", "content": user_query}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Sorry, I couldn't reach AI services. Error: {e}"
