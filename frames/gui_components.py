import customtkinter
from api_requests import get_userid_from_channelid, open_dm_with_userid


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, toggle_command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.toggle_command = toggle_command
        self.label_list = []
        self.total_message_labels = []
        self.sent_message_labels = []
        self.checkbox_list = []
        self.dms_widgets = {}

    def add_item(self, item, image=None, dm=None, total_messages="Total Messages:", sent_messages="Sent Messages:"):
        if dm is None or 'id' not in dm:
            raise ValueError("DM must be provided and contain an 'id' key")

        if not self.item_exists(item):
            label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
            total_label = customtkinter.CTkLabel(self, text=total_messages, padx=5, anchor="w")
            sent_label = customtkinter.CTkLabel(self, text=sent_messages, padx=5, anchor="w")
            checkbox = customtkinter.CTkCheckBox(self, text="Enable", onvalue=True, offvalue=False)

            if self.toggle_command is not None:
                checkbox.configure(command=lambda: self.on_toggle_state(dm, checkbox))

            row_index = len(self.label_list)
            label.grid(row=row_index, column=0, pady=(0, 10), sticky="w")
            total_label.grid(row=row_index, column=1, pady=(0, 10), sticky="w")
            sent_label.grid(row=row_index, column=2, pady=(0, 10), sticky="w")
            checkbox.grid(row=row_index, column=3, pady=(0, 10), padx=5)

            self.label_list.append(label)
            self.total_message_labels.append(total_label)
            self.sent_message_labels.append(sent_label)
            self.checkbox_list.append(checkbox)
            self.dms_widgets[dm['id']] = {'label': label, 'total_label': total_label, 'sent_label': sent_label,
                                          'checkbox': checkbox}

    def on_toggle_state(self, dm, checkbox):
        # Implement any specific logic for toggling state here
        if self.toggle_command is not None:
            self.toggle_command(dm, checkbox.get())

    def disable_all_buttons(self):
        for dm_id in self.dms_widgets:
            self.dms_widgets[dm_id]['checkbox'].configure(state="disabled")

    def restore_button_states(self):
        for dm_id in self.dms_widgets:
            self.dms_widgets[dm_id]['checkbox'].configure(state="normal")

    def remove_item(self, item):
        if item in self.dms_widgets:
            widgets = self.dms_widgets.pop(item)
            widgets['label'].destroy()
            widgets['total_label'].destroy()
            widgets['sent_label'].destroy()
            widgets['checkbox'].destroy()

    def item_exists(self, text):
        return any(text == label.cget("text") for label in self.label_list)

    def update_item(self, text, image):
        for label in self.label_list:
            if text in label.cget("text"):
                label.configure(text=text, image=image)
                label.image = image  # Keep a reference to avoid garbage collection
                break

    def update_message_labels(self, item, total_messages, sent_messages):
        if item in self.dms_widgets:
            widgets = self.dms_widgets[item]
            widgets['total_label'].configure(text=f"Total messages: {total_messages}")
            widgets['sent_label'].configure(text=f"Messages sent: {sent_messages}")

    def clear_items(self):
        # Iterate through the widgets and destroy them
        for dm_id in list(self.dms_widgets.keys()):
            widgets = self.dms_widgets.pop(dm_id)
            widgets['label'].destroy()
            widgets['total_label'].destroy()
            widgets['sent_label'].destroy()
            widgets['checkbox'].destroy()

        # Clear the lists and dictionary
        self.label_list.clear()
        self.total_message_labels.clear()
        self.sent_message_labels.clear()
        self.checkbox_list.clear()
        self.dms_widgets.clear()


