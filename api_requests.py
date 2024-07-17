import requests
import time


def get_userid_from_channelid(channel_id, auth):
    url = f'https://ptb.discord.com/api/v9/channels/{channel_id}'
    headers = {
        'Authorization': auth
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('Request successful')
        data = response.json()
        # pprint.pprint(data)
        recipients = data['recipients'][0]['id']
        # print(recipients)
        return recipients
    else:
        print('Request failed with status code:', response.status_code)


def open_dm_with_userid(user_id, auth):
    url = f'https://ptb.discord.com/api/v9/users/@me/channels'
    headers = {
        'Authorization': auth
    }
    data = {
        "recipients": [user_id]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print('Request successful')
        data = response.json()
        # pprint.pprint(data)
        recipients = data
        # print(recipients)
        return recipients
    else:
        print('Request failed with status code:', response.status_code)
        return response





def get_all_open_dms(auth):
    url = f'https://discord.com/api/v9/users/@me/channels'
    headers = {
        'Authorization': auth
    }
    response = requests.get(url, headers=headers)
    print("attempting to login")
    if response.status_code == 200:
        print('Request successful')
        data = response.json()
        sorted_dms = sorted(data, key=lambda dm: int(dm['last_message_id']), reverse=True)
        # pprint.pprint(sorted_dms)

        return sorted_dms
    else:
        print('Request failed with status code:', response.status_code)
        return None


def find_dm_channel_id(user_id, auth):
    '''
    requires channel id to be an open dm
    :param user_id: userid
    :param auth: auth token
    :return: channelid
    '''
    dm_channels = get_all_open_dms(auth)
    for dm in dm_channels:
        if dm['type'] == 1:  # Only consider direct messages
            recipient = dm['recipients'][0]
            if recipient['id'] == user_id:
                return dm['id']
    return None


def get_channel_messages(auth, channel_id, limit=100, before=None, author_id=None):
    """
    Fetch messages from a specific Discord channel.

    Parameters:
    token (str): The bot or user token for authentication.
    channel_id (str): The ID of the channel to fetch messages from.
    limit (int): The number of messages to retrieve (max 100).
    before (str): The message ID to fetch messages before.

    Returns:
    list: A list of messages from the channel.
    """
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"{auth}",  # If using a user token (less recommended)
        "Content-Type": "application/json"
    }
    params = {
        "limit": limit
    }
    if before:
        params["before"] = before

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json()}")
        return None


def get_all_messages_fasterforsomedmsmethod(auth, channel_id, author_id=None):
    """
    Get all messages from a Discord channel.

    Parameters:
    - token (str): The bot token.
    - channel_id (str): The ID of the channel to load messages from.
    - author_id (str, optional): The ID of the author to filter messages by. Defaults to None.

    Returns:
    - list: A list of all messages from the channel.
    """
    all_messages = []
    before = None

    while True:
        messages = get_channel_messages(auth, channel_id, before=before)
        # pprint.pprint(messages)
        if not messages:
            break
        filtered = []
        if author_id:
            for message in messages:
                if message['author']['id'] == author_id:
                    filtered.append(message)
            all_messages.extend(filtered)
        else:
            all_messages.extend(messages)
        before = messages[-1]['id']
        time.sleep(1)  # Sleep to avoid hitting rate limits

    return all_messages


def get_count_messages_for_user(auth, channel_id, author_id=None, log=None, max_retries=5):
    headers = {
        "Authorization": f"{auth}",  # If using a user token (less recommended)
    }
    params = {}
    if author_id:
        params['author_id'] = author_id

    def get_message_count(url, params, delay=1):
        retry_count = 0
        while retry_count < max_retries:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('total_results', 0)
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', delay)) + 1
                log(f'Rate limited. Retrying in {retry_after} seconds...')
                time.sleep(retry_after)
                retry_count += 1
                delay *= 2  # Exponential backoff
            else:
                print(f'Failed to fetch messages: {response.status_code} - {response.text}')
                return None
        print('Max retries reached. Returning None.')
        return None

    url_to_check_channel_type = f'https://ptb.discord.com/api/v9/channels/{channel_id}'
    response_check = requests.get(url_to_check_channel_type, headers=headers)
    if response_check.status_code == 200:
        if response_check.json()['type'] == 0:
            server_id = response_check.json()['guild_id']
            url = f'https://discord.com/api/v9/guilds/{server_id}/messages/search'
            params['channel_id'] = channel_id
            print("channel type is guild, using url: ", url)
        else:
            # print("type is dm")
            url = f'https://discord.com/api/v9/channels/{channel_id}/messages/search'
        return get_message_count(url, params)
    else:
        print(f"Error {response_check.status_code}: {response_check.json()}")
        return None


def get_count_messages_for_user_by_server(auth, server_id, author_id=None, log=None, max_retries=5):
    headers = {
        "Authorization": f"{auth}",  # If using a user token (less recommended)
    }
    params = {}
    if author_id:
        params['author_id'] = author_id

    def get_message_count(url, params, delay=1):
        retry_count = 0
        while retry_count < max_retries:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('total_results', 0)
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', delay)) + 1
                log(f'Rate limited. Retrying in {retry_after} seconds...')
                time.sleep(retry_after)
                retry_count += 1
                delay *= 2  # Exponential backoff
            else:
                print(f'Failed to fetch messages: {response.status_code} - {response.text}')
                return None
        print('Max retries reached. Returning None.')
        return None

    url = f'https://discord.com/api/v9/guilds/{server_id}/messages/search'
    return get_message_count(url, params)


