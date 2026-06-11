"""
Streamlit Murder Mystery Investigation
A premium detective headquarters experience.
"""

import json
import random
import urllib.error
import urllib.request

import streamlit as st

GEMINI_API_KEY = ""
GEMINI_API_URL = "https://api.openai.com/v1/responses"


def generate_game_data():
    

    cases = [

        {
            "case_title": "Bank Vault Homicide",
            "location": "Downtown Bank",
            "victim": "Bank Manager",
            "victim_occupation": "Financial Manager",

            "suspects": [
                {
                    "name": "Alice",
                    "occupation": "Accountant",
                    "motive": "Dispute over missing funds",
                    "alibi": "Working in the records room",
                    "suspicious_behavior": "Avoided eye contact",
                    "contradiction_text": "Records show she left the room.",
                    "contradiction_clue_index": 2,
                    "interrogated": False,
                    "contradiction_found": False,
                },
                {
                    "name": "Bob",
                    "occupation": "Security Guard",
                    "motive": "Debt problems",
                    "alibi": "Patrolling the building",
                    "suspicious_behavior": "Disabled cameras",
                    "contradiction_text": "Camera logs contradict his route.",
                    "contradiction_clue_index": 3,
                    "interrogated": False,
                    "contradiction_found": False,
                },
                {
                    "name": "Charlie",
                    "occupation": "CEO",
                    "motive": "Insurance payout",
                    "alibi": "Working late",
                    "suspicious_behavior": "Changed statements",
                    "contradiction_text": "Evidence places him near the vault.",
                    "contradiction_clue_index": 0,
                    "interrogated": False,
                    "contradiction_found": False,
                },
            ],

            "murderer_index": 1,

            "clues": [
                "Vault door showed signs of forced entry",
                "Footprints near the safe",
                "Records room was empty",
                "Security cameras were disabled",
                "A keycard was used after hours",
                "A glove was found near the vault",
            ],

            "solution_summary": "Bob disabled the cameras and entered the vault."
        },

        {
            "case_title": "Hotel Mystery",
            "location": "Grand Palace Hotel",
            "victim": "Famous Singer",
            "victim_occupation": "Performer",

            "suspects": [
                {
                    "name": "Emma",
                    "occupation": "Receptionist",
                    "motive": "Personal dispute",
                    "alibi": "At the front desk",
                    "suspicious_behavior": "Deleted call logs",
                    "contradiction_text": "Phone records don't match.",
                    "contradiction_clue_index": 1,
                    "interrogated": False,
                    "contradiction_found": False,
                },
                {
                    "name": "Jake",
                    "occupation": "Hotel Manager",
                    "motive": "Blackmail",
                    "alibi": "Checking rooms",
                    "suspicious_behavior": "Acted nervous",
                    "contradiction_text": "Room access logs contradict him.",
                    "contradiction_clue_index": 3,
                    "interrogated": False,
                    "contradiction_found": False,
                },
                {
                    "name": "Sophia",
                    "occupation": "Tourist",
                    "motive": "Revenge",
                    "alibi": "At dinner",
                    "suspicious_behavior": "Seen near victim's room",
                    "contradiction_text": "Witness saw her elsewhere.",
                    "contradiction_clue_index": 5,
                    "interrogated": False,
                    "contradiction_found": False,
                },
            ],

            "murderer_index": 0,

            "clues": [
                "Victim received a threatening message",
                "Deleted hotel phone records",
                "Keycard found near room",
                "Access logs changed",
                "Witness heard arguing",
                "Fingerprint found on the door",
            ],

            "solution_summary": "Emma deleted evidence to hide her involvement."
        },

        {
            "case_title": "Movie Studio Murder",
            "location": "Sunrise Studios",
            "victim": "Film Director",
            "victim_occupation": "Director",

            "suspects": [
                {
                    "name": "Ryan",
                    "occupation": "Actor",
                    "motive": "Lost lead role",
                    "alibi": "In makeup room",
                    "suspicious_behavior": "Angry before incident",
                    "contradiction_text": "Makeup artist never saw him.",
                    "contradiction_clue_index": 2,
                    "interrogated": False,
                    "contradiction_found": False,
                },
                {
                    "name": "Olivia",
                    "occupation": "Producer",
                    "motive": "Financial conflict",
                    "alibi": "In meeting",
                    "suspicious_behavior": "Destroyed documents",
                    "contradiction_text": "Meeting ended earlier.",
                    "contradiction_clue_index": 4,
                    "interrogated": False,
                    "contradiction_found": False,
                },
                {
                    "name": "Liam",
                    "occupation": "Cameraman",
                    "motive": "Career sabotage",
                    "alibi": "Equipment room",
                    "suspicious_behavior": "Tampered footage",
                    "contradiction_text": "Footage timestamps were altered.",
                    "contradiction_clue_index": 5,
                    "interrogated": False,
                    "contradiction_found": False,
                },
            ],

            "murderer_index": 2,

            "clues": [
                "Broken camera found",
                "Director received threats",
                "Makeup room was empty",
                "Script pages torn apart",
                "Meeting schedule altered",
                "Video timestamps were changed",
            ],

            "solution_summary": "Liam altered footage to hide the crime."
        }

    ]

    return random.choice(cases)

