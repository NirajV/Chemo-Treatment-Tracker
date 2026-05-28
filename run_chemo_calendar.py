#!/usr/bin/env python3
"""
Chemo Treatment Calendar - Multi-Agent Pipeline Runner
Generates complete production-ready healthcare application
"""

import os
import sys
import json
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("❌ anthropic module not found")
    print("Install with: pip install anthropic")
    sys.exit(1)

from multi_agent_system import MultiAgentOrchestrator


CHEMO_PROJECT_DESCRIPTION = """
CHEMO TREATMENT CALENDAR APPLICATION
====================================

EXECUTIVE SUMMARY
Build a comprehensive Chemotherapy Calendar Management System with bidirectional communication between healthcare providers and patients. This is a sophisticated healthcare application requiring HIPAA compliance, secure PHI handling, and careful architecture.

SYSTEM ARCHITECTURE
===================
├── FRONTEND LAYER
│   ├── Web Application (React + TypeScript + Tailwind CSS)
│   │   ├── Provider Dashboard (manage patients, regimens, calendars)
│   │   ├── Patient Management (view assigned patients, track progress)
│   │   ├── Regimen Management (create/edit/copy regimens with drugs)
│   │   ├── Calendar Visualization (month/week/list views)
│   │   ├── Event Management (add/edit/delete treatment events)
│   │   └── Profile & Settings (user prefs, notifications)
│   └── Mobile Application (React Native - Phase 2)
│       ├── Patient App (appointments, medications, side effects)
│       ├── Appointment Management
│       ├── Medication Tracking
│       └── Side Effect Reporting
│
├── BACKEND LAYER
│   ├── API Server (Node.js + Express + TypeScript)
│   ├── Authentication & Authorization (JWT, Supabase Auth)
│   ├── Business Logic (regimen engine, calendar generation)
│   ├── Real-time Communication (WebSockets - Phase 2)
│   └── HIPAA Audit Logging
│
├── DATABASE LAYER
│   └── Supabase (PostgreSQL with RLS)
│       ├── Users & Authentication (auth.users)
│       ├── User Profiles (doctors, nurses, patients, staff)
│       ├── Patients (MRN, demographics)
│       ├── Regimens (treatment templates)
│       ├── Cycles (treatment cycles within regimens)
│       ├── Cycle Drugs (individual drugs in cycles)
│       ├── Treatment Calendars (patient treatment schedule)
│       ├── Calendar Events (individual treatment events)
│       ├── Side Effects (patient-reported side effects)
│       ├── Messages (provider-patient communication)
│       └── Notification Preferences
│
└── INFRASTRUCTURE
    ├── Docker (local development + production)
    ├── Docker Compose (Supabase + backend + frontend)
    ├── Environment Configuration (.env files)
    └── CI/CD Pipeline (GitHub Actions)


DATABASE SCHEMA
===============
1. user_profiles (connected to auth.users)
   - id (uuid, PK, FK to auth.users)
   - first_name, last_name, email, phone
   - role ('organizer', 'doctor', 'nurse', 'patient', 'staff')
   - specialty (for doctors), organization, address
   - language, country, timezone
   - created_at, updated_at

2. patients
   - id (uuid, PK)
   - mrn (varchar, UNIQUE)
   - first_name, last_name, date_of_birth, gender
   - phone, email, address
   - assigned_provider_id (FK to user_profiles)
   - created_at, updated_at

3. regimens
   - id (uuid, PK)
   - name, disease_type, description
   - owner_id (FK to user_profiles)
   - is_standard (bool), is_shared (bool)
   - created_at, updated_at

4. cycles
   - id (uuid, PK)
   - regimen_id (FK to regimens, CASCADE)
   - cycle_number, cycle_name
   - cycle_length_days, notes
   - created_at

5. cycle_drugs
   - id (uuid, PK)
   - cycle_id (FK to cycles, CASCADE)
   - drug_name, generic_name, brand_names
   - dose, days (format: "1,4,8,11" or "1-21")
   - route ('Intravenous', 'Oral', 'Subcutaneous', etc.)
   - location, infusion_duration_min, observation_time_min
   - dose_cap, warnings, department_name, office_address
   - calendar_color (hex color)
   - created_at

6. treatment_calendars
   - id (uuid, PK)
   - patient_id (FK to patients, CASCADE)
   - regimen_id (FK to regimens)
   - provider_id (FK to user_profiles)
   - start_date (date)
   - custom_name, status ('active', 'completed', 'paused')
   - created_at, updated_at

7. calendar_events
   - id (uuid, PK)
   - calendar_id (FK to treatment_calendars, CASCADE)
   - event_type ('drug_administration', 'clinic_visit', 'lab_draw', 'radiology', 'custom')
   - event_date (date), time (optional)
   - drug_id (FK to cycle_drugs)
   - cycle_number, day_in_cycle
   - custom_event_name, description
   - color (hex), created_at, updated_at

8. side_effects
   - id (uuid, PK)
   - patient_id (FK to patients, CASCADE)
   - calendar_id (FK to treatment_calendars)
   - effect_type, category ('gastrointestinal', 'systemic', 'dermatological', etc.)
   - severity ('mild', 'moderate', 'severe')
   - date_reported, trend, frequency, notes
   - reported_at (timestamp)

9. messages
   - id (uuid, PK)
   - sender_id (FK to user_profiles)
   - recipient_id (FK to user_profiles)
   - subject, message (text)
   - is_read (bool), read_at (optional)
   - created_at

10. notification_preferences
    - id (uuid, PK)
    - user_id (FK to user_profiles, CASCADE)
    - email_enabled, sms_enabled, push_enabled
    - phone_enabled, mail_enabled
    - updated_at


FEATURE MODULES BY PRIORITY
===========================

P0 (CRITICAL - MVP):
  - Authentication: User registration, login, password reset, role-based access
  - Regimen Management: Create/edit/copy regimens, cycle management, drug database
  - Calendar Creation: Patient info input, regimen selection, start date, cycle selection
  - Calendar Visualization: Month/week/list views, color-coded drugs, event details
  - Patient Management: Add patients, view profiles, track treatment progress

P1 (HIGH):
  - Event Management: Add/edit/delete events, drag-drop rescheduling, bulk date adjustment
  - Provider Tab: Manage providers, role assignment, specialty tracking
  - Mobile App (React Native): Appointments, medications, side effect reporting, notifications
  - Advanced Filtering: Filter calendars by drug, date range, patient, etc.

P2 (MEDIUM - Phase 2):
  - Communications: Messages, notifications (email, SMS, push), reschedule requests
  - Reporting: Treatment summary, side effect history, progress tracking
  - Real-time Collaboration: WebSocket updates for provider-patient interactions
  - Advanced Analytics: Treatment outcome tracking, side effect trends


TECHNICAL REQUIREMENTS
=======================

Frontend Stack:
  - Framework: React 18+
  - Language: TypeScript (strict mode)
  - Build: Vite
  - Styling: Tailwind CSS v3+
  - UI Components: React Query, React Hook Form, Headless UI (or similar)
  - State Management: Zustand or React Context
  - Routing: React Router v6+
  - HTTP Client: fetch or axios with interceptors
  - Date Handling: Day.js or date-fns
  - Charts (optional): Recharts for side effect trends

Backend Stack:
  - Runtime: Node.js 18+
  - Framework: Express.js (or Fastify)
  - Language: TypeScript
  - Database Client: @supabase/supabase-js
  - Authentication: Supabase Auth (JWT)
  - Validation: Zod or Joi
  - Logging: Winston or Pino (structured logging, NO PHI)
  - Error Handling: Express error middleware

Database:
  - PostgreSQL via Supabase
  - Row-Level Security (RLS) policies for all tables
  - Connection pooling (Supabase built-in)
  - Prepared statements for SQL injection prevention
  - Audit triggers on sensitive tables

Security & Compliance:
  - HTTPS/TLS only (enforced in production)
  - JWT token-based authentication (no session cookies)
  - Supabase RLS for authorization at DB level
  - Input validation and sanitization
  - CSRF protection (SameSite cookies)
  - XSS prevention (Content Security Policy)
  - SQL injection prevention (parameterized queries)
  - HIPAA audit logging (who accessed what PHI, when)
  - Environment variables for all secrets (never committed)
  - Password hashing: bcrypt or Argon2
  - CORS configured properly

Deployment:
  - Docker Compose for local development
  - Docker containers for all services
  - GitHub Actions for CI/CD
  - Environment-specific .env files
  - Database migrations (versioned SQL files)
  - Health check endpoints

Performance Requirements:
  - API response time: < 200ms for 95th percentile
  - Calendar rendering: < 1s for 100+ events
  - Support 1000+ concurrent users
  - Database query optimization (indexes on foreign keys)
  - Pagination for large data sets (events, messages)
  - Caching strategy (browser cache, optional Redis)

Testing:
  - Unit tests: Jest (80%+ coverage target)
  - Integration tests: Supertest for API
  - E2E tests: Cypress or Playwright
  - Test database: Isolated Supabase instance or Docker


HIPAA & HEALTHCARE COMPLIANCE
==============================
- Never log patient names, MRNs, SSNs, or dates of birth
- Audit trail: Log who accessed/modified patient records (without PHI details)
- Access Control: RLS policies enforce role-based access
- Data Encryption: Use TLS in transit, consider encryption at rest
- Data Retention: Plan for secure deletion of archived records
- Backup Strategy: Supabase automated backups, tested recovery procedures
- Incident Response: Logging mechanism for security incidents
- User Documentation: Privacy notices, data handling procedures


DEPLOYMENT ARCHITECTURE
=======================
Docker Compose services:
  - postgres (Supabase backend)
  - supabase (auth, API, real-time)
  - backend (Express API server)
  - frontend (Vite dev server)
  - redis (optional, for caching/sessions)

Environments:
  - Local development (Docker Compose)
  - Staging (Supabase free tier + Node.js on PaaS)
  - Production (Supabase + Node.js on PaaS or container service)


DELIVERABLES
=============
1. Complete React/Vite frontend with all P0 modules
2. Complete Node.js/Express API backend with all endpoints
3. Database schema (SQL migrations for all 9 tables)
4. Supabase RLS policies for access control
5. Docker Compose for local development
6. API documentation (OpenAPI/Swagger format)
7. Setup guide and deployment instructions
8. Test suite (unit + integration tests)
9. GitHub Actions CI/CD pipeline
10. .env.example with all required variables


ACCEPTANCE CRITERIA
===================
- ✓ All P0 features implemented and functional
- ✓ Database deployed to Supabase with RLS policies
- ✓ API passes all tests (80%+ coverage)
- ✓ Frontend passes ESLint, TypeScript strict mode
- ✓ HIPAA security best practices implemented
- ✓ Supports 1000+ users with sub-200ms response times
- ✓ Docker Compose runs complete system locally
- ✓ Authentication and role-based access working end-to-end
- ✓ Documentation complete and clear


CONSTRAINTS & ASSUMPTIONS
==========================
- Timeline: 2-3 weeks for full development
- Team: Can be done by 1-2 full-stack developers
- Budget: Use free tier services where possible (Supabase free tier, GitHub free tier)
- Third-party services: Supabase (auth, database), optional Stripe (Phase 2 payments)
- No requirement for mobile app in Phase 1 (web-first)
- Assumes developers familiar with React, Node.js, and PostgreSQL
"""


