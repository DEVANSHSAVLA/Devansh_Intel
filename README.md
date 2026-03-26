# 💎 DEVANSH INTEL: Executive Market Terminal
**DEVANSH INTEL** is a high-performance, enterprise-grade AI terminal for recruitment intelligence, career pathing, and strategic decisioning. Powered by the **Vanguard Pro++ Engine**, it guarantees 100% stable, high-fidelity visualizations across all strategic nodes.

## 🚀 Signature Features
- **🕸️ DEVANSH Relational Engine**: Dependency-free visual map of skill architecture (100% Online).
- **🤖 Trajectory Simulator PRO**: High-FID Radar Charts with market difficulty indexing.
- **📄 Neural Resume Intel**: Achievement-centric Bullet AI and ATS keyword density optimization.
- **💰 Salary Intelligence PRO**: High-ROI compensation matrix with automatic data hydration.
- **📉 Strategic Audit Engine**: Multi-page high-resolution PDF reporting (`DEVANSH_Strategic_Audit_v5.pdf`).

## 🛠️ Quick Start

### 1. Setup Environment
```bash
python -m venv venv
.\venv\Scripts\activate.ps1  # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run Data Pipeline (v3.0)
```bash
$env:PYTHONPATH="."
python src/generate_data.py   # Generate synthetic jobs
python src/cleaning.py        # Clean data
python src/skill_extractor.py # Extract v3.0 features (Salary, Exp, Edu)
python src/salary_predictor.py # Train Elite Salary Model
```

### 3. Launch Elite Dashboard
```bash
streamlit run app.py
```

## 📂 Project Structure
- `app.py`: The Main Elite Terminal.
- `src/`: Modular AI & NLP engines (Simulator, Knowledge Graph, Resume Pro, etc.).
- `data/`: Cleaned job market datasets.
- `models/`: Trained ML weights and encoders.

## 📜 Documentation
- [Project Overview](.gemini/antigravity/brain/51432095-7614-423f-999e-a285b10c0d4b/project_overview.md)
- [Walkthrough & Verification](.gemini/antigravity/brain/51432095-7614-423f-999e-a285b10c0d4b/walkthrough.md)
- [Task Progress](.gemini/antigravity/brain/51432095-7614-423f-999e-a285b10c0d4b/task.md)

---
*Built with ❤️ by AI Job Market Intelligence Team*
