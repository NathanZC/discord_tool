import threading
from frames.gui_components import ScrollableLabelButtonFrame2
import tkinter.filedialog as fd
from helpers import *


class ForthFrame(customtkinter.CTkFrame):
    def __init__(self, master, auth_key, servers, user_data):
        super().__init__(master)
        self.master = master
        self.auth_key = auth_key
        self.user_data = user_data

        self.open_dms = None
        self.jobs = []
        self.servers_loaded = False
        self.is_running = False
        self.is_getting_message_counts = False
        self.stop_thread = threading.Event()
        self.slider_delay = 1  # Initial delay value
        self.file_data = None

        self.total_progress_value = 100
        self.current_progress_value = 0

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=3)

        self.scrollable_frame = ScrollableLabelButtonFrame2(master=self, corner_radius=0, toggle_command=self.handle_toggle, logger=self.append_log)
        self.scrollable_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.get_counts_button = customtkinter.CTkButton(self, text="Get message counts", state="disabled", command=self.get_message_counts_button)
        self.get_counts_button.grid(row=0, column=2, padx=50, pady=10, sticky="n")
        self.new_button = customtkinter.CTkButton(self, text="Start", command=self.toggle_button, fg_color='red', hover_color="#8c0000")
        self.new_button.grid(row=0, column=2, padx=50, pady=(10, 10), sticky="s")

        self.progress_bar = customtkinter.CTkProgressBar(self, orientation='horizontal', mode='determinate')
        self.progress_bar.grid(row=0, column=1, columnspan=1, padx=(20, 10), pady=(30, 30), sticky="nsew")
        self.progress_bar.set(0)  # Initialize progress bar to 0

        slider_frame = customtkinter.CTkFrame(self)
        slider_frame.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="s")
        self.slider_label = customtkinter.CTkLabel(slider_frame, text="Delay")
        self.slider_label.grid(row=0, column=0, padx=10, pady=5)
        self.slider_value = customtkinter.StringVar()
        self.slider_value_label = customtkinter.CTkLabel(slider_frame, textvariable=self.slider_value)
        self.slider_value_label.grid(row=0, column=1, padx=10, pady=5)
        self.slider_1 = customtkinter.CTkSlider(slider_frame, from_=0, to=20, number_of_steps=15, command=self.update_slider_value)
        self.slider_1.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.slider_1.set(self.slider_delay)  # Set to the initial delay value
        self.update_slider_value(self.slider_delay)  # Initialize the display

        # Add a large text output box for logs
        self.log_textbox = customtkinter.CTkTextbox(self, wrap="word")
        self.log_textbox.grid(row=0, column=4, rowspan=2, padx=(20, 10), pady=(10, 10), sticky="nsew")

        input_frame = customtkinter.CTkFrame(self)
        input_frame.grid(row=1, column=3, rowspan=1, padx=10, pady=10, sticky="nsew")
        input_frame.grid_rowconfigure(0, weight=0)
        input_frame.grid_rowconfigure(1, weight=0)
        input_frame.grid_columnconfigure(0, weight=1)
        label_text = "Use this to open a DM without having to send a friend request. Input user ID:"
        label = customtkinter.CTkLabel(input_frame, text=label_text, wraplength=200)
        label.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.input_text = customtkinter.CTkTextbox(input_frame, wrap="word", height=10)
        self.input_text.grid(row=9, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.input_text.bind("<KeyRelease>", self.check_text_input)
        self.submit_button_by_id = customtkinter.CTkButton(input_frame, text="Open DM", state="disabled", command=self.open_dm_from_input)
        self.submit_button_by_id.grid(row=11, column=0, padx=10, pady=(10, 10), sticky="n")
        self.open_all_dms_button = customtkinter.CTkButton(input_frame, text="Open All Dms", state="disabled", command=self.open_all_dms)
        self.open_all_dms_button.grid(row=7, column=0, padx=10, pady=(10, 10), sticky="n")
        label_text = "(Max 100 open at once)"
        label = customtkinter.CTkLabel(input_frame, text=label_text, wraplength=200)
        label.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="nsew")
        start_index_label = customtkinter.CTkLabel(input_frame, text="Start Index:")
        start_index_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.start_index_input = customtkinter.CTkTextbox(input_frame, wrap="word", height=10)
        self.start_index_input.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")
        end_index_label = customtkinter.CTkLabel(input_frame, text="End Index:")
        end_index_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.end_index_input = customtkinter.CTkTextbox(input_frame, wrap="word", height=10)
        self.end_index_input.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.submit_button_by_id.grid(row=10, column=0, padx=10, pady=(10, 10), sticky="n")
        self.open_all_dms_button.grid(row=5, column=0, padx=10, pady=(10, 10), sticky="n")
        label_text = "Batch Open Dms (delay included)"
        label = customtkinter.CTkLabel(input_frame, text=label_text, wraplength=200)
        label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.file_input_button = customtkinter.CTkButton(self, text="Input File", command=self.open_file_dialog)
        self.file_input_button.grid(row=0, column=3, padx=10, pady=10, sticky="s")

        self.append_log("To use this, you should request your data from discord and then go to "
                        "package>messages>index.json file and input as the input file. This will allow you to re-open "
                        "all closed dms and delete them.")
    def check_text_input(self, event=None):
        text = self.input_text.get("1.0", "end-1c")
        if text.strip():
            self.submit_button_by_id.configure(state="normal")
        else:
            self.submit_button_by_id.configure(state="disabled")

    def open_all_dms_threaded(self):
        """Thread target function for opening DMs."""
        try:
            start_index = int(self.start_index_input.get("1.0", "end").strip()) - 1
            end_index = int(self.end_index_input.get("1.0", "end").strip()) - 1
        except ValueError:
            self.append_log("Invalid indices. Please enter valid integers.")
            return
        if end_index - start_index > 100:
            self.append_log("Invalid indices. Discord has a 100 open dm limit max")
            return
        if start_index > end_index:
            self.append_log("Invalid indices. start must be < end")
            return

        dms = list(self.scrollable_frame.dms_widgets.items())[start_index:end_index + 1]
        print(dms)
        for key, value in dms:
            if key not in self.scrollable_frame.open_dms:
                self.scrollable_frame.open_dm({'id': key, 'description': value['label']._text})
            else:
                self.append_log(f"Already open {key} with description: {value['label']._text}")
                print(f"Already opened {key} with description: {value['label']._text}")
            time.sleep(self.slider_delay)

    def open_all_dms(self):
        """Starts the open_all_dms_threaded function in a separate thread."""
        threading.Thread(target=self.open_all_dms_threaded, daemon=True).start()

    def open_dm_from_input(self):
        text = self.input_text.get("1.0", "end-1c").strip()
        print(text)
        if text:
            self.append_log(f"Attempting to open DM with input: {text}")
            r = open_dm_with_userid(text, self.auth_key)
            if 'recipients' in r:
                self.submit_button_by_id.configure(state="disabled")
                self.input_text.delete("1.0", "end")  # Clear the input text box
                self.append_log(f"Successfully opened dm: {text}")
            else:
                print(self.append_log(f"Failed to Open DM: {r.content}"))
            # Add your logic here to handle opening the DM based on the input text
            # Example: self.open_dm_logic(text)

    def open_file_dialog(self):
        # Open a file dialog and handle the file
        file_path = fd.askopenfilename(title="Select a file",
                                       filetypes=(
                                           ("JSON files", "*.json"), ("All files", "*.*")))
        if file_path:
            # Process the file if needed
            self.append_log(f"File selected: {file_path}")
            data = load_discord_data(file_path)
            self.file_data = {key: value for key, value in data.items() if "Direct Message" in value}
            threading.Thread(target=self.update_frame).start()

        else:
            self.append_log("File selection cancelled.")

    def handle_toggle(self, dm, is_enabled):
        item_text = f"Channel: {dm['description']}"
        print("is enabled: ", is_enabled, "dm: ", dm)
        if is_enabled:
            # Queue the job
            self.queue_job_event(dm, item_text)
        else:
            # Cancel the job
            self.cancel_job_event(dm, item_text)

    def queue_job_event(self, dm, item):
        self.jobs.append((dm['id'], item))
        print(dm)
        self.append_log(f"{item.strip()} has been added to the queue")
        current_jobs = ', '.join([str(job[1]) for job in self.jobs])
        self.append_log(f"Current jobs:\n{self.format_jobs()}")

    # cancel job
    def cancel_job_event(self, server, item):
        # Handle the cancel job event
        self.append_log(f"Removed {item.split(':', 1)[1].strip() if ':' in item else item.strip()} from the queue")
        job_to_remove = None
        for job in self.jobs:
            if job[0] == server['id']:
                job_to_remove = job
                break

        if job_to_remove:
            self.jobs.remove(job_to_remove)
            self.append_log(f"Canceled job for server ID: {server['id']}")
            current_jobs = ', '.join([str(job[1]) for job in self.jobs])
            self.append_log(f"Current jobs:\n{self.format_jobs()}")
        else:
            self.append_log(f"No job found for server ID: {server['id']}")

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
        print("bar increased, progress value: ", progress_value)
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
        self.append_log("starting Jobs")

        for job in self.jobs:
            for _ in range(int(self.slider_delay)):  # Break the sleep into smaller intervals
                if not self.is_running:
                    if self.servers_loaded:
                        print("here")
                        self.get_counts_button.configure(state="enabled")
                    self.new_button.configure(text="Start")
                    self.append_log("Stopped deleting messages")
                    return
                time.sleep(1)  # Sleep for 1 second and check again
            get_and_del_all_messages_from_channel_search(
                self.auth_key,
                channel_id=job[0],
                author_id=self.user_data['id'],
                delay=lambda: self.slider_delay,  # Pass delay as a callable to get the updated value
                self=self,
                is_running=lambda: self.is_running,
                channel_name=job[1],
                is_guild=False
            )
        if self.servers_loaded:
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
        for i, (channel_id, widgets) in enumerate(self.scrollable_frame.dms_widgets.items(), start=1):
            label_text = widgets['label'].cget("text")  # Access the text of the label widget
            if self.file_data:
                sent_messages = get_count_messages_for_user(self.auth_key, channel_id,
                                                            author_id=self.user_data['id'], log=self.append_log)
                print(sent_messages)
                self.update_progress()
                self.append_log(
                    f"got message counts for {label_text.split(':', 1)[1].strip() if ':' in label_text else label_text.strip()}:{i}/{len(self.file_data)}")
                self.after(0, self.scrollable_frame.update_sent_messages, channel_id,
                           sent_messages)
                if not self.is_getting_message_counts:
                    self.get_counts_button.configure(text="Get message counts")
                    self.new_button.configure(state="enabled")
                    self.append_log("Stopped getting message counts.")
                    return
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

    def update_frame(self):
        print("Updating third frame")
        self.reset_progress_bar(len(self.file_data))
        print(len(self.file_data))
        if self.file_data:
            for i, (channel_id, description) in enumerate(self.file_data.items(), start=1):
                # u_id = get_userid_from_channelid(channel_id, self.auth_key)
                item_text = f"{i}. {description}"
                if not self.scrollable_frame.item_exists(channel_id):
                    self.scrollable_frame.add_item(item_text, dm={'id': channel_id, 'description': description})
                    self.update_progress()

        self.servers_loaded = True
        self.get_counts_button.configure(state="normal")
        self.open_all_dms_button.configure(state="normal")

    def format_jobs(self):
        formatted_jobs = [
            f"{index + 1}. {item.split(':', 1)[1].strip() if ':' in item else item.strip()}"
            for index, (_, item) in enumerate(self.jobs)
        ]
        return "\n".join(formatted_jobs)

    def update_data(self, auth_key, user_data, open_dms):
        self.auth_key = auth_key
        self.user_data = user_data
        self.open_dms = open_dms
        self.scrollable_frame.update_dms([dm['id'] for dm in self.open_dms], self.auth_key)
