# VetTech & Pet Care Domain Guide for SDETs
### Veterinary Practice Technology — PetDesk, Vetstoria & Beyond

---

## Table of Contents
1. [What Is VetTech / Pet Care Tech?](#1-what-is-vettech--pet-care-tech)
2. [The Veterinary Practice Ecosystem](#2-the-veterinary-practice-ecosystem)
3. [Core Domain Concepts](#3-core-domain-concepts)
4. [Key Platforms Deep Dive](#4-key-platforms-deep-dive)
5. [Key Players & Products](#5-key-players--products)
6. [Data & Integrations](#6-data--integrations)
7. [SDET Testing Guide for VetTech](#7-sdet-testing-guide-for-vettech)
8. [Tech Stack in VetTech](#8-tech-stack-in-vettech)
9. [Regulatory & Compliance Concepts](#9-regulatory--compliance-concepts)
10. [Glossary](#10-glossary)

---

## 1. What Is VetTech / Pet Care Tech?

**VetTech** (Veterinary Technology) is the application of software to veterinary practices, pet health management, and the broader pet care industry. It encompasses everything from booking a vet appointment to managing a clinic's operations, tracking a pet's medical history, and offering telemedicine consultations.

```
Traditional Vet Clinic          VetTech Version
──────────────────────────────────────────────────────────────
Phone call to book appt    →    Online booking (Vetstoria)
Paper health records       →    Digital PIMS (ezyVet, Provet)
Handwritten reminders      →    Automated SMS/email recalls
In-person only consult     →    Telehealth / video consult
Manual invoicing           →    Integrated POS & billing
Verbal medication refills  →    Online prescription portal
Loyalty stamp card         →    Digital wellness plans (PetDesk)
Lost pet paper poster      →    Microchip + digital registration
```

**Why it matters:** The global pet care industry is ~$300B+ and growing. Over 67% of US households own a pet. Vet visits generate ~$35B in revenue annually in the US alone.

---

## 2. The Veterinary Practice Ecosystem

### 2.1 Stakeholders

```
┌──────────────────────────────────────────────────────────────────┐
│                   VETTECH STAKEHOLDER MAP                        │
│                                                                  │
│  PET OWNER (Client)                                              │
│    ↕ books via app/web, receives reminders, pays online         │
│  FRONT DESK STAFF (CSR — Client Service Representative)          │
│    ↕ manages appointments, check-ins, invoicing                  │
│  VETERINARIAN (DVM)                                              │
│    ↕ creates SOAPs, prescribes, orders diagnostics               │
│  VET TECHNICIAN / NURSE                                          │
│    ↕ takes vitals, assists procedures, administers meds          │
│  PRACTICE MANAGER                                                │
│    ↕ sees reports, staff scheduling, KPIs, inventory             │
│  PRACTICE OWNER / VETERINARY GROUP (DSO/VCSO)                   │
│    ↕ multi-location oversight, financial reporting               │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Types of Veterinary Practices

| Type | Description |
|---|---|
| **GP (General Practice)** | Primary care clinic for routine wellness, sick visits |
| **Emergency & Critical Care** | 24/7 emergency hospital (like A&E for pets) |
| **Specialist Practice** | Oncology, cardiology, surgery, dermatology, neurology |
| **Mobile Vet** | Vet travels to client's home |
| **Cat-Only Clinic** | Specialist cat practices (less stressful for cats) |
| **House Call Practice** | Entirely home-based vet service |
| **Humane Society / Shelter** | High-volume, low-cost clinics |
| **Corporate Group** | Chains like VCA, Banfield, BluePearl (owned by Mars) |

---

## 3. Core Domain Concepts

### 3.1 PIMS — Practice Information Management System

The **heart of every vet practice** — equivalent to an EHR (Electronic Health Record) in human medicine.

```
PIMS contains:
  ✦ Patient records (each pet = a patient)
  ✦ Client records (owner linked to pet)
  ✦ Appointment scheduling
  ✦ Medical records (SOAPs)
  ✦ Invoicing and payment
  ✦ Inventory management (medications, supplies)
  ✦ Prescription management
  ✦ Lab and diagnostic integration
  ✦ Reporting and analytics
```

### 3.2 SOAP Notes — Clinical Documentation

The standard format veterinarians use to document every visit:

```
S — SUBJECTIVE
  What the owner reports: "Max has been vomiting for 2 days and is lethargic"

O — OBJECTIVE
  What the vet observes and measures:
  Weight: 12.3 kg | Temp: 39.2°C | Heart Rate: 110 bpm | Respiratory Rate: 24
  Physical exam findings: abdomen tender on palpation, mild dehydration

A — ASSESSMENT
  Veterinarian's diagnosis:
  Probable gastroenteritis; rule out pancreatitis, foreign body obstruction

P — PLAN
  Treatment and next steps:
  Blood panel ordered | Subcutaneous fluids administered
  Metronidazole 250mg BID × 5 days prescribed
  Recheck in 3 days or return to ER if condition worsens
```

### 3.3 Appointment Types

| Type | Description |
|---|---|
| **Wellness / Preventive** | Annual checkup, vaccinations, parasite prevention |
| **Sick Visit** | Pet is unwell; symptoms being investigated |
| **Surgery** | Spay, neuter, dental, orthopaedic procedures |
| **Dental** | Dental cleaning (requires anaesthesia) |
| **Recheck / Follow-up** | Post-treatment check |
| **Vaccination** | Specific vaccine appointments (Rabies, DAPP, Bordetella) |
| **Euthanasia** | End-of-life appointment (emotionally sensitive UX) |
| **Telehealth** | Video or chat consultation |
| **Boarding Check-in/out** | Pet hotel services attached to clinic |

### 3.4 Reminder & Recall System

One of the most valuable features — automatically reminding clients when pets are due for care:

```
REMINDER TYPES:
  Vaccination Recall    → "Max's Rabies vaccine is due next month"
  Annual Wellness       → "Time for Luna's annual checkup"
  Heartworm Test        → "Seasonal reminder for parasite testing"
  Dental               → "It's been 12 months since Max's dental"
  Flea/Tick Prevention → "Refill reminder for NexGard"
  Lab Results          → "Max's bloodwork results are ready"
  Appointment Reminder → "Your appointment is tomorrow at 2pm"
  Post-Visit Follow-up → "How is Max doing after his visit?"

CHANNELS:
  Email | SMS | Push Notification | Postcard (physical mail)

TIMING:
  Advance notice: 30 days, 14 days, 7 days, 1 day before due
  Post-visit: 24 hours, 3 days, 1 week after
```

### 3.5 Wellness Plans / Membership Plans

Subscription-based preventive care packages:

```
Example Wellness Plan ($49/month for a dog):
  ✦ 2 wellness exams per year
  ✦ Core vaccinations included
  ✦ Annual heartworm test
  ✦ Annual flea/tick prevention
  ✦ 10% off additional services

Business logic to test:
  ✓ Plan benefits track consumption (2/2 exams used)
  ✓ Services cannot exceed plan limit without override
  ✓ Monthly billing recurs exactly on billing date
  ✓ Plan cancellation mid-term — what's refunded?
  ✓ Plan transferred if pet ownership changes
  ✓ Multi-pet household — separate plan per pet
```

### 3.6 Pharmaceutical / Prescription Management

```
PRESCRIPTION FLOW:
  Vet examines patient
        ↓
  Vet creates prescription in PIMS
        ↓
  Options:
    In-house dispensing → Medication given at clinic + invoiced
    Written Rx          → Client takes script to pharmacy
    Online pharmacy     → e-Rx sent to Vetsource, Covetrus, Chewy Health

CONTROLLED SUBSTANCES:
  Some medications are DEA-controlled (e.g., phenobarbital, ketamine)
  Require strict DEA log tracking: in, out, waste, count
  SDET: This data must be 100% accurate; audit trail immutable

DRUG INTERACTIONS:
  System should flag if two prescribed drugs interact negatively
  SDET: Test that interaction alerts fire correctly
```

---

## 4. Key Platforms Deep Dive

### 4.1 PetDesk

**PetDesk** is a **client communication and engagement platform** for vet clinics — not a PIMS itself, but an add-on layer that connects to a PIMS.

```
What PetDesk Does:
  ✦ Automated appointment reminders (SMS, email, push)
  ✦ Loyalty/rewards program for pet owners
  ✦ Two-way messaging between clinic and client
  ✦ Online appointment requests (feeds into PIMS)
  ✦ Health record sharing with pet owners
  ✦ Post-visit surveys and reputation management
  ✦ Digital wellness plan management
  ✦ Petly — the client-facing app

How it integrates:
  PetDesk ↔ PIMS (via API/HL7)
  Reads: appointments, patient data, due dates, client info
  Writes: appointment requests, survey responses

Key tech concepts:
  Webhook-driven: PIMS sends events to PetDesk (appointment created, etc.)
  HL7 messaging: Standard healthcare data exchange format
  HIPAA-adjacent: Pet data isn't technically HIPAA but clinics treat it similarly
```

### 4.2 Vetstoria

**Vetstoria** is an **online appointment booking platform** specifically for veterinary practices.

```
What Vetstoria Does:
  ✦ Real-time online booking (24/7, no phone call needed)
  ✦ Syncs live with PIMS calendar (no double-bookings)
  ✦ Customisable booking flows by practice
  ✦ Species-specific booking (dog, cat, rabbit, exotic)
  ✦ New client vs returning client flows
  ✦ Appointment type selection
  ✦ Automated confirmation + reminders
  ✦ Waitlist management
  ✦ Telemedicine booking
  ✦ Google/Facebook booking integration

How it works technically:
  PIMS calendar ← bidirectional sync → Vetstoria
  Client books on Vetstoria widget/app
  Appointment appears in PIMS in real-time
  Prevents double-booking via real-time slot locking

Supported PIMS integrations (what to know):
  ezyVet, Provet Cloud, Shepherd, Rhapsody, ImproMed,
  AVImark, Cornerstone, Digitail, VetlinX
```

### 4.3 Key PIMS Platforms (That PetDesk/Vetstoria Integrate With)

| PIMS | Market | Notes |
|---|---|---|
| **ezyVet** | Global | Modern cloud-based PIMS (NZ-founded) |
| **Provet Cloud** | Global | Cloud PIMS popular in Europe/Australia |
| **Cornerstone** | US | IDEXX's flagship PIMS (desktop-based) |
| **AVImark** | US | Popular older PIMS (Henry Schein) |
| **Shepherd** | US | Modern cloud PIMS for GP practices |
| **Digitail** | Global | Modern cloud PIMS with built-in comms |
| **ImproMed** | US | Corporate practice PIMS |
| **RxWorks** | Australia/NZ | |
| **VetlinX** | Europe | |

---

## 5. Key Players & Products

```
CLIENT ENGAGEMENT / COMMUNICATION:
  PetDesk          → Client comms, reminders, loyalty
  Vet2Pet          → White-label clinic apps
  Petvisor (Zipwhip + PetDesk merged)
  Solutionreach    → Multi-industry (includes vet)

ONLINE BOOKING:
  Vetstoria        → Pure online booking for vets
  PetDesk          → Booking requests (not real-time)
  Calendly (generic) → Some small clinics use this

TELEHEALTH:
  GuardianVets     → After-hours triage service
  Airvet           → On-demand video vet consults
  Pawp             → Subscription telehealth for pets
  VetNOW           → Emergency telehealth triage

DIAGNOSTICS INTEGRATION:
  IDEXX Laboratories → Blood panels, urinalysis, pathology
  Zoetis             → Diagnostics + pharmaceuticals
  Heska              → In-house diagnostic equipment

ONLINE PHARMACY:
  Vetsource          → Integrated online pharmacy
  Covetrus           → Large veterinary distributor + pharmacy
  Chewy Health       → Chewy's vet pharmacy

PET INSURANCE:
  Trupanion          → Direct-to-vet integration for claims
  Nationwide Pet     → Insurance claims
  Lemonade Pet       → New-gen insurance
```

---

## 6. Data & Integrations

### 6.1 HL7 — Healthcare Messaging Standard

Even though animals aren't human patients, veterinary software borrows heavily from healthcare standards.

```
HL7 v2 (older, most common in legacy PIMS):
  Pipe-delimited messages
  MSH|^~\&|PIMS|VetClinic|PETDESK|COMMS|20260701||SIU^S12|123|P|2.5
  
  MSH = Message Header
  SIU = Scheduling Information Unsolicited
  S12 = Notification of new appointment

HL7 FHIR (modern, REST-based):
  JSON/XML format, API-driven
  Resources: Patient, Appointment, Observation, Medication
  Adapted for vet use (Patient resource = animal)

What SDETs test in HL7:
  ✓ Correct message type for each event
  ✓ Required fields populated
  ✓ Character encoding (special chars in pet names)
  ✓ Message delivered within SLA
  ✓ Duplicate message handling (idempotency)
  ✓ Rejected messages caught and alerted
```

### 6.2 IDEXX Integration (Diagnostics)

IDEXX is the dominant veterinary diagnostics company. Tight PIMS integration is critical:

```
IDEXX Integration Flow:
  Vet orders blood panel in PIMS
          ↓
  Test order sent to IDEXX machine (in-house) or lab
          ↓
  Results returned to PIMS within minutes (in-house) / hours (reference lab)
          ↓
  Results auto-attach to patient record
          ↓
  Vet reviews; abnormal values flagged in red

SDET tests:
  ✓ Order transmitted correctly with correct species/tests
  ✓ Results attach to correct patient (no wrong-patient assignment)
  ✓ Abnormal values flagged according to species-specific reference ranges
  ✓ Out-of-reference-range result generates alert
  ✓ Result arrived within SLA
```

### 6.3 Trupanion Direct Pay Integration

Trupanion integrates directly with POS at vet clinics, paying the insured portion instantly:

```
Without integration:      Owner pays 100% → submits claim → waits weeks
With Trupanion Direct:    Trupanion pays their portion AT checkout

SDET tests:
  ✓ Eligibility check returns correct coverage for patient
  ✓ Claim amount calculated correctly (coverage %, deductible applied)
  ✓ Payment splits correctly on invoice
  ✓ Decline (not covered) handled gracefully with clear message
  ✓ Pre-existing condition exclusion flagged
```

---

## 7. SDET Testing Guide for VetTech

### 7.1 Online Booking Testing (Vetstoria-style)

```
CRITICAL TEST SCENARIOS:

Double-booking prevention:
  ✓ Slot appears available → User A starts booking
  ✓ User B books same slot (concurrent) → Only one succeeds
  ✓ Loser sees "slot no longer available" message
  ✓ Both PIMS and booking platform update together (no desync)

Appointment type rules:
  ✓ New puppy exam: blocks species = "Cat" correctly
  ✓ Dental: blocked if under 6 months old (age restriction)
  ✓ Surgery: requires prior wellness exam on record
  ✓ Euthanasia: flows to human-reviewed booking (no self-service auto-book)

PIMS sync:
  ✓ Booked online → appears in PIMS within 30 seconds
  ✓ Cancelled in PIMS → slot reopens on booking widget
  ✓ Provider goes on leave → those slots disappear from widget
  ✓ Public holiday → clinic closed; no slots shown

Species and breed logic:
  ✓ Exotic pet (rabbit, reptile) → routes to exotic-trained vet only
  ✓ Cat → books in cat-friendly room
  ✓ Large breed dog → duration extended vs. small dog

Confirmation:
  ✓ Email confirmation sent within 60 seconds
  ✓ SMS confirmation with correct date, time, clinic address
  ✓ iCal/Google Calendar invite attached
  ✓ Reminder fires at configured intervals (48hr, 24hr, 1hr)
```

### 7.2 Reminder System Testing (PetDesk-style)

```
Reminder trigger testing:
  ✓ Vaccination due → reminder fires exactly X days before due date
  ✓ Timezone handling: reminder at 9am in the clinic's timezone
  ✓ Client opted out of SMS → email only, no SMS sent
  ✓ Client has no email → SMS only
  ✓ Lapsed client (no visit in 18 months) → reactivation campaign
  ✓ Deceased pet flag → NO reminders sent (sensitive edge case!)

Content accuracy:
  ✓ Pet name, owner name, clinic name correct in message
  ✓ Due date correct (not off by one day)
  ✓ Correct vaccine in reminder (Rabies vs DAPP vs Bordetella)
  ✓ Link in email goes to correct clinic's booking page

Multi-pet household:
  ✓ Two pets, different due dates → separate, correct reminders
  ✓ One email per pet or combined per owner? (per clinic config)

Do-Not-Disturb:
  ✓ No messages before 8am or after 8pm (local time)
  ✓ No reminders on public holidays
```

### 7.3 Medical Record & SOAP Testing

```
Data integrity tests:
  ✓ Weight recorded in correct units (lbs vs kg — configurable)
  ✓ Temperature recorded (Fahrenheit vs Celsius per region)
  ✓ SOAP saves and retrieves correctly
  ✓ Deleted SOAP creates audit trail (who deleted, when)
  ✓ Signed SOAP cannot be edited without reason + override log
  ✓ Medication dosage displayed in correct units (mg, ml, mg/kg)

Dose calculation:
  For weight-based dosing:
  ✓ Drug: Amoxicillin 10mg/kg BID
  ✓ Pet weight: 5.2 kg
  ✓ Calculated dose: 52mg BID
  ✓ Available formulation: 50mg/ml liquid
  ✓ Volume to dispense: 1.04ml per dose
  System should calculate and display all of the above accurately.

Allergy alerts:
  ✓ Known allergy on record → alert fires when same drug prescribed
  ✓ Alert cannot be silently dismissed without reason logged

Controlled substance log:
  ✓ Every dispensing event: drug, qty, patient, vet who authorised
  ✓ Waste recorded (e.g., 0.5ml wasted from vial)
  ✓ Total dispensed + wasted = total drawn from vial
  ✓ Immutable: log entry cannot be edited
```

### 7.4 Telehealth Testing

```
Video consultation tests:
  ✓ Both vet and client can join from app and web
  ✓ Video/audio quality acceptable on low bandwidth
  ✓ Recording starts/stops correctly (where permitted)
  ✓ Chat available as fallback if video fails
  ✓ Vet can add SOAP notes during/after teleconsult
  ✓ Prescription generated from teleconsult flagged as telehealth Rx
  ✓ Telemedicine session billed correctly (separate code)

Triage chatbot:
  ✓ Symptom checker routes to correct urgency level
  ✓ Emergency symptoms (difficulty breathing) → direct to ER, not booking
  ✓ Non-emergency → offered telehealth or next available appointment
```

### 7.5 Sensitive UX Test Scenarios

VetTech has unique emotional edge cases:

```
Euthanasia appointment:
  ✓ Cannot be booked self-service (always requires phone call)
  ✓ Confirmation message uses sensitive language
  ✓ Post-visit follow-up: NO automated "How was your visit?" sent
  ✓ Pet status updated to "Deceased" after appointment
  ✓ Future reminders for that pet immediately suppressed

Deceased pet:
  ✓ All reminders stop immediately when deceased flag set
  ✓ No renewal campaign, no wellness plan renewal notice
  ✓ Historical records remain accessible for reference
  ✓ Owner receives appropriate condolence message (optional clinic setting)

Aggressive/dangerous animal flag:
  ✓ "Caution" flag visible on patient record
  ✓ Flag visible to ALL staff before appointment
  ✓ Flag visible on check-in workflow
```

---

## 8. Tech Stack in VetTech

| Technology | Usage in VetTech |
|---|---|
| **React / Angular** | Dashboard UIs for clinic staff |
| **React Native / Flutter** | Pet owner mobile apps |
| **Node.js / Python / Ruby** | Backend APIs |
| **PostgreSQL** | Patient, client, appointment data |
| **HL7 FHIR / HL7 v2** | Health data exchange with PIMS |
| **Twilio** | SMS reminders and two-way messaging |
| **SendGrid / Mailgun** | Email campaigns and transactional emails |
| **Stripe / Square** | Payment processing at checkout |
| **WebRTC** | Browser-based video telehealth |
| **AWS / GCP** | Cloud infrastructure |
| **Redis** | Session management, real-time slot locking |
| **Elasticsearch** | Patient record search |
| **Webhooks** | PIMS event notifications |

---

## 9. Regulatory & Compliance Concepts

### Regulations Affecting VetTech

| Regulation | What It Covers |
|---|---|
| **VCPR** | Veterinarian-Client-Patient Relationship — legally required before prescribing |
| **DEA Registration** | Required to prescribe/dispense controlled substances |
| **AVMA Guidelines** | Professional standards (American Veterinary Medical Association) |
| **State Vet Board Rules** | Each US state has its own veterinary licensing board |
| **HIPAA (adjacent)** | Not technically HIPAA (animals), but clinics handle it similarly |
| **GDPR / CCPA** | Pet owner personal data privacy |
| **FSMA** | Food Safety Modernization Act (affects pet food/treats sold in clinic) |
| **Telemedicine Laws** | Many states require in-person VCPR before telehealth Rx |

### VCPR — The Foundational Rule

```
VCPR (Veterinarian-Client-Patient Relationship) must exist before:
  ✓ Prescribing any medication
  ✓ Providing telemedicine diagnosis
  ✓ Issuing a health certificate

A VCPR requires:
  - Vet has physically examined the animal (or knows the animal's history)
  - Vet is available for follow-up care
  - Owner has agreed to follow vet's advice

SDET test:
  ✓ System prevents prescription without prior examination on record
  ✓ Telehealth prescription blocked if no in-person VCPR established
  ✓ VCPR date recorded and visible on Rx
```

---

## 10. Glossary

| Term | Definition |
|---|---|
| **PIMS** | Practice Information Management System — core vet clinic software |
| **SOAP** | Subjective, Objective, Assessment, Plan — medical record format |
| **DVM / VMD** | Doctor of Veterinary Medicine — licensed veterinarian |
| **VCPR** | Veterinarian-Client-Patient Relationship |
| **Patient** | The animal (pet) receiving care |
| **Client** | The pet owner |
| **Recall** | Reminder that a pet is due for a service |
| **HL7** | Health Level 7 — healthcare data messaging standard |
| **FHIR** | Fast Healthcare Interoperability Resources — modern HL7 standard |
| **IDEXX** | Largest veterinary diagnostics company |
| **DEA** | Drug Enforcement Administration (controls veterinary narcotics) |
| **Controlled Substance** | Regulated drugs requiring DEA logging |
| **Wellness Plan** | Monthly subscription for preventive care |
| **BID** | Twice daily (medical dosing instruction) |
| **SID / QD** | Once daily |
| **TID** | Three times daily |
| **QID** | Four times daily |
| **PRN** | As needed |
| **PO** | By mouth (oral medication) |
| **SQ / SC** | Subcutaneous (under the skin injection) |
| **IM** | Intramuscular injection |
| **IV** | Intravenous |
| **AVMA** | American Veterinary Medical Association |
| **GP Practice** | General practice vet clinic |
| **Specialist** | Board-certified specialist (cardiologist, oncologist, etc.) |
| **ER / Emergency** | Emergency veterinary hospital |
| **Telehealth** | Remote veterinary consultation via video/chat |
| **PetDesk** | Client engagement platform for vet clinics |
| **Vetstoria** | Online appointment booking platform for vets |
| **ezyVet** | Cloud-based PIMS platform |
| **Trupanion** | Pet insurance with direct-to-vet payment |
| **Chewy Health** | Chewy's veterinary pharmacy division |
| **Boarding** | Overnight pet care at a facility |
| **Grooming** | Pet washing, trimming, and styling service |
| **DSO / VCSO** | Dental/Veterinary Service Organisation — corporate clinic group |

---

*VetTech & Pet Care Domain Guide for SDETs | PetDesk, Vetstoria & Veterinary Technology*
*Last updated: July 2026*
