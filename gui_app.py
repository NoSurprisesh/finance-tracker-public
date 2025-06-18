import customtkinter as ctk
from ui.views.main_menu import MainMenu
from ui.views.add_entry_view import AddEntryView
from core.models import UserData

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class FinanceTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Finance Tracker")
        self.geometry("500x400")

        #Here would be a user load
        self.user = UserData("TestUser")

        # container
        self.current_view = MainMenu(self, self.user)
        self.show_main_menu()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_main_menu(self):
        self.clear_view()
        self.current_view = MainMenu(self, self.user)
        self.current_view.pack(expand=True, fill="both")

    def show_add_entry_view(self):
        self.clear_view()
        self.current_view = AddEntryView(self, self.user, self.show_main_menu)
        self.current_view.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.mainloop()
