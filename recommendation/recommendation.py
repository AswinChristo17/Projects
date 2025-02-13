import requests

# Groq API Key (Replace with your actual key)
API_KEY = "Api-Key"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_workout_recommendation(height, weight):
    bmi = weight / ((height / 100) ** 2)  # BMI Calculation

    # Define the prompt
    prompt = f"""
    My height is {height} cm and my weight is {weight} kg. My BMI is {bmi:.2f}.
    Based on this, suggest a detailed weekly food routine that consider my training, cardio, and flexibility exercises.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    # Send request to Groq API
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    height = float(input("Enter your height in cm: "))
    weight = float(input("Enter your weight in kg: "))

    recommendation = get_workout_recommendation(height, weight)
    print("\nWorkout Recommendation:\n", recommendation)
