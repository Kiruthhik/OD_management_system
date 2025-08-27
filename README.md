# OD Management System – README

> A Django-based system to digitize the **On Duty (OD)** request & approval workflow for a college, replacing the manual letter-and-signature process.

---

## Table of Contents

1. [Overview](#overview)
2. [Current Manual Process](#current-manual-process)
3. [Goals & Scope](#goals--scope)
4. [Key Features](#key-features)
5. [User Roles & Permissions](#user-roles--permissions)
6. [System Architecture](#system-architecture)
7. [Data Model](#data-model)

   * [Entities](#entities)
   * [ER Diagram](#er-diagram)
8. [Workflow](#workflow)

   * [End-to-End Flow Diagram](#end-to-end-flow-diagram)
   * [Approval Logic](#approval-logic)
9. [Installation & Setup](#installation--setup)
10. [Configuration](#configuration)
11. [Data Import (Excel Uploads)](#data-import-excel-uploads)
12. [Running the App](#running-the-app)
13. [Directory & Template References](#directory--template-references)
14. [URLs & Views (Reference)](#urls--views-reference)
15. [Security Notes](#security-notes)
16. [Testing Ideas](#testing-ideas)
17. [Known Limitations](#known-limitations)
18. [Future Improvements](#future-improvements)
19. [License](#license)

---

## Overview

**OD Management System** digitizes the process for students to request On Duty (OD) permissions and for faculty to approve or reject them. It models the real-world approval chain — **Class Incharge → Academic Head → HOD** — and supports single or team-based ODs, role-based dashboards, and evidence file uploads.

> Tech stack: **Django** (backend + server-rendered **Django Templates**), Django Auth & Groups, Django ORM.

---

## Current Manual Process

1. Student writes a physical letter stating OD reason.
2. Attaches evidence (if any).
3. Collects signatures from **Class Incharge → Academic Head → HOD**.
4. Shares approved OD letter with **all subject teachers** for that day so they can mark attendance.

---

## Goals & Scope

* Replace paper workflow with a digital system.
* Provide **role-aware dashboards** to view, approve, or reject OD requests.
* Track OD status (pending / approved / rejected) and show history to students.
* Make it easy to configure classes, students, and faculty via **bulk imports (Excel)**.
* **Scope:** currently designed to satisfy the needs of one college/department; can be extended later.

---

## Key Features

* Student portal to **apply for OD**, including:

  * Event name/type, venue, date range, evidence upload.
  * **Team ODs** (add teammates).
* Faculty portals for:

  * **Class Incharge** approval.
  * **Academic Head** approval.
  * **HOD** final approval.
* **Dashboards**:

  * Student: pending / approved / rejected ODs.
  * Faculty: requests awaiting action; students on OD in their classes.
  * HOD: filter OD requests by date and see pending/processed breakdown.
* Evidence uploads stored under a configured media directory.

---

## User Roles & Permissions

* **Student:** login, apply for OD, view status.
* **Faculty (Teaching / Class Incharge):** login, review & approve/reject OD for their students.
* **Academic Head (per year):** review & approve/reject after Class Incharge.
* **HOD:** final approver.

> Authentication: Django `User` + **Groups** (e.g., `student`, `faculty`). Authorization is enforced by role-checks in views and via faculty type.

---

## System Architecture

* **Django MVC** (MTV):

  * **Models:** `Student`, `Faculty`, `Class`, `student_OD`, `faculty_OD`.
  * **Views:** Student dashboard & apply flow; Faculty dashboard & approval actions; HOD dashboard & filters.
  * **Templates:** Server-rendered HTML for each page.
* **File Storage:** Evidence files under `MEDIA_ROOT/proofs/`.
* **Bulk Data Import:** Django management commands to seed Users/Students/Faculty and map Classes.

---

## Data Model

### Entities

* **Student**: linked 1‑to‑1 with `User`; has roll number, department, section, year.
* **Faculty**: linked 1‑to‑1 with `User`; has department, a unique `faculty_code`, and `faculty_type` (HOD / Academic Head I/II/III / Teaching / DC).
* **Class**: has department, year, section; **M2M** with Students and Faculties; one **class\_incharge** (faculty) associated.
* **student\_OD**: OD request; fields: event name/type, venue, `proof` (file), `start_date`, `end_date`, `isTeam`, `teammates` (M2M Students), approver reference (`class_incharge`), boolean flags for each approval stage & rejection.
* **faculty\_OD**: minimal model for faculty OD requests (description field).

### ER Diagram

```mermaid
erDiagram
    USER ||--o| STUDENT : has
    USER ||--o| FACULTY : has

    CLASS ||--o{ STUDENT : contains
    CLASS ||--o{ FACULTY : handled_by
    CLASS ||--|| FACULTY : class_incharge

    STUDENT_OD }|--|| STUDENT : applicant
    STUDENT_OD }|--|| CLASS   : for_class
    STUDENT_OD }o--o{ STUDENT : teammates
    STUDENT_OD }|--|| FACULTY : approver_class_incharge

    FACULTY_OD }|--|| FACULTY : applicant

    %% Fields (selected)
    STUDENT {
      int id PK
      int user_id FK
      string roll_number
      string department
      string section
      int year
    }

    FACULTY {
      int id PK
      int user_id FK
      string department
      string faculty_code UNIQUE
      enum faculty_type
    }

    CLASS {
      int id PK
      string department
      string year
      string section
      int class_incharge_id FK
    }

    STUDENT_OD {
      int id PK
      int student_id FK
      int class_id FK
      string eventName
      string eventType
      string venue
      file proof
      date start_date
      date end_date
      bool isTeam
      bool class_incharge_approval
      bool academic_head_approval
      bool hod_approval
      bool OD_rejection
    }

    FACULTY_OD {
      int id PK
      int faculty_id FK
      string description
    }
```

> **Note:** `CLASS.class_incharge` is modeled as a `OneToOne` to `FACULTY` (meaning one faculty can be in‑charge of **one** class). If a faculty can be in‑charge of multiple classes, convert this to a `ForeignKey`.

---

## Workflow

### End-to-End Flow Diagram

```mermaid
flowchart TD
    A[Student logs in] --> B[Apply OD: enter event\n dates, venue, upload proof\n(optional teammates)]
    B --> C{Class Incharge\n approves?}
    C -- No --> R1[Rejected]
    C -- Yes --> D{Academic Head\n approves?}
    D -- No --> R2[Rejected]
    D -- Yes --> E{HOD\n approves?}
    E -- No --> R3[Rejected]
    E -- Yes --> F[OD Approved]
    F --> G[Faculty dashboards show\n students on OD for the dates]
    R1 --> H[Student sees status]
    R2 --> H
    R3 --> H
```

### Approval Logic

* **Sequential approvals:** Class Incharge → Academic Head (I/II/III per year) → HOD.
* **Any stage can reject**; rejection marks the request as closed.
* **Final status** is **approved** only when **HOD** approves.
* Faculty dashboards highlight **students with approved ODs** in each class for attendance decisions on those dates.

---

## Installation & Setup

### Prerequisites

* Python 3.10+
* pip / venv
* Django (version as per `requirements.txt` or install latest 4.x)

### Steps

```bash
# 1) Clone the repository
git clone <your-repo-url>
cd od-management-system

# 2) Create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt   # or: pip install django openpyxl

# 4) Create DB tables
python manage.py migrate

# 5) Create superuser
python manage.py createsuperuser

# 6) Create groups (one-time)
python manage.py shell <<'PY'
from django.contrib.auth.models import Group
Group.objects.get_or_create(name='student')
Group.objects.get_or_create(name='faculty')
print('Groups ensured: student, faculty')
PY

# 7) Configure media (see Configuration) and run server
python manage.py runserver
```

---

## Configuration

Add the following to `settings.py` (or `.env` with `django-environ`) to support evidence uploads:

```python
# settings.py (snippets)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# In urls.py (project-level)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # ... your urls
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Ensure your web server (if deploying) serves `/media/` safely.

---

## Data Import (Excel Uploads)

The project includes **management commands** to bulk-import Faculty, Students, and map Class–Faculty relationships from Excel files.

> **Important:** The sample scripts have **hard-coded Windows file paths**. Update the `file_path` variables or refactor to accept a command-line `--file` argument.

### 1) Faculty Import

```bash
python manage.py upload_faculty_data
```

**Expected columns (from the active sheet):**

* Faculty Code
* Full Name ("First Last")
* Faculty Type (e.g., "HOD", "Academic Head I/II/III", other → Teaching)

### 2) Student Import

```bash
python manage.py upload-student-data
```

**Expected columns:**

* Student Name
* Roll Number
* Section

### 3) Class ↔ Faculty Mapping

```bash
python manage.py upload-class-faculty-data
```

**Expected columns:**

* Faculty Code
* Section
* Year

> After imports, ensure users are placed in the correct **Groups** (e.g., students in `student`, staff in `faculty`) so they can access the appropriate portals.

---

## Running the App

* **Student Login:** students authenticate using their roll numbers (as usernames) if imported that way.
* **Student Home:** shows **Pending / Approved / Rejected** ODs and links to details.
* **Apply OD:** submit event details, date range, upload evidence, add teammates.
* **Faculty Login:** staff authenticate using their faculty codes.
* **Faculty Home:** shows OD requests awaiting your action (based on role) and lists of students on OD in classes you handle.
* **HOD Home:** a dedicated dashboard to filter by date, and view pending vs processed ODs.

---

## Directory & Template References

**Templates used (server-rendered):**

* `student_login.html`, `student_home.html`, `apply_OD.html`, `student_OD.html`
* `faculty_login.html`, `faculty_home.html`
* `hod-home.html`, `od_details.html`

Organize them under your app templates directories, e.g., `student/templates/` and `faculty/templates/`.

---

## URLs & Views (Reference)



```python
# student/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='student_login'),
    path('home/', views.home, name='student_home'),
    path('apply/', views.apply_OD, name='apply_OD'),
    path('od/<int:id>/', views.OD_status, name='OD_status'),
]

# faculty/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='faculty_login'),
    path('home/', views.home, name='faculty_home'),
    path('hod/', views.hod_home, name='hod_home'),
    path('od/<int:id>/', views.od_details, name='od_details'),
    path('od/<int:od_id>/<str:action>/', views.process_od, name='process_od'), # action in {approve, reject}
]
```

---

## Security Notes

* Ensure all role-based views **check group membership** and/or **faculty type**.
* Restrict OD objects so that:

  * Students can only see their own ODs (or the ones they are teammates in).
  * Approvers only see ODs relevant to their classes/year/department.
* Validate date ranges (start ≤ end) and file types/size for proofs.
* Use CSRF protection on all POST forms (Django default).

---

## Testing Ideas

* **Unit tests** for: model constraints, approval transitions.
* **Integration tests** for: full request → approval → visibility in dashboards.
* **Edge cases:** overlapping ODs, team ODs where teammate drops, invalid date ranges, missing evidence policy.

---

## Known Limitations

* `Class.class_incharge` is `OneToOne` with `Faculty` — one faculty can be in-charge of **only one** class. Change to `ForeignKey` if needed.
* Academic Head is selected by **faculty type**, not dynamically tied to **Class.year**; add a mapping if multiple academic heads exist per year/department.
* Approval state is tracked by **boolean flags**; a more robust **state machine** (single `status` field + state transitions + audit trail) can improve maintainability.
* Notifications (email/SMS) to subject teachers are not included by default; the current approach relies on dashboards.

---

## Future Improvements

* Replace boolean approvals with a **finite-state machine** (e.g., `status in {PENDING_CI, PENDING_AH, PENDING_HOD, APPROVED, REJECTED}`) and an **audit log** (who approved when, comments).
* **Year-based Academic Head routing** based on class year.
* **Notifications** (email/WhatsApp/SMS) to class incharge, academic head, HOD, and subject teachers.
* **Calendar integration** so approved OD date ranges appear for staff.
* **CSV/Excel export** of OD records.
* **Admin UI** to manage departments/years/sections and map class incharges.
* **Attachments policy** (file type/size restrictions) and virus scanning on uploads.
* **Role-based dashboards** with richer filters (date, department, class).

---

## License

Internal/Academic Project. Add your preferred license (e.g., MIT) if open-sourcing.

---

> *Tip: Keep screenshots (login, dashboards, OD form, approvals) in a `/docs/` folder and reference them here for a complete report-style README.*
