import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import os
import datetime
import random
import pandas as pd
from io import BytesIO
import speech_recognition as sr  
from textblob import TextBlob  
import time 
st.set_page_config(
    page_title="Growth Mindset App",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

genai.configure(api_key="AIzaSyBhypGHX8U-B52fUJ4fJiy3q6mvVHOdZPc")

model = genai.GenerativeModel("gemini-pro")

def chat_with_gemini(prompt):
    """Generates a response from the Gemini AI model."""
    try:
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            return response.text
        else:
            return "Sorry, I couldn't generate a valid response. Please try again."
    except Exception as e:
        return f"An error occurred: {str(e)}"

response = chat_with_gemini("Hello, Gemini!")
print(response)

def get_motivation():
    motivations = [
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
        "It always seems impossible until it's done. - Nelson Mandela",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "The only way to do great work is to love what you do. - Steve Jobs"
    ]
    return random.choice(motivations)


def habit_tracker_app():
    st.title("📊 Habit Tracker")
    st.write("Track your daily habits and build a better routine! 🚀")

    if 'habits' not in st.session_state:
        st.session_state.habits = []

    habit = st.text_input("📝 Add a new habit:")
    frequency = st.selectbox("🔄 Frequency", ["Daily", "Weekly", "Monthly"])
    goal = st.number_input("🎯 Goal (e.g., times per week)", min_value=1, value=1)

    if st.button("Add Habit"):
        if habit:
            st.session_state.habits.append({
                "habit": habit,
                "frequency": frequency,
                "goal": goal,
                "progress": 0
            })
            st.success("Habit added successfully! 🎉")
        else:
            st.warning("Please enter a habit!")

    if st.session_state.habits:
        st.subheader("📋 Your Habits:")
        for i, habit in enumerate(st.session_state.habits, 1):
            st.write(f"{i}. {habit['habit']} - Frequency: {habit['frequency']} - Goal: {habit['goal']} times")
            progress = st.slider(f"Progress for {habit['habit']}", 0, habit['goal'], habit['progress'])
            st.session_state.habits[i-1]['progress'] = progress
            st.write(f"Progress: {progress}/{habit['goal']}")

            if st.button(f"Delete Habit {i}"):
                st.session_state.habits.pop(i-1)
                st.success("Habit deleted successfully! 🗑")
    else:
        st.info("No habits added yet. Add some habits to get started! 🌟")

def pomodoro_timer_app():
    st.title("⏳ Pomodoro Timer")
    st.write("Stay focused and productive with the Pomodoro Technique! 🍅")

    work_time = st.number_input("Work Time (minutes)", min_value=1, value=25)
    break_time = st.number_input("Break Time (minutes)", min_value=1, value=5)
    cycles = st.number_input("Number of Cycles", min_value=1, value=4)

    if st.button("Start Pomodoro Timer"):
        for cycle in range(cycles):
            st.write(f"Cycle {cycle + 1}: Work Time ⏳")
            time.sleep(work_time * 60)
            st.write(f"Cycle {cycle + 1}: Break Time ☕")
            time.sleep(break_time * 60)
        st.success("Pomodoro session completed! 🎉")

def journaling_app():
    st.title("📔 Journaling")
    st.write("Write daily journal entries to reflect on your thoughts and experiences. ✍️")

    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []

    date = st.date_input("Select Date", datetime.date.today())
    entry = st.text_area("📝 Write your journal entry:")

    if st.button("Save Journal Entry"):
        if entry:
            st.session_state.journal_entries.append({
                "date": date,
                "entry": entry
            })
            st.success("Journal entry saved successfully! 🎉")
        else:
            st.warning("Please write something in your journal entry!")

    if st.session_state.journal_entries:
        st.subheader("📜 Your Journal Entries:")
        for i, entry in enumerate(st.session_state.journal_entries, 1):
            st.write(f"{i}. Date: {entry['date']}")
            st.write(f"Entry: {entry['entry']}")
            if st.button(f"Delete Entry {i}"):
                st.session_state.journal_entries.pop(i-1)
                st.success("Journal entry deleted successfully! 🗑")
    else:
        st.info("No journal entries yet. Start writing to reflect on your day! 🌟")


def task_manager_app():
    st.title("✅ Task Manager")
    st.write("Organize your tasks and stay productive! 🚀")

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    task = st.text_input("📝 Add a new task:")
    priority = st.selectbox("🔝 Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("📅 Due Date", datetime.date.today())
    category = st.text_input("📂 Category (or select from existing)", "Work")
    
    if st.button("Add Custom Category"):
        if category:
            if 'custom_categories' not in st.session_state:
                st.session_state.custom_categories = []
            if category not in st.session_state.custom_categories:
                st.session_state.custom_categories.append(category)
                st.success(f"Custom category '{category}' added!")
            else:
                st.warning(f"Category '{category}' already exists!")
        else:
            st.warning("Please enter a category name!")

    if 'custom_categories' in st.session_state:
        all_categories = ["Work", "Personal", "Study", "Other"] + st.session_state.custom_categories
    else:
        all_categories = ["Work", "Personal", "Study", "Other"]
    
    category = st.selectbox("📂 Select Category", all_categories)

    if st.button("Add Task"):
        if task:
            st.session_state.tasks.append({
                "task": task,
                "priority": priority,
                "due_date": due_date,
                "category": category,
                "completed": False
            })
            st.success("Task added successfully!  ")
        else:
            st.warning("Please enter a task!")

    st.subheader("🔍 Sort Tasks")
    sort_by = st.selectbox("Sort by", ["Priority", "Due Date", "Category"])
    if sort_by == "Priority":
        sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x["priority"], reverse=True)
    elif sort_by == "Due Date":
        sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x["due_date"])
    elif sort_by == "Category":
        sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x["category"])
    else:
        sorted_tasks = st.session_state.tasks

    st.subheader("🔍 Filter Tasks")
    filter_by = st.selectbox("Filter by", ["All", "Completed", "Pending"])
    if filter_by == "Completed":
        filtered_tasks = [task for task in sorted_tasks if task["completed"]]
    elif filter_by == "Pending":
        filtered_tasks = [task for task in sorted_tasks if not task["completed"]]
    else:
        filtered_tasks = sorted_tasks

    if st.session_state.tasks:
        st.subheader("📋 Your Tasks:")
        for i, task in enumerate(filtered_tasks, 1):
            st.write(f"{i}. {task['task']} - Priority: {task['priority']} - Due: {task['due_date']} - Category: {task['category']}")
            if st.button(f"Complete Task {i}"):
                st.session_state.tasks[i-1]['completed'] = True
                st.success("Task marked as completed! 🎉")
            if st.button(f"Delete Task {i}"):
                st.session_state.tasks.pop(i-1)
                st.success("Task deleted successfully! 🗑")
    else:
        st.info("No tasks added yet. Add some tasks to get started! 🌟")

    st.subheader("⏰ Task Reminders")
    today = datetime.date.today()
    due_soon_tasks = [task for task in st.session_state.tasks if (task['due_date'] - today).days <= 2 and not task['completed']]
    
    if due_soon_tasks:
        st.warning("🚨 Tasks due soon:")
        for task in due_soon_tasks:
            st.write(f"- {task['task']} (Due: {task['due_date']})")
    else:
        st.info("No tasks due soon. Great job! 🎉")

