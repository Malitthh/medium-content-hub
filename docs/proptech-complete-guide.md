# PropTech Domain Guide for SDETs
### Property Technology — From Listings to Smart Buildings

---

## Table of Contents
1. [What Is PropTech?](#1-what-is-proptech)
2. [PropTech Sub-Sectors](#2-proptech-sub-sectors)
3. [Core Domain Concepts](#3-core-domain-concepts)
4. [Property Management Software Deep Dive](#4-property-management-software-deep-dive)
5. [Key Players & Products](#5-key-players--products)
6. [Data & Integrations in PropTech](#6-data--integrations-in-proptech)
7. [SDET Testing Guide for PropTech](#7-sdet-testing-guide-for-proptech)
8. [Tech Stack in PropTech](#8-tech-stack-in-proptech)
9. [Regulatory & Compliance Concepts](#9-regulatory--compliance-concepts)
10. [Glossary](#10-glossary)

---

## 1. What Is PropTech?

**PropTech (Property Technology)** is the application of technology to the real estate and property management industry. It covers every stage of a property's lifecycle — searching, buying, renting, managing, maintaining, and selling.

```
Traditional Real Estate          PropTech Version
─────────────────────────────────────────────────────────
Newspaper classifieds      →     Zillow / Rightmove listings
Physical lease signing     →     E-signature + digital lease
Cash/cheque rent           →     Online rent payment portals
Manual maintenance calls   →     In-app maintenance tickets
On-site property manager   →     Remote management dashboards
Manual inspections         →     IoT sensors + smart building
Agent walkthroughs         →     3D virtual tours / VR
Paper accounting           →     Cloud property accounting
```

**Market Size:** Global PropTech market valued at ~$40B+ (2024) growing rapidly.

---

## 2. PropTech Sub-Sectors

```
┌──────────────────────────────────────────────────────────────────┐
│                        PROPTECH ECOSYSTEM                        │
├────────────────┬─────────────────┬──────────────┬───────────────┤
│ Real Estate    │ Property        │ Construction │ Smart         │
│ Marketplaces   │ Management      │ Tech         │ Buildings     │
├────────────────┼─────────────────┼──────────────┼───────────────┤
│ Zillow         │ Yardi Systems   │ Procore      │ IoT Sensors   │
│ Rightmove      │ AppFolio        │ PlanGrid     │ BMS Systems   │
│ Redfin         │ Buildium        │ Autodesk BIM │ HVAC Control  │
│ CoStar         │ RealPage        │ eSUB         │ Access Control│
│ Trulia         │ PropertyMe      │ BuilderTrend │ Energy Mgmt   │
├────────────────┼─────────────────┼──────────────┼───────────────┤
│ iBuying /      │ Short-Term      │ Real Estate  │ Proptech      │
│ Investment     │ Rentals         │ Finance      │ Analytics     │
├────────────────┼─────────────────┼──────────────┼───────────────┤
│ Opendoor       │ Airbnb          │ Blend        │ Reonomy        │
│ Offerpad       │ Vrbo            │ Better.com   │ HouseCanary   │
│ Roofstock      │ Furnished Finder│ LoanSnap     │ CompStak      │
└────────────────┴─────────────────┴──────────────┴───────────────┘
```

---

## 3. Core Domain Concepts

### 3.1 Property Types

| Type | Description | Examples |
|---|---|---|
| **Residential** | Properties people live in | Houses, apartments, condos, studios |
| **Commercial** | Business use | Offices, retail stores, restaurants |
| **Industrial** | Manufacturing/warehousing | Factories, distribution centres |
| **Mixed-Use** | Combined residential + commercial | Ground floor retail, upper floor apartments |
| **Multi-Family** | Multiple units in one building | Apartment complexes, duplexes |
| **Single-Family** | One household per property | Detached house |

### 3.2 Stakeholders (Who Uses PropTech Software)

```
PROPERTY OWNER / LANDLORD
  ↕ (manages portfolio via software)
PROPERTY MANAGER / MANAGEMENT COMPANY
  ↕ (communicates with)
TENANT / RESIDENT
  ↕ (uses for)
MAINTENANCE TECHNICIAN / VENDOR
  ↕ (reports to)
ACCOUNTANT / FINANCE TEAM
  ↕ (integrates with)
REAL ESTATE AGENT / BROKER
```

### 3.3 Key Processes in Property Management

```
PROPERTY LIFECYCLE:
  Listing → Inquiry → Showing → Application → Screening
     ↓
  Lease Signing → Move-In Inspection → Tenancy
     ↓
  Rent Collection → Maintenance Requests → Inspections
     ↓
  Lease Renewal / Lease Termination → Move-Out Inspection
     ↓
  Security Deposit Return → Re-listing
```

### 3.4 Lease Concepts

- **Lease Agreement** — Legal contract between landlord and tenant
- **Lease Term** — Duration (month-to-month, 6-month, 12-month, multi-year)
- **Rent Roll** — List of all units, tenants, rent amounts, and payment status
- **Vacancy Rate** — % of units not occupied; key performance metric
- **NOI (Net Operating Income)** — Revenue from property minus operating expenses
- **Cap Rate** — NOI ÷ Property Value; measures investment return
- **CAM (Common Area Maintenance)** — Commercial lease charges for shared spaces

### 3.5 Rent & Payment Concepts

```
PAYMENT TYPES:
  Base Rent           → Core monthly rent amount
  Security Deposit    → Refundable upfront payment (usually 1-2 months rent)
  Pet Deposit         → Additional deposit for pets (may be non-refundable)
  Late Fee            → Charged after grace period (e.g., 5 days after due date)
  NSF Fee             → Non-Sufficient Funds — returned cheque fee
  Utility Charges     → Water, gas, electric passed through to tenant
  CAM Charges         → (Commercial) Shared building cost pass-throughs

PAYMENT STATES:
  Scheduled → Pending → Processing → Posted / Failed / Reversed

GRACE PERIOD:
  Days after the due date before a late fee applies
  E.g., rent due 1st, grace period 5 days → late fee on 6th
```

### 3.6 Maintenance & Work Orders

```
MAINTENANCE REQUEST FLOW:

Tenant submits request (app/portal)
          ↓
Property Manager reviews + assigns priority
     [Emergency / Urgent / Routine]
          ↓
Work Order created → Assigned to Vendor/Tech
          ↓
Vendor schedules + completes work
          ↓
Completion confirmed → Tenant notified
          ↓
Invoice processed → Cost recorded against property
```

**Priority Levels:**
- Emergency — Life/safety risk (gas leak, no heat in winter, flooding)
- Urgent — Significant inconvenience (no hot water, broken lock)
- Routine — Minor inconvenience (dripping tap, light bulb)

---

## 4. Property Management Software Deep Dive

### 4.1 Core Modules in Any PMS (Property Management System)

```
┌──────────────────────────────────────────────────────────────┐
│              PROPERTY MANAGEMENT SYSTEM (PMS)                │
├──────────────┬───────────────┬──────────────┬───────────────┤
│   Leasing    │   Resident    │  Accounting  │  Maintenance  │
│   Module     │   Portal      │  Module      │  Module       │
├──────────────┼───────────────┼──────────────┼───────────────┤
│ Listings     │ Online Pay    │ GL / Ledger  │ Work Orders   │
│ Applications │ Maintenance   │ AP / AR      │ Vendor Mgmt   │
│ Screening    │ Documents     │ Bank Recs    │ Inspections   │
│ Lease Gen    │ Messaging     │ Reporting    │ Scheduling    │
│ E-Signature  │ Move-in/out   │ Budgeting    │ Asset Tracking│
└──────────────┴───────────────┴──────────────┴───────────────┘
```

### 4.2 Tenant Screening

```
SCREENING CHECKS:
  ✦ Credit Check     → Credit score, payment history, debt levels
  ✦ Criminal Check   → Background criminal history
  ✦ Eviction Check   → Prior eviction history
  ✦ Income Verify    → Income typically must be 3× monthly rent
  ✦ Reference Check  → Prior landlord references
  ✦ Identity Verify  → ID document verification

Screening Providers (3rd party integrations to test):
  TransUnion ResidentScreen
  Experian RentBureau
  Checkr
  RentPrep
```

### 4.3 Accounting in Property Management

```
KEY ACCOUNTING CONCEPTS:
  Trust Accounting    → Security deposits held separately (legally required)
                        Never mix with operating funds
  Accounts Receivable → Rent owed to landlord
  Accounts Payable    → Bills the landlord must pay (vendors, utilities)
  Bank Reconciliation → Matching software records to bank statement
  Owner Distributions → Sending property owners their net income
  1099 Reporting      → US tax reporting for vendors paid > $600/year

GENERAL LEDGER ENTRIES:
  When rent collected:
    DR: Cash / Bank
    CR: Rental Income

  When vendor paid:
    DR: Maintenance Expense
    CR: Cash / Bank
```

---

## 5. Key Players & Products

### Major Property Management Platforms

| Platform | Market | Specialisation |
|---|---|---|
| **Yardi Systems** | Global | Enterprise — large multi-family and commercial |
| **AppFolio** | US | Mid-market residential PM |
| **Buildium** | US | Small-large residential PM |
| **RealPage** | US | Large enterprise, revenue management |
| **MRI Software** | Global | Commercial real estate |
| **PropertyMe** | Australia | Residential PM, popular in ANZ |
| **Re-Leased** | NZ/UK/AU/US | Commercial PM |
| **Rent Manager** | US | Residential and commercial PM |
| **Entrata** | US | Multi-family, all-in-one platform |
| **Doorloop** | US | Modern, fast-growing PM platform |

### Real Estate Marketplaces

| Platform | Region | Focus |
|---|---|---|
| **Zillow** | US | Residential listings, Zestimate valuations |
| **Redfin** | US | Listings + brokerage hybrid |
| **CoStar** | US/Global | Commercial real estate data |
| **Rightmove** | UK | Residential listings |
| **Zoopla** | UK | Residential listings + data |
| **Domain** | Australia | Residential listings |
| **REA Group** | Australia | Realestate.com.au |

### Short-Term Rental (STR) Platforms

| Platform | Use Case |
|---|---|
| **Airbnb** | Global peer-to-peer short-term rentals |
| **VRBO** | Vacation rentals (Expedia Group) |
| **Hostaway** | Channel manager for STR hosts |
| **Guesty** | Enterprise STR management |
| **Lodgify** | STR website + booking engine |

---

## 6. Data & Integrations in PropTech

### 6.1 Key Integrations PropTech Platforms Have

```
PMS Platform integrates with:
  ├── Payment Gateways    (Stripe, PayPal, Dwolla, ACH processors)
  ├── Screening Providers (TransUnion, Experian, Checkr)
  ├── E-Signature         (DocuSign, HelloSign, Adobe Sign)
  ├── Listing Syndication (Zillow, Trulia, Apartments.com, Craigslist)
  ├── Accounting Software (QuickBooks, Xero)
  ├── Smart Locks         (August, Schlage, Yale)
  ├── Maintenance Tools   (Lula, Homee, ServiceChannel)
  ├── Utility Billing     (Conservice, Livable)
  ├── Renter's Insurance  (Lemonade, Sure)
  └── Communication       (Twilio SMS, SendGrid email)
```

### 6.2 Listing Syndication

When a property is listed vacant, it needs to appear on multiple platforms simultaneously:

```
PMS (Source of Truth)
    ↓ Syndicates to:
  Zillow        → Automatically
  Trulia        → Automatically (Zillow Network)
  Apartments.com → Via API
  Facebook Marketplace → Via API
  Craigslist    → Sometimes manual

Sync challenges to test:
  ✓ Price update in PMS → reflects on all portals
  ✓ Unit marked as rented → removed from all portals
  ✓ Photo changes propagate correctly
  ✓ Syndication failures are detected and alerted
```

### 6.3 Payment Processing in PropTech

```
PAYMENT METHODS:
  ACH (Automated Clearing House) → Direct bank transfer (US standard)
  Credit/Debit Card               → Convenience fee typically applies
  Cheque                          → Manual processing
  Cash                            → Rare; requires cash receipt

ACH PAYMENT FLOW:
  Tenant initiates → ACH transaction created → NACHA network
       ↓
  Pending (1-3 business days)
       ↓
  Settled / Returned (NSF, account closed, unauthorised)

NACHA (National Automated Clearing House Association):
  The governing body for ACH in the US. Key rules:
  - R01: Insufficient Funds
  - R02: Account Closed
  - R10: Customer Advises Not Authorized
  All return codes must be handled and communicated correctly.
```

---

## 7. SDET Testing Guide for PropTech

### 7.1 Core Test Areas

#### A. Leasing Workflow Testing

```
Test the end-to-end leasing funnel:

  ✓ Unit listing appears with correct details (address, beds, baths, price)
  ✓ Online application form — all fields validated correctly
  ✓ Required documents upload (ID, pay stubs)
  ✓ Screening trigger — fires correctly after application submitted
  ✓ Screening result received within SLA
  ✓ Conditional / Approved / Denied decision applied correctly
  ✓ Lease generated with correct terms (start date, rent, unit details)
  ✓ E-signature flow works on web and mobile
  ✓ Countersignature by landlord/manager required before activation
  ✓ Move-in date blocked until lease is countersigned

Edge cases:
  ✗ Co-applicant: all parties must sign before lease activates
  ✗ Lease start date in past → should be rejected
  ✗ Overlapping lease terms on same unit → system should catch
  ✗ Screening provider returns no result → graceful timeout handling
```

#### B. Rent Collection Testing

```
Critical payment test scenarios:

  ✓ Rent charge auto-posted on 1st of month
  ✓ Late fee auto-applied after grace period (check exact day/time)
  ✓ ACH payment submitted → status transitions correctly
  ✓ Payment posted → tenant ledger updated → owner ledger updated
  ✓ NSF return → payment reversed → NSF fee applied → tenant notified
  ✓ Partial payment posted → remaining balance carried forward
  ✓ Prepayment (paid in advance) → credit applied correctly
  ✓ Security deposit collected separately (trust account)
  ✓ Security deposit NEVER mixes with operating funds

Calculation tests:
  ✓ Prorated rent: tenant moves in mid-month
    Formula: (Monthly Rent ÷ Days in Month) × Days Remaining
    E.g. $1,500 ÷ 31 days × 16 days = $774.19
  ✓ Late fee calculation exact to the day
  ✓ Owner disbursement = Rent Collected - Management Fee - Expenses
```

#### C. Maintenance Module Testing

```
Work order state machine:
  New → Assigned → In Progress → Completed → Closed
  New → Cancelled
  Assigned → Unassigned (vendor refuses)

Test scenarios:
  ✓ Emergency work order → immediate notification (push + SMS + email)
  ✓ Routine order → assigned within business hours
  ✓ Vendor notified with correct address, unit, contact details
  ✓ Tenant can track status in real time
  ✓ Photo uploads attach correctly to work order
  ✓ Vendor marks complete → tenant satisfaction survey sent
  ✓ Cost recorded against correct property/unit/category
  ✓ Recurring maintenance (HVAC filters) auto-creates on schedule

Edge cases:
  ✗ Tenant submits duplicate maintenance request → detected/merged
  ✗ Work order on vacant unit → no tenant notification sent
  ✗ Vendor invoice amount differs from estimate → flag for approval
```

#### D. Accounting & Financial Testing

```
This is where bugs cost real money — test with extreme care:

  ✓ Rent roll report balances to sum of individual ledgers
  ✓ Trust account balance = sum of all held security deposits
  ✓ Bank reconciliation: software balance matches bank statement
  ✓ Owner statement: all income and expenses accounted for
  ✓ Management fee calculated correctly (% of rent collected)
  ✓ 1099 report: all vendor payments aggregated correctly
  ✓ Year-end financials: income statement, balance sheet accurate
  ✓ Journal entries balanced (debits = credits always)

Boundary tests:
  ✗ Owner statement on property with zero activity → shows correctly
  ✗ Management fee on partial month → prorated correctly
  ✗ Two payments same day → both recorded, no duplication
  ✗ Negative balance → system handles without crashing
```

#### E. Tenant Portal Testing

```
Test as a tenant:
  ✓ Login and authentication (SSO, 2FA options)
  ✓ Pay rent online (ACH and card)
  ✓ View ledger / payment history
  ✓ Submit maintenance request with photos
  ✓ View lease document (PDF download)
  ✓ Receive push/email/SMS notifications
  ✓ Communicate with property manager (in-app messaging)
  ✓ Renew lease online
  ✓ Submit move-out notice
  ✓ View/download move-in inspection report

Mobile-specific tests:
  ✓ App works offline (cached data)
  ✓ Push notifications received on iOS and Android
  ✓ Photo upload from camera vs. gallery both work
  ✓ Biometric login (Face ID, fingerprint)
```

#### F. Smart Building / IoT Testing (Emerging)

```
IoT test scenarios:
  ✓ Smart lock generates access code for new tenant on lease start
  ✓ Smart lock revokes access on move-out date
  ✓ Access code for maintenance vendor — time-limited (e.g., 9am-5pm only)
  ✓ Thermostat setpoint changes propagate within expected time
  ✓ Water leak sensor triggers emergency work order automatically
  ✓ Occupancy sensor data feeds into energy management reports
  ✓ Device offline → alert raised to building manager

Data integrity:
  ✓ Sensor readings timestamped correctly (UTC vs local timezone)
  ✓ Historical sensor data queryable for audit/insurance purposes
```

### 7.2 Performance Testing Considerations

| Scenario | Test What |
|---|---|
| Rent due date (1st of month) | All charges post simultaneously without failure |
| Listing syndication | Updates push to 5+ portals within SLA |
| Lease renewal campaign | 1000+ renewal offers sent without queue backup |
| Large portfolio load | Dashboard loads 10,000 units without timeout |
| Report generation | Year-end owner statements for 500 owners complete in time |

### 7.3 Integration Testing Matrix

```
Integration         Test Scenario
─────────────────────────────────────────────────────
DocuSign            Lease e-signature webhook received and processed
Stripe              Payment succeeded webhook → ledger update
ACH Processor       NSF return code → payment reversed in 2 business days
TransUnion          Screening request → result returned in < 60 seconds
Zillow              New listing → appears on Zillow within 24 hours
SendGrid            Rent reminder email delivered (not spam-filtered)
Twilio              SMS notification delivered; handles opt-out (STOP)
QuickBooks          Rent income syncs correctly to QB income account
Smart Lock API      New tenant lease → access code provisioned
```

---

## 8. Tech Stack in PropTech

### Languages & Frameworks

| Technology | Usage |
|---|---|
| **React / Next.js** | Tenant portals, manager dashboards (web) |
| **React Native / Flutter** | Mobile tenant and manager apps |
| **Node.js / Ruby on Rails** | Backend APIs |
| **Python** | Data analytics, ML-based rent pricing |
| **Java / Kotlin** | Android native apps |
| **Swift** | iOS native apps |
| **PostgreSQL** | Core property, lease, and financial data |
| **Redis** | Session management, real-time notifications |
| **Elasticsearch** | Property search with geo-filters |

### Key Infrastructure Concepts

```
MULTI-TENANCY:
  PropTech SaaS platforms serve many PM companies on one platform.
  Data isolation is critical — Company A must NEVER see Company B's data.
  Test: Can user of Company A access Company B's data via API manipulation?

GEO-SEARCH:
  "Find properties within 5 miles of [location]"
  Powered by PostGIS (PostgreSQL), Elasticsearch geo-queries, or Google Maps API
  Test: Distance calculations correct, results ordered by proximity

DOCUMENT STORAGE:
  Leases, IDs, inspection reports stored in S3 / Azure Blob
  Test: Upload works, download returns correct version, old versions retained

WEBHOOKS:
  Events trigger notifications to integrated systems
  Test: Webhook retry on failure, idempotency (duplicate events handled)
```

---

## 9. Regulatory & Compliance Concepts

### US Regulations Affecting PropTech

| Regulation | Covers |
|---|---|
| **Fair Housing Act** | Cannot discriminate in housing by race, religion, sex, disability, familial status, national origin |
| **FCRA (Fair Credit Reporting Act)** | Rules around using credit reports for screening |
| **ADA (Americans with Disabilities Act)** | Accessibility requirements in commercial properties |
| **SCRA (Servicemembers Civil Relief Act)** | Special lease protections for US military members |
| **GDPR / CCPA** | Data privacy for EU / California tenants |
| **NACHA Rules** | ACH payment processing compliance |
| **State/Local Rent Control** | Some cities cap rent increases (e.g., NYC, San Francisco) |

### SDET Compliance Test Scenarios

```
Fair Housing:
  ✓ Screening criteria applied equally to all applicants
  ✓ No protected class information collected on applications
  ✓ Denial letters include legally required adverse action notices

Data Privacy:
  ✓ Tenant can request their data (GDPR right to access)
  ✓ Tenant can request deletion (right to erasure)
  ✓ PII masked in logs and non-production environments
  ✓ SSN / credit card numbers never stored in plain text

Rent Control:
  ✓ System enforces maximum rent increase % for rent-controlled units
  ✓ Rent increase notice sent with legally required notice period
```

---

## 10. Glossary

| Term | Definition |
|---|---|
| **PMS** | Property Management System — core software platform |
| **NOI** | Net Operating Income — revenue minus operating expenses |
| **Cap Rate** | NOI ÷ Property Value — measures investment return |
| **Rent Roll** | List of all units with tenant, rent, and lease details |
| **Vacancy Rate** | % of units not currently occupied |
| **ACH** | Automated Clearing House — US bank transfer network |
| **NSF** | Non-Sufficient Funds — returned payment due to low balance |
| **Trust Account** | Separate bank account required for holding security deposits |
| **Prorated Rent** | Partial rent for a partial month |
| **Work Order** | Maintenance task assigned to a vendor or technician |
| **CAM** | Common Area Maintenance charges in commercial leases |
| **Lease Abstract** | Summary of key lease terms (for quick reference) |
| **E-Signature** | Legally binding digital signature (DocuSign, HelloSign) |
| **Listing Syndication** | Publishing a listing to multiple platforms simultaneously |
| **Screening** | Credit, criminal, eviction background check on applicant |
| **Gross Lease** | Landlord pays all property expenses; tenant pays flat rent |
| **Net Lease** | Tenant pays base rent + some/all property expenses |
| **STR** | Short-Term Rental (Airbnb, VRBO) |
| **MTM** | Month-to-Month lease — no fixed end date |
| **HOA** | Homeowners Association — governs shared community rules |
| **1099** | US tax form reporting vendor payments > $600 |
| **FCRA** | Fair Credit Reporting Act — rules around credit-based decisions |
| **BMS** | Building Management System — controls HVAC, lighting, access |
| **IoT** | Internet of Things — connected sensors in smart buildings |
| **Yield** | Annual rental income as % of property value |

---

*PropTech Domain Guide for SDETs | Property Management & Services*
*Last updated: July 2026*
