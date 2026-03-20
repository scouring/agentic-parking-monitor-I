# 🚗 Smart Parking AI System

An end-to-end AI-powered system that transforms parking lot images into real-time operational decisions using computer vision, forecasting, and agent-based reasoning.

---

## 📌 Overview

This project simulates a production-grade intelligent parking management system. It combines:

- Computer Vision (YOLO) for vehicle detection  
- Time-series tracking and forecasting  
- Rule-based + LLM-powered decision engine  
- Interactive dashboard (Streamlit)  

The system converts raw visual data into actionable insights such as pricing adjustments, traffic redirection, and operational alerts.

---

## 🎯 Business Value (ROI)

This system is designed to deliver measurable impact:

- 💰 **Revenue Optimization**: Dynamic pricing based on occupancy  
- 💸 **Cost Reduction**: Reduced need for manual monitoring  
- ⚙️ **Operational Efficiency**: Automated alerts and decisions  
- 🚗 **Customer Experience**: Reduced search time for parking  

---

## 🏗️ Architecture

```text
Image Feed (Simulated)
        ↓
Vision Service (YOLO Detection)
        ↓
Occupancy Counter
        ↓
Data Logger (Time Series)
        ↓
Forecasting Model (Next-hour prediction)
        ↓
Agent (Decision Engine + LLM Explanation)
        ↓
Streamlit Dashboard
```

---

## 📋 Prerequisites
- **WSL: Ubuntu**
- **Python 3.10**
- **OpenAI API key** # put in .env file

---

## ⚙️ Features

🔍**Computer Vision**
    * YOLO-based vehicle detection
    * Handles dense scenes and small objects
📊 **Real-Time Dashboard**
    * Live feed simulation from image stock
    * Occupancy metrics (total, occupied, available)
    * Occupancy rate visualization
📈 **Time-Series Tracking**
    * Persistent logging of occupancy data
    * Trend visualization over time
🔮 **Forecasting**
    * Linear regression-based next-hour occupancy prediction
    * Enables proactive decision-making
🤖 **Agent-Based Decision System**
    * Structured decisions:
        - Pricing adjustments
        - Traffic redirection
        - Alerts
    * LLM-generated explanations for business users
🚨 **Alerts**
    * High occupancy warnings
    * Forecast-based demand alerts

---

## 📸 Screenshots
    **Dashboard**
    **Live Feed Simulation**
    ![App Demo](static/video/Recording%202026-03-20%20150310.gif)
    **Forecasting**
    <p align="center">
   <img src="static/video/Recording%202026-03-20%20150310.gif" width="700" />
   </p>

---

## 📊 Model Training Summary
    * Model: YOLOv8 (Ultralytics)
    * Dataset: PKLot
    * Task: Vehicle detection
    * Metrics:
        - maP@0.5: 0.99
        - mAP@50_95: 0.97
        - Precision: 0.998
        - Recall: 0.998

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/scouring/agentic-parking-monitor-I.git
cd agentic-parking-monitor-I
```

### 2. Create a Virtual Environment
```bash
## Using python venv
python3 -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate

## Using conda
conda activate venv # whatever the name of the env
```

### 3. Install dependancies
```bash
pip install -r requirements.txt
```

### 4. Run locally
```bash

streamlit run app/app.py
```

### 5. Open a webpage for the UI
```bash
http://localhost:8501
```
Select the button "Start Live Feed Simulation"

---

## Project Structure
agentic-parking-monitor/
├── app/
├── vision_service/
├── agent_service/
├── models/
├── dataset/
├── requirements.txt
└── README.md

---

## License

This project is licensed under the [MIT License](LICENSE)

---

## Future Work
- Real-time camera integration
- Multi-lot optimization
- Advanced forecasting (ARIMA, LSTM)
- API integration for pricing systems
- Notification system (Slack/SMS)

