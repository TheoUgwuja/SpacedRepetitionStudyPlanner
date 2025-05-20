Spaced Repetition Study Planner
A lightweight desktop application built with Python and Tkinter to help you plan and track your study sessions using spaced repetition.

![spaced planner screenshot](https://github.com/user-attachments/assets/119fe649-2eb3-4f18-9745-03e5369adccf)

Features
📅 Calendar view with color-coded study intensity

⏳ Spaced repetition schedule: reviews on Days 1, 2, 3, 5, and 7

📝 Session summary viewer

💾 Save/load your plan to JSON

🔁 Clear and reset your study plan anytime

How It Works
Launch the App
Run the script using Python:

bash
Copy
Edit
python spaced_repetition_planner.py
Add a Study Session

Enter a subject (e.g., "Math") in the text field.

Select a start date on the calendar.

Click Add to Plan.

Automatic Scheduling
The app generates 5 follow-up study dates spaced across 7 days using the spaced repetition method.

Visual Overview

Each date gets color-coded based on how many subjects are scheduled that day.

A summary pane lists all planned sessions.

Manage Your Plan

Click Save Plan to store your study schedule in study_plan.json.

Click Clear Plan to reset everything.

Click Info to view the color legend.

Requirements
Python 3.x

Required packages:

bash
Copy
Edit
pip install tkcalendar
Tkinter is included with most Python installations.

File Structure
pgsql
Copy
Edit
spaced_repetition_planner.py
study_plan.json  # (auto-generated after saving a plan)
License
This project is open-source and free to use.
