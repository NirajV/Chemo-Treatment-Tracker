# CHEMO CALENDAR - Comprehensive Technical Prompts & Implementation Plan

I've analyzed your requirement document thoroughly. Here's a complete breakdown with detailed technical prompts for each layer and a comprehensive implementation plan.

---

## **PART 1: COMPLETE APPLICATION PLAN OVERVIEW**

### **Architecture Summary**
```
┌─────────────────────────────────────────────────────────┐
│                    CHEMO CALENDAR APP                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  FRONTEND LAYER          BACKEND LAYER    DATABASE      │
│  ├─ React Web App        ├─ Node.js       └─ Supabase   │
│  ├─ React Native Mobile  ├─ Express       PostgreSQL    │
│  └─ Responsive UI        ├─ REST APIs                   │
│                          └─ Real-time Sync              │
│                                                         │
│  DEPLOYMENT: Docker + Docker Compose                    │
│  HOSTING: Local/Cloud (AWS/Heroku/DigitalOcean)        │
└─────────────────────────────────────────────────────────┘
```

### **8 Main Application Components**
1. **Dashboard** - Summary & Quick Actions
2. **Authentication** - Login/Registration/Profile
3. **Regimen Management** - Create/Edit/Manage Chemotherapy Regimens
4. **Calendar System** - Patient-specific treatment schedules
5. **Drug Management** - Drug library & custom drugs
6. **Provider Management** - Staff/Doctor management
7. **Patient Management** - Patient records & side effects
8. **Mobile App** - Patient-facing appointment & medication tracker

---

## **PART 2: DETAILED TECHNICAL PROMPTS BY LAYER**

---

# **SESSION 1: DATABASE DESIGN & SETUP (SUPABASE)**

## **Prompt 1.1: Supabase Installation & Configuration**

```
Create a comprehensive step-by-step guide for setting up Supabase 
for the Chemo Calendar application. Include:

1. Supabase Account Creation
   - Navigate to supabase.com
   - Sign up with email/GitHub
   - Create new project
   - Configure project name, database password, region (closest to target users)

2. Database Schema Design for Chemo Calendar
   - Table: users (id, email, password_hash, full_name, role, created_at)
   - Table: providers (id, user_id, speciality, organization, phone, created_at)
   - Table: patients (id, mrn, first_name, last_name, dob, gender, email, phone, address, created_at)
   - Table: regimens (id, name, disease_type, description, owner_id, is_standard, created_at, updated_at)
   - Table: cycles (id, regimen_id, cycle_number, cycle_length_days, notes, created_at)
   - Table: cycle_drugs (id, cycle_id, drug_id, dose, days, route, location, infusion_duration, observation_time, dose_cap, warnings, created_at)
   - Table: drugs (id, generic_name, brand_names, description, default_route, default_location, color, created_at, is_personal, created_by_id)
   - Table: patient_calendars (id, patient_id, regimen_id, start_date, provider_id, cycle_count, created_at, updated_at)
   - Table: calendar_events (id, calendar_id, event_type, drug_id, dose, route, location, event_date, day_number, cycle_number, custom_name, description, created_at)
   - Table: side_effects_log (id, patient_id, effect_name, severity, date_reported, trend, frequency, notes, category, created_at)
   - Table: notifications (id, patient_id, type, message, status, created_at, read_at)
   - Table: user_settings (id, user_id, language, country, timezone, enforcement_mode, created_at, updated_at)
   - Table: holidays (id, user_id, holiday_name, date, repeat_yearly, created_at)

3. Set Row Level Security (RLS) Policies
   - Users can only view their own data
   - Providers can view their assigned patients
   - Patients can view their own calendar only
   - Admins have full access

4. Enable Real-time Subscriptions
   - Subscribe to calendar_events changes
   - Subscribe to notifications for real-time updates

5. Create Indexes for Performance
   - Index on patient_calendars(patient_id, created_at)
   - Index on calendar_events(calendar_id, event_date)
   - Index on users(email)

6. Export Connection Details
   - Supabase URL
   - Anon Public Key
   - Service Role Secret Key
   - PostgreSQL Connection String

7. Environment Configuration
   - Create .env.local file with these credentials
   - Set up for development environment
```

## **Prompt 1.2: Database Relationships & Constraints**

```
Design and implement the database relationships for Chemo Calendar 
with proper foreign keys and constraints:

RELATIONSHIPS:
- users → providers (one-to-one)
- users → patients (one-to-one)  
- regimens → cycles (one-to-many)
- regimens → users (many-to-one, owner)
- cycles → cycle_drugs (one-to-many)
- drugs ← cycle_drugs (many-to-one)
- patient_calendars → regimens (many-to-one)
- patient_calendars → patients (many-to-one)
- patient_calendars → users/providers (many-to-one)
- calendar_events → patient_calendars (many-to-one)
- side_effects_log → patients (many-to-one)
- notifications → patients (many-to-one)

CONSTRAINTS:
- NOT NULL constraints on required fields
- UNIQUE constraints on email, MRN, regimen names
- CHECK constraints for date validations
- CASCADE DELETE for cleanup

DATA INTEGRITY RULES:
- Patient MRN must be unique
- Email must be unique across users
- Calendar start date must be in the future or today
- Cycle number must be sequential
- Event dates must fall within calculated cycle dates

AUDIT FIELDS (add to all tables):
- created_at (auto-generated)
- updated_at (auto-updated)
- created_by (user_id)
```

---

# **SESSION 2: BACKEND API DESIGN (NODE.JS/EXPRESS)**

## **Prompt 2.1: Express Server Setup & Project Structure**

```
Create a complete Node.js/Express backend for Chemo Calendar application 
with the following structure:

PROJECT STRUCTURE:
```
chemo-calendar-backend/
├── config/
│   ├── database.js          (Supabase connection)
│   ├── environment.js       (Env variables)
│   └── constants.js         (App constants)
├── middleware/
│   ├── auth.js              (JWT authentication)
│   ├── errorHandler.js      (Global error handling)
│   ├── validation.js        (Request validation)
│   └── roleCheck.js         (Role-based access control)
├── controllers/
│   ├── authController.js
│   ├── userController.js
│   ├── patientController.js
│   ├── regimenController.js
│   ├── calendarController.js
│   ├── drugController.js
│   ├── eventController.js
│   └── notificationController.js
├── routes/
│   ├── auth.js
│   ├── users.js
│   ├── patients.js
│   ├── regimens.js
│   ├── calendars.js
│   ├── drugs.js
│   ├── events.js
│   └── notifications.js
├── services/
│   ├── authService.js
│   ├── regimenService.js
│   ├── calendarService.js   (Complex calendar logic)
│   ├── dateCalculationService.js (Days pattern parsing)
│   ├── notificationService.js
│   └── validationService.js
├── utils/
│   ├── logger.js
│   ├── dateUtils.js
│   ├── passwordUtils.js
│   └── tokenUtils.js
├── models/
│   └── schemas.js           (Joi validation schemas)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── .env
├── .env.example
├── package.json
├── server.js                (Entry point)
└── README.md
```

TECH STACK:
- express (Framework)
- supabase (Database)
- jsonwebtoken (JWT auth)
- bcryptjs (Password hashing)
- joi (Data validation)
- dotenv (Environment config)
- cors (Cross-origin requests)
- helmet (Security headers)
- morgan (Logging)
- nodemailer (Email notifications)

SETUP INSTRUCTIONS:
1. Initialize npm project: npm init -y
2. Install dependencies
3. Create .env file with Supabase credentials
4. Create server.js with Express app initialization
5. Setup middleware stack: CORS, helmet, body-parser, logging
6. Initialize Supabase client in config/database.js
7. Create main routes file with all API endpoints
8. Start dev server: npm run dev
```

## **Prompt 2.2: Authentication & Authorization API Endpoints**

