# LearnLens

A small working prototype of a Pre-Class Learning Diagnostic System.

## What it demonstrates

Previous lesson → 5-question diagnostic → automatic concept analysis → learning-state classification → instructor dashboard → teaching recommendation.

### Learning states
- Ready: 80–100%
- Needs Reinforcement: 50–79%
- Needs Support: below 50%

## Run locally

1. Install Python 3.10+
2. Open a terminal in this folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
streamlit run app.py
```

The app opens in your browser.

## Demo

1. Open **Instructor Dashboard** first.
2. Show the class summary and concept gaps.
3. Go to **Student Diagnostic**.
4. Enter a new student name and answer the five questions.
5. Submit.
6. Return to **Instructor Dashboard** and show that the class analysis updates.

## Note

This prototype intentionally uses one lesson and in-memory demo data. It is designed to demonstrate the core product value quickly. Authentication, persistent databases, multiple courses, teacher accounts, question banks, and advanced AI recommendations can be added after the competition.

