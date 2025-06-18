import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
    def __init__(self, controller, user):
        super().__init__(controller)
        self.controller = controller
        self.user = user

        ctk.CTkLabel(self, text="Main Menu", font=("Arial", 20)).pack(pady=20)

        ctk.CTkButton(self, text="➕ Add Entry", command=self.add_entry).pack(pady=10)
        ctk.CTkButton(self, text="📰 Show all entries", command=self.show_all_entries).pack(pady=10)
        ctk.CTkButton(self, text="💰 Show Balance", command=self.show_balance).pack(pady=10)
        ctk.CTkButton(self, text="💱 Change Currency", command=self.change_currency).pack(pady=10)
        ctk.CTkButton(self, text="❌ Exit", command=self.master.destroy).pack(pady=20)

    def add_entry(self):
        self.controller.show_add_entry_view()

    def show_all_entries(self):
        print("Switch to Show All Entries View")

    def show_balance(self):
        print("Switch to Balance View")

    def change_currency(self):
        print("Switch to Currency View")