```
Design and implement comprehensive authentication endpoints for Chemo Calendar:

ENDPOINTS:

POST /api/auth/register
- Request: { email, password, full_name, role, speciality?, organization? }
- Validation: Email format, password (min 8 chars), required fields
- Response: { user_id, email, access_token, refresh_token }
- Logic:
  * Hash password with bcryptjs
  * Create user record in users table
  * Auto-create provider or patient role record
  * Generate JWT tokens
  * Send verification email (optional for MVP)

POST /api/auth/login
- Request: { email, password }
- Response: { user_id, email, role, access_token, refresh_token }
- Logic:
  * Validate email/password against database
  * Check user status (active/inactive)
  * Generate new JWT tokens
  * Update last_login timestamp
  * Return role-specific data

POST /api/auth/logout
- Request: { refresh_token }
- Response: { success: true }
- Logic:
  * Invalidate refresh token
  * Clear session if applicable

POST /api/auth/refresh-token
- Request: { refresh_token }
- Response: { access_token, refresh_token }
- Logic:
  * Validate refresh token
  * Issue new access token
  * Optionally rotate refresh token

GET /api/auth/me
- Headers: Authorization: Bearer <token>
- Response: { user_id, email, role, full_name, profile_data }
- Logic:
  * Extract user from JWT
  * Return authenticated user data

POST /api/auth/password-reset
- Request: { email }
- Response: { message: "Reset link sent" }
- Logic:
  * Generate reset token
  * Send email with reset link
  * Store reset token in DB with expiry

POST /api/auth/password-reset-confirm
- Request: { reset_token, new_password }
- Response: { success: true }
- Logic:
  * Validate reset token
  * Hash new password
  * Update user password
  * Invalidate reset token

MIDDLEWARE IMPLEMENTATION:

authMiddleware.js:
- Verify JWT token
- Extract user_id from token
- Check token expiry
- Attach user to request object
- Handle expired/invalid tokens

roleCheckMiddleware.js:
- Verify user has required role
- Check role-specific permissions
- Return 403 Forbidden if unauthorized
- Support role hierarchy (Admin > Provider > Patient)

SECURITY MEASURES:
- Use httpOnly cookies for refresh tokens
- JWT stored in memory for access token
- Implement token rotation
- Rate limiting on login endpoint (5 attempts/15 min)
- Password requirements: min 8 chars, uppercase, lowercase, number
- Hash passwords with bcryptjs (salt rounds: 10)
```

## **Prompt 2.3: Patient Management APIs**

```
Create comprehensive patient management endpoints:

ENDPOINTS:

POST /api/patients
- Auth: Provider/Admin only
- Request: {
    first_name, last_name, mrn, gender, dob, phone, email, address,
    emergency_contact_name?, emergency_contact_phone?
  }
- Response: { patient_id, mrn, created_at }
- Validation:
  * MRN must be unique
  * DOB must be valid date
  * Email optional but must be valid if provided
  * Phone format validation

GET /api/patients
- Auth: Provider/Admin
- Query: { page, limit, search?, status? }
- Response: {
    patients: [
      { patient_id, mrn, first_name, last_name, age, gender, 
        email, phone, active_regimen_count, created_at }
    ],
    total_count, page, limit
  }
- Logic:
  * Paginate results (default 20 per page)
  * Search by name or MRN
  * Filter by status (active/inactive)
  * Order by last modified

GET /api/patients/:patient_id
- Auth: Provider (own patients), Admin
- Response: {
    patient_id, mrn, first_name, last_name, dob, gender,
    email, phone, address, emergency_contact_name,
    emergency_contact_phone, active_calendars,
    medical_history, created_at, updated_at
  }

PUT /api/patients/:patient_id
- Auth: Provider (own patient), Admin
- Request: { first_name?, last_name?, phone?, email?, address? }
- Response: { patient_id, updated_at }
- Validation: Same as creation

DELETE /api/patients/:patient_id
- Auth: Admin only
- Response: { success: true }
- Logic: Soft delete (archive) rather than hard delete

GET /api/patients/:patient_id/calendars
- Auth: Provider (own patient), Patient (self), Admin
- Response: {
    calendars: [
      { calendar_id, regimen_name, start_date, status,
        cycles_completed, cycles_remaining, provider_name,
        created_at }
    ]
  }

GET /api/patients/:patient_id/side-effects
- Auth: Patient (self), Provider (own patient), Admin
- Query: { from_date?, to_date?, category? }
- Response: {
    side_effects: [
      { id, effect_name, severity, date_reported, trend,
        frequency, category, notes }
    ],
    total_count
  }

POST /api/patients/:patient_id/side-effects
- Auth: Patient (self)
- Request: {
    effect_name, severity, date_reported, trend,
    frequency, category, notes?
  }
- Response: { id, created_at }
- Logic:
  * Validate against extensiveSideEffects array
  * Auto-set category based on effect_name
  * Timestamp on backend

GET /api/patients/:patient_id/overview
- Auth: Patient (self), Provider (own patient), Admin
- Response: {
    patient_info: { ... },
    active_calendar: { ... },
    upcoming_appointments: [ ... ],
    recent_side_effects: [ ... ],
    treatment_progress: { ... }
  }

VALIDATION RULES:
- First name & last name: 2-50 characters
- MRN: Unique, alphanumeric, 5-20 characters
- DOB: Valid date, must be in past
- Phone: Valid format (E.164 or local format)
- Email: Valid RFC 5322 format
- Address: 5-200 characters (optional)
```

## **Prompt 2.4: Regimen Management APIs**

```
Create comprehensive regimen management endpoints:

ENDPOINTS:

POST /api/regimens
- Auth: Provider/Admin
- Request: {
    name, disease_type, description, is_standard,
    cycles: [
      {
        cycle_number, cycle_length_days, notes,
        drugs: [
          {
            drug_id, dose, days, route, location,
            infusion_duration?, observation_time?,
            dose_cap?, warnings?
          }
        ]
      }
    ]
  }
- Response: { regimen_id, created_at }
- Validation:
  * Name: unique, 3-200 characters
  * Disease type: from predefined list
  * Days format: "1,4,8,11" or "1-21" or "1-4,9-12"
  * At least one cycle required
  * Each cycle must have at least one drug

GET /api/regimens
- Auth: All authenticated users
- Query: { page, limit, search?, disease_type?, show=standard|owned|shared|all }
- Response: {
    regimens: [
      { regimen_id, name, disease_type, owner_name, cycle_count,
        is_standard, created_at }
    ],
    total_count
  }
- Logic:
  * Standard regimens visible to all
  * Owned regimens visible to creator
  * Shared regimens visible to organization
  * Filter by disease type
  * Search by name

GET /api/regimens/:regimen_id
- Auth: Creator, organization members, Admin
- Response: {
    regimen_id, name, disease_type, description, owner_id,
    owner_name, is_standard, created_at, updated_at,
    cycles: [
      {
        cycle_id, cycle_number, cycle_length_days, notes,
        drugs: [
          { cycle_drug_id, drug_id, drug_name, dose, days,
            route, location, infusion_duration, observation_time,
            dose_cap, warnings, color }
        ]
      }
    ]
  }

PUT /api/regimens/:regimen_id
- Auth: Creator, Admin
- Request: { name?, disease_type?, description? }
- Response: { regimen_id, updated_at }
- Validation: Same as creation
- Logic: Don't allow editing if regimen in use

DELETE /api/regimens/:regimen_id
- Auth: Creator, Admin
- Response: { success: true }
- Logic:
  * Check if regimen in use in any patient calendar
  * If in use: prevent deletion or soft delete
  * Return warning if attempting to delete used regimen

POST /api/regimens/:regimen_id/copy
- Auth: All authenticated
- Request: { new_name, new_owner_id? }
- Response: { new_regimen_id, created_at }
- Logic:
  * Deep copy all cycles and drugs
  * Check for duplicates (same name, same drugs, same structure)
  * Prevent duplicate copies
  * Set new owner to requesting user

POST /api/regimens/:regimen_id/cycles
- Auth: Regimen creator, Admin
- Request: {
    cycle_number, cycle_length_days, notes,
    drugs: [ ... ]
  }
- Response: { cycle_id, created_at }

PUT /api/regimens/:regimen_id/cycles/:cycle_id
- Auth: Regimen creator, Admin
- Request: { cycle_length_days?, notes? }
- Response: { cycle_id, updated_at }

POST /api/regimens/:regimen_id/cycles/:cycle_id/drugs
- Auth: Regimen creator, Admin
- Request: { drug_id, dose, days, route, location, ... }
- Response: { cycle_drug_id, created_at }

PUT /api/regimens/:regimen_id/cycles/:cycle_id/drugs/:cycle_drug_id
- Auth: Regimen creator, Admin
- Request: { dose?, days?, route?, location?, ... }
- Response: { cycle_drug_id, updated_at }

DELETE /api/regimens/:regimen_id/cycles/:cycle_id/drugs/:cycle_drug_id
- Auth: Regimen creator, Admin
- Response: { success: true }

VALIDATION SERVICE (dateCalculationService):

Function: parseDays(daysString)
- Input: "1,4,8,11" or "1-21" or "1-4,9-12"
- Output: [1, 4, 8, 11] or [1,2,3...21] or [1,2,3,4,9,10,11,12]
- Error handling for invalid formats

Function: calculateEventDates(startDate, regimen, cycleNumber)
- Input: start date, regimen object, cycle number
- Output: array of event dates for that cycle
- Logic:
  * Calculate cycle start date = startDate + (cycleNumber - 1) * cycle_length
  * For each drug day in cycle: add to cycle start date
```

