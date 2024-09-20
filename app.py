import streamlit as st
import pandas as pd
from datetime import datetime

# Define the schedule data
schedule_data = {
    'Monday': {
        'Active Listening': '30 minutes: Listen to a podcast on a topic of interest (e.g., history, science). Take notes on key points.',
        'Speaking Practice': '20 minutes: Role-play a job interview or customer service scenario with a language partner or tutor.',
        'Reading Comprehension': '30 minutes: Read a news article from an English online newspaper. Summarize the main idea and key details.',
        'Writing Skills': '20 minutes: Write a journal entry about your weekend activities and plans for the week.',
        'Vocabulary Expansion': '15 minutes: Create a list of 10 new words from today\'s podcast and article. Use flashcards to study them.',
        'Grammar Fundamentals': '15 minutes: Practice using past tense verbs in 5 sentences about yesterday\'s events.'
    },
    'Tuesday': {
        'Active Listening': '30 minutes: Watch a short (15-20 min) video lecture or TED talk. Focus on understanding the main argument.',
        'Speaking Practice': '20 minutes: Describe your favorite book or movie to a friend or in a voice memo.',
        'Reading Comprehension': '30 minutes: Read a chapter of a book or a story. Note any unfamiliar words and look up their meanings.',
        'Writing Skills': '20 minutes: Write a short review of the video lecture or TED talk you listened to.',
        'Vocabulary Expansion': '15 minutes: Study vocabulary related to hobbies and leisure activities. Use them in sentences.',
        'Grammar Fundamentals': '15 minutes: Complete exercises on conjunctions and practice forming complex sentences.'
    },
    'Wednesday': {
        'Active Listening': '30 minutes: Listen to an English radio channel or playlist. Focus on understanding lyrics or spoken content.',
        'Speaking Practice': '20 minutes: Record yourself talking about your daily routine, using varied vocabulary and expressions.',
        'Reading Comprehension': '30 minutes: Read an opinion piece or editorial. Answer comprehension questions about the author\'s viewpoint.',
        'Writing Skills': '20 minutes: Write an email to a friend describing your experience with learning English so far.',
        'Vocabulary Expansion': '15 minutes: Learn 10 new idiomatic expressions. Try to use them during the day.',
        'Grammar Fundamentals': '15 minutes: Practice forming conditional sentences (e.g., If I were...).'
    },
    'Thursday': {
        'Active Listening': '30 minutes: Listen to a cooking show or recipe video. Write down the steps and ingredients.',
        'Speaking Practice': '20 minutes: Explain the recipe you listened to in your own words, either to a partner or in a recording.',
        'Reading Comprehension': '30 minutes: Read a how-to guide or tutorial. Summarize the main steps.',
        'Writing Skills': '20 minutes: Write your own how-to guide on a topic you know well.',
        'Vocabulary Expansion': '15 minutes: Create a themed vocabulary list (e.g., restaurant phrases). Practice using them in dialogue.',
        'Grammar Fundamentals': '15 minutes: Review and practice relative clauses (e.g., who, which, that).'
    },
    'Friday': {
        'Active Listening': '30 minutes: Watch an episode of an English TV sitcom. Note down any interesting phrases or slang.',
        'Speaking Practice': '20 minutes: Have a casual conversation with a language exchange partner or friend.',
        'Reading Comprehension': '30 minutes: Read an interesting blog post or online article. Write a brief commentary on it.',
        'Writing Skills': '20 minutes: Compose a blog post or a social media update about something exciting you learned or did this week.',
        'Vocabulary Expansion': '15 minutes: Review the week\'s new vocabulary. Create a short story using at least 10 new words.',
        'Grammar Fundamentals': '15 minutes: Practice advanced prepositions and their uses in context.'
    },
    'Saturday': {
        'Active Listening': '30 minutes: Join a live streaming event or webinar in English. Pay attention to the Q&A session.',
        'Speaking Practice': '20 minutes: Discuss what you learned from the live stream in a small study group or with friends.',
        'Reading Comprehension': '30 minutes: Read a chapter of a non-fiction book or a detailed article. Jot down key facts and figures.',
        'Writing Skills': '20 minutes: Write a summary or review of the webinar/live event you attended.',
        'Vocabulary Expansion': '15 minutes: Use a vocabulary app like Duolingo to review learned words and discover new ones.',
        'Grammar Fundamentals': '15 minutes: Focus on verb patterns and gerund/infinitive usage exercises.'
    },
    'Sunday': {
        'Active Listening': '30 minutes: Listen to an English audiobook chapter. Pay attention to pronunciation and intonation.',
        'Speaking Practice': '20 minutes: Narrate a story or talk about your week\'s activities, focusing on fluency and accuracy.',
        'Reading Comprehension': '30 minutes: Select an article or a story linked to cultural aspects of English-speaking countries. Reflect on the key elements.',
        'Writing Skills': '20 minutes: Write a letter or an email to a friend from an English-speaking country, asking about their culture or expressing interest in visiting.',
        'Vocabulary Expansion': '15 minutes: Incorporate themed vocabulary (e.g., travel, culture) into a mind map.',
        'Grammar Fundamentals': '15 minutes: Review and do exercises on indirect speech and reported questions.'
    }
}

# Function to load and return the user's progress
def load_progress():
    try:
        return pd.read_csv('progress.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Day', 'Activity', 'Completed'])

# Function to save the user's progress
def save_progress(progress_df):
    progress_df.to_csv('progress.csv', index=False)

# Streamlit app
def main():
    st.title("English Learning Schedule Tracker")

    # Load progress
    progress_df = load_progress()

    # Get current day
    current_day = datetime.now().strftime("%A")
    
    # Display current day's schedule
    st.header(f"Today's Schedule ({current_day})")
    
    for category, task in schedule_data[current_day].items():
        st.subheader(category)
        col1, col2 = st.columns([3, 1])
        col1.write(task)
        
        # Check if task is already completed
        task_completed = progress_df[(progress_df['Date'] == datetime.now().date().isoformat()) & 
                                     (progress_df['Day'] == current_day) & 
                                     (progress_df['Activity'] == category)]['Completed'].any()
        
        if col2.button("Mark Complete" if not task_completed else "Completed", key=category, disabled=task_completed):
            new_entry = pd.DataFrame({
                'Date': [datetime.now().date().isoformat()],
                'Day': [current_day],
                'Activity': [category],
                'Completed': [True]
            })
            progress_df = pd.concat([progress_df, new_entry], ignore_index=True)
            save_progress(progress_df)
            st.rerun()

    # Display weekly progress
    st.header("Weekly Progress")
    weekly_progress = progress_df[progress_df['Date'] >= (datetime.now().date() - pd.Timedelta(days=7)).isoformat()]
    st.write(weekly_progress)

if __name__ == "__main__":
    main()