"""
Jasmine Hospital System — Streamlit prototype.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

Demo accounts (see db.py seed data):
    admin / admin123        (sees every module)
    doctor / doctor123      (creates medication orders)
    pharmacist / pharm123   (dispenses medication orders)
    reception / recep123    (reception & queue)
    callcenter / call123    (call center log)
    pr / pr123              (PR & complaints)
"""

import streamlit as st
import db
from i18n import t as translate

st.set_page_config(page_title="Jasmine Hospital System", page_icon="🏥", layout="wide")

db.init_db()

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "user" not in st.session_state:
    st.session_state.user = None


def t(key: str) -> str:
    return translate(key, st.session_state.lang)


# ---------------------------------------------------------------------------
# Global styling — flips the whole page to RTL when Arabic is selected
# ---------------------------------------------------------------------------
is_ar = st.session_state.lang == "ar"
st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        direction: {"rtl" if is_ar else "ltr"};
        text-align: {"right" if is_ar else "left"};
    }}
    .top-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Which name field to read from patients/users depending on language
NAME_FIELD = "name_ar" if is_ar else "name_en"

# ---------------------------------------------------------------------------
# Top bar: title + language toggle + login/logout
# ---------------------------------------------------------------------------
top_l, top_r = st.columns([3, 2])
with top_l:
    st.markdown(f"### 🏥 {t('app_title')}")
    st.caption(t("tagline"))
with top_r:
    b1, b2, b3 = st.columns([1, 1, 2])
    with b1:
        if st.button("EN", use_container_width=True, type="primary" if not is_ar else "secondary"):
            st.session_state.lang = "en"
            st.rerun()
    with b2:
        if st.button("AR", use_container_width=True, type="primary" if is_ar else "secondary"):
            st.session_state.lang = "ar"
            st.rerun()
    with b3:
        if st.session_state.user:
            st.write(f"**{t('logged_in_as')}:** {st.session_state.user[NAME_FIELD]}")

if st.session_state.user:
    with st.sidebar:
        st.write(f"👤 {st.session_state.user[NAME_FIELD]}")
        st.caption(f"{t('role')}: {st.session_state.user['role']}")
        if st.button(f"🚪 {t('logout')}", use_container_width=True):
            st.session_state.user = None
            st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# Login screen
