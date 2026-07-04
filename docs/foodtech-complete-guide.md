# Food Service & Supply Chain Technology Guide for SDETs
### Sysco Labs, B2B Commerce & Food Distribution Technology

---

## Table of Contents
1. [What Is Food Service Technology?](#1-what-is-food-service-technology)
2. [Sysco Corporation & Sysco Labs](#2-sysco-corporation--sysco-labs)
3. [Core Domain Concepts](#3-core-domain-concepts)
4. [B2B E-Commerce in Food Service](#4-b2b-e-commerce-in-food-service)
5. [Supply Chain & Logistics Deep Dive](#5-supply-chain--logistics-deep-dive)
6. [Key Platform Areas](#6-key-platform-areas)
7. [SDET Testing Guide](#7-sdet-testing-guide)
8. [Tech Stack](#8-tech-stack)
9. [Regulatory & Compliance](#9-regulatory--compliance)
10. [Glossary](#10-glossary)

---

## 1. What Is Food Service Technology?

**Food Service Technology** is the digital infrastructure that powers the foodservice industry — from food manufacturers and distributors to restaurants, hotels, hospitals, and schools. It covers B2B ordering, supply chain management, delivery logistics, inventory management, menu planning, and business analytics.

```
THE FOODSERVICE CHAIN:

MANUFACTURER / PRODUCER
  (Farms, factories: Tyson, Kraft Heinz, Sysco's own brands)
          ↓
BROADLINE DISTRIBUTOR
  (Warehouses, trucks: Sysco, US Foods, Performance Food Group)
          ↓
OPERATOR / CUSTOMER
  (Restaurants, hotels, hospitals, schools, caterers)
          ↓
END CONSUMER
  (The person eating the food)

WHERE TECHNOLOGY FITS:
  ✦ B2B ordering portal (restaurant orders from Sysco online)
  ✦ Route planning (delivery truck routes optimised)
  ✦ Warehouse management (pick, pack, ship from cold storage)
  ✦ Inventory management (stock levels across warehouses)
  ✦ Demand forecasting (predict what to stock, when)
  ✦ Menu & recipe tools (help chefs build profitable menus)
  ✦ Business analytics (help restaurants understand their costs)
```

**Scale:** Sysco Corporation alone serves ~700,000 customers, operates ~330 distribution facilities, and delivers ~1.5 billion cases of product annually. That scale demands sophisticated technology.

---

## 2. Sysco Corporation & Sysco Labs

### 2.1 Sysco Corporation — The Business

**Sysco** is the world's largest foodservice distributor. Understanding the business is essential to testing its technology.

```
SYSCO AT A GLANCE:
  Founded:        1969, Houston, Texas
  Headquarters:   Houston, Texas, USA
  Revenue:        ~$76 billion (FY2024)
  Employees:      ~72,000 globally
  Customers:      ~700,000 (restaurants, healthcare, education, hospitality)
  Facilities:     ~330 distribution centres globally
  Fleet:          ~10,000 delivery vehicles
  Products:       ~400,000 SKUs (products)
  Markets:        US, Canada, UK, Ireland, France, Sweden, Mexico, and more

WHAT SYSCO SELLS:
  Fresh produce, meat, seafood, dairy, frozen foods, dry goods,
  beverages, paper goods, cleaning supplies, kitchen equipment
  — essentially everything a commercial kitchen needs.

CUSTOMER SEGMENTS:
  ✦ Restaurants        (~60% of revenue) — from fast food to fine dining
  ✦ Healthcare         — hospitals, nursing homes, cafeterias
  ✦ Education          — school cafeterias, university dining
  ✦ Hospitality        — hotels, resorts, casinos
  ✦ Government         — military bases, correctional facilities
  ✦ Retail             — small grocery, convenience stores
```

### 2.2 Sysco Labs — The Technology Arm

**Sysco Labs** is Sysco's technology innovation centre, headquartered in **Colombo, Sri Lanka** 🇱🇰, with additional presence in the US.

```
SYSCO LABS AT A GLANCE:
  Location:        Colombo, Sri Lanka (+ US)
  Role:            Builds digital products for Sysco globally
  Teams:           Engineering, Product, Design, QA/SDET, Data Science
  Products built:  Sysco Shop, Sysco Driver App, Sysco Analytics,
                   Supply chain tools, CRM tools, Menu cost tools

WHY SRI LANKA?
  Sysco Labs was established to leverage Sri Lanka's strong
  software engineering talent at global quality standards.
  It is one of the most significant tech employers in Colombo.

WHAT SYSCO LABS BUILDS:
  ✦ Sysco Shop        → B2B e-commerce ordering platform for customers
  ✦ Delivery apps     → Driver routing and proof-of-delivery apps
  ✦ Warehouse systems → Warehouse management and picking tools
  ✦ Analytics         → Business intelligence for Sysco and its customers
  ✦ CRM tools         → Salesforce integrations for Sysco's sales team
  ✦ Menu tools        → Recipe costing, menu planning for restaurant clients
  ✦ Mobile apps       → iOS + Android for customers and internal teams
```

---

## 3. Core Domain Concepts

### 3.1 The Distributor Business Model

```
HOW SYSCO MAKES MONEY:
  Buy products from manufacturers → Store in warehouses → Sell to restaurants

  Margin = Selling Price to Customer - Cost of Product - Distribution Cost

  Key metrics:
  ✦ Case volume         → How many cases delivered (primary volume metric)
  ✦ Gross profit per case → Margin made on each unit
  ✦ Penetration         → % of customer's total spend going through Sysco
  ✦ Customer retention  → Keeping customers from switching to US Foods, etc.

PRICING MODEL:
  Cost-plus pricing:
    Product cost: $10.00
    Markup (%):   +18%
    Sell price:   $11.80 to restaurant

  Contract pricing:
    Large customers negotiate fixed prices on key items
    Prices in system must match contracted amounts exactly
    SDET: Price displayed in ordering system = contracted price (critical)
```

### 3.2 Products, SKUs & Catalogue

```
SKU (Stock Keeping Unit):
  A unique identifier for every product in the catalogue
  Each SKU represents: brand + product + size + pack format

  Example:
    SKU: 4321987
    Description: Sysco Classic Chicken Breast, Boneless Skinless, IQF
    Pack: 4 × 5 lb bags (20 lbs per case)
    Price: $42.50/case
    Brand: Sysco Classic (Sysco's own label)
    Category: Poultry > Chicken > Breast

SYSCO BRAND TIERS:
  Sysco Classic    → Value tier — competitive quality, lower price
  Sysco Imperial   → Premium tier — top quality ingredients
  Sysco Natural    → Clean label, natural/organic products
  Sysco Brand      → Standard everyday products

CATALOGUE COMPLEXITY:
  ~400,000 SKUs across categories:
  Fresh → short shelf life, temperature-controlled
  Frozen → long shelf life, frozen storage
  Dry → ambient, non-perishable
  Non-food → paper goods, chemicals, smallwares

  SDET: Catalogue search must return relevant results;
        filter by category, brand, pack size must work correctly
```

### 3.3 Customer (Operator) Concepts

```
ACCOUNT HIERARCHY:
  Parent Account (Restaurant Group / Chain)
    ↓ Child Account (Individual location / restaurant)
      ↓ Ship-to Location (Delivery address)

Example:
  Parent: McDonald's Southeast Region
    Child: McDonald's Store #1042 (Atlanta)
      Ship-to: 123 Peachtree St, Atlanta, GA

CUSTOMER TYPES:
  Independent (indie)   → Single-location restaurant (highest priority for Sysco)
  Chain / Multi-unit    → Same concept across multiple locations
  Healthcare            → Hospital, nursing home (regulated menu requirements)
  B&I (Business & Industry) → Corporate cafeterias, employee dining
  Education             → Schools, universities (USDA meal requirements)

DELIVERY SCHEDULES:
  Each customer has agreed delivery days (e.g., Monday, Wednesday, Friday)
  Order cutoff time: typically midnight or 6am before delivery day
  Minimum order: some accounts have minimum case/dollar requirements
  SDET: Orders placed after cutoff → pushed to next delivery date
```

### 3.4 Ordering Concepts

```
ORDER TYPES:
  Regular Order      → Scheduled delivery on agreed day
  Will Call          → Customer picks up from warehouse (rare)
  Drop Ship          → Manufacturer delivers direct to customer
  Emergency Order    → Outside normal schedule (surcharge often applies)
  Standing Order     → Auto-reorder same items each week

ORDER STATUS FLOW:
  Draft → Submitted → Confirmed → Picking → Loaded → Out for Delivery
       → Delivered → Invoiced → Paid

CUTOFF TIME:
  Orders must be placed by a specific time to make the next delivery
  E.g., Order by 11:59 PM Monday → Delivered Tuesday
  After cutoff → system pushes to next available delivery date
  SDET: Cutoff enforcement is critical — test edge cases around exact cutoff time

SUBSTITUTIONS:
  If an item is out of stock, Sysco may substitute with similar product
  Customer can allow or disallow substitutions
  Driver/delivery note must clearly communicate substitution
  SDET: Substituted item must be priced correctly, not at original item price
```

### 3.5 Inventory & Warehouse Concepts

```
WAREHOUSE ZONES:
  Dry Storage:    Ambient temperature, non-perishables
  Cooler:         35-38°F / 2-4°C (dairy, produce, deli)
  Freezer:        -10°F to 0°F / -23°C to -18°C (frozen foods)
  Chemical:       Cleaning supplies, segregated from food
  Each zone has different picking sequences and vehicle requirements

PICK TYPES:
  Full Case Pick    → Entire case selected from location
  Split Case Pick   → Partial case (some customers order by each, not case)

INVENTORY METRICS:
  Days on Hand (DOH)    → Inventory value ÷ average daily usage
  Shrinkage             → Inventory lost to damage, theft, spoilage
  FIFO                  → First In First Out — older stock shipped first
  FEFO                  → First Expired First Out — prioritise shorter shelf life
  Reorder Point         → Trigger to order more stock
  Safety Stock          → Buffer inventory to prevent stockouts

COLD CHAIN:
  Critical concept — perishable products must be maintained at correct
  temperature throughout the supply chain. A temperature break
  (warm truck, delayed delivery) can make products unsafe and unusable.
```

---

## 4. B2B E-Commerce in Food Service

### 4.1 Sysco Shop — B2B Ordering Platform

Sysco Shop is the digital ordering platform where restaurant operators place their orders. Think of it as Amazon, but for commercial kitchens and B2B pricing.

```
CORE FEATURES:
  ✦ Product search and browse by category
  ✦ Customer-specific pricing (contracted prices per account)
  ✦ Order guides — curated lists of products each customer regularly buys
  ✦ Reorder from history
  ✦ Delivery date selection (within available schedule)
  ✦ Order tracking (where is my delivery?)
  ✦ Invoice and payment history
  ✦ Nutritional and allergen information per product
  ✦ Product images, specifications, pack details
  ✦ Mobile app (iOS and Android)
```

### 4.2 Order Guide

The single most important feature for customer experience in B2B food ordering:

```
WHAT IS AN ORDER GUIDE?
  A personalised list of products a specific customer regularly orders.
  Instead of searching 400,000 SKUs every time, they see their
  usual 50-200 products and simply update quantities.

  Example order guide entry:
  ┌────────────────────────────────────────────────────────┐
  │ Sysco Classic Chicken Breast 20lb   SKU: 4321987       │
  │ Last ordered: 3 cases | Price: $42.50/case             │
  │ In stock: ✓ | Qty: [___] cases                         │
  └────────────────────────────────────────────────────────┘

ORDER GUIDE TYPES:
  Assigned guide:   Sysco's sales rep creates this for the customer
  Custom guide:     Customer builds their own list
  Hybrid:           Core assigned + customer additions

SDET critical tests:
  ✓ Customer A's guide does not show items from Customer B's guide
  ✓ Price in guide = customer's contracted price (not list price)
  ✓ Out-of-stock item flagged in guide with alternative suggested
  ✓ Discontinued item removed from guide with notification
  ✓ Guide loads fast even for large guides (200+ items)
```

### 4.3 Pricing Engine

Pricing is the most business-critical component to test accurately:

```
PRICING LAYERS:
  List Price      → Base price for all customers (starting point)
  Contract Price  → Negotiated price for specific customer
  Promotional     → Temporary price reduction (manufacturer-funded)
  Volume Rebate   → Discount earned after buying a certain volume
  Exception Price → One-off override set by sales rep

PRICE DETERMINATION ORDER:
  Exception Price (highest priority)
  → Contract Price
  → Promotional Price
  → List Price (lowest priority, default)

SURCHARGES:
  Fuel surcharge:     Added when fuel costs are high
  Small order fee:    Below minimum order value
  Delivery distance:  Remote locations may have surcharge
  Refrigerated items: Additional handling fee sometimes

SDET PRICING TESTS (most critical in entire system):
  ✓ Customer sees their contracted price, never list price
  ✓ Promo price applied within correct date range only
  ✓ Promo price expires → reverts to contract price (not list price)
  ✓ Volume rebate accumulates correctly across orders
  ✓ Price on order confirmation = price on invoice (no discrepancy)
  ✓ Price change mid-order → customer notified before confirmation
  ✓ Multiple pricing rules → correct priority order applied
```

---

## 5. Supply Chain & Logistics Deep Dive

### 5.1 Demand Forecasting

```
WHY IT MATTERS:
  Sysco must predict how much of each product to stock before
  customers order. Over-stock = waste + storage cost.
  Under-stock = lost sales + unhappy customers.

FORECASTING INPUTS:
  ✦ Historical sales by SKU, by region, by season
  ✦ Weather forecasts (BBQ products spike in summer)
  ✦ Holiday calendar (Thanksgiving → turkey demand spike)
  ✦ Local events (Super Bowl → wings and beer demand)
  ✦ Customer growth trends
  ✦ Promotions planned

SDET relevance:
  ✓ Forecast numbers feed replenishment system correctly
  ✓ Seasonal uplift factors applied to correct date range
  ✓ New product added to forecast correctly (no history → ML estimated)
  ✓ Discontinued product removed from forecast
```

### 5.2 Route Planning & Delivery Optimisation

```
ROUTE PLANNING PROBLEM:
  Each warehouse has 30-100 trucks, each serving 15-25 customers per day.
  Goal: Minimise total distance driven while meeting all time windows.
  This is the classic "Vehicle Routing Problem" (VRP) in operations research.

CONSTRAINTS:
  ✦ Customer time windows  → "Deliver between 6am and 10am only"
  ✦ Truck capacity         → Maximum weight and volume per truck
  ✦ Temperature zones      → Frozen and fresh on same truck require split
  ✦ Driver hours           → Max driving hours per shift
  ✦ Traffic patterns       → Peak hours avoided
  ✦ Delivery priority      → High-value or time-sensitive first
  ✦ Vehicle type           → Not all trucks can access all locations

ROUTE OPTIMISATION OUTPUTS:
  ✦ Stop sequence for each truck
  ✦ Estimated arrival time per stop
  ✦ Load manifest (what goes on each truck)
  ✦ Driver instructions

SDET tests:
  ✓ Generated route respects all customer time windows
  ✓ Truck load does not exceed weight/volume limits
  ✓ Frozen and fresh products correctly separated
  ✓ ETA shown to customer updates when driver deviates
  ✓ Route regenerated correctly if stop added/removed last minute
```

### 5.3 Driver App & Proof of Delivery

```
DRIVER WORKFLOW:
  Log in to driver app → View today's route → Depart warehouse
          ↓
  Navigate to first stop → Arrive
          ↓
  Offload products → Customer signs delivery on app (or e-POD)
          ↓
  Record exceptions:
    Short delivery (item out of stock, not loaded)
    Refused delivery (customer not available)
    Damaged goods (photographed)
    Returns (customer returning unused product)
          ↓
  Move to next stop → Repeat
          ↓
  Return to warehouse → End of day summary submitted

PROOF OF DELIVERY (POD):
  Electronic signature captured on driver tablet
  Geo-tagged with GPS coordinates (proves delivery location)
  Timestamped (proves delivery time)
  Photo of delivery location (optional, for unattended drops)

SDET tests:
  ✓ GPS location recorded at signature time (within 50m accuracy)
  ✓ Signature captured correctly and non-repudiable
  ✓ Short delivery recorded → invoice adjusted automatically
  ✓ Return recorded → credit memo generated
  ✓ Delivery exception photo uploads correctly with metadata
  ✓ Offline capability: app works without data signal, syncs on reconnect
  ✓ ETA pushed to customer app when driver is 2 stops away
```

### 5.4 Warehouse Management System (WMS)

```
WMS KEY FUNCTIONS:
  ✦ Receiving:       Inbound product from supplier, check quantity/quality
  ✦ Put-away:        Assign product to correct warehouse location
  ✦ Slotting:        Optimise where products are stored (fast-movers near door)
  ✦ Picking:         Assemble customer orders from storage locations
  ✦ Packing:         Stage picked items for loading onto truck
  ✦ Loading:         Load truck in reverse stop-order (last stop = load first)
  ✦ Shipping:        Generate manifest, dispatch truck

PICKING METHODS:
  Single order pick  → One order picked at a time
  Batch picking      → One picker handles multiple orders simultaneously
  Zone picking       → Different pickers handle different warehouse zones
  Voice picking      → Audio instructions guide pickers (hands-free)
  RF scanning        → Barcode scanner confirms correct product picked

SDET tests:
  ✓ Pick instruction routes picker efficiently (shortest path)
  ✓ Wrong scan (wrong product) → immediate rejection alert
  ✓ Quantity picked matches order quantity
  ✓ FEFO enforced: shorter-shelf-life product picked first
  ✓ Substitution: if picking reveals out-of-stock, substitution offered
  ✓ Truck loading sequence: last stop loaded first
```

---

## 6. Key Platform Areas

### 6.1 Sysco Analytics & Business Intelligence

```
WHAT IT PROVIDES:

For Sysco internally:
  ✦ Sales performance by rep, region, product category
  ✦ Customer churn risk predictions
  ✦ Inventory turnover and slow-moving product reports
  ✦ Delivery performance (on-time %, exceptions, damages)
  ✦ Profitability by customer and product

For restaurant customers (Sysco Periscope / Market Insights):
  ✦ "How does your food cost compare to similar restaurants?"
  ✦ Spend analysis by category (protein, produce, dairy)
  ✦ Price trend analysis for planning
  ✦ Product performance (what's selling vs. not selling)
  ✦ Sustainability metrics (waste, carbon footprint)
```

### 6.2 Menu & Recipe Tools

```
MENU ENGINEERING:
  Sysco provides tools to help restaurant owners build profitable menus.
  
  Recipe Costing:
    Ingredients listed per recipe → costs pulled from Sysco catalogue
    Total recipe cost calculated → portion cost derived
    Menu price suggestion based on target food cost %
    
    Example:
      Chicken Alfredo Pasta (serves 1):
        Chicken breast:  4 oz @ $2.12/lb = $0.53
        Pasta:           3 oz @ $0.45/lb = $0.08
        Alfredo sauce:   4 oz @ $1.20/lb = $0.30
        Total cost:      $0.91
        Target food cost: 28%
        Suggested price: $3.25 (but goes on menu at $18.95)
    
  SDET tests:
    ✓ Recipe cost recalculates automatically when product price changes
    ✓ Yield percentage applied correctly (chicken breast loses 15% weight when cooked)
    ✓ Unit conversion: ordered in cases, recipe uses ounces
    ✓ Multi-serving recipe: cost-per-portion mathematically correct
```

### 6.3 CRM & Sales Force Tools

```
SALES REPRESENTATIVE WORKFLOW:
  Sysco has thousands of field sales reps visiting restaurant customers.
  Their CRM tools (often Salesforce-integrated) cover:

  ✦ Customer visit logging (who visited, when, what was discussed)
  ✦ Lead management (prospects being converted)
  ✦ Account portfolio (all customers assigned to this rep)
  ✦ Opportunity tracking (large contract bids)
  ✦ Product recommendations (AI-based cross-sell suggestions)
  ✦ Customer health score (risk of churn)
  ✦ Sample and product demo tracking

SDET tests:
  ✓ Visit log saves with correct customer, date, rep, notes
  ✓ AI recommendation based on customer purchase history is relevant
  ✓ Customer health score updates when spending drops
  ✓ Notification to rep when assigned customer hasn't ordered in 14 days
```

---

## 7. SDET Testing Guide

### 7.1 B2B Ordering Platform Tests

#### A. Product Search & Catalogue

```
Search accuracy:
  ✓ "chicken breast" → returns relevant chicken breast products
  ✓ SKU number search → returns exact product
  ✓ Brand filter → only Sysco Imperial products shown
  ✓ Category filter → only "Fresh Poultry" products shown
  ✓ Search "chiken" (typo) → returns chicken results (fuzzy search)
  ✓ Discontinued product → not in search results; "no longer available"

Product detail page:
  ✓ Price displayed = customer's contracted price
  ✓ Pack size shown correctly (e.g., "4 × 5 lb bags")
  ✓ Allergen information accurate (contains: gluten, dairy, nuts)
  ✓ Nutritional info per serving accurate
  ✓ Stock availability shown correctly ("In Stock" / "Low Stock" / "Out of Stock")
  ✓ Estimated delivery date shown based on cutoff and schedule
```

#### B. Order Placement & Cutoff Logic

```
Cutoff time testing (most critical):
  Setup: Customer cutoff = midnight Tuesday for Wednesday delivery

  ✓ Order placed Monday 11:59 PM → delivers Wednesday
  ✓ Order placed Tuesday 12:00 AM → delivers Wednesday (on the dot)
  ✓ Order placed Tuesday 12:01 AM → pushed to NEXT available delivery
  ✓ Cutoff timer on UI counts down correctly
  ✓ System time used: server UTC time, not customer's browser time

Order modification after submission:
  ✓ Before cutoff: customer can modify quantities
  ✓ After cutoff: order locked; modification requires customer service
  ✓ Cancellation: before cutoff only; after cutoff requires CS

Min order validation:
  ✓ Order below minimum → warning shown, cannot submit
  ✓ Minimum met after adding item → warning removed
  ✓ Minimum displayed clearly during ordering
```

#### C. Pricing Validation

```
These tests should run as a matrix against multiple customers and scenarios:

  ✓ Customer with contract price: sees contract price, not list price
  ✓ Customer with promotion: promotion price applied within date range
  ✓ Day after promo ends: reverts to contract price
  ✓ Customer without contract: sees list price
  ✓ Exception price: overrides all other prices
  ✓ Fuel surcharge: shown as separate line item, not baked into price
  ✓ Invoice total matches order confirmation total exactly
  ✓ Tax calculated correctly (tax-exempt customers not charged tax)
```

#### D. Order Guide Tests

```
  ✓ Order guide loads all customer's usual products
  ✓ Products sorted by category consistently
  ✓ Previous order quantity shown as reference
  ✓ Out-of-stock item in guide: flagged with alternative
  ✓ Seasonal item (not available in winter): removed with note
  ✓ Quick add quantity: pressing "+" increments by 1 case
  ✓ Guide search filters to matching items only
  ✓ Adding new item to guide saves permanently for future orders
  ✓ Guide does not show items not available in customer's region
```

### 7.2 Driver App & Delivery Tests

```
Route and navigation:
  ✓ Route loads before driver leaves warehouse
  ✓ All stops shown in correct sequence
  ✓ Navigation updates if traffic re-routes driver
  ✓ Stop arrival detected within 100m of customer address

Delivery completion:
  ✓ Each item scanned before offload (scan to confirm)
  ✓ Short delivery: missing item logged, quantity adjusted
  ✓ Customer signature captured and stored
  ✓ GPS coordinates recorded at delivery time
  ✓ Signature timestamp in server time (UTC)
  ✓ Completed delivery syncs to back-end within 2 minutes

Offline mode (critical — many warehouses and routes have poor signal):
  ✓ App works fully without internet connection
  ✓ All deliveries completed offline synced when signal restored
  ✓ No data lost during sync
  ✓ Duplicate POD not created on resync
```

### 7.3 Inventory & Warehouse Tests

```
Stock level accuracy:
  ✓ Product ordered → available stock decremented in real-time
  ✓ Product received from supplier → stock incremented correctly
  ✓ Stock count override: cycle count updated correctly
  ✓ Negative stock: system flags, does not allow to go below zero without alert

FEFO / FIFO compliance:
  ✓ Product with expiry 15 Aug appears before product with expiry 30 Aug
  ✓ Picker directed to correct slot for first-expiring product
  ✓ Scanning wrong slot (later expiry) → rejection with reason

Temperature breach simulation:
  ✓ Freezer temp reading > 0°F → alert generated immediately
  ✓ Alert escalates to warehouse manager if not acknowledged in 15 min
  ✓ Products in breached zone flagged for quality review
```

### 7.4 Integration Testing

```
Key integrations to test in Sysco ecosystem:

Integration              What to validate
────────────────────────────────────────────────────────
ERP (SAP)            → Order confirmed → financial record created in SAP
WMS                  → Order submitted → pick task created in WMS
TMS (Route Planning) → Order confirmed → stop added to relevant route
Customer portal      → Invoice generated → visible in portal within 1 hour
EDI (850/810/856)    → Chain customer orders via EDI processed correctly
Salesforce CRM       → Customer order triggers sales rep notification
Analytics platform   → Order data flows to BI within reporting window
Supplier portal      → Purchase order sent → supplier acknowledges
```

### 7.5 Data Integrity & Reconciliation Tests

```
Financial reconciliation:
  ✓ Sum of all invoices = sum of all order totals (no missing invoices)
  ✓ Credits (returns) match physical return records
  ✓ Cash collected by drivers matches system receipts
  ✓ End-of-day report balances to individual transactions

Inventory reconciliation:
  ✓ Units shipped (per delivery records) = units deducted from inventory
  ✓ Units received (per inbound records) = units added to inventory
  ✓ Physical count vs. system count variance within tolerance
```

---

## 8. Tech Stack

| Technology | Usage in Sysco Labs |
|---|---|
| **React / Next.js** | Sysco Shop web ordering platform |
| **React Native / Flutter** | Driver app, customer mobile app |
| **Java / Spring Boot** | Core order management microservices |
| **Python** | Demand forecasting, pricing ML models |
| **Node.js** | API gateway, real-time services |
| **SAP** | Enterprise ERP (finance, procurement) |
| **Salesforce** | CRM for sales representatives |
| **PostgreSQL** | Transactional data (orders, accounts, pricing) |
| **Apache Kafka** | Real-time order events, delivery status streaming |
| **Elasticsearch** | Product catalogue search (400K+ SKUs) |
| **Redis** | Session management, pricing cache |
| **AWS** | Cloud infrastructure (Sysco is heavily AWS) |
| **Snowflake / Redshift** | Data warehouse for analytics |
| **Tableau / Power BI** | Business intelligence dashboards |
| **Google Maps / HERE** | Routing and navigation |
| **EDI (X12 850/810/856)** | B2B order/invoice exchange with chain customers |
| **Docker / Kubernetes** | Container orchestration |
| **Jenkins / GitHub Actions** | CI/CD pipelines |
| **Selenium / Appium** | UI test automation |
| **JMeter / Gatling** | Performance and load testing |

---

## 9. Regulatory & Compliance

### Food Safety & Quality Standards

| Regulation | What It Covers |
|---|---|
| **FSMA** | Food Safety Modernization Act — US food safety regulation |
| **HACCP** | Hazard Analysis Critical Control Points — food safety process |
| **FDA Food Code** | US standards for food handling and storage temperatures |
| **USDA** | Meat, poultry, egg product regulation and inspection |
| **GFSI** | Global Food Safety Initiative — certification standard |
| **SQF** | Safe Quality Food — GFSI-recognised certification |
| **BRC** | British Retail Consortium standard — global quality benchmark |
| **Allergen Labelling** | FDA: 9 major allergens must be declared (FALCPA) |
| **Country of Origin** | Must disclose where produce and meats originate |

### Traceability — Critical Regulatory Requirement

```
FDA RULE 204 (FSMA Traceability):
  For high-risk foods (leafy greens, tomatoes, fresh herbs, seafood, etc.)
  Sysco must be able to trace: WHERE did this product come from?
  And: WHO received this product?

TRACEABILITY CHAIN:
  Farm → Processor → Sysco warehouse → Restaurant → Consumer

  If a contamination event occurs (e.g., E. coli outbreak in romaine lettuce):
  FDA can mandate recall. Sysco must identify:
    ✓ Every case of affected product received (from which supplier, which lot)
    ✓ Every customer who received that product
    ✓ All within 24 hours

SDET TESTS:
  ✓ Lot number captured on every inbound receipt
  ✓ Lot number tracked through pick, ship, delivery records
  ✓ Recall query: "Show all customers who received Lot #ABC123" — correct results
  ✓ Traceability data retained for minimum 2 years (FSMA Rule 204)
```

### Temperature Compliance

```
COLD CHAIN REQUIREMENTS:
  Frozen:   0°F / -18°C or below at all times
  Cooler:   35-40°F / 2-4°C
  Fresh meat: 41°F / 5°C or below

SDET: Temperature breach → alert must fire
  ✓ Temperature sensor reading recorded every 15 minutes
  ✓ Data stored for minimum 1 year (audit requirement)
  ✓ If delivery truck temp breached during route → flagged for QA review
  ✓ Customer may refuse delivery if temperature out of range
```

---

## 10. Glossary

| Term | Definition |
|---|---|
| **SKU** | Stock Keeping Unit — unique product identifier |
| **Case** | Standard unit of ordering (e.g., 4 × 5 lb bags = 1 case) |
| **Each** | Individual unit within a case (split case ordering) |
| **Order Guide** | Curated list of a customer's regularly ordered products |
| **Cutoff Time** | Deadline to submit order for next scheduled delivery |
| **POD** | Proof of Delivery — electronic signature confirming receipt |
| **Short Delivery** | Item on order but not delivered (out of stock at loading) |
| **WMS** | Warehouse Management System |
| **TMS** | Transportation Management System — route planning tool |
| **ERP** | Enterprise Resource Planning (SAP — finance and operations) |
| **EDI** | Electronic Data Interchange — B2B document exchange standard |
| **850** | EDI Purchase Order document type |
| **810** | EDI Invoice document type |
| **856** | EDI Advance Ship Notice (ASN) document type |
| **VRP** | Vehicle Routing Problem — logistics optimisation challenge |
| **FEFO** | First Expired First Out — stock rotation method |
| **FIFO** | First In First Out — stock rotation method |
| **DOH** | Days on Hand — how many days of inventory is in stock |
| **HACCP** | Hazard Analysis Critical Control Points — food safety system |
| **FSMA** | Food Safety Modernization Act (US FDA) |
| **Cold Chain** | Temperature-controlled supply chain from origin to customer |
| **Broadline** | Full-line food distributor (stocks everything) |
| **Operator** | Sysco's term for a restaurant/foodservice customer |
| **Penetration** | % of a customer's total food spend going through Sysco |
| **CAO** | Computer-Assisted Ordering — auto-replenishment system |
| **Demand Forecasting** | Predicting future demand to plan inventory levels |
| **Shrinkage** | Inventory lost to damage, theft, spoilage, or errors |
| **Safety Stock** | Buffer inventory held to prevent stockouts |
| **Cross-dock** | Product transferred directly from inbound to outbound without storage |
| **Slotting** | Assigning optimal storage location for each product in warehouse |
| **MHE** | Material Handling Equipment (forklifts, pallet jacks, conveyors) |
| **Last Mile** | Final delivery leg from distribution centre to customer |
| **Food Cost %** | Food cost as a % of menu price (restaurant's key metric) |
| **Yield** | Usable portion after preparation (e.g., chicken loses 15% weight when cooked) |
| **Contract Pricing** | Negotiated product prices for specific customers |
| **Lot Number** | Batch identifier for traceability and recall purposes |
| **Allergen** | Food ingredient causing allergic reactions (peanuts, gluten, dairy, etc.) |

---

*Food Service & Supply Chain Technology Guide for SDETs | Sysco Labs & B2B Commerce*
*Last updated: July 2026*
