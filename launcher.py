import tkinter as tk

class TowerDefenseLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tower Defense Launcher")
        self.geometry("500x300")

        # Define IntVar() for selected value
        self.selected_value = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        self.intro_label = tk.Label(self, text="Choose your side:").pack()
        
        self.attacker = tk.Radiobutton(
            self,
            text="Attacker",
            padx=0,
            pady=5,
            variable=self.selected_value,
            value=1
        ).pack()

        self.defender = tk.Radiobutton(
            self,
            text="Defender",
            padx=5,
            pady=5,
            variable=self.selected_value,
            value=2
        ).pack()

        self.ip_label = tk.Label(
            self,
            text="IP address"
        ).pack()

        self.ip = tk.Text(
            self,
            height=1,
            width=25,
            bg="white",
        ).pack()
        
        self.ip_label = tk.Label(
            self,
            text="Port"
        ).pack()

        self.port = tk.Text(
            self,
            height=1,
            width=25,
            bg="white"
        ).pack()

        self.join = tk.Button(
            self,
            text="Join",
            padx=5,
            pady=5,
        ).pack()

        self.host = tk.Button(
            self,
            text="Host",
            padx=5,
            pady=5,
        ).pack()

if __name__ == "__main__":
    launcher = TowerDefenseLauncher()
    launcher.mainloop()