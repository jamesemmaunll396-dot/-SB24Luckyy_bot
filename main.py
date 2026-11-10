import requests

def get_forex_news(update, context):
    try:
        # Replace with your actual Forex API endpoint and key
        response = requests.get("https://api.yourforexsource.com/news", timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Parse your data here and send it to the user
            news_text = f"Latest News: {data['headline']}"
            context.bot.send_message(chat_id=update.effective_chat.id, text=news_text)
        else:
            # This logs the specific failure code instead of crashing silently
            print(f"API Error Code: {response.status_code}")
            context.bot.send_message(chat_id=update.effective_chat.id, text="Temporarily unable to fetch market updates.")
            
    except Exception as e:
        print(f"Error fetching forex news: {e}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to retrieve Forex news at the moment.")