def search_message_from_channel(auth, channel_or_guild_id, author_id=None, offset=0, self=None, reset_bar=False,
                                isguild=False):
    headers = {
        "Authorization": f"{auth}",  # If using a user token (less recommended)
    }
    params = {}
    if author_id:
        params['author_id'] = author_id
    if offset:
        params['offset'] = offset
    if not isguild:
        url_to_check_channel_type = f'https://ptb.discord.com/api/v9/channels/{channel_or_guild_id}'
        response_check = requests.get(url_to_check_channel_type, headers=headers)
        if response_check.status_code == 200:
            if response_check.json()['type'] == 0:
                server_id = response_check.json()['guild_id']
                # print("type is server:", serverid)
                url = f'https://discord.com/api/v9/guilds/{channel_or_guild_id}/messages/search'
                params['channel_id'] = channel_or_guild_id
            else:
                # print("type is dm")
                url = f'https://discord.com/api/v9/channels/{channel_or_guild_id}/messages/search'
        else:
            print(f"Error {response_check.status_code}: {response_check.json()}")
            return None
    else:
        url = f'https://discord.com/api/v9/guilds/{channel_or_guild_id}/messages/search'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        messages = [msg for sublist in data['messages'] for msg in sublist]
        sorted_messages = sorted(messages, key=lambda x: int(x['id']), reverse=True)
        total = int(data['total_results'])
        if reset_bar:
            self.reset_progress_bar(int(data['total_results']))
            self.append_log(f"found {int(data['total_results'])} messages total in DM ")
        return sorted_messages, total
    else:
        print(f'Failed to fetch messages meow meow: {response.status_code} - {response.text}')
        return None


def delete_message(auth, channel_id, message_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
    headers = {
        "Authorization": f"{auth}",  # If using a user token (less recommended)
    }

    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        # print(f"Successfully deleted message {message_id}")
        return True
    else:
        print(f"Failed to delete message {message_id}: {response.status_code} - {response.text}")
        return False


def get_and_del_all_messages_from_channel_search(auth, channel_id, delay, author_id=None, self=None, is_running=None,
                                                 is_guild=False, channel_name=None):
    seen = set()
    page = 1
    offset = 0
    total = 0
    delete_messages_count = 0
    print("here")
    while True:
        if page == 1:
            data, total = search_message_from_channel(auth, channel_id, author_id, offset, self=self, reset_bar=True,
                                                      isguild=is_guild)
        else:
            data, _ = search_message_from_channel(auth, channel_id, author_id, offset, self=self, reset_bar=False,
                                                  isguild=is_guild)
        if data is None:
            # print("Rate limited, sleeping 10 seconds")
            time.sleep(10)
        else:
            to_delete = []
            messages = data
            # print("potential messages found: ", len(data))
            for message in messages:
                # print(message['id'])
                if message['id'] not in seen:
                    if message['type'] == 0 or 6 <= message['type'] <= 21:  # filter out messages (can't be deleted)
                        to_delete.append((message['id'], message['content'], message['channel_id']))
                    else:
                        self.append_log("skipping message because not deletable")
                        seen.add(message['id'])
                        offset += 1
                else:
                    print("errrrrm this its going over the same message more than once for some reason: ",
                          message['id'])

            # print(f"found {len(to_delete)} messages to delete on page")
            if len(to_delete) > 0:
                self.append_log(f'found: {len(to_delete)} to delete')
            else:
                if total > 0:
                    self.append_log("found no messages, waiting for discord to index and searching again")
                    time.sleep(5)
            page += 1
            for message_id, content, c_id in to_delete:
                if self is not None:
                    if not is_running():
                        self.get_counts_button.configure(state="enabled")
                        self.new_button.configure(text="Start")
                        self.append_log("Stopped deleting messages")
                        return
                retry_count = 0
                max_retries = 5
                while retry_count < max_retries:
                    # print(f"attempting to delete message: channel: {c_id} messageid: {message_id}")
                    if delete_message(auth, c_id, message_id):
                        delete_messages_count += 1
                        seen.add(message_id)
                        # print("delete message count: ", delete_messages_count)
                        if channel_name:
                            self.append_log(channel_name + ', Deleted: ' + content)
                        else:
                            self.append_log('Deleted: ' + content)
                        self.update_progress()
                        break  # Exit the retry loop if deletion is successful
                    else:
                        retry_count += 1
                        self.append_log(f'Error deleting message: {content}')
                        if retry_count < max_retries:
                            delay_value = delay() * (2 ** retry_count) + 1  # Exponential backoff
                            self.append_log(f'Retrying in {delay_value} seconds...')
                            time.sleep(delay_value)  # Increase delay before retrying
                        else:
                            self.append_log('Max retries reached. Moving to next message.')
                            self.update_progress()
                            seen.add(message_id)
                            offset += 1
                            break
                            # print("issue deleting message so skipping it!")
                time.sleep(delay())  # Call delay as a function to fetch updated value
            print("offset: ", offset, "len of seen: ", len(seen), "total: ", total)
            if len(seen) >= total:
                self.append_log("finished DM")
                break
        self.append_log(f'searching next page for messages after {delay() * 3 + 20}s delay')
        time.sleep(delay() * 3 + 20)  # Call delay as a function to fetch updated value


def get_user_data(auth):
    headers = {
        "Authorization": f"{auth}",
    }
    url = "https://discord.com/api/v9/users/@me"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        print(f"Failed to fetch user ID: {response.status_code} - {response.text}")
        return None


def get_user_guilds(auth):
    headers = {
        'Authorization': f'{auth}'
    }

    def get_guilds():
        url = "https://discord.com/api/v10/users/@me/guilds"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch guilds: {response.status_code} - {response.text}")
            return None

    guilds = get_guilds()
    return guilds