class ScrollableLabelButtonFrame2(customtkinter.CTkScrollableFrame):
    def __init__(self, master, toggle_command=None, logger=None, open_dms=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.auth = None
        self.logger = logger

        self.dms_widgets = {}  # Dictionary to store widgets by channel_id
        self.open_dms = open_dms if open_dms is not None else []
        self.toggle_command = toggle_command

    def add_item(self, item, image=None, dm=None, sent_messages="Messages:"):
        if dm is None or 'id' not in dm:
            raise ValueError("DM must be provided and contain an 'id' key")

        channel_id = dm['id']
        if channel_id not in self.dms_widgets:
            label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
            sent_label = customtkinter.CTkLabel(self, text=sent_messages, padx=5, anchor="w")
            checkbox = customtkinter.CTkCheckBox(self, text="Enable", onvalue=True, offvalue=False)
            open_dm_button = customtkinter.CTkButton(self, text="Open DM",
                                                     command=lambda: self.open_dm(dm),
                                                     state="normal" if channel_id not in self.open_dms else "disabled")

            if self.toggle_command is not None:
                checkbox.configure(command=lambda: self.on_toggle_state(dm, checkbox.get()))

            # Grid placement
            row_index = len(self.dms_widgets)
            label.grid(row=row_index, column=0, pady=(0, 10), sticky="w")
            sent_label.grid(row=row_index, column=1, pady=(0, 10), sticky="w")
            checkbox.grid(row=row_index, column=2, pady=(0, 10), padx=5)
            open_dm_button.grid(row=row_index, column=3, pady=(0, 10), padx=5)

            # Store in dictionary
            self.dms_widgets[channel_id] = {
                "label": label,
                "sent_label": sent_label,
                "checkbox": checkbox,
                "button": open_dm_button
            }

    def on_toggle_state(self, dm, checkbox_state):
        if self.toggle_command is not None:
            self.toggle_command(dm, checkbox_state)

    def remove_item(self, channel_id):
        if channel_id in self.dms_widgets:
            widgets = self.dms_widgets[channel_id]
            widgets['label'].destroy()
            widgets['sent_label'].destroy()
            widgets['checkbox'].destroy()
            widgets['button'].destroy()
            del self.dms_widgets[channel_id]

    def open_dm(self, dm):
        channel_id = dm['id']
        button = self.dms_widgets[channel_id]['button']
        if button:
            button.configure(state="disabled")
            print(f"Opening DM for ID: {channel_id} with description: {dm['description']}")
            u_id = get_userid_from_channelid(channel_id, self.auth)
            response = open_dm_with_userid(u_id, self.auth)
            self.open_dms.append(channel_id)
            if self.logger:
                if len(response['recipients']) == 1:
                    self.logger(f"Opened dm with {response['recipients'][0]['username']}")
                else:
                    self.logger(f"Opened GROUP with {response['recipients'][0]['username']}....")

    def update_item(self, channel_id, new_text, new_image):
        if channel_id in self.dms_widgets:
            label = self.dms_widgets[channel_id]['label']
            label.configure(text=new_text, image=new_image)
            label.image = new_image  # Keep a reference to avoid garbage collection

    def update_sent_messages(self, channel_id, sent_messages_count):
        if channel_id in self.dms_widgets:
            sent_label = self.dms_widgets[channel_id]['sent_label']
            sent_label.configure(text=f"Messages sent: {sent_messages_count}")

    def disable_all_buttons(self):
        for channel_id in self.dms_widgets:
            checkbox = self.dms_widgets[channel_id]['checkbox']
            checkbox.configure(state="disabled")

    def restore_button_states(self):
        for channel_id in self.dms_widgets:
            checkbox = self.dms_widgets[channel_id]['checkbox']
            checkbox.configure(state="normal")

    def update_dms(self, open_dms, auth):
        self.open_dms = open_dms
        self.auth = auth

    def item_exists(self, channel_id):
        return channel_id in self.dms_widgets

    def clear(self):
        for channel_id in list(self.dms_widgets.keys()):
            self.remove_item(channel_id)

    def get_dms_sorted(self):
        sorted_items = sorted(self.dms_widgets.items(), key=lambda x: int(x[1]['label'].cget("text").split(".")[0]))
        return sorted_items
