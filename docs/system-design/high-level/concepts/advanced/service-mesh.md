# Service Mesh

## Blogs and websites


## Medium


## Youtube

- [Service Mesh and its Architecture | How Microservices Communicate?](https://www.youtube.com/watch?v=eIxdHepOeHw)
- [Load Balancer is Dead!](https://www.youtube.com/watch?v=kqQfdOoOXc4)


## Theory

### What is a Service Mesh?

A **service mesh** is a dedicated **infrastructure layer** that handles service-to-service communication in a microservices architecture. Instead of embedding networking logic (retries, timeouts, encryption, discovery) into every application, the mesh moves that responsibility into a **proxy sidecar** that runs alongside each service.

**The core problem it solves:** In a monolith, function calls are in-process. In microservices, every "function call" becomes a network request — unreliable, unsecured, and unobservable by default. A service mesh makes the network reliable, secure, and observable without changing application code.

```
WITHOUT SERVICE MESH                          WITH SERVICE MESH
┌─────────────┐     ┌─────────────┐          ┌─────────────────────┐     ┌─────────────────────┐
│  Service A  │     │  Service B  │          │      Service A      │     │      Service B      │
│             │     │             │          │  ┌───────────────┐  │     │  ┌───────────────┐  │
│  App Code   │     │  App Code   │          │  │   App Code    │  │     │  │   App Code    │  │
│  + Retries  │────►│  + Retries  │          │  │ (business     │  │     │  │ (business     │  │
│  + Timeouts │     │  + Timeouts │          │  │  logic only)  │  │     │  │  logic only)  │  │
│  + TLS      │     │  + TLS      │          │  └───────┬───────┘  │     │  └───────▲───────┘  │
│  + Discovery│     │  + Discovery│          │          │           │     │          │           │
│  + Metrics  │     │  + Metrics  │          │  ┌───────▼───────┐  │     │  ┌───────┴───────┐  │
│             │     │             │          │  │  Envoy Proxy  │──┼─────┼─►│  Envoy Proxy  │  │
│  (tight     │     │  (tight     │          │  │  (sidecar)    │  │     │  │  (sidecar)    │  │
│   coupling) │     │   coupling) │          │  │  handles all  │  │     │  │  handles all  │  │
└─────────────┘     └─────────────┘          │  │  networking   │  │     │  │  networking   │  │
                                              │  └───────────────┘  │     │  └───────────────┘  │
Each service must implement                   └─────────────────────┘     └─────────────────────┘
networking concerns in its                    Networking is decoupled from application code
own language (Go, Java, Python...)            Same proxy works for ALL languages
```

### Architecture: Data Plane vs Control Plane

Every service mesh has two fundamental components:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          CONTROL PLANE                                   │
│                                                                          │
│  Centralized management layer that configures all proxies                │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   Config     │  │  Certificate │  │   Service    │  │  Policy    │  │
│  │   Management │  │  Authority   │  │   Registry   │  │  Engine    │  │
│  │              │  │  (mTLS certs)│  │  (endpoints) │  │  (authz)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │
│         │                 │                  │                │          │
│         └────────┬────────┴──────────┬───────┴────────┬───────┘          │
│                  │     xDS API       │                │                  │
└──────────────────┼───────────────────┼────────────────┼──────────────────┘
                   ▼                   ▼                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           DATA PLANE                                     │
│                                                                          │
│  Network of proxies deployed as sidecars alongside every service         │
│                                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │ Proxy A  │◄──►│ Proxy B  │◄──►│ Proxy C  │◄──►│ Proxy D  │          │
│  │(sidecar) │    │(sidecar) │    │(sidecar) │    │(sidecar) │          │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘          │
│       │               │               │               │                 │
│  ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐          │
│  │Service A │    │Service B │    │Service C │    │Service D │          │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │
└──────────────────────────────────────────────────────────────────────────┘
```

| Component | Role | Examples |
|---|---|---|
| **Data Plane** | Proxy sidecars that intercept and manage all network traffic between services | Envoy, Linkerd-proxy |
| **Control Plane** | Centralized brain that configures proxies, distributes certs, and enforces policies | istiod, Linkerd control plane, Consul server |

The control plane pushes configuration to the data plane using the **xDS protocol** (a set of discovery service APIs: CDS, EDS, LDS, RDS).

---

### Feature 1: Traffic Management

Traffic management controls **how requests are routed** between services. The mesh intercepts all traffic and applies routing rules declaratively, without touching application code.

#### Capabilities

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAFFIC MANAGEMENT                           │
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │ Request Routing│  │ Traffic        │  │ Traffic        │   │
│  │                │  │ Splitting      │  │ Mirroring      │   │
│  │ Route by:      │  │                │  │                │   │
│  │ • URI path     │  │ v1: 90%        │  │ Send copy of   │   │
│  │ • Headers      │  │ v2: 10%        │  │ live traffic   │   │
│  │ • Query params │  │ (canary)       │  │ to shadow svc  │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │ Retries        │  │ Timeouts       │  │ Header-based   │   │
│  │                │  │                │  │ Routing        │   │
│  │ Auto-retry on  │  │ Per-request    │  │                │   │
│  │ 5xx, reset,    │  │ and per-try    │  │ Route internal │   │
│  │ connect-failure│  │ timeout caps   │  │ users to v2,   │   │
│  │                │  │                │  │ others to v1   │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

#### Canary Deployment (Traffic Splitting)

```
                    ┌─────────────┐
                    │   Incoming   │
                    │   Traffic    │
                    │   (100%)     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ VirtualSvc  │
                    │ (routing    │
                    │  rules)     │
                    └──┬───────┬──┘
                       │       │
                 90%   │       │  10%
                       │       │
                ┌──────▼──┐ ┌──▼──────┐
                │  v1     │ │  v2     │
                │ (stable)│ │(canary) │
                │ 3 pods  │ │ 1 pod   │
                └─────────┘ └─────────┘
```

#### Istio Example: VirtualService + DestinationRule

```yaml
# Route 90% to v1, 10% to v2 (canary deployment)
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
            subset: v1
          weight: 90
        - destination:
            host: my-service
            subset: v2
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 5s
        retryOn: "5xx,reset,connect-failure"
      timeout: 15s
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-service
spec:
  host: my-service
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

#### Header-Based Routing

```yaml
# Route internal testers to v2, everyone else to v1
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
    - my-service
  http:
    - match:
        - headers:
            x-user-group:
              exact: "internal-testers"
      route:
        - destination:
            host: my-service
            subset: v2
    - route:
        - destination:
            host: my-service
            subset: v1
```

#### Traffic Mirroring (Shadow Traffic)

```yaml
# Mirror 100% of production traffic to a shadow service for testing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
            subset: v1
      mirror:
        host: my-service
        subset: v2
      mirrorPercentage:
        value: 100.0  # Mirror all traffic; responses from v2 are discarded
```

---

### Feature 2: Load Balancing

The mesh provides **client-side load balancing** at L7 — each sidecar proxy knows all healthy upstream pod IPs and distributes requests across them directly, bypassing kube-proxy.

#### Load Balancing Algorithms

```
ROUND ROBIN                    LEAST REQUEST                  RANDOM
(default)                      (best for varying latency)     (simple, uniform)

Request 1 → Pod A              Request → Pod with             Request → random Pod
Request 2 → Pod B              fewest active requests
Request 3 → Pod C
Request 4 → Pod A              Better for:                    Good for:
...                             - Uneven processing times      - Large clusters
                                - Mixed workloads               - Stateless services

CONSISTENT HASHING             LOCALITY-AWARE
(sticky sessions)              (prefer nearby pods)

Hash(header/cookie) →          Same zone > Same region > Cross-region
always routes to               Reduces latency and cross-zone costs
same Pod (affinity)
```

#### Comparison: kube-proxy vs Service Mesh Load Balancing

```
kube-proxy (without mesh)              Service Mesh (with Envoy)
┌───────────────────┐                  ┌───────────────────┐
│    Service VIP    │                  │  Envoy Sidecar    │
│   (iptables/IPVS) │                  │  (per-pod proxy)  │
│                   │                  │                   │
│  L4 load balance  │                  │  L7 load balance  │
│  (random/round    │                  │  (round robin,    │
│   robin only)     │                  │   least request,  │
│                   │                  │   consistent hash)│
│  No health check  │                  │                   │
│  No retries       │                  │  Active health    │
│  No circuit break │                  │   checking        │
│  No observability │                  │  Auto retries     │
│                   │                  │  Circuit breaking  │
└───────────────────┘                  │  Full metrics     │
                                       └───────────────────┘
```

#### Istio DestinationRule Example

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-service
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST  # Route to pod with fewest active requests
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 10  # Limit connection reuse (spread load)
```

#### Consistent Hashing (Session Affinity)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-service
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpHeaderName: "x-user-id"  # Same user always hits same pod
        # Alternatives:
        # httpCookie:
        #   name: "session-id"
        #   ttl: 3600s
        # useSourceIp: true
```

---

### Feature 3: Service Discovery

Service discovery answers: **"Where are the instances of Service X right now?"** In a mesh, this happens automatically — services register and deregister as pods scale up/down, and every proxy gets a live endpoint list.

#### How Service Discovery Works in a Mesh

```
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│  1. Pod created → Kubernetes adds Endpoint                       │
│                                                                   │
│     kubectl get endpoints my-service                              │
│     NAME         ENDPOINTS                                        │
│     my-service   10.1.0.5:8080, 10.1.0.6:8080, 10.1.0.7:8080   │
│                                                                   │
│  2. istiod watches Kubernetes API Server                         │
│     (watches Services, Endpoints, Pods)                          │
│                                                                   │
│     ┌──────────────┐       ┌──────────────┐                      │
│     │  Kubernetes  │──────►│   istiod     │                      │
│     │  API Server  │ watch │  (Pilot)     │                      │
│     └──────────────┘       └──────┬───────┘                      │
│                                   │                               │
│  3. istiod pushes endpoint list to all Envoy proxies via xDS     │
│                                   │                               │
│              ┌────────────────────┼────────────────┐              │
│              │                    │                │              │
│              ▼                    ▼                ▼              │
│     ┌──────────────┐    ┌──────────────┐  ┌──────────────┐      │
│     │  Envoy A     │    │  Envoy B     │  │  Envoy C     │      │
│     │  knows:      │    │  knows:      │  │  knows:      │      │
│     │  10.1.0.5    │    │  10.1.0.5    │  │  10.1.0.5    │      │
│     │  10.1.0.6    │    │  10.1.0.6    │  │  10.1.0.6    │      │
│     │  10.1.0.7    │    │  10.1.0.7    │  │  10.1.0.7    │      │
│     └──────────────┘    └──────────────┘  └──────────────┘      │
│                                                                   │
│  4. When a pod dies or scales down, istiod pushes updated list   │
│     Envoy stops routing to dead pod within seconds               │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

#### xDS Discovery APIs

| API | Full Name | Purpose |
|---|---|---|
| **CDS** | Cluster Discovery Service | Which upstream services (clusters) exist |
| **EDS** | Endpoint Discovery Service | Which pod IPs belong to each cluster |
| **LDS** | Listener Discovery Service | What ports/protocols the proxy should listen on |
| **RDS** | Route Discovery Service | How to route requests to the right cluster |
| **SDS** | Secret Discovery Service | TLS certificates for mTLS |

```
App sends request to "http://payment-service:8080/pay"
                │
                ▼
        ┌───────────────┐
        │   Envoy       │
        │               │
        │  LDS: listen  │──► "I should intercept traffic on port 8080"
        │  on 8080      │
        │               │
        │  RDS: route   │──► "payment-service:8080/pay maps to cluster 'payment-service'"
        │  /pay → cluster│
        │               │
        │  CDS: cluster │──► "cluster 'payment-service' uses ROUND_ROBIN, mTLS"
        │  config       │
        │               │
        │  EDS: endpoints│──► "payment-service has pods at 10.1.0.5, 10.1.0.6, 10.1.0.7"
        │               │
        │  SDS: certs   │──► "Use this certificate for mTLS handshake"
        │               │
        └───────┬───────┘
                │
                ▼
        Direct pod-to-pod connection to 10.1.0.6:8080
```

#### Application Code — No Discovery Logic Needed

The beauty of a service mesh is that application code uses plain DNS names:

```python
# Python — just use the Kubernetes service name
import httpx

async def call_payment():
    # Envoy intercepts this, does discovery + load balancing + mTLS
    resp = await httpx.AsyncClient().get("http://payment-service:8080/pay")
    return resp.json()
```

```go
// Go — same simple HTTP call
resp, err := http.Get("http://payment-service:8080/pay")
```

```java
// Java — RestTemplate or WebClient
ResponseEntity<String> resp = restTemplate.getForEntity(
    "http://payment-service:8080/pay", String.class);
```

---

### Feature 4: Fault Injection

Fault injection lets you **deliberately introduce failures** into the system to test resilience. The mesh injects faults at the proxy level — no code changes, no mock servers.

#### Types of Fault Injection

```
┌──────────────────────────────────────────────────────────────────┐
│                     FAULT INJECTION                              │
│                                                                  │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│  │     DELAY FAULT         │  │      ABORT FAULT            │  │
│  │                         │  │                             │  │
│  │  Add artificial latency │  │  Return error code without  │  │
│  │  to responses           │  │  calling upstream           │  │
│  │                         │  │                             │  │
│  │  "What happens if the   │  │  "What happens if the      │  │
│  │   payment service is    │  │   payment service returns   │  │
│  │   slow?"                │  │   500 errors?"              │  │
│  │                         │  │                             │  │
│  │  Request ──► [3s delay] │  │  Request ──► [HTTP 503]     │  │
│  │           ──► Response  │  │           (no upstream call) │  │
│  └─────────────────────────┘  └─────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

#### How It Works

```
Normal flow:
  App A ──► Envoy A ──── mTLS ────► Envoy B ──► App B ──► Response

With delay fault (5s):
  App A ──► Envoy A ──── [WAIT 5 seconds] ──── mTLS ────► Envoy B ──► App B ──► Response

With abort fault (503):
  App A ──► Envoy A ──── [RETURN 503 immediately] ✗ (never reaches Envoy B)
```

#### Istio Fault Injection Examples

```yaml
# Inject a 5-second delay into 10% of requests to payment-service
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
    - payment-service
  http:
    - fault:
        delay:
          percentage:
            value: 10.0     # Affect 10% of requests
          fixedDelay: 5s     # Add 5 seconds of latency
      route:
        - destination:
            host: payment-service
---
# Abort 20% of requests with HTTP 503 (Service Unavailable)
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
    - payment-service
  http:
    - fault:
        abort:
          percentage:
            value: 20.0     # Affect 20% of requests
          httpStatus: 503    # Return 503 error
      route:
        - destination:
            host: payment-service
---
# Combine both: delay + abort for chaos testing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
    - payment-service
  http:
    - fault:
        delay:
          percentage:
            value: 50.0
          fixedDelay: 3s
        abort:
          percentage:
            value: 10.0
          httpStatus: 500
      route:
        - destination:
            host: payment-service
```

#### Why Fault Injection Matters — Chaos Engineering

```
Production Scenario:
  Order Service ──► Payment Service (normally 100ms response)

Question: What happens when Payment Service has 5s latency?

Without testing:  Order Service hangs → cascading timeout → entire system down
With fault injection:  Discover the bug in staging, add timeout + circuit breaker

                    ┌─────────────────────────┐
                    │   Resilience Patterns    │
                    │   discovered via fault   │
                    │   injection:             │
                    │                         │
                    │   • Timeouts needed?     │
                    │   • Retries idempotent?  │
                    │   • Circuit breaker set? │
                    │   • Fallback defined?    │
                    │   • Graceful degradation?│
                    └─────────────────────────┘
```

---

### Feature 5: Circuit Breaking

Circuit breaking **prevents cascading failures** by stopping requests to an unhealthy service. If a service starts returning errors or becomes slow, the circuit "opens" and requests fail fast instead of piling up.

#### Circuit Breaker State Machine

```
                 ┌──────────────────────────────────────────────────┐
                 │                                                  │
      success    │    ┌────────────┐    failures exceed    ┌───────▼──────┐
   ┌─────────────┼───►│  CLOSED    │    threshold          │    OPEN      │
   │             │    │ (normal)   │──────────────────────►│ (failing fast)│
   │             │    │            │                        │              │
   │             │    │ All requests│                        │ All requests │
   │             │    │ pass through│                        │ rejected     │
   │             │    └────────────┘                        │ immediately  │
   │             │          ▲                               └──────┬───────┘
   │             │          │                                      │
   │             │          │ success                    timeout    │
   │             │          │                           expires    │
   │             │    ┌─────┴──────────┐                          │
   │             │    │  HALF-OPEN     │◄─────────────────────────┘
   │             │    │                │
   │             └────│ Allow limited  │
   │                  │ test requests  │
   │                  │ to check if    │
   │                  │ service is back│
   │                  └────────┬───────┘
   │                           │
   │                    failure │
   │                           │
   │                  ┌────────▼───────┐
   └──────────────────│    OPEN        │ (go back to OPEN)
                      └────────────────┘
```

#### Without vs With Circuit Breaking

```
WITHOUT CIRCUIT BREAKING:

Client ──► Service A ──► Service B (failing)
                              │
                         ┌────┴────┐
                         │ Timeout │ (30s)
                         │ waiting │
                         └────┬────┘
                              │
              ┌───────────────▼───────────────┐
              │  Meanwhile, requests pile up:  │
              │  Thread 1: waiting...          │
              │  Thread 2: waiting...          │
              │  Thread 3: waiting...          │
              │  ...                           │
              │  Thread pool exhausted!        │
              │  Service A ALSO goes down!     │
              │  ══► CASCADING FAILURE         │
              └───────────────────────────────┘

WITH CIRCUIT BREAKING:

Client ──► Service A ──► Service B (failing)
                              │
                    ┌─────────▼──────────┐
                    │ Circuit OPENS after│
                    │ 3 consecutive 5xx  │
                    └─────────┬──────────┘
                              │
              ┌───────────────▼───────────────┐
              │  Subsequent requests:          │
              │  → Fail IMMEDIATELY (no wait) │
              │  → Return 503 to caller        │
              │  → Service A stays healthy     │
              │  → No cascading failure        │
              │                                │
              │  After 30s: try one request    │
              │  → Success? Close circuit      │
              │  → Failure? Keep circuit open  │
              └───────────────────────────────┘
```

#### Istio Circuit Breaking via Outlier Detection

In Istio, circuit breaking is implemented through **outlier detection** in `DestinationRule`. It works by ejecting (removing) unhealthy pods from the load balancing pool.

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100        # Max concurrent TCP connections
      http:
        http1MaxPendingRequests: 50  # Max queued requests waiting for connection
        http2MaxRequests: 100       # Max concurrent HTTP/2 requests
        maxRequestsPerConnection: 10 # Close connection after 10 requests
        maxRetries: 3                # Max parallel retries
    outlierDetection:
      consecutive5xxErrors: 3      # Eject pod after 3 consecutive 5xx errors
      interval: 10s                # Check every 10 seconds
      baseEjectionTime: 30s        # Eject for at least 30 seconds
      maxEjectionPercent: 50       # Never eject more than 50% of pods
      minHealthPercent: 30         # Only do outlier detection if >30% pods healthy
```

**How outlier detection works:**

```
Pod pool: [A, B, C, D]

1. Pod C returns 3 consecutive 5xx errors
2. Envoy ejects Pod C from pool
3. Traffic splits across [A, B, D] only
4. After 30s, Envoy tries Pod C again (half-open)
5. If Pod C is healthy → add back to pool
6. If Pod C still failing → eject for 60s (exponential backoff)

Timeline:
  t=0   [A ✓] [B ✓] [C ✓] [D ✓]   ← All healthy
  t=5   [A ✓] [B ✓] [C ✗] [D ✓]   ← C returns 3x 5xx
  t=6   [A ✓] [B ✓] [C ⊘] [D ✓]   ← C ejected (circuit open)
  t=36  [A ✓] [B ✓] [C ?] [D ✓]   ← Try C again (half-open)
  t=37  [A ✓] [B ✓] [C ✓] [D ✓]   ← C recovered (circuit closed)
```

---

### Feature 6: Observability

A service mesh provides **three pillars of observability** automatically — without adding any instrumentation to your application code.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     THREE PILLARS OF OBSERVABILITY                           │
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐     │
│  │      METRICS       │  │     TRACES         │  │      LOGS          │     │
│  │                    │  │                    │  │                    │     │
│  │  Quantitative data │  │  End-to-end request│  │  Detailed event   │     │
│  │  about system      │  │  flow across       │  │  records for each │     │
│  │  behavior          │  │  services          │  │  request           │     │
│  │                    │  │                    │  │                    │     │
│  │  • Request rate    │  │  • Latency per hop │  │  • Access logs    │     │
│  │  • Error rate      │  │  • Service         │  │  • Request headers│     │
│  │  • Latency (p50,   │  │    dependency map  │  │  • Response codes │     │
│  │    p95, p99)       │  │  • Bottleneck      │  │  • Upstream info  │     │
│  │  • Throughput      │  │    identification  │  │  • TLS details    │     │
│  │  • Connection pool │  │                    │  │                    │     │
│  │                    │  │                    │  │                    │     │
│  │  Tool: Prometheus  │  │  Tool: Jaeger /    │  │  Tool: Envoy      │     │
│  │        + Grafana   │  │        Zipkin      │  │        access logs │     │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘     │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    SERVICE GRAPH / TOPOLOGY                          │   │
│  │                    Tool: Kiali                                        │   │
│  │                                                                      │   │
│  │    Visualize which services talk to which, traffic flow, errors      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Golden Signals (What Envoy Reports Automatically)

```
For EVERY request through the mesh, Envoy emits:

┌──────────────────────────────────────────────────────────────┐
│  Metric                    │  Prometheus Metric Name         │
│────────────────────────────│─────────────────────────────────│
│  Request count             │  istio_requests_total           │
│  Request duration          │  istio_request_duration_ms      │
│  Request size              │  istio_request_bytes            │
│  Response size             │  istio_response_bytes           │
│  TCP connections opened    │  istio_tcp_connections_opened   │
│  TCP connections closed    │  istio_tcp_connections_closed   │
│  TCP bytes sent            │  istio_tcp_sent_bytes_total     │
│  TCP bytes received        │  istio_tcp_received_bytes_total │
└──────────────────────────────────────────────────────────────┘

Labels include: source, destination, response_code, method, etc.
```

#### Distributed Tracing Flow

```
User request: POST /api/order

┌─────────────────────────────────────────────────────────────────────────┐
│  Trace ID: abc-123                                                      │
│                                                                         │
│  ┌──────────────────────────────────────────────────────┐  0ms          │
│  │ Span 1: Gateway → Order Service  (200ms total)       │              │
│  │  ┌─────────────────────────────────────┐  20ms        │              │
│  │  │ Span 2: Order → Inventory (50ms)    │              │              │
│  │  └─────────────────────────────────────┘  70ms        │              │
│  │  ┌──────────────────────────────────────────────┐ 75ms│              │
│  │  │ Span 3: Order → Payment (100ms)              │     │              │
│  │  │  ┌────────────────────────┐  80ms             │     │              │
│  │  │  │ Span 4: Payment → Bank│  (60ms)           │     │              │
│  │  │  └────────────────────────┘  140ms            │     │              │
│  │  └──────────────────────────────────────────────┘175ms│              │
│  │  ┌──────────────────┐  180ms                          │              │
│  │  │ Span 5: Order →  │                                 │              │
│  │  │ Notification(10ms)│                                 │              │
│  │  └──────────────────┘  190ms                          │              │
│  └──────────────────────────────────────────────────────┘  200ms        │
│                                                                         │
│  Bottleneck identified: Payment → Bank call (60ms) is the slowest hop  │
└─────────────────────────────────────────────────────────────────────────┘
```

The Envoy sidecar automatically propagates trace headers (`x-request-id`, `x-b3-traceid`, etc.) — services just need to forward these headers on outbound calls.

#### Istio Telemetry Configuration

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-defaults
  namespace: istio-system  # Mesh-wide
spec:
  accessLogging:
    - providers:
        - name: envoy
  tracing:
    - providers:
        - name: jaeger
      randomSamplingPercentage: 10  # Sample 10% in production
  metrics:
    - providers:
        - name: prometheus
```

---

### Feature 7: Security (mTLS)

**Mutual TLS (mTLS)** encrypts all service-to-service communication and provides **mutual authentication** — both sides verify each other's identity via certificates.

#### How mTLS Works in a Service Mesh

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        mTLS HANDSHAKE                                    │
│                                                                          │
│   Service A (client)                         Service B (server)          │
│   Envoy Sidecar                              Envoy Sidecar              │
│                                                                          │
│   1. ClientHello ──────────────────────────►                             │
│      (supported ciphers, TLS version)                                    │
│                                                                          │
│   2. ◄──────────────────────────── ServerHello                           │
│      (chosen cipher, server certificate)                                 │
│                                                                          │
│   3. Client verifies server cert                                         │
│      against CA (istiod/Citadel)                                         │
│      ✓ "Yes, this is really Service B"                                   │
│                                                                          │
│   4. Client sends its certificate ─────────►                             │
│      (this is the MUTUAL part)                                           │
│                                                                          │
│   5.                    Server verifies client cert                      │
│                         against CA (istiod/Citadel)                      │
│                         ✓ "Yes, this is really Service A"                │
│                                                                          │
│   6. ◄────── Encrypted channel established ──────►                      │
│      Both sides have verified identity                                   │
│      All traffic encrypted with TLS 1.3                                  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

#### SPIFFE Identity

Istio uses **SPIFFE (Secure Production Identity Framework For Everyone)** to assign identities:

```
Each service gets a SPIFFE identity encoded in its X.509 certificate:

  spiffe://cluster.local/ns/production/sa/payment-service
  ─────── ───────────── ── ────────── ── ───────────────
    │          │          │      │      │        │
  scheme    trust       namespace    service  service
            domain      identifier   account  account
                                     prefix   name

This identity is used in AuthorizationPolicy to control
which services can talk to which:

  "Allow spiffe://cluster.local/ns/production/sa/order-service
   to call spiffe://cluster.local/ns/production/sa/payment-service"
```

#### Certificate Lifecycle

```
┌──────────────────────────────────────────────────────────────────┐
│                    CERTIFICATE MANAGEMENT                        │
│                                                                  │
│  ┌──────────┐                                                    │
│  │  istiod   │  (built-in Certificate Authority)                │
│  │  Citadel  │                                                   │
│  └─────┬─────┘                                                   │
│        │                                                         │
│        │  1. Pod starts → istio-agent (in sidecar) sends CSR    │
│        │  2. istiod validates pod identity via K8s SA token      │
│        │  3. istiod signs certificate (default: 24h validity)    │
│        │  4. Certificate delivered to Envoy via SDS              │
│        │  5. Before expiry → auto-rotate (no downtime)           │
│        │                                                         │
│        ▼                                                         │
│  ┌──────────────┐                                                │
│  │  Envoy       │  cert valid: 24 hours                         │
│  │  Sidecar     │  auto-renewed before expiry                    │
│  │              │  zero-downtime rotation                         │
│  │  Private key │  key never leaves the pod                      │
│  │  never sent  │  stored in memory (not on disk)                │
│  │  over network│                                                │
│  └──────────────┘                                                │
└──────────────────────────────────────────────────────────────────┘
```

#### mTLS Modes

```yaml
# STRICT: All traffic MUST be mTLS (reject plaintext)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# PERMISSIVE: Accept both mTLS and plaintext (for migration)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: PERMISSIVE  # Use during mesh rollout, switch to STRICT when ready
---
# DISABLE: No mTLS (not recommended)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: DISABLE
```

#### Authorization Policies (Zero-Trust)

```yaml
# Deny all by default (zero-trust baseline)
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}  # Empty spec = deny everything
---
# Allow only order-service to call payment-service
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-order-to-payment
  namespace: production
spec:
  selector:
    matchLabels:
      app: payment-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/production/sa/order-service"
      to:
        - operation:
            methods: ["POST"]
            paths: ["/api/pay"]
```

---

### Popular Solutions Comparison

#### Istio

```
┌──────────────────────────────────────────────────────────────────┐
│  ISTIO                                                           │
│  "The most feature-rich service mesh"                           │
│                                                                  │
│  Control Plane: istiod (merged Pilot + Citadel + Galley)        │
│  Data Plane:    Envoy proxy (sidecar)                           │
│                                                                  │
│  ✅ Strengths:                                                   │
│  • Most features (traffic, security, observability)              │
│  • Largest community and ecosystem                               │
│  • Extensive documentation                                       │
│  • Multi-cluster and multi-mesh support                          │
│  • Fine-grained AuthorizationPolicy                              │
│  • Built-in certificate authority                                │
│  • VirtualService + DestinationRule (powerful traffic control)   │
│  • EnvoyFilter for custom proxy configuration                    │
│                                                                  │
│  ❌ Weaknesses:                                                  │
│  • Highest resource overhead (~50-100MB per sidecar)             │
│  • Complex configuration (steep learning curve)                  │
│  • Envoy sidecar adds ~2-5ms latency per hop                    │
│  • Many CRDs to manage                                           │
│                                                                  │
│  Best for: Large organizations, complex multi-cluster setups,   │
│  teams that need maximum control and features                    │
└──────────────────────────────────────────────────────────────────┘
```

**Istio Architecture:**

```
┌──────────────────────────────────────────────────────────────────┐
│                     istiod (Control Plane)                       │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │   Pilot    │  │  Citadel   │  │   Galley   │                │
│  │            │  │            │  │            │                │
│  │ Service    │  │ Certificate│  │ Config     │                │
│  │ discovery  │  │ authority  │  │ validation │                │
│  │ Traffic    │  │ mTLS cert  │  │ & distrib. │                │
│  │ management │  │ management │  │            │                │
│  │ xDS API    │  │ SPIFFE     │  │ Watches    │                │
│  │            │  │ identity   │  │ K8s API    │                │
│  └────────────┘  └────────────┘  └────────────┘                │
└──────────────────────────┬───────────────────────────────────────┘
                           │ xDS (gRPC streaming)
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Envoy   │ │  Envoy   │ │  Envoy   │
        │ (sidecar)│ │ (sidecar)│ │ (sidecar)│
        │          │ │          │ │          │
        │ Service A│ │ Service B│ │ Service C│
        └──────────┘ └──────────┘ └──────────┘
```

**Install Istio:**

```bash
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Production profile (minimal, no addons)
istioctl install --set profile=default -y

# Demo profile (includes Kiali, Jaeger, Prometheus, Grafana)
istioctl install --set profile=demo -y

# Enable sidecar injection for a namespace
kubectl label namespace my-app istio-injection=enabled

# Verify
istioctl analyze
```

#### Linkerd

```
┌──────────────────────────────────────────────────────────────────┐
│  LINKERD                                                         │
│  "The lightweight, simple service mesh"                         │
│                                                                  │
│  Control Plane: Linkerd control plane (Go)                      │
│  Data Plane:    linkerd2-proxy (Rust, purpose-built)            │
│                                                                  │
│  ✅ Strengths:                                                   │
│  • Ultra-lightweight proxy (~10MB memory per sidecar)            │
│  • Minimal latency overhead (~1ms per hop)                       │
│  • Simplest to install and operate                               │
│  • mTLS enabled by default (zero config)                         │
│  • Fastest time-to-value                                         │
│  • CNCF graduated project                                        │
│  • Purpose-built proxy (not general-purpose Envoy)               │
│                                                                  │
│  ❌ Weaknesses:                                                  │
│  • Fewer features than Istio                                     │
│  • No VirtualService/DestinationRule equivalent (less traffic   │
│    management flexibility)                                       │
│  • Smaller ecosystem and fewer integrations                      │
│  • No built-in ingress gateway                                   │
│  • No EnvoyFilter equivalent for custom proxy config             │
│                                                                  │
│  Best for: Small-medium teams, platform teams wanting            │
│  simplicity, when mTLS + observability is the primary need       │
└──────────────────────────────────────────────────────────────────┘
```

**Linkerd Architecture:**

```
┌──────────────────────────────────────────────────────────────────┐
│               Linkerd Control Plane                              │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ Destination│  │  Identity  │  │   Proxy    │                │
│  │ Controller │  │  Service   │  │  Injector  │                │
│  │            │  │            │  │            │                │
│  │ Service    │  │ mTLS cert  │  │ Webhook to │                │
│  │ discovery  │  │ management │  │ auto-inject│                │
│  │ & config   │  │ (auto-     │  │ sidecar    │                │
│  │            │  │  rotate)   │  │            │                │
│  └────────────┘  └────────────┘  └────────────┘                │
└──────────────────────────────────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │linkerd2  │ │linkerd2  │ │linkerd2  │
        │-proxy    │ │-proxy    │ │-proxy    │
        │(Rust)    │ │(Rust)    │ │(Rust)    │
        │~10MB RAM │ │~10MB RAM │ │~10MB RAM │
        │          │ │          │ │          │
        │Service A │ │Service B │ │Service C │
        └──────────┘ └──────────┘ └──────────┘
```

**Install Linkerd:**

```bash
# Install CLI
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$HOME/.linkerd2/bin:$PATH

# Pre-check cluster
linkerd check --pre

# Install control plane
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -

# Verify
linkerd check

# Inject sidecars into a namespace
kubectl get deploy -n my-app -o yaml | linkerd inject - | kubectl apply -f -

# Or annotate the namespace for auto-injection
kubectl annotate namespace my-app linkerd.io/inject=enabled

# Install observability extension (Prometheus, Grafana)
linkerd viz install | kubectl apply -f -
linkerd viz dashboard  # Opens browser
```

**Linkerd Traffic Split (SMI):**

```yaml
# Linkerd uses the SMI (Service Mesh Interface) spec for traffic splitting
apiVersion: split.smi-spec.io/v1alpha2
kind: TrafficSplit
metadata:
  name: my-service
  namespace: my-app
spec:
  service: my-service     # Root service
  backends:
    - service: my-service-v1
      weight: 90           # 90% to v1
    - service: my-service-v2
      weight: 10           # 10% to v2
```

#### Consul Connect

```
┌──────────────────────────────────────────────────────────────────┐
│  CONSUL CONNECT                                                  │
│  "Service mesh built on HashiCorp's service discovery"          │
│                                                                  │
│  Control Plane: Consul Server (Go)                              │
│  Data Plane:    Envoy proxy (or built-in Connect proxy)         │
│                                                                  │
│  ✅ Strengths:                                                   │
│  • Works across Kubernetes AND VMs/bare metal                    │
│  • Built-in service discovery + health checking (Consul core)   │
│  • Multi-datacenter support out of the box                       │
│  • Intentions (simple allow/deny security model)                 │
│  • HashiCorp ecosystem integration (Vault, Terraform, Nomad)    │
│  • Service discovery for non-mesh services too                   │
│  • Key/value store for config management                         │
│                                                                  │
│  ❌ Weaknesses:                                                  │
│  • Less traffic management features than Istio                   │
│  • Consul servers are stateful (need careful operations)         │
│  • Smaller Kubernetes-native community vs Istio/Linkerd          │
│  • More operational complexity (Consul cluster management)       │
│  • Not a CNCF project (HashiCorp BSL license)                   │
│                                                                  │
│  Best for: Hybrid environments (K8s + VMs), HashiCorp shops,    │
│  multi-datacenter deployments, existing Consul users             │
└──────────────────────────────────────────────────────────────────┘
```

**Consul Connect Architecture:**

```
┌──────────────────────────────────────────────────────────────────┐
│             Consul Server Cluster (3 or 5 nodes)                 │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │   Leader   │  │  Follower  │  │  Follower  │                │
│  │   Server   │◄─┤   Server   │◄─┤   Server   │                │
│  │            │  │            │  │            │                │
│  │ • Service  │  │ • Raft     │  │ • Raft     │                │
│  │   catalog  │  │   replica  │  │   replica  │                │
│  │ • Intentions│ │            │  │            │                │
│  │ • CA       │  │            │  │            │                │
│  │ • KV store │  │            │  │            │                │
│  └──────┬─────┘  └────────────┘  └────────────┘                │
│         │                                                        │
│         │  ┌──────────────────────────────┐                      │
│         ├──┤  Kubernetes (via consul-k8s) │                      │
│         │  └──────────────────────────────┘                      │
│         │  ┌──────────────────────────────┐                      │
│         └──┤  VMs (via consul agent)      │                      │
│            └──────────────────────────────┘                      │
└──────────────────────────────────────────────────────────────────┘

On each pod/VM:
┌─────────────────────┐
│  ┌───────────────┐  │
│  │  Application  │  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │ Envoy Proxy   │  │  (or Connect native proxy)
│  │ (sidecar)     │  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │ Consul Agent  │  │  (registers service, health checks)
│  └───────────────┘  │
└─────────────────────┘
```

**Consul Intentions (Security):**

```bash
# Allow order-service to talk to payment-service
consul intention create order-service payment-service

# Deny all by default
consul intention create -deny '*' '*'

# Allow specific
consul intention create -allow web api
consul intention create -allow api database
```

```hcl
# Consul config file (HCL)
Kind = "service-intentions"
Name = "payment-service"
Sources = [
  {
    Name   = "order-service"
    Action = "allow"
  },
  {
    Name   = "*"       # Everything else
    Action = "deny"
  }
]
```

### Head-to-Head Comparison

| Feature | Istio | Linkerd | Consul Connect |
|---|---|---|---|
| **Data Plane Proxy** | Envoy (C++) | linkerd2-proxy (Rust) | Envoy (C++) |
| **Memory per Sidecar** | ~50-100 MB | ~10-20 MB | ~50-100 MB |
| **Latency Overhead** | ~2-5 ms | ~1 ms | ~2-5 ms |
| **mTLS** | Yes (configurable) | Yes (on by default) | Yes (via Connect) |
| **Traffic Splitting** | VirtualService (powerful) | TrafficSplit (SMI) | Splitter config |
| **Fault Injection** | Yes (delay + abort) | No (use chaos tools) | No |
| **Circuit Breaking** | Yes (outlier detection) | Basic (via retries) | Yes |
| **Multi-cluster** | Yes (advanced) | Yes (multi-cluster) | Yes (multi-DC native) |
| **VM Support** | Yes (WorkloadEntry) | No (K8s only) | Yes (native) |
| **Complexity** | High | Low | Medium |
| **License** | Apache 2.0 | Apache 2.0 | BSL (HashiCorp) |
| **CNCF Status** | Graduated | Graduated | Not CNCF |
| **Best For** | Feature-rich, large orgs | Simplicity, low overhead | Hybrid K8s + VM |

### When to Use a Service Mesh

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  USE a service mesh when:                                               │
│  ✓ You have >10 microservices                                           │
│  ✓ Services are written in multiple languages                           │
│  ✓ You need mTLS between all services (compliance, zero-trust)          │
│  ✓ You need fine-grained traffic control (canary, A/B testing)          │
│  ✓ You need consistent observability across all services                │
│  ✓ You want to decouple networking from application code                │
│  ✓ You operate across multiple clusters or clouds                       │
│                                                                         │
│  DON'T use a service mesh when:                                         │
│  ✗ You have <5 services (overkill)                                      │
│  ✗ All services are in one language with good libraries                  │
│  ✗ You can't accept the resource overhead (each sidecar uses memory)   │
│  ✗ Your team doesn't have Kubernetes expertise                          │
│  ✗ Latency is ultra-critical (sub-millisecond requirements)             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Service Mesh vs API Gateway vs Load Balancer

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│                  │  Load Balancer   │  API Gateway     │  Service Mesh    │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Traffic          │ North-South      │ North-South      │ East-West        │
│ Direction        │ (external→int)   │ (external→int)   │ (service→service)│
│                  │                  │                  │                  │
│ OSI Layer        │ L4 (TCP/UDP)     │ L7 (HTTP)        │ L7 (HTTP/gRPC)   │
│                  │                  │                  │                  │
│ Deployment       │ Centralized      │ Centralized      │ Distributed      │
│                  │ (edge)           │ (edge)           │ (per-pod sidecar)│
│                  │                  │                  │                  │
│ Scope            │ Ingress only     │ Ingress +        │ All internal     │
│                  │                  │ API management   │ communication    │
│                  │                  │                  │                  │
│ Auth             │ No               │ API keys, OAuth  │ mTLS (identity)  │
│                  │                  │                  │                  │
│ Rate Limiting    │ Basic            │ Advanced         │ Per-service      │
│                  │                  │                  │                  │
│ Observability    │ Basic metrics    │ API analytics    │ Full distributed │
│                  │                  │                  │ tracing + metrics│
│                  │                  │                  │                  │
│ Examples         │ AWS ALB, HAProxy │ Kong, Apigee     │ Istio, Linkerd   │
│                  │ Nginx            │ AWS API Gateway  │ Consul Connect   │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘

                External Users
                     │
              ┌──────▼──────┐
              │ Load Balancer│  ← L4 traffic distribution
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │ API Gateway  │  ← Auth, rate limit, transform
              └──────┬──────┘
                     │
            ─────────┼─────────  (cluster boundary)
                     │
              ┌──────▼──────┐
              │Service Mesh  │  ← mTLS, discovery, routing
              │ (east-west)  │     between internal services
              └──────────────┘
```

---

## End-to-End Service Mesh: Distributed Workflow Management System

### Use Case Overview

A **Distributed Workflow Management System** used in scientific computing environments. The system manages computational workflows across heterogeneous infrastructure — submitting jobs, managing data, authenticating users, and orchestrating batch/interactive workloads.

Each component is written in a **different language**, has **multiple replicas**, and they all need secure, observable, resilient communication — a perfect use case for a service mesh.

### System Components

| Component | Language | Purpose | Replicas |
|---|---|---|---|
| **Science Gateway** | Python (FastAPI) | Web portal for scientists to submit and monitor workflows | 3 |
| **IAM (Identity & Access Management)** | Go | Authentication, authorization, token validation | 2 |
| **Global Wrapper Execution API** | Java (Spring Boot) | Orchestrates workflow execution across clusters | 3 |
| **Local Batch Execution API** | Go | Submits and manages batch jobs (HPC/Slurm) | 2 per cluster |
| **Local Interactive API** | Python (Flask) | Manages interactive sessions (Jupyter, RStudio) | 2 per cluster |
| **Data Management** | Java (Quarkus) | File transfers, metadata management, data catalog | 2 |
| **Local Datalake / S3** | MinIO (Go-based) | Object storage for workflow inputs/outputs | 3 (distributed) |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          KUBERNETES CLUSTER                                     │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                     ISTIO CONTROL PLANE                                  │   │
│  │  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐   │   │
│  │  │  istiod  │  │  Pilot   │  │  Citadel │  │  Galley (Config Mgmt) │   │   │
│  │  │ (core)   │  │ (xDS)    │  │ (mTLS/   │  │                       │   │   │
│  │  │          │  │          │  │  certs)   │  │                       │   │   │
│  │  └─────────┘  └──────────┘  └──────────┘  └────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                     ISTIO INGRESS GATEWAY                                │   │
│  │              (TLS termination, external traffic entry)                   │   │
│  └──────────────────────────┬───────────────────────────────────────────────┘   │
│                             │                                                   │
│          ┌──────────────────┼──────────────────────────────┐                   │
│          │                  │                               │                   │
│          ▼                  ▼                               ▼                   │
│  ┌───────────────┐  ┌───────────────┐              ┌───────────────┐           │
│  │Science Gateway│  │Science Gateway│              │Science Gateway│           │
│  │  (Python)     │  │  (Python)     │    ...       │  (Python)     │           │
│  │ ┌───────────┐ │  │ ┌───────────┐ │              │ ┌───────────┐ │           │
│  │ │Envoy Proxy│ │  │ │Envoy Proxy│ │              │ │Envoy Proxy│ │           │
│  │ │ (sidecar) │ │  │ │ (sidecar) │ │              │ │ (sidecar) │ │           │
│  │ └───────────┘ │  │ └───────────┘ │              │ └───────────┘ │           │
│  └───────┬───────┘  └───────┬───────┘              └───────┬───────┘           │
│          │                  │                               │                   │
│          ▼                  ▼                               ▼                   │
│  ┌─────────────────────────────────────────────────────────────────────┐        │
│  │                    MESH INTERNAL TRAFFIC (mTLS)                     │        │
│  │                                                                     │        │
│  │  ┌───────────┐  ┌─────────────────┐  ┌───────────────────────┐     │        │
│  │  │    IAM    │  │ Global Wrapper  │  │   Data Management     │     │        │
│  │  │   (Go)    │  │ Execution API   │  │   (Java/Quarkus)      │     │        │
│  │  │ x2 pods   │  │ (Java/Spring)   │  │   x2 pods             │     │        │
│  │  │ +sidecar  │  │ x3 pods         │  │   +sidecar            │     │        │
│  │  └─────┬─────┘  │ +sidecar        │  └───────────┬───────────┘     │        │
│  │        │         └────────┬────────┘              │                 │        │
│  │        │                  │                       │                 │        │
│  │        │         ┌────────┴────────┐              │                 │        │
│  │        │         │                 │              │                 │        │
│  │        ▼         ▼                 ▼              ▼                 │        │
│  │  ┌───────────┐  ┌───────────┐  ┌─────────────────────┐            │        │
│  │  │Local Batch│  │Local Inter│  │  Local Datalake/S3  │            │        │
│  │  │Exec API   │  │active API │  │  (MinIO)            │            │        │
│  │  │  (Go)     │  │ (Python)  │  │  x3 pods            │            │        │
│  │  │ x2 pods   │  │ x2 pods   │  │  +sidecar           │            │        │
│  │  │ +sidecar  │  │ +sidecar  │  │                     │            │        │
│  │  └───────────┘  └───────────┘  └─────────────────────┘            │        │
│  └─────────────────────────────────────────────────────────────────────┘        │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                     OBSERVABILITY STACK                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐                   │   │
│  │  │Prometheus│  │ Grafana  │  │  Jaeger   │  │  Kiali │                   │   │
│  │  │(metrics) │  │(dashbrd) │  │(tracing)  │  │(mesh   │                   │   │
│  │  │          │  │          │  │           │  │ viz)   │                   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘                   │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Request Flow Through the Mesh

```
Scientist (Browser)
       │
       ▼
┌─────────────────┐
│  Istio Ingress  │  ← TLS termination, routing rules
│  Gateway        │
└────────┬────────┘
         │ (mTLS)
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Science Gateway │────►│      IAM        │  ← Token validation
│  Envoy ◄──► App │     │  Envoy ◄──► App │
└────────┬────────┘     └─────────────────┘
         │ (mTLS, JWT validated)
         ▼
┌─────────────────────────┐
│ Global Wrapper Exec API │  ← Orchestrates workflow
│   Envoy ◄──► App        │
└────────┬────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────────┐    ┌──────────────┐
│ Batch  │ │Interactive │    │    Data       │
│ Exec   │ │  API       │───►│  Management  │
│ API    │ │            │    │              │
└────┬───┘ └────────────┘    └──────┬───────┘
     │                              │
     └──────────┬───────────────────┘
                ▼
        ┌──────────────┐
        │ Local S3 /   │
        │ Datalake     │
        └──────────────┘
```

---

### Step 1: Kubernetes Namespace and Istio Setup

#### 1.1 Install Istio

```bash
# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*

# Install with demo profile (includes observability addons)
istioctl install --set profile=demo -y

# Verify installation
kubectl get pods -n istio-system
```

#### 1.2 Namespace Configuration

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: workflow-system
  labels:
    istio-injection: enabled  # Auto-inject Envoy sidecar into every pod
    app.kubernetes.io/part-of: distributed-workflow
---
apiVersion: v1
kind: Namespace
metadata:
  name: observability
  labels:
    istio-injection: disabled
```

```bash
kubectl apply -f namespace.yaml
```

> The label `istio-injection: enabled` tells Istio's admission webhook to automatically inject an Envoy sidecar container into every pod created in this namespace. No manual sidecar configuration needed per deployment.

---

### Step 2: mTLS Configuration (Strict Mode)

#### 2.1 Mesh-Wide Strict mTLS

```yaml
# peer-authentication.yaml
# Enforce mTLS across the entire mesh — no plaintext allowed
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: workflow-system
spec:
  mtls:
    mode: STRICT  # All traffic must be mTLS encrypted
```

#### 2.2 Destination Rules for mTLS

```yaml
# destination-rule-mtls.yaml
# Tell all clients in the mesh to use ISTIO_MUTUAL TLS when connecting
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: mesh-wide-mtls
  namespace: workflow-system
spec:
  host: "*.workflow-system.svc.cluster.local"
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL  # Use Istio-managed certificates automatically
```

**How mTLS works in Istio:**

```
Pod A (App Container)                    Pod B (App Container)
        │                                         ▲
        │ plaintext HTTP                          │ plaintext HTTP
        ▼                                         │
┌───────────────┐                        ┌───────────────┐
│  Envoy Proxy  │ ──── mTLS tunnel ────► │  Envoy Proxy  │
│  (Sidecar A)  │                        │  (Sidecar B)  │
│               │                        │               │
│ Has cert +    │  mutual certificate    │ Has cert +    │
│ private key   │  verification via      │ private key   │
│ from Citadel  │  Citadel (istiod)      │ from Citadel  │
└───────────────┘                        └───────────────┘
```

- The application code speaks **plain HTTP** to `localhost`
- The Envoy sidecar **intercepts** outbound traffic, encrypts it with mTLS
- The receiving Envoy sidecar **decrypts** and forwards plain HTTP to the app
- Certificates are **automatically rotated** by istiod (Citadel component)

---

### Step 3: Component Implementations

#### 3.1 IAM Service (Go)

```go
// iam-service/main.go
package main

import (
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"sync"
	"time"
)

// Token represents an issued authentication token
type Token struct {
	AccessToken string `json:"access_token"`
	TokenType   string `json:"token_type"`
	ExpiresIn   int    `json:"expires_in"`
	Roles       []string `json:"roles"`
	Subject     string `json:"subject"`
}

// TokenStore holds valid tokens (in production, use Redis or a DB)
type TokenStore struct {
	mu     sync.RWMutex
	tokens map[string]*TokenInfo
}

type TokenInfo struct {
	Subject   string
	Roles     []string
	ExpiresAt time.Time
}

var store = &TokenStore{tokens: make(map[string]*TokenInfo)}

func generateToken() string {
	b := make([]byte, 32)
	rand.Read(b)
	return base64.URLEncoding.EncodeToString(b)
}

// POST /auth/login — issues a token
func loginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var creds struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}
	if err := json.NewDecoder(r.Body).Decode(&creds); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Simplified auth — in production, check against a user database
	if creds.Username == "" || creds.Password == "" {
		http.Error(w, "Missing credentials", http.StatusUnauthorized)
		return
	}

	token := generateToken()
	store.mu.Lock()
	store.tokens[token] = &TokenInfo{
		Subject:   creds.Username,
		Roles:     []string{"scientist", "data-reader"},
		ExpiresAt: time.Now().Add(1 * time.Hour),
	}
	store.mu.Unlock()

	resp := Token{
		AccessToken: token,
		TokenType:   "Bearer",
		ExpiresIn:   3600,
		Roles:       []string{"scientist", "data-reader"},
		Subject:     creds.Username,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// GET /auth/validate — validates a Bearer token
func validateHandler(w http.ResponseWriter, r *http.Request) {
	authHeader := r.Header.Get("Authorization")
	if !strings.HasPrefix(authHeader, "Bearer ") {
		http.Error(w, "Missing or invalid Authorization header", http.StatusUnauthorized)
		return
	}

	token := strings.TrimPrefix(authHeader, "Bearer ")

	store.mu.RLock()
	info, exists := store.tokens[token]
	store.mu.RUnlock()

	if !exists || time.Now().After(info.ExpiresAt) {
		http.Error(w, "Token invalid or expired", http.StatusUnauthorized)
		return
	}

	resp := map[string]interface{}{
		"valid":   true,
		"subject": info.Subject,
		"roles":   info.Roles,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// GET /health — health check for Kubernetes probes
func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/auth/login", loginHandler)
	mux.HandleFunc("/auth/validate", validateHandler)
	mux.HandleFunc("/health", healthHandler)

	server := &http.Server{
		Addr:         ":8080",
		Handler:      mux,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	fmt.Println("IAM Service starting on :8080")
	log.Fatal(server.ListenAndServe())
}
```

```dockerfile
# iam-service/Dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o iam-service .

FROM alpine:3.19
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/iam-service /usr/local/bin/
EXPOSE 8080
USER 1000:1000
ENTRYPOINT ["iam-service"]
```

#### 3.2 Science Gateway (Python/FastAPI)

```python
# science-gateway/app.py
import httpx
import os
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("science-gateway")

app = FastAPI(title="Science Gateway", version="1.0.0")

# Service URLs — resolved via Kubernetes DNS + Envoy sidecar
IAM_SERVICE_URL = os.getenv("IAM_SERVICE_URL", "http://iam-service.workflow-system.svc.cluster.local:8080")
GLOBAL_EXEC_URL = os.getenv("GLOBAL_EXEC_URL", "http://global-execution-api.workflow-system.svc.cluster.local:8080")
DATA_MGMT_URL = os.getenv("DATA_MGMT_URL", "http://data-management.workflow-system.svc.cluster.local:8080")


class WorkflowSubmission(BaseModel):
    name: str
    workflow_type: str  # "batch" or "interactive"
    input_data_path: str
    parameters: dict = {}


class LoginRequest(BaseModel):
    username: str
    password: str


async def validate_token(authorization: str) -> dict:
    """Validate token against IAM service — traffic goes through Envoy sidecar (mTLS)."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{IAM_SERVICE_URL}/auth/validate",
            headers={"Authorization": authorization}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Authentication failed")
        return resp.json()


@app.post("/api/login")
async def login(req: LoginRequest):
    """Proxy login to IAM service."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{IAM_SERVICE_URL}/auth/login",
            json={"username": req.username, "password": req.password}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Login failed")
        return resp.json()


@app.post("/api/workflows")
async def submit_workflow(
    submission: WorkflowSubmission,
    authorization: str = Header(...)
):
    """Submit a new workflow — orchestrated through Global Execution API."""
    user_info = await validate_token(authorization)
    
    workflow_id = str(uuid.uuid4())
    logger.info(f"User {user_info['subject']} submitting workflow {workflow_id}")

    # Forward to Global Wrapper Execution API
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{GLOBAL_EXEC_URL}/api/execute",
            json={
                "workflow_id": workflow_id,
                "name": submission.name,
                "type": submission.workflow_type,
                "input_data_path": submission.input_data_path,
                "parameters": submission.parameters,
                "submitted_by": user_info["subject"]
            },
            headers={"Authorization": authorization}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Execution API error")
        return {"workflow_id": workflow_id, "status": "submitted", **resp.json()}


@app.get("/api/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str, authorization: str = Header(...)):
    """Check workflow status."""
    await validate_token(authorization)
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{GLOBAL_EXEC_URL}/api/execute/{workflow_id}",
            headers={"Authorization": authorization}
        )
        return resp.json()


@app.get("/api/data")
async def list_data(authorization: str = Header(...)):
    """List available datasets via Data Management service."""
    await validate_token(authorization)
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{DATA_MGMT_URL}/api/datasets",
            headers={"Authorization": authorization}
        )
        return resp.json()


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "science-gateway"}
```

```dockerfile
# science-gateway/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
USER 1000:1000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### 3.3 Global Wrapper Execution API (Java/Spring Boot)

```java
// global-execution-api/src/main/java/com/workflow/execution/ExecutionController.java
package com.workflow.execution;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@RestController
@RequestMapping("/api/execute")
public class ExecutionController {

    // Kubernetes DNS names — traffic routed through Envoy sidecar automatically
    @Value("${services.batch-execution.url:http://batch-execution-api.workflow-system.svc.cluster.local:8080}")
    private String batchExecutionUrl;

    @Value("${services.interactive-api.url:http://interactive-api.workflow-system.svc.cluster.local:5000}")
    private String interactiveApiUrl;

    @Value("${services.data-management.url:http://data-management.workflow-system.svc.cluster.local:8080}")
    private String dataManagementUrl;

    private final RestTemplate restTemplate;
    private final ConcurrentHashMap<String, Map<String, Object>> workflows = new ConcurrentHashMap<>();

    public ExecutionController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> executeWorkflow(@RequestBody Map<String, Object> request) {
        String workflowId = (String) request.get("workflow_id");
        String type = (String) request.get("type");
        String inputDataPath = (String) request.get("input_data_path");

        // Store workflow state
        workflows.put(workflowId, Map.of(
            "status", "DISPATCHING",
            "type", type,
            "submitted_by", request.getOrDefault("submitted_by", "unknown")
        ));

        // Validate input data exists via Data Management
        try {
            restTemplate.getForEntity(
                dataManagementUrl + "/api/datasets/validate?path=" + inputDataPath,
                Map.class
            );
        } catch (Exception e) {
            workflows.put(workflowId, Map.of("status", "FAILED", "error", "Input data not found"));
            return ResponseEntity.badRequest().body(Map.of("error", "Input data validation failed"));
        }

        // Dispatch to the appropriate execution backend
        Map<String, Object> result;
        if ("batch".equals(type)) {
            result = dispatchBatch(workflowId, request);
        } else if ("interactive".equals(type)) {
            result = dispatchInteractive(workflowId, request);
        } else {
            return ResponseEntity.badRequest().body(Map.of("error", "Unknown workflow type: " + type));
        }

        workflows.put(workflowId, Map.of("status", "RUNNING", "type", type, "details", result));
        return ResponseEntity.ok(Map.of("execution_id", UUID.randomUUID().toString(), "status", "DISPATCHED"));
    }

    @GetMapping("/{workflowId}")
    public ResponseEntity<Map<String, Object>> getStatus(@PathVariable String workflowId) {
        Map<String, Object> workflow = workflows.get(workflowId);
        if (workflow == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(workflow);
    }

    private Map<String, Object> dispatchBatch(String workflowId, Map<String, Object> request) {
        ResponseEntity<Map> response = restTemplate.postForEntity(
            batchExecutionUrl + "/api/jobs",
            request,
            Map.class
        );
        return response.getBody() != null ? response.getBody() : Map.of();
    }

    private Map<String, Object> dispatchInteractive(String workflowId, Map<String, Object> request) {
        ResponseEntity<Map> response = restTemplate.postForEntity(
            interactiveApiUrl + "/api/sessions",
            request,
            Map.class
        );
        return response.getBody() != null ? response.getBody() : Map.of();
    }
}
```

```java
// global-execution-api/src/main/java/com/workflow/execution/ExecutionApplication.java
package com.workflow.execution;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class ExecutionApplication {
    public static void main(String[] args) {
        SpringApplication.run(ExecutionApplication.class, args);
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

#### 3.4 Local Batch Execution API (Go)

```go
// batch-execution-api/main.go
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/google/uuid"
)

type Job struct {
	ID         string `json:"id"`
	WorkflowID string `json:"workflow_id"`
	Status     string `json:"status"`
	CreatedAt  string `json:"created_at"`
	Cluster    string `json:"cluster"`
}

type JobStore struct {
	mu   sync.RWMutex
	jobs map[string]*Job
}

var jobs = &JobStore{jobs: make(map[string]*Job)}

func submitJobHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

	jobID := uuid.New().String()
	workflowID, _ := req["workflow_id"].(string)

	job := &Job{
		ID:         jobID,
		WorkflowID: workflowID,
		Status:     "QUEUED",
		CreatedAt:  time.Now().UTC().Format(time.RFC3339),
		Cluster:    "hpc-cluster-01",
	}

	jobs.mu.Lock()
	jobs.jobs[jobID] = job
	jobs.mu.Unlock()

	log.Printf("Job %s queued for workflow %s", jobID, workflowID)

	// Simulate async job submission to HPC scheduler (Slurm, PBS, etc.)
	go func() {
		time.Sleep(2 * time.Second)
		jobs.mu.Lock()
		if j, ok := jobs.jobs[jobID]; ok {
			j.Status = "RUNNING"
		}
		jobs.mu.Unlock()
	}()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(job)
}

func getJobHandler(w http.ResponseWriter, r *http.Request) {
	jobID := r.URL.Path[len("/api/jobs/"):]
	
	jobs.mu.RLock()
	job, exists := jobs.jobs[jobID]
	jobs.mu.RUnlock()

	if !exists {
		http.Error(w, "Job not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(job)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/jobs", submitJobHandler)
	mux.HandleFunc("/api/jobs/", getJobHandler)
	mux.HandleFunc("/health", healthHandler)

	server := &http.Server{
		Addr:         ":8080",
		Handler:      mux,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	fmt.Println("Batch Execution API starting on :8080")
	log.Fatal(server.ListenAndServe())
}
```

#### 3.5 Local Interactive API (Python/Flask)

```python
# interactive-api/app.py
from flask import Flask, request, jsonify
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("interactive-api")

app = Flask(__name__)

# In-memory session store
sessions = {}


@app.route("/api/sessions", methods=["POST"])
def create_session():
    """Create an interactive session (Jupyter, RStudio, etc.)."""
    data = request.get_json()
    session_id = str(uuid.uuid4())
    
    session = {
        "session_id": session_id,
        "workflow_id": data.get("workflow_id"),
        "type": data.get("parameters", {}).get("session_type", "jupyter"),
        "status": "STARTING",
        "endpoint": f"https://interactive.example.com/session/{session_id}",
    }
    sessions[session_id] = session
    
    logger.info(f"Created interactive session {session_id}")
    return jsonify(session), 200


@app.route("/api/sessions/<session_id>", methods=["GET"])
def get_session(session_id):
    """Get session status."""
    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(session)


@app.route("/api/sessions/<session_id>", methods=["DELETE"])
def stop_session(session_id):
    """Stop an interactive session."""
    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    session["status"] = "TERMINATED"
    return jsonify(session)


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "interactive-api"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

#### 3.6 Data Management Service (Java/Quarkus)

```java
// data-management/src/main/java/com/workflow/data/DataManagementResource.java
package com.workflow.data;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import io.minio.*;
import io.minio.messages.Item;

import java.util.*;

@Path("/api")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class DataManagementResource {

    @ConfigProperty(name = "minio.endpoint", defaultValue = "http://minio.workflow-system.svc.cluster.local:9000")
    String minioEndpoint;

    @ConfigProperty(name = "minio.access-key", defaultValue = "minioadmin")
    String accessKey;

    @ConfigProperty(name = "minio.secret-key", defaultValue = "minioadmin")
    String secretKey;

    private MinioClient getClient() {
        return MinioClient.builder()
                .endpoint(minioEndpoint)
                .credentials(accessKey, secretKey)
                .build();
    }

    @GET
    @Path("/datasets")
    public Response listDatasets() {
        try {
            MinioClient client = getClient();
            List<Map<String, String>> datasets = new ArrayList<>();

            Iterable<Result<Item>> results = client.listObjects(
                ListObjectsArgs.builder().bucket("workflow-data").recursive(false).build()
            );

            for (Result<Item> result : results) {
                Item item = result.get();
                datasets.add(Map.of(
                    "name", item.objectName(),
                    "size", String.valueOf(item.size()),
                    "last_modified", item.lastModified().toString()
                ));
            }

            return Response.ok(datasets).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }

    @GET
    @Path("/datasets/validate")
    public Response validateDataset(@QueryParam("path") String path) {
        try {
            MinioClient client = getClient();
            client.statObject(
                StatObjectArgs.builder().bucket("workflow-data").object(path).build()
            );
            return Response.ok(Map.of("valid", true, "path", path)).build();
        } catch (Exception e) {
            return Response.status(Response.Status.NOT_FOUND)
                    .entity(Map.of("valid", false, "error", "Dataset not found"))
                    .build();
        }
    }

    @GET
    @Path("/health")
    public Response health() {
        return Response.ok(Map.of("status", "healthy", "service", "data-management")).build();
    }
}
```

---

### Step 4: Kubernetes Deployments with Sidecar Injection

> With `istio-injection: enabled` on the namespace, **every pod automatically gets an Envoy sidecar**. The YAML below shows standard Kubernetes deployments — Istio handles the rest.

#### 4.1 IAM Service Deployment

```yaml
# k8s/iam-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iam-service
  namespace: workflow-system
  labels:
    app: iam-service
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: iam-service
  template:
    metadata:
      labels:
        app: iam-service
        version: v1
      annotations:
        # Sidecar is auto-injected, but we can configure it:
        sidecar.istio.io/proxyCPU: "100m"
        sidecar.istio.io/proxyMemory: "128Mi"
        # Enable access logging on the sidecar
        sidecar.istio.io/logLevel: "info"
    spec:
      serviceAccountName: iam-service
      containers:
        - name: iam-service
          image: registry.example.com/workflow/iam-service:1.0.0
          ports:
            - containerPort: 8080
              name: http
              protocol: TCP
          resources:
            requests:
              cpu: "100m"
              memory: "64Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 3
            periodSeconds: 5
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
---
apiVersion: v1
kind: Service
metadata:
  name: iam-service
  namespace: workflow-system
  labels:
    app: iam-service
spec:
  ports:
    - port: 8080
      targetPort: 8080
      name: http  # Named ports are required for Istio protocol detection
  selector:
    app: iam-service
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: iam-service
  namespace: workflow-system
```

#### 4.2 Science Gateway Deployment

```yaml
# k8s/science-gateway.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: science-gateway
  namespace: workflow-system
  labels:
    app: science-gateway
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: science-gateway
  template:
    metadata:
      labels:
        app: science-gateway
        version: v1
    spec:
      serviceAccountName: science-gateway
      containers:
        - name: science-gateway
          image: registry.example.com/workflow/science-gateway:1.0.0
          ports:
            - containerPort: 8000
              name: http
          env:
            - name: IAM_SERVICE_URL
              value: "http://iam-service.workflow-system.svc.cluster.local:8080"
            - name: GLOBAL_EXEC_URL
              value: "http://global-execution-api.workflow-system.svc.cluster.local:8080"
            - name: DATA_MGMT_URL
              value: "http://data-management.workflow-system.svc.cluster.local:8080"
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
---
apiVersion: v1
kind: Service
metadata:
  name: science-gateway
  namespace: workflow-system
spec:
  ports:
    - port: 8000
      targetPort: 8000
      name: http
  selector:
    app: science-gateway
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: science-gateway
  namespace: workflow-system
```

#### 4.3 Global Wrapper Execution API Deployment

```yaml
# k8s/global-execution-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: global-execution-api
  namespace: workflow-system
  labels:
    app: global-execution-api
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: global-execution-api
  template:
    metadata:
      labels:
        app: global-execution-api
        version: v1
    spec:
      serviceAccountName: global-execution-api
      containers:
        - name: global-execution-api
          image: registry.example.com/workflow/global-execution-api:1.0.0
          ports:
            - containerPort: 8080
              name: http
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: "kubernetes"
            - name: SERVICES_BATCH_EXECUTION_URL
              value: "http://batch-execution-api.workflow-system.svc.cluster.local:8080"
            - name: SERVICES_INTERACTIVE_API_URL
              value: "http://interactive-api.workflow-system.svc.cluster.local:5000"
            - name: SERVICES_DATA_MANAGEMENT_URL
              value: "http://data-management.workflow-system.svc.cluster.local:8080"
          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 20
            periodSeconds: 5
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            allowPrivilegeEscalation: false
---
apiVersion: v1
kind: Service
metadata:
  name: global-execution-api
  namespace: workflow-system
spec:
  ports:
    - port: 8080
      targetPort: 8080
      name: http
  selector:
    app: global-execution-api
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: global-execution-api
  namespace: workflow-system
```

#### 4.4 Batch Execution API Deployment

```yaml
# k8s/batch-execution-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-execution-api
  namespace: workflow-system
  labels:
    app: batch-execution-api
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: batch-execution-api
  template:
    metadata:
      labels:
        app: batch-execution-api
        version: v1
    spec:
      serviceAccountName: batch-execution-api
      containers:
        - name: batch-execution-api
          image: registry.example.com/workflow/batch-execution-api:1.0.0
          ports:
            - containerPort: 8080
              name: http
          resources:
            requests:
              cpu: "100m"
              memory: "64Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 3
            periodSeconds: 5
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
---
apiVersion: v1
kind: Service
metadata:
  name: batch-execution-api
  namespace: workflow-system
spec:
  ports:
    - port: 8080
      targetPort: 8080
      name: http
  selector:
    app: batch-execution-api
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: batch-execution-api
  namespace: workflow-system
```

#### 4.5 Interactive API Deployment

```yaml
# k8s/interactive-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: interactive-api
  namespace: workflow-system
  labels:
    app: interactive-api
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: interactive-api
  template:
    metadata:
      labels:
        app: interactive-api
        version: v1
    spec:
      serviceAccountName: interactive-api
      containers:
        - name: interactive-api
          image: registry.example.com/workflow/interactive-api:1.0.0
          ports:
            - containerPort: 5000
              name: http
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 5
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            allowPrivilegeEscalation: false
---
apiVersion: v1
kind: Service
metadata:
  name: interactive-api
  namespace: workflow-system
spec:
  ports:
    - port: 5000
      targetPort: 5000
      name: http
  selector:
    app: interactive-api
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: interactive-api
  namespace: workflow-system
```

#### 4.6 Data Management Deployment

```yaml
# k8s/data-management.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-management
  namespace: workflow-system
  labels:
    app: data-management
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: data-management
  template:
    metadata:
      labels:
        app: data-management
        version: v1
    spec:
      serviceAccountName: data-management
      containers:
        - name: data-management
          image: registry.example.com/workflow/data-management:1.0.0
          ports:
            - containerPort: 8080
              name: http
          env:
            - name: MINIO_ENDPOINT
              value: "http://minio.workflow-system.svc.cluster.local:9000"
            - name: MINIO_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: minio-credentials
                  key: access-key
            - name: MINIO_SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: minio-credentials
                  key: secret-key
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /api/health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /api/health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            allowPrivilegeEscalation: false
---
apiVersion: v1
kind: Service
metadata:
  name: data-management
  namespace: workflow-system
spec:
  ports:
    - port: 8080
      targetPort: 8080
      name: http
  selector:
    app: data-management
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: data-management
  namespace: workflow-system
```

#### 4.7 MinIO (Local Datalake/S3) Deployment

```yaml
# k8s/minio.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: minio
  namespace: workflow-system
  labels:
    app: minio
spec:
  serviceName: minio
  replicas: 3
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
        version: v1
    spec:
      serviceAccountName: minio
      containers:
        - name: minio
          image: minio/minio:RELEASE.2024-01-01T00-00-00Z
          args:
            - server
            - /data
            - --console-address
            - ":9001"
          ports:
            - containerPort: 9000
              name: http
            - containerPort: 9001
              name: console
          env:
            - name: MINIO_ROOT_USER
              valueFrom:
                secretKeyRef:
                  name: minio-credentials
                  key: access-key
            - name: MINIO_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: minio-credentials
                  key: secret-key
          volumeMounts:
            - name: data
              mountPath: /data
          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          livenessProbe:
            httpGet:
              path: /minio/health/live
              port: 9000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /minio/health/ready
              port: 9000
            initialDelaySeconds: 5
            periodSeconds: 5
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: minio
  namespace: workflow-system
spec:
  ports:
    - port: 9000
      targetPort: 9000
      name: http
    - port: 9001
      targetPort: 9001
      name: console
  selector:
    app: minio
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: minio
  namespace: workflow-system
---
apiVersion: v1
kind: Secret
metadata:
  name: minio-credentials
  namespace: workflow-system
type: Opaque
stringData:
  access-key: "minioadmin"       # Change in production
  secret-key: "minioadmin123"    # Change in production
```

---

### Step 5: Istio Networking — Gateway, Virtual Services, and Traffic Management

#### 5.1 Ingress Gateway

```yaml
# istio/gateway.yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: workflow-gateway
  namespace: workflow-system
spec:
  selector:
    istio: ingressgateway  # Use the default Istio ingress controller
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE  # TLS termination at the gateway
        credentialName: workflow-tls-credential  # K8s secret with cert/key
      hosts:
        - "workflow.example.com"
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "workflow.example.com"
      tls:
        httpsRedirect: true  # Force HTTPS
```

#### 5.2 Virtual Services (Routing Rules)

```yaml
# istio/virtual-services.yaml

# Route external traffic to Science Gateway
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: science-gateway-vs
  namespace: workflow-system
spec:
  hosts:
    - "workflow.example.com"
  gateways:
    - workflow-gateway
  http:
    - match:
        - uri:
            prefix: /api
      route:
        - destination:
            host: science-gateway
            port:
              number: 8000
      retries:
        attempts: 3
        perTryTimeout: 10s
        retryOn: "5xx,reset,connect-failure"
      timeout: 30s
---
# Internal routing: Global Execution API with load balancing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: global-execution-vs
  namespace: workflow-system
spec:
  hosts:
    - global-execution-api
  http:
    - route:
        - destination:
            host: global-execution-api
            port:
              number: 8080
      retries:
        attempts: 3
        perTryTimeout: 15s
        retryOn: "5xx,reset,connect-failure,unavailable"
      timeout: 60s
      fault:
        # Fault injection for testing resilience (disable in production)
        # delay:
        #   percentage:
        #     value: 5
        #   fixedDelay: 3s
---
# Batch Execution — with locality-aware routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: batch-execution-vs
  namespace: workflow-system
spec:
  hosts:
    - batch-execution-api
  http:
    - route:
        - destination:
            host: batch-execution-api
            port:
              number: 8080
      retries:
        attempts: 2
        perTryTimeout: 30s
      timeout: 120s  # Batch jobs may take time to submit
```

#### 5.3 Destination Rules (Load Balancing + Connection Pooling)

```yaml
# istio/destination-rules.yaml

# Science Gateway — round robin with outlier detection
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: science-gateway-dr
  namespace: workflow-system
spec:
  host: science-gateway
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
    tls:
      mode: ISTIO_MUTUAL
---
# IAM Service — least connections (stateless auth lookups)
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: iam-service-dr
  namespace: workflow-system
spec:
  host: iam-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST
    connectionPool:
      tcp:
        maxConnections: 200
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 200
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 5s
      baseEjectionTime: 15s
      maxEjectionPercent: 30
    tls:
      mode: ISTIO_MUTUAL
---
# Global Execution API — round robin with circuit breaking
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: global-execution-dr
  namespace: workflow-system
spec:
  host: global-execution-api
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 33
    tls:
      mode: ISTIO_MUTUAL
---
# Batch Execution API
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: batch-execution-dr
  namespace: workflow-system
spec:
  host: batch-execution-api
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 60s
    tls:
      mode: ISTIO_MUTUAL
---
# Data Management
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: data-management-dr
  namespace: workflow-system
spec:
  host: data-management
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST
    connectionPool:
      tcp:
        maxConnections: 50
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
    tls:
      mode: ISTIO_MUTUAL
---
# MinIO
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: minio-dr
  namespace: workflow-system
spec:
  host: minio
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 100
    tls:
      mode: ISTIO_MUTUAL
```

---

### Step 6: Authorization Policies (Zero-Trust Network)

```yaml
# istio/authorization-policies.yaml

# Default: deny all traffic in the namespace
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: workflow-system
spec:
  {}  # Empty spec = deny all
---
# Allow ingress gateway → Science Gateway
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-ingress-to-gateway
  namespace: workflow-system
spec:
  selector:
    matchLabels:
      app: science-gateway
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account"]
---
# Allow Science Gateway → IAM
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-gateway-to-iam
  namespace: workflow-system
spec:
  selector:
    matchLabels:
      app: iam-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/workflow-system/sa/science-gateway"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/auth/*"]
---
# Allow Science Gateway → Global Execution API
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-gateway-to-execution
  namespace: workflow-system
spec:
  selector:
    matchLabels:
      app: global-execution-api
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/workflow-system/sa/science-gateway"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/execute", "/api/execute/*"]
---
# Allow Global Execution → Batch + Interactive + Data Management
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-execution-to-backends
  namespace: workflow-system
spec:
  selector:
    matchLabels:
      app: batch-execution-api
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/workflow-system/sa/global-execution-api"]
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-execution-to-interactive
  namespace: workflow-system
spec:
  selector:
    matchLabels:
      app: interactive-api
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/workflow-system/sa/global-execution-api"]
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-execution-to-data
  namespace: workflow-system
spec:
  selector:
    matchLabels:
      app: data-management
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/workflow-system/sa/global-execution-api"
              - "cluster.local/ns/workflow-system/sa/science-gateway"
---
# Allow Data Management → MinIO
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-data-to-minio
  namespace: workflow-system
spec:
  selector:
    matchLabels:
      app: minio
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/workflow-system/sa/data-management"]
```

**Zero-Trust Network Topology:**

```
                    ┌──────────────────────────────────────────────┐
                    │         Authorization Policy Map             │
                    │                                              │
                    │  Ingress ──────► Science Gateway             │
                    │                      │                       │
                    │                ┌─────┴─────┐                │
                    │                ▼           ▼                 │
                    │              IAM    Global Exec API          │
                    │                      │                       │
                    │              ┌───────┼───────┐              │
                    │              ▼       ▼       ▼              │
                    │           Batch  Interactive  Data Mgmt     │
                    │                                  │          │
                    │                                  ▼          │
                    │                               MinIO         │
                    │                                              │
                    │  ✗ All other communication paths DENIED     │
                    └──────────────────────────────────────────────┘
```

---

### Step 7: Observability Configuration

#### 7.1 Distributed Tracing with Jaeger

```yaml
# observability/jaeger.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  namespace: observability
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
        - name: jaeger
          image: jaegertracing/all-in-one:1.53
          ports:
            - containerPort: 16686  # UI
            - containerPort: 14268  # Collector
          env:
            - name: COLLECTOR_ZIPKIN_HOST_PORT
              value: ":9411"
---
apiVersion: v1
kind: Service
metadata:
  name: jaeger
  namespace: observability
spec:
  ports:
    - port: 16686
      name: ui
    - port: 14268
      name: collector
    - port: 9411
      name: zipkin
  selector:
    app: jaeger
```

#### 7.2 Prometheus and Grafana

```yaml
# observability/prometheus.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: observability
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'istio-mesh'
        kubernetes_sd_configs:
          - role: endpoints
            namespaces:
              names: ['istio-system']
        relabel_configs:
          - source_labels: [__meta_kubernetes_service_name]
            regex: istiod
            action: keep
      - job_name: 'envoy-stats'
        metrics_path: /stats/prometheus
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names: ['workflow-system']
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_container_name]
            regex: istio-proxy
            action: keep
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
            regex: '(\d+)'
            target_label: __address__
            replacement: ${1}:15090
```

#### 7.3 Istio Telemetry Configuration

```yaml
# istio/telemetry.yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-default
  namespace: workflow-system
spec:
  # Enable access logging for all sidecars
  accessLogging:
    - providers:
        - name: envoy
  # Enable distributed tracing
  tracing:
    - providers:
        - name: jaeger
      randomSamplingPercentage: 100  # 100% in dev, lower in production
  # Enable metrics
  metrics:
    - providers:
        - name: prometheus
```

---

### Step 8: Network Policies (Defense in Depth)

```yaml
# k8s/network-policies.yaml
# Kubernetes NetworkPolicy as a second layer of defense beyond Istio AuthorizationPolicy

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: workflow-system
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
# Allow DNS resolution
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: workflow-system
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to: []
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
---
# Allow all intra-namespace traffic (Istio handles fine-grained control)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-intra-namespace
  namespace: workflow-system
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: workflow-system
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: istio-system
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: workflow-system
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: istio-system
```

---

### Step 9: Pod Disruption Budgets and Horizontal Pod Autoscaling

```yaml
# k8s/pdb-hpa.yaml

# PDB: Ensure minimum availability during cluster operations
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: science-gateway-pdb
  namespace: workflow-system
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: science-gateway
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: iam-service-pdb
  namespace: workflow-system
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: iam-service
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: global-execution-pdb
  namespace: workflow-system
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: global-execution-api
---
# HPA: Auto-scale based on CPU/memory
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: science-gateway-hpa
  namespace: workflow-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: science-gateway
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: global-execution-hpa
  namespace: workflow-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: global-execution-api
  minReplicas: 3
  maxReplicas: 8
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

---

### Step 10: Canary Deployments with Traffic Splitting

```yaml
# istio/canary-deployment.yaml
# Example: Rolling out v2 of Science Gateway with 10% traffic

apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: science-gateway-canary
  namespace: workflow-system
spec:
  hosts:
    - science-gateway
  http:
    - route:
        - destination:
            host: science-gateway
            subset: v1
          weight: 90
        - destination:
            host: science-gateway
            subset: v2
          weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: science-gateway-versions
  namespace: workflow-system
spec:
  host: science-gateway
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

---

### Step 11: Rate Limiting

```yaml
# istio/rate-limit.yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: rate-limit-science-gateway
  namespace: workflow-system
spec:
  workloadSelector:
    labels:
      app: science-gateway
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: envoy.filters.network.http_connection_manager
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.local_ratelimit
          typed_config:
            "@type": type.googleapis.com/udpa.type.v1.TypedStruct
            type_url: type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
            value:
              stat_prefix: http_local_rate_limiter
              token_bucket:
                max_tokens: 100
                tokens_per_fill: 100
                fill_interval: 60s
              filter_enabled:
                runtime_key: local_rate_limit_enabled
                default_value:
                  numerator: 100
                  denominator: HUNDRED
              filter_enforced:
                runtime_key: local_rate_limit_enforced
                default_value:
                  numerator: 100
                  denominator: HUNDRED
              response_headers_to_add:
                - append_action: OVERWRITE_IF_EXISTS_OR_ADD
                  header:
                    key: x-local-rate-limit
                    value: "true"
```

---

### Step 12: Deploy Everything

```bash
#!/bin/bash
# deploy.sh — Full deployment script

set -euo pipefail

echo "=== Creating namespaces ==="
kubectl apply -f k8s/namespace.yaml

echo "=== Applying mTLS policies ==="
kubectl apply -f istio/peer-authentication.yaml
kubectl apply -f istio/destination-rule-mtls.yaml

echo "=== Deploying services ==="
kubectl apply -f k8s/minio.yaml
kubectl apply -f k8s/iam-service.yaml
kubectl apply -f k8s/data-management.yaml
kubectl apply -f k8s/batch-execution-api.yaml
kubectl apply -f k8s/interactive-api.yaml
kubectl apply -f k8s/global-execution-api.yaml
kubectl apply -f k8s/science-gateway.yaml

echo "=== Applying Istio networking ==="
kubectl apply -f istio/gateway.yaml
kubectl apply -f istio/virtual-services.yaml
kubectl apply -f istio/destination-rules.yaml

echo "=== Applying authorization policies ==="
kubectl apply -f istio/authorization-policies.yaml

echo "=== Applying network policies ==="
kubectl apply -f k8s/network-policies.yaml

echo "=== Applying PDB and HPA ==="
kubectl apply -f k8s/pdb-hpa.yaml

echo "=== Applying observability ==="
kubectl apply -f observability/jaeger.yaml
kubectl apply -f observability/prometheus.yaml
kubectl apply -f istio/telemetry.yaml

echo "=== Applying rate limiting ==="
kubectl apply -f istio/rate-limit.yaml

echo "=== Verifying deployment ==="
kubectl get pods -n workflow-system
kubectl get svc -n workflow-system

echo "=== Verifying sidecar injection ==="
kubectl get pods -n workflow-system -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .spec.containers[*]}{.name}{","}{end}{"\n"}{end}'

echo "=== Checking mTLS status ==="
istioctl authn tls-check -n workflow-system
```

---

### How the Sidecar Pattern Works (Detailed)

```
┌─────────────────────────────────────────────────────────┐
│                     POD BOUNDARY                        │
│                                                         │
│  ┌─────────────────────┐   ┌─────────────────────────┐ │
│  │  Application         │   │  Envoy Sidecar Proxy    │ │
│  │  Container            │   │                         │ │
│  │                       │   │  • Injected by Istio    │ │
│  │  • Your code (Go,    │   │    admission webhook    │ │
│  │    Python, Java)     │   │                         │ │
│  │  • Sends HTTP to     │   │  • Intercepts ALL       │ │
│  │    localhost or       │◄─►│    inbound & outbound   │ │
│  │    K8s service DNS   │   │    network traffic      │ │
│  │  • No mesh awareness │   │    via iptables rules   │ │
│  │    needed             │   │                         │ │
│  │                       │   │  • Adds mTLS encryption │ │
│  │  Ports: 8080         │   │  • Collects metrics     │ │
│  │                       │   │  • Enforces policies    │ │
│  │                       │   │  • Load balances        │ │
│  │                       │   │  • Retries failed reqs  │ │
│  │                       │   │  • Circuit breaking     │ │
│  │                       │   │                         │ │
│  │                       │   │  Ports: 15001 (outbound)│ │
│  │                       │   │         15006 (inbound) │ │
│  │                       │   │         15090 (metrics) │ │
│  │                       │   │         15021 (health)  │ │
│  └─────────────────────┘   └─────────────────────────┘ │
│                                                         │
│  ┌─────────────────────┐                                │
│  │  istio-init          │  (init container)             │
│  │  Sets up iptables    │  Runs BEFORE app starts       │
│  │  rules to redirect   │  Redirects ports 8080 →       │
│  │  traffic to Envoy    │  Envoy 15006 (inbound)        │
│  └─────────────────────┘                                │
└─────────────────────────────────────────────────────────┘
```

**Key insight:** The application container has **zero awareness** of the mesh. It just talks HTTP to Kubernetes DNS names. The `istio-init` container sets up iptables rules that transparently redirect all traffic through the Envoy sidecar.

**What happens when Pod A calls Pod B:**

```
1. App A sends HTTP to "http://iam-service:8080/auth/validate"
2. iptables redirects this to Envoy sidecar A (port 15001)
3. Envoy A resolves "iam-service" via Pilot/xDS configuration
4. Envoy A picks a healthy Pod B instance (load balancing)
5. Envoy A initiates mTLS connection to Envoy B (port 15006)
6. Envoy B verifies A's certificate (mTLS handshake)
7. Envoy B checks AuthorizationPolicy (is A allowed?)
8. Envoy B forwards decrypted request to App B on localhost:8080
9. Response travels the reverse path
10. Metrics, traces, and logs are emitted at each step
```

---

### Service Discovery in the Mesh

Service discovery happens at **three layers**:

```
┌────────────────────────────────────────────┐
│           Layer 1: Kubernetes DNS          │
│                                            │
│  science-gateway.workflow-system.svc.      │
│  cluster.local → ClusterIP (10.x.x.x)     │
│                                            │
│  CoreDNS resolves service names to         │
│  virtual IPs                               │
├────────────────────────────────────────────┤
│           Layer 2: Istio Pilot (xDS)       │
│                                            │
│  istiod watches Kubernetes API for:        │
│  • Service objects                         │
│  • Endpoint objects                        │
│  • Pod additions/removals                  │
│                                            │
│  Pushes real-time endpoint lists to all    │
│  Envoy sidecars via xDS (discovery svc)    │
├────────────────────────────────────────────┤
│           Layer 3: Envoy Load Balancing    │
│                                            │
│  Each Envoy sidecar maintains a live       │
│  list of upstream pod IPs and performs:    │
│  • Health checking                         │
│  • Load balancing (round robin, least req) │
│  • Outlier detection (circuit breaking)    │
│  • Locality-aware routing                  │
│                                            │
│  Bypasses kube-proxy entirely — traffic    │
│  goes directly pod-to-pod                  │
└────────────────────────────────────────────┘
```

---

### Verification and Testing Commands

```bash
# Check all pods have 2 containers (app + sidecar)
kubectl get pods -n workflow-system -o wide

# Verify mTLS is active between services
istioctl proxy-config listener <pod-name> -n workflow-system
istioctl proxy-config cluster <pod-name> -n workflow-system

# Check Envoy is correctly configured for a service
istioctl analyze -n workflow-system

# View sidecar proxy logs
kubectl logs <pod-name> -n workflow-system -c istio-proxy

# Test connectivity from one service to another
kubectl exec -it deploy/science-gateway -n workflow-system -c science-gateway -- \
  curl -s http://iam-service:8080/health

# Check authorization policy enforcement
kubectl exec -it deploy/batch-execution-api -n workflow-system -c batch-execution-api -- \
  curl -s http://iam-service:8080/health
# Should be DENIED (no AuthorizationPolicy allows batch → IAM)

# View mesh topology in Kiali
istioctl dashboard kiali

# View distributed traces in Jaeger
istioctl dashboard jaeger

# View metrics in Grafana
istioctl dashboard grafana
```

---

### Best Practices Summary

| Practice | Implementation |
|---|---|
| **mTLS Everywhere** | `PeerAuthentication` with `STRICT` mode — no plaintext in the mesh |
| **Zero-Trust Network** | `AuthorizationPolicy` deny-all default + explicit allow rules per service pair |
| **Sidecar Injection** | Namespace-level `istio-injection: enabled` — automatic, no per-pod config |
| **Service Discovery** | Kubernetes DNS + Istio Pilot xDS — application code uses simple HTTP URLs |
| **Load Balancing** | `DestinationRule` with `ROUND_ROBIN` or `LEAST_REQUEST` per service |
| **Circuit Breaking** | `outlierDetection` in `DestinationRule` — eject unhealthy pods automatically |
| **Retry + Timeout** | `VirtualService` retry policies with `perTryTimeout` and total `timeout` |
| **Rate Limiting** | `EnvoyFilter` with local rate limiter — per-pod token bucket |
| **Canary Deployments** | `VirtualService` weighted routing + `DestinationRule` subsets |
| **Observability** | Prometheus metrics + Jaeger tracing + Envoy access logs + Kiali visualization |
| **Network Policies** | Kubernetes `NetworkPolicy` as defense-in-depth below Istio |
| **Pod Security** | `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false` |
| **Availability** | `PodDisruptionBudget` + `HorizontalPodAutoscaler` for resilience |
| **Secrets Management** | Kubernetes `Secrets` with `secretKeyRef` — never hardcode credentials |
| **Named Ports** | All Service ports have `name: http` — required for Istio protocol detection |
| **Service Accounts** | Each service has its own `ServiceAccount` — used in AuthorizationPolicy principals |