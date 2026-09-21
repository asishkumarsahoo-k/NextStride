# NextStride
An AI-architected career accelerator and step-gated proof-of-work platform built with Streamlit and Gemini Flash.
# ⚡ NextStride | Neural Career Accelerator

> **Tip:** For the best visual experience and immersive cyber-terminal aesthetics, we recommend using the platform in **🌙 Night Mode** (toggleable directly from the sidebar).

NextStride is an AI-architected career engineering platform that replaces passive tutorial checklists with rigorous, step-gated proof-of-work challenges. Built entirely in Python using Streamlit and the Google GenAI SDK (`gemini-3.6-flash` / `gemini-3.5-flash-lite`), NextStride guides developers through structured, production-grade milestone tracks that unlock only when their submissions satisfy automated AI rubrics.

---

## 🌟 Key Features

- **Autonomous 6-Tier Step Gating:** Progresses sequentially through 6 foundational-to-production tiers (Tooling, Streaming & Memory, Type Safety, Testing, Concurrency, and Containerization). Each tier remains locked until your submission achieves a passing score ($\ge 70/100$).
- **Granular Blueprints (4+ Steps per Stage):** Every stage provides at least 4 detailed blueprint expanders featuring comprehensive architectural guidance and executable code snippets.
- **OR-Mode Verification Gates:** Candidates can submit proof via terminal source code, 1 to 3 execution screenshots, or both.
- **Dual Evaluator Calibration:** Toggle between **Supportive Mentor** (educational feedback and hints) and **Strict Interviewer** (production security and edge-case auditing) modes.
- **Language & Systems Lab:** Practice systems programming languages (Python, TypeScript, Go, Rust, Java, C++, SQL) in either *Free Learning Mode* or step-gated *Job Mode*.
- **Privacy-Shielded Recruiter Dossiers:** Shareable public URLs (`?cred=NS-XXXXXX`) that display candidate competency metrics and 5-point rubric proofs while protecting private OS directories, source code, and API keys.
- **High-Contrast Theming Engine:** Custom CSS engine supporting randomized dual-tone gradients in Day Mode with pastel-pink card architecture, alongside a high-contrast cyber Night Mode.
- **Deterministic Offline Demo Engine:** Fully functional out of the box with pre-seeded verified pathways (`NS-859916` and `NS-412093`) when running without an active Gemini API key.

---

## 🛠️ Tech Stack

- **Frontend & App Engine:** [Streamlit](https://streamlit.io/) (100% Pure Python)[cite: 12, 13]
- **AI Assessment & Chat Engine:** [Google GenAI SDK](https://pypi.org/project/google-genai/) (`gemini-3.6-flash`, `gemini-3.5-flash-lite`)
- **Vector Icons:** Embedded inline SVG vector library
- **State Management:** Reactive session-state machine with native query parameter routing (`st.query_params`)

---

## 📂 Project Structure

```text
nextstride/
├── app.py              # Main monolithic Streamlit application
├── requirements.txt    # Production runtime dependencies
└── README.md           # Project documentation and setup guide
🚀 Getting Started
1. Clone the Repository
Bash
git clone [https://github.com/](https://github.com/)<asishkumarsahoo-k>/<NextStride>.git
cd <NextStride>
2. Set Up a Virtual Environment
Bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Gemini API Key (Optional)
NextStride functions offline with pre-seeded demonstration pathways[cite: 12]. To enable dynamic AI roadmap generation and live submission evaluation, set your API key:

Bash
# On Windows (Command Prompt)
set GEMINI_API_KEY=AIzaSyYourActualKeyHere

# On Windows (PowerShell)
$env:GEMINI_API_KEY="AIzaSyYourActualKeyHere"

# On macOS/Linux
export GEMINI_API_KEY="AIzaSyYourActualKeyHere"
(Alternatively, enter your key directly inside the collapsible API Key Configuration expander in the application sidebar).

5. Launch the Application
Bash
streamlit run app.py
The application will open in your default browser at http://localhost:8501.

📋 Recruiter Verification View
To view the sandboxed recruiter dossier interface, append the demo credential ID to your URL:

Python Foundations Dossier: http://localhost:8501/?cred=NS-859916

Production API & Microservices Dossier: http://localhost:8501/?cred=NS-412093