## **Prompt 2.5: Calendar & Event Management APIs**

```
Create comprehensive calendar management endpoints:

ENDPOINTS:

POST /api/calendars
- Auth: Provider/Admin
- Request: {
    patient_id, regimen_id, start_date,
    cycle_selection: 'all' | 'specific',
    selected_cycles?: [1, 2, 3],  (if cycle_selection == 'specific')
    end_date?  (optional, default = start + regimen duration)
  }
- Response: { calendar_id, patient_id, event_count, created_at }
- Logic:
  * Validate patient exists
  * Validate regimen exists
  * Calculate all events based on regimen + start date
  * Generate calendar_events records
  * Prevent creation if patient already has this regimen active
  * Send notification to patient

GET /api/calendars/:calendar_id
- Auth: Associated patient, provider, admin
- Response: {
    calendar_id, patient_id, patient_name, mrn,
    regimen_id, regimen_name, start_date, end_date,
    provider_id, provider_name, status,
    cycle_count, cycles_completed, treatment_progress,
    last_modified, created_at,
    events: [ ... ]  (optional, controlled by query param)
  }

GET /api/calendars/:calendar_id/events
- Auth: Associated patient, provider, admin
- Query: { from_date, to_date?, cycle?, event_type? }
- Response: {
    events: [
      { event_id, event_date, event_type, drug_name,
        dose, route, location, cycle_number, day_number,
        status }  // status: pending, completed, skipped, rescheduled
    ],
    calendar_meta: { ... }
  }
- Logic:
  * Return events in chronological order
  * Default to next 30 days if no from/to date
  * Paginate if large result set

GET /api/calendars/:calendar_id/events/:event_id
- Auth: Associated patient, provider, admin
- Response: {
    event_id, calendar_id, event_date, event_type,
    drug_id, drug_name, dose, route, location,
    cycle_number, day_number, infusion_duration,
    observation_time, dose_cap, warnings,
    department_name, department_address, department_phone,
    department_hint,
    status, notes, updated_at
  }

PUT /api/calendars/:calendar_id/events/:event_id
- Auth: Provider, Admin
- Request: {
    new_date?, dose?, route?, location?, notes?,
    status?  // completed, skipped, rescheduled
  }
- Response: { event_id, updated_at }
- Logic:
  * Validate new date doesn't conflict
  * Update event_date
  * Create audit log of change
  * Notify patient of rescheduling

DELETE /api/calendars/:calendar_id/events/:event_id
- Auth: Provider, Admin
- Response: { success: true }
- Logic: Soft delete, mark as cancelled

POST /api/calendars/:calendar_id/bulk-adjust
- Auth: Provider, Admin
- Request: {
    from_date, to_date?,
    adjustment: { direction: 'forward' | 'backward', days: number }
  }
- Response: { adjusted_count, affected_events: [ ... ] }
- Logic:
  * Find all events in range
  * Move forward/backward by N days
  * Check for conflicts (holidays, etc.)
  * Return preview before applying

POST /api/calendars/:calendar_id/bulk-adjust/preview
- Auth: Provider, Admin
- Request: Same as bulk-adjust
- Response: Preview of changes without applying

POST /api/calendars/:calendar_id/bulk-adjust/apply
- Auth: Provider, Admin
- Request: Same as bulk-adjust
- Response: { adjusted_count, results }
- Logic: Apply the adjustments

POST /api/calendars/:calendar_id/events
- Auth: Provider, Admin
- Request: {
    event_type: 'drug_administration' | 'clinic_visit' | 'lab_draw' | 'radiology' | 'custom',
    event_date, drug_id?, custom_name?, time?,
    day_pattern?: { days_of_week?: [...], pattern?: 'mwf,1-5' }
  }
- Response: { event_id, events_created_count }
- Logic:
  * Create single event or recurring events
  * Validate dates
  * Handle day pattern for recurring events

PUT /api/calendars/:calendar_id
- Auth: Provider (creator), Admin
- Request: { start_date?, end_date?, status? }
- Response: { calendar_id, updated_at }

DELETE /api/calendars/:calendar_id
- Auth: Provider (creator), Admin
- Response: { success: true }
- Logic: Soft delete, archive calendar

GET /api/patients/:patient_id/calendars
- Auth: Patient (self), Provider, Admin
- Response: {
    calendars: [
      { calendar_id, regimen_name, start_date, status,
        cycles_completed, cycles_total, treatment_progress,
        next_appointment_date, provider_name, created_at }
    ]
  }

POST /api/calendars/:calendar_id/print
- Auth: Associated provider, admin
- Response: PDF stream
- Logic: Generate printable calendar view
```

## **Prompt 2.6: Drug Management APIs**

```
Create drug management endpoints:

ENDPOINTS:

GET /api/drugs
- Auth: All authenticated
- Query: { page, limit, search?, type=system|personal|all }
- Response: {
    drugs: [
      { drug_id, generic_name, brand_names, description,
        default_route, default_location, color,
        is_personal, created_by_name, created_at }
    ],
    total_count
  }

POST /api/drugs
- Auth: Admin only (system drugs)
- Request: {
    generic_name, brand_names[], description,
    default_route, default_location, calendar_color
  }
- Response: { drug_id, created_at }
- Validation:
  * Generic name: unique, required
  * Brand names: array of strings
  * Route: from predefined list
  * Location: from predefined list
  * Color: valid hex color

GET /api/drugs/:drug_id
- Auth: All authenticated
- Response: {
    drug_id, generic_name, brand_names, description,
    default_route, default_location, color,
    usage_count, last_used
  }

POST /api/drug-requests
- Auth: All authenticated
- Request: {
    generic_name, brand_names[], description,
    default_route, default_location, calendar_color,
    justification
  }
- Response: { request_id, status: 'pending', created_at }
- Logic:
  * Create request for admin review
  * Notify admins
  * Track request status
  * Auto-approve if matches existing similar drug

GET /api/drug-requests
- Auth: Admin only
- Query: { status=pending|approved|rejected }
- Response: {
    requests: [
      { request_id, requested_by, generic_name, brand_names,
        justification, status, created_at }
    ]
  }

PUT /api/drug-requests/:request_id
- Auth: Admin only
- Request: { status: 'approved' | 'rejected', notes? }
- Response: { request_id, status, created_drug_id? }
- Logic:
  * If approved: create new system drug
  * If rejected: store rejection reason
  * Notify requester of decision

POST /api/my-drugs
- Auth: All authenticated
- Request: {
    source_drug_id?, generic_name, brand_names[],
    description, default_route, default_location,
    calendar_color
  }
- Response: { drug_id, created_at }
- Logic:
  * Copy from system drug or create new
  * Mark as personal (is_personal=true)
  * Only visible to creating user
  * Cannot be used in shared regimens

GET /api/my-drugs
- Auth: All authenticated
- Query: { page, limit, search? }
- Response: Personal drug list

PUT /api/my-drugs/:drug_id
- Auth: Drug creator
- Request: { generic_name?, brand_names?, default_route?, ... }
- Response: { drug_id, updated_at }

DELETE /api/my-drugs/:drug_id
- Auth: Drug creator
- Response: { success: true }
- Logic: Prevent deletion if used in regimens

VALIDATION:
- Routes: ['Intravenous', 'Subcutaneous', 'Oral', 'Intramuscular', 'Intrathecal', 'Topical', 'Other']
- Locations: ['Facility Administered', 'Inpatient Admission', 'Home Administration']
- Color: Valid hex color (#RRGGBB)
```

