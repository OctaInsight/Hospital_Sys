"""
Simple translation dictionary for the prototype.
Add new keys here and they become available via t("key") in app.py
"""

TRANSLATIONS = {
    "app_title": {"en": "Abdulla Issa Hospital System", "ar": "نظام مستشفى عبدالله عيسى"},
    "tagline": {"en": "Unified Hospital Information System — Prototype",
                "ar": "نظام المعلومات الموحد للمستشفى - نموذج أولي"},

    # Login
    "login": {"en": "Login", "ar": "تسجيل الدخول"},
    "logout": {"en": "Logout", "ar": "تسجيل الخروج"},
    "username": {"en": "Username", "ar": "اسم المستخدم"},
    "password": {"en": "Password", "ar": "كلمة المرور"},
    "login_button": {"en": "Sign in", "ar": "دخول"},
    "login_error": {"en": "Invalid username or password", "ar": "اسم المستخدم أو كلمة المرور غير صحيحة"},
    "welcome": {"en": "Welcome", "ar": "أهلاً بك"},
    "logged_in_as": {"en": "Logged in as", "ar": "مسجل الدخول باسم"},
    "role": {"en": "Role", "ar": "الدور الوظيفي"},
    "demo_accounts": {"en": "Demo accounts (username / password)", "ar": "حسابات تجريبية (اسم المستخدم / كلمة المرور)"},

    # Nav / modules
    "nav_dashboard": {"en": "Dashboard", "ar": "لوحة المتابعة"},
    "nav_reception": {"en": "Reception & Queue", "ar": "الاستقبال والانتظار"},
    "nav_emergency": {"en": "Emergency", "ar": "الطوارئ"},
    "nav_lab_radiology": {"en": "Lab & Radiology", "ar": "المعمل والأشعة"},
    "nav_inpatient_icu": {"en": "Inpatient / ICU", "ar": "الأقسام الداخلية والعناية المركزة"},
    "nav_contracts": {"en": "Contracts", "ar": "التعاقدات"},
    "nav_call_center": {"en": "Call Center", "ar": "مركز الاتصال"},
    "nav_pr_crm": {"en": "PR & Complaints", "ar": "العلاقات العامة والشكاوى"},
    "nav_pharmacy": {"en": "Pharmacy Orders", "ar": "طلبات الصيدلية"},

    # Dashboard
    "dashboard_overview": {"en": "Overview", "ar": "نظرة عامة"},
    "total_patients": {"en": "Total patients", "ar": "إجمالي المرضى"},
    "patients_in_queue": {"en": "Patients in queue", "ar": "المرضى في الانتظار"},
    "pending_medication_orders": {"en": "Pending medication orders", "ar": "طلبات أدوية معلقة"},
    "open_complaints": {"en": "Open complaints", "ar": "شكاوى مفتوحة"},

    # Reception / Queue
    "add_to_queue": {"en": "Add patient to queue", "ar": "إضافة مريض إلى الانتظار"},
    "select_patient": {"en": "Select patient", "ar": "اختر المريض"},
    "department": {"en": "Department", "ar": "القسم"},
    "add": {"en": "Add", "ar": "إضافة"},
    "current_queue": {"en": "Current queue", "ar": "قائمة الانتظار الحالية"},
    "ticket_no": {"en": "Ticket #", "ar": "رقم التذكرة"},
    "patient": {"en": "Patient", "ar": "المريض"},
    "status": {"en": "Status", "ar": "الحالة"},
    "waiting": {"en": "Waiting", "ar": "في الانتظار"},
    "in_service": {"en": "In service", "ar": "قيد الخدمة"},
    "done": {"en": "Done", "ar": "منتهي"},
    "call_next": {"en": "Call next", "ar": "استدعاء التالي"},
    "mark_done": {"en": "Mark done", "ar": "تمت الخدمة"},

    # Medication / Pharmacy
    "new_medication_order": {"en": "New medication order", "ar": "طلب دواء جديد"},
    "medicine_name": {"en": "Medicine name", "ar": "اسم الدواء"},
    "dosage": {"en": "Dosage", "ar": "الجرعة"},
    "instructions": {"en": "Instructions", "ar": "تعليمات"},
    "send_to_pharmacy": {"en": "Send to pharmacy", "ar": "إرسال إلى الصيدلية"},
    "order_sent": {"en": "Medication order sent to pharmacy", "ar": "تم إرسال طلب الدواء إلى الصيدلية"},
    "pharmacy_queue": {"en": "Pharmacy queue", "ar": "قائمة طلبات الصيدلية"},
    "ordered_by": {"en": "Ordered by", "ar": "طلب بواسطة"},
    "ordered_at": {"en": "Ordered at", "ar": "وقت الطلب"},
    "pending": {"en": "Pending", "ar": "معلق"},
    "dispensed": {"en": "Dispensed", "ar": "تم الصرف"},
    "rejected": {"en": "Rejected", "ar": "مرفوض"},
    "dispense": {"en": "Dispense", "ar": "صرف"},
    "reject": {"en": "Reject", "ar": "رفض"},
    "no_pending_orders": {"en": "No pending orders", "ar": "لا توجد طلبات معلقة"},
    "my_recent_orders": {"en": "Recent orders you placed", "ar": "أحدث الطلبات التي أرسلتها"},

    # Call Center
    "log_call": {"en": "Log a call", "ar": "تسجيل مكالمة"},
    "caller_name": {"en": "Caller name", "ar": "اسم المتصل"},
    "phone": {"en": "Phone", "ar": "رقم الهاتف"},
    "purpose": {"en": "Purpose", "ar": "الغرض من المكالمة"},
    "book_appointment": {"en": "Book appointment", "ar": "حجز موعد"},
    "follow_up": {"en": "Follow-up", "ar": "متابعة"},
    "complaint": {"en": "Complaint", "ar": "شكوى"},
    "general_inquiry": {"en": "General inquiry", "ar": "استفسار عام"},
    "save_call": {"en": "Save call log", "ar": "حفظ سجل المكالمة"},
    "recent_calls": {"en": "Recent calls", "ar": "أحدث المكالمات"},

    # PR / Complaints
    "new_complaint": {"en": "Log a complaint", "ar": "تسجيل شكوى"},
    "description": {"en": "Description", "ar": "الوصف"},
    "submit_complaint": {"en": "Submit", "ar": "إرسال"},
    "open": {"en": "Open", "ar": "مفتوحة"},
    "resolved": {"en": "Resolved", "ar": "تم الحل"},
    "resolve": {"en": "Mark resolved", "ar": "وضع علامة تم الحل"},
    "all_complaints": {"en": "All complaints", "ar": "جميع الشكاوى"},

    # Generic
    "no_data": {"en": "No data yet", "ar": "لا توجد بيانات بعد"},
    "language": {"en": "Language", "ar": "اللغة"},
    "prototype_note": {
        "en": "Prototype demo — data is stored in a local SQLite file, not production-ready.",
        "ar": "نموذج تجريبي - البيانات مخزنة في ملف SQLite محلي، وليست جاهزة للتشغيل الفعلي.",
    },
}


def t(key: str, lang: str) -> str:
    """Translate a key into the given language, falling back to English then the raw key."""
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang, entry.get("en", key))
