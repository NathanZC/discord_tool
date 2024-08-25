import os

from frames.closed_dms import ForthFrame
from frames.homeframegui import *
from frames.instructions import Instructions
from frames.opendmsframegui import *
from frames.accessibleserversframegui import *

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DiscordTool.py")
        self.geometry("1500x800")
        self.auth_key = ''
        self.open_dms = []
        self.user_data = {}
        self.servers = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Load images
        self.load_images()

        # Create navigation frame
        self.create_navigation_frame()

        # Create frames
        self.home_frame = HomeFrame(self, self.auth_key)
        self.second_frame = SecondFrame(self, self.auth_key, self.open_dms, self.user_data)
        self.third_frame = ThirdFrame(self, self.auth_key, self.servers, self.user_data)
        self.fourth_frame = ForthFrame(self, self.auth_key, self.open_dms, self.user_data)
        self.fifth_frame = Instructions(self)

        # Select default frame
        self.select_frame_by_name("home")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.second_frame.reset()
        self.select_frame_by_name("frame_2")
        self.second_frame.update_data(self.auth_key, self.open_dms, self.user_data)
        self.second_frame.dms_loaded = False
        self.second_frame.get_counts_button.configure(state="disabled")
        threading.Thread(target=self.second_frame.update_second_frame).start()

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        #hi2
        print("selected frame 3 ")
        self.third_frame.update_data(self.auth_key, self.servers, self.user_data)
        self.third_frame.get_counts_button.configure(state="disabled")
        threading.Thread(target=self.third_frame.update_third_frame).start()

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
        self.fourth_frame.update_data(self.auth_key, self.user_data, self.open_dms)

    def strong_indexing_search_button_event(self):
        self.select_frame_by_name("frame_5")

    def load_images(self):

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                                       size=(500, 200))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20)
        )
        self.chat_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20)
        )
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20)
        )
        self.server_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "server2.png")),
            dark_image=Image.open(os.path.join(image_path, "server.png")), size=(20, 20)
        )
        self.search_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "help.png")),
            dark_image=Image.open(os.path.join(image_path, "help2.png")), size=(20, 20)
        )

    def create_navigation_frame(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="Discord Tool", image=self.logo_image,
            compound="left", font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Auth",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.home_image, anchor="w", command=self.home_button_event
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="View Open Dms",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.chat_image, anchor="w", command=self.frame_2_button_event, state="disabled"
        )
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Accessible Servers",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.server_image, anchor="w", command=self.frame_3_button_event, state="disabled"
        )
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Find Closed Dms",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w", command=self.frame_4_button_event, state="disabled"
        )
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.strong_indexing_search_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="How to use",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.search_image, anchor="w", command=self.strong_indexing_search_button_event, state="enabled"
        )
        self.strong_indexing_search_button.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame, values=["Light", "Dark", "System"],
            command=change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

    def create_strong_indexing_search_frame(self):
        frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        return frame

    def select_frame_by_name(self, name):
        # Set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.strong_indexing_search_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")

        # Show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fifth_frame.grid_forget()

    def update_button_states(self, selected_frame, enable_all):
        buttons = {
            "home": self.home_button,
            "frame_2": self.frame_2_button,
            "frame_3": self.frame_3_button,
            "frame_4": self.frame_4_button,
            "frame_5": self.strong_indexing_search_button
        }
        for frame_name, button in buttons.items():
            if frame_name == selected_frame:
                button.configure(state="disabled")
            else:
                button.configure(state="normal" if enable_all else "disabled")

    def update_data(self, auth_key, open_dms, user_data, servers):
        self.auth_key = auth_key
        self.open_dms = get_all_open_dms(auth_key)
        self.user_data = user_data
        self.servers = servers


if __name__ == "__main__":
    app = App()
    app.mainloop()
