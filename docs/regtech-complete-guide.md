# RegTech Domain Guide for SDETs
### Regulatory Technology — Compliance & Regulatory Intelligence

---

## Table of Contents
1. [What Is RegTech?](#1-what-is-regtech)
2. [RegTech Sub-Sectors](#2-regtech-sub-sectors)
3. [Core Domain Concepts](#3-core-domain-concepts)
4. [Regulatory Intelligence Deep Dive — Cube Style](#4-regulatory-intelligence-deep-dive--cube-style)
5. [KYC & AML Deep Dive](#5-kyc--aml-deep-dive)
6. [Regulatory Reporting Deep Dive](#6-regulatory-reporting-deep-dive)
7. [Key Players & Products](#7-key-players--products)
8. [SDET Testing Guide for RegTech](#8-sdet-testing-guide-for-regtech)
9. [Tech Stack in RegTech](#9-tech-stack-in-regtech)
10. [Global Regulators Reference](#10-global-regulators-reference)
11. [Glossary](#11-glossary)

---

## 1. What Is RegTech?

**RegTech (Regulatory Technology)** is the use of technology to help financial institutions and businesses comply with regulations efficiently, accurately, and cost-effectively.

```
THE PROBLEM REGTECH SOLVES:

Financial regulation is:
  ✦ Massive in volume    → Tens of thousands of rules globally
  ✦ Always changing      → 300+ regulatory changes per day globally (Cube estimates)
  ✦ Jurisdictionally complex → Every country/region has different rules
  ✦ Costly to comply with → Banks spend $200–$300B/year on compliance
  ✦ High penalty for failure → Billions in fines for non-compliance

REGTECH'S ANSWER:
  Automate monitoring    → Track regulatory changes automatically
  Automate mapping       → Map rules to internal policies
  Automate reporting     → Generate regulatory reports accurately
  Automate screening     → KYC/AML checks at scale
  Automate audit trails  → Immutable logs of all compliance actions
```

**Why it matters:** In 2023 alone, global financial institutions were fined over $5 billion for compliance failures. RegTech exists to prevent this.

---

## 2. RegTech Sub-Sectors

```
┌────────────────────────────────────────────────────────────────────┐
│                       REGTECH ECOSYSTEM                           │
├──────────────────┬───────────────────┬────────────────────────────┤
│ Regulatory       │ KYC / AML /       │ Regulatory                 │
│ Intelligence     │ Financial Crime   │ Reporting                  │
├──────────────────┼───────────────────┼────────────────────────────┤
│ Cube             │ ComplyAdvantage   │ Regnology                  │
│ Ascent RegTech   │ NICE Actimize     │ Wolters Kluwer             │
│ Reg-Room         │ Refinitiv W-Check │ Axiom SL                   │
│ Corlytics        │ LexisNexis Risk   │ VERMEG                     │
├──────────────────┼───────────────────┼────────────────────────────┤
│ Risk Management  │ Trade Surveillance│ Policy & Audit             │
│ & Governance     │ & Market Abuse    │ Management                 │
├──────────────────┼───────────────────┼────────────────────────────┤
│ MetricStream     │ Nasdaq Surveillance│ ServiceNow GRC            │
│ LogicGate        │ Behavox           │ OneTrust                   │
│ Riskonnect       │ Eventus Systems   │ SAP GRC                    │
└──────────────────┴───────────────────┴────────────────────────────┘
```

---

## 3. Core Domain Concepts

### 3.1 The Regulatory Hierarchy

```
GLOBAL
  ↓
  G20 / BCBS / IOSCO / FATF
  (Sets global standards and principles)
  ↓
REGIONAL
  ↓
  EU (ESMA, EBA, EIOPA) | US (SEC, CFTC, Fed) | UK (FCA, PRA)
  (Translates global principles into regional rules)
  ↓
NATIONAL / LOCAL REGULATOR
  ↓
  FCA (UK) | BaFin (Germany) | FINRA (US) | MAS (Singapore) | ASIC (Australia)
  (Issues specific rules, guidance, supervisory expectations)
  ↓
FINANCIAL INSTITUTION
  ↓
  Interprets rules, builds policies, implements controls
  ↓
REGTECH PLATFORM
  ↓
  Tracks, maps, monitors, reports compliance with those controls
```

### 3.2 Key Regulatory Frameworks to Know

| Framework | Full Name | What It Covers |
|---|---|---|
| **MiFID II** | Markets in Financial Instruments Directive II | EU trade reporting, investor protection |
| **EMIR** | European Market Infrastructure Regulation | Derivatives reporting and clearing |
| **GDPR** | General Data Protection Regulation | EU data privacy |
| **DORA** | Digital Operational Resilience Act | EU cyber/operational resilience for finance |
| **Basel III / IV** | Basel Committee standards | Bank capital adequacy and risk |
| **Dodd-Frank** | US Wall Street Reform Act | US derivatives, swaps, systemic risk |
| **FATCA** | Foreign Account Tax Compliance Act | US tax evasion via foreign accounts |
| **AML Directive (AMLD)** | EU Anti-Money Laundering | EU-wide AML requirements |
| **PSD2 / PSD3** | Payment Services Directive | EU open banking, payment regulation |
| **SOX** | Sarbanes-Oxley Act | US public company financial reporting |
| **SFDR** | Sustainable Finance Disclosure Regulation | ESG reporting requirements |
| **CSRD** | Corporate Sustainability Reporting Directive | EU sustainability disclosures |

### 3.3 Compliance Lifecycle

```
HORIZON SCANNING
  Monitor upcoming regulations before they take effect
  → "What's changing in the next 6-18 months?"
       ↓
IMPACT ASSESSMENT
  Determine how a new rule affects the business
  → "Which of our processes, products, or teams are affected?"
       ↓
POLICY MAPPING
  Map external rule to internal policy/control
  → "Rule says X, our Policy 42.B says the same — linked"
       ↓
CONTROL IMPLEMENTATION
  Build or update controls to comply
  → "New trade reporting field required — update report format"
       ↓
TESTING & VALIDATION
  Verify compliance controls work
  → "Are we actually reporting what the rule requires?"
       ↓
MONITORING & AUDIT
  Ongoing checks that controls continue to work
  → "Daily monitoring, periodic internal audit"
       ↓
REGULATORY REPORTING
  Submit required reports to regulator
  → MiFID II transaction reports, EMIR trade reports
```

### 3.4 Three Lines of Defence Model

The standard risk management framework banks use:

```
1st LINE: Business / Front Office
  → Owns and manages risk day-to-day
  → Traders, relationship managers, product teams
  → Primary responsibility for compliance

2nd LINE: Risk & Compliance Function
  → Sets standards, monitors 1st line, reports exceptions
  → Compliance team, risk managers
  → RegTech tools used heavily here

3rd LINE: Internal Audit
  → Independent assurance that 1st and 2nd lines work
  → Reviews processes, tests controls
  → Audit management tools used here
```

---

## 4. Regulatory Intelligence Deep Dive — Cube Style

### 4.1 What Cube Does

**Cube** is a leading regulatory intelligence platform. It automates the tracking and management of regulatory change globally — so banks don't have to manually monitor hundreds of regulators across dozens of countries.

```
CUBE'S CORE PRODUCT:
  Regulatory Universe  → Complete library of all regulations globally
  Change Monitoring    → Detects regulatory updates in near-real time
  Rule Mapping         → Links regulation to internal policies and obligations
  Workflow             → Assigns regulatory changes to correct teams
  Analytics            → Reports on compliance posture
  API Access           → Clients can consume regulatory data in their own systems
```

### 4.2 Regulatory Change Management Flow

```
REGULATOR (e.g., FCA) publishes new guidance
          ↓
Cube's content team / AI captures the change
          ↓
Change classified:
  Jurisdiction: UK
  Regulator: FCA
  Topic: Consumer Duty, AML, Capital Requirements
  Effective Date: 2026-09-01
  Impact Level: High / Medium / Low
          ↓
Change appears in client's Cube dashboard
          ↓
Client compliance officer:
  Reviews change → Assesses impact → Assigns to business owner → Sets deadline
          ↓
Business owner:
  Updates internal policy / control → Marks complete
          ↓
Audit trail: every action recorded with user + timestamp
```

### 4.3 Obligations Management

**Obligations** are the specific things a company must do to comply with a regulation:

```
Regulation: MiFID II, Article 26 — Transaction Reporting
Obligation: "Report all transactions in financial instruments to national regulator
             by end of business day following the transaction"

Broken into granular requirements:
  ✓ Report must contain 65 fields
  ✓ Submitted to: ESMA / National CA (e.g., FCA)
  ✓ Within: T+1 (next business day)
  ✓ Format: ISO 20022 XML
  ✓ Rejection must be resubmitted within 24 hours

SDET relevance:
  Testing that obligation data is:
  ✓ Correctly extracted from the regulation text
  ✓ Mapped to correct internal control
  ✓ Assigned to correct team/owner
  ✓ Effective date captured accurately
  ✓ Change in effective date propagated correctly
```

### 4.4 Policy Management

```
POLICY HIERARCHY:
  Regulatory Rule (External)
          ↓
  Group Policy (Internal, top-level)
          ↓
  Procedure (How to implement the policy)
          ↓
  Control (Specific action that proves compliance)
          ↓
  Evidence (Proof that control was performed)

MAPPINGS TO TEST:
  One regulation → many obligations
  One obligation → many policies
  One policy     → many controls
  One control    → one or more pieces of evidence

SDET: Test that adding a new rule correctly creates obligations
      and that mappings persist through system updates
```

---

## 5. KYC & AML Deep Dive

### 5.1 KYC — Know Your Customer

Before a financial institution serves a client, they must verify who that client is:

```
KYC COMPONENTS:
  ✦ Identity Verification   → Government ID check (passport, driving licence)
  ✦ Address Verification    → Proof of address (utility bill, bank statement)
  ✦ PEP Screening           → Is the client a Politically Exposed Person?
  ✦ Sanctions Screening     → Is the client on a sanctions list?
  ✦ Adverse Media           → Any negative news about the client?
  ✦ Beneficial Ownership    → Who ultimately owns/controls the entity?
  ✦ Source of Wealth / Funds→ Where did the money come from?

KYC TYPES:
  Standard CDD    → Regular customers, normal risk
  Enhanced DD     → High-risk customers (PEPs, high-value, certain jurisdictions)
  Simplified DD   → Low-risk (regulated financial institutions as clients)

KYC RENEWAL:
  KYC must be periodically refreshed:
  Low risk:    Every 3-5 years
  Medium risk: Every 2-3 years
  High risk:   Annually or more often
```

### 5.2 AML — Anti-Money Laundering

**Money laundering** is the process of making illegally obtained money appear legitimate. There are three stages:

```
PLACEMENT   → Dirty money enters the financial system
               E.g., depositing cash in small amounts (structuring)

LAYERING    → Complex transactions obscure the origin
               E.g., multiple wire transfers, shell companies, crypto

INTEGRATION → Laundered money re-enters the economy as "clean"
               E.g., buying real estate, luxury goods, investments

AML CONTROLS:
  Transaction Monitoring  → Alerts on suspicious patterns
  SAR Filing              → Suspicious Activity Report to regulator
  Currency Transaction    → Report cash transactions > $10,000 (US: CTR)
  OFAC Screening          → Screen transactions against US Treasury sanctions
  Travel Rule             → Crypto: must include sender/receiver info > $3,000
```

### 5.3 Sanctions Screening

```
SANCTIONS LISTS (Global):
  OFAC (US)    → Office of Foreign Assets Control — SDN List
  UN           → United Nations consolidated sanctions list
  EU           → European Union consolidated list
  UK           → OFSI sanctions list (Office of Financial Sanctions Implementation)
  HMT          → UK His Majesty's Treasury

WHAT'S SCREENED:
  ✦ Customer names → at onboarding and on list updates
  ✦ Transaction counterparties → every payment
  ✦ Countries → OFAC-sanctioned countries (Cuba, Iran, North Korea, Russia*)
  ✦ Entities → Sanctioned companies, vessels, aircraft

MATCHING:
  Exact match     → Easy but misses spelling variations
  Fuzzy match     → Catches "Muhammad Ali" vs "Mohammed Ali"
  Phonetic match  → Sounds like the same name
  Transliteration → Arabic/Cyrillic names translated to Latin

SDET CRITICAL TESTS:
  ✓ Name on sanctions list → correctly blocked, alert generated
  ✓ Name removed from list → block lifted on next screen
  ✓ Fuzzy match: "Vladmir" matches "Vladimir" (typo)
  ✓ Transliteration: Arabic name matches Latin equivalent
  ✓ False positive rate: common names (John Smith) not blocked unfairly
  ✓ Alert generated within X seconds of match
  ✓ SAR workflow triggered when match confirmed
```

### 5.4 Transaction Monitoring

```
HOW IT WORKS:
  Every transaction runs through rules engine:
  
  Rule examples:
  ✦ Cash deposit > $9,900 (structuring / just under $10K report threshold)
  ✦ Multiple small transactions to same account in 24 hours
  ✦ Wire to high-risk jurisdiction (Iran, North Korea) any amount
  ✦ Rapid movement: funds in → out within 24 hours (layering)
  ✦ Transaction inconsistent with customer profile
     (Student account receiving $50,000 wire)

ALERT TRIAGE:
  Alert generated → Analyst reviews → True positive / False positive
  True positive → SAR filed with FinCEN (US) / NCA (UK)
  False positive → Alert dismissed with reason (audit logged)

SDET TESTS:
  ✓ Rule fires on exact threshold amount
  ✓ Rule does NOT fire below threshold
  ✓ Alert contains all required fields (amount, parties, rule triggered)
  ✓ Analyst notes saved and auditable
  ✓ SAR generated with correct FinCEN format
  ✓ Duplicate transactions don't generate duplicate alerts
```

---

## 6. Regulatory Reporting Deep Dive

### 6.1 MiFID II Transaction Reporting

One of the most complex reporting regimes in finance:

```
WHO:     All investment firms in the EU/UK
WHAT:    Every transaction in financial instruments (stocks, bonds, derivatives)
WHEN:    T+1 (by end of next business day)
WHERE:   Sent to national regulator via ARM (Approved Reporting Mechanism)
HOW:     ISO 20022 XML format

65 MANDATORY FIELDS include:
  Field 1:  Transaction Reference Number (unique per report)
  Field 2:  Trading venue (MIC code, e.g., XLON for LSE)
  Field 4:  Instrument ID (ISIN)
  Field 7:  Buyer LEI (Legal Entity Identifier)
  Field 9:  Seller LEI
  Field 28: Price
  Field 30: Quantity
  Field 32: Trade Date/Time (UTC, microsecond precision)
  Field 36: Execution venue
  Field 65: Transmission of order indicator

LEI (Legal Entity Identifier):
  20-character alphanumeric code identifying legal entities globally
  E.g.: 549300OL514RA0SXJJ46 (Barclays Bank PLC)
  SDET: Validate LEI format, check LEI is not lapsed/expired
```

### 6.2 EMIR Trade Reporting

```
WHO:    Counterparties to OTC derivatives (swaps, forwards, options)
WHAT:   All derivative trades reported
WHEN:   T+1
WHERE:  Trade Repository (e.g., DTCC, REGIS-TR, CME TR)
FORMAT: XML/CSV per TR requirements

KEY FIELDS:
  UTI (Unique Trade Identifier) — must be agreed between both counterparties
  UPI (Unique Product Identifier) — identifies derivative type
  Notional Amount, Currency
  Maturity Date
  Counterparty 1 & 2 LEIs

SDET tests:
  ✓ UTI generated in correct format (per ESMA standards)
  ✓ UTI agreed between counterparties before reporting
  ✓ Report submitted within T+1 deadline
  ✓ Modification event: amending a reported trade sends correct "MODI" action
  ✓ Cancellation: cancelled trade sends "EROR" or "TERM" action
```

### 6.3 Audit Trail Requirements

All regulated activities must have an immutable audit log:

```
WHAT MUST BE LOGGED:
  ✦ Who did what, when (user ID, action, timestamp)
  ✦ All order activity (entry, modification, cancellation)
  ✦ All client communications (MiFID II: 5-year retention)
  ✦ Compliance decisions (SAR filings, KYC approvals)
  ✦ System access (logins, permission changes)
  ✦ Data changes (who modified what field, old vs new value)

REQUIREMENTS:
  Immutable:  Cannot be altered or deleted (WORM storage)
  Timestamped: UTC, accurate to at least second (microseconds for trading)
  Retained:   MiFID II = 5 years; AML = 5-7 years; GDPR = minimum necessary

SDET tests:
  ✓ Every action generates a log entry
  ✓ Log entries contain: user, action, timestamp, IP, before/after values
  ✓ Logs cannot be edited or deleted (test via direct DB attempt)
  ✓ Logs queryable for audit review
  ✓ Retention policy: old logs archived, not deleted
```

---

## 7. Key Players & Products

| Company | Sector | What They Do |
|---|---|---|
| **Cube** | Reg Intelligence | Automated regulatory change management |
| **Ascent RegTech** | Reg Intelligence | AI-driven obligations management |
| **ComplyAdvantage** | KYC/AML | AI-powered sanctions + AML screening |
| **NICE Actimize** | AML / Surveillance | Transaction monitoring, trade surveillance |
| **Refinitiv World-Check** | KYC / Screening | PEP and sanctions database (LSEG) |
| **LexisNexis Risk Solutions** | KYC / Fraud | Risk data and screening |
| **Behavox** | Conduct / Surveillance | AI behaviour analytics for compliance |
| **Nasdaq Surveillance** | Trade Surveillance | Market manipulation detection |
| **Regnology** | Reg Reporting | Regulatory report generation |
| **Wolters Kluwer FRR** | Reg Reporting | Finance reporting solutions |
| **MetricStream** | GRC | Governance, Risk, Compliance platform |
| **OneTrust** | Privacy / GRC | GDPR, data privacy management |
| **ServiceNow GRC** | GRC | Integrated risk and compliance |
| **Eventus Systems** | Trade Surveillance | Futures and equities surveillance |
| **Chainalysis** | Crypto AML | Blockchain transaction monitoring |

---

## 8. SDET Testing Guide for RegTech

### 8.1 Regulatory Content Testing

```
Testing the rules database:
  ✓ New regulation ingested → classified with correct: 
      Jurisdiction, Regulator, Topic, Effective Date
  ✓ Updated regulation → change correctly applied; version history retained
  ✓ Repealed regulation → removed from active rules; archived
  ✓ Effective date change → obligation deadlines updated
  ✓ Multi-jurisdiction rule → appears under all relevant jurisdictions

Content accuracy (critical):
  ✓ Regulation text matches official source verbatim
  ✓ Links to official regulatory documents are live and correct
  ✓ Translation accuracy for non-English regulations
  ✓ Summary/interpretation flagged as interpretation (not official text)
```

### 8.2 Rule Mapping & Obligations Testing

```
Mapping logic:
  ✓ New obligation created → auto-mapped to relevant internal policy
  ✓ Mapping change logged with: who made it, when, reason
  ✓ Orphaned obligation (no policy mapped) → flagged in dashboard
  ✓ Policy deleted → mapped obligations flagged as unmapped

Workflow:
  ✓ Regulatory change assigned to correct business unit
  ✓ Deadline date calculated correctly from effective date
  ✓ Escalation triggers if deadline approaches without action
  ✓ Approval workflow: reviewer → approver → complete
  ✓ Rejected task returns to assignee with comments

Notification:
  ✓ Email notification when assigned regulatory change
  ✓ Reminder 7 days before deadline
  ✓ Overdue notification on deadline day
  ✓ Manager notified on overdue after 48 hours
```

### 8.3 KYC / Screening Testing

```
Identity verification:
  ✓ Valid passport → approved
  ✓ Expired passport → rejected with correct error
  ✓ Passport data extracted correctly (name, DOB, expiry)
  ✓ Document tamper detection works
  ✓ Selfie liveness check passes for real person
  ✓ Selfie check fails for printed photo

Sanctions screening:
  ✓ SDN list match → blocked, alert generated
  ✓ Fuzzy match within threshold → alert for manual review
  ✓ False positive cleared → audit log records who, why, when
  ✓ PEP match → automatically triggers Enhanced Due Diligence
  ✓ Sanctions list update (new name added) → re-screen all existing clients

Performance:
  ✓ Single name screen: < 2 seconds
  ✓ Batch screen 10,000 names: completes within SLA
  ✓ System handles simultaneous screen requests at transaction volume
```

### 8.4 Transaction Monitoring Testing

```
Rule engine tests (parameterised for each rule):
  Rule: Flag transactions > $10,000 cash
    ✓ $10,001 cash deposit → alert generated
    ✓ $10,000.00 exact → alert generated (boundary — at or above)
    ✓ $9,999.99 → no alert
    ✓ $10,001 non-cash → no alert (rule is cash-only)

  Rule: Structuring — multiple cash deposits same day totalling > $10,000
    ✓ 3 deposits of $3,500 same day = $10,500 → alert
    ✓ 2 deposits of $4,900 same day = $9,800 → alert (below $10K but suspicious)
    ✓ Deposits on different days → no structuring alert

Alert management:
  ✓ Alert appears in analyst queue within 60 seconds of trigger
  ✓ Alert contains all required data (customer, amount, account, rule)
  ✓ Analyst can add notes, escalate, or close
  ✓ All alert actions logged with timestamp
  ✓ Closed alert with reason: reason recorded and searchable

SAR filing:
  ✓ SAR generated with all required FinCEN/NCA fields
  ✓ SAR submitted to correct authority (US vs UK vs EU)
  ✓ SAR confirmation (reference number) stored in system
  ✓ Tipping off prevention: customer NOT notified of SAR
```

### 8.5 Regulatory Reporting Testing

```
MiFID II report tests:
  ✓ All 65 required fields present in report
  ✓ LEI format valid (20 alphanumeric chars)
  ✓ ISIN format valid (12 chars, prefix = country code)
  ✓ Timestamps in UTC, ISO 8601 format
  ✓ Price in correct decimal format
  ✓ Submission to ARM before T+1 deadline
  ✓ Rejected report → re-submission within 24 hours
  ✓ Duplicate report detection (same UTI submitted twice)

Audit trail tests:
  ✓ Every user action creates immutable log entry
  ✓ Attempt to edit/delete log entry → blocked, attempt itself logged
  ✓ Log contains: timestamp (UTC), user ID, action type, before/after
  ✓ Logs retained for required period (5+ years)
  ✓ Logs searchable by date range, user, action type
```

### 8.6 Data Privacy Testing (GDPR)

```
Right to Access:
  ✓ User requests their data → report generated within 30 days
  ✓ Report contains all personal data held

Right to Erasure:
  ✓ Deletion request → PII deleted from all systems
  ✓ Audit log entry retained (deletion event itself logged)
  ✓ Retention override: if legally required to keep data, erasure blocked
    with reason (e.g., AML requires 5-year retention)

Data Minimisation:
  ✓ Only required fields collected (not extra personal data)
  ✓ Consent recorded with timestamp and scope

PII in non-prod environments:
  ✓ Real names/SSNs/account numbers masked in test/dev environments
  ✓ Synthetic test data used for functional testing
```

---

## 9. Tech Stack in RegTech

| Technology | Usage |
|---|---|
| **Python / Java** | Rules engines, data processing pipelines |
| **NLP / AI (spaCy, BERT)** | Extracting obligations from regulatory text |
| **React / Angular** | Compliance dashboards and workflow UIs |
| **PostgreSQL / Oracle** | Regulatory content database, audit logs |
| **Elasticsearch** | Full-text search across regulatory library |
| **Kafka** | Event streaming for transaction monitoring |
| **AWS / Azure** | Cloud hosting; Azure popular in finance sector |
| **WORM Storage (S3 Object Lock)** | Immutable audit trail storage |
| **REST APIs** | Integration with client compliance systems |
| **ISO 20022 / XML** | Regulatory report formats |
| **SFTP / AS2** | Secure file transfer for regulatory submissions |
| **OAuth2 / SAML** | Enterprise SSO integration |
| **Docker / Kubernetes** | Container orchestration |

---

## 10. Global Regulators Reference

| Region | Regulator | Abbreviation | Focus |
|---|---|---|---|
| **US** | Securities and Exchange Commission | SEC | Securities |
| **US** | Commodity Futures Trading Commission | CFTC | Derivatives |
| **US** | Financial Industry Regulatory Authority | FINRA | Broker-dealers |
| **US** | Financial Crimes Enforcement Network | FinCEN | AML/SAR |
| **US** | Office of Foreign Assets Control | OFAC | Sanctions |
| **EU** | European Securities and Markets Authority | ESMA | Capital markets |
| **EU** | European Banking Authority | EBA | Banking |
| **UK** | Financial Conduct Authority | FCA | All financial services |
| **UK** | Prudential Regulation Authority | PRA | Banks, insurers |
| **UK** | Office of Financial Sanctions Implementation | OFSI | Sanctions |
| **Singapore** | Monetary Authority of Singapore | MAS | All financial services |
| **Australia** | Australian Securities and Investments Commission | ASIC | Securities |
| **Hong Kong** | Securities and Futures Commission | SFC | Securities |
| **Switzerland** | Swiss Financial Market Supervisory Authority | FINMA | All financial |
| **Germany** | Bundesanstalt für Finanzdienstleistungsaufsicht | BaFin | All financial |

---

## 11. Glossary

| Term | Definition |
|---|---|
| **RegTech** | Regulatory Technology — compliance through automation |
| **GRC** | Governance, Risk & Compliance — broad compliance framework |
| **KYC** | Know Your Customer — identity verification before onboarding |
| **AML** | Anti-Money Laundering — detecting and preventing money laundering |
| **CDD** | Customer Due Diligence — the process of verifying customer identity and risk |
| **EDD** | Enhanced Due Diligence — deeper checks for high-risk customers |
| **PEP** | Politically Exposed Person — politician, official, or their family |
| **SAR** | Suspicious Activity Report — filed with regulator when crime suspected |
| **CTR** | Currency Transaction Report — filed for cash transactions > $10,000 |
| **SDN** | Specially Designated Nationals — OFAC sanctions list |
| **LEI** | Legal Entity Identifier — 20-char code for legal entities globally |
| **ISIN** | International Securities Identification Number — 12-char security ID |
| **UTI** | Unique Trade Identifier — ID for a derivative trade in EMIR reporting |
| **UPI** | Unique Product Identifier — classifies derivative product type |
| **ARM** | Approved Reporting Mechanism — MiFID II report submission channel |
| **TR** | Trade Repository — entity receiving EMIR derivative reports |
| **WORM** | Write Once Read Many — immutable storage for audit logs |
| **Horizon Scanning** | Monitoring upcoming regulatory changes before they are effective |
| **Obligations** | Specific actions a firm must take to comply with a regulation |
| **Policy Mapping** | Linking external rule to internal policy or control |
| **Tipping Off** | Illegally warning a customer that they've been reported (SAR) |
| **False Positive** | An AML alert triggered for a legitimate transaction |
| **MiFID II** | EU markets regulation covering trade reporting and investor protection |
| **EMIR** | EU regulation on derivatives reporting and central clearing |
| **GDPR** | EU data protection regulation |
| **DORA** | EU digital operational resilience act for financial entities |
| **Dodd-Frank** | US financial reform law (post-2008 crisis) |
| **FATCA** | US law requiring foreign banks to report US account holders |
| **FATF** | Financial Action Task Force — global AML standards body |
| **FinCEN** | US financial intelligence unit — receives SARs |
| **NCA** | National Crime Agency (UK) — receives SARs in the UK |

---

*RegTech Domain Guide for SDETs | Regulatory Technology & Compliance*
*Last updated: July 2026*