def get_rank(score):
    if score >= 70:
        return "Master Detective", 90
    if score >= 50:
        return "Lead Investigator", 70
    if score >= 30:
        return "Detective Sergeant", 50
    return "Field Agent", 30


def get_achievement_badges(game_data):
    badges = []
    clues_found = len(game_data["clues"]) if game_data["clues_viewed"] else 0
    if clues_found >= 6:
        badges.append("Evidence Specialist")
    if game_data["detective_score"] >= 20:
        badges.append("Contradiction Hunter")
    if game_data["accusations_made"] == 0:
        badges.append("Flawless Accuser")
    return badges or ["Case Initiate"]


def initialize_game():
    """Initialize a new game with a generated or fallback case."""
    game_data = generate_game_data()
    
    # Ensure all required gameplay fields are present
    game_data.setdefault("accusations_made", 0)
    game_data.setdefault("max_accusations", 3)
    game_data.setdefault("clues_viewed", False)
    game_data.setdefault("clues_found", 0)
    game_data.setdefault("detective_score", 0)
    game_data.setdefault("points_per_contradiction", 10)
    game_data.setdefault("case_difficulty", random.choice(["Standard", "High Stakes", "Black Ops"]))
    game_data.setdefault("case_id", f"CASE-{random.randint(1000, 9999)}")
    
    return game_data


def reset_state():
    st.session_state.started = False
    st.session_state.game_data = None
    st.session_state.selected_suspect = None
    st.session_state.show_clues = False
    st.session_state.accusation_choice = 0
    st.session_state.show_accuse_confirm = False
    st.session_state.accusation_result = None
    st.session_state.notice = ""


