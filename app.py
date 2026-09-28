
import streamlit as st
from collections import Counter, defaultdict

st.set_page_config(
    page_title="LearnLens | Pre-Class Learning Diagnostic",
    page_icon="🎯",
    layout="wide",
)

# -----------------------------
# Demo lesson and questions
# -----------------------------
QUESTIONS = [
    {
        "id": 1,
        "concept": "Function basics",
        "question": "Which statement best describes a Python function?",
        "options": [
            "A reusable block of code designed to perform a specific task",
            "A variable that can only store numbers",
            "A file that stores Python libraries",
            "A loop that always runs forever",
        ],
        "answer": 0,
    },
    {
        "id": 2,
        "concept": "Parameters",
        "question": "What is the purpose of a parameter in a function?",
        "options": [
            "To permanently save the function's output",
            "To receive a value that can be used inside the function",
            "To stop a function from executing",
            "To import another Python program",
        ],
        "answer": 1,
    },
    {
        "id": 3,
        "concept": "Return values",
        "question": "What does the return statement do?",
        "options": [
            "Repeats a function",
            "Prints every variable automatically",
            "Sends a result back from a function",
            "Creates a new class",
        ],
        "answer": 2,
    },
    {
        "id": 4,
        "concept": "Calling functions",
        "question": "How would you call a function named calculate_total?",
        "options": [
            "call.calculate_total",
            "calculate_total()",
            "function calculate_total",
            "run:calculate_total",
        ],
        "answer": 1,
    },
    {
        "id": 5,
        "concept": "Parameters",
        "question": "Given def greet(name):, what does greet('Amina') do?",
        "options": [
            "Defines another function called Amina",
            "Passes 'Amina' to the name parameter",
            "Deletes the name parameter",
            "Returns the word name",
        ],
        "answer": 1,
    },
]

DEMO_RESULTS = [
    {"name": "Aisha", "answers": [0, 1, 2, 1, 1]},
    {"name": "David", "answers": [0, 0, 2, 1, 0]},
    {"name": "Musa", "answers": [1, 0, 0, 0, 2]},
    {"name": "Fatima", "answers": [0, 1, 2, 1, 1]},
    {"name": "John", "answers": [0, 1, 2, 0, 1]},
    {"name": "Zainab", "answers": [0, 0, 2, 1, 0]},
    {"name": "Ibrahim", "answers": [1, 0, 0, 0, 2]},
    {"name": "Maryam", "answers": [0, 1, 2, 1, 1]},
]

def classify(score):
    if score >= 80:
        return "Ready", "🟢"
    if score >= 50:
        return "Needs Reinforcement", "🟡"
    return "Needs Support", "🔴"

def analyze_student(name, answers):
    correct = sum(a == q["answer"] for a, q in zip(answers, QUESTIONS))
    score = round(correct / len(QUESTIONS) * 100)
    state, icon = classify(score)

    weak = []
    for a, q in zip(answers, QUESTIONS):
        if a != q["answer"]:
            weak.append(q["concept"])

    return {
        "name": name,
        "score": score,
        "state": state,
        "icon": icon,
        "weak": weak,
        "answers": answers,
    }