## **Prompt 2.7: Notification & Communication APIs**

```
Create notification and messaging endpoints:

ENDPOINTS:

GET /api/notifications
- Auth: Patient (self)
- Query: { page, limit, unread_only=false, from_date?, to_date? }
- Response: {
    notifications: [
      { notification_id, type, message, read_status,
        sender_name, created_at }
    ],
    unread_count
  }

PUT /api/notifications/:notification_id/mark-read
- Auth: Recipient
- Response: { notification_id, read_at }

PUT /api/notifications/mark-all-read
- Auth: Patient
- Response: { marked_count, timestamp }

DELETE /api/notifications/:notification_id
- Auth: Recipient
- Response: { success: true }

POST /api/messages
- Auth: Patient or Provider
- Request: {
    recipient_id, subject, message, attachment_id?
  }
- Response: { message_id, sent_at }
- Logic:
  * Store message in database
  * Create notification for recipient
  * Send notification based on preference

GET /api/messages
- Auth: Sender/Recipient
- Query: { conversation_id?, unread_only?, page, limit }
- Response: {
    messages: [
      { message_id, sender_id, sender_name, recipient_id,
        subject, message, read_status, created_at }
    ]
  }

PUT /api/messages/:message_id/mark-read
- Auth: Recipient
- Response: { message_id, read_at }

GET /api/notification-preferences
- Auth: Patient (self)
- Response: {
    email_enabled, email_count,
    sms_enabled, sms_count,
    push_enabled, push_count,
    phone_enabled, phone_count,
    mail_enabled, mail_count,
    notification_types: {
      appointment_reminder: 'email,sms,push',
      appointment_changed: 'all',
      medication_reminder: 'all',
      side_effect_request: 'email',
      provider_message: 'all'
    }
  }

PUT /api/notification-preferences
- Auth: Patient (self)
- Request: {
    email_enabled?, sms_enabled?, push_enabled?,
    phone_enabled?, mail_enabled?,
    notification_types: { ... }
  }
- Response: { updated_at }
- Logic:
  * Update notification preferences
  * Respect patient preferences on all future notifications

POST /api/notifications/send
- Auth: System/Admin (internal endpoint)
- Request: {
    patient_id, type, title, message, data?,
    channels: ['email', 'sms', 'push', 'phone', 'mail']
  }
- Response: { notification_id, sent_to_channels: [...] }
- Logic:
  * Check patient preferences
  * Send via appropriate channels
  * Log delivery status

NOTIFICATION TYPES:
1. appointment_reminder - Upcoming appointment
2. appointment_changed - Provider rescheduled appointment
3. appointment_cancelled - Appointment cancelled
4. medication_reminder - Medication day approaching
5. side_effect_request - Provider asks about side effects
6. provider_message - New message from provider
7. calendar_update - Calendar updated
8. test_results - Lab results available
```

---

# **SESSION 3: FRONTEND DEVELOPMENT (REACT)**

## **Prompt 3.1: React Project Setup & Component Architecture**

```
Create a comprehensive React application for Chemo Calendar with 
complete project structure:

PROJECT STRUCTURE:
```
chemo-calendar-frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Navigation.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   ├── ErrorBoundary.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Button.jsx
│   │   │   └── Input.jsx
│   │   ├── auth/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── ForgotPasswordPage.jsx
│   │   │   ├── ResetPasswordPage.jsx
│   │   │   └── DisclaimerModal.jsx
│   │   ├── dashboard/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── StatsSummary.jsx
│   │   │   ├── AppointmentWidget.jsx
│   │   │   ├── DrugApprovalWidget.jsx
│   │   │   └── RescheduleRequestWidget.jsx
│   │   ├── patients/
│   │   │   ├── PatientList.jsx
│   │   │   ├── PatientCard.jsx
│   │   │   ├── PatientDetail.jsx
│   │   │   ├── AddPatientForm.jsx
│   │   │   ├── PatientOverview.jsx
│   │   │   └── SideEffectLog.jsx
│   │   ├── regimens/
│   │   │   ├── RegimenList.jsx
│   │   │   ├── RegimenDetail.jsx
│   │   │   ├── CreateRegimenForm.jsx
│   │   │   ├── EditCycleForm.jsx
│   │   │   ├── DrugSelector.jsx
│   │   │   └── RegimenPreview.jsx
│   │   ├── calendar/
│   │   │   ├── CalendarView.jsx
│   │   │   ├── MonthView.jsx
│   │   │   ├── WeekView.jsx
│   │   │   ├── ListViewView.jsx
│   │   │   ├── EventDetail.jsx
│   │   │   ├── EventEditor.jsx
│   │   │   ├── BulkAdjustmentModal.jsx
│   │   │   ├── CalendarHeader.jsx
│   │   │   └── EventCard.jsx
│   │   ├── drugs/
│   │   │   ├── DrugLibrary.jsx
│   │   │   ├── DrugList.jsx
│   │   │   ├── DrugDetail.jsx
│   │   │   ├── AddSystemDrug.jsx
│   │   │   ├── RequestNewDrug.jsx
│   │   │   ├── DrugRequestList.jsx
│   │   │   └── MyDrugs.jsx
│   │   ├── providers/
│   │   │   ├── ProviderList.jsx
│   │   │   ├── ProviderCard.jsx
│   │   │   ├── AddProviderForm.jsx
│   │   │   └── ProviderDetail.jsx
│   │   ├── messages/
│   │   │   ├── MessageCenter.jsx
│   │   │   ├── ConversationList.jsx
│   │   │   ├── ConversationDetail.jsx
│   │   │   ├── MessageComposer.jsx
│   │   │   └── NotificationPanel.jsx
│   │   └── profile/
│   │       ├── ProfilePage.jsx
│   │       ├── EditProfileForm.jsx
│   │       ├── ChangePasswordForm.jsx
│   │       ├── SettingsPanel.jsx
│   │       ├── NotificationPreferences.jsx
│   │       ├── RegionalSettings.jsx
│   │       ├── HolidaySettings.jsx
│   │       ├── FeedbackForm.jsx
│   │       └── ThemeSelector.jsx
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── NotFoundPage.jsx
│   │   └── UnauthorizedPage.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useAPI.js
│   │   ├── usePagination.js
│   │   ├── useNotification.js
│   │   ├── useTheme.js
│   │   ├── useCalendar.js
│   │   └── useLocalStorage.js
│   ├── context/
│   │   ├── AuthContext.js
│   │   ├── ThemeContext.js
│   │   ├── NotificationContext.js
│   │   └── UserContext.js
│   ├── services/
│   │   ├── api.js              (Axios instance)
│   │   ├── authService.js
│   │   ├── patientService.js
│   │   ├── regimenService.js
│   │   ├── calendarService.js
│   │   ├── drugService.js
│   │   ├── notificationService.js
│   │   └── messageService.js
│   ├── utils/
│   │   ├── dateUtils.js
│   │   ├── validation.js
│   │   ├── storage.js
│   │   ├── logger.js
│   │   ├── constants.js
│   │   └── formatters.js
│   ├── styles/
│   │   ├── themes/
│   │   │   ├── oceanBreeze.css
│   │   │   ├── forestDusk.css
│   │   │   ├── emberGlow.css
│   │   │   ├── midnightStudio.css
│   │   │   ├── slatePro.css
│   │   │   ├── roseGold.css
│   │   │   ├── arcticFrost.css
│   │   │   ├── carbon.css
│   │   │   ├── sunsetPeach.css
│   │   │   ├── lavenderMist.css
│   │   │   ├── goldenHour.css
│   │   │   └── neonCity.css
│   │   ├── global.css
│   │   ├── variables.css
│   │   └── responsive.css
│   ├── App.jsx
│   ├── App.css
│   ├── index.js
│   ├── index.css
│   └── .env
├── package.json
├── .env.example
├── .eslintrc.json
└── README.md
```

INSTALLATION & SETUP:
1. Create React app: npx create-react-app chemo-calendar-frontend
2. Install dependencies:
   - axios (API calls)
   - react-router-dom (Navigation)
   - zustand or Redux (State management)
   - react-hot-toast (Notifications)
   - date-fns or dayjs (Date handling)
   - react-big-calendar (Calendar component)
   - react-select (Dropdown selector)
   - react-hook-form (Form handling)
   - zod (Validation)
   - tailwindcss (Styling - recommended)
   - chart.js and react-chartjs-2 (Charts for progress)
   - lucide-react (Icons)

3. Setup environment: Create .env file with API_BASE_URL, SUPABASE_URL

COMPONENT ARCHITECTURE:
- Use functional components with hooks
- Implement custom hooks for logic reuse
- Use Context API for global state (auth, theme)
- Use local state for component-specific data
- Implement error boundaries for error handling
```

## **Prompt 3.2: Authentication & Profile Components**

```
Create comprehensive authentication and profile components:

AUTH COMPONENTS:

1. LoginPage.jsx
   - Email and password inputs
   - "Remember me" checkbox
   - "Forgot password" link
   - "Continue with Google" button
   - Form validation (real-time)
   - Loading spinner during submission
   - Error message display
   - Redirect to dashboard on success
   - Redirect to register for new users

2. RegisterPage.jsx
   - Form fields:
     * Full Name (required)
     * Email (required, unique validation)
     * Speciality dropdown (for providers)
     * Organization name
     * Password (8+ chars, requirements shown)
     * Confirm Password (must match)
     * Terms & Conditions checkbox (required)
   - Field-level validation (real-time)
   - Show password strength indicator
   - Show requirements as user types
   - Handle registration success
   - Display email verification message
   - Link to login page

3. DisclaimerModal.jsx
   - Display on first login
   - Show legal disclaimer about application
   - Key points:
     * For planning purposes only
     * Not sole decision-making tool
     * Always verify with official sources
     * Patient privacy notice
   - Accept/Decline buttons
   - Don't show again checkbox
   - Store acceptance in localStorage

4. ChangePasswordForm.jsx
   - Current password field (required)
   - New password field (8+ chars)
   - Confirm password field
   - Show password strength
   - Validate match before submit
   - Success/error messages

5. ResetPasswordForm.jsx
   - Email input field
   - Submit button
   - Success message confirmation
   - Error handling
   - Link back to login

PROFILE COMPONENTS:

6. ProfileInformationTab.jsx
   - Display user info in read mode
   - Edit mode with form
   - Fields:
     * First Name
     * Last Name
     * Email (read-only)
     * Organization
     * Speciality (for providers)
     * Phone
   - Edit button to toggle edit mode
   - Save/Cancel buttons in edit mode
   - Validation on edit
   - Success notification on save

7. RegionalSettingsTab.jsx
   - Language dropdown (EN-US default)
   - Country dropdown (searchable)
   - Timezone dropdown (searchable)
   - Show current offset
   - Save button
   - Persist to localStorage + backend

8. HolidaySettingsTab.jsx
   - Toggle enforcement on/off
   - Display country-specific holidays
   - For US: New Year's, MLK Day, Presidents Day, etc.
   - For India: Republic Day, Independence Day, Diwali, etc.
   - For UK: New Year's, Good Friday, Easter Monday, etc.
   - Custom holiday section:
     * Name input
     * Date picker
     * Repeat yearly checkbox
     * Add button
   - List of custom holidays
   - Delete button for each custom holiday
   - Save preferences button

9. NotificationPreferencesTab.jsx
   - Toggle switches for:
     * Email notifications
     * SMS notifications
     * Push notifications
     * Phone call notifications
     * Postal mail notifications
   - For each type show count of how many
   - Notification type preferences:
     * Appointment reminder (channels: email, sms, push)
     * Appointment changed (channels: all)
     * Medication reminder (channels: all)
     * Provider message (channels: all)
     * Side effect request (channels: email)
   - Save preferences button
   - Show saved confirmation

10. FeedbackForm.jsx
    - Type dropdown:
      * Feature Request
      * Bug Report
      * General Feedback
      * Enhancement
      * Other
    - Subject field
    - Message textarea
    - Submit button
    - Success message
    - Notify that owner will receive feedback

11. ThemeSelector.jsx
    - Display 12 theme options in a grid
    - Each theme card shows:
      * Theme icon/preview
      * Theme name
      * Theme description (vibes)
      * Colors swatch
    - Themes:
      1. Ocean Breeze (Cool blues, serif)
      2. Forest Dusk (Earthy greens, elegant)
      3. Ember Glow (Warm reds/oranges)
      4. Midnight Studio (Dark purple, monospace)
      5. Slate Pro (Clean neutral, professional)
      6. Rose Gold (Rich pinks, refined)
      7. Arctic Frost (Icy whites & cyan, clean sans-serif)
      8. Carbon (Pure black bg, neon yellow accent, monospace)
      9. Sunset Peach (Warm orange-pink, elegant Optima font)
      10. Lavender Mist (Soft purples & lilac, Garamond serif)
      11. Golden Hour (Rich amber & gold, classic Baskerville)
      12. Neon City (Dark bg, electric green, techy monospace)
    - Click to apply theme
    - Show theme color strip at bottom
    - Persist theme selection to localStorage
```

## **Prompt 3.3: Calendar & Event Management Components**

