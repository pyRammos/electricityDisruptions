# Electricity Disruptions Notification

This project fetches electricity outage information for a selected prefecture and municipality, and sends notifications for new outages via Pushover.

## Features

- Fetches electricity outage information from the [Deddie](https://siteapps.deddie.gr/outages2public) website.
- Filters outages based on the selected prefecture and municipality.
- Sends notifications for new outages via Pushover.
- Stores previously notified outages to avoid duplicate notifications.

## Requirements

- Python 3.x
- Pushover account and API token

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/electricity-disruptions.git
    cd electricity-disruptions
    ```

2. Install the required Python libraries:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a [config.json](http://_vscodecontentref_/4) file in the project directory with the following content:

    ```json
    {
        "selected_prefecture": "10",
        "selected_municipality": "ΓΛΥΦΑΔΑΣ",
        "pushover_api_token": "your_pushover_api_token",
        "pushover_user_key": "your_pushover_user_key"
    }
    ```

## Usage

Run the script:

```sh
python electricityDisrpuptions.py