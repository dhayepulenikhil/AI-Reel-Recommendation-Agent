import streamlit as st
import re

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Reel Recommendation Agent",
    page_icon="🎬",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🎬 AI Reel Recommendation Agent")

st.caption(
    "Understand interests. Recommend useful technology content."
)

st.divider()


# ============================================================
# SAMPLE / ANONYMIZED STUDENT REEL HISTORY
# ============================================================

student_history = [
    {
        "title": "Java Programming Meme",
        "description": "Funny Java meme about software developers",
        "category": "Java"
    },
    {
        "title": "Software Engineer Lifestyle",
        "description": "Day in the life of a software engineer",
        "category": "Career"
    },
    {
        "title": "Coding Interview Joke",
        "description": "Funny coding interview and programming problem joke",
        "category": "DSA"
    },
    {
        "title": "Laptop Comparison",
        "description": "Laptop comparison for programmers and developers",
        "category": "Hardware"
    }
]


# ============================================================
# TECHNOLOGY RECOMMENDATION DATABASE
# ============================================================

recommendations = [
    {
        "title": "Understanding Data Structures for Coding Interviews",
        "category": "DSA",
        "difficulty": "Intermediate",
        "topics": [
            "software",
            "programming",
            "coding",
            "developer",
            "interview",
            "java",
            "dsa"
        ]
    },

    {
        "title": "How Large Language Models Actually Work",
        "category": "AI",
        "difficulty": "Intermediate",
        "topics": [
            "ai",
            "technology",
            "programming",
            "software"
        ]
    },

    {
        "title": "System Design Fundamentals for Software Engineers",
        "category": "HLD",
        "difficulty": "Advanced",
        "topics": [
            "software",
            "developer",
            "engineering",
            "programming",
            "system design"
        ]
    },

    {
        "title": "Cybersecurity Fundamentals for Developers",
        "category": "Cybersecurity",
        "difficulty": "Beginner",
        "topics": [
            "security",
            "cybersecurity",
            "developer",
            "software"
        ]
    },

    {
        "title": "Cloud Computing with AWS",
        "category": "Cloud",
        "difficulty": "Intermediate",
        "topics": [
            "cloud",
            "aws",
            "developer",
            "technology"
        ]
    },

    {
        "title": "Choosing the Right Laptop for Programming",
        "category": "Hardware",
        "difficulty": "Beginner",
        "topics": [
            "laptop",
            "hardware",
            "computer",
            "programming"
        ]
    }
]


# ============================================================
# INTEREST INFERENCE
# ============================================================

def infer_interest(history):

    combined_text = ""

    for reel in history:
        combined_text += " "
        combined_text += reel["title"]
        combined_text += " "
        combined_text += reel["description"]

    text = combined_text.lower()

    interest_groups = {

        "Software Engineering": [
            "java",
            "software",
            "developer",
            "coding",
            "programming",
            "interview",
            "engineer"
        ],

        "Artificial Intelligence": [
            "ai",
            "artificial intelligence",
            "machine learning",
            "llm",
            "neural"
        ],

        "Cybersecurity": [
            "cybersecurity",
            "security",
            "hacking",
            "ethical hacking"
        ],

        "Cloud Computing": [
            "cloud",
            "aws",
            "azure",
            "devops"
        ],

        "Hardware": [
            "laptop",
            "hardware",
            "computer",
            "gpu",
            "processor"
        ]
    }

    scores = {}

    for interest, keywords in interest_groups.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[interest] = score

    best_interest = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_interest]

    # --------------------------------------------------------
    # WHY INTEREST WAS DETECTED
    # --------------------------------------------------------

    matched_topics = []

    for keyword in interest_groups[best_interest]:

        if keyword in text:
            matched_topics.append(keyword)

    if best_score == 0:

        return (
            "Technology",
            "The available interaction history does not provide "
            "enough evidence for a specific technology domain.",
            "Low"
        )

    if best_score >= 4:
        confidence = "High"

    elif best_score >= 2:
        confidence = "Medium"

    else:
        confidence = "Low"

    why = (
        "The student's interaction history contains signals such as "
        + ", ".join(matched_topics)
        + ". These signals indicate a broader interest in "
        + best_interest
        + " rather than a single repeated keyword."
    )

    return (
        best_interest,
        why,
        confidence
    )


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def get_recommendation(interest):

    if interest == "Software Engineering":

        return recommendations[0]

    if interest == "Artificial Intelligence":

        return recommendations[1]

    if interest == "Cybersecurity":

        return recommendations[3]

    if interest == "Cloud Computing":

        return recommendations[4]

    if interest == "Hardware":

        return recommendations[5]

    return recommendations[2]


