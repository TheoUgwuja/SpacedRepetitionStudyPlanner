import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import Calendar
from datetime import datetime, timedelta
import json

class StudySession:
    def __init__(self, subject):
        self.subject = subject
        self.dates = []

    def add_date(self, date, label):
        self.dates.append((date, label))

class SpacedRepetitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spaced Repetition Study Planner")
        self.sessions = []
        self.study_dates = {}
        self.setup_ui()
        self.load_plan()

    def setup_ui(self):
        self.root.configure(padx=10, pady=10)
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=0, column=0, sticky="ew")
        
        calendar_frame = ttk.Frame(self.root)
        calendar_frame.grid(row=1, column=0, sticky="ew")
        
        summary_frame = ttk.Frame(self.root)
        summary_frame.grid(row=2, column=0, sticky="ew")

        self.create_widgets(control_frame, calendar_frame, summary_frame)

    def create_widgets(self, control_frame, calendar_frame, summary_frame):
        self.calendar = Calendar(calendar_frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.pack(fill="both", expand=True)
        
        ttk.Label(control_frame, text="Subject:").grid(row=0, column=0)
        self.subject_entry = ttk.Entry(control_frame)
        self.subject_entry.grid(row=0, column=1, sticky="ew")
        
        plan_button = ttk.Button(control_frame, text="Add to Plan", command=self.add_to_plan)
        plan_button.grid(row=0, column=2)

        save_button = ttk.Button(control_frame, text="Save Plan", command=self.save_plan)
        save_button.grid(row=0, column=3)

        clear_button = ttk.Button(control_frame, text="Clear Plan", command=self.clear_plan)
        clear_button.grid(row=0, column=4)

        info_button = ttk.Button(control_frame, text="Info", command=self.show_info)
        info_button.grid(row=0, column=5)

        # Improved scrolled text widget for aesthetic summary display
        self.summary_label = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD, font=('Helvetica', 12), height=10, background="white")
        self.summary_label.pack(fill="both", expand=True)
        self.summary_label.tag_configure('date', font=('Helvetica', 12, 'bold'), background='lightgray', spacing1=10)
        self.summary_label.tag_configure('session', font=('Helvetica', 12), spacing3=5)

    def add_to_plan(self):
        subject = self.subject_entry.get()
        start_date = self.calendar.selection_get()
        if subject:
            new_session = StudySession(subject)
            study_days = [1, 2, 3, 5, 7]
            for i, day in enumerate(study_days):
                date = start_date + timedelta(days=day)
                session_label = f"{subject} (Cram)" if i == 0 else subject
                new_session.add_date(date, session_label)
                self.study_dates.setdefault(date, []).append(session_label)
            self.sessions.append(new_session)
            self.update_summary()
            self.update_calendar()
        else:
            messagebox.showerror("Error", "Please enter a subject.")

    def update_calendar(self):
        color_map = {1: "red", 2: "orange", 3: "yellow", 4: "green", 5: "blue", 6: "indigo", 7: "violet"}
        contrast_color_map = {1: "white", 2: "black", 3: "black", 4: "white", 5: "white", 6: "white", 7: "white"}
        for date, session_labels in self.study_dates.items():
            num_sessions = len(session_labels)
            background_color = color_map.get(num_sessions, "violet")
            foreground_color = contrast_color_map.get(num_sessions, "white")
            self.calendar.calevent_create(date, ', '.join(session_labels), tags=str(date))
            self.calendar.tag_config(str(date), background=background_color, foreground=foreground_color, font=('Helvetica', '10', 'bold'))

    def update_summary(self):
        self.summary_label.delete('1.0', tk.END)
        sorted_dates = sorted(self.study_dates.items())
        for date, session_labels in sorted_dates:
            date_str = date.strftime('%A, %B %d, %Y')
            self.summary_label.insert(tk.END, f"{date_str}:\n", 'date')
            for label in session_labels:
                self.summary_label.insert(tk.END, f"  - {label}\n", 'session')

    def show_info(self):
        info_text = ("Color Key:\n"
                     "1 Subject: Red\n"
                     "2 Subjects: Orange\n"
                     "3 Subjects: Yellow\n"
                     "4 Subjects: Green\n"
                     "5 Subjects: Blue\n"
                     "6 Subjects: Indigo\n"
                     "7+ Subjects: Violet")
        messagebox.showinfo("Color Information", info_text)

    def save_plan(self):
        with open('study_plan.json', 'w') as f:
            json.dump({str(date): sessions for date, sessions in self.study_dates.items()}, f)
        messagebox.showinfo("Save Successful", "The study plan has been saved to 'study_plan.json'.")

    def clear_plan(self):
        self.study_dates.clear()
        self.sessions.clear()
        self.calendar.calevent_remove('all')
        self.update_summary()
        messagebox.showinfo("Clear Successful", "The study plan has been cleared.")

    def load_plan(self):
        try:
            with open('study_plan.json', 'r') as f:
                data = json.load(f)
                for date_str, sessions in data.items():
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    self.study_dates[date] = sessions
            self.update_calendar()
            self.update_summary()
        except FileNotFoundError:
            print("No saved plan found. Starting fresh.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the saved plan: {e}")

def main():
    root = tk.Tk()
    app = SpacedRepetitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

