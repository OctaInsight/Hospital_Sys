# Jasmine Hospital System — Prototype

A quick, clickable Streamlit prototype of the unified hospital information
system described in the improvement proposal for Abdullah Issa Specialized
Hospital: one application, one database, shared across every department.

This is a **demo**, not a production system — data lives in a local SQLite
file (`hospital.db`) created automatically the first time the app runs, and
passwords are stored in plain text for simplicity.

## Features in this prototype

- Top bar language toggle: English / Arabic (switches text and page direction to RTL)
- Login / logout with role-based navigation (admin, doctor, pharmacist, reception, call center, PR)
- Reception & queue (also reused for Emergency, Lab & Radiology, Inpatient/ICU, Contracts)
- **Pharmacy module** — a doctor sends a medication order for a patient straight to the
  pharmacy queue; the pharmacist sees it appear live and marks it dispensed or rejected
- Call center call logging
- PR & complaints tracking
- A small dashboard with live counts pulled from the same database every module writes to

## Demo accounts

| Username | Password | Role |
|---|---|---|
| admin | admin123 | sees every module |
| doctor | doctor123 | creates medication orders |
| pharmacist | pharm123 | dispenses medication orders |
| reception | recep123 | reception & queue |
| callcenter | call123 | call center |
| pr | pr123 | PR & complaints |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Push to GitHub

```bash
git init
git add .
git commit -m "Jasmine Hospital System prototype"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Deploy for free on Streamlit Community Cloud

1. Push this folder to a GitHub repo (steps above).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, pick the repo/branch, set the main file to `app.py`.
4. Click **Deploy** — you'll get a public `https://<something>.streamlit.app` link
   you can send to the hospital director to click through.

## Project structure

```
hospital-prototype/
├── app.py            # UI, navigation, login, language toggle, all pages
├── db.py             # SQLite schema, seed data, data access functions
├── i18n.py           # English/Arabic translation dictionary
├── requirements.txt
└── README.md
```

## Extending it

- Add new UI text by adding a key to `TRANSLATIONS` in `i18n.py`, then call `t("your_key")`.
- Add a new module by writing a `page_xxx()` function in `app.py`, registering it in
  `ROUTES`, and adding it to the relevant role(s) in `NAV_BY_ROLE`.
- Swap SQLite for Postgres/MySQL later by changing only `db.py` — the rest of the
  app talks to it through plain function calls, not raw SQL.
