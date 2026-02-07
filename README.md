# Arcadian Data — Business + Data Context (for AI + Humans)

This repository exists to support analytics, reporting, automation, and operational decision-making for **Arcadian Outfitters LLC**.

If you’re an AI assistant (Claude/ChatGPT), treat this README as the **source of truth** for business context, definitions, and how to interpret datasets in this repo.

---

## 1) Company Overview

**Arcadian Outfitters** crafts premium **state-pride + lifestyle headwear** and installs **small, high-margin hat displays** in convenience and grocery stores.

**Tagline:** Love Where You Live  
**Mission:** We craft goods that help people feel proud of where they’re from and connected to the places and beliefs that shape them.  
**Vision:** Build a nationwide culture of pride, connection, and belonging through apparel that celebrates every community—becoming the most trusted brand in regional identity through meaning, craftsmanship, and retailer partnerships.

**Origin / Heritage (important for brand voice):**
- The Howerton family has ~45+ years in hats/custom apparel.
- Arcadian’s roots come through a legacy of quality, integrity, and retailer-first partnership.

---

## 2) Core Business Model (How We Make Money)

### What we sell
- **Hats** sold B2B to retailers (common pack size: **8 hats per sleeve**).
- **Compact hat displays** placed in-store to drive impulse purchases and maximize profit per square foot.

### Where we sell
Primary channels:
- Convenience stores (c-stores)
- Grocery stores

Additional channels (when they fit):
- Hardware, farm supply, tourist stops, gift shops, travel plazas, outdoor outfitters, etc.

### Why retailers say “yes”
- **Impulse item** near checkout / high-traffic zones
- **High margin** compared to typical c-store categories
- **Low maintenance** and no spoilage/expiration
- **Small footprint**, high ROI

---

## 3) Merchandising + Account Ownership Workflow (Critical)

Arcadian’s operating model separates **selling** from **servicing**:

1. **Sales rep opens the account**
   - Prospect, pitch, place the display, secure initial order
   - Capture clear before/after photos (countable per peg)

2. **Hand-off to 3PM merchandiser** (third-party merchandising)
   - 3PM keeps the stand tidy, updated, and documented with photos/notes
   - Goal: keep displays spotless and selling without rep needing to be there

3. **Rep remains accountable**
   - Rep reviews 3PM visit reports in the 3PM portal and in Arcadian’s ordering system
   - Rep places reorders “on the store’s behalf” based on visit photos + sell-through

4. **Relationship maintenance**
   - Rep personally visits each account **twice per year** (minimum) for relationship + performance check

**Data implication:** A “visit” record may be created by 3PM, but “account ownership” remains with the rep who opened it.

---

## 4) Pricing Model (Required for margin + reporting)

Typical reference price points:
- **Wholesale:** ~$12 per hat (ex: $96 per sleeve of 8)
- **MAP (Minimum Advertised Price):** $20 (retailers should not advertise below this)
- **MSRP (Suggested Retail):** $30

Retailer gross margin examples:
- At $20: ~$8/hat (40%)
- At $30: ~$18/hat (60%)

**Data implication:** In reporting, distinguish:
- Wholesale revenue (Arcadian revenue)
- Retail price (store price) if captured (often not captured)

---

## 5) Sales Rep Compensation (If used in analytics)

- **20% commission** on all revenue from new accounts opened (initial set)
- **10% commission** on reorders from those accounts
- **Guaranteed sales policy:** if a store receives a **credit memo/return**, the related amount is deducted from commission for that period
- Commissions are paid after customer payment is received and returns/credits are reconciled

**Data implication:** Commission reports must account for:
- Payment status / cash application timing
- Credits/returns tied to original invoices/orders

---

## 6) The “Units” of the Business (Entities to Know)

These are the key objects you’ll see repeatedly across datasets:

### Store / Customer (Retail Account)
A retail location Arcadian sells into (c-store, grocery, etc.).  
May have multiple identifiers across systems (NetSuite, Shopify, 3PM).

### Sales Rep
The person who opened the account and owns the relationship.

### Display
The physical stand in a store. One store may have 0, 1, or multiple displays.

### Visit
A servicing event (often by 3PM) that includes photos, notes, and a restock outcome.

### Order / Invoice
Wholesale transaction from Arcadian to the retailer.

### Credit Memo / Return
Offsets revenue and affects commissions and “true” account performance.

---

## 7) Systems + Data Sources (Where the truth lives)

Common systems (may change over time):
- **NetSuite**: ERP / financial truth (invoices, payments, credits, customers)
- **Shopify**: website ordering + customer account UX (integration may exist)
- **3PM Portal**: merchandising visits, photos, service notes, “restock authorized” signals
- **Internal files**: visitation lists, master customer file exports, exception trackers

**Rule of thumb for analytics:**
- Financial truth = NetSuite (revenue, credits, payments)
- Servicing truth = 3PM (visits, photos, merchandising outcomes)
- Customer experience truth = Shopify (if/when used for ordering + account history)

---

## 8) ID Strategy (IMPORTANT — avoid broken joins)

**Problem you may see:** “Internal IDs” can change across exports, migrations, or transfers.

**Repository standard:**
- Prefer a stable **Arcadian Customer Key** for joining datasets.
- If the source system ID isn’t stable, create a deterministic key using:
  - normalized customer name + ship-to address + city + state + zip (and/or store number if present)
  - then store the mapping in a crosswalk table

### Recommended crosswalk table
`/reference/customer_id_crosswalk.csv`
- `arcadian_customer_key` (stable primary key used in this repo)
- `netsuite_customer_internal_id`
- `shopify_customer_id`
- `3pm_location_id`
- `customer_name`
- `ship_to_address`, `city`, `state`, `zip`
- `created_at`, `last_verified_at`

**Instruction for AI:** if joins don’t match, DO NOT guess—use the crosswalk or build one.

---

## 9) Suggested Repo Structure (if you want it standardized)