```
Create comprehensive calendar and event management components:

CALENDAR VIEW COMPONENTS:

1. CalendarView.jsx (Main Container)
   - View selector buttons: Month | Week | List
   - Calendar header with controls
   - Date navigation (previous/next month)
   - Today button
   - Filter options
   - Event legend
   - Responsive layout

2. MonthView.jsx
   - Standard calendar grid (7 columns for days)
   - Week rows
   - Day cells with:
     * Date number (clickable to see details)
     * Event indicators (colored dots or bars)
     * Event count badge if multiple events
   - Hover to show event preview
   - Click to open event detail modal
   - Highlight today's date
   - Show event truncated names
   - Full calendar colors for different drugs

3. WeekView.jsx
   - 7-day view (Monday-Sunday)
   - Time slots on left (optional for detailed view)
   - Event blocks in time slots or just days
   - Show time if event has specific time
   - Click event to view detail
   - Add event button on empty day

4. ListViewView.jsx
   - Table format:
     * Date column
     * Event column (drug name or custom name)
     * Type column (Drug, Clinic Visit, Lab, etc.)
     * Cycle/Day column (e.g., "Cycle 1, Day 5")
   - Sort by date (ascending)
   - Filter by date range
   - Filter by event type
   - Click row to view detail

5. EventDetail.jsx (Modal)
   - Display event information:
     * Event type
     * Drug name / Custom name
     * Date and time
     * Dose (if drug)
     * Route (if drug)
     * Location
     * Department/Provider info:
       - Department name
       - Address
       - Phone number
       - Map button (links to Google Maps)
       - Call button
     * Cycle and day information
     * Arrive by time (for appointments)
     * Additional notes/warnings
   - If appointment:
     * "Reschedule or Cancel" button
     * "Add to Calendar" button
     * "Visit Early?" opt-in button
     * "Confirm Appointment" button
   - If medication:
     * Show warnings
     * Infusion duration
     * Observation time
   - Edit button (if provider)
   - Delete button (if provider/admin)

6. EventEditor.jsx (Modal/Form)
   - Event type selector (if creating new)
   - Date picker
   - Time picker (optional)
   - Drug selector (if drug type)
   - Custom event name (if custom type)
   - Dose field
   - Route dropdown
   - Location dropdown
   - Department hints
   - Notes textarea
   - Recurring pattern selector:
     * Single event radio button
     * Day of week checkboxes
     * Pattern text input (mwf, 1-5, etc.)
   - Save button
   - Cancel button
   - Delete button (if editing existing)

7. BulkAdjustmentModal.jsx
   - Select date range (From Date, To Date optional)
   - Adjustment direction: Forward or Backward (radio buttons)
   - Days to adjust (number input)
   - Preview button
   - Shows affected event list in preview
   - Cancel and Apply Changebuttons
   - Success message after applying

CALENDAR HEADER & CONTROLS:

8. CalendarHeader.jsx
   - Patient name display (top left)
   - Calendar navigation:
     * Previous month/week/day button
     * Month/Year display
     * Next month/week/day button
     * Today button
   - View selector: Month | Week | List
   - Print calendar button
   - Customize names & colors button
   - Bulk date adjustment button
   - Multi-select toggle
   - Save changes button (green, bottom right)
   - Filter options:
     * By cycle
     * By drug name
     * By date range

HELPER COMPONENTS:

9. CustomizeNamesColorsModal.jsx
   - For each drug in calendar:
     * Drug name field
     * Print name field (max 20 chars)
     * Color picker
     * Save button
   - List of all drugs in calendar
   - Scroll if many drugs
   - Save changes button

10. EventCard.jsx (Compact)
    - Shows in calendar cells or list items
    - Drug name or custom name
    - Dose (abbreviated, if applicable)
    - Time (if available)
    - Color coded by drug
    - Hover to show full info

11. DatePickerInput.jsx
    - Date input field
    - Calendar popup on click
    - Type date directly or use picker
    - Format: MM/DD/YYYY

12. PatientCalendarList.jsx
    - Shows all patient calendars
    - For each calendar:
      * Regimen name
      * Start date
      * Status (Active/Completed/Archived)
      * Cycles completed / Total cycles
      * Provider name
      * Action buttons: View, Edit, Print, Delete
```

## **Prompt 3.4: Regimen Management Components**

```
Create comprehensive regimen management components:

REGIMEN LIST & MANAGEMENT:

1. RegimenList.jsx
   - Filter tabs:
     * All Regimens
     * Standard Regimens
     * My Owned Regimens
     * Shared With Me
   - Search bar (by name or disease type)
   - Disease type filter dropdown
   - Sort options: Name, Created Date, Last Modified
   - List/Grid view toggle
   - Pagination (20 per page default)
   - For each regimen card:
     * Regimen name
     * Disease type
     * Owner name
     * Number of cycles
     * Created date
     * Action buttons:
       - View (eye icon)
       - Duplicate (copy icon)
       - Delete (trash icon, if owner)
       - Share (share icon, if owner)
   - Create New Regimen button (+ button, top right)

2. RegimenDetail.jsx
   - Header:
     * Regimen name
     * Disease type badge
     * Owner name
     * Is Standard label (if applicable)
     * Created/Updated dates
     * Edit button (if owner/admin)
   - Description section
   - Cycles section:
     * Accordion list of cycles
     * For each cycle:
       - Cycle number
       - Cycle length (days)
       - Notes
       - Drugs list (see below)
       - Edit cycle button
       - Delete cycle button (if no events using it)
       - Add Drug button
   - Action buttons:
     * Share
     * Duplicate/Copy
     * Print/Download PDF
     * Delete (if owner/admin)
   - Use button to create calendar from this regimen

3. CreateRegimenForm.jsx
   - Form sections:
     A. Basic Info:
        * Regimen name (required)
        * Disease type dropdown (required)
        * Description textarea
        * Is Standard checkbox (admin only)
     B. Copy from Existing (optional section):
        * "Copy cycles from existing regimen" toggle
        * Regimen selector dropdown
        * Cycle selection checkboxes
        * Text: "Selected cycles will be copied with all their drugs and events. You can modify them after creation."
     C. Cycles Builder:
        * Start with 1 empty cycle
        * For each cycle:
          - Cycle number (auto-incremented)
          - Cycle length in days (required)
          - Notes textarea
          - Drug list (empty initially)
          - "Add Drug" button
          - "Add Another Cycle" button
          - "Remove Cycle" button (if > 1)
        * After drug added to cycle:
          - Drug name
          - Dose
          - Days
          - Route
          - Location
          - Edit button (modal)
          - Remove button
   - Form validation:
     * Name required & unique
     * At least one cycle
     * Each cycle has at least one drug
     * Days format validation
   - Save button
   - Cancel button

4. EditCycleForm.jsx (Modal)
   - Cycle number (read-only)
   - Cycle length days (number input)
   - Notes textarea
   - Drug list (same structure as create)
   - Add another drug button
   - For each drug in cycle:
     * Drug name
     * Dose
     * Days
     * Route
     * Location
     * Infusion duration (optional)
     * Observation time (optional)
     * Dose cap (optional)
     * Warnings textarea
     * Edit drug button
     * Remove drug button
   - Save button
   - Cancel button

5. DrugSelector.jsx
   - Searchable dropdown
   - Search by generic name or brand name
   - Display format:
     * Generic Name - (Brand 1, Brand 2)
     * Default route and location below name
   - Option to "View Drug Database" link
   - Option to "Request New Drug" if drug not found
   - Selected drug shows color preview
   - Show drug details on select:
     * Default route (editable for this cycle)
     * Default location (editable for this cycle)
     * Color (editable for this calendar)

6. RegimenPreview.jsx
   - Show selected cycles overview
   - For each cycle:
     * Cycle number and length
     * Drug list with abbreviated info
     * Timeline showing cycle progression
   - Total regimen duration
   - Print/export button

7. DrugSelectModal.jsx
   - Two tabs: System Drugs | My Drugs
   - Search bar
   - Filter by route or location
   - Drug list with details
   - Click drug to select
   - "Add to Cycle" button at bottom
   - "Request New Drug" link

REUSABLE HELPERS:

8. RegimenCard.jsx
   - Compact regimen preview
   - Regimen name (clickable)
   - Disease type badge
   - Owner name
   - Cycle count
   - Last modified date
   - Action button dropdown (View, Edit, Copy, Delete)

9. CycleSummary.jsx
   - Shows cycle structure
   - Drug timeline visualization
   - Calendar days with drug dosing schedule
```

---

# **SESSION 4: MOBILE APPLICATION (REACT NATIVE / PWA)**

## **Prompt 4.1: Mobile App Setup & Navigation**

