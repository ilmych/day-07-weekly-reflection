"""
Weekly Reflection Journal
A calming space for weekly reflections and personal growth tracking.
Now with Supabase authentication and cloud storage.
"""

import streamlit as st
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# --- Supabase Configuration ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing Supabase credentials. Please check your .env file.")
    st.stop()

# Initialize Supabase client
@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# --- Configuration ---
EMOJI_RATINGS = ["1", "2", "3", "4", "5"]
EMOJI_DISPLAY = {
    "1": "Rough",
    "2": "Meh",
    "3": "Okay",
    "4": "Good",
    "5": "Great"
}
EMOJI_ICONS = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5"}

# --- Page Configuration ---
st.set_page_config(
    page_title="Weekly Reflection Journal",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for calming design ---
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }

    /* Headers */
    h1 {
        color: #4a5568 !important;
        font-weight: 300 !important;
        letter-spacing: 0.05em;
    }

    h2, h3 {
        color: #5a6878 !important;
        font-weight: 400 !important;
    }

    /* Text areas */
    .stTextArea textarea {
        background-color: #fafbfc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    .stTextArea textarea:focus {
        border-color: #a0aec0 !important;
        box-shadow: 0 0 0 3px rgba(160, 174, 192, 0.2) !important;
    }

    /* Text inputs */
    .stTextInput input {
        background-color: #fafbfc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 32px !important;
        font-weight: 500 !important;
        letter-spacing: 0.03em;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #edf2f7 100%) !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #4a5568;
    }

    /* Radio buttons for emoji rating */
    .stRadio > div {
        display: flex !important;
        gap: 8px !important;
        flex-wrap: wrap !important;
    }

    .stRadio > div > label {
        background-color: #f7fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
    }

    .stRadio > div > label:hover {
        border-color: #a0aec0 !important;
        background-color: #edf2f7 !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #667eea !important;
    }

    /* Dividers */
    hr {
        border-color: #e2e8f0 !important;
        margin: 2rem 0 !important;
    }

    /* Success/info messages */
    .stSuccess, .stInfo {
        background-color: #f0fff4 !important;
        border-radius: 12px !important;
    }

    /* Cards styling */
    .reflection-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .week-btn {
        background: white;
        border-radius: 10px;
        padding: 12px;
        margin: 6px 0;
        border-left: 3px solid #667eea;
        cursor: pointer;
    }

    /* Auth forms */
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f7fafc !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        color: #4a5568 !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #edf2f7 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
    }

    /* Form labels */
    .stTextInput label, .stTextArea label {
        color: #4a5568 !important;
        font-weight: 500 !important;
    }

    /* Input text color */
    .stTextInput input, .stTextArea textarea {
        color: #2d3748 !important;
    }

    /* Input placeholders */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #a0aec0 !important;
    }

    /* All paragraph and span text */
    p, span, label {
        color: #4a5568 !important;
    }

    /* Markdown text */
    .stMarkdown p {
        color: #4a5568 !important;
    }

    /* Warning/error/success messages text */
    .stAlert p {
        color: #2d3748 !important;
    }

    /* Tab panel content */
    [data-baseweb="tab-panel"] {
        color: #4a5568 !important;
    }

    [data-baseweb="tab-panel"] p,
    [data-baseweb="tab-panel"] span,
    [data-baseweb="tab-panel"] label {
        color: #4a5568 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Helper Functions ---
def get_week_key(date: datetime = None) -> str:
    """Get ISO week key (e.g., '2026-W03')."""
    if date is None:
        date = datetime.now()
    return f"{date.isocalendar()[0]}-W{date.isocalendar()[1]:02d}"


def parse_week_key(week_key: str) -> tuple:
    """Parse week key to (year, week_number)."""
    parts = week_key.split("-W")
    return int(parts[0]), int(parts[1])


def get_week_dates(week_key: str) -> tuple:
    """Get the Monday and Sunday dates for a given week."""
    year, week = parse_week_key(week_key)
    # Find the Monday of the given ISO week
    jan4 = datetime(year, 1, 4)  # Jan 4 is always in week 1
    start_of_week1 = jan4 - timedelta(days=jan4.weekday())
    monday = start_of_week1 + timedelta(weeks=week - 1)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def format_week_display(week_key: str) -> str:
    """Format week key for display."""
    monday, sunday = get_week_dates(week_key)
    return f"{monday.strftime('%b %d')} - {sunday.strftime('%b %d, %Y')}"


# --- Authentication Functions ---
def sign_up(email: str, password: str) -> tuple[bool, str]:
    """Sign up a new user."""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if response.user:
            return True, "Account created successfully! Please check your email to verify your account."
        return False, "Sign up failed. Please try again."
    except Exception as e:
        error_msg = str(e)
        if "User already registered" in error_msg:
            return False, "This email is already registered. Please log in instead."
        elif "Password should be at least" in error_msg:
            return False, "Password should be at least 6 characters long."
        elif "Unable to validate email" in error_msg or "Invalid email" in error_msg:
            return False, "Please enter a valid email address."
        return False, f"Sign up error: {error_msg}"


def sign_in(email: str, password: str) -> tuple[bool, str]:
    """Sign in an existing user."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user:
            return True, "Logged in successfully!"
        return False, "Login failed. Please check your credentials."
    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            return False, "Invalid email or password. Please try again."
        elif "Email not confirmed" in error_msg:
            return False, "Please verify your email before logging in."
        return False, f"Login error: {error_msg}"


def sign_out():
    """Sign out the current user."""
    try:
        supabase.auth.sign_out()
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        return True
    except Exception as e:
        return False


def get_current_user():
    """Get the current authenticated user."""
    try:
        response = supabase.auth.get_user()
        return response.user if response else None
    except Exception:
        return None


def get_session():
    """Get the current session."""
    try:
        response = supabase.auth.get_session()
        return response.session if response else None
    except Exception:
        return None


# --- Database Functions ---
def load_reflections(user_id: str) -> dict:
    """Load all reflections for a user from Supabase."""
    try:
        response = supabase.table("reflections").select("*").eq("user_id", user_id).execute()

        # Convert list to dict keyed by week_key
        data = {}
        if response.data:
            for row in response.data:
                data[row["week_key"]] = {
                    "id": row["id"],
                    "went_well": row.get("went_well", ""),
                    "challenges": row.get("challenges", ""),
                    "learned": row.get("learned", ""),
                    "focus": row.get("focus", ""),
                    "rating": row.get("rating", "3"),
                    "created_at": row.get("created_at"),
                    "updated_at": row.get("updated_at")
                }
        return data
    except Exception as e:
        st.error(f"Error loading reflections: {e}")
        return {}


def save_reflection(user_id: str, week_key: str, entry: dict) -> tuple[bool, str]:
    """Save or update a reflection in Supabase."""
    try:
        data = {
            "user_id": user_id,
            "week_key": week_key,
            "went_well": entry.get("went_well", ""),
            "challenges": entry.get("challenges", ""),
            "learned": entry.get("learned", ""),
            "focus": entry.get("focus", ""),
            "rating": entry.get("rating", "3"),
            "updated_at": datetime.now().isoformat()
        }

        # Use upsert to insert or update based on user_id + week_key
        response = supabase.table("reflections").upsert(
            data,
            on_conflict="user_id,week_key"
        ).execute()

        if response.data:
            return True, "Reflection saved!"
        return False, "Failed to save reflection."
    except Exception as e:
        return False, f"Error saving reflection: {e}"


def calculate_stats(data: dict) -> dict:
    """Calculate journal statistics."""
    if not data:
        return {"streak": 0, "avg_rating": 0, "total": 0}

    # Total entries
    total = len(data)

    # Average rating
    ratings = [int(entry.get("rating", 3)) for entry in data.values() if entry.get("rating")]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    # Current streak (consecutive weeks from current week backwards)
    current_week = get_week_key()
    streak = 0

    # Get all weeks sorted
    weeks = sorted(data.keys(), reverse=True)

    if weeks:
        current_date = datetime.now()

        for week_key in weeks:
            expected_date = current_date - timedelta(weeks=streak)
            expected_key = get_week_key(expected_date)

            if week_key == expected_key:
                streak += 1
            else:
                break

    return {
        "streak": streak,
        "avg_rating": round(avg_rating, 1),
        "total": total
    }


# --- Initialize Session State ---
if "selected_week" not in st.session_state:
    st.session_state.selected_week = get_week_key()

if "just_saved" not in st.session_state:
    st.session_state.just_saved = False

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

if "data" not in st.session_state:
    st.session_state.data = {}


# --- Check Authentication ---
user = get_current_user()

# --- Authentication UI (if not logged in) ---
if not user:
    st.markdown("# Weekly Reflection Journal")
    st.markdown("*A calming space for your weekly reflections*")
    st.markdown("---")

    # Create centered container for auth
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Tab selection for login/signup
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            st.markdown("### Welcome back")
            login_email = st.text_input("Email", key="login_email", placeholder="you@example.com")
            login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

            if st.button("Log In", use_container_width=True, type="primary", key="login_btn"):
                if login_email and login_password:
                    success, message = sign_in(login_email, login_password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter both email and password.")

        with tab2:
            st.markdown("### Create an account")
            signup_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
            signup_password = st.text_input("Password", type="password", key="signup_password", placeholder="At least 6 characters")
            signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm", placeholder="Confirm your password")

            if st.button("Sign Up", use_container_width=True, type="primary", key="signup_btn"):
                if signup_email and signup_password and signup_password_confirm:
                    if signup_password != signup_password_confirm:
                        st.error("Passwords do not match.")
                    elif len(signup_password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        success, message = sign_up(signup_email, signup_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields.")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #a0aec0; font-size: 0.85em; padding: 20px;'>"
        "Your reflections are private and secure."
        "</div>",
        unsafe_allow_html=True
    )
    st.stop()


# --- User is authenticated - Show main app ---

# Load user's reflections if not already loaded
if "user_id" not in st.session_state or st.session_state.user_id != user.id:
    st.session_state.user_id = user.id
    st.session_state.data = load_reflections(user.id)


# --- Sidebar: History & Stats ---
with st.sidebar:
    # User info and logout
    st.markdown(f"**{user.email}**")
    if st.button("Logout", use_container_width=True):
        if sign_out():
            st.rerun()

    st.markdown("---")
    st.markdown("### Journal")

    # Stats section
    stats = calculate_stats(st.session_state.data)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Streak", f"{stats['streak']}w")
    with col2:
        st.metric("Avg", f"{stats['avg_rating']}" if stats['avg_rating'] else "-")
    with col3:
        st.metric("Total", stats['total'])

    st.markdown("---")
    st.markdown("### Past Entries")

    # New entry button
    current_week = get_week_key()
    if st.button("+ This Week", use_container_width=True, type="primary"):
        st.session_state.selected_week = current_week
        st.rerun()

    st.markdown("")

    # List past entries
    if st.session_state.data:
        sorted_weeks = sorted(st.session_state.data.keys(), reverse=True)

        for week_key in sorted_weeks:
            entry = st.session_state.data[week_key]
            rating = entry.get("rating", "3")
            rating_num = rating if rating else "3"

            # Format display
            monday, sunday = get_week_dates(week_key)
            date_str = f"{monday.strftime('%b %d')} - {sunday.strftime('%d')}"

            # Highlight current selection
            is_selected = week_key == st.session_state.selected_week

            if st.button(
                f"[{rating_num}] {week_key}\n{date_str}",
                key=f"btn_{week_key}",
                use_container_width=True,
                type="secondary" if not is_selected else "primary"
            ):
                st.session_state.selected_week = week_key
                st.rerun()
    else:
        st.caption("No entries yet. Start your first reflection!")


# --- Main Content ---
st.markdown("# Weekly Reflection Journal")
st.markdown("*Take a moment to reflect on your week*")
st.markdown("---")

# Week selector
selected_week = st.session_state.selected_week
monday, sunday = get_week_dates(selected_week)
st.markdown(f"### Week of {monday.strftime('%B %d')} - {sunday.strftime('%B %d, %Y')}")
st.caption(f"Week {selected_week}")

# Check if this is the current week
is_current = selected_week == get_week_key()
if is_current:
    st.info("This is the current week")

# Load existing entry or create empty
existing_entry = st.session_state.data.get(selected_week, {})

st.markdown("")

# --- Reflection Prompts ---

# What went well
st.markdown("#### What went well this week?")
went_well = st.text_area(
    label="went_well",
    value=existing_entry.get("went_well", ""),
    placeholder="Celebrate your wins, big or small...",
    height=120,
    label_visibility="collapsed",
    key="went_well"
)

st.markdown("")

# What didn't go as planned
st.markdown("#### What didn't go as planned?")
challenges = st.text_area(
    label="challenges",
    value=existing_entry.get("challenges", ""),
    placeholder="Reflect on obstacles or setbacks...",
    height=120,
    label_visibility="collapsed",
    key="challenges"
)

st.markdown("")

# What did you learn
st.markdown("#### What did you learn?")
learned = st.text_area(
    label="learned",
    value=existing_entry.get("learned", ""),
    placeholder="Insights, discoveries, new skills...",
    height=120,
    label_visibility="collapsed",
    key="learned"
)

st.markdown("")

# Focus for next week
st.markdown("#### What's one thing to focus on next week?")
focus = st.text_area(
    label="focus",
    value=existing_entry.get("focus", ""),
    placeholder="Set an intention for the week ahead...",
    height=100,
    label_visibility="collapsed",
    key="focus"
)

st.markdown("---")

# Week rating
st.markdown("#### How would you rate this week?")

rating = st.radio(
    label="Week rating",
    options=EMOJI_RATINGS,
    format_func=lambda x: EMOJI_DISPLAY[x],
    horizontal=True,
    index=EMOJI_RATINGS.index(existing_entry.get("rating", "3")) if existing_entry.get("rating") in EMOJI_RATINGS else 2,
    label_visibility="collapsed",
    key="rating"
)

st.markdown("")
st.markdown("")

# Save button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Save Reflection", use_container_width=True, type="primary"):
        # Build entry
        entry = {
            "went_well": went_well,
            "challenges": challenges,
            "learned": learned,
            "focus": focus,
            "rating": rating
        }

        # Save to Supabase
        success, message = save_reflection(user.id, selected_week, entry)

        if success:
            # Update local cache
            st.session_state.data[selected_week] = entry
            st.session_state.just_saved = True
            st.rerun()
        else:
            st.error(message)

# Show success message
if st.session_state.just_saved:
    st.success("Reflection saved!")
    st.session_state.just_saved = False

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #a0aec0; font-size: 0.85em; padding: 20px;'>"
    "Take time to reflect. Growth comes from looking back."
    "</div>",
    unsafe_allow_html=True
)
