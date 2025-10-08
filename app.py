from flask import Flask, render_template, request
import google.generativeai as genai
import os

# ----------------------------
# Step 1: Configure API Key
# ----------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyBnXp1VG8J2EkWTcvXc9jiI7phlwnOdvF0"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# ----------------------------
# Step 2: Initialize Gemini Model
# ----------------------------
model = genai.GenerativeModel("gemini-pro-latest")

# ----------------------------
# Flask App Setup
# ----------------------------
app = Flask(__name__)

# Function to generate AI-based recommendations
def generate_recommendation(dietary_preferences, fitness_goals, lifestyle_factors,
                            dietary_restrictions, health_conditions, user_query):
    prompt = f"""
    You are an expert AI fitness and diet planner. Based on the following user information:
    - Dietary Preferences: {dietary_preferences}
    - Fitness Goals: {fitness_goals}
    - Lifestyle Factors: {lifestyle_factors}
    - Dietary Restrictions: {dietary_restrictions}
    - Health Conditions: {health_conditions}
    - User Query: {user_query}

    Create a personalized recommendation plan including:

    **Diet Recommendations:** List 5 specific diet types (e.g., High-Protein, Keto, Mediterranean, etc.)

    **Workout Recommendations:** List 5 workouts matching their goals and lifestyle.

    **Meal Suggestions:**
    - 5 Breakfast Ideas
    - 5 Dinner Ideas

    **Additional Tips:** Provide 5 short lifestyle or nutrition tips (snacks, hydration, supplements, etc.)
    """

    response = model.generate_content(prompt)
    return response.text if response else "No response received from Gemini."


@app.route('/')
def index():
    return render_template('index.html', recommendations=None)


@app.route('/recommendations', methods=['POST'])
def recommendations():
    dietary_preferences = request.form.get('dietary_preferences')
    fitness_goals = request.form.get('fitness_goals')
    lifestyle_factors = request.form.get('lifestyle_factors')
    dietary_restrictions = request.form.get('dietary_restrictions')
    health_conditions = request.form.get('health_conditions')
    user_query = request.form.get('user_query')

    # Get AI recommendations
    recommendations_text = generate_recommendation(
        dietary_preferences, fitness_goals, lifestyle_factors,
        dietary_restrictions, health_conditions, user_query
    )

    # Create empty dictionary for categorized results
    recommendations = {
        "diet_types": [],
        "workouts": [],
        "breakfasts": [],
        "dinners": [],
        "additional_tips": []
    }

    # Parse text into categories
    current_section = None
    for line in recommendations_text.splitlines():
        line = line.strip()
        if not line:
            continue

        if "Diet Recommendations" in line:
            current_section = "diet_types"
        elif "Workout" in line:
            current_section = "workouts"
        elif "Breakfast" in line:
            current_section = "breakfasts"
        elif "Dinner" in line:
            current_section = "dinners"
        elif "Tips" in line:
            current_section = "additional_tips"
        elif current_section:
            recommendations[current_section].append(line.lstrip("-•12345. "))

    print("Parsed Recommendations:", recommendations)
    return render_template('index.html', recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)
