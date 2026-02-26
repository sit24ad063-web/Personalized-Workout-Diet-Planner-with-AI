def generate_workout_plan(age, weight, height, goal, diet, budget, location):

    prompt = f"""
Create a structured weekly workout and nutrition plan.

User:
- Age: {age}
- Weight: {weight}kg
- Height: {height}cm
- Goal: {goal}
- Diet: {diet}
- Budget: {budget}
- Training Location: {location}

STRICT RULES:
- Use markdown headings (##, ###)
- Use bullet points
- No long paragraphs
- Separate workout and nutrition clearly
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ stable Groq model
            messages=[
                {"role": "system", "content": "You are an elite fitness coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Groq API Error: {str(e)}"
