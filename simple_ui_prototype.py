from tkinter import *
from PIL import ImageTk, Image

class PoIInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("PoI Network Interface")
        self.window.geometry("600x400")
        self.window.resizable(False, False)

        # Background Image
        self.background_image = ImageTk.PhotoImage(Image.open("background.jpg"))
        self.background_label = Label(self.window, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title Label
        self.title_label = Label(self.window, text="PoI Network Interface", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=20)

        # Text Entry
        self.text_label = Label(self.window, text="Enter Interaction Data:")
        self.text_label.pack(pady=10)
        self.text_entry = Entry(self.window, width=50)
        self.text_entry.pack()

        # Public Key Entry
        self.pubkey_label = Label(self.window, text="Enter Public Key:")
        self.pubkey_label.pack(pady=10)
        self.pubkey_entry = Entry(self.window, width=50)
        self.pubkey_entry.pack()

        # Private Key Entry
        self.privkey_label = Label(self.window, text="Enter Private Key:")
        self.privkey_label.pack(pady=10)
        self.privkey_entry = Entry(self.window, width=50)
        self.privkey_entry.pack()

        # Points Entry
        self.points_label = Label(self.window, text="Enter Points:")
        self.points_label.pack(pady=10)
        self.points_entry = Entry(self.window, width=50)
        self.points_entry.pack()

        # Submit Button
        self.submit_button = Button(self.window, text="Submit", command=self.submit_interaction)
        self.submit_button.pack(pady=20)

        # Result Label
        self.result_label = Label(self.window, text="")
        self.result_label.pack()

    def submit_interaction(self):
        data = self.text_entry.get()
        pubkey = self.pubkey_entry.get()
        privkey = self.privkey_entry.get()
        points = self.points_entry.get()

        # Code to submit interaction to the PoI Network

        self.result_label.config(text="Interaction Submitted")

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    ui = PoIInterface()
    ui.run()
