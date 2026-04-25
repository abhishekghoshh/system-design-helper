# Web Hooks

## Blogs and websites


## Medium


## Youtube


## Theory

HTTP callbacks triggered by events.

**How it Works:**
1. Client registers webhook URL with server
2. Event occurs on server
3. Server sends HTTP POST to webhook URL
4. Client processes the payload

**Use Cases:**
- Payment confirmations (Stripe, PayPal)
- Git push notifications (GitHub)
- CI/CD triggers
- Real-time integrations

**Best Practices:**
- Verify webhook signatures
- Handle retries and idempotency
- Process asynchronously
- Return 2xx quickly
