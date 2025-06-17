# Smart-Event-Planner---Backend-Assignment
1. Weather API Integration
Integrated OpenWeatherMap 5-day forecast API.

Parsed weather data including:

Temperature

Precipitation (rain)

Wind speed

General weather condition (clear, clouds, etc.)

Graceful error handling for failed API calls.

2. Event Management System
Users can create events with:

Name

City

Date

Event Type (Outdoor Sports, Wedding/Formal)

Events are stored in Streamlit session state (in-memory).

3. Simple Weather Suitability Analysis
For each event:

Weather forecast is fetched for the event’s date & location.

Suitability is scored dynamically based on event type:

Outdoor Sports: focuses on temp (15–30°C), low wind, low rain, clear/cloudy.

Weddings/Formal: favors milder temp (18–28°C), calm winds, no rain.

Output classification: Good, Okay, or Poor.

Events with “Poor” weather show a warning.

4. Streamlit Frontend
Intuitive form to create events.

Real-time display of all planned events and their weather suitability.

Minimal and clean interface, with:

Sectioned layout

Emojis/icons for user engagement

Clear output messages
