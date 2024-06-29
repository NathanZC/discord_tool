import json

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


def display_messages(auth_token, channel_id):
    messages_data = search_message_from_channel(auth_token, channel_id)
    if messages_data:
        messages = messages_data.get('messages', [])
        if messages:
            for message_group in messages:
                for message in message_group:
                    author = message['author']['username']
                    content = message['content']
                    print(f"{author}: {content}")
        else:
            print("No messages found.")
    else:
        print("Failed to fetch messages.")


def load_discord_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data


def change_appearance_mode_event(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)


