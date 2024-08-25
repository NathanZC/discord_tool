import json
from datetime import datetime
from api_requests import *
import customtkinter
from PIL import Image


def download_avatar_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        avatar_image = Image.open(response.raw)
        return customtkinter.CTkImage(avatar_image)
    return None


def print_dms_with_numbers(auth_token):
    data = get_all_open_dms(auth_token)
    if data:
        print("Login Successful\n")
        for i, dm in enumerate(data, start=1):
            usernames = [recipient['username'] for recipient in dm['recipients']]
            if dm["type"] == 3:
                print(f"{i}. Group DM with: {', '.join(usernames)}")
            else:
                print(f"{i}. DM with: {usernames[0]}")
    else:
        print("Failed to load DMs or no DMs available.")
    return data


# def display_messages(auth_token, channel_id):
#     messages_data = search_message_from_channel(auth_token, channel_id)
#     if messages_data:
#         messages = messages_data.get('messages', [])
#         if messages:
#             for message_group in messages:
#                 for message in message_group:
#                     author = message['author']['username']
#                     content = message['content']
#                     print(f"{author}: {content}")
#         else:
#             print("No messages found.")
#     else:
#         print("Failed to fetch messages.")


def load_discord_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data


def change_appearance_mode_event(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)


def calculate_time_remaining(total_messages, delay):
    """
    Calculate the estimated time remaining.

    Args:
        total_messages (int): The total number of messages.
        delay (float): The delay between each message operation in seconds.

    Returns:
        str: A string representing the estimated time remaining in the format 'HH:MM:SS'.
    """
    # Calculate the total time in seconds
    total_seconds = total_messages * delay + (total_messages)  # need num of pages since its inconsistent

    # Convert the total seconds to a timedelta object
    time_remaining = datetime.timedelta(seconds=total_seconds)

    # Format the timedelta as HH:MM:SS
    return str(time_remaining)


def date_to_snowflake(date_str):
    discord_epoch = 1420070400000
    # Convert the date string to a datetime object
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    # Convert the datetime to a timestamp in milliseconds
    timestamp = int(dt.timestamp() * 1000)
    # Calculate the snowflake
    snowflake = (timestamp - discord_epoch) << 22
    return snowflake


def is_valid_date(date_str):
    try:
        # Attempt to parse the date
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_to_snowflake(date_str) >= 0
    except ValueError:
        return False
