import json
import requests
from bs4 import BeautifulSoup
import os

NOTIFIED_OUTAGES_FILE = "notified_outages.json"

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_outages_for_prefecture(url, prefecture_id):
    """Fetch and parse outage information for a given prefecture."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch the page: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    form = soup.find("form", id="AjaxformId")
    if not form:
        print("Form not found in the HTML content.")
        return []

    form_data = {
        "PrefectureID": prefecture_id,
        "MunicipalityID": "",
        "Submit": "Submit"
    }

    try:
        response = requests.post(url, data=form_data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to submit the form: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    outages = []
    table = soup.find("table", id="tblOutages")
    if table:
        for row in table.find("tbody").find_all("tr"):
            columns = row.find_all("td")
            if columns:
                outages.append({
                    "start_time": columns[0].text.strip(),
                    "end_time": columns[1].text.strip(),
                    "municipality": columns[2].text.strip(),
                    "description": columns[3].text.strip(),
                    "note_number": columns[4].text.strip(),
                    "purpose": columns[5].text.strip()
                })
    else:
        print("No table found in the HTML content.")
    
    return outages

def send_pushover_notification(api_token, user_key, message):
    """Send a notification via Pushover."""
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": api_token,
        "user": user_key,
        "title": "Electricity Outages",
        "message": message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Pushover notification sent successfully.")
    except requests.RequestException as e:
        print(f"Failed to send Pushover notification: {e}")

def load_notified_outages(file_path):
    """Load previously notified outages from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_notified_outages(file_path, outages):
    """Save notified outages to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(outages, file, ensure_ascii=False, indent=4)

def main():
    # Load configuration
    config = load_config('config.json')
    url = config['url']
    selected_prefecture_id = config['selected_prefecture']
    selected_municipality = config['selected_municipality']
    pushover_api_token = config['pushover_api_token']
    pushover_user_key = config['pushover_user_key']

    # Get outages for the selected prefecture
    outages = get_outages_for_prefecture(url, selected_prefecture_id)

    # Filter outages for the selected municipality
    filtered_outages = [outage for outage in outages if selected_municipality in outage['municipality']]

    # Load previously notified outages
    notified_outages = load_notified_outages(NOTIFIED_OUTAGES_FILE)

    # Find new outages
    new_outages = [outage for outage in filtered_outages if outage not in notified_outages]

    # Send Pushover notification for new outages
    if new_outages:
        message = "\n\n".join(
            f"Description: {outage['description']}\nPurpose: {outage['purpose']}"
            for outage in new_outages
        )
        print(message)
        send_pushover_notification(pushover_api_token, pushover_user_key, message)
        # Update the notified outages file
        save_notified_outages(NOTIFIED_OUTAGES_FILE, filtered_outages)
    else:
        print("No new outages found for the selected municipality.")

if __name__ == "__main__":
    main()