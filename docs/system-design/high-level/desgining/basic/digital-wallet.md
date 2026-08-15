# Design a Digital Wallet

## Blogs and websites

## Medium

## Youtube

## Theory

### Problem Statement
Design a digital wallet system (like Google Pay, Apple Pay, Paytm) that supports adding money, peer-to-peer transfers, merchant payments, and transaction history with strong consistency guarantees.

### Functional Requirements
- User registration and KYC verification
- Add money from bank/card to wallet
- Peer-to-peer (P2P) money transfers
- Pay merchants (QR code, payment link)
- Transaction history and statements
- Refunds and dispute resolution
- Wallet balance inquiry

### Non-Functional Requirements
- **Consistency**: Strong — money must never be lost or duplicated
- **Availability**: 99.99% (financial system)
- **Latency**: Transfer completes < 1 second
- **Security**: PCI-DSS compliant, encrypted at rest and in transit
- **Audit**: Every transaction traceable

### High-Level Architecture

```
┌──────────┐     ┌──────────────┐     ┌──────────────────────────┐
│  Client  │────▶│   API GW /   │────▶│   Application Layer       │
│  (App)   │     │   LB         │     │                           │
└──────────┘     └──────────────┘     │  ┌─────────────────────┐  │
                                      │  │ Wallet Service       │  │
                                      │  │ Transfer Service     │  │
                                      │  │ Payment Service      │  │
                                      │  │ Ledger Service       │  │
                                      │  │ Notification Service │  │
                                      │  └──────────┬──────────┘  │
                                      └─────────────┼─────────────┘
                                                    │
                              ┌──────────────────────┼──────────────┐
                              ▼                      ▼              ▼
                        ┌───────────┐         ┌───────────┐  ┌──────────┐
                        │  Wallet   │         │  Ledger   │  │ Bank     │
                        │  DB       │         │  DB       │  │ Gateway  │
                        └───────────┘         └───────────┘  └──────────┘
```

### Double-Entry Ledger

Every transaction creates two entries (debit + credit):

```
Transfer: Alice sends $100 to Bob

Ledger entries:
┌──────────┬──────┬────────┬────────┬─────────────────┐
│ Entry ID │ User │ Debit  │ Credit │ Description      │
├──────────┼──────┼────────┼────────┼─────────────────┤
│ 1        │Alice │ $100   │        │ Transfer to Bob  │
│ 2        │Bob   │        │ $100   │ Transfer from    │
└──────────┴──────┴────────┴────────┴─────────────────┘

Invariant: SUM(debits) = SUM(credits) — ALWAYS
```

### Transfer Flow (P2P)

```
1. Client → Transfer Service: send($100, Alice→Bob)
2. Validate: Alice balance >= $100, Bob exists, limits check
3. BEGIN TRANSACTION
     Debit Alice's wallet: balance -= $100
     Credit Bob's wallet:  balance += $100
     Insert 2 ledger entries
   COMMIT
4. Send notifications to both
5. Return transaction receipt
```

**Idempotency:**
- Client generates unique `idempotency_key` per request
- Server checks if key already processed → return cached result
- Prevents double-charging on network retries

### Handling Failures

```
Scenario: Transfer partially fails

Solution: Saga Pattern with compensation
  Step 1: Debit Alice    → Success ✓
  Step 2: Credit Bob     → FAILS ✗
  Compensate: Credit Alice back (reverse Step 1)
  
Alternative: Two-Phase Commit (2PC) for same-DB transactions
```

### Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Consistency | Strong (ACID) | Money can't be eventually consistent |
| Database | PostgreSQL | ACID transactions, proven for financial |
| Idempotency | Request-level dedup | Prevent double payments |
| Ledger | Double-entry bookkeeping | Audit trail, balance verification |
| Concurrency | Optimistic locking on balance | Prevent overdraft race conditions |

### Security Considerations
- **Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Authentication**: MFA, biometrics, device binding
- **Authorization**: Transaction PIN for payments
- **Rate limiting**: Max transactions per minute/day
- **Fraud detection**: ML models on transaction patterns
- **PCI-DSS**: Compliance for card data handling
