# Design UPI Payments System


## YouTube

- [System Design of UPI Payments](https://www.youtube.com/watch?v=fqySz1Me2pI)

---

## Blogs

- [Designing UPI - System Design](https://www.geeksforgeeks.org/system-design/designing-upi-system-design/)
- [System Design: UPI (Unified Payment Interface)](https://dev.to/zeeshanali0704/system-design-upi-unified-payment-interface-2ng3)
- [System Design for Unified Payments Interface (UPI)](https://www.linkedin.com/pulse/system-design-unified-payments-interface-upi-nikhil-joshi-7s5kf/)
- [What is UPI? Unified Payments Interface Features and How UPI Works](https://razorpay.com/blog/what-is-upi-and-how-it-works/)

---

## Medium

- [UPI System Design](https://medium.com/career-drill/upi-system-design-f310d881b33d)
- [Technical Flow of Unified Payment Interface P2P Payments](https://medium.com/@vansh7uppal/technical-flow-of-united-payment-interface-p2p-payments-f553f49eae14)

---

## Theory

### Key Concepts

- **VPA (Virtual Payment Address):**  
    A unique identifier for users in the UPI ecosystem, e.g., `username@bank`. It abstracts away sensitive bank details.

- **Bank Account Details:**  
    Traditionally, to transfer money, you need:
    - Account Number
    - Bank Name
    - Branch Code
    - IFSC Code

- **Payment Methods in India:**
    - **IMPS (Immediate Payment Service):** Real-time, 24x7, instant fund transfer.
    - **NEFT (National Electronic Funds Transfer):** Batch-processed, may take some time, uses UTR number, has amount limits.
    - **RTGS (Real Time Gross Settlement):** Real-time, for large-value transactions.
    - **UPI (Unified Payments Interface):** Real-time, instant, works 24x7, abstracts bank details using VPA.

### UPI Architecture

- **NPCI (National Payments Corporation of India):**  
    Governs and operates the UPI infrastructure. Only authorized banks can access NPCI APIs.

- **Banks:**  
    Must be authorized by RBI and NPCI to participate in UPI. They act as Payment Service Providers (PSPs).

- **Third-party Apps (PSPs):**  
    Apps like Google Pay, PhonePe, Paytm act as customer-facing interfaces but must partner with banks to access UPI.

### UPI Flow (Simplified)

1. **User initiates payment** via a UPI-enabled app using VPA.
2. **App communicates with partner bank** (PSP) to initiate the transaction.
3. **Bank interacts with NPCI** to route the transaction to the recipient's bank.
4. **NPCI validates and settles** the transaction in real-time.
5. **Confirmation** is sent back to both sender and receiver.

### Security

- UPI transactions are secured by multi-factor authentication (e.g., device binding, UPI PIN).
- Only authorized apps and banks can access the UPI APIs.

---

**Summary:**  
UPI revolutionizes payments in India by providing a unified, secure, and real-time payment interface, abstracting complex bank details and enabling seamless peer-to-peer and merchant transactions.