def ensure_session_state():
    defaults = {
        "started": False,
        "game_data": None,
        "selected_suspect": None,
        "show_clues": False,
        "accusation_choice": 0,
        "show_accuse_confirm": False,
        "accusation_result": None,
        "notice": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def calculate_progress(game_data):
    interrogated = sum(1 for suspect in game_data["suspects"] if suspect["interrogated"])
    revealed = len(game_data["clues"]) if game_data["clues_viewed"] else 0
    return int((interrogated / 3 * 0.55 + revealed / len(game_data["clues"]) * 0.45) * 100)


def check_contradiction(game_data, suspect_index):
    suspect = game_data["suspects"][suspect_index]
    if suspect["contradiction_found"]:
        return None

    clue_text = game_data["clues"][suspect["contradiction_clue_index"]]
    suspect["contradiction_found"] = True
    game_data["detective_score"] += game_data["points_per_contradiction"]
    return {
        "message": suspect["contradiction_text"],
        "clue": clue_text,
        "points": game_data["points_per_contradiction"],
    }


def accuse_suspect(game_data, accused_index):
    accused = game_data["suspects"][accused_index]
    murderer = game_data["suspects"][game_data["murderer_index"]]

    if accused_index == game_data["murderer_index"]:
        game_data["detective_score"] += 50
        return {
            "outcome": "won",
            "title": "CASE CLOSED",
            "message": f"{accused['name']} was the murderer. The case is solved.",
            "details": f"Detective Score: {game_data['detective_score']}",
        }

    game_data["accusations_made"] += 1
    if game_data["accusations_made"] >= game_data["max_accusations"]:
        game_data["detective_score"] -= 50

        return {
            "outcome": "lost",
            "title": "CASE FAILED",
            "message": f"Wrong accusation. The murderer was {murderer['name']}.",
            "details": "You ran out of accusations and the case cooled.",
        }
    return {
        "outcome": "wrong",
        "title": "ACCUSATION MISSED",
        "message": f"{accused['name']} is innocent. Continue investigating.",
        "details": f"Remaining accusations: {game_data['max_accusations'] - game_data['accusations_made']}",
    }


def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Quicksand:wght@500;600;700&display=swap');
        html, body, [data-testid='stAppViewContainer'], [data-testid='stAppViewContainer'] > div:first-child {
            min-height: 100vh;
            background: linear-gradient(180deg, #e8f4f8 0%, #f0e8d8 50%, #e8f2d8 100%);
            color: #3d4d42;
            font-family: 'Quicksand', sans-serif;
        }
        body {
            font-family: 'Quicksand', sans-serif;
        }
        #MainMenu, footer, header, .stAppHeader {
            visibility: hidden;
            height: 0;
            overflow: hidden;
        }
        .stButton > button {
            font-family: 'Fredoka', sans-serif;
            background: linear-gradient(135deg, #6b9f7f 0%, #5a8d6f 100%);
            color: #fff8f0;
            border: 2px solid rgba(255, 255, 255, 0.35);
            border-radius: 24px;
            padding: 0.85rem 1.8rem;
            box-shadow: 0 8px 20px rgba(107, 159, 127, 0.28);
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
            font-weight: 600;
            letter-spacing: 0.04em;
        }
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 28px rgba(107, 159, 127, 0.38);
            background: linear-gradient(135deg, #7aad8e 0%, #6a9b7e 100%);
        }
        .investigation-hero {
            border-radius: 28px;
            background: linear-gradient(135deg, #a8d8e8 0%, #c8e6f0 50%, #e8d47e 100%);
            color: #3d4d42;
            padding: 2.5rem 2rem;
            box-shadow: 0 12px 35px rgba(168, 216, 232, 0.25);
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            border: 2px solid rgba(255, 255, 255, 0.4);
        }
        .investigation-hero::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at top right, rgba(255, 255, 255, 0.3), transparent 30%);
            pointer-events: none;
        }
        .hero-title {
            font-family: 'Fredoka', sans-serif;
            font-size: clamp(2.2rem, 5vw, 4rem);
            line-height: 1;
            letter-spacing: 0.08em;
            margin-bottom: 0.6rem;
            max-width: min(100%, 78ch);
            word-break: normal;
            overflow-wrap: normal;
            white-space: normal;
            color: #3d4d42;
            font-weight: 700;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            color: #3d4d42;
            max-width: 700px;
            margin-bottom: 1rem;
            line-height: 1.6;
            font-weight: 500;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.6rem;
            background: rgba(107, 159, 127, 0.15);
            border: 2px solid #6b9f7f;
            border-radius: 999px;
            padding: 0.6rem 0.95rem;
            color: #3d4d42;
            font-weight: 600;
            font-size: 0.92rem;
        }
        .hero-cta {
            font-size: 0.95rem;
        }
        .headquarters-panel,
        .board-panel,
        .scene-panel,
        .accuse-card,
        .reveal-panel {
            background: linear-gradient(135deg, #f9f5ed 0%, #fbf8f2 100%);
            border-radius: 26px;
            padding: 1.8rem;
            box-shadow: 0 12px 32px rgba(107, 159, 127, 0.12);
            border: 2px solid rgba(107, 159, 127, 0.15);
            margin-bottom: 1.6rem;
        }
        .section-heading {
            font-family: 'Fredoka', sans-serif;
            font-size: 1.4rem;
            color: #3d4d42;
            margin-bottom: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }
        .detective-card {
            background: linear-gradient(135deg, #e8f0e8 0%, #f0f4f0 100%);
            border: 2px solid #c8e6c8;
            border-radius: 24px;
            padding: 1.4rem;
            box-shadow: 0 8px 20px rgba(107, 159, 127, 0.12);
        }
        .profile-avatar {
            width: 76px;
            height: 76px;
            border-radius: 16px;
            background: linear-gradient(135deg, #7bc3a8 0%, #6bb59b 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff8f0;
            font-size: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 18px rgba(123, 195, 168, 0.28);
        }
        .profile-meta {
            color: #3d4d42;
            line-height: 1.8;
            font-size: 0.95rem;
        }
        .profile-meta strong {
            color: #2d3d32;
            font-weight: 700;
        }
        .stat-tile {
            border-radius: 20px;
            padding: 1.1rem 1.2rem;
            background: linear-gradient(135deg, #e8f2e8 0%, #f0f8f0 100%);
            border: 1.5px solid #d0e8d0;
            box-shadow: 0 8px 18px rgba(107, 159, 127, 0.1);
            margin-bottom: 0.9rem;
            position: relative;
        }
        .stat-title {
            font-family: 'Fredoka', sans-serif;
            font-weight: 700;
            margin-bottom: 0.3rem;
            color: #3d4d42;
            font-size: 0.92rem;
        }
        .stat-value {
            font-size: 1.25rem;
            color: #6b9f7f;
            font-weight: 700;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #ffd699 0%, #ffe6b8 100%);
            border: 1.5px solid #e8c97f;
            border-radius: 999px;
            padding: 0.45rem 0.85rem;
            color: #5d3d1f;
            font-size: 0.88rem;
            font-weight: 600;
            box-shadow: 0 6px 14px rgba(232, 212, 126, 0.25);
            margin-right: 0.6rem;
            margin-bottom: 0.6rem;
        }
        .file-card {
            position: relative;
            background: linear-gradient(135deg, #f9e8cc 0%, #f5e0c0 100%);
            border-radius: 22px;
            padding: 1.35rem 1.3rem;
            border: 2px solid rgba(232, 178, 121, 0.25);
            box-shadow: 0 12px 28px rgba(100, 60, 20, 0.16);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            overflow: hidden;
            min-height: 260px;
        }
        .file-card::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at top left, rgba(255, 255, 255, 0.4), transparent 35%);
            pointer-events: none;
        }
        .file-card:hover {
            transform: translateY(-5px) rotate(-0.5deg);
            box-shadow: 0 16px 38px rgba(100, 60, 20, 0.22);
        }
        .file-pin {
            position: absolute;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: linear-gradient(135deg, #e8726f 0%, #d44f4c 100%);
            top: 12px;
            left: 18px;
            box-shadow: 0 6px 14px rgba(212, 79, 76, 0.28);
        }
        .file-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.9rem;
            position: relative;
            z-index: 1;
        }
        .file-name {
            font-family: 'Fredoka', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: #3d4d42;
        }
        .threat-tag {
            background: linear-gradient(135deg, #f09090 0%, #e8626b 100%);
            color: #fff8f0;
            border-radius: 999px;
            padding: 0.3rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            box-shadow: 0 4px 10px rgba(212, 79, 76, 0.25);
        }
        .file-detail {
            color: #3d4d42;
            line-height: 1.75;
            margin-bottom: 0.7rem;
            font-size: 0.93rem;
            position: relative;
            z-index: 1;
        }
        .file-line {
            height: 1px;
            background: rgba(107, 159, 127, 0.2);
            margin: 0.9rem 0;
        }
        .board-panel {
            background: linear-gradient(135deg, #c8b89f 0%, #d4c4a8 100%);
            border: 2px solid rgba(180, 140, 100, 0.25);
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.15), 0 12px 35px rgba(100, 70, 40, 0.18);
            padding: 1.8rem;
        }
        .board-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            position: relative;
            z-index: 1;
        }
        .evidence-card {
            background: linear-gradient(135deg, #fef8f0 0%, #fdf4e8 100%);
            border-radius: 20px;
            padding: 1.1rem 1.05rem;
            position: relative;
            border: 1.5px solid rgba(232, 178, 121, 0.3);
            box-shadow: 0 10px 24px rgba(100, 60, 20, 0.14);
            overflow: hidden;
            min-height: 200px;
        }
        .evidence-card::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at top left, rgba(255, 255, 255, 0.35), transparent 30%);
        }
        .evidence-card.locked {
            color: rgba(61, 77, 66, 0.5);
            background: rgba(253, 244, 232, 0.75);
            border-style: dashed;
        }
        .evidence-pin {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: linear-gradient(135deg, #4488cc 0%, #2d5fa8 100%);
            position: absolute;
            top: 10px;
            right: 12px;
            box-shadow: 0 6px 12px rgba(77, 136, 204, 0.28);
        }
        .evidence-title {
            font-family: 'Fredoka', sans-serif;
            font-size: 0.98rem;
            color: #3d4d42;
            margin-bottom: 0.7rem;
            font-weight: 700;
            position: relative;
            z-index: 1;
        }
        .evidence-detail {
            color: #3d4d42;
            line-height: 1.75;
            font-size: 0.92rem;
            position: relative;
            z-index: 1;
        }
        .scene-panel {
            background: linear-gradient(135deg, #e8f0f5 0%, #f0f4f8 100%);
            border: 2px solid rgba(168, 216, 232, 0.25);
            padding: 1.8rem;
        }
        .bubble {
            border-radius: 24px;
            padding: 0.95rem 1.1rem;
            margin-bottom: 0.9rem;
            max-width: 100%;
            display: inline-block;
            line-height: 1.7;
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.1);
            border: 1.5px solid rgba(255, 255, 255, 0.3);
            font-size: 0.94rem;
        }
        .bubble.detective {
            background: linear-gradient(135deg, #c8e6f0 0%, #d8eef5 100%);
            color: #2d3d42;
        }
        .bubble.suspect {
            background: linear-gradient(135deg, #f5d4d4 0%, #f8e0e0 100%);
            border-color: rgba(232, 114, 111, 0.2);
            color: #3d4d42;
        }
        .accuse-card {
            background: linear-gradient(135deg, #fef8f0 0%, #fdf4e8 100%);
            border: 2px solid rgba(232, 178, 121, 0.25);
            padding: 1.6rem;
            border-radius: 26px;
            box-shadow: 0 12px 32px rgba(100, 60, 20, 0.16);
        }
        .accuse-title {
            font-family: 'Fredoka', sans-serif;
            color: #3d4d42;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        .accuse-highlight {
            color: #e8726f;
            font-weight: 700;
        }
        .reveal-panel {
            background: linear-gradient(135deg, #e8f8d8 0%, #f0fce0 100%);
            border: 2px solid rgba(107, 159, 127, 0.25);
            padding: 2rem;
            position: relative;
        }
        .reveal-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.75rem 1.2rem;
            font-family: 'Fredoka', sans-serif;
            font-size: 0.95rem;
            letter-spacing: 0.06em;
            background: linear-gradient(135deg, #f5d4d4 0%, #ffe8c3 100%);
            color: #5d3d1f;
            border: 1.5px solid rgba(232, 178, 121, 0.2);
            border-radius: 999px;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        .reveal-title {
            font-family: 'Fredoka', sans-serif;
            font-size: clamp(1.6rem, 3.5vw, 2.8rem);
            color: #3d4d42;
            margin-bottom: 0.8rem;
            font-weight: 700;
        }
        .reveal-subtitle {
            color: #3d4d42;
            line-height: 1.8;
            margin-bottom: 1.3rem;
            font-weight: 500;
        }
        .confetti {
            font-size: 1.6rem;
            margin-right: 0.3rem;
        }
        input[type='radio'] {
            accent-color: #6b9f7f;
        }
        div[role='radiogroup'] label {
            color: #3d4d42;
            font-family: 'Quicksand', sans-serif;
            font-size: 0.98rem;
            font-weight: 500;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class='investigation-hero'>
            <div style='display:flex; align-items:center; justify-content:space-between; gap:2rem; flex-wrap:wrap;'>
                <div style='max-width: 860px; width: 100%;'>
                    <div class='hero-title'>DETECTIVE HEADQUARTERS</div>
                    <div class='hero-subtitle'>Uncover clues, interrogate suspects, and solve the mystery in this immersive detective adventure.</div>
                    <div class='hero-badge'>🕵️ New Case Available</div>
                </div>
                <div style='margin-top: 1rem;'>
                    <button class='primary-button hero-cta' onclick='window.location.href="#start-game"'>Enter Investigation</button>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_detective_hub(game_data):
    rank_name, rank_progress = get_rank(game_data["detective_score"])
    badge_list = get_achievement_badges(game_data)
    progress = calculate_progress(game_data)

    with st.container():
        st.markdown("<div class='headquarters-panel'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-heading'>{game_data.get('case_title', 'Active Case')}</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='detective-card'>
                <div class='profile-avatar'>🕵️</div>
                <div class='profile-meta'>
                    <div><strong>Location:</strong> {game_data.get('location', 'Unknown')}</div>
                    <div><strong>Victim:</strong> {game_data.get('victim', 'Unknown')}</div>
                    <div><strong>Case ID:</strong> {game_data.get('case_id', 'UNKNOWN')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='stat-tile'><div class='stat-title'>Investigation Score</div><div class='stat-value'>{game_data['detective_score']} XP</div></div>"
            f"<div class='stat-tile'><div class='stat-title'>Rank</div><div class='stat-value'>{rank_name}</div></div>"
            f"<div class='stat-tile'><div class='stat-title'>Case Progress</div><div class='stat-value'>{progress}%</div></div>"
            f"<div class='stat-tile'><div class='stat-title'>Evidence Collected</div><div class='stat-value'>{game_data["clues_found"]}/{len(game_data['clues'])}</div></div>"
            f"<div class='stat-tile'><div class='stat-title'>Case Status</div><div class='stat-value'>{'ACTIVE' if not st.session_state.accusation_result else 'RESOLVED'}</div></div>"
            f"<div class='stat-tile'><div class='stat-title'>Difficulty</div><div class='stat-value'>{game_data['case_difficulty']}</div></div>"
            f"<div class='stat-tile'><div class='stat-title'>Accusations Remaining</div><div class='stat-value'>{game_data['max_accusations'] - game_data['accusations_made']}/{game_data['max_accusations']}</div></div>"
            ,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='section-heading'>Investigation Badges</div>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex; gap:0.75rem; flex-wrap:wrap;'>" + "".join([f"<span class='badge'>{badge}</span>" for badge in badge_list]) + "</div>", unsafe_allow_html=True)
        if st.button("Start New Case"):
            reset_state()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def render_suspect_wall(game_data):
    st.markdown("<div class='section-heading'>Suspect Wall</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for index, suspect in enumerate(game_data["suspects"]):
        danger = "High" if index == game_data["murderer_index"] else "Medium"
        with cols[index]:
            st.markdown(
                f"""
                <div class='file-card' style='transform: rotate({-4 + index * 4}deg);'>
                    <div class='file-pin'></div>
                    <div class='file-header'>
                        <div class='file-name'>{suspect['name']}</div>
                        <div class='threat-tag'>{danger}</div>
                    </div>
                    <div class='file-detail'><strong>Occupation:</strong> {suspect.get('occupation', 'Unknown')}</div>
                    <div class='file-detail'><strong>Motive:</strong> {suspect.get('motive', suspect.get('suspicious_behavior', 'Unknown'))}</div>
                    <div class='file-detail'><strong>Alibi:</strong> {suspect.get('alibi', 'Not stated')}</div>
                    <div class='file-line'></div>
                    <div class='file-detail'><strong>Status:</strong> {'Interrogated' if suspect.get('interrogated', False) else 'Not yet interviewed'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Interrogate", key=f"suspect_{index}"):
                st.session_state.selected_suspect = index
                if not game_data["suspects"][index]["interrogated"]:
                    game_data["suspects"][index]["interrogated"] = True
                    game_data["clues_found"] += 1
                    contradiction = check_contradiction(game_data, index)
                    if contradiction:
                        st.session_state.notice = f"Contradiction uncovered: {contradiction['message']}"
                        st.session_state.show_clues = True
                    else:
                        st.session_state.notice = "Interrogation complete. Continue exploring evidence."


def render_evidence_board(game_data):
    st.markdown("<div class='section-heading'>Evidence Board</div>", unsafe_allow_html=True)
    st.markdown("<div class='board-panel'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1.25rem;'>
            <div style='font-family: Poppins, sans-serif; font-size:1.05rem; color:#1D3557; font-weight:700;'>Pinned Evidence</div>
            <div style='color:#1F2937; font-size:0.95rem;'>The case board updates as you discover clues.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.show_clues:
        if st.button("Investigate the Scene"):
            game_data["clues_found"] += 3
            if game_data["clues_found"] > len(game_data["clues"]):
                game_data["clues_found"] = len(game_data["clues"])
            st.session_state.show_clues = True
            st.session_state.notice = "Evidence is now visible on the board."

    cols = st.columns(3)
    for index, clue in enumerate(game_data["clues"]):
        with cols[index % 3]:
            if st.session_state.show_clues:
                st.markdown(
                    f"""
                    <div class='evidence-card'>
                        <div class='evidence-pin'></div>
                        <div class='evidence-title'>Evidence {index + 1}</div>
                        <div class='evidence-detail'>{clue}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class='evidence-card locked'>
                        <div class='evidence-pin'></div>
                        <div class='evidence-title'>Undiscovered</div>
                        <div class='evidence-detail'>This clue remains hidden until the scene is searched.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    st.markdown("</div>", unsafe_allow_html=True)


def render_interrogation_room(game_data):
    st.markdown("<div class='section-heading'>Interrogation Chamber</div>", unsafe_allow_html=True)
    st.markdown("<div class='scene-panel'>", unsafe_allow_html=True)
    selected = st.session_state.selected_suspect
    if selected is None:
        st.markdown(
            "<div style='color:#3d4d42;'>Select a suspect from the wall to begin interrogation.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    suspect = game_data["suspects"][selected]
    location = game_data.get("location", "the crime scene")
    st.markdown(
        f"""
        <div class='bubble detective'>Detective: "Tell me about your whereabouts at {location}."</div>
        <div class='bubble suspect'>Suspect: "{suspect.get('alibi', 'I was not involved.')}"</div>
        <div class='bubble detective'>Detective: "What do you know about the motive here?"</div>
        <div class='bubble suspect'>Suspect: "{suspect.get('suspicious_behavior', 'Nothing unusual.')}"</div>
        """,
        unsafe_allow_html=True,
    )
    if suspect["contradiction_found"]:
        clue_text = game_data["clues"][suspect["contradiction_clue_index"]]
        st.markdown(
            f"""
            <div class='bubble detective' style='background: rgba(230, 57, 70, 0.18); border-color: rgba(230, 57, 70, 0.25);'>
                Detective: "This evidence contradicts your story: {clue_text}. Explain yourself."
            </div>
            <div class='bubble suspect' style='background: rgba(255, 255, 255, 0.14); color:#3d4d42; border:1px solid rgba(107,159,127,0.16);'>
                Suspect: "{suspect.get('contradiction_text', 'I have no explanation.')}"
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_accusation_theater(game_data):
    st.markdown("<div class='section-heading'>Final Accusation</div>", unsafe_allow_html=True)
    st.markdown("<div class='accuse-card'>", unsafe_allow_html=True)
    suspects = [suspect['name'] for suspect in game_data['suspects']]
    choice = st.radio("Choose your final suspect", suspects, index=st.session_state.accusation_choice)
    st.session_state.accusation_choice = suspects.index(choice)
    st.markdown("<div style='margin: 1rem 0; color:#3d4d42;'>Make your final determination. This decision will determine the case outcome.</div>", unsafe_allow_html=True)
    if st.button("Lock in Accusation"):
        st.session_state.show_accuse_confirm = True

    if st.session_state.show_accuse_confirm:
        st.markdown(
            f"""
            <div style='padding:1.2rem; border-radius:22px; background: linear-gradient(135deg, #7bc3a8 0%, #6bb59b 100%); color:#fff8f0; margin-bottom:1rem;'>
                <strong>Confirm Accusation:</strong> You are accusing <span class='accuse-highlight' style='color:#fff8f0;'>{choice}</span> of the murder.
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Execute Accusation"):
            result = accuse_suspect(game_data, st.session_state.accusation_choice)
            st.session_state.accusation_result = result['outcome']
            st.session_state.notice = result['message']
            st.session_state.show_accuse_confirm = False
            if result['outcome'] == 'won':
                st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)


def render_murderer_reveal(game_data):
    murderer = game_data['suspects'][game_data['murderer_index']]['name']
    badges = get_achievement_badges(game_data)
    st.markdown("<div class='reveal-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='reveal-badge'><span class='confetti'>🎉</span>CASE CLOSED</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='reveal-title'>Justice Delivered</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='reveal-subtitle'>You identified the murderer: <strong>{murderer}</strong>. The investigation is complete.</div>", unsafe_allow_html=True)
    
    solution = game_data.get('solution_summary', 'Every piece of evidence led to the guilty party.')
    st.markdown(f"<div style='padding: 1rem; background: rgba(107, 159, 127, 0.08); border-radius: 16px; margin: 1rem 0; color: #3d4d42;'><strong>Case Summary:</strong> {solution}</div>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div class='stat-tile'><div class='stat-title'>Final Score</div><div class='stat-value'>{game_data['detective_score']} XP</div></div>
        <div class='stat-tile'><div class='stat-title'>Clues Discovered</div><div class='stat-value'>{len(game_data['clues']) if game_data['clues_viewed'] else 0}/{len(game_data['clues'])}</div></div>
        <div class='stat-tile'><div class='stat-title'>Accusations Used</div><div class='stat-value'>{game_data['accusations_made']}/{game_data['max_accusations']}</div></div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='display:flex; gap:1rem; flex-wrap:wrap;'>" + "".join([f"<span class='badge'>{badge}</span>" for badge in badges]) + "</div>", unsafe_allow_html=True)
    if st.button("Investigate New Case"):
        reset_state()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_case_outcome(game_data):
    if st.session_state.accusation_result == 'won':
        render_murderer_reveal(game_data)
    elif st.session_state.accusation_result == 'lost':
        st.markdown("<div class='reveal-panel'>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><div style='font-size: 2rem; margin-bottom: 1rem;'>❌</div><div style='font-size: 1.4rem; color: #3d4d42; font-weight: 700; margin-bottom: 1rem;'>Case Failed</div></div>", unsafe_allow_html=True)
        st.markdown("<div style='color: #3d4d42; margin: 1rem 0;'>The investigation stalled. You've exhausted all available accusations and the real murderer escaped justice.</div>", unsafe_allow_html=True)
        if st.button("Start Fresh Investigation"):
            reset_state()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Murder Mystery Investigation", page_icon="🕵️‍♂️", layout="wide")
    inject_custom_css()
    ensure_session_state()

    if not st.session_state.started:
        render_hero()
        if st.button("Start the Investigation"):
            st.session_state.started = True
            st.session_state.game_data = initialize_game()
            st.rerun()
        return

    if st.session_state.game_data is None:
        st.session_state.game_data = initialize_game()

    game_data = st.session_state.game_data

    if st.session_state.accusation_result:
        render_case_outcome(game_data)
        return

    st.markdown("<div id='start-game'></div>", unsafe_allow_html=True)
    columns = st.columns((1.2, 1))
    with columns[0]:
        render_detective_hub(game_data)
    with columns[1]:
        render_suspect_wall(game_data)

    render_evidence_board(game_data)
    render_interrogation_room(game_data)
    render_accusation_theater(game_data)

    if st.session_state.notice:
        st.markdown(f"<div style='padding:1rem; border-radius:20px; background: rgba(107, 159, 127, 0.15); color:#3d4d42; margin-top:1rem; border: 1px solid #c8e6c8;'>{st.session_state.notice}</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