```
Create a mobile application for Chemo Calendar patients with 
authentication, appointments, medications, and notifications.

APPROACH OPTIONS:
1. React Native (iOS + Android native apps)
2. Flutter (Google's alternative)
3. PWA (Progressive Web App - web app that works offline)

RECOMMENDED: React Native Expo for faster development

PROJECT SETUP:
1. Create project: npx create-expo-app chemo-calendar-mobile
2. Install dependencies:
   - expo (Framework)
   - react-navigation (Navigation)
   - expo-notifications (Push notifications)
   - axios (API calls)
   - zustand or Redux (State)
   - react-native-gesture-handler (Gestures)
   - date-fns (Dates)
   - react-native-calendars (Calendar widget)
   - react-native-maps (Maps)

FOLDER STRUCTURE:
```
chemo-calendar-mobile/
├── app/
│   ├── (auth)/
│   │   ├── login.jsx
│   │   ├── register.jsx
│   │   ├── forgot-password.jsx
│   │   └── splash.jsx
│   ├── (tabs)/
│   │   ├── appointments.jsx
│   │   ├── medications.jsx
│   │   ├── side-effects.jsx
│   │   ├── messages.jsx
│   │   ├── settings.jsx
│   │   └── _layout.jsx
│   ├── appointment/
│   │   ├── [id].jsx
│   │   └── reschedule.jsx
│   ├── medication/
│   │   └── [id].jsx
│   └── _layout.jsx
├── components/
│   ├── AppointmentCard.jsx
│   ├── MedicationCard.jsx
│   ├── NotificationBanner.jsx
│   └── ...
├── services/
│   ├── api.js
│   ├── authService.js
│   ├── appointmentService.js
│   └── ...
├── utils/
│   ├── storage.js
│   ├── notifications.js
│   └── ...
└── app.json
```

BOTTOM TAB NAVIGATION:
1. Appointments (Calendar icon)
   - Shows upcoming appointments
   - Click to view details
2. Medications (Pill icon)
   - Shows today's medications
   - Click to view details
   - Mark as taken
3. Side Effects (Heart icon)
   - Report side effects
   - View reported effects
4. Messages (Chat icon)
   - Messages from provider
   - Badge for unread count
5. Settings (Gear icon)
   - Profile
   - Preferences
   - Help

KEY MOBILE FEATURES:
- Offline capability (cache appointments/medications)
- Push notifications (appointment reminders)
- Native camera for photo attachments
- Geolocation (navigate to appointment location)
- Home screen shortcuts (quick actions)
- Native calendar integration
- Contact emergency provider (quick call)
```

## **Prompt 4.2: Mobile Appointment & Medication Screens**

```
Create detailed mobile screens for appointments and medications:

APPOINTMENTS TAB SCREEN (appointments.jsx):
Layout:
- Header with "Appointments" title
- "Upcoming" and "Past" segment control
- Pull-to-refresh
- FlatList of appointment cards

For UPCOMING appointments:
- "Arrive by 12:30 PM" (prominent, large text)
- "Starts at 12:45 PM"
- "15 minutes before appointment"
- Provider name: "Daniel Longacre, PA-C"
- Department: "Orthopaedics Selinsgrove"
- Address with MAP button
- Phone number with CALL button
- Action buttons:
  * "Reschedule or Cancel" (secondary button)
  * "Add to Calendar" (secondary button)
  * "Opt in to offers" (if available)
- "Get Ready" section:
  * "Confirm Appointment" (primary button with checkmark)
  * "Confirm now to skip the reminder call"

For PAST appointments:
- Date with status badge (Completed/Cancelled)
- Provider and department info
- "View After Visit Summary" (if available, with document icon)
- "View clinical notes" (if available, with document icon)

Appointment Detail Modal (tap on card):
- Full appointment details
- All action buttons
- Notes section (what to bring, prepare)
- Provider photo
- Map view (optional)
- Call provider button
- Share appointment button

MEDICATIONS TAB SCREEN (medications.jsx):
Layout:
- Header with "Medications" title
- "Today" | "Upcoming" segment control
- Pull-to-refresh
- List of medications

TODAY section:
- "Drug Treatments" heading
- For each medication:
  * Drug name and strength (e.g., "Rituximab 375mg/m2")
  * Route (e.g., "IV Inpatient Admission")
  * Dose
  * Days (e.g., "Days: 7, 10, 28, 33")
  * Checkbox to mark as "Taken" (optional for patients)
  * Clock icon showing times
  * Tap to expand for full details

UPCOMING section:
- Medications scheduled for future dates
- Grouped by date
- "Next Medication: [Date] - [Drug Name]"

Medication Detail Modal (tap on card):
- Drug name and strength (prominent)
- Dose
- Route of administration
- Location/Department
- Infusion duration (if applicable)
- Observation time (if applicable)
- Warnings (displayed in alert box if present)
- Date and time
- Department location hint
- "Preparing for this medication?" expandable section:
  * Patient instructions
  * What to bring
  * Side effects to watch for
- Mark as completed button
- Reschedule button
- Share medication reminder button

SIDE EFFECTS TAB SCREEN (side-effects.jsx):
Layout:
- Header "Side Effects"
- "Report" | "View Reported" tabs
- Pull-to-refresh

REPORT side effects tab:
- Category selector (dropdown or tabs):
  * Gastrointestinal
  * Systemic
  * Dermatological
  * Neurological
  * Psychological
  * Other
- Within category, list of common side effects
- Each effect shows:
  * Emoji/icon
  * Effect name
  * Severity level selector:
    - Mild
    - Moderate
    - Severe
  * Trend indicator:
    - Improving
    - Stable
    - Worsening
  * Notes textarea (optional)
- "Report Side Effects" button (primary)
- Success notification after submission
- "View Reported Effects" link

VIEW REPORTED side effects tab:
- List of reported side effects in card format
- For each effect card:
  * Effect name with emoji
  * Date reported
  * Severity badge (color coded: green/yellow/red)
  * Trend arrow (up/down/right)
  * "ago" text (e.g., "Today", "2 days ago")
  * Click to expand for full details
- "Add New" button
- Filter by:
  * Severity
  * Date range
- Sort by date (newest first)

MESSAGES TAB SCREEN (messages.jsx):
Layout:
- Header with "Messages" title
- Badge showing unread count
- Search bar (optional)
- List of conversations or messages

Message List:
- For each message/conversation:
  * Provider avatar
  * Provider name
  * Message preview (truncated)
  * Timestamp (e.g., "2 hours ago")
  * Unread badge (if unread)
  * Swipe actions (Archive, Delete)
- Pull-to-refresh

Message Detail:
- Provider info at top (name, avatar, online status if applicable)
- Message thread (chronological order)
- Message bubbles (left for provider, right for patient)
- Timestamp under each message
- Input field at bottom for reply
- Send button
- Attach file button (optional)

SETTINGS TAB (settings.jsx):
Sections:
1. Contact Information
   - Email
   - Phone
   - "Review contact info" button

2. Notification Settings
   - Email toggle (with count)
   - SMS toggle (with count)
   - Push notifications toggle (with count)
   - Phone call toggle (with count)
   - Mail toggle (with count)

3. Account Settings
   - Edit profile button
   - Change password button

4. About
   - App version
   - Terms of service link
   - Privacy policy link
   - Help/Support link

5. Logout button (red/warning color)

COMMON MOBILE PATTERNS:
- Tab bar always visible at bottom
- Pull-to-refresh on lists
- Swipe back gesture to go back
- Loading spinners for async operations
- Toast notifications for confirmations
- Badge counts on icons with unread messages/notifications
- Status bar shows connection status
- Haptic feedback on important actions (optional)
```

---

# **SESSION 5: DOCKER DEPLOYMENT CONFIGURATION**

## **Prompt 5.1: Docker Setup & Configuration Files**

```
Create complete Docker setup for Chemo Calendar application 
deployment (local and cloud):

DOCKERFILE FOR FRONTEND (Dockerfile.frontend):
```
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

