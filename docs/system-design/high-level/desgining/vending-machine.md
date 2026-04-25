# Design Vending Machine

## Blogs and websites


## Medium


## Youtube


## Theory

### Problem Statement
Design a vending machine system that allows users to select products, make payments, and dispense items reliably.

### Functional Requirements
- Display available products with prices and stock levels
- Accept multiple payment methods (coins, bills, cards, digital wallets)
- Dispense selected product after successful payment
- Return change for cash payments
- Handle refunds for failed dispensing
- Admin interface for restocking and revenue tracking

### Non-Functional Requirements
- **Reliability**: Never charge without dispensing (or refund immediately)
- **Availability**: 99.9% uptime
- **Consistency**: Accurate inventory and payment tracking
- **Low Latency**: Transaction completes in < 2 seconds

### High-Level Design

```
┌─────────────────────────────────────────────────┐
│                  Vending Machine                  │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  Display  │  │ Keypad / │  │   Payment     │  │
│  │  Panel    │  │ Touch UI │  │   Terminal    │  │
│  └────┬─────┘  └────┬─────┘  └───────┬───────┘  │
│       │              │                │           │
│  ┌────▼──────────────▼────────────────▼────────┐ │
│  │           Vending Controller                 │ │
│  │  ┌─────────────┐  ┌──────────────────────┐  │ │
│  │  │   State     │  │   Inventory          │  │ │
│  │  │   Machine   │  │   Manager            │  │ │
│  │  └─────────────┘  └──────────────────────┘  │ │
│  │  ┌─────────────┐  ┌──────────────────────┐  │ │
│  │  │   Payment   │  │   Dispenser          │  │ │
│  │  │   Processor │  │   Controller         │  │ │
│  │  └─────────────┘  └──────────────────────┘  │ │
│  └──────────────────────┬──────────────────────┘ │
│                         │                         │
│                    ┌────▼─────┐                   │
│                    │ Local DB │                   │
│                    └────┬─────┘                   │
└─────────────────────────┼─────────────────────────┘
                          │ (periodic sync)
                    ┌─────▼──────┐
                    │  Cloud     │
                    │  Backend   │
                    └────────────┘
```

### State Machine Design

```
IDLE → PRODUCT_SELECTED → PAYMENT_PENDING → PAYMENT_RECEIVED → DISPENSING → IDLE
                                  │                                    │
                                  ▼                                    ▼
                              CANCELLED                          DISPENSE_FAILED
                              (refund)                           (refund + alert)
```

**States:**
1. **IDLE**: Waiting for user interaction
2. **PRODUCT_SELECTED**: User chose a product, displaying price
3. **PAYMENT_PENDING**: Accepting payment input
4. **PAYMENT_RECEIVED**: Full amount received, processing
5. **DISPENSING**: Mechanical arm delivering product
6. **CANCELLED**: User cancelled, refunding
7. **DISPENSE_FAILED**: Mechanical failure, refunding + alerting admin

### Key Design Decisions

**Payment Processing:**
- Coins/bills: Local validation with coin/bill acceptor hardware
- Cards/digital: API call to payment gateway (need network connectivity)
- Two-phase: Authorize → Dispense → Capture (never capture before dispensing)

**Inventory Management:**
- Local inventory count per slot
- Periodic sync to cloud for analytics and restock scheduling
- Weight sensors for real-time stock verification

**Concurrency:**
- Single user per machine (physical constraint)
- Transaction timeout (60s) to prevent blocking
- Mutex on dispenser mechanism

### Scalability (Fleet Management)

For managing thousands of machines:
```
Machines ──(MQTT/HTTP)──→ IoT Gateway ──→ Fleet Management Service
                                              │
                                    ┌─────────┼──────────┐
                                    ▼         ▼          ▼
                              Inventory   Analytics   Alerting
                              Service     Service     Service
```
