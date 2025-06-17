import streamlit as st
import requests
import datetime

# ---------------------- Configuration ----------------------
API_KEY = "your_openweather_api_key_here"  # Replace with your actual OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ---------------------- Helper Functions ----------------------
def get_weather_forecast(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return None
    return response.json()

def analyze_weather(weather_data, event_date, event_type):
    target_date = datetime.datetime.strptime(event_date, "%Y-%m-%d").date()
    scores = []

    for entry in weather_data['list']:
        forecast_time = datetime.datetime.fromtimestamp(entry['dt'])
        if forecast_time.date() == target_date:
            temp = entry['main']['temp']
            wind = entry['wind']['speed']
            weather_desc = entry['weather'][0]['main'].lower()

            precip = 0
            if 'rain' in entry:
                precip = entry['rain'].get('3h', 0)

            score = 0
            # Scoring Logic
            if event_type == "Outdoor Sports":
                if 15 <= temp <= 30:
                    score += 30
                if precip < 1:
                    score += 25
                if wind < 5:
                    score += 20
                if 'clear' in weather_desc or 'cloud' in weather_desc:
                    score += 25

            elif event_type == "Wedding/Formal":
                if 18 <= temp <= 28:
                    score += 30
                if precip < 0.5:
                    score += 30
                if wind < 4:
                    score += 25
                if 'clear' in weather_desc or 'cloud' in weather_desc:
                    score += 15

            scores.append(score)

    if not scores:
        return "No Data"
    avg_score = sum(scores) / len(scores)

    if avg_score >= 80:
        return "Good"
    elif avg_score >= 50:
        return "Okay"
    else:
        return "Poor"

# ---------------------- Main App ----------------------
st.set_page_config(page_title="Smart Event Planner", layout="centered")
st.title("🌤️ Smart Event Planner")

# In-memory storage for demonstration
if 'events' not in st.session_state:
    st.session_state.events = []

# ---------------------- Event Form ----------------------
st.header("📅 Create a New Event")
with st.form("event_form"):
    name = st.text_input("Event Name")
    city = st.text_input("City")
    date = st.date_input("Event Date", min_value=datetime.date.today())
    event_type = st.selectbox("Event Type", ["Outdoor Sports", "Wedding/Formal"])
    submit = st.form_submit_button("Add Event")

    if submit:
        st.session_state.events.append({
            'name': name,
            'city': city,
            'date': date.strftime("%Y-%m-%d"),
            'event_type': event_type
        })
        st.success("✅ Event Added!")

# ---------------------- Display Events ----------------------
st.header("📋 Your Events")
for idx, event in enumerate(st.session_state.events):
    st.subheader(f"{event['name']} - {event['city']} on {event['date']}")

    forecast_data = get_weather_forecast(event['city'])
    if forecast_data is None:
        st.error("❌ Failed to fetch weather data.")
        continue

    suitability = analyze_weather(forecast_data, event['date'], event['event_type'])
    st.write(f"**Weather Suitability:** {suitability}")

    if suitability == "Poor":
        st.warning("⚠️ Consider rescheduling this event.")

# ---------------------- Footer ----------------------
st.markdown("---")
st.caption("Made with ❤️ using Streamlit and OpenWeatherMap")