DOCKERFILE FOR BACKEND (Dockerfile.backend):
```
FROM node:18-alpine
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Copy application
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node healthcheck.js

EXPOSE 5000
CMD ["node", "server.js"]
```

DOCKER-COMPOSE.yml (Local Development):
```
version: '3.8'

services:
  # Frontend
  frontend:
    build:
      context: ./chemo-calendar-frontend
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:5000/api
    depends_on:
      - backend
    networks:
      - chemo-network

  # Backend
  backend:
    build:
      context: ./chemo-calendar-backend
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:password@postgres:5432/chemo_calendar
      - JWT_SECRET=${JWT_SECRET}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./chemo-calendar-backend:/app
      - /app/node_modules
    networks:
      - chemo-network

  # PostgreSQL Database (if not using Supabase)
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=chemo_calendar
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - chemo-network

  # Redis for caching (optional)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - chemo-network

volumes:
  postgres_data:
  redis_data:

networks:
  chemo-network:
    driver: bridge
```

NGINX CONFIGURATION (nginx.conf):
```
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    gzip on;

    server {
        listen 80;
        server_name _;

        root /usr/share/nginx/html;
        index index.html;

        # Cache static files
        location ~* ^/static/(.*)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # API proxy
        location /api {
            proxy_pass http://backend:5000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # React Router fallback
        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
```

ENV FILE TEMPLATE (.env.example):
```
# Frontend
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key

# Backend
NODE_ENV=development
PORT=5000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/chemo_calendar

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRY=7d

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Logging
LOG_LEVEL=info
```

HEALTHCHECK.js (for backend):
```
const http = require('http');

const options = {
  hostname: 'localhost',
  port: process.env.PORT || 5000,
  path: '/api/health',
  method: 'GET',
  timeout: 2000
};

const request = http.request(options, (res) => {
  if (res.statusCode === 200) {
    process.exit(0);
  } else {
    process.exit(1);
  }
});

request.on('error', () => {
  process.exit(1);
});

request.setTimeout(2000, () => {
  request.destroy();
  process.exit(1);
});

request.end();
```

.DOCKERIGNORE:
```
node_modules
npm-debug.log
.git
.gitignore
.DS_Store
.env.local
.env.*.local
dist
build
.next
out
coverage
.vscode
.idea
*.swp
*.swo
```
```

## **Prompt 5.2: Deployment Instructions (Step-by-Step)**

```
Complete step-by-step deployment guide for Chemo Calendar:

PREREQUISITE SETUP:

1. Install Required Tools:
   - Docker Desktop (https://www.docker.com/products/docker-desktop)
   - Docker Compose (usually included with Docker Desktop)
   - Git (https://git-scm.com/)

2. Clone/Prepare Repository:
   ```bash
   git clone <your-repo-url>
   cd chemo-calendar
   ```

3. Prepare Environment Variables:
   ```bash
   # Create .env file in root directory
   cp .env.example .env
   
   # Edit .env with your actual values:
   - SUPABASE_URL: Get from Supabase project dashboard
   - SUPABASE_ANON_KEY: Get from Supabase project dashboard
   - SUPABASE_SERVICE_KEY: Get from Supabase project settings
   - JWT_SECRET: Generate random string (openssl rand -hex 32)
   - SMTP credentials: Use Gmail or SendGrid
   ```

LOCAL DEPLOYMENT (Docker Compose):

STEP 1: Build Images
```bash
# Build both frontend and backend images
docker-compose build

# Expected output:
# Building frontend...
# Building backend...
# Successfully tagged chemo-calendar-frontend:latest
# Successfully tagged chemo-calendar-backend:latest
```

STEP 2: Start Services
```bash
# Start all services in detached mode
docker-compose up -d

# Expected output:
# [+] Running 5/5
#  ✔ Container postgres ...
#  ✔ Container redis ...
#  ✔ Container backend ...
#  ✔ Container frontend ...
# Migration from Buildkit completed
```

STEP 3: Verify Services
```bash
# Check if all containers are running
docker-compose ps

# Expected output:
# CONTAINER ID   IMAGE                        STATUS
# xxx            chemo-calendar-backend:...   Up 2 minutes
# xxx            chemo-calendar-frontend:...  Up 2 minutes
# xxx            postgres:15-alpine           Up 2 minutes
# xxx            redis:7-alpine               Up 2 minutes
```

STEP 4: Check Logs
```bash
# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend

# View all logs with timestamps
docker-compose logs --timestamps
```

STEP 5: Access Application
```bash
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000/api
# Health check: http://localhost:5000/api/health
# Database: localhost:5432 (user: user, password: password)
# Redis: localhost:6379

# Test backend is running:
curl http://localhost:5000/api/health

# Expected response:
# {"status":"ok","timestamp":"2024-01-15T10:30:00Z"}
```

STEP 6: Initialize Database (if using PostgreSQL, not Supabase)
```bash
# Run migrations
docker-compose exec backend npm run db:migrate

# Seed initial data (optional)
docker-compose exec backend npm run db:seed
```

STEP 7: Run Tests
```bash
# Backend tests
docker-compose exec backend npm test

# Frontend tests (in separate command)
docker-compose exec frontend npm test
```

COMMON COMMANDS:

Stop All Services:
```bash
docker-compose down
# Note: This stops containers but preserves data volumes
```

Stop and Remove Everything:
```bash
docker-compose down -v
# Warning: This removes data volumes too!
```

Rebuild After Code Changes:
```bash
docker-compose up --build
```

View Real-time Logs:
```bash
docker-compose logs -f backend  # Follow backend logs
docker-compose logs -f frontend # Follow frontend logs
docker-compose logs -f          # Follow all
```

Restart a Single Service:
```bash
docker-compose restart backend
```

Execute Command in Container:
```bash
docker-compose exec backend node -e "console.log('test')"
docker-compose exec backend npm run seed
```

CLOUD DEPLOYMENT (AWS/Heroku/DigitalOcean):

OPTION 1: AWS EC2 + RDS

1. Launch EC2 Instance:
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (or larger)
   - Security group: Allow ports 80, 443, 22
   - Storage: 30GB minimum

2. SSH into Instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. Install Docker on EC2:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose git
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```

4. Clone Repository:
   ```bash
   git clone <your-repo>
   cd chemo-calendar
   ```

5. Set Environment Variables:
   ```bash
   nano .env  # Edit with your production values
   ```

6. Start Application:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

7. Setup SSL/HTTPS (Let's Encrypt):
   ```bash
   sudo apt-get install -y certbot python3-certbot-nginx
   sudo certbot certonly --standalone -d your-domain.com
   ```

8. Configure Nginx (production configuration):
   ```
   # Update nginx.conf with SSL certificates
   # Redirect HTTP to HTTPS
   # Set appropriate cache headers
   ```

OPTION 2: Heroku Deployment

1. Install Heroku CLI:
   ```bash
   curl https://cli.heroku.com/install.sh | sh
   heroku login
   ```

2. Create Heroku Apps:
   ```bash
   heroku create chemo-calendar-backend
   heroku create chemo-calendar-frontend
   ```

3. Set Environment Variables on Heroku:
   ```bash
   heroku config:set -a chemo-calendar-backend \
     SUPABASE_URL=xxx \
     SUPABASE_ANON_KEY=xxx \
     JWT_SECRET=xxx
   ```

4. Deploy:
   ```bash
   git push heroku main
   ```

OPTION 3: DigitalOcean App Platform

1. Create DigitalOcean Account
2. Connect GitHub repository
3. Create App from Dockerfile
4. Set environment variables in dashboard
5. Deploy (automatic on push to main)

MONITORING & MAINTENANCE:

Health Checks:
```bash
# Setup monitoring endpoint in backend
GET /api/health
Response: { status: "ok", timestamp: "...", services: { db: "ok", redis: "ok" } }
```

Backup Database:
```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U user chemo_calendar > backup.sql

# Restore from backup
docker-