def analyze_all(results):
    analyzed = [analyze_student(r["name"], r["answers"]) for r in results]
    concept_total = Counter()
    concept_wrong = Counter()

    for r in analyzed:
        for q, answer in zip(QUESTIONS, r["answers"]):
            concept_total[q["concept"]] += 1
            if answer != q["answer"]:
                concept_wrong[q["concept"]] += 1

    gaps = []
    for concept, total in concept_total.items():
        pct = round(concept_wrong[concept] / total * 100)
        gaps.append((concept, pct))
    gaps.sort(key=lambda x: x[1], reverse=True)

    return analyzed, gaps

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
.hero {
    padding: 1.4rem 1.6rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    border: 1px solid #e2e8f0;
    margin-bottom: 1.2rem;
}
.hero h1 {margin: 0; font-size: 2.1rem;}
.hero p {margin: .35rem 0 0; color: #475569; font-size: 1.02rem;}
.card {
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1rem;
    background: white;
}
.small {color:#64748b; font-size:.88rem;}
.gapbar {
    padding: .65rem .8rem;
    border-radius: 10px;
    background:#f8fafc;
    margin:.35rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🎯 LearnLens</h1>
<p>Pre-Class Learning Diagnostic: know what students need before the lesson starts.</p>
</div>
""", unsafe_allow_html=True)

# Session state
if "results" not in st.session_state:
    st.session_state.results = list(DEMO_RESULTS)
if "student_answers" not in st.session_state:
    st.session_state.student_answers = {}

analyzed, gaps = analyze_all(st.session_state.results)

page = st.sidebar.radio(
    "Navigate",
    ["Instructor Dashboard", "Student Diagnostic", "How It Works"],
)

st.sidebar.divider()
st.sidebar.caption("Competition MVP")
st.sidebar.caption("Demo lesson: Python Functions")

# -----------------------------
# Instructor dashboard
# -----------------------------
if page == "Instructor Dashboard":
    st.subheader("Instructor Dashboard")
    st.caption("Diagnostic: Python Functions • Previous lesson → next-class preparation")

    total = len(analyzed)
    counts = Counter(r["state"] for r in analyzed)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students assessed", total)
    c2.metric("🟢 Ready", counts["Ready"])
    c3.metric("🟡 Reinforcement", counts["Needs Reinforcement"])
    c4.metric("🔴 Support", counts["Needs Support"])

    st.divider()

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown("### Class learning gaps")
        for concept, pct in gaps:
            st.markdown(
                f'<div class="gapbar"><b>{concept}</b> — {pct}% incorrect</div>',
                unsafe_allow_html=True
            )

        if gaps:
            top = gaps[0][0]
            second = gaps[1][0] if len(gaps) > 1 else None
            focus = f"Focus first on **{top}**"
            if second:
                focus += f", then reinforce **{second}**."

            st.info(
                f"💡 **Pre-class recommendation:** {focus} "
                "before introducing new material."
            )

    with right:
        st.markdown("### Student learning states")
        for state, icon in [
            ("Ready", "🟢"),
            ("Needs Reinforcement", "🟡"),
            ("Needs Support", "🔴"),
        ]:
            names = [r["name"] for r in analyzed if r["state"] == state]
            st.markdown(f"**{icon} {state}**")
            st.caption(", ".join(names) if names else "None")

    st.divider()
    st.markdown("### Student diagnostic details")

    for r in analyzed:
        with st.expander(f"{r['icon']} {r['name']} — {r['score']}% — {r['state']}"):
            if r["weak"]:
                st.write("**Concepts needing attention:** " + ", ".join(sorted(set(r["weak"]))))
            else:
                st.write("No significant prerequisite gaps detected.")

# -----------------------------
# Student diagnostic
# -----------------------------
elif page == "Student Diagnostic":
    st.subheader("Student Diagnostic")
    st.caption("5 questions • based on the previous lesson: Python Functions")

    name = st.text_input("Student name", placeholder="e.g. Amina")

    with st.form("diagnostic_form"):
        answers = []
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"**{i+1}. {q['question']}**")
            choice = st.radio(
                "Choose one answer",
                q["options"],
                key=f"q_{q['id']}",
                index=None,
                label_visibility="collapsed",
            )
            answers.append(q["options"].index(choice) if choice else -1)

        submitted = st.form_submit_button("Submit Diagnostic", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        elif -1 in answers:
            st.error("Please answer all five questions.")
        else:
            st.session_state.results.append({"name": name.strip(), "answers": answers})
            result = analyze_student(name.strip(), answers)
            st.success("Diagnostic submitted. The instructor dashboard has been updated.")

            st.markdown("### Your diagnostic result")
            st.metric("Score", f"{result['score']}%")
            st.write(f"### {result['icon']} {result['state']}")
            if result["weak"]:
                st.warning(
                    "Concepts to revisit: " + ", ".join(sorted(set(result["weak"])))
                )
            else:
                st.success("You demonstrated understanding of the prerequisite concepts.")

# -----------------------------
# How it works
# -----------------------------
else:
    st.subheader("How LearnLens works")

    cols = st.columns(4)
    steps = [
        ("1", "Previous lesson", "The instructor selects the concepts students should already understand."),
        ("2", "3–5 questions", "Students complete a short pre-class diagnostic."),
        ("3", "Automatic analysis", "Responses are mapped to concepts and learning states."),
        ("4", "Adapt the class", "The instructor sees the gaps and adjusts the next lesson."),
    ]
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"### {num}. {title}")
            st.write(desc)

    st.divider()
    st.markdown("### Learning-state logic")
    st.markdown("""
    - **🟢 Ready:** 80–100%: prerequisite understanding is demonstrated.
    - **🟡 Needs Reinforcement:** 50–79%: some prerequisite gaps are present.
    - **🔴 Needs Support:** below 50%: significant difficulty is indicated.
    """)

    st.info(
        " LearnLens is not trying to replace the instructor. "
        "It gives the instructor timely evidence about what students need before class."
    )