def growth_mindset_app():
    st.title("🌱 Growth Mindset Challenge")

    st.header("Welcome to the Growth Mindset Challenge! 🌟")
    st.write(
        "A growth mindset is the belief that abilities can be developed through dedication and hard work. "
        "This web app is designed to help you track your progress, stay motivated, and cultivate a positive learning attitude. "
        "Remember, every challenge is an opportunity for growth! 🌟"
    )

    st.subheader("💬 Daily Affirmation")
    affirmations = [
        "You are capable of amazing things!",
        "Every small step you take brings you closer to your goals.",
        "Challenges are opportunities to grow stronger.",
        "You have the power to create positive change in your life.",
        "Believe in yourself, and you will achieve greatness."
    ]
    daily_affirmation = random.choice(affirmations)
    st.success(f"🌟 Today's Affirmation: {daily_affirmation}")

    st.subheader("📅 Daily Reflection")
    date = st.date_input("Select Date", datetime.date.today())
    reflection = st.text_area("📝 What did you learn today?")
    challenges = st.text_area("💡 What challenges did you face, and how did you overcome them?")
    next_goal = st.text_area("🎯 What is your next goal for improvement?")

    if st.button("✅ Submit Reflection"):
        if 'reflections' not in st.session_state:
            st.session_state.reflections = []
        st.session_state.reflections.append({
            "date": date,
            "reflection": reflection,
            "challenges": challenges,
            "next_goal": next_goal
        })
        st.success("Reflection Saved! Keep Growing! 🚀")

    st.subheader("📊 Progress Tracking")
    if 'reflections' in st.session_state and st.session_state.reflections:
        progress_data = {
            "Date": [entry["date"] for entry in st.session_state.reflections],
            "Reflection Length": [len(entry["reflection"]) for entry in st.session_state.reflections],
            "Challenges Length": [len(entry["challenges"]) for entry in st.session_state.reflections],
            "Next Goal Length": [len(entry["next_goal"]) for entry in st.session_state.reflections]
        }
        progress_df = pd.DataFrame(progress_data)
        st.line_chart(progress_df.set_index("Date"))
    else:
        st.info("No reflections yet. Start reflecting to track your progress! 🌟")

    st.subheader("🤝 Community Sharing")
    st.write("Share your reflections or goals with the community to inspire others!")
    share_reflection = st.text_area("✍️ Write something to share with the community:")
    if st.button("Share with Community"):
        if share_reflection:
            st.success("Your reflection has been shared with the community! 🌟")
        else:
            st.warning("Please write something to share!")

    st.header("💡 Growth Mindset Tips")
    st.write("✔ Embrace challenges as learning opportunities. 💪")
    st.write("✔ Learn from mistakes instead of fearing them. 🔄")
    st.write("✔ Celebrate effort and progress over perfection. 🎉")
    st.write("✔ Stay positive and keep pushing forward! 😊")
    st.write("✔ Seek feedback and use it as a tool for improvement. 🔧")
    st.write("✔ Visualize success and take small steps toward your goals. 🌈")
    st.write("✔ Surround yourself with positive and supportive people. 🤝")
    st.write("✔ Practice gratitude to stay motivated and focused. 🙏")

    if st.button("💖 Get Inspired"):
        st.success(get_motivation())

    st.header("🎯 Weekly Goal Setting")
    weekly_goal = st.text_area("What is your goal for this week?")
    if st.button("Set Weekly Goal"):
        if weekly_goal:
            st.success("Weekly goal set! Let's achieve it together! �")
        else:
            st.warning("Please enter a goal!")

    st.header("📅 Monthly Reflection")
    monthly_reflection = st.text_area("Reflect on your progress this month. What went well? What could be improved?")
    if st.button("Submit Monthly Reflection"):
        if monthly_reflection:
            st.success("Monthly reflection saved! Keep growing! 🌱")
        else:
            st.warning("Please write your reflection!")

    st.header("🙏 Gratitude Journal")
    gratitude_entry = st.text_area("What are you grateful for today?")
    if st.button("Submit Gratitude Entry"):
        if gratitude_entry:
            st.success("Gratitude entry saved! Practicing gratitude boosts positivity! 🌟")
        else:
            st.warning("Please write something you're grateful for!")

    st.header("📚 Resources for Growth")
    st.write("Here are some resources to help you on your growth journey:")
    st.write("- Books: 'Mindset' by Carol Dweck, 'Atomic Habits' by James Clear")
    st.write("- Podcasts: 'The Growth Mindset Podcast', 'The Tim Ferriss Show'")
    st.write("- Videos: TED Talks on growth mindset and personal development")
    st.write("- Courses: Online courses on Coursera, Udemy, or LinkedIn Learning")

    st.header("🤝 Join the Community")
    st.write("Connect with like-minded individuals and share your growth journey!")
    st.write("- Forums: Reddit communities like r/GetMotivated, r/PersonalDevelopment")
    st.write("- Social Media: Follow hashtags like #GrowthMindset, #PersonalGrowth")
    st.write("- Local Meetups: Join local groups focused on self-improvement and growth")

    st.write("---")
    st.write("Built with ❤ by Areesha Abdul Sattar | Stay motivated and keep growing! 🌱")
    st.write("📧 Contact: areesha21314@gmail.com")

