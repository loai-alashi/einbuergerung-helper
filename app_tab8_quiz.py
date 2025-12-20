import streamlit as st
import random
import uuid
from supabase import create_client

OFFICIAL_QUIZ_CATALOG_URL = "https://www.lebenindeutschland.eu/fragenkatalog"


# ----------------------------
# SUPABASE HELPERS
# ----------------------------
def _get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


def _fetch_questions(limit=50):
    """
    Fetch questions from Supabase table: public.questions
    Expected columns:
      id, question, option_a, option_b, option_c, option_d, correct_option
    """
    supabase = _get_supabase_client()
    res = supabase.table("questions").select("*").limit(limit).execute()
    return res.data or []


def _insert_attempt(question_id: int, selected_option: str, is_correct: bool):
    """
    Insert a single attempt into Supabase table: public.attempts
    Expected columns:
      session_id, question_id, selected_option, is_correct
    """
    supabase = _get_supabase_client()
    supabase.table("attempts").insert(
        {
            "session_id": st.session_state.session_id,
            "question_id": question_id,
            "selected_option": selected_option,  # "A" / "B" / "C" / "D"
            "is_correct": is_correct,
        }
    ).execute()


# ----------------------------
# SESSION STATE
# ----------------------------
def _init_quiz_state(total_questions: int):
    # anonymous tracking
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # store total so if DB size changes we reset safely
    if "quiz_total" not in st.session_state:
        st.session_state.quiz_total = total_questions

    # question order
    if "quiz_index_order" not in st.session_state or st.session_state.quiz_total != total_questions:
        st.session_state.quiz_total = total_questions
        st.session_state.quiz_index_order = list(range(total_questions))
        random.shuffle(st.session_state.quiz_index_order)
        st.session_state.quiz_pos = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected_letter = None  # "A"/"B"/"C"/"D"
        st.session_state.quiz_feedback = ""

    if "quiz_pos" not in st.session_state:
        st.session_state.quiz_pos = 0

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = False

    if "quiz_selected_letter" not in st.session_state:
        st.session_state.quiz_selected_letter = None

    if "quiz_feedback" not in st.session_state:
        st.session_state.quiz_feedback = ""


def _reset_quiz(total_questions: int):
    st.session_state.quiz_total = total_questions
    st.session_state.quiz_index_order = list(range(total_questions))
    random.shuffle(st.session_state.quiz_index_order)
    st.session_state.quiz_pos = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_selected_letter = None
    st.session_state.quiz_feedback = ""


def _current_question_row(questions):
    idx = st.session_state.quiz_index_order[st.session_state.quiz_pos]
    return questions[idx]


def _options_map(qrow):
    """
    Converts DB row -> dict of options {"A": "...", "B": "...", ...}
    """
    return {
        "A": qrow["option_a"],
        "B": qrow["option_b"],
        "C": qrow["option_c"],
        "D": qrow["option_d"],
    }


# ----------------------------
# TAB 8 RENDER (KEEP NAME!)
# ----------------------------
def render_tab8():
    st.title("Quiz – Leben in Deutschland")
    st.caption("This quiz is for learning/demonstration. It is not legal advice.")

    st.markdown(f"**Official question catalogue:** {OFFICIAL_QUIZ_CATALOG_URL}")
    st.markdown("---")

    # 1) Fetch questions first (needed to know total)
    # Fetch questions only once per browser session (speed)
    if "questions_cache" not in st.session_state:
        st.session_state.questions_cache = _fetch_questions(limit=200)

    questions = st.session_state.questions_cache



    # 2) Init state based on DB size
    _init_quiz_state(total_questions=len(questions))

    # Top bar: score + controls
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        st.metric("Score", f"{st.session_state.quiz_score} / {len(questions)}")
    with col_b:
        if st.button("Restart", use_container_width=True):
            _reset_quiz(total_questions=len(questions))
            st.rerun()
    with col_c:
        if st.button("Shuffle", use_container_width=True):
            _reset_quiz(total_questions=len(questions))
            st.rerun()

    st.markdown("")

    # End screen
    if st.session_state.quiz_pos >= len(questions):
        st.success("✅ Quiz finished!")
        st.write(f"Your final score: **{st.session_state.quiz_score} / {len(questions)}**")
        st.info("You can Restart or Shuffle to try again.")
        return

    # 3) Current question
    q = _current_question_row(questions)
    opts = _options_map(q)

    st.subheader(f"Question {st.session_state.quiz_pos + 1} of {len(questions)}")
    st.write(q["question"])

    disabled = st.session_state.quiz_answered

    # default selection if none chosen yet
    default_letter = st.session_state.quiz_selected_letter or "A"

    selected_letter = st.radio(
        "Choose one answer:",
        options=["A", "B", "C", "D"],
        format_func=lambda k: f"{k}) {opts[k]}",
        index=["A", "B", "C", "D"].index(default_letter),
        disabled=disabled,
        key="quiz_radio_letter",
    )

    if not disabled:
        st.session_state.quiz_selected_letter = selected_letter

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Check answer", use_container_width=True, disabled=disabled):
            correct_letter = q["correct_option"]  # "A"/"B"/"C"/"D"
            chosen_letter = st.session_state.quiz_selected_letter
            is_correct = (chosen_letter == correct_letter)

            st.session_state.quiz_answered = True

            # Save attempt to Supabase (anonymous)
            try:
                _insert_attempt(
                    question_id=q["id"],
                    selected_option=chosen_letter,
                    is_correct=is_correct,
                )
            except Exception as e:
                st.warning("Answer checked, but saving to Supabase failed.")
                st.code(str(e))

            if is_correct:
                st.session_state.quiz_score += 1
                st.session_state.quiz_feedback = "✅ Correct!"
            else:
                st.session_state.quiz_feedback = (
                    f"❌ Wrong. Correct answer: **{correct_letter}) {opts[correct_letter]}**"
                )

            st.rerun()

    with col2:
        if st.button(
            "Next question",
            use_container_width=True,
            disabled=not st.session_state.quiz_answered,
        ):
            st.session_state.quiz_pos += 1
            st.session_state.quiz_answered = False
            st.session_state.quiz_selected_letter = None
            st.session_state.quiz_feedback = ""
            st.rerun()

    if st.session_state.quiz_feedback:
        st.markdown(st.session_state.quiz_feedback)

    st.markdown("---")
    st.caption("No login required. Attempts are stored anonymously using a session_id.")


# allow running alone: streamlit run app_tab8_quiz.py
if __name__ == "__main__":
    render_tab8()
