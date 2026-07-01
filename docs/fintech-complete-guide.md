# The Complete Fintech Domain Guide for SDETs
### From Zero to Interview-Ready — A Practical Reference

---

## Table of Contents

1. [What Is Fintech?](#1-what-is-fintech)
2. [Capital Markets — The Foundation](#2-capital-markets--the-foundation)
3. [Financial Instruments Deep Dive](#3-financial-instruments-deep-dive)
4. [Market Structure & Microstructure](#4-market-structure--microstructure)
5. [Order Lifecycle — How a Trade Really Works](#5-order-lifecycle--how-a-trade-really-works)
6. [Trading Platforms & Technology](#6-trading-platforms--technology)
7. [Risk Management](#7-risk-management)
8. [Regulatory Environment](#8-regulatory-environment)
9. [FIX Protocol — The Language of Trading](#9-fix-protocol--the-language-of-trading)
10. [SDET in Fintech — The Complete Testing Guide](#10-sdet-in-fintech--the-complete-testing-guide)
11. [Tech Stack in Fintech](#11-tech-stack-in-fintech)
12. [Key Metrics & Numbers to Know](#12-key-metrics--numbers-to-know)
13. [Glossary — Quick Reference](#13-glossary--quick-reference)
14. [LSEG — London Stock Exchange Group Deep Dive](#14-lseg--london-stock-exchange-group-deep-dive)

---

## 1. What Is Fintech?

**Fintech (Financial Technology)** is the use of software and technology to deliver financial services faster, cheaper, and more efficiently than traditional banking. It covers a broad spectrum:

| Fintech Sector | What It Does | Examples |
|---|---|---|
| **Trading Platforms** | Software to execute trades | NinjaTrader, MetaTrader, Thinkorswim |
| **Digital Banking** | App-based banking | Revolut, Chime, N26 |
| **Payments** | Moving money digitally | Stripe, PayPal, Square |
| **InsurTech** | Technology-driven insurance | Lemonade, Root |
| **RegTech** | Compliance via automation | Chainalysis, ComplyAdvantage |
| **WealthTech** | Robo-advisors, portfolio tools | Betterment, Wealthfront |
| **Blockchain/Crypto** | Decentralized finance | Coinbase, Binance |

> **Your Focus:** Trading Platform Fintech — specifically futures and forex technology, where NinjaTrader operates.

---

## 2. Capital Markets — The Foundation

### What Are Capital Markets?
Markets where **buyers and sellers trade financial assets** — stocks, bonds, currencies, and derivatives. They allow businesses to raise capital and investors to grow wealth.

### Two Sides of the Market

```
PRIMARY MARKET                        SECONDARY MARKET
(New securities issued)               (Existing securities traded)

Company → Issues Shares (IPO)         Investor A → Sells to Investor B
Government → Issues Bonds             Happens on exchanges (NYSE, CME)
Money flows to the issuer             Money flows between investors
```

### Major Global Exchanges

| Exchange | Location | What Trades There |
|---|---|---|
| **NYSE** | New York | Stocks |
| **NASDAQ** | New York (electronic) | Tech stocks, ETFs |
| **CME Group** | Chicago | Futures, Options |
| **CBOE** | Chicago | Options, Volatility |
| **ICE** | Atlanta | Energy, FX futures |
| **LSE** | London | Stocks, Bonds |
| **Euronext** | Amsterdam | Pan-European stocks |

> NinjaTrader users primarily trade on **CME Group** — the world's largest futures exchange.

### Market Sessions (US Futures — Your Domain)

```
Sunday 5:00 PM CT  → Market Opens (Globex/Electronic)
Friday 4:00 PM CT  → Market Closes

Regular Trading Hours (RTH): 8:30 AM – 3:00 PM CT
Extended Hours (ETH):        Overnight + pre/post market

Key times to know as a tester:
- Market Open  (8:30 AM CT) → Highest volatility, most test risk
- Market Close (3:00 PM CT) → Settlement, P&L calculations run
- Overnight    (ETH)        → Low liquidity, different behavior
```

---

## 3. Financial Instruments Deep Dive

### 3.1 Stocks (Equities)
- Represent **ownership** in a company
- Price driven by company performance, sentiment, economy
- Key concepts: Dividends, Earnings Per Share (EPS), Market Cap
- **Test relevance:** Price feeds, corporate action handling (splits, dividends)

### 3.2 Bonds (Fixed Income)
- A **loan to a government or company** in exchange for interest (coupon)
- Safer than stocks; lower return
- Price moves **inversely** to interest rates (important concept)
- Types: Government bonds (Treasuries), Corporate bonds, Municipal bonds
- **Test relevance:** Yield calculations, coupon payment schedules

### 3.3 Futures ⭐ (Core for NinjaTrader)
A legally binding contract to **buy or sell an asset at a predetermined price on a future date**.

```
Example:
  Today (July):     You agree to buy 1 contract of Gold at $2,000/oz in October
  In October:       Gold price is $2,100. You profit $100/oz (× contract size)
  Alternatively:    Gold is $1,900. You lose $100/oz
```

**Why futures exist:**
- **Hedging** — A farmer locks in a wheat price to avoid price drops at harvest
- **Speculation** — Traders bet on price direction for profit
- **Price discovery** — Markets set fair prices in real time

**Key futures contracts (NinjaTrader users trade these daily):**

| Ticker | Name | Underlying Asset | Tick Size | Tick Value |
|---|---|---|---|---|
| **ES** | E-mini S&P 500 | S&P 500 Index | 0.25 | $12.50 |
| **NQ** | E-mini NASDAQ-100 | NASDAQ-100 Index | 0.25 | $5.00 |
| **CL** | Crude Oil | WTI Crude Oil | 0.01 | $10.00 |
| **GC** | Gold | Gold (troy oz) | 0.10 | $10.00 |
| **ZB** | 30-Year T-Bond | US Treasury Bond | 1/32 | $31.25 |
| **6E** | Euro FX | EUR/USD | 0.0001 | $12.50 |

**Contract Specs Matter for Testing:**
```
ES Futures:
  Contract Size:   $50 × S&P 500 Index value
  Expiry Months:   March (H), June (M), September (U), December (Z)
  Expiry Code:     ESU26 = ES, September (U), 2026
  Trading Hours:   Nearly 23 hours/day
  Last Trading:    Third Friday of expiry month
```

**Contract Rollover:**
When a contract nears expiry, traders move ("roll") to the next contract. This is a critical period for testing — charts must switch correctly, historical data must align, and no orders should remain on the expired contract.

### 3.4 Options
The **right, but not the obligation**, to buy or sell an asset at a set price before expiry.

```
Call Option  = Right to BUY  (you think price goes UP)
Put Option   = Right to SELL (you think price goes DOWN)

Strike Price = The agreed price
Premium      = Cost of buying the option
Expiry Date  = When the right expires
```

**The Greeks (Risk measures for options):**

| Greek | Measures | Simple Meaning |
|---|---|---|
| **Delta** | Price sensitivity | How much option moves per $1 move in asset |
| **Gamma** | Delta's rate of change | How fast delta changes |
| **Theta** | Time decay | How much value is lost per day |
| **Vega** | Volatility sensitivity | How much value changes with volatility |
| **Rho** | Interest rate sensitivity | Effect of rate changes |

> As an SDET, you'd test that Greeks are calculated accurately in real time.

### 3.5 Forex (Foreign Exchange)
Trading **currency pairs** — the world's largest and most liquid market ($7+ trillion/day).

```
Major Pairs (USD involved):   EUR/USD, GBP/USD, USD/JPY, USD/CHF
Cross Pairs (no USD):         EUR/GBP, EUR/JPY
Exotic Pairs:                 USD/TRY, USD/ZAR

How to read EUR/USD = 1.0850:
  1 Euro = 1.0850 US Dollars
  Base currency (EUR) / Quote currency (USD)

PIP = Smallest price movement. For EUR/USD, 1 pip = 0.0001
```

### 3.6 ETFs (Exchange Traded Funds)
Baskets of assets (like stocks) that trade on an exchange like a single stock. Example: SPY tracks the S&P 500 index.

### 3.7 CFDs (Contracts for Difference)
Agreement to exchange the **difference in price** of an asset between open and close. You never own the underlying asset. Popular in Europe; restricted in the US.

---

## 4. Market Structure & Microstructure

### 4.1 The Order Book (DOM — Depth of Market)
The real-time record of all **buy and sell orders** waiting at different price levels.

```
SELL SIDE (ASKS / OFFERS)
Price     | Volume
2,050.25  | 150      ← Lowest Ask (Best Ask)
2,050.50  | 300
2,050.75  | 220
──────────────────── SPREAD
2,050.00  | 180      ← Highest Bid (Best Bid)
2,049.75  | 400
2,049.50  | 250
BUY SIDE (BIDS)

Spread = 2,050.25 - 2,050.00 = 0.25 (1 tick for ES)
```

> NinjaTrader's **SuperDOM** is its flagship DOM tool. Knowing this deeply = big interview points.

### 4.2 Market Participants

| Participant | Role | Behavior |
|---|---|---|
| **Retail Traders** | Individual traders | Use platforms like NinjaTrader |
| **Market Makers** | Provide liquidity | Always quote bid and ask, profit from spread |
| **Institutional Traders** | Hedge funds, banks | Large order sizes, market-moving |
| **High-Frequency Traders (HFT)** | Algorithmic speed traders | Millisecond execution, massive volume |
| **Brokers** | Intermediaries | Route orders from traders to exchanges |
| **Exchanges** | Matching engines | CME, NYSE — match buyers and sellers |

### 4.3 Price Action Concepts

**Support & Resistance:**
- Support = price level where buying is strong enough to stop a decline
- Resistance = price level where selling is strong enough to stop a rise

**Moving Averages:**
- SMA (Simple Moving Average) — Average price over N periods
- EMA (Exponential Moving Average) — Weighted, gives more importance to recent prices

**Volume:**
- High volume confirms a price move is real
- Low volume = weak move, likely to reverse
- As a tester: volume data must match exchange data exactly

---

## 5. Order Lifecycle — How a Trade Really Works

This is the most important flow for an SDET to understand and test thoroughly.

```
┌─────────────────────────────────────────────────────────────┐
│                    ORDER LIFECYCLE                          │
└─────────────────────────────────────────────────────────────┘

  Trader Action          Platform               Exchange/Broker
  ─────────────          ────────               ───────────────
  Places Order     →    Validates Order    →    Receives Order
                        (qty, price, acct)
                             ↓
                        Order Status:
                        [PENDING SUBMIT]
                             ↓
                   Sent to Broker/Exchange →    Order Status:
                                               [WORKING]
                                                    ↓
                                          Matching Engine
                                          tries to fill
                                                    ↓
                              ┌──────────────────────────────┐
                              │  FILL SCENARIOS:             │
                              │  Full Fill   → [FILLED]      │
                              │  Partial     → [PART FILLED] │
                              │  No match    → [WORKING]     │
                              │  Cancelled   → [CANCELLED]   │
                              │  Rejected    → [REJECTED]    │
                              └──────────────────────────────┘
                                                    ↓
                             Execution Report sent back
                             to platform → Update P&L,
                             Position, Account Balance
```

### Order States to Test as an SDET

| State | Meaning | Test Scenario |
|---|---|---|
| `PENDING_SUBMIT` | Sent from app, not yet at exchange | Network drop here — what happens? |
| `WORKING` | Live at exchange, waiting for fill | Cancel/modify while working |
| `PARTIALLY_FILLED` | Some quantity filled | Rest of order still at exchange |
| `FILLED` | Fully executed | P&L, position, balance update correctly |
| `CANCELLED` | Removed from exchange | No position created, buying power restored |
| `REJECTED` | Exchange or broker refused | Error displayed correctly to user |
| `CANCEL_PENDING` | Cancel request sent, not confirmed | App handles limbo state |

### Order Types — Full List

```
MARKET ORDER      → Execute immediately at best available price
                    Risk: Slippage in fast markets

LIMIT ORDER       → Execute only at specified price or better
                    Buy Limit = at or BELOW limit price
                    Sell Limit = at or ABOVE limit price

STOP ORDER        → Becomes a market order when price hits stop price
                    Used for stop-loss; risk of slippage

STOP-LIMIT        → Becomes a LIMIT order (not market) at stop price
                    More control, but risk of not filling

MARKET IF TOUCHED → Like a stop, but used to enter (opposite direction)

MIT (MIT)         → Triggers when price touches the level

OCO (One Cancels Other) → Two orders; when one fills, the other cancels
                          E.g., Take Profit + Stop Loss together

Bracket Order     → Entry + automatic Stop Loss + Take Profit
                    NinjaTrader's ATM Strategy is this
```

---

## 6. Trading Platforms & Technology

### 6.1 NinjaTrader Architecture (What You're Testing)

```
┌────────────────────────────────────────────────────────────┐
│                   NINJATRADER PLATFORM                     │
│                                                            │
│  ┌──────────────┐   ┌──────────────┐   ┌───────────────┐  │
│  │   UI Layer   │   │  NinjaScript │   │  Data Engine  │  │
│  │  (Charts,    │   │  Engine (C#) │   │  (Tick/Bar    │  │
│  │   DOM, etc.) │   │  Strategies, │   │   Data Feed)  │  │
│  └──────┬───────┘   │  Indicators) │   └───────┬───────┘  │
│         │           └──────┬───────┘           │          │
│         └──────────────────┴───────────────────┘          │
│                            │                               │
│                    ┌───────▼────────┐                      │
│                    │   Order Server │                      │
│                    └───────┬────────┘                      │
└────────────────────────────┼───────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────▼──────┐ ┌─────▼──────┐ ┌────▼──────┐
       │   Broker    │ │ Market Data│ │  Exchange  │
       │  (Orders)   │ │  Provider  │ │  (CME,etc) │
       └─────────────┘ └────────────┘ └───────────┘
```

### 6.2 NinjaScript
- Built on **C# (.NET Framework)**
- Used to create: Custom Indicators, Automated Strategies, Market Analyzers
- Strategies can run in **backtesting mode** (historical data) or **live mode**
- Key test risk: A strategy behaving differently live vs. in simulation

### 6.3 Market Data Feeds
Platforms receive data from market data providers:

```
Raw Exchange Data (CME DataMine, etc.)
        ↓
Data Vendors (Rithmic, CQG, Continuum/NinjaTrader)
        ↓
Platform (NinjaTrader)
        ↓
Trader's Chart / DOM

Types of data:
  Level 1 (L1) → Best Bid, Best Ask, Last Price, Volume
  Level 2 (L2) → Full order book (all bid/ask levels)
  Time & Sales → Every single trade that occurred (tape)
```

### 6.4 Backtesting
Running a trading strategy against **historical data** to see how it would have performed.

Test challenges:
- Historical data must be complete and accurate (no gaps, no bad ticks)
- Strategy must process bars in strict chronological order
- No "look-ahead bias" (strategy must not see future data)
- Commission and slippage must be factored in correctly

### 6.5 Paper Trading (Simulation Mode)
Simulated trading with fake money. Critical isolation requirements:
- Sim orders must NEVER reach a real exchange
- Sim P&L must be completely separate from real account
- Sim must behave identically to live for testing purposes

---

## 7. Risk Management

### 7.1 Leverage and Margin

```
LEVERAGE:
  Without leverage: $10,000 controls $10,000 of assets
  With 10:1 leverage: $1,000 controls $10,000 of assets

  1% price move:
    Without leverage: $100 gain/loss (1% of $10,000)
    With leverage:    $100 gain/loss (10% of your $1,000)

MARGIN:
  Initial Margin   = Deposit required to OPEN a position
  Maintenance Margin = Minimum to KEEP the position open
  Margin Call      = Broker demands more money when equity < maintenance margin
  Liquidation      = Broker forcibly closes position if margin not met
```

### 7.2 P&L Calculation

```
REALIZED P&L   = Profit/Loss from CLOSED positions
UNREALIZED P&L = Profit/Loss from OPEN positions (mark-to-market)

Example (Long 1 ES contract):
  Bought at:  5,000.00
  Current:    5,010.00
  Difference: 10 points × $50/point = $500 unrealized P&L

  Ticks: 10 points = 40 ticks (ES tick = 0.25)
  Tick value × ticks = $12.50 × 40 = $500 ✓

Daily Settlement (Mark-to-Market):
  Futures P&L is settled DAILY, not when you close
  This is unique to futures vs. stocks
```

### 7.3 Risk Metrics

| Metric | What It Measures |
|---|---|
| **Value at Risk (VaR)** | Maximum expected loss over a time period at a confidence level |
| **Max Drawdown** | Largest peak-to-trough decline in account value |
| **Sharpe Ratio** | Return per unit of risk (higher = better) |
| **Win Rate** | % of trades that are profitable |
| **Profit Factor** | Gross profit ÷ Gross loss (>1.0 means profitable) |
| **Risk/Reward Ratio** | How much you risk vs. how much you aim to gain |

### 7.4 Position Sizing
How many contracts to trade based on account size and risk tolerance.

```
Basic formula:
  Risk per trade = Account × Risk % (e.g., $50,000 × 1% = $500)
  Position Size  = Risk ÷ (Stop Loss in ticks × Tick Value)

Example:
  Risk = $500, Stop = 10 ticks, Tick value = $12.50
  Position Size = $500 ÷ (10 × $12.50) = 4 contracts
```

---

## 8. Regulatory Environment

### US Regulators (Key for NinjaTrader)

| Regulator | Full Name | What They Oversee |
|---|---|---|
| **SEC** | Securities and Exchange Commission | Stocks, bonds, ETFs, public companies |
| **CFTC** | Commodity Futures Trading Commission | Futures, options on futures, swaps |
| **FINRA** | Financial Industry Regulatory Authority | Broker-dealers, registered reps |
| **NFA** | National Futures Association | Futures industry self-regulator |
| **FDIC** | Federal Deposit Insurance Corp | Bank deposits |
| **Federal Reserve** | Central Bank | Interest rates, monetary policy |

> NinjaTrader (as a broker) is registered with the **NFA** and regulated by the **CFTC**.

### Key Compliance Concepts

**Know Your Customer (KYC):**
Verifying the identity of clients before allowing trading. Test: Does the onboarding flow enforce all required document collection?

**Anti-Money Laundering (AML):**
Monitoring for suspicious activity. Automated alerts for unusual trading patterns.

**Best Execution:**
Brokers must ensure clients get the best available price. Test: Are orders routed optimally?

**Audit Trail:**
Every order, modification, and cancellation must be logged with timestamps. Test: Is every state change captured in logs?

**Pattern Day Trader (PDT) Rule:**
US rule: If you make 4+ day trades in 5 days in a margin account under $25,000, you're flagged. Test: Does the platform enforce and track PDT correctly?

**Position Limits:**
Exchanges impose limits on how many contracts a single trader can hold. Test: Are these enforced and does the system reject orders that breach limits?

---

## 9. FIX Protocol — The Language of Trading

### What Is FIX?
**FIX (Financial Information eXchange)** is the standard messaging protocol used across the financial industry to communicate trades, orders, and executions.

Think of it as the **HTTP of trading** — a universal language that brokers, exchanges, and platforms all speak.

### FIX Message Structure

```
Every FIX message is a series of Tag=Value pairs separated by | (SOH character):

8=FIX.4.4|35=D|49=CLIENT|56=BROKER|11=ORDER001|55=ES|54=1|38=1|40=2|44=5000.00|10=123|

Tag Reference:
  8  = BeginString     (FIX version — FIX.4.2, FIX.4.4, FIXT.1.1)
  35 = MsgType         (D=New Order, 8=Execution Report, F=Cancel Request)
  49 = SenderCompID    (Who's sending)
  56 = TargetCompID    (Who's receiving)
  11 = ClOrdID         (Client's unique order ID)
  55 = Symbol          (Instrument — ES, NQ, GC etc.)
  54 = Side            (1=Buy, 2=Sell, 5=Sell Short)
  38 = OrderQty        (Number of contracts)
  40 = OrdType         (1=Market, 2=Limit, 3=Stop, 4=Stop Limit)
  44 = Price           (Limit price)
  10 = CheckSum        (Message integrity check)
```

### Key FIX Message Types

| MsgType | Code | Description |
|---|---|---|
| New Order Single | D | Placing a new order |
| Execution Report | 8 | Fill, reject, cancel confirmation |
| Order Cancel Request | F | Request to cancel an existing order |
| Order Cancel/Replace | G | Modify an existing order |
| Order Status Request | H | Query current order state |
| Market Data Request | V | Subscribe to price data |
| Market Data Snapshot | W | Full order book snapshot |
| Market Data Incremental | X | Real-time order book updates |
| Logon | A | Establish FIX session |
| Heartbeat | 0 | Keep-alive message |
| Logout | 5 | End FIX session |

### SDET Testing of FIX

- Validate correct tag-value pairs in outgoing messages
- Verify Execution Reports update order state correctly
- Test session recovery (reconnect after disconnect)
- Validate sequence numbers (FIX uses sequence numbers; gaps = issue)
- Test heartbeat interval compliance
- Validate CheckSum (Tag 10) calculation

---

## 10. SDET in Fintech — The Complete Testing Guide

### 10.1 Testing Pyramid in Fintech

```
                    ┌─────────────────┐
                    │   E2E Tests     │  ← Full trade flows, user journeys
                    │   (Few, slow)   │
                  ┌─┴─────────────────┴─┐
                  │  Integration Tests   │  ← Order routing, data feeds, FIX
                  │  (Some, medium)      │
                ┌─┴──────────────────────┴─┐
                │     Unit Tests           │  ← P&L calc, margin calc, Greeks
                │     (Many, fast)         │
                └──────────────────────────┘
```

### 10.2 Core Test Areas

#### A. Order Management Testing

Test every order type across all states:

```
Test Matrix Example (Market Order):
  ✓ Buy market order → Full fill
  ✓ Sell market order → Full fill
  ✓ Market order when market closed → Rejected with correct message
  ✓ Market order with insufficient margin → Rejected
  ✓ Market order during fast market (illiquid) → Slippage handled
  ✓ Cancel attempt on filled order → Correct error
  ✓ Duplicate order ID → System handles gracefully
  ✓ Market order → Partial fill → Rest cancelled
```

#### B. Data Feed / Price Feed Testing

```
Validate:
  ✓ Bid/Ask are logically correct (Ask > Bid always)
  ✓ Last price is between bid and ask (or at it)
  ✓ Volume is cumulative and never decreases during session
  ✓ Timestamps are monotonically increasing
  ✓ Data gaps detected and handled (reconnect, backfill)
  ✓ Bad tick filtering (a $0 or astronomically wrong price)
  ✓ Feed failover (primary → backup feed seamlessly)
  ✓ Data matches reference source (CME official data)
```

#### C. P&L and Calculation Testing

This is where **accuracy is non-negotiable** — financial calculations must be exact:

```python
# Example: ES Futures P&L Calculation Test
instrument = "ES"
tick_size = 0.25
tick_value = 12.50
entry_price = 5000.00
exit_price = 5010.00
quantity = 2  # contracts

points = exit_price - entry_price                  # = 10.00
ticks = points / tick_size                         # = 40
pnl = ticks * tick_value * quantity               # = $1,000.00

# Test: Platform P&L matches calculated P&L exactly
assert platform_pnl == pnl  # Must be exact, not approximate
```

#### D. Performance / Latency Testing

Fintech is microsecond-sensitive. Key metrics:

| Metric | Acceptable Range | Critical Threshold |
|---|---|---|
| Order submission latency | < 10ms | > 100ms = issue |
| Market data latency | < 5ms | > 50ms = issue |
| Chart rendering (tick update) | < 16ms (60fps) | > 100ms = noticeable |
| DOM update speed | < 10ms | > 50ms = unusable |

**Tools for performance testing:**
- JMeter, Gatling for load testing
- Custom scripts to measure round-trip time
- Exchange test environments to simulate high-volume sessions

```
Performance Test Scenario:
  "Simulate 10,000 ticks per second on ES
   while 100 concurrent orders are being submitted.
   Assert: No data loss, no order drops, latency < 10ms"
```

#### E. Backtesting Engine Testing

```
Key validation points:
  ✓ Strategy processes bars in correct chronological order
  ✓ No look-ahead bias (strategy can't access future bars)
  ✓ Commission deducted correctly per trade
  ✓ Slippage model applied correctly
  ✓ Results are deterministic (same input = same output, always)
  ✓ Rollover handled correctly in multi-contract backtests
  ✓ Performance metrics (Sharpe, Drawdown) match manual calculation
```

#### F. Market Edge Cases — The Most Important Test Scenarios

These are the scenarios that break trading platforms:

```
MARKET EVENTS TO TEST:
  ┌─────────────────────────────────────────────────────────┐
  │ 1. Market Halt / Trading Suspension                     │
  │    → Orders must be suspended, not lost                 │
  │    → Position calculations frozen correctly             │
  │                                                         │
  │ 2. Circuit Breaker (Limit Up / Limit Down)              │
  │    → Market can't move beyond a daily limit             │
  │    → Orders outside limit should be rejected            │
  │                                                         │
  │ 3. Flash Crash                                          │
  │    → Extreme price spike and recovery                   │
  │    → Bad fills should be handled; cancellation flows    │
  │                                                         │
  │ 4. Contract Rollover                                    │
  │    → Charts switch from ESM26 to ESU26 correctly        │
  │    → No open orders on expired contract                 │
  │    → Historical data continuity maintained              │
  │                                                         │
  │ 5. Market Open (8:30 AM CT)                             │
  │    → Opening bell: high volatility, wide spreads        │
  │    → Order queue built up overnight executes            │
  │    → Platform handles burst of data correctly           │
  │                                                         │
  │ 6. Market Close (3:00 PM CT)                            │
  │    → Settlement prices calculated                       │
  │    → Open futures positions marked-to-market            │
  │    → Daily P&L report generated accurately              │
  │                                                         │
  │ 7. Network Disconnection                                │
  │    → Mid-session disconnect: what happens to orders?    │
  │    → Reconnect: platform syncs state correctly          │
  │    → No ghost orders (orders that platform lost track)  │
  └─────────────────────────────────────────────────────────┘
```

#### G. Security Testing

```
Critical security test areas for trading platforms:
  ✓ Authentication — Multi-factor auth, session timeout
  ✓ Authorization — User can only see/modify own orders
  ✓ Data in transit — All FIX/API traffic encrypted (TLS)
  ✓ Input validation — Prevent injection in order fields
  ✓ Rate limiting — Prevent order flooding attacks
  ✓ Account isolation — Account A cannot affect Account B
  ✓ Audit logging — All actions immutably logged
  ✓ Simulation isolation — Sim trades never reach live markets
```

### 10.3 Automation Framework Considerations for Fintech

```
Recommended Stack:
  Language:     Java / C# / Python
  Framework:    TestNG / JUnit / NUnit / pytest
  API Testing:  REST Assured / Postman / Requests
  Performance:  Gatling / JMeter / k6
  Reporting:    Allure / Extent Reports
  CI/CD:        Jenkins / GitHub Actions / Azure DevOps
  Mocking:      WireMock (for market data simulation)

Fintech-Specific Additions:
  FIX Testing:  QuickFIX/J (open-source FIX engine)
  Time mocking: Ability to simulate specific market times
  Market simulator: Replaying recorded tick data for tests
```

### 10.4 Test Data Management in Fintech

```
Challenges:
  ✗ Cannot use real market data in test (licensing)
  ✗ Cannot use real account data (privacy/regulatory)
  ✗ Markets are live only during trading hours

Solutions:
  ✓ Use CME replay data (historical tick data replayed)
  ✓ Build a market simulator that generates synthetic ticks
  ✓ Use paper trading environment as test environment
  ✓ Anonymize/mask account data for test scenarios
  ✓ Create fixtures for specific market scenarios (halts, gaps)
```

---

## 11. Tech Stack in Fintech

### Common Technologies You'll Encounter

#### Languages
| Language | Usage in Fintech |
|---|---|
| **C#/.NET** | Trading platform UIs, NinjaScript, order management |
| **Java** | Back-end order processing, risk engines, FIX gateways |
| **Python** | Data analysis, backtesting, algo strategies, automation |
| **C++** | Ultra-low latency systems (HFT), exchange matching engines |
| **SQL** | Trade databases, reporting, audit logs |
| **JavaScript** | Web-based trading platforms, dashboards |

#### Databases
| Database | Usage |
|---|---|
| **SQL Server / PostgreSQL** | Trade records, account data, audit logs |
| **TimescaleDB / InfluxDB** | Time-series tick data (optimized for it) |
| **Redis** | Real-time caching (current prices, session state) |
| **KDB+/q** | Industry-standard for financial time series (HFT/banks) |

#### Messaging / Infrastructure
| Technology | Usage |
|---|---|
| **Kafka** | Real-time market data streaming, event pipelines |
| **RabbitMQ** | Order message queuing |
| **FIX Protocol** | Order routing (as above) |
| **WebSockets** | Real-time browser-based price updates |
| **gRPC** | High-performance internal service communication |
| **Docker / Kubernetes** | Container deployment of trading services |
| **AWS / Azure** | Cloud infrastructure for non-latency-sensitive services |

#### Monitoring (Critical in Trading)
| Tool | Usage |
|---|---|
| **Grafana + Prometheus** | Real-time dashboards, latency monitoring |
| **ELK Stack** | Centralized logging (Elasticsearch, Logstash, Kibana) |
| **PagerDuty** | Incident alerting (a latency spike at market open = emergency) |
| **Splunk** | Log analysis and audit trail search |

---

## 12. Key Metrics & Numbers to Know

### Fintech Numbers Every SDET Should Know

| Fact | Detail |
|---|---|
| Futures market hours (US) | ~23 hours/day, 5 days/week |
| CME ES tick size | 0.25 points = $12.50/contract |
| FIX version most used | FIX 4.2, FIX 4.4 |
| NinjaScript language | C# (.NET) |
| Major US futures exchange | CME Group (Chicago) |
| PDT rule minimum equity | $25,000 |
| Futures settlement | Daily mark-to-market |
| Quarterly expiry months | March, June, September, December |
| Average FX daily volume | ~$7.5 trillion/day |
| HFT order speed | Microseconds (millionths of a second) |

---

## 13. Glossary — Quick Reference

| Term | Definition |
|---|---|
| **Ask** | Lowest price a seller will accept |
| **ATM Strategy** | Auto Trade Management — NinjaTrader's bracket order feature |
| **Backtesting** | Testing a strategy on historical data |
| **Best Bid/Ask** | The highest bid and lowest ask in the market |
| **Circuit Breaker** | Automatic market halt during extreme moves |
| **CME** | Chicago Mercantile Exchange — primary US futures exchange |
| **Drawdown** | Decline from peak to trough in account value |
| **DOM** | Depth of Market — visual order book display |
| **EMA** | Exponential Moving Average |
| **ETH** | Extended Trading Hours (outside regular session) |
| **Execution Report** | FIX message confirming order status |
| **Fill** | When an order is executed |
| **FIX Protocol** | Financial Information eXchange — industry messaging standard |
| **Futures** | Contract to buy/sell asset at set price on future date |
| **Greeks** | Risk metrics for options (Delta, Gamma, Theta, Vega, Rho) |
| **Hedge** | Taking an opposite position to reduce risk |
| **HFT** | High-Frequency Trading — algorithmic microsecond trading |
| **Initial Margin** | Deposit required to open a futures position |
| **L1 Data** | Level 1 — best bid, ask, last price, volume |
| **L2 Data** | Level 2 — full order book depth |
| **Latency** | Delay in order/data transmission |
| **Leverage** | Controlling more than your capital using borrowed funds |
| **Limit Order** | Order to buy/sell at a specific price or better |
| **Liquidity** | Ease of buying/selling without affecting price |
| **Long** | Buying, expecting price to rise |
| **Maintenance Margin** | Minimum equity to keep a position open |
| **Mark-to-Market** | Daily revaluation of futures positions |
| **Market Order** | Buy/sell immediately at current market price |
| **NFA** | National Futures Association — futures self-regulator |
| **OCO** | One Cancels Other — paired order type |
| **Open Interest** | Total outstanding futures contracts not yet settled |
| **Options** | Right (not obligation) to buy/sell at a set price |
| **P&L** | Profit and Loss |
| **Paper Trading** | Simulated trading with virtual money |
| **PDT Rule** | Pattern Day Trader rule — $25,000 minimum for frequent day trading |
| **Pip** | Smallest forex price movement (0.0001 for most pairs) |
| **Position** | The amount of a security owned (long) or owed (short) |
| **Realized P&L** | Profit/loss from closed positions |
| **Rollover** | Moving from expiring futures contract to next one |
| **RTH** | Regular Trading Hours |
| **Settlement** | Final price calculation at market close |
| **Short** | Selling borrowed asset, expecting price to fall |
| **Slippage** | Difference between expected and actual fill price |
| **Spread** | Difference between bid and ask price |
| **Stop Order** | Triggers market order when price hits a level |
| **SuperDOM** | NinjaTrader's advanced Depth of Market panel |
| **Tick** | Minimum price movement of a futures contract |
| **Tick Value** | Dollar value of one tick move |
| **Time & Sales** | Real-time record of every executed trade |
| **Unrealized P&L** | Profit/loss on open, not yet closed positions |
| **VaR** | Value at Risk — statistical risk measure |
| **Volatility** | Degree of price fluctuation |
| **Volume** | Number of contracts/shares traded |

---

## Appendix: Interview Prep Cheat Sheet

### Things to Say Confidently in the Interview

```
"I understand the full order lifecycle from placement through
 execution report, and I've tested edge cases like partial fills,
 cancel-pending states, and network disconnections mid-order."

"I'd focus on ensuring the P&L calculations are mathematically
 exact, especially for futures where tick value and daily
 mark-to-market make precision critical."

"For data feed testing, I'd validate timestamp monotonicity,
 bid/ask spread logic, and failover to backup feed scenarios."

"I'm aware that FIX Protocol is the industry standard for order
 routing and I understand key message types like New Order Single
 (35=D) and Execution Reports (35=8)."

"Contract rollover is a critical regression scenario — I'd test
 that charts switch correctly, no orders remain on expired contracts,
 and continuous data is maintained."
```

### Questions to Ask Them
```
1. "What's your current test automation coverage on the order
    management system?"

2. "How do you handle regression testing around contract rollover
    periods when the live market is your test environment?"

3. "Do you use a FIX simulator or a real exchange test environment
    for order flow testing?"

4. "How is latency benchmarked in your CI/CD pipeline — do you
    have threshold gates before deployment?"

5. "What's your strategy for testing NinjaScript strategies to
    ensure simulation behavior matches live behavior?"
```

---

## 14. LSEG — London Stock Exchange Group Deep Dive

### 14.1 What Is LSEG?

**LSEG (London Stock Exchange Group)** is one of the world's largest financial markets infrastructure companies. It is not just a stock exchange — it is a full-spectrum financial data, analytics, trading, and clearing business that sits at the heart of global capital markets.

```
LSEG At a Glance:
  Headquartered:    London, United Kingdom
  Founded:          1801 (London Stock Exchange); modern LSEG formed over decades
  Key Acquisition:  Refinitiv (bought from Blackstone/Thomson Reuters, 2021, ~$27B)
  Employees:        ~25,000 globally
  Revenue:          ~£8.7 billion (2024 est.)
  Listed On:        London Stock Exchange (ticker: LSEG.L)
  Serves:           Banks, brokers, asset managers, hedge funds, regulators globally
```

> Think of LSEG as the **backbone of financial markets** — they provide the infrastructure
> (exchanges, clearing houses), the data (prices, reference data), and the tools
> (terminals, APIs, analytics) that the entire industry runs on.

---

### 14.2 LSEG's Business Divisions

LSEG operates across four main divisions:

```
┌──────────────────────────────────────────────────────────────────┐
│                        LSEG GROUP                                │
├──────────────┬──────────────────┬──────────────┬────────────────┤
│  Data &      │  Capital Markets │  Post Trade  │  Technology    │
│  Analytics   │                  │              │  Services      │
├──────────────┼──────────────────┼──────────────┼────────────────┤
│ Refinitiv    │ London Stock     │ LCH          │ LSEG           │
│ Workspace    │ Exchange (LSE)   │ (Clearing)   │ Technology     │
│ Elektron     │ Turquoise MTF    │ MillenniumIT │                │
│ FTSE Russell │ Borsa Italiana   │              │                │
│ World-Check  │ Oslo Børs        │              │                │
└──────────────┴──────────────────┴──────────────┴────────────────┘
```

---

### 14.3 Division 1: Data & Analytics (Refinitiv)

This is LSEG's largest revenue driver, inherited from the **Refinitiv acquisition in 2021**.
Refinitiv was previously the financial data arm of Thomson Reuters.

#### Refinitiv Workspace (formerly Eikon)
The professional financial terminal — LSEG's answer to Bloomberg Terminal.

```
What it provides:
  ✦ Real-time market data (prices, quotes, news)
  ✦ Financial analytics and charting tools
  ✦ Company fundamentals and financial statements
  ✦ Fixed income, FX, derivatives pricing
  ✦ News feeds (Reuters news)
  ✦ Portfolio analytics tools
  ✦ Messaging (Eikon Messenger / LSEG Messenger)

Who uses it:
  Traders, analysts, portfolio managers, risk managers in banks and funds

SDET relevance:
  Testing this = validating data accuracy, UI responsiveness,
  API integrations, and real-time feed reliability
```

#### Elektron Data Platform (EDP)
LSEG's real-time financial data delivery infrastructure.

```
Components:
  Refinitiv Data Platform (RDP) → Cloud-based API for financial data
  Elektron Real-Time (ERT)      → Ultra-low latency streaming data
  Elektron SDK                  → Libraries for consuming data in apps
  WebSocket API                 → Real-time streaming for web apps
  REST API                      → On-demand data retrieval

Data types available:
  Level 1 (Best Bid/Ask, Last)
  Level 2 (Full Order Book)
  Time Series (Historical OHLCV)
  Reference Data (instrument metadata)
  News (Reuters real-time news)
  ESG Data (environmental/social/governance scores)
```

**Elektron Message API (EMA) — SDET Must Know:**
```java
// Example: Subscribing to real-time ES futures price via LSEG EMA
OmmConsumer consumer = EmaFactory.createOmmConsumer(
    EmaFactory.createOmmConsumerConfig().host("elektron-host:14002")
);

consumer.registerClient(
    EmaFactory.createReqMsg()
        .domainType(EmaRdm.MMT_MARKET_PRICE)
        .serviceName("ELEKTRON_DD")
        .name("ESU6:VIP"),  // ES September futures
    appClient
);

// What to test:
// ✓ Data arrives within latency SLA
// ✓ Bid always ≤ Last ≤ Ask
// ✓ Correct instrument name resolves correctly
// ✓ Reconnect after session drop restores subscription
```

#### FTSE Russell — Index Business
LSEG owns **FTSE Russell**, one of the world's largest index providers.

| Index | Tracks | Used For |
|---|---|---|
| **FTSE 100** | Top 100 companies on LSE by market cap | UK market benchmark |
| **FTSE 250** | Next 250 companies | Mid-cap UK benchmark |
| **FTSE All-World** | Global equities across 49 countries | Global equity benchmark |
| **Russell 2000** | 2,000 US small-cap stocks | US small-cap benchmark |
| **Russell 1000** | 1,000 largest US stocks | US large-cap benchmark |
| **FTSE4Good** | ESG-compliant companies | Sustainable investing |

```
SDET relevance for index testing:
  ✓ Index constituent changes (quarterly rebalancing)
  ✓ Index value calculation (weighted average of components)
  ✓ Corporate actions (splits, mergers affect index weights)
  ✓ Reconstitution: when stocks are added/removed from index
```

#### World-Check (Risk Intelligence)
LSEG's **KYC/AML screening database** — used to screen clients against:
- Sanctions lists (OFAC, UN, EU, UK HMT)
- Politically Exposed Persons (PEPs)
- Adverse media and watchlists

```
SDET relevance:
  ✓ API returns correct risk classification for a given entity
  ✓ Sanctions list updates propagate within SLA (often < 1 hour)
  ✓ False positive/negative rates within acceptable thresholds
  ✓ Data privacy — GDPR/data handling compliance in tests
  ✓ Batch screening performance (thousands of records)
```

---

### 14.4 Division 2: Capital Markets — Trading Venues

#### London Stock Exchange (LSE)
One of the world's oldest and most prestigious stock exchanges.

```
Key Facts:
  Founded:    1801
  Location:   Paternoster Square, London
  Listed cos: ~2,000+ companies
  Market cap: ~$4+ trillion (one of the largest globally)

Market Segments:
  Main Market   → Large, established companies (e.g., HSBC, Shell, BP)
  AIM           → Alternative Investment Market (smaller, growth companies)
  International → Foreign companies listed on LSE

Trading System: Millennium Exchange (built by MillenniumIT, an LSEG subsidiary)

Trading Hours (LSE):
  Pre-open:          07:50 – 08:00 BST
  Continuous:        08:00 – 16:30 BST
  Closing Auction:   16:30 – 16:35 BST
  After hours:       16:35 – 17:15 BST
```

#### Turquoise — Pan-European MTF
A **Multilateral Trading Facility (MTF)** — an alternative trading venue to traditional exchanges.

```
What is an MTF?
  A trading venue that is NOT a regulated stock exchange but allows
  trading of securities listed on other exchanges. Competes on price
  and speed with traditional exchanges.

Turquoise:
  ✦ Pan-European equities trading
  ✦ Lower transaction costs than primary exchanges
  ✦ Turquoise Plato Block Discovery — for large "dark pool" trades
  ✦ Used by institutional investors for best execution

Dark Pool vs Lit Market:
  Lit Market  = Order book is visible to all (transparent)
  Dark Pool   = Orders hidden from public view (opaque)
               Used to avoid moving the market with large orders
```

#### Borsa Italiana
Italy's primary stock exchange, acquired by LSEG in 2021.

```
Key Markets:
  MTA (Mercato Telematico Azionario) → Main equities market
  MIV                                → Investment vehicles
  MOT                                → Bond market
  IDEM                               → Derivatives

Key Index: FTSE MIB (Italy's equivalent of the FTSE 100)
```

---

### 14.5 Division 3: Post-Trade — LCH (Clearing & Settlement)

**LCH** is one of the world's largest **Central Counterparty Clearing Houses (CCPs)** — a critical piece of financial infrastructure most people have never heard of.

#### What Does a Clearing House Do?

```
WITHOUT A CLEARING HOUSE:
  Trader A ──────────────────────────────────► Trader B
  (If Trader B defaults, Trader A loses everything)

WITH A CLEARING HOUSE (LCH):
  Trader A ──────────────► LCH ◄────────────── Trader B
  (LCH becomes the buyer to every seller and seller to every buyer)
  (If Trader B defaults, LCH guarantees Trader A still gets paid)

This is called NOVATION — LCH steps in between all trades.
```

#### LCH Services

| Service | Asset Class | Description |
|---|---|---|
| **SwapClear** | Interest Rate Swaps | World's largest IRS clearing service |
| **ForexClear** | FX Derivatives | OTC FX option and NDF clearing |
| **RepoClear** | Repos & Bonds | European government bonds clearing |
| **EquityClear** | Equities | European equity clearing |
| **CDSClear** | Credit Default Swaps | CDS clearing |
| **Listed Rates** | Exchange-traded derivatives | Futures and options clearing |

#### Key Concepts in Clearing — SDET Must Know

```
INITIAL MARGIN:
  Collateral deposited with LCH when opening a position
  Protects against potential future losses
  Test: Is margin calculated correctly per LCH's SPAN algorithm?

VARIATION MARGIN:
  Daily cash settlement of P&L (mark-to-market)
  Winners receive cash, losers pay cash — every day
  Test: Is variation margin calculated and transferred correctly?

MARGIN CALL:
  When a member's margin falls below minimum, LCH demands top-up
  Test: Is margin call generated and communicated within SLA?

DEFAULT FUND:
  Pool of contributions from all members to cover a major default
  Test: Is contribution calculated correctly per member?

SPAN (Standard Portfolio Analysis of Risk):
  CME's margining methodology, used globally
  Calculates worst-case loss across a portfolio of futures/options
  SDET: You may test SPAN margin calculations

NET vs GROSS SETTLEMENT:
  Net: All trades aggregated; one net payment at end of day (efficient)
  Gross: Each trade settled individually (safer but slower)
```

#### Settlement

After clearing, trades must be **settled** — the actual transfer of securities and cash.

```
Settlement Cycle:
  T+0 = Same day (rare; some bonds)
  T+1 = Next business day (US standard since 2024)
  T+2 = Two business days (most European markets)

Settlement Infrastructure:
  Euroclear  → European bond/equity settlement
  Clearstream → European bond settlement
  DTCC (DTC) → US equities settlement
  CRESTCo    → UK equity settlement (operated by Euroclear UK)

SDET relevance:
  ✓ Trade details match between execution venue and CCP
  ✓ Settlement instructions generated correctly
  ✓ Failed trades detected and reported (settlement fails)
  ✓ Corporate action processing during settlement window
```

---

### 14.6 Division 4: LSEG Technology (MillenniumIT)

LSEG owns **MillenniumIT**, a Sri Lanka-based technology firm that built the exchange trading systems used not just by LSE but by stock exchanges worldwide.

```
MillenniumIT — Sri Lanka Connection 🇱🇰:
  Founded:     1996, Colombo, Sri Lanka
  Acquired:    2009 by London Stock Exchange Group
  HQ:          Sri Lanka (with offices in London, NY)

What they built:
  Millennium Exchange  → Core trading engine used by LSE, Borsa Italiana,
                         Johannesburg SE, Oslo Børs, and many others
  Millennium Post-Trade → Clearing and settlement systems
  MillenniumIT ESP     → Enterprise Software Platform for exchanges

Why this matters to you as an SDET in Sri Lanka:
  MillenniumIT is a major tech employer in Sri Lanka.
  Working with LSEG-related systems gives you direct relevance
  to one of the strongest fintech companies connected to your country.
```

**Millennium Exchange Performance (What SDET Must Know):**
```
Order matching speed:  < 100 microseconds
Messages per second:   Millions of messages
Uptime SLA:            99.999% (Five nines — less than 5.26 min downtime/year)
Key test challenge:    How do you test microsecond latency?
                       → Specialized hardware timestamping
                       → Kernel-bypass networking (DPDK, RDMA)
                       → Co-location testing at exchange data centres
```

---

### 14.7 LSEG Data API — Practical for SDETs

LSEG provides modern APIs for accessing their data. As an SDET, you may write tests against these.

#### LSEG Data API (formerly Refinitiv Data Platform API)

```python
# Example: Fetch real-time quote using LSEG Data API (Python)
import lseg.data as ld

# Open session
ld.open_session()

# Get real-time snapshot for FTSE 100 constituents
response = ld.get_data(
    universe=["HSBA.L", "BP.L", "AZN.L"],  # LSE tickers
    fields=["BID", "ASK", "TRDPRC_1", "ACVOL_1", "NETCHNG_1"]
)

# fields:
# BID       = Best bid price
# ASK       = Best ask price
# TRDPRC_1  = Last traded price
# ACVOL_1   = Accumulated volume
# NETCHNG_1 = Net change from previous close

print(response)
ld.close_session()
```

#### Key API Endpoints for Testing

| Endpoint | Purpose | Test Scenario |
|---|---|---|
| `/data/pricing/snapshots` | Get current prices | Validate bid ≤ last ≤ ask |
| `/data/pricing/stream` | Stream real-time prices | Test reconnect, data gaps |
| `/data/historical-pricing` | Historical OHLCV data | Validate completeness, no gaps |
| `/data/fundamental-and-reference` | Company financials | Validate EPS, P/E accuracy |
| `/data/search` | Search for instruments | Test by ISIN, RIC, name |
| `/auth/token` | OAuth2 token | Test token expiry, refresh |

#### RIC (Reuters Instrument Code)
LSEG's proprietary identifier for financial instruments:

```
Format: TICKER.EXCHANGE_CODE

Examples:
  HSBA.L    → HSBC on London Stock Exchange
  BP.L      → BP on London Stock Exchange
  AAPL.O    → Apple on NASDAQ
  MSFT.OQ   → Microsoft on NASDAQ (OTC quoted)
  ESc1      → ES Futures, continuous front-month contract
  GBP=      → GBP spot FX rate
  .FTSE     → FTSE 100 index
  .SPX      → S&P 500 index
  EUR=EBS   → EUR/USD on EBS platform

SDET relevance:
  ✓ RIC resolution — does the correct instrument load?
  ✓ Continuous RICs (c1, c2) roll over correctly at expiry
  ✓ Invalid RICs return correct error, not null/crash
```

---

### 14.8 LSEG vs. Bloomberg — Know the Difference

You'll often hear these two compared in the industry:

| Feature | LSEG (Refinitiv Workspace) | Bloomberg Terminal |
|---|---|---|
| **Market share** | ~30% of terminals | ~33% of terminals |
| **Strength** | FX data, news (Reuters), emerging markets | Equity data, fixed income, analytics |
| **News** | Reuters News (owned by LSEG data arm) | Bloomberg News |
| **Terminal cost** | ~$22,000/year | ~$24,000/year/user |
| **API quality** | Strong REST/WebSocket APIs | Bloomberg API (BLPAPI) |
| **Mobile** | Refinitiv Workspace app | Bloomberg app |
| **Excel add-in** | Datastream / Workspace Excel | Bloomberg Excel Add-in (BDP/BDS) |
| **Used by** | Banks, FX traders, bond traders | Equities, fixed income, hedge funds |

---

### 14.9 LSEG in the SDET World — What You'd Actually Test

If you work on an LSEG-integrated system, here's what your test work looks like:

#### A. Data Quality Testing
```
Test: Does LSEG data match official exchange data?

Approach:
  1. Fetch LSEG prices via API at timestamp T
  2. Fetch LSE official published data for the same timestamp
  3. Compare: price, volume, bid/ask

Tolerance:
  For real-time data: within 1 tick / within 5ms timestamp delta
  For historical data: exact match required

Common issues found:
  ✗ Stale data (LSEG feed lags exchange by > SLA)
  ✗ Bad ticks (erroneous prices from source exchange)
  ✗ Missing data (gaps in tick history)
  ✗ Corporate action not applied (split not reflected in price)
```

#### B. API Integration Testing
```
Test areas for LSEG Data API:
  ✓ Authentication (OAuth2 token flow, token expiry and refresh)
  ✓ Rate limiting (API has request limits — what happens at limit?)
  ✓ Pagination (large responses come in pages)
  ✓ Error handling (invalid RIC, unavailable service)
  ✓ Latency SLA (real-time data within promised milliseconds)
  ✓ WebSocket stability (long-running stream, 24-hour test)
  ✓ Data type validation (numbers as numbers, not strings)

Example negative test:
  Request: GET /data/pricing/snapshots?universe=INVALID.XX
  Expected: HTTP 200 with error status in response body, NOT 500
  Actual observed: Some providers return 500 — that's a bug
```

#### C. Settlement & Clearing Testing
```
If testing LCH-integrated systems:
  ✓ Margin calculation accuracy (compare to SPAN reference values)
  ✓ Variation margin: daily cash flows correct direction and amount
  ✓ Margin call generation within SLA (typically 30 minutes)
  ✓ Collateral substitution (swapping one eligible asset for another)
  ✓ Default management: simulate a member default, verify waterfall
  ✓ End-of-day settlement batch: all trades matched and settled
  ✓ Failed trade reporting: unmatched trades flagged by cut-off time
```

#### D. Index Testing (FTSE Russell)
```
Quarterly rebalancing test scenarios:
  ✓ New constituents added with correct weight
  ✓ Removed constituents excluded from calculation
  ✓ Index value recalculated correctly post-rebalancing
  ✓ Corporate actions (dividends, splits) reflected in index
  ✓ Fast exit rule: company in distress removed between rebalances
  ✓ IPO inclusions: fast-track rule for large IPOs

Index calculation test:
  Free-float market cap weighted index:
  
  Constituent weight = (Free-float shares × Price) ÷ Index Divisor
  
  Test: Does the system compute each weight correctly
        and does sum of all weights = 100%?
```

---

### 14.10 LSEG Ecosystem Quick-Reference

```
LSEG Product        → What It Does                    → Your Test Focus
─────────────────────────────────────────────────────────────────────────
Refinitiv Workspace → Professional terminal            UI, data accuracy
Elektron/EDP        → Real-time data delivery          Latency, reliability
LSEG Data API       → REST/WebSocket data access       Integration, auth
World-Check         → KYC/AML screening                Data accuracy, speed
FTSE Russell        → Index computation                Calculation accuracy
Millennium Exchange → Exchange matching engine         Performance, latency
LCH SwapClear       → Interest rate swap clearing      Margin, settlement
LCH ForexClear      → FX derivatives clearing          Margin, exposure
RepoClear           → Bond repo clearing               Settlement accuracy
MillenniumIT        → Exchange technology (Sri Lanka)  Infrastructure testing
Borsa Italiana      → Italian equities exchange        Trading, data feeds
Turquoise           → Pan-European MTF                 Order routing, best execution
```

---

### 14.11 Key LSEG Terms for the Interview

| Term | Definition |
|---|---|
| **RIC** | Reuters Instrument Code — LSEG's instrument identifier (e.g., AAPL.O) |
| **ISIN** | International Securities Identification Number — global 12-digit ID |
| **Refinitiv** | LSEG's data and analytics division (ex-Thomson Reuters) |
| **Elektron** | LSEG's ultra-low latency data platform |
| **EDP** | Elektron Data Platform — API layer for accessing LSEG data |
| **Workspace** | LSEG's professional financial terminal (successor to Eikon) |
| **LCH** | Clearing house subsidiary — guarantees trades don't fail |
| **CCP** | Central Counterparty — entity that sits between buyer and seller |
| **Novation** | Legal process where CCP replaces original counterparty |
| **MTF** | Multilateral Trading Facility — alternative to stock exchange |
| **Turquoise** | LSEG's pan-European MTF |
| **FTSE** | LSEG's index business (Financial Times Stock Exchange, historically) |
| **MillenniumIT** | LSEG's Sri Lanka-based exchange technology subsidiary |
| **Variation Margin** | Daily P&L cash settlement at clearing house |
| **Initial Margin** | Upfront collateral deposited with clearing house |
| **SPAN** | Standard Portfolio Analysis of Risk — margin methodology |
| **T+1** | Trade settlement next business day (US standard from 2024) |
| **Free Float** | Shares available for public trading (excludes locked-in insiders) |
| **World-Check** | LSEG's KYC/AML risk screening database |
| **Dark Pool** | Private trading venue; orders not visible to market |
| **Lit Market** | Public exchange with visible order book |

---

*Guide prepared for NinjaTrader & LSEG interview preparation | Capital Markets + SDET Domain Reference*
*Last updated: July 2026*
