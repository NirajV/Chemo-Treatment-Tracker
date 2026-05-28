Chemo Calendar - Full Stack Application Development Plan
Executive Summary
I will build a comprehensive Chemotherapy Calendar Management System with bidirectional communication between providers and patients. This is a sophisticated healthcare application requiring careful architecture, security, and user experience design.

PHASE 1: APPLICATION ARCHITECTURE & PLANNING
Complete Application Plan
CopyCHEMO CALENDAR APPLICATION
├── FRONTEND LAYER
│   ├── Web Application (React)
│   │   ├── Provider Dashboard
│   │   ├── Patient Management
│   │   ├── Regimen Management
│   │   ├── Calendar Visualization
│   │   └── Profile & Settings
│   └── Mobile Application (React Native)
│       ├── Patient App
│       ├── Appointment Management
│       ├── Medication Tracking
│       └── Side Effect Reporting
├── BACKEND LAYER
│   ├── API Server (Node.js/Express)
│   ├── Authentication & Authorization
│   ├── Business Logic
│   └── Real-time Communication (WebSockets)
├── DATABASE LAYER
│   └── Supabase (PostgreSQL)
│       ├── Users & Authentication
│       ├── Patients
│       ├── Providers
│       ├── Regimens
│       ├── Calendars
│       ├── Events
│       ├── Side Effects
│       └── Communications
└── INFRASTRUCTURE
    ├── Docker (Local & Production)
    ├── Environment Configuration
    └── Deployment Scripts
Key Features by Module
ModuleFeaturesPriorityAuthenticationUser registration, Login, Password reset, Role-based accessP0Regimen ManagementCreate/Edit/Copy regimens, Cycle management, Drug databaseP0Calendar CreationPatient info input, Regimen selection, Start date, Cycle selectionP0Calendar VisualizationMonth/Week/List views, Color-coded drugs, Event detailsP0Event ManagementAdd/Edit/Delete events, Drag-drop rescheduling, Bulk date adjustmentP1Patient ManagementAdd patients, View profiles, Track treatment progress, Side effectsP0Provider TabManage providers, Role assignment, Specialty trackingP1Mobile AppAppointments, Medications, Side effect reporting, NotificationsP1CommunicationsMessages, Notifications (Email, SMS, Push), Reschedule requestsP2ReportingTreatment summary, Side effect history, Progress trackingP2

SESSION 1: DATABASE DESIGN & SUPABASE SETUP
Step 1: Supabase Installation & Configuration
Prompt for Session 1:

"Set up Supabase free tier project with complete authentication, user roles, and initial database schema for Chemo Calendar. Include environment configuration files for local development."

Instructions:

Create Supabase Account
bashCopy# Visit https://supabase.com
# Sign up with email or GitHub
# Create a new project:
# - Project name: chemo-calendar
# - Database password: [Strong password]
# - Region: Choose closest to you

Get Connection Credentials

In Supabase dashboard → Settings → Database
Copy: Connection String (PostgreSQL)
Note: Project URL, Anon Key, Service Role Key


Database Schema

I'll provide the SQL schema for database setup.

Create .env.local file
envCopyVITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key


Step 2: Database Schema Creation
sqlCopy-- Users table (handled by Supabase Auth)
-- Add custom user profiles
CREATE TABLE public.user_profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name varchar(255),
  last_name varchar(255),
  email varchar(255),
  phone varchar(20),
  role varchar(50), -- 'organizer', 'doctor', 'nurse', 'patient', 'staff'
  specialty varchar(255), -- for doctors
  organization varchar(255),
  address text,
  language varchar(10) DEFAULT 'en-US',
  country varchar(2),
  timezone varchar(50),
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

-- Patients table
CREATE TABLE public.patients (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  mrn varchar(50) UNIQUE,
  first_name varchar(255) NOT NULL,
  last_name varchar(255) NOT NULL,
  date_of_birth date,
  gender varchar(20),
  phone varchar(20),
  email varchar(255),
  address text,
  assigned_provider_id uuid REFERENCES user_profiles(id),
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

-- Regimens table
CREATE TABLE public.regimens (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(500) NOT NULL,
  disease_type varchar(255),
  description text,
  owner_id uuid REFERENCES user_profiles(id),
  is_standard boolean DEFAULT false,
  is_shared boolean DEFAULT false,
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

-- Cycles within regimens
CREATE TABLE public.cycles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  regimen_id uuid REFERENCES public.regimens(id) ON DELETE CASCADE,
  cycle_number integer,
  cycle_name varchar(255),
  cycle_length_days integer,
  notes text,
  created_at timestamp DEFAULT now()
);

-- Drugs in cycles
CREATE TABLE public.cycle_drugs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  cycle_id uuid REFERENCES public.cycles(id) ON DELETE CASCADE,
  drug_name varchar(255) NOT NULL,
  generic_name varchar(255),
  brand_names text,
  dose varchar(100),
  days varchar(50), -- "1,4,8,11" or "1-21" format
  route varchar(50), -- 'Intravenous', 'Oral', 'Subcutaneous', etc.
  location varchar(255), -- 'Inpatient Admission', 'Facility Administered'
  infusion_duration_min integer,
  observation_time_min integer,
  dose_cap varchar(100),
  warnings text,
  department_name varchar(255),
  office_address text,
  office_location_hint text,
  print_name varchar(20),
  calendar_color varchar(7),
  created_at timestamp DEFAULT now()
);

-- Patient treatment calendars
CREATE TABLE public.treatment_calendars (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id uuid REFERENCES public.patients(id) ON DELETE CASCADE,
  regimen_id uuid REFERENCES public.regimens(id),
  provider_id uuid REFERENCES user_profiles(id),
  start_date date NOT NULL,
  custom_name varchar(255),
  status varchar(50) DEFAULT 'active', -- 'active', 'completed', 'paused'
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

-- Calendar events
CREATE TABLE public.calendar_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  calendar_id uuid REFERENCES public.treatment_calendars(id) ON DELETE CASCADE,
  event_type varchar(50), -- 'drug_administration', 'clinic_visit', 'lab_draw', 'radiology', 'custom'
  event_date date NOT NULL,
  drug_id uuid REFERENCES public.cycle_drugs(id),
  cycle_number integer,
  day_in_cycle integer,
  custom_event_name varchar(255),
  time time,
  description text,
  color varchar(7),
  created_at timestamp DEFAULT now(),
  updated_at timestamp DEFAULT now()
);

-- Side effects tracking
CREATE TABLE public.side_effects (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id uuid REFERENCES public.patients(id) ON DELETE CASCADE,
  calendar_id uuid REFERENCES public.treatment_calendars(id),
  effect_type varchar(255), -- 'Nausea', 'Fatigue', etc.
  category varchar(50), -- 'gastrointestinal', 'systemic', 'dermatological', etc.
  severity varchar(20), -- 'mild', 'moderate', 'severe'
  date_reported date NOT NULL,
  trend varchar(20), -- 'improving', 'stable', 'worsening'
  frequency varchar(50),
  notes text,
  reported_at timestamp DEFAULT now()
);

-- Messages between provider and patient
CREATE TABLE public.messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  sender_id uuid REFERENCES user_profiles(id),
  recipient_id uuid REFERENCES user_profiles(id),
  subject varchar(255),
  message text NOT NULL,
  is_read boolean DEFAULT false,
  read_at timestamp,
  created_at timestamp DEFAULT now()
);

-- Notification preferences
CREATE TABLE public.notification_preferences (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES user_profiles(id) ON DELETE CASCADE,
  email_enabled boolean DEFAULT true,
  sms_enabled boolean DEFAULT true,
  push_enabled boolean DEFAULT true,
  phone_enabled boolean DEFAULT false,
  mail_enabled boolean DEFAULT false,
  updated_at timestamp DEFAULT now()
);

-- Create indexes for performance
CREATE INDEX idx_patients_provider ON public.patients(assigned_provider_id);
CREATE INDEX idx_regimens_owner ON public.regimens(owner_id);
CREATE INDEX idx_calendars_patient ON public.treatment_calendars(patient_id);
CREATE INDEX idx_events_calendar ON public.calendar_events(calendar_id);
CREATE INDEX idx_sideeffects_patient ON public.side_effects(patient_id);

SESSION 2: FRONTEND SETUP - REACT + VITE
Prompt for Session 2:

"Create a professional React + Vite frontend application structure for Chemo Calendar with TypeScript, Tailwind CSS, and Supabase integration. Include reusable components, state management, and routing."

I'm ready to proceed to the next session. Would you like me to:

Continue with Session 2 - Frontend setup and component architecture
Adjust the database schema - Any modifications needed?
Clarify any requirements - Before we start implementation

What would you like me to focus on next?
Once you confirm, I'll provide:

Complete Vite + React setup guide
Component structure
State management solution (Zustand/Redux)
API client setup
Live preview of the application building in real-time
Add to Conversation2735