def print_banner():
    """Print welcome banner"""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║        CHEMO TREATMENT CALENDAR - MULTI-AGENT PIPELINE                ║
║    Autonomous Healthcare Application Development Pipeline             ║
║    Task Manager → Developer → Tester → Deployer                       ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)


def run_pipeline():
    """Run the complete pipeline for Chemo Calendar"""

    print_banner()

    # Verify API key is set
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    print("\n✅ API Key found")
    print("🏥 Project: Chemo Treatment Calendar")
    print("📊 Starting multi-agent pipeline execution...\n")

    # Create orchestrator
    orchestrator = MultiAgentOrchestrator(
        project_name="Chemo Treatment Calendar",
        project_description=CHEMO_PROJECT_DESCRIPTION
    )

    # Run the pipeline
    results = orchestrator.run_pipeline()

    # Save results
    output_file = orchestrator.save_results("chemo_pipeline_results.json")
    print(f"\n💾 Results saved to: {output_file}")

    # Print summary
    print("\n" + "=" * 80)
    print("📋 FINAL PIPELINE SUMMARY")
    print("=" * 80)
    summary = orchestrator.get_summary()
    print(json.dumps(summary, indent=2))

    return results, output_file


if __name__ == "__main__":
    try:
        results, output_file = run_pipeline()
        print("\n✅ Pipeline execution completed successfully!")
        print(f"📁 Check {output_file} for full agent outputs")
    except Exception as e:
        print(f"\n❌ Pipeline failed: {str(e)}")
        sys.exit(1)
