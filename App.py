from st_pages import Page, add_page_title, show_pages


show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Page("chatbot.py", "Chatbot Guru", "🤖"),
        # The pages appear in the order you pass them
        Page("Tutor.py", "AI Tutor", "🧑‍🏫"),
        Page("Path_planner.py", "Path Planning", "✏"),
        Page("Quiz.py", "Quiz", "📖"),
        Page("Interview.py", "Interview", "🎙️"),
        
    ]
)

add_page_title()  # Optional method to add title and icon to current page
