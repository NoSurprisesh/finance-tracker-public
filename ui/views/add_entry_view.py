import customtkinter as ctk


class AddEntryView(ctk.CTkFrame):
    def __init__(self, master, user, go_back):
        super().__init__(master)
        self.user = user
        self.go_back = go_back

        ctk.CTkLabel(self, text='Add Entry', font=('Arial', 20)).pack(pady=20)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text='Amount')
        self.amount_entry.pack(pady=10)

        self.type_option = ctk.CTkOptionMenu(self, values=['income', 'expense'])
        self.type_option.set('income')
        self.type_option.pack(pady=10)

        self.currency_option = ctk.CTkOptionMenu(self, values=['USD', 'EUR', 'PLN'])
        self.currency_option.set(user.base_currency)
        self.currency_option.pack(pady=10)

        self.category_entry = ctk.CTkEntry(self, placeholder_text='Category')
        self.category_entry.pack(pady=10)

        self.note_entry = ctk.CTkEntry(self, placeholder_text='Note')
        self.note_entry.pack(pady=10)

        ctk.CTkButton(self, text='Save', command=self.save_entry).pack(pady=15)
        ctk.CTkButton(self, text='Back', command=self.go_back).pack()

    def save_entry(self):
        amount = self.amount_entry.get()
        flow_type = self.type_option.get()
        currency = self.currency_option.get()
        category = self.category_entry.get()
        note = self.note_entry.get()

        # for save_new_entry()
        print(f"Saving entry: {amount} {currency} as {flow_type} "
              f"in category {category}, with note {note}.")