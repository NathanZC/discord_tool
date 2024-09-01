import threading
from frames.gui_components import ScrollableLabelButtonFrame
from helpers import *
from api_requests import *

class SecondFrame(customtkinter.CTkFrame):
    def __init__(self, master, auth_key, open_dms, user_data):
        super().__init__(master)
        self.master = master
        self.auth_key = auth_key
        self.open_dms = open_dms
        self.user_data = user_data

        self.jobs = []
        self.dms_loaded = False
        self.is_running = False
        self.is_getting_message_counts = False
        self.stop_thread = threading.Event()
        self.slider_delay = 1  # Initial delay value
        self.total_progress_value = 100
        self.current_progress_value = 0

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=3)

        # Add ScrollableLabelButtonFrame
        self.scrollable_frame = ScrollableLabelButtonFrame(master=self, toggle_command=self.handle_toggle,
                                                           corner_radius=0)
        self.scrollable_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.get_counts_button = customtkinter.CTkButton(self, text="Get message counts", state="disabled",
                                                         command=self.get_message_counts_button)
        self.get_counts_button.grid(row=0, column=2, padx=50, pady=10, sticky="n")

        self.new_button = customtkinter.CTkButton(self, text="Start", command=self.toggle_button, fg_color='red',
                                                  hover_color="#8c0000")
        self.new_button.grid(row=0, column=2, padx=50, pady=(10, 10), sticky="s")

        self.progress_bar = customtkinter.CTkProgressBar(self, orientation='horizontal', mode='determinate')
        self.progress_bar.grid(row=0, column=1, columnspan=1, padx=(20, 10), pady=(30, 30), sticky="nsew")
        self.progress_bar.set(0)  # Initialize progress bar to 0

        # Create a frame to hold the label, slider, and value display
        slider_frame = customtkinter.CTkFrame(self)
        slider_frame.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="s")
        self.slider_label = customtkinter.CTkLabel(slider_frame, text="Delay")
        self.slider_label.grid(row=0, column=0, padx=10, pady=5)
        self.slider_1 = customtkinter.CTkSlider(slider_frame, from_=0, to=20, number_of_steps=15,
                                                command=self.update_slider_value)
        self.slider_1.set(self.slider_delay)  # Set to the initial delay value
        self.slider_1.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.slider_value = customtkinter.StringVar()
        self.slider_value_label = customtkinter.CTkLabel(slider_frame, textvariable=self.slider_value)
        self.slider_value_label.grid(row=0, column=1, padx=10, pady=5)
        self.update_slider_value(self.slider_delay)  # Initialize the display

        self.log_textbox = customtkinter.CTkTextbox(self, wrap="word")  # Add a large text output box for logs
        self.log_textbox.grid(row=0, column=4, rowspan=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=3, rowspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Options")
        self.tabview.add("Extras")
        self.tabview.tab("Options").grid_columnconfigure(0, weight=2)  # configure grid of individual tabs
        self.tabview.tab("Extras").grid_columnconfigure(0, weight=1)
        self.checkbox = customtkinter.CTkCheckBox(self.tabview.tab("Options"), text="Close Dm After Delete", onvalue=True, offvalue=False)
        self.checkbox.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="s")
        # Add input fields for "before" and "after" dates
        # Add input fields for "before" and "after" dates
        self.before_date_label = customtkinter.CTkLabel(self.tabview.tab("Options"), text="Before Date (YYYY-MM-DD):")
        self.before_date_label.grid(row=1, column=0, padx=(20, 10), pady=(5, 5), sticky="w")

        self.before_date_entry = customtkinter.CTkEntry(self.tabview.tab("Options"), width=200)
        self.before_date_entry.grid(row=2, column=0, padx=(20, 10), pady=(5, 10), sticky="w")

        self.after_date_label = customtkinter.CTkLabel(self.tabview.tab("Options"), text="After Date (YYYY-MM-DD):")
        self.after_date_label.grid(row=3, column=0, padx=(20, 10), pady=(5, 5), sticky="w")

        self.after_date_entry = customtkinter.CTkEntry(self.tabview.tab("Options"), width=200)
        self.after_date_entry.grid(row=4, column=0, padx=(20, 10), pady=(5, 10), sticky="w")

        # Add input field for "containing text"
        self.containing_text_label = customtkinter.CTkLabel(self.tabview.tab("Options"), text="Containing Text:")
        self.containing_text_label.grid(row=5, column=0, padx=(20, 10), pady=(5, 5), sticky="w")

        self.containing_text_entry = customtkinter.CTkEntry(self.tabview.tab("Options"), width=200)
        self.containing_text_entry.grid(row=6, column=0, padx=(20, 10), pady=(5, 10), sticky="w")

        # # Add checkboxes for "Has Link", "Has File", and "Include Pinned"
        # self.has_link_checkbox = customtkinter.CTkCheckBox(self.tabview.tab("Options"), text="Has Link", onvalue=True,
        #                                                    offvalue=False)
        # self.has_link_checkbox.grid(row=7, column=0, padx=(20, 10), pady=(5, 5), sticky="w")
        # self.has_link_checkbox.select()  # Automatically enable the checkbox
        #
        # self.has_file_checkbox = customtkinter.CTkCheckBox(self.tabview.tab("Options"), text="Has File", onvalue=True,
        #                                                    offvalue=False)
        # self.has_file_checkbox.grid(row=8, column=0, padx=(20, 10), pady=(5, 5), sticky="w")
        # self.has_file_checkbox.select()  # Automatically enable the checkbox
        #
        # self.include_pinned_checkbox = customtkinter.CTkCheckBox(self.tabview.tab("Options"), text="Include Pinned",
        #                                                          onvalue=True, offvalue=False)
        # self.include_pinned_checkbox.grid(row=9, column=0, padx=(20, 10), pady=(5, 10), sticky="w")
        # self.include_pinned_checkbox.select()  # Automatically enable the checkbox

    def handle_toggle(self, dm, is_enabled):
        if is_enabled:
            # Queue the job
            self.queue_job_event(dm)
        else:
            # Cancel the job
            self.cancel_job_event(dm)

    def queue_job_event(self, dm):     # start job
        self.jobs.append(dm['id'])
        self.append_log(f"{self.id_to_name(dm['id'])} has been added to the queue")
        self.append_log(f"Current jobs:\n{self.format_jobs()}")

    def cancel_job_event(self, dm):     # cancel job
        # Handle the cancel job event
        self.append_log(f"Removed {self.id_to_name(dm['id'])} from the queue")
        job_to_remove = None
        for job in self.jobs:
            if job == dm['id']:
                job_to_remove = job
                break

        if job_to_remove:
            self.jobs.remove(job_to_remove)
            self.append_log(f"Canceled job for DM ID: {dm['id']}")
            current_jobs = ', '.join([str(job[1]) for job in self.jobs])
            self.append_log(f"Current jobs:\n{self.format_jobs()}")
        else:
            self.append_log(f"No job found for DM ID: {dm['id']}")

    def get_message_counts_button(self):
        if self.is_getting_message_counts:
            # Signal the thread to stop
            self.is_getting_message_counts = False
        else:
            # Clear the stop event and start the thread
            self.is_getting_message_counts = True
            self.get_counts_button.configure(text="Stop getting counts")
            self.append_log(f"Getting message counts... With {int(self.slider_delay)}"
                            f" Seconds delay (Try increasing it if rate limited)")
            self.new_button.configure(state="disabled")
            threading.Thread(target=self.update_message_counts).start()

    def update_slider_value(self, value):
        self.slider_value.set(f"{int(value)} seconds")
        self.slider_delay = int(value)

    def update_progress(self):
        self.current_progress_value += 1
        progress_value = self.current_progress_value / self.total_progress_value
        # print("bar increased, progress value: ", progress_value)
        self.progress_bar.set(progress_value)  # Update progress bar

    def reset_progress_bar(self, total):
        print("resetting progress bar with,", total)
        self.current_progress_value = 0
        self.total_progress_value = total
        self.progress_bar.set(0)  # Update progress bar

    def toggle_button(self):
        if self.is_running:
            self.is_running = False
            self.append_log("Jobs Stopping")
            self.scrollable_frame.restore_button_states()
        else:
            self.is_running = True
            self.new_button.configure(text="Stop")
            self.get_counts_button.configure(state="disabled")
            self.scrollable_frame.disable_all_buttons()
            threading.Thread(target=self.handle_jobs).start()

    def handle_jobs(self):
        content = self.containing_text_entry.get().strip()
        if len(content) == 0:
            content = None
        before_date = self.before_date_entry.get().strip()  # Get and strip any extra whitespace
        after_date = self.after_date_entry.get().strip()
        before_date = before_date if before_date else None
        after_date = after_date if after_date else None
        if before_date and not is_valid_date(before_date):
            self.append_log("Invalid before date format or time. Please use 'YYYY-MM-DD' and only dates since discord was created.")
            if self.dms_loaded:
                self.get_counts_button.configure(state="enabled")
            self.scrollable_frame.restore_button_states()
            self.new_button.configure(text="Start")
            self.is_running = False
            self.append_log("Jobs finished")
            return
        if after_date and not is_valid_date(after_date):
            self.append_log("Invalid after date format or time. Please use 'YYYY-MM-DD' and only dates since discord was created.")
            if self.dms_loaded:
                self.get_counts_button.configure(state="enabled")
            self.scrollable_frame.restore_button_states()
            self.new_button.configure(text="Start")
            self.is_running = False
            self.append_log("Jobs finished")
            return
        if after_date:
            after_date = date_to_snowflake(after_date)
        if before_date:
            before_date = date_to_snowflake(before_date)
        self.append_log("starting Jobs")
        for job in self.jobs:
            self.append_log(f"Job: {self.id_to_name(job)}")
            for _ in range(int(self.slider_delay)):  # Break the sleep into smaller intervals
                if not self.is_running:
                    if self.dms_loaded:
                        self.get_counts_button.configure(state="enabled")
                    self.new_button.configure(text="Start")
                    self.append_log("Stopped deleting messages")
                    return
                time.sleep(1)  # Sleep for 1 second and check again
                # print(f"trying: {self.auth_key}, {job[0]}, {self.user_data['id']}, {self.slider_delay},
                # {self.append_log}")
            get_and_del_all_messages_from_channel_search(
                self.auth_key,
                channel_id=job,
                author_id=self.user_data['id'],
                delay=lambda: self.slider_delay,  # Pass delay as a callable to get the updated value
                self=self,
                is_running=lambda: self.is_running,
                channel_name=self.id_to_name(job),
                before_date=before_date,
                after_date=after_date,
                content_search=content
            )
            if self.checkbox.get():
                close_dm(job, self.auth_key, self)
        if self.dms_loaded:
            self.get_counts_button.configure(state="enabled")
        self.scrollable_frame.restore_button_states()
        self.new_button.configure(text="Start")
        self.is_running = False
        self.append_log("Jobs finished")

    def append_log(self, message):
        # Method to append text to the log_textbox
        self.log_textbox.insert(customtkinter.END, message + "\n")
        self.log_textbox.yview(customtkinter.END)  # Scroll to the end of the text box

    def update_message_counts(self):
        self.reset_progress_bar(len(self.scrollable_frame.dms_widgets))
        for channel_id, _ in self.scrollable_frame.dms_widgets.items():
            total_messages = get_count_messages_for_user(self.auth_key, channel_id, log=self.append_log)
            sent_messages = get_count_messages_for_user(self.auth_key, channel_id,
                                                        author_id=self.user_data['id'], log=self.append_log)
            self.update_progress()
            self.append_log(f"got message counts: " + self.id_to_name(channel_id))
            self.after(0, self.scrollable_frame.update_message_labels, channel_id, total_messages,
                       sent_messages)
            for _ in range(int(self.slider_delay)):  # Break the sleep into smaller intervals
                if not self.is_getting_message_counts:
                    self.get_counts_button.configure(text="Get message counts")
                    self.new_button.configure(state="enabled")
                    self.append_log("Stopped getting message counts.")
                    return
                time.sleep(1)  # Sleep for 1 second and check again

        self.get_counts_button.configure(text="Get message counts")
        self.new_button.configure(state="enabled")
        self.is_getting_message_counts = False

    def update_second_frame(self):
        if self.open_dms:
            for i, dm in enumerate(self.open_dms, start=1):
                usernames = sorted([recipient['username'] for recipient in dm['recipients']])
                avatar_urls = [
                    f"https://cdn.discordapp.com/avatars/{recipient['id']}/{recipient['avatar']}.png"
                    for recipient in dm['recipients'] if recipient['avatar']
                ]
                item_text = f"{i}. Group DM with: {(', '.join(usernames))[:8]}..." if dm[
                                                                                          "type"] == 3 else f"{i}. DM with: {usernames[0]}"
                if not self.scrollable_frame.item_exists(item_text):
                    self.scrollable_frame.add_item(item_text, image=None, dm=dm)
                    if avatar_urls:
                        self.update_avatar_image(i, avatar_urls[0], usernames, dm["type"] == 3)
        self.dms_loaded = True
        if not self.is_running:
            self.get_counts_button.configure(state="normal")

    def update_avatar_image(self, index, avatar_url, usernames, is_group_dm):
        avatar_image = download_avatar_image(avatar_url)
        self.after(0, self.update_ui_with_image, index, avatar_image, usernames, is_group_dm)

    def update_ui_with_image(self, index, avatar_image, usernames, is_group_dm):
        if is_group_dm:
            self.scrollable_frame.update_item(f"{index}. Group DM with: {(', '.join(usernames))[:8]}...", avatar_image)
        else:
            self.scrollable_frame.update_item(f"{index}. DM with: {usernames[0]}", avatar_image)

    def format_jobs(self):
        formatted_jobs = [
            f"{index + 1}. {self.id_to_name(job)}"
            for index, job in enumerate(self.jobs)
        ]
        return "\n".join(formatted_jobs)

    def update_data(self, auth_key, open_dms, user_data):
        self.auth_key = auth_key
        self.open_dms = get_all_open_dms(auth_key)
        self.user_data = user_data

    def id_to_name(self, id):
        for item in self.open_dms:
            if id == item['id']:
                if len(item['recipients']) == 1:
                    return item['recipients'][0]['username']
                else:
                    s = ["Group DM: "]
                    for r in item['recipients']:
                        s.append(f'{r['username']}, ')
                        s.append(r[)
                    return ''.join(s)
        return None
    #meow
    def reset(self):
        # Reset the jobs list
        self.jobs.clear()

        # Reset the progress bar
        self.reset_progress_bar(100)

        # Clear the log text box
        self.log_textbox.delete(1.0, customtkinter.END)
        self.append_log("Welcome To Discord Tool. Select A Dm to delete all messages")
        # Reset buttons and other UI elements
        self.get_counts_button.configure(state="disabled")
        self.new_button.configure(text="Start", state="normal")
        self.scrollable_frame.clear_items()  # If you have a method to clear the scrollable frame
        self.open_dms = get_all_open_dms(self.auth_key)
        self.is_running = False
        self.is_getting_message_counts = False
