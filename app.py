import streamlit as st
import datetime
import random

def get_motivation():
    motivations = [
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
        "It always seems impossible until it's done. - Nelson Mandela",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "The only way to do great work is to love what you do. - Steve Jobs"
    ]
    return random.choice(motivations)

def task_manager_app():
    st.title("✅ Task Manager")
    st.write("Organize your tasks and stay productive! 🚀")

    task = st.text_input("📝 Add a new task:")
    priority = st.selectbox("🔝 Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("📅 Due Date", datetime.date.today())
    category = st.selectbox("📂 Category", ["Work", "Personal", "Study", "Other"])

    if st.button("Add Task"):
        if task:
            if 'tasks' not in st.session_state:
                st.session_state.tasks = []
            st.session_state.tasks.append({
                "task": task,
                "priority": priority,
                "due_date": due_date,
                "category": category,
                "completed": False
            })
            st.success("Task added successfully! 🎉")
        else:
            st.warning("Please enter a task!")

    if 'tasks' in st.session_state and st.session_state.tasks:
        st.subheader("📋 Your Tasks:")
        for i, task in enumerate(st.session_state.tasks, 1):
            st.write(f"{i}. {task['task']} - Priority: {task['priority']} - Due: {task['due_date']} - Category: {task['category']}")
            if st.button(f"Complete Task {i}"):
                st.session_state.tasks[i-1]['completed'] = True
                st.success("Task marked as completed! 🎉")
            if st.button(f"Delete Task {i}"):
                st.session_state.tasks.pop(i-1)
                st.success("Task deleted successfully! 🗑")
    else:
        st.info("No tasks added yet. Add some tasks to get started! 🌟")

def growth_mindset_app():
    st.title("🌱 Growth Mindset Challenge")

    st.header("Welcome to the Growth Mindset Challenge! 🚀")
    st.write(
        "A growth mindset is the belief that abilities can be developed through dedication and hard work. "
        "This web app is designed to help you track your progress, stay motivated, and cultivate a positive learning attitude. "
        "Remember, every challenge is an opportunity for growth! 🌟"
    )

    st.subheader("📅 Daily Reflection")
    date = st.date_input("Select Date", datetime.date.today())
    reflection = st.text_area("📝 What did you learn today?")
    challenges = st.text_area("💡 What challenges did you face, and how did you overcome them?")
    next_goal = st.text_area("🎯 What is your next goal for improvement?")

    if st.button("✅ Submit Reflection"):
        st.success("Reflection Saved! Keep Growing! 🚀")

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

    st.header("📌 Track Your Progress")
    st.write("🗂 Keep a journal of your reflections and review your progress over time!")
    st.write("📊 Set weekly or monthly growth goals to measure your improvement.")
    st.write("🔄 Stay consistent and celebrate small wins!")

    progress = st.slider("📈 How motivated do you feel today?", 0, 100, 50)
    if progress >= 75:
        st.success("🔥 Amazing! Keep up the great work!")
    elif progress >= 50:
        st.info("💪 You're doing great! Keep pushing forward!")
    else:
        st.warning("🌟 Keep going! Every small effort matters!")

    st.header("🎯 Weekly Goal Setting")
    weekly_goal = st.text_area("What is your goal for this week?")
    if st.button("Set Weekly Goal"):
        st.success("Weekly goal set! Let's achieve it together! 🚀")

    st.header("📅 Monthly Reflection")
    monthly_reflection = st.text_area("Reflect on your progress this month. What went well? What could be improved?")
    if st.button("Submit Monthly Reflection"):
        st.success("Monthly reflection saved! Keep growing! 🌱")

    st.header("🙏 Gratitude Journal")
    gratitude_entry = st.text_area("What are you grateful for today?")
    if st.button("Submit Gratitude Entry"):
        st.success("Gratitude entry saved! Practicing gratitude boosts positivity! 🌟")

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
                    "question": "Which vitamin is produced by the human body when exposed to sunlight? ☀️",
                    "options": ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin E"],
                    "answer": "Vitamin D"
                },
                {
                    "question": "What is the normal resting heart rate for adults? 💓",
                    "options": ["60-100 bpm", "40-60 bpm", "100-120 bpm", "120-140 bpm"],
                    "answer": "60-100 bpm"
                }
            ]
        }

    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = 0

    profession = st.session_state.profession if 'profession' in st.session_state else "General"
    quiz_category = profession if profession in st.session_state.quizzes else "General"
    quizzes = st.session_state.quizzes[quiz_category]

    if st.session_state.current_quiz < len(quizzes):
        quiz = quizzes[st.session_state.current_quiz]
        st.subheader(f"Question {st.session_state.current_quiz + 1}")
        st.write(quiz["question"])
        user_answer = st.radio("Options", quiz["options"])
        if st.button("Submit Answer"):
            if user_answer == quiz["answer"]:
                st.success("Correct! 🎉")
            else:
                st.error(f"Wrong! The correct answer is {quiz['answer']}.")
            st.session_state.current_quiz += 1
    else:
        st.success("You have completed all the quizzes! 🎉")
        if st.button("Restart Quizzes"):
            st.session_state.current_quiz = 0

def profile_app():
    st.title("👤 Profile")
    st.write("Update your profile information.")

    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'profession' not in st.session_state:
        st.session_state.profession = "General"
    if 'profile_image' not in st.session_state:
        st.session_state.profile_image = None

    name = st.text_input("Name", st.session_state.name)
    profession = st.selectbox("Profession", ["Software Engineer", "Doctor", "Teacher", "Other"], index=0 if st.session_state.profession not in ["Software Engineer", "Doctor", "Teacher"] else ["Software Engineer", "Doctor", "Teacher"].index(st.session_state.profession))
    profile_image = st.file_uploader("Upload Profile Image", type=["jpg", "jpeg", "png"])

    if st.button("Update Profile"):
        st.session_state.name = name
        st.session_state.profession = profession
        if profile_image is not None:
            st.session_state.profile_image = profile_image
        st.success("Profile updated successfully! 🎉")

    if st.session_state.profile_image is not None:
        st.image(st.session_state.profile_image, caption="Your Profile Image", width=150)

def settings_app():
    st.title("⚙️ Settings")
    st.write("Customize your app settings.")

    theme = st.selectbox("Theme", ["Light", "Dark"])
    notifications = st.checkbox("Enable Notifications", True)

    if st.button("Save Settings"):
        st.success("Settings saved successfully! 🎉")

def main():
    st.sidebar.title("🌱 Navigation")
    if 'name' not in st.session_state or st.session_state.name == "":
        st.session_state.name = st.text_input("Enter your name:")
        st.session_state.profession = st.selectbox("Enter your profession:", ["Software Engineer", "Doctor", "Teacher", "Other"])
        if st.session_state.name and st.session_state.profession:
            st.success(f"Welcome, {st.session_state.name} ({st.session_state.profession})!")
        else:
            return

    app_choice = st.sidebar.radio("Choose an App:", ["Task Manager", "Growth Mindset Challenge", "Quizzes", "Profile", "Settings"])

    if app_choice == "Task Manager":
        task_manager_app()
    elif app_choice == "Growth Mindset Challenge":
        growth_mindset_app()
    elif app_choice == "Quizzes":
        quizzes_app()
    elif app_choice == "Profile":
        profile_app()
    elif app_choice == "Settings":
        settings_app()

if __name__ == "__main__":
    main()