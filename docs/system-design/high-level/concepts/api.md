# API (Application Programming Interface)

## Blogs and websites


## Medium

- [API Design 101: From Basics to Best Practices](https://levelup.gitconnected.com/api-design-101-from-basics-to-best-practices-a0261cdf8886)

## Youtube

### Single Videos

- [API Gateway vs Load Balancer | System Design](https://www.youtube.com/watch?v=KGM9eSPeZ04)
- [REST vs GraphQL | System Design](https://www.youtube.com/watch?v=htQlfMV0Dys)
- [Server-Sent Events vs WebSockets | System Design](https://www.youtube.com/watch?v=X_DdIXrmWOo)
- [Event Sourcing VS CRUD | System Design](https://www.youtube.com/watch?v=jjhdQwQBBuA)
- [HTTP/1.1 vs HTTP/2 vs HTTP/3 | System Design](https://www.youtube.com/watch?v=ocGtt0IX0Js)


- [CORS Explained - Cross-Origin Resource Sharing](https://www.youtube.com/watch?v=WWnR4xptSRk)

- [Understand Attacks: CSRF, XSS, CORS, SQL Injection with DEMO | Spring Security](https://www.youtube.com/watch?v=3pYioNIPj84)

## Theory

Interface that allows different software systems to communicate.

**Types:**
- **REST**: Resource-based, uses HTTP
- **GraphQL**: Query language for APIs
- **gRPC**: High-performance RPC framework
- **SOAP**: XML-based protocol (legacy)

### Content Negotiation

Client and server agree on response format.

**HTTP Headers:**
- `Accept`: Preferred content type
- `Accept-Language`: Preferred language
- `Accept-Encoding`: Compression support

### API Versioning

Managing changes to APIs.

**Strategies:**
- **URI**: `/v1/users`, `/v2/users`
- **Header**: `API-Version: 2`
- **Query**: `/users?version=2`
- **Content Negotiation**: `Accept: application/vnd.api.v2+json`

---

### API related things