# ---------------------------------------------------------------------------
if not st.session_state.user:
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        st.subheader(t("login"))
        with st.form("login_form"):
            username = st.text_input(t("username"))
            password = st.text_input(t("password"), type="password")
            submitted = st.form_submit_button(t("login_button"), use_container_width=True)
        if submitted:
            user = db.authenticate(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error(t("login_error"))

        with st.expander(t("demo_accounts")):
            st.code(
                "admin / admin123\n"
                "doctor / doctor123\n"
                "pharmacist / pharm123\n"
                "reception / recep123\n"
                "callcenter / call123\n"
                "pr / pr123"
            )
    st.stop()

# ---------------------------------------------------------------------------
# Role-based navigation
# ---------------------------------------------------------------------------
role = st.session_state.user["role"]

NAV_BY_ROLE = {
    "admin": ["dashboard", "reception", "emergency", "lab_radiology", "inpatient_icu",
              "contracts", "call_center", "pr_crm", "pharmacy"],
    "doctor": ["dashboard", "pharmacy"],
    "pharmacist": ["dashboard", "pharmacy"],
    "reception": ["dashboard", "reception"],
    "call_center": ["dashboard", "call_center"],
    "pr": ["dashboard", "pr_crm"],
}
NAV_LABELS = {
    "dashboard": "nav_dashboard",
    "reception": "nav_reception",
    "emergency": "nav_emergency",
    "lab_radiology": "nav_lab_radiology",
    "inpatient_icu": "nav_inpatient_icu",
    "contracts": "nav_contracts",
    "call_center": "nav_call_center",
    "pr_crm": "nav_pr_crm",
    "pharmacy": "nav_pharmacy",
}

pages = NAV_BY_ROLE.get(role, ["dashboard"])
with st.sidebar:
    st.markdown("---")
    choice = st.radio(
        t("nav_dashboard"),
        options=pages,
        format_func=lambda k: t(NAV_LABELS[k]),
        label_visibility="collapsed",
    )

patients = db.list_patients()
patient_options = {p["id"]: f"{p[NAME_FIELD]} ({p['mrn']})" for p in patients}


def patient_label(pid):
    return patient_options.get(pid, str(pid))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
def page_dashboard():
    st.subheader(t("dashboard_overview"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("total_patients"), len(patients))
    c2.metric(t("patients_in_queue"), len([q for q in db.list_queue() if q["status"] != "done"]))
    c3.metric(t("pending_medication_orders"), len(db.list_medication_orders(status="pending")))
    c4.metric(t("open_complaints"), len(db.list_complaints(status="open")))
    st.info(t("prototype_note"))


# ---------------------------------------------------------------------------
# Reception & generic department queue (reused for ER, Lab/Radiology, Contracts)
# ---------------------------------------------------------------------------
def page_queue(department_key: str, department_label_key: str):
    st.subheader(t(department_label_key))

    with st.form(f"queue_form_{department_key}"):
        pid = st.selectbox(t("select_patient"), options=list(patient_options.keys()), format_func=patient_label)
        submitted = st.form_submit_button(t("add"))
    if submitted:
        db.add_to_queue(pid, department_key)
        st.success(t("add_to_queue"))
        st.rerun()

    st.markdown(f"**{t('current_queue')}**")
    rows = db.list_queue(department=department_key)
    if not rows:
        st.caption(t("no_data"))
        return

    for r in rows:
        cols = st.columns([1, 3, 2, 2, 2])
        cols[0].write(f"#{r['id']}")
        cols[1].write(r[NAME_FIELD])
        status_label = {"waiting": t("waiting"), "in_service": t("in_service"), "done": t("done")}[r["status"]]
        cols[2].write(status_label)
        cols[3].write(r["created_at"])
        with cols[4]:
            if r["status"] == "waiting":
                if st.button(t("call_next"), key=f"call_{department_key}_{r['id']}"):
                    db.update_queue_status(r["id"], "in_service")
                    st.rerun()
            elif r["status"] == "in_service":
                if st.button(t("mark_done"), key=f"done_{department_key}_{r['id']}"):
                    db.update_queue_status(r["id"], "done")
                    st.rerun()


# ---------------------------------------------------------------------------
# Pharmacy module — the core new ask: send medication orders to pharmacy
# ---------------------------------------------------------------------------
def page_pharmacy():
    st.subheader(t("nav_pharmacy"))

    if role in ("doctor", "admin"):
        st.markdown(f"**{t('new_medication_order')}**")
        with st.form("medication_order_form"):
            pid = st.selectbox(t("select_patient"), options=list(patient_options.keys()), format_func=patient_label)
            medicine = st.text_input(t("medicine_name"))
            dosage = st.text_input(t("dosage"))
            instructions = st.text_area(t("instructions"))
            submitted = st.form_submit_button(t("send_to_pharmacy"))
        if submitted and medicine:
            db.create_medication_order(
                patient_id=pid,
                medicine=medicine,
                dosage=dosage,
                instructions=instructions,
                ordered_by=st.session_state.user[NAME_FIELD],
            )
            st.success(t("order_sent"))
            st.rerun()

        st.markdown(f"**{t('my_recent_orders')}**")
        mine = db.list_medication_orders(ordered_by=st.session_state.user[NAME_FIELD])
        if not mine:
            st.caption(t("no_data"))
        else:
            for o in mine[:10]:
                status_map = {"pending": t("pending"), "dispensed": t("dispensed"), "rejected": t("rejected")}
                st.write(f"#{o['id']} — {o[NAME_FIELD]} — {o['medicine']} ({o['dosage']}) — "
                         f"**{status_map[o['status']]}** — {o['created_at']}")
        st.divider()

    if role in ("pharmacist", "admin"):
        st.markdown(f"**{t('pharmacy_queue')}**")
        pending = db.list_medication_orders(status="pending")
        if not pending:
            st.caption(t("no_pending_orders"))
        for o in pending:
            with st.container(border=True):
                cols = st.columns([3, 2, 2, 2, 1, 1])
                cols[0].write(f"**{o[NAME_FIELD]}** ({o['mrn']})")
                cols[1].write(f"{o['medicine']} — {o['dosage']}")
                cols[2].write(f"{t('ordered_by')}: {o['ordered_by']}")
                cols[3].write(f"{t('ordered_at')}: {o['created_at']}")
                if o["instructions"]:
                    st.caption(o["instructions"])
                if cols[4].button(t("dispense"), key=f"disp_{o['id']}"):
                    db.update_medication_status(o["id"], "dispensed")
                    st.rerun()
                if cols[5].button(t("reject"), key=f"rej_{o['id']}"):
                    db.update_medication_status(o["id"], "rejected")
                    st.rerun()


# ---------------------------------------------------------------------------
# Call Center
# ---------------------------------------------------------------------------
def page_call_center():
    st.subheader(t("nav_call_center"))
    with st.form("call_form"):
        caller = st.text_input(t("caller_name"))
        phone = st.text_input(t("phone"))
        purpose = st.selectbox(
            t("purpose"),
            options=["book_appointment", "follow_up", "complaint", "general_inquiry"],
            format_func=lambda k: t(k),
        )
        submitted = st.form_submit_button(t("save_call"))
    if submitted and caller:
        db.log_call(caller, phone, t(purpose))
        st.success(t("save_call"))
        st.rerun()

    st.markdown(f"**{t('recent_calls')}**")
    calls = db.list_calls()
    if not calls:
        st.caption(t("no_data"))
    for c in calls[:15]:
        st.write(f"#{c['id']} — {c['caller_name']} ({c['phone']}) — {c['purpose']} — {c['created_at']}")


# ---------------------------------------------------------------------------
# PR & Complaints
# ---------------------------------------------------------------------------
def page_pr_crm():
    st.subheader(t("nav_pr_crm"))
    with st.form("complaint_form"):
        pid = st.selectbox(
            t("select_patient"),
            options=[None] + list(patient_options.keys()),
            format_func=lambda k: "-" if k is None else patient_label(k),
        )
        description = st.text_area(t("description"))
        submitted = st.form_submit_button(t("submit_complaint"))
    if submitted and description:
        db.create_complaint(description, pid)
        st.success(t("submit_complaint"))
        st.rerun()

    st.markdown(f"**{t('all_complaints')}**")
    complaints = db.list_complaints()
    if not complaints:
        st.caption(t("no_data"))
    for c in complaints:
        with st.container(border=True):
            cols = st.columns([4, 2, 1])
            cols[0].write(c["description"])
            status_label = t("open") if c["status"] == "open" else t("resolved")
            cols[1].write(f"{status_label} — {c['created_at']}")
            if c["status"] == "open":
                if cols[2].button(t("resolve"), key=f"resolve_{c['id']}"):
                    db.update_complaint_status(c["id"], "resolved")
                    st.rerun()


# ---------------------------------------------------------------------------
# Inpatient / ICU — lightweight placeholder built on the same queue table
# ---------------------------------------------------------------------------
def page_inpatient_icu():
    page_queue("inpatient_icu", "nav_inpatient_icu")


def page_emergency():
    page_queue("emergency", "nav_emergency")


def page_lab_radiology():
    page_queue("lab_radiology", "nav_lab_radiology")


def page_contracts():
    page_queue("contracts", "nav_contracts")


def page_reception():
    page_queue("reception", "nav_reception")


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
ROUTES = {
    "dashboard": page_dashboard,
    "reception": page_reception,
    "emergency": page_emergency,
    "lab_radiology": page_lab_radiology,
    "inpatient_icu": page_inpatient_icu,
    "contracts": page_contracts,
    "call_center": page_call_center,
    "pr_crm": page_pr_crm,
    "pharmacy": page_pharmacy,
}

ROUTES[choice]()
