
import customtkinter

from api_requests import get_all_open_dms, get_user_data, get_user_guilds
from gui import App


class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master: App, auth_key):
        super().__init__(master)
        self.master = master
        self.auth_key = auth_key

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=3)

        # Add ScrollableLabelButtonFrame
        frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, columnspan=4, sticky="nsew")  # Place frame in HomeFrame grid
        self.home_frame_large_image_label = customtkinter.CTkLabel(frame, text="", image=self.master.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.auth_key_label = customtkinter.CTkLabel(frame, text="Discord Auth Key:")
        self.auth_key_label.grid(row=1, column=0, padx=20, pady=(20, 5), sticky="ew")

        self.auth_key_entry = customtkinter.CTkEntry(frame, placeholder_text="Enter your auth key", show="*")
        self.auth_key_entry.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.submit_key_button = customtkinter.CTkButton(frame, text="Submit Key", command=self.submit_auth_key)
        self.submit_key_button.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="ew")

        self.auth_key_status = customtkinter.CTkLabel(frame, text="", text_color="red")
        self.auth_key_status.grid(row=4, column=0, padx=20, pady=(5, 20), sticky="ew")

    def submit_auth_key(self):
        auth_key = self.auth_key_entry.get()
        data = get_all_open_dms(auth_key)
        if data is not None:
            self.auth_key = auth_key
            self.master.update_data(self.auth_key, data, get_user_data(auth_key), get_user_guilds(auth_key))
            # pprint.pprint(data)
            self.auth_key_status.configure(text="Key is valid!", text_color="green")
            self.master.update_button_states("home", True)  # Enable other frames
        else:
            self.auth_key_status.configure(text="Invalid Auth Key", text_color="red")
            self.master.update_button_states("home", False)  # Keep other frames disabled