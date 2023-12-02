import tkinter as tk
import ipaddress
import subprocess
from PIL import Image, ImageTk

class TowerDefenseLauncher(tk.Tk):
    """
    A Tkinter-based GUI application for launching a tower defense game.

    This application allows users to select whether they want to be an attacker or a defender,
    input the IP address and port number for network connectivity, and choose to either join
    or host a game.

    Attributes:
        selected_value (tk.IntVar): Holds the value indicating the selected role (attacker/defender).
        ip_entry (tk.Entry): Text entry widget for the IP address.
        port_entry (tk.Entry): Text entry widget for the port number.
    """

    def __init__(self):
        """
        Initialize the TowerDefenseLauncher application, setting up the main window,
        title, and geometry. Also, it initializes the GUI widgets.
        """
        super().__init__()
        self.title("Tower Defense Launcher")
        self.geometry("500x500")

        self.load_background_image("assets/background.png")

        self.selected_value = tk.IntVar(value=0)
        self.message_label = None
        self.create_widgets()

    def load_background_image(self, image_path):
        """
        Load and set the background image.

        :param image_path: Path to the background image file.
        """
        # Load the image
        self.background_image = Image.open(image_path)
        self.background_image = self.background_image.resize((500, 500))  # Resize image
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a Label or Canvas to hold the background image
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch to the size of the window


    def create_widgets(self):
        """
        Create and layout the widgets in the main application window, including labels,
        radio buttons for role selection, text entries for IP and port, and buttons for
        joining or hosting a game.
        """
         # Create a frame for other widgets that will be on top of the background
        main_frame = tk.Frame(self, bd=1)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame


        radio_frame = tk.Frame(main_frame)  # Frame for radio buttons
        radio_frame.pack(pady=(5, 10))
        tk.Radiobutton(radio_frame, text="Attacker", variable=self.selected_value, value=1, command=self.clear_message).pack(side=tk.LEFT)
        tk.Radiobutton(radio_frame, text="Defender", variable=self.selected_value, value=2, command=self.clear_message).pack(side=tk.LEFT)

        # IP and Port entries
        tk.Label(main_frame, text="IP address").pack()
        self.ip_entry = tk.Entry(main_frame, bg="white", fg="black")
        self.ip_entry.pack(pady=(0, 5))
        self.ip_entry.bind("<Key>", lambda event: self.clear_message())

        tk.Label(main_frame, text="Port").pack()
        self.port_entry = tk.Entry(main_frame, bg="white", fg="black")
        self.port_entry.pack(pady=(0, 0))
        self.port_entry.bind("<Key>", lambda event: self.clear_message())

        # Buttons
        button_frame = tk.Frame(main_frame)  # Frame for buttons
        button_frame.pack(pady=(5, 0))
        tk.Button(button_frame, text="Join", command=self.join_game).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Host", command=self.host_game).pack(side=tk.LEFT, padx=5)
       
        # Message label
        self.message_label = tk.Label(main_frame, fg="red")
        self.message_label.pack()

    def is_valid_ip(self, ip):
        """
        Validate the IP address.

        :param ip: String representing the IP address.
        :return: True if the IP is valid, False otherwise.
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def is_valid_port(self, port):
        """
        Validate the port number.

        :param port: String representing the port number.
        :return: True if the port is valid, False otherwise.
        """
        try:
            return 0 <= int(port) <= 65535
        except ValueError:
            return False

    def validate_inputs(self):
        """
        Validates the user inputs for role selection, IP address, and port.
        Returns True if all validations pass, otherwise shows an error message and returns False.
        """
        error_messages = []

        if self.selected_value.get() == 0:
            error_messages.append("Please select Attacker or Defender.")

        if not self.is_valid_ip(self.ip_entry.get()):
            error_messages.append("Invalid IP address.")

        if not self.is_valid_port(self.port_entry.get()):
            error_messages.append("Invalid port.")

        if error_messages:
            self.show_message(error_messages)
            return False

        return True

    def join_game(self):
        if not self.validate_inputs():
            return
        # Add logic for joining a game
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        print(f"Joining game at IP: {ip}, Port: {port}")
        subprocess.Popen(["python3", "game2.py", "--ip", ip, "--port",  port])  


    def host_game(self):
        if not self.validate_inputs():
            return
        # Add logic for hosting a game
        ip = self.ip_entry.get()
        port = self.port_entry.get()

        print(f"Hosting game at IP: {ip}, Port: {port}")

        subprocess.Popen(["python3", "server.py", "--ip", ip, "--port",  port])
        subprocess.Popen(["python3", "game2.py", "--ip", ip, "--port",  port])  

    def show_message(self, messages):
        """
        Display a message in the GUI.

        :param message: List of strings representing the messages to display.
        """
        if self.message_label is None:
            self.message_label = tk.Label(self, fg="red")
            self.message_label.pack()

        # Check if messages is a list and join, otherwise use it as is
        full_message = "\n".join(messages) if isinstance(messages, list) else messages
        self.message_label.config(text=full_message)

    def clear_message(self):
        """
        Clear the error message displayed in the GUI.
        """
        if self.message_label is not None:
            self.message_label.config(text="")

if __name__ == "__main__":
    launcher = TowerDefenseLauncher()
    launcher.mainloop()