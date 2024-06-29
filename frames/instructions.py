import customtkinter as ctk


class Instructions(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)  # Configure the column to expand and fill available space
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="How to Use", font=("Roboto", 18, "bold"))
        self.title_label.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        # Instructions Text
        instructions_text = (
            "Welcome to DiscordTool.py!\n\n"
            "1. Authentication: Start by authenticating your session with your Discord auth key. To get this key you "
            "can go into the network tab on the browser after logging in. To do this Press CTL + SHIT + I, go to the "
            "network tab look for a request with the auth token. you might be able to press CTL + SHIFT + I in the desktop"
            "discord app and find it depending on settings (Be careful with this token!!!). "
            "Then copy it and paste it in the auth tab.\n\n"
            "2. Once you are authenticated you will be able to use the other tabs.\n\n"
            "3. To delete messages check the boxes you would like to delete dms with and the press start at the top "
            "and it will start deleting all dms with selected users in order. \n\n"
            "4. Find Closed DMs: To do this you must request data from discord and then once you get the files. Go to "
            "the messages > index.json file and put it as input.\n\n"
            "5. You may change delay between message deletions and getting the message counts to try and avoid rate "
            "limits\n\n"
            "For any issues just try restarting the program or open an issue on github"
        )
        self.instructions_label = ctk.CTkLabel(self, text=instructions_text, justify="left", wraplength=800)
        self.instructions_label.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

        # You can adjust the row and column parameters as needed to fit your layout
