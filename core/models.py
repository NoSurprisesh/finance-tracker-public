from datetime import datetime

class Entry:
    def __init__(self,
                 flow_type : str,
                 quantity : float,
                 currency : str,
                 date : datetime,
                 category: str,
                 note : str):
        self.flow_type = flow_type
        self.quantity = quantity
        self.currency = currency
        self.date = date
        self.category = category
        self.note = note

    def to_dict(self) -> dict:
        return {
            'flow_type': self.flow_type,
            'quantity': self.quantity,
            'currency': self.currency,
            'date': self.date.strftime('%Y-%m-%d'),
            'category': self.category,
            'note': self.note
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            flow_type = data['flow_type'],
            quantity = data['quantity'],
            currency = data['currency'],
            date = datetime.strptime(data['date'], '%Y-%m-%d'),
            category = data['category'],
            note = data['note'],
        )

class UserData:
    def __init__(self, username: str):
        self.username = username
        self.incomes: list[Entry] = []
        self.expenses: list[Entry] = []

    def add_entry(self, entry: Entry) -> None:
        if entry.flow_type == 'income':
            self.incomes.append(entry)
        elif entry.flow_type == 'expense' :
            self.expenses.append(entry)
        else:
            raise ValueError(f'Unknown flow_type: {entry.flow_type}')

    def get_balance(self) -> float:
        total_income = sum(entry.quantity for entry in self.incomes)
        total_expenses = sum(entry.quantity for entry in self.expenses)
        return total_income - total_expenses

    def edit_entry(self, index: int, flow_type: str, new_entry: Entry) -> None:
        if flow_type == 'income':
            self.incomes[index] = new_entry
        elif flow_type == 'expense':
            self.expenses[index] = new_entry
        else:
            raise ValueError(f'Unknown flow_type: {flow_type}')

    def remove_entry(self, index: int, flow_type) -> None:
        if flow_type == 'income':
            del self.incomes[index]
        elif flow_type == 'expense':
            del self.expenses[index]
        else:
            raise ValueError(f'Unknown flow_type: {flow_type}')