# ============================================================
# REEL URL INPUT
# ============================================================

st.subheader("📎 Enter Instagram Reel")

reel_url = st.text_input(
    "Instagram Reel URL",
    placeholder="https://www.instagram.com/reel/..."
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🤖 Analyze Reel",
    use_container_width=True
):

    # --------------------------------------------------------
    # URL VALIDATION
    # --------------------------------------------------------

    pattern = r"instagram\.com/reel/([A-Za-z0-9_-]+)"

    match = re.search(
        pattern,
        reel_url
    )

    if not match:

        st.error(
            "❌ Please enter a valid Instagram Reel URL."
        )

    else:

        reel_id = match.group(1)

        # ----------------------------------------------------
        # INTEREST ANALYSIS
        # ----------------------------------------------------

        interest, why, confidence = infer_interest(
            student_history
        )

        recommendation = get_recommendation(
            interest
        )

        # ----------------------------------------------------
        # CURRENT REEL
        # ----------------------------------------------------

        st.success(
            "✅ Instagram Reel detected"
        )

        st.divider()

        st.subheader(
            "🎬 CURRENT REEL"
        )

        st.write(
            "**Reel ID:**",
            reel_id
        )

        st.write(
            "**Reference:**"
        )

        st.code(
            reel_url
        )

        # ----------------------------------------------------
        # CONTENT STATUS
        # ----------------------------------------------------

        st.info(
            "ℹ️ The current Instagram API configuration "
            "does not provide the Reel's actual caption/video "
            "metadata. The prototype therefore uses the "
            "anonymized interaction history required by the "
            "problem statement to infer interest."
        )

        # ----------------------------------------------------
        # INTEREST DETECTED
        # ----------------------------------------------------

        st.subheader(
            "🧠 INTEREST DETECTED"
        )

        st.success(
            interest
        )

        # ----------------------------------------------------
        # WHY
        # ----------------------------------------------------

        st.subheader(
            "🔍 WHY"
        )

        st.write(
            why
        )

        # ----------------------------------------------------
        # RECOMMENDED REEL
        # ----------------------------------------------------

        st.subheader(
            "🚀 RECOMMENDED TECH REEL"
        )

        st.write(
            "**" + recommendation["title"] + "**"
        )

        # ----------------------------------------------------
        # OUTPUT DETAILS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "CATEGORY",
                recommendation["category"]
            )

        with col2:

            st.metric(
                "DIFFICULTY",
                recommendation["difficulty"]
            )

        with col3:

            st.metric(
                "CONFIDENCE",
                confidence
            )

        # ----------------------------------------------------
        # WHY RECOMMENDATION
        # ----------------------------------------------------

        st.subheader(
            "💡 WHY THIS RECOMMENDATION"
        )

        st.success(
            "This recommendation connects the student's "
            + interest.lower()
            + " interest with useful technical learning "
            "content instead of repeating the same type of "
            "Reel."
        )

        # ----------------------------------------------------
        # STUDENT HISTORY
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📱 Student Interaction History"
        )

        for reel in student_history:

            st.write(
                "• **"
                + reel["title"]
                + "** — "
                + reel["category"]
            )

        # ----------------------------------------------------
        # TRAP EXPLANATION
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "🧠 Why This Is Not Simple Keyword Matching"
        )

        st.write(
            "The student interacted with Java, software-engineer "
            "lifestyle, coding-interview and laptop content. "
            "Instead of recommending another generic Java Reel, "
            "the agent infers the broader Software Engineering "
            "interest and recommends DSA content."
        )

        st.success(
            "🎯 Recommendation generated successfully."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Reel Recommendation Agent | BTech Project Prototype"
)