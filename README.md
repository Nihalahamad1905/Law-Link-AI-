# LawLink AI Bot - FIR Analysis using ML for Proper Acts and Sections

## Overview

LawLink AI Bot is a **Telegram bot** that utilizes **Machine Learning (ML), Natural Language Processing (NLP), and Sentiment Analysis** to analyze user-reported incidents and determine the applicable legal sections. Additionally, it provides location-based services to find the nearest **police stations, government buildings**, and **emergency contacts** using live location data.

## Features

- **Incident Analysis**: Uses ML and NLP to analyze user-input incidents and suggest applicable legal sections and acts.
- **Sentiment Analysis**: Implements **Logistic Regression** and **Naïve Bayes** for classification.
- **Live Location Services**: Identifies the nearest police station and government offices using **Google Maps API**.
- **Emergency Assistance**: Provides emergency contact details for quick help.
- **Telegram Bot Integration**: Enables users to interact with the system through a Telegram bot.
- **Admin Dashboard**: Provides a control panel for admins to monitor user activity.
- **Database Support**: Stores user queries and analysis results for future reference.
- **Live User Activity Tracking**: Admins can view real-time user searches along with their locations.

## Tech Stack

- **Programming Language**: Python
- **Framework**: Flask
- **Machine Learning**: scikit-learn
- **Natural Language Processing (NLP)**: nltk
- **Telegram Bot Integration**: python-telegram-bot
- **Location Services**: Google Maps API, requests
- **Data Handling**: pandas
- **Database**: SQLite / PostgreSQL
- **Admin Dashboard**: Flask with HTML/CSS and JavaScript

## Installation

### Prerequisites

Ensure you have Python installed (preferably Python 3.7+). You can install the required dependencies using:

```bash
pip install Flask pandas nltk scikit-learn python-telegram-bot requests
````
## Setup and Usage
### 1. Clone the Repository
```bash
git clone <repo-link>
cd lawlink-ai-bot
````
### 2. Train the Model (If required)
```bash
python train_model.py
````
### 3. Run the Flask Server
```bash
python app.py
````
### 4. Start the Telegram Bot
Configure your Telegram Bot Token in the script and run:
```bash
python bot.py
````

## API Endpoints
<table style="width:100%; border-collapse: collapse; text-align: left;">
  <tr style="background-color: #f2f2f2;">
    <th style="border: 1px solid #ddd; padding: 8px;">Endpoint</th>
    <th style="border: 1px solid #ddd; padding: 8px;">Method</th>
    <th style="border: 1px solid #ddd; padding: 8px;">Description</th>
  </tr>
  <tr>
    <td style="border: 1px solid #ddd; padding: 8px;">/predict</td>
    <td style="border: 1px solid #ddd; padding: 8px;">POST</td>
    <td style="border: 1px solid #ddd; padding: 8px;">Predicts the applicable legal section based on input text</td>
  </tr>
  <tr style="background-color: #f9f9f9;">
    <td style="border: 1px solid #ddd; padding: 8px;">/location</td>
    <td style="border: 1px solid #ddd; padding: 8px;">GET</td>
    <td style="border: 1px solid #ddd; padding: 8px;">Returns the nearest police station based on user location</td>
  </tr>
  <tr>
    <td style="border: 1px solid #ddd; padding: 8px;">/emergency</td>
    <td style="border: 1px solid #ddd; padding: 8px;">GET</td>
    <td style="border: 1px solid #ddd; padding: 8px;">Fetches emergency contact details</td>
  </tr>
  <tr style="background-color: #f9f9f9;">
    <td style="border: 1px solid #ddd; padding: 8px;">/admin</td>
    <td style="border: 1px solid #ddd; padding: 8px;">GET</td>
    <td style="border: 1px solid #ddd; padding: 8px;">Provides access to the admin dashboard</td>
  </tr>
</table>

## Example Usage
- User sends an incident description via Telegram.
- The bot analyzes it and returns the relevant legal sections.
- The bot can also provide the nearest police station and emergency contacts.
- Admins can monitor user searches and locations in real time.

## Contributors
- Nihalahamad Aslam Shaikh
- Sakshi Menkar
- Sanika Jadhav
- Shradhha Thorat