def data_sweeper_app():
    st.title("📊 Data Sweeper")
    st.write("✨ Transform your files between CSV and Excel formats with built-in data cleaning and visualization 📈")

    uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[-1].lower()

            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue  

            st.write(f"📄 *File Name:* {file.name}")
            st.write(f"📏 *File Size:* {file.size / 1024:.2f} KB")

            st.write("👀 Preview the Head of the Dataframe")
            st.dataframe(df.head())

            st.subheader("🧹 Data Cleaning Options")
            if st.checkbox(f"🧽 Clean Data for {file.name}"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"🚫 Remove Duplicates from {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write("✅ Duplicates Removed!")

                    if st.button(f"📉 Remove Outliers from {file.name}"):
                        numeric_cols = df.select_dtypes(include=["number"]).columns
                        for col in numeric_cols:
                            Q1 = df[col].quantile(0.25)
                            Q3 = df[col].quantile(0.75)
                            IQR = Q3 - Q1
                            df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
                        st.write("✅ Outliers Removed!")

                with col2:
                    if st.button(f"🪣 Fill Missing Values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=["number"]).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✅ Missing Values have been Filled!")

                    if st.button(f"📊 Normalize Data for {file.name}"):
                        numeric_cols = df.select_dtypes(include=["number"]).columns
                        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
                        st.write("✅ Data Normalized!")

            st.subheader("🔍 Select Columns to Convert")
            columns = st.multiselect(f"📌 Choose Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            st.subheader("📊 Data Analysis")
            if st.checkbox(f"📈 Show Basic Statistics for {file.name}"):
                numeric_data = df.select_dtypes(include="number")
                if not numeric_data.empty:
                    st.write("📊 Basic Statistics:")
                    st.write(numeric_data.describe())
                else:
                    st.warning(f"⚠ No numeric columns found in {file.name} for analysis!")

            st.subheader("📊 Data Visualization")
            if st.checkbox(f"📈 Show visualization for {file.name}"):
                numeric_data = df.select_dtypes(include="number")
                st.write("📊 Numeric Data Preview:", numeric_data)

                if not numeric_data.empty and numeric_data.shape[1] >= 1:
                    st.bar_chart(numeric_data)
                else:
                    st.warning(f"⚠ No numeric columns found in {file.name} for visualization!")

            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"🔧 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"🔃 Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                st.download_button(
                    label=f"⬇ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

            st.subheader("☁️ Export Data")
            if st.button(f"📤 Export {file.name} to Cloud Storage (Simulated)"):
                st.success(f"✅ Data from {file.name} has been exported to cloud storage! (Simulated)")

    st.success("🎉 All files processed!")

def quizzes_app():
    st.title("🧠 Quizzes")
    st.write("Test your knowledge and learn something new!")

    if 'quizzes' not in st.session_state:
        st.session_state.quizzes = {
            "General": [
                {
                    "question": "What is the capital of France? 🇫🇷",
                    "options": ["Paris", "London", "Berlin", "Madrid"],
                    "answer": "Paris"
                },
                {
                    "question": "Which planet is known as the Red Planet? 🪐",
                    "options": ["Earth", "Mars", "Jupiter", "Saturn"],
                    "answer": "Mars"
                },
                {
                    "question": "Who wrote 'To Kill a Mockingbird'? 📚",
                    "options": ["Harper Lee", "Mark Twain", "J.K. Rowling", "Stephen King"],
                    "answer": "Harper Lee"
                }
            ],
            "Software Engineer": [
                {
                    "question": "What does HTML stand for? 🌐",
                    "options": ["Hyper Text Markup Language", "High-Level Text Machine Language", "Hyperlink and Text Markup Language", "Home Tool Markup Language"],
                    "answer": "Hyper Text Markup Language"
                },
                {
                    "question": "Which language is used for Android development? 📱",
                    "options": ["Java", "Python", "Swift", "C#"],
                    "answer": "Java"
                },
                {
                    "question": "What is the main use of Docker? 🐳",
                    "options": ["Virtualization", "Containerization", "Networking", "Data Storage"],
                    "answer": "Containerization"
                }
            ],
            "Doctor": [
                {
                    "question": "What is the largest organ in the human body? 🩺",
                    "options": ["Heart", "Skin", "Liver", "Brain"],
                    "answer": "Skin"
                },
                {
                    "question": "Which vitamin is produced by the human body when exposed to sunlight? ☀",
                    "options": ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin E"],
                    "answer": "Vitamin D"
                },
                {
                    "question": "What is the normal resting heart rate for adults? 💓",
                    "options": ["60-100 bpm", "40-60 bpm", "100-120 bpm", "120-140 bpm"],
                    "answer": "60-100 bpm"
                }
            ],
            "History": [
                {
                    "question": "Who was the first President of the United States? 🇺🇸",
                    "options": ["George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"],
                    "answer": "George Washington"
                },
                {
                    "question": "In which year did World War II end? 🌍",
                    "options": ["1945", "1939", "1941", "1950"],
                    "answer": "1945"
                },
                {
                    "question": "Who discovered America? 🚢",
                    "options": ["Christopher Columbus", "Vasco da Gama", "Ferdinand Magellan", "Marco Polo"],
                    "answer": "Christopher Columbus"
                }
            ],
            "Science": [
                {
                    "question": "What is the chemical symbol for water? 💧",
                    "options": ["H2O", "CO2", "O2", "NaCl"],
                    "answer": "H2O"
                },
                {
                    "question": "What is the speed of light? 🌌",
                    "options": ["299,792 km/s", "150,000 km/s", "450,000 km/s", "1,000,000 km/s"],
                    "answer": "299,792 km/s"
                },
                {
                    "question": "Who developed the theory of relativity? 🧠",
                    "options": ["Albert Einstein", "Isaac Newton", "Stephen Hawking", "Galileo Galilei"],
                    "answer": "Albert Einstein"
                }
            ]
        }

    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    if 'current_score' not in st.session_state:
        st.session_state.current_score = 0

    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = None

    quiz_category = st.selectbox("📚 Select Quiz Category", list(st.session_state.quizzes.keys()))
    quizzes = st.session_state.quizzes[quiz_category]

    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = 0

    if st.session_state.quiz_start_time is not None:
        elapsed_time = datetime.datetime.now() - st.session_state.quiz_start_time
        st.write(f"⏱️ Time Elapsed: {elapsed_time.seconds} seconds")

    if st.session_state.current_quiz < len(quizzes):
        quiz = quizzes[st.session_state.current_quiz]
        st.subheader(f"Question {st.session_state.current_quiz + 1}")
        st.write(quiz["question"])
        user_answer = st.radio("Options", quiz["options"])

        if st.button("Submit Answer"):
            if st.session_state.quiz_start_time is None:
                st.session_state.quiz_start_time = datetime.datetime.now()

            if user_answer == quiz["answer"]:
                st.session_state.current_score += 1
                st.success("Correct! 🎉")
            else:
                st.error(f"Wrong! The correct answer is {quiz['answer']}.")
            st.session_state.current_quiz += 1
    else:
        st.success("You have completed all the quizzes! 🎉")
        st.write(f"Your final score: {st.session_state.current_score}/{len(quizzes)}")

        if 'name' in st.session_state and st.session_state.name:
            st.session_state.scores[st.session_state.name] = st.session_state.current_score

        st.subheader("🏆 Leaderboard")
        if st.session_state.scores:
            leaderboard = pd.DataFrame(st.session_state.scores.items(), columns=["Name", "Score"])
            st.write(leaderboard.sort_values(by="Score", ascending=False))
        else:
            st.info("No scores yet. Be the first to top the leaderboard! 🌟")

        if st.button("Restart Quizzes"):
            st.session_state.current_quiz = 0
            st.session_state.current_score = 0
            st.session_state.quiz_start_time = None

def profile_app():
    st.title("👤 Profile")
    st.write("Update your profile information and view your analytics.")

    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'email' not in st.session_state:
        st.session_state.email = ""
    if 'profile_image' not in st.session_state:
        st.session_state.profile_image = None
    if 'social_media' not in st.session_state:
        st.session_state.social_media = {
            "twitter": "",
            "linkedin": "",
            "github": ""
        }
    if 'tasks_completed' not in st.session_state:
        st.session_state.tasks_completed = 0
    if 'quizzes_taken' not in st.session_state:
        st.session_state.quizzes_taken = 0

    st.subheader("📝 Profile Information")
    name = st.text_input("Name", st.session_state.name)
    email = st.text_input("Email", st.session_state.email)
    profile_image = st.file_uploader("Upload Profile Image", type=["jpg", "jpeg", "png"])

    st.subheader("🔗 Social Media Links")
    st.session_state.social_media["twitter"] = st.text_input("Twitter Profile URL", st.session_state.social_media["twitter"])
    st.session_state.social_media["linkedin"] = st.text_input("LinkedIn Profile URL", st.session_state.social_media["linkedin"])
    st.session_state.social_media["github"] = st.text_input("GitHub Profile URL", st.session_state.social_media["github"])

    if st.button("Update Profile"):
        st.session_state.name = name
        st.session_state.email = email
        if profile_image is not None:
            st.session_state.profile_image = profile_image
        st.success("Profile updated successfully! 🎉")

    if st.session_state.profile_image is not None:
        st.image(st.session_state.profile_image, caption="Your Profile Image", width=150)

    st.subheader("📊 Profile Analytics")
    if 'tasks' in st.session_state:
        st.session_state.tasks_completed = sum(1 for task in st.session_state.tasks if task["completed"])
    if 'quizzes' in st.session_state:
        st.session_state.quizzes_taken = len(st.session_state.quizzes)

    st.write(f"✅ Tasks Completed: {st.session_state.tasks_completed}")
    st.write(f"🧠 Quizzes Taken: {st.session_state.quizzes_taken}")

    st.subheader("🌐 Social Media Profiles")
    if st.session_state.social_media["twitter"]:
        st.write(f"🐦 Twitter: [{st.session_state.social_media['twitter']}]({st.session_state.social_media['twitter']})")
    if st.session_state.social_media["linkedin"]:
        st.write(f"🔗 LinkedIn: [{st.session_state.social_media['linkedin']}]({st.session_state.social_media['linkedin']})")
    if st.session_state.social_media["github"]:
        st.write(f"🐙 GitHub: [{st.session_state.social_media['github']}]({st.session_state.social_media['github']})")

def settings_app():
    st.title("⚙ Settings")
    st.write("Customize your app settings.")

    st.subheader("🎨 Custom Themes")
    theme_options = ["Light", "Dark", "Custom"]
    theme = st.selectbox("Select Theme", theme_options)

    if theme == "Custom":
        st.write("Create your custom theme:")
        primary_color = st.color_picker("Primary Color", "#00f")
        background_color = st.color_picker("Background Color", "#fff")
        text_color = st.color_picker("Text Color", "#000")

        if st.button("Apply Custom Theme"):
            custom_theme = {
                "primaryColor": primary_color,
                "backgroundColor": background_color,
                "textColor": text_color
            }
            st.session_state.custom_theme = custom_theme
            st.success("Custom theme applied! 🎉")
    else:
        st.session_state.custom_theme = None

    st.subheader("🌍 Language Support")
    languages = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese": "zh"
    }
    selected_language = st.selectbox("Select Language", list(languages.keys()))

    if st.button("Apply Language"):
        st.session_state.language = languages[selected_language]
        st.success(f"Language set to {selected_language}! 🌍")

    st.subheader("🔔 Notifications")
    notifications = st.checkbox("Enable Notifications", True)

    if st.button("Save Settings"):
        st.success("Settings saved successfully! 🎉")

def chatbot_app():
    st.title("🤖 Chatbot")
    st.write("Chat with our AI-powered chatbot in real-time!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_context" not in st.session_state:
        st.session_state.chat_context = []

    st.subheader("🎤 Voice Input")
    if st.button("Start Voice Input"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening... Speak now!")
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio)
                st.write(f"🎤 You said: {user_input}")
            except sr.UnknownValueError:
                st.error("Sorry, I could not understand the audio.")
                user_input = ""
            except sr.RequestError:
                st.error("Sorry, there was an issue with the speech recognition service.")
                user_input = ""
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(f"**You:** {user_input}")

            with st.spinner("Thinking..."):
                bot_response = chat_with_gemini(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                with st.chat_message("assistant"):
                    st.markdown(f"**Assistant:** {bot_response}")

    st.subheader("✍️ Text Input")
    user_input = st.chat_input("You: ")

    if user_input:
        blob = TextBlob(user_input)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            emotion = "positive"
        elif sentiment < 0:
            emotion = "negative"
        else:
            emotion = "neutral"

        st.session_state.chat_history.append({"role": "user", "content": user_input, "emotion": emotion})
        with st.chat_message("user"):
            st.markdown(f"**You:** {user_input}")

        context = st.session_state.chat_context
        if context:
            user_input = f"Context: {', '.join(context)}\n\nUser: {user_input}"

        with st.spinner("Thinking..."):
            bot_response = chat_with_gemini(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            st.session_state.chat_context.append(user_input)  
            with st.chat_message("assistant"):
                st.markdown(f"**Assistant:** {bot_response}")

    if st.session_state.chat_history:
        st.subheader("📜 Chat History:")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                if "emotion" in message:
                    st.markdown(f"**{message['role'].capitalize()} ({message['emotion']}):** {message['content']}")
                else:
                    st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")


def main():
    st.sidebar.title("🌱 Navigation")

    if 'name' not in st.session_state or st.session_state.name == "":
        st.session_state.name = st.sidebar.text_input("Enter your name:")
        st.session_state.email = st.sidebar.text_input("Enter your email:")

        if st.sidebar.button("Submit"):
            if st.session_state.name and st.session_state.email:
                st.sidebar.success(f"Welcome, {st.session_state.name}!")
            else:
                st.sidebar.warning("Please enter both name and email.")
        return  

    app_choice = st.sidebar.radio(
        "Choose an App:", 
        ["Data Sweeper", "Task Manager", "Chatbot", "Growth Mindset Challenge", "Quizzes", "Profile", "Settings", "Habit Tracker", "Pomodoro Timer", "Journaling"]
    )

    if app_choice == "Data Sweeper":
        data_sweeper_app()
    elif app_choice == "Task Manager":
        task_manager_app()
    elif app_choice == "Chatbot":
        chatbot_app()
    elif app_choice == "Growth Mindset Challenge":
        growth_mindset_app()
    elif app_choice == "Quizzes":
        quizzes_app()
    elif app_choice == "Profile":
        profile_app()
    elif app_choice == "Settings":
        settings_app()
    elif app_choice == "Habit Tracker":
        habit_tracker_app()
    elif app_choice == "Pomodoro Timer":
        pomodoro_timer_app()
    elif app_choice == "Journaling":
        journaling_app()

if __name__ == "__main__":
    main()