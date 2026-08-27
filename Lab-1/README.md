# SE Lab 1 — Requirements Engineering & UML

| Field | Details |
|---|---|
| **Name** | Dhanush R |
| **SRN** | PES1UG24AM427 |
| **Problem Statement** | #39 — Second-Hand Product Escrow Marketplace |
| **Course** | Software Engineering Lab |

---

## System Description

A secure peer-to-peer trading marketplace where buyer payments are held in escrow, independent third-party inspectors certify product condition, and funds are released only upon buyer sign-off.

The platform connects **Buyers**, **Sellers**, and certified **Inspection Agents**. Payments are processed through an external **Payment Gateway** and held in escrow until both the Inspection Agent's verification report and the Buyer's explicit sign-off are on record. If the buyer is dissatisfied, they can raise a dispute — immediately freezing escrow funds — and the Inspection Agent resolves the dispute before any payment is disbursed.

---

## Repository Contents

```
Lab-1/
├── Requirements_Table.xlsx   # 5 Functional + 2 Non-Functional requirements
├── Use_Case_Diagram.pdf      # UML Use-Case Diagram (A3, 4 actors, 8 use cases)
├── Use_Case_Flow.pdf         # Detailed flow for UC-05 (Review Inspection & Sign Off)
└── README.md                 # This file
```

---

## Escrow Transaction Flow

```
Buyer places order
        │
        ▼
Payment locked in escrow  ──────────────────────────────────────────────┐
        │  (order status → "Under Inspection")                          │
        ▼                                                               │
Inspection Agent performs physical inspection                           │
        │                                                               │
        ▼                                                               │
Inspection report submitted to system                                   │
        │                                                               │
        ▼                                                               │
Buyer reviews inspection report                                         │
        │                                                               │
  ──────┴──────────────────────────────────────────────────────         │
  │ Accept                                  │ Raise Dispute             │
  ▼                                         ▼                           │
Buyer sign-off recorded             Dispute ticket created              │
(order → "Awaiting Release")        Escrow funds FROZEN                 │
        │                           Inspection Agent investigates       │
        ▼                                   │                           │
Both conditions met?                        ▼                           │
  inspection_verified = true        Dispute resolved                    │
  buyer_signed_off    = true                │                           │
        │                                   │                           │
        ▼                                   ▼                           │
Escrow released to Seller ◄─────── Outcome determines final action ◄───┘
(order → "Completed")
```

### Key Rules

1. **Escrow lock is atomic** — funds move to escrow in the same transaction as order creation; no partial states.
2. **Dual-confirmation release** — the system checks both `inspection_verified` and `buyer_signed_off` before crediting the seller.
3. **Immediate dispute freeze** — fund freeze occurs within 5 seconds of dispute registration; no withdrawal is possible during investigation.
4. **Immutable audit trail** — every action (escrow lock, inspection report, sign-off, dispute) is recorded with the authenticated user's ID and a UTC timestamp and cannot be altered without authorization.

---

## Requirements Summary

| Req ID | Type | Priority | One-line Summary |
|---|---|---|---|
| FR-001 | Functional | High | Lock buyer payment in escrow; set order to "Under Inspection" |
| FR-002 | Functional | High | Inspection Agent submits physical inspection report |
| FR-003 | Functional | High | Buyer reviews report and provides sign-off |
| FR-004 | Functional | High | Release escrow only after both inspection and sign-off |
| FR-005 | Functional | High | Buyer raises dispute; escrow funds frozen immediately |
| NFR-001 | Non-Functional | High | Fund freeze within 500 ms of dispute registration |
| NFR-002 | Non-Functional | High | All actions recorded with authenticated identity; immutable audit log |

---

## UML Use-Case Diagram Summary

- **System boundary**: Second-Hand Product Escrow Marketplace
- **Actors**: Buyer, Seller, Inspection Agent, Payment Gateway *(external)*
- **Use Cases**: UC-01 List Product · UC-02 Place Order · UC-03 Process Escrow Payment · UC-04 Inspect Product · UC-05 Review Inspection & Sign Off · UC-06 Release Escrow Funds · UC-07 Raise Dispute · UC-08 Resolve Dispute
- **«include»**: UC-02 → UC-03 · UC-03 → UC-04
- **«extend»**: UC-07 → UC-05
