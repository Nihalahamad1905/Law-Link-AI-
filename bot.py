import logging
import sqlite3
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from fir_analysis import analyze_fir

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot and Foursquare API tokens (replace with your credentials)
TOKEN = "7693826570:AAGP9n7vIP61v20lySD7ewEC7IMxD_QI0-I"  # Replace with your actual bot token
FOURSQUARE_API_KEY = "fsq3WZGjaNuzsA9liuTk2Ig6MC553xLbXW0mvkr+E+iLhag="  # Replace with your actual Foursquare API key

# Foursquare API functions
async def get_nearby_police_stations(latitude, longitude):
    radius = 1000000
    url = "https://api.foursquare.com/v3/places/nearby"
    headers = {"Authorization": FOURSQUARE_API_KEY}
    params = {'ll': f'{latitude},{longitude}', 'radius': radius, 'query': 'police'}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        places = []
        if "results" in data:
            for place in data['results']:
                name = place.get('name', 'Unnamed Police Station')
                lat = place['geocodes']['main']['latitude']
                lon = place['geocodes']['main']['longitude']
                places.append((name, lat, lon))
        return places if places else [("No nearby police stations found.", None, None)]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching police stations: {e}")
        return [("Error fetching police stations.", None, None)]

async def get_nearby_government_buildings(latitude, longitude):
    radius = 1000000
    url = "https://api.foursquare.com/v3/places/nearby"
    headers = {"Authorization": FOURSQUARE_API_KEY}
    params = {'ll': f'{latitude},{longitude}', 'radius': radius, 'query': 'Government Building'}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        places = []
        if "results" in data:
            for place in data['results']:
                name = place.get('name', 'Unnamed Government Building')
                lat = place['geocodes']['main']['latitude']
                lon = place['geocodes']['main']['longitude']
                places.append((name, lat, lon))
        return places if places else [("No nearby government buildings found.", None, None)]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching government buildings: {e}")
        return [("Error fetching government buildings.", None, None)]

# Bot menu keyboard
def create_keyboard():
    keyboard = [
        [InlineKeyboardButton("1. FIR Analysis ⚖️", callback_data="fir_analysis")],
        [InlineKeyboardButton("2. Find Nearest Police Station 🚓", callback_data="2")],
        [InlineKeyboardButton("3. Find Nearest Government Building 🏛️", callback_data="3")],
        [InlineKeyboardButton("4. Emergency Contacts 🚨", callback_data="4")]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "👋 Welcome to LawLink AI! ⚖️🔗\n\nI’m here to assist you with:\n\n✅ FIR Analysis – Get insights on legal acts & sections 📜\n✅ Finding Nearby Police Stations 🚔\n✅ Locating Government Buildings 🏛️🏥\n\nPlease choose an option below to get started! 🚀",
        reply_markup=create_keyboard()
    )

# Button callback handler for non-choose_another options
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "fir_analysis":
        await query.edit_message_text("You selected FIR Analysis. Please enter a description of the incident.")
        context.user_data['request'] = "fir_analysis"
    elif query.data == "2":
        response_text = "You selected: *Find Nearest Police Station* 🚓. Please share your location."
        await query.edit_message_text(text=response_text)
        context.user_data['request'] = 'police'
        location_button = KeyboardButton("Share Location 📍", request_location=True)
        reply_markup = ReplyKeyboardMarkup([[location_button]], one_time_keyboard=True)
        await query.message.reply_text("Please share your location:", reply_markup=reply_markup)
    elif query.data == "3":
        response_text = "You selected: *Find Nearest Government Building* 🏛️. Please share your location."
        await query.edit_message_text(text=response_text)
        context.user_data['request'] = 'government'
        location_button = KeyboardButton("Share Location 📍", request_location=True)
        reply_markup = ReplyKeyboardMarkup([[location_button]], one_time_keyboard=True)
        await query.message.reply_text("Please share your location:", reply_markup=reply_markup)
    elif query.data == "4":
        response_text = "Emergency Contacts 🚨:\n\n- Police: 100\n- Ambulance: 102\n- Hospital: 103"
        keyboard = [[InlineKeyboardButton("Choose Another Option 🔄", callback_data="choose_another")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=response_text, reply_markup=reply_markup)

# Separate handler for "choose_another"
async def choose_another(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Please choose an option below:", reply_markup=create_keyboard())

# Handler for location messages
async def handle_location(update: Update, context: CallbackContext) -> None:
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    username = update.message.from_user.username
    request_type = context.user_data.get('request', None)
    if request_type == 'police':
        places = await get_nearby_police_stations(latitude, longitude)
        response_message = "Nearby Police Stations: 🚓"
    elif request_type == 'government':
        places = await get_nearby_government_buildings(latitude, longitude)
        response_message = "Nearby Government Buildings: 🏛️"
    else:
        response_message = "Please choose an option first."
        await update.message.reply_text(response_message)
        return

    # Log user activity in SQLite
    conn = sqlite3.connect('user_activity.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS activity (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        latitude REAL,
                        longitude REAL,
                        activity TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    activity = f"Requested nearest {request_type}"
    cursor.execute("INSERT INTO activity (username, latitude, longitude, activity) VALUES (?, ?, ?, ?)",
                   (username, latitude, longitude, activity))
    conn.commit()
    conn.close()

    if places and ((places[0][0] == "No nearby police stations found.") or (places[0][0] == "No nearby government buildings found.")):
        response_message = places[0][0]
        await update.message.reply_text(response_message)
        return

    keyboard = []
    for name, lat, lon in places:
        if lat is not None and lon is not None:
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=driving"
            keyboard.append([InlineKeyboardButton(name, url=maps_url)])
    keyboard.append([InlineKeyboardButton("Choose Another Option 🔄", callback_data="choose_another")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response_message, reply_markup=reply_markup)

# Handler for text messages (for FIR Analysis)
async def handle_text(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('request') == 'fir_analysis':
        user_input = update.message.text
        ipc_sections = analyze_fir(user_input)
        if ipc_sections:
            response = "🔎 Applicable IPC Sections:\n\n" + "\n\n".join(ipc_sections)
        else:
            response = "No matching IPC sections found for the provided description."
        
        # Log FIR Analysis activity in SQLite (latitude & longitude not applicable)
        conn = sqlite3.connect('user_activity.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS activity (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT,
                            latitude REAL,
                            longitude REAL,
                            activity TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                          )''')
        activity_text = f"FIR Analysis: {user_input}"
        cursor.execute("INSERT INTO activity (username, latitude, longitude, activity) VALUES (?, ?, ?, ?)",
                       (update.message.from_user.username, None, None, activity_text))
        conn.commit()
        conn.close()

        keyboard = [[InlineKeyboardButton("Choose Another Option 🔄", callback_data="choose_another")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response, reply_markup=reply_markup)
        context.user_data['request'] = None
    else:
        await update.message.reply_text("Please choose an option from the menu.")

# Register handlers and run the bot
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler('start', start))
# Register button handler without "choose_another"
application.add_handler(CallbackQueryHandler(button, pattern='^(fir_analysis|2|3|4)$'))
# Register a separate handler for "choose_another"
application.add_handler(CallbackQueryHandler(choose_another, pattern='^choose_another$'))
application.add_handler(MessageHandler(filters.LOCATION, handle_location))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

application.run_polling()
