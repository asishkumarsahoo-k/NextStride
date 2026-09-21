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
- **Dual Evaluator Calibration:** Toggle between **Supportive Mentor** (educational feedback and hints) and **Strict Interviewer** (production security and edge-case auditing) modes[cite: 12].
- **Language & Systems Lab:** Practice systems programming languages (Python, TypeScript, Go, Rust, Java, C++, SQL) in either *Free Learning Mode* or step-gated *Job Mode*[cite: 12].
- **Privacy-Shielded Recruiter Dossiers:** Shareable public URLs (`?cred=NS-XXXXXX`) that display candidate competency metrics and 5-point rubric proofs while protecting private OS directories, source code, and API keys[cite: 12].
- **High-Contrast Theming Engine:** Custom CSS engine supporting randomized dual-tone gradients in Day Mode with pastel-pink card architecture, alongside a high-contrast cyber Night Mode[cite: 12].
- **Deterministic Offline Demo Engine:** Fully functional out of the box with pre-seeded verified pathways (`NS-859916` and `NS-412093`) when running without an active Gemini API key[cite: 12].

---

## 🛠️ Tech Stack

- **Frontend & App Engine:** [Streamlit](https://streamlit.io/) (100% Pure Python)[cite: 12, 13]
- **AI Assessment & Chat Engine:** [Google GenAI SDK](https://pypi.org/project/google-genai/) (`gemini-3.6-flash`, `gemini-3.5-flash-lite`)[cite: 12, 13]
- **Vector Icons:** Embedded inline SVG vector library[cite: 12]
- **State Management:** Reactive session-state machine with native query parameter routing (`st.query_params`)[cite: 12]

---

## 📂 Project Structure

```text
nextstride/
├── app.py              # Main monolithic Streamlit application
├── requirements.txt    # Production runtime dependencies
└── README.md           # Project documentation and setup guide
