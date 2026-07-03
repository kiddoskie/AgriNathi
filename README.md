AGRI-NATHI: Empowering Farmers Through Voice
AGRI-NATHI is an AI-driven, voice-based platform designed to bridge the digital divide for rural farmers in South Africa. By utilizing standard phone calls, it provides real-time access to weather, market prices, and agricultural advice in local languages—without the need for internet access or smartphones.

🚀 The Mission
Many farmers in rural areas face significant barriers to growth due to limited access to modern digital tools. AGRI-NATHI removes these barriers by turning any mobile device into a powerful agricultural information hub, speaking the farmer's language.

⚙️ How It Works
Dial In: The farmer calls the dedicated AGRI-NATHI phone number.

Select Language: The system greets the user and prompts them to select their preferred language (English or IsiZulu).

Navigate Options: Using simple voice prompts, the farmer can:

Get Daily Weather: Hear real-time min/max temperature forecasts for their area.

Check Market Prices: Receive the latest market pricing for specific crops.

Log a Query: Submit a specific agricultural question or issue for expert processing.

Action: The backend processes the request and provides an immediate or logged response.

🏗️ Technical Architecture
AGRI-NATHI is built for scalability and reliability:

Frontend/Voice Gateway: Twilio handles incoming calls and powers Speech-to-Text (STT) and Text-to-Speech (TTS) integration.

Backend: A robust Python Flask server acts as the logic engine, managing call flows via webhooks.

Database: MongoDB securely stores crop queries for analytics and follow-up.

Integrations:

Weather API: (e.g., OpenWeatherMap) for real-time meteorological data.

Market API: Real-time South African crop market data.
