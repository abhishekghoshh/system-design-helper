# System Design Concepts

A comprehensive guide to understanding core system design concepts and principles.

---

## Table of Contents

- [System Design Concepts](#system-design-concepts)
  - [Table of Contents](#table-of-contents)
  - [The Philosophy of System Design: A Unified Theory](#the-philosophy-of-system-design-a-unified-theory)
    - [The Grand Vision](#the-grand-vision)
    - [The Fundamental Truth: Everything is a Trade-off](#the-fundamental-truth-everything-is-a-trade-off)
    - [The Three Pillars of System Design](#the-three-pillars-of-system-design)
      - [1. **Data** (The Foundation)](#1-data-the-foundation)
      - [2. **Computation** (The Engine)](#2-computation-the-engine)
      - [3. **Communication** (The Nervous System)](#3-communication-the-nervous-system)
    - [The Evolutionary Stages of System Design](#the-evolutionary-stages-of-system-design)
      - [**Stage 1: The Monolith** (0-100K users)](#stage-1-the-monolith-0-100k-users)
      - [**Stage 2: Vertical Scaling** (100K-500K users)](#stage-2-vertical-scaling-100k-500k-users)
      - [**Stage 3: Horizontal Scaling** (500K-5M users)](#stage-3-horizontal-scaling-500k-5m-users)
      - [**Stage 4: Distributed Systems** (5M-50M users)](#stage-4-distributed-systems-5m-50m-users)
      - [**Stage 5: Global Scale** (50M+ users)](#stage-5-global-scale-50m-users)
    - [The CAP Theorem: The Immutable Law](#the-cap-theorem-the-immutable-law)
    - [The Principle of Graceful Degradation](#the-principle-of-graceful-degradation)
    - [The Hierarchy of Optimization](#the-hierarchy-of-optimization)
    - [The Data Gravity Principle](#the-data-gravity-principle)
    - [The Principle of Least Surprise](#the-principle-of-least-surprise)
    - [The Observability Imperative](#the-observability-imperative)
    - [The Security-First Mindset](#the-security-first-mindset)
    - [The Cost-Consciousness Principle](#the-cost-consciousness-principle)
    - [The Testing Pyramid: Quality Assurance](#the-testing-pyramid-quality-assurance)
    - [The Human Element](#the-human-element)
    - [The Unified Theory of System Design](#the-unified-theory-of-system-design)
  - [1. Introduction to System Design](#1-introduction-to-system-design)
    - [Why Learn System Design](#why-learn-system-design)
    - [How to Learn System Design](#how-to-learn-system-design)
    - [How to Approach System Design in Interviews](#how-to-approach-system-design-in-interviews)
  - [2. Foundational Concepts](#2-foundational-concepts)
    - [Client-Server Architecture](#client-server-architecture)
      - [The Foundational Paradigm of Distributed Computing](#the-foundational-paradigm-of-distributed-computing)
      - [The Deep Theory](#the-deep-theory)
      - [The State Problem](#the-state-problem)
      - [Architectural Tiers: Evolution of Separation](#architectural-tiers-evolution-of-separation)
      - [The Communication Contract: APIs](#the-communication-contract-apis)
      - [Request-Response Patterns](#request-response-patterns)
      - [The Scalability Implications](#the-scalability-implications)
      - [Modern Evolutions](#modern-evolutions)
      - [The Fundamental Trade-offs](#the-fundamental-trade-offs)
      - [The Wisdom](#the-wisdom)
    - [IP Addresses \& Ports](#ip-addresses--ports)
      - [IP Addresses: The Internet's Postal System](#ip-addresses-the-internets-postal-system)
        - [IPv4 Architecture](#ipv4-architecture)
        - [IPv6: The Future (and Present)](#ipv6-the-future-and-present)
      - [Ports: Doorways to Applications](#ports-doorways-to-applications)
        - [Port Ranges and Their Purposes](#port-ranges-and-their-purposes)
        - [Real-World Use Cases](#real-world-use-cases)
        - [Code Example: Socket Programming](#code-example-socket-programming)
        - [Network Address Translation (NAT)](#network-address-translation-nat)
        - [Common Networking Commands](#common-networking-commands)
        - [Security Considerations](#security-considerations)
    - [Domain Name System (DNS)](#domain-name-system-dns)
      - [The Internet's Phone Book](#the-internets-phone-book)
      - [How DNS Resolution Works: The Complete Journey](#how-dns-resolution-works-the-complete-journey)
      - [DNS Record Types: The Complete Reference](#dns-record-types-the-complete-reference)
        - [A Record (Address Record)](#a-record-address-record)
        - [AAAA Record (IPv6 Address)](#aaaa-record-ipv6-address)
        - [CNAME Record (Canonical Name)](#cname-record-canonical-name)
        - [MX Record (Mail Exchange)](#mx-record-mail-exchange)
        - [TXT Record (Text Information)](#txt-record-text-information)
        - [NS Record (Name Server)](#ns-record-name-server)
        - [Other Important Records](#other-important-records)
      - [DNS Caching: The Speed Secret](#dns-caching-the-speed-secret)
      - [Real-World Use Cases](#real-world-use-cases-1)
      - [DNS Commands \& Tools](#dns-commands--tools)
      - [DNS Security](#dns-security)
      - [Common DNS Issues](#common-dns-issues)
      - [Best Practices](#best-practices)
    - [Cloud Computing](#cloud-computing)
  - [3. Network Protocols](#3-network-protocols)
    - [Protocols](#protocols)
    - [TCP Protocol (Transmission Control Protocol)](#tcp-protocol-transmission-control-protocol)
      - [The Reliable Foundation of the Internet](#the-reliable-foundation-of-the-internet)
      - [The Deep Theory: Solving the Impossible](#the-deep-theory-solving-the-impossible)
      - [The Three-Way Handshake: Establishing Truth](#the-three-way-handshake-establishing-truth)
      - [Guaranteed Delivery: The Acknowledgment Dance](#guaranteed-delivery-the-acknowledgment-dance)
      - [Flow Control: Respecting the Receiver](#flow-control-respecting-the-receiver)
      - [Congestion Control: Respecting the Network](#congestion-control-respecting-the-network)
      - [Ordered Delivery: Sequence Numbers Save the Day](#ordered-delivery-sequence-numbers-save-the-day)
      - [Connection Termination: Graceful Goodbye](#connection-termination-graceful-goodbye)
      - [TCP Header: Every Bit Matters](#tcp-header-every-bit-matters)
      - [Performance Characteristics](#performance-characteristics)
      - [When TCP Shines](#when-tcp-shines)
      - [When TCP Struggles](#when-tcp-struggles)
      - [TCP Variants and Evolution](#tcp-variants-and-evolution)
      - [The Trade-offs](#the-trade-offs)
      - [The Wisdom](#the-wisdom-1)
    - [UDP Protocol (User Datagram Protocol)](#udp-protocol-user-datagram-protocol)
    - [HTTP / HTTPS (HyperText Transfer Protocol)](#http--https-hypertext-transfer-protocol)
      - [HTTPS: Security Through Encryption](#https-security-through-encryption)
      - [HTTP/1.1 vs HTTP/2 vs HTTP/3](#http11-vs-http2-vs-http3)
      - [HTTP: Advantages \& Disadvantages](#http-advantages--disadvantages)
      - [Alternatives to HTTP](#alternatives-to-http)
      - [Decision Matrix: Which Protocol?](#decision-matrix-which-protocol)
      - [When NOT to Use HTTP](#when-not-to-use-http)
      - [HTTP Best Practices](#http-best-practices)
    - [WebSockets](#websockets)
      - [The Real-Time Communication Channel](#the-real-time-communication-channel)
      - [Advantages of WebSockets](#advantages-of-websockets)
      - [Disadvantages of WebSockets](#disadvantages-of-websockets)
      - [Alternatives to WebSockets](#alternatives-to-websockets)
      - [When to Use WebSockets vs Alternatives](#when-to-use-websockets-vs-alternatives)
      - [WebSocket Implementation Examples](#websocket-implementation-examples)
      - [WebSocket Best Practices](#websocket-best-practices)
      - [Scaling WebSocket Servers](#scaling-websocket-servers)
      - [WebSocket vs HTTP: The Decision](#websocket-vs-http-the-decision)
  - [4. APIs \& Communication Patterns](#4-apis--communication-patterns)
    - [API (Application Programming Interface)](#api-application-programming-interface)
    - [REST API (Representational State Transfer)](#rest-api-representational-state-transfer)
      - [REST API: Advantages](#rest-api-advantages)
      - [REST API: Disadvantages](#rest-api-disadvantages)
      - [Alternatives to REST](#alternatives-to-rest)
      - [REST API Best Practices](#rest-api-best-practices)
      - [When to Use REST vs Alternatives](#when-to-use-rest-vs-alternatives)
    - [GraphQL](#graphql)
    - [gRPC (Google Remote Procedure Call)](#grpc-google-remote-procedure-call)
    - [Message Queue](#message-queue)
    - [Web Hooks](#web-hooks)
  - [5. Networking \& Infrastructure](#5-networking--infrastructure)
    - [Forward Proxy](#forward-proxy)
    - [Reverse Proxy](#reverse-proxy)
    - [Load Balancer](#load-balancer)
      - [The Traffic Conductor of Modern Infrastructure](#the-traffic-conductor-of-modern-infrastructure)
      - [The Deep Theory: Why Load Balancing Exists](#the-deep-theory-why-load-balancing-exists)
      - [The Algorithms: Different Strategies for Different Needs](#the-algorithms-different-strategies-for-different-needs)
        - [1. Round Robin (The Democrat)](#1-round-robin-the-democrat)
        - [2. Weighted Round Robin (The Meritocrat)](#2-weighted-round-robin-the-meritocrat)
        - [3. Least Connections (The Optimizer)](#3-least-connections-the-optimizer)
        - [4. Least Response Time (The Perfectionist)](#4-least-response-time-the-perfectionist)
        - [5. IP Hash (The Consistent Router)](#5-ip-hash-the-consistent-router)
        - [6. Random (The Gambler)](#6-random-the-gambler)
        - [7. Least Bandwidth (The Bandwidth Manager)](#7-least-bandwidth-the-bandwidth-manager)
      - [Layer 4 vs Layer 7: The Fundamental Choice](#layer-4-vs-layer-7-the-fundamental-choice)
        - [Layer 4 (Transport Layer) Load Balancing](#layer-4-transport-layer-load-balancing)
        - [Layer 7 (Application Layer) Load Balancing](#layer-7-application-layer-load-balancing)
        - [The Decision Matrix](#the-decision-matrix)
      - [Health Checks: Detecting Failure](#health-checks-detecting-failure)
        - [Active Health Checks (Proactive)](#active-health-checks-proactive)
        - [Passive Health Checks (Reactive)](#passive-health-checks-reactive)
      - [Load Balancer Deployment Patterns](#load-balancer-deployment-patterns)
        - [Pattern 1: Single Load Balancer](#pattern-1-single-load-balancer)
        - [Pattern 2: Active-Passive (HA Pair)](#pattern-2-active-passive-ha-pair)
        - [Pattern 3: Active-Active (Equal Cost Multi-Path)](#pattern-3-active-active-equal-cost-multi-path)
        - [Pattern 4: Cloud Native (Managed Service)](#pattern-4-cloud-native-managed-service)
      - [Advanced Scenarios](#advanced-scenarios)
        - [Global Load Balancing (GSLB)](#global-load-balancing-gslb)
        - [Session Persistence (Sticky Sessions)](#session-persistence-sticky-sessions)
        - [Zero-Downtime Deployments](#zero-downtime-deployments)
      - [The Critical Trade-offs](#the-critical-trade-offs)
      - [The Wisdom](#the-wisdom-2)
    - [API Gateway](#api-gateway)
    - [CDN (Content Delivery Network)](#cdn-content-delivery-network)
    - [Service Discovery](#service-discovery)
    - [Service Mesh](#service-mesh)
  - [6. Data Storage](#6-data-storage)
    - [Database Fundamentals](#database-fundamentals)
    - [SQL (Relational Databases)](#sql-relational-databases)
      - [SQL Databases: Advantages](#sql-databases-advantages)
      - [SQL Databases: Disadvantages](#sql-databases-disadvantages)
      - [SQL vs NoSQL: The Complete Comparison](#sql-vs-nosql-the-complete-comparison)
      - [When to Choose SQL](#when-to-choose-sql)
      - [Alternatives to Traditional SQL](#alternatives-to-traditional-sql)
    - [NoSQL](#nosql)
      - [Key-Value Stores](#key-value-stores)
      - [Document Databases](#document-databases)
      - [Graph Databases](#graph-databases)
      - [Wide Column Databases](#wide-column-databases)
      - [Time-Series Databases](#time-series-databases)
      - [NoSQL: Advantages](#nosql-advantages)
      - [NoSQL: Disadvantages](#nosql-disadvantages)
      - [When to Choose NoSQL](#when-to-choose-nosql)
      - [NoSQL Database Comparison](#nosql-database-comparison)
      - [Hybrid Approach: Polyglot Persistence](#hybrid-approach-polyglot-persistence)
      - [Decision Framework: SQL vs NoSQL](#decision-framework-sql-vs-nosql)
    - [SQL vs NoSQL](#sql-vs-nosql)
    - [Object Storage / Blob Storage](#object-storage--blob-storage)
  - [7. Database Optimization](#7-database-optimization)
    - [Indexing](#indexing)
    - [Replication](#replication)
    - [Sharding (Horizontal Partitioning)](#sharding-horizontal-partitioning)
    - [Vertical Partitioning](#vertical-partitioning)
    - [Denormalization](#denormalization)
  - [8. Caching](#8-caching)
    - [What is Caching?](#what-is-caching)
      - [The Art of Remembering: The Most Powerful Optimization](#the-art-of-remembering-the-most-powerful-optimization)
      - [The Deep Theory: Why Caching Works](#the-deep-theory-why-caching-works)
      - [The Cache Hierarchy: Layers Upon Layers](#the-cache-hierarchy-layers-upon-layers)
        - [Browser Cache (Client-Side)](#browser-cache-client-side)
        - [CDN Cache (Edge)](#cdn-cache-edge)
        - [Application Cache (In-Memory)](#application-cache-in-memory)
        - [Database Cache (Query Cache)](#database-cache-query-cache)
      - [The Cache Hierarchy Strategy](#the-cache-hierarchy-strategy)
    - [Cache Aside (Lazy Loading)](#cache-aside-lazy-loading)
    - [Read Through Strategy](#read-through-strategy)
    - [Write Through Strategy](#write-through-strategy)
    - [Write Behind (Write Back)](#write-behind-write-back)
    - [Write Around](#write-around)
    - [Cache Invalidation](#cache-invalidation)
  - [9. Scalability \& Performance](#9-scalability--performance)
    - [Latency \& Bandwidth](#latency--bandwidth)
    - [Scalability](#scalability)
    - [Throughput](#throughput)
    - [Performance Optimization](#performance-optimization)
  - [10. Reliability \& Consistency](#10-reliability--consistency)
    - [Availability \& Reliability](#availability--reliability)
    - [Single Point of Failure (SPOF)](#single-point-of-failure-spof)
    - [Consistency](#consistency)
    - [CAP Theorem](#cap-theorem)
      - [The Immutable Law of Distributed Systems](#the-immutable-law-of-distributed-systems)
      - [The Deep Theory: Why CAP is Inevitable](#the-deep-theory-why-cap-is-inevitable)
      - [The Three Properties: Deep Dive](#the-three-properties-deep-dive)
        - [Consistency (C)](#consistency-c)
        - [Availability (A)](#availability-a)
        - [Partition Tolerance (P)](#partition-tolerance-p)
      - [The Real Choice: CP vs AP](#the-real-choice-cp-vs-ap)
        - [CP Systems (Consistency over Availability)](#cp-systems-consistency-over-availability)
        - [AP Systems (Availability over Consistency)](#ap-systems-availability-over-consistency)
      - [CA Systems: The Myth](#ca-systems-the-myth)
      - [The Spectrum: It's Not Binary](#the-spectrum-its-not-binary)
        - [Cassandra: The Exemplar](#cassandra-the-exemplar)
      - [PACELC: The CAP Extension](#pacelc-the-cap-extension)
      - [Real-World Examples: Who Chose What?](#real-world-examples-who-chose-what)
      - [The Wisdom: How to Choose](#the-wisdom-how-to-choose)
      - [The Fundamental Insight](#the-fundamental-insight)
    - [PACELC Theorem](#pacelc-theorem)
    - [Fault Tolerance](#fault-tolerance)
    - [Disaster Recovery](#disaster-recovery)
  - [11. Architecture Patterns](#11-architecture-patterns)
    - [Monolith Architecture](#monolith-architecture)
    - [Microservices Architecture](#microservices-architecture)
    - [Event-Driven Architecture](#event-driven-architecture)
    - [Serverless Architecture](#serverless-architecture)
  - [12. Performance \& Resilience Patterns](#12-performance--resilience-patterns)
    - [Rate Limiting](#rate-limiting)
    - [Throttling](#throttling)
    - [Backpressure](#backpressure)
    - [Idempotency](#idempotency)
    - [Circuit Breaker](#circuit-breaker)
    - [Retry Mechanisms](#retry-mechanisms)
    - [Bulkhead Pattern](#bulkhead-pattern)
    - [Health Checks](#health-checks)
  - [13. Security](#13-security)
    - [Authentication vs Authorization](#authentication-vs-authorization)
    - [OAuth](#oauth)
    - [JWT (JSON Web Token)](#jwt-json-web-token)
  - [14. Observability](#14-observability)
    - [Logging](#logging)
    - [Monitoring](#monitoring)
    - [Tracing](#tracing)
    - [Alerting](#alerting)
  - [15. Advanced Concepts](#15-advanced-concepts)
    - [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
    - [Event Sourcing](#event-sourcing)
    - [Saga Pattern](#saga-pattern)
    - [Distributed Consensus](#distributed-consensus)
    - [Content Negotiation](#content-negotiation)
    - [API Versioning](#api-versioning)
  - [16. Data Processing](#16-data-processing)
    - [Batch Processing](#batch-processing)
    - [Stream Processing](#stream-processing)
    - [Text-Based Search \& Indexing](#text-based-search--indexing)
  - [17. Additional Important Concepts](#17-additional-important-concepts)
    - [Back-of-the-Envelope Calculations](#back-of-the-envelope-calculations)
    - [Data Partitioning](#data-partitioning)
    - [Cold Start Problem](#cold-start-problem)
    - [Blue-Green Deployment](#blue-green-deployment)
    - [Canary Deployment](#canary-deployment)
    - [Feature Flags](#feature-flags)
  - [18. Resources \& Learning](#18-resources--learning)
    - [Books](#books)
    - [Engineering Blogs](#engineering-blogs)
    - [Practice Resources](#practice-resources)
    - [Project Ideas](#project-ideas)
  - [Summary: The Art and Science of System Design](#summary-the-art-and-science-of-system-design)
    - [The Essential Truth](#the-essential-truth)
    - [The Core Trade-offs](#the-core-trade-offs)
    - [The Golden Rules of System Design](#the-golden-rules-of-system-design)
    - [The System Design Mental Model](#the-system-design-mental-model)
      - [**Phase 1: Understanding (Requirements \& Constraints)**](#phase-1-understanding-requirements--constraints)
      - [**Phase 2: Estimation (Back-of-the-Envelope)**](#phase-2-estimation-back-of-the-envelope)
      - [**Phase 3: Design (High-Level Architecture)**](#phase-3-design-high-level-architecture)
      - [**Phase 4: Deep Dive (Bottlenecks \& Optimization)**](#phase-4-deep-dive-bottlenecks--optimization)
      - [**Phase 5: Trade-offs (Alternatives \& Justification)**](#phase-5-trade-offs-alternatives--justification)
    - [Interview-Specific Guidance](#interview-specific-guidance)
      - [**The Interview Framework**](#the-interview-framework)
      - [**Common Interview Questions \& Approaches**](#common-interview-questions--approaches)
      - [**Red Flags to Avoid**](#red-flags-to-avoid)
      - [**Green Flags to Exhibit**](#green-flags-to-exhibit)
    - [The Path to Mastery](#the-path-to-mastery)
    - [The Journey Continues](#the-journey-continues)

---

## The Philosophy of System Design: A Unified Theory

### The Grand Vision

System design is not merely about connecting components or choosing technologies—it's about orchestrating complexity into harmony. At its core, system design is the art and science of **managing trade-offs** in pursuit of a singular goal: **building systems that serve human needs at scale while remaining economically viable and technically sustainable**.

### The Fundamental Truth: Everything is a Trade-off

In system design, there are no perfect solutions—only optimal choices for specific contexts. Every decision you make involves sacrificing one quality for another:

- **Performance vs Cost**: Faster systems require more resources
- **Consistency vs Availability**: Strong guarantees limit uptime during failures
- **Simplicity vs Flexibility**: Easy-to-use systems may lack customization
- **Speed of Development vs System Quality**: Quick launches may accumulate technical debt
- **Scalability vs Complexity**: Distributed systems bring operational overhead

**The Master's Mindset**: A great system designer doesn't seek the "best" solution—they seek the most **appropriate** solution for their specific constraints, user needs, and business goals.

### The Three Pillars of System Design

Every system, regardless of scale or domain, rests on three fundamental pillars:

#### 1. **Data** (The Foundation)
- How data is **stored** (databases, file systems, caches)
- How data is **structured** (schemas, models, formats)
- How data is **accessed** (queries, indexes, APIs)
- How data is **distributed** (replication, sharding, partitioning)
- How data maintains **integrity** (consistency, transactions, validation)

*Philosophy*: Data is the lifeblood of your system. Respect it, protect it, and structure it wisely—all other components serve to manipulate and transport this precious resource.

#### 2. **Computation** (The Engine)
- How **requests are processed** (synchronous vs asynchronous)
- How **logic is organized** (monolith, microservices, serverless)
- How **work is distributed** (load balancing, task queues)
- How **failures are handled** (retries, circuit breakers, fallbacks)
- How **performance is optimized** (caching, parallel processing, batching)

*Philosophy*: Computation transforms data into value. Design your computational model to be resilient, efficient, and aligned with your data access patterns.

#### 3. **Communication** (The Nervous System)
- How **components connect** (APIs, message queues, event streams)
- How **data flows** (request/response, pub/sub, streaming)
- How **services discover** each other (DNS, service mesh, registries)
- How **errors propagate** (graceful degradation, bulkheads)
- How **latency is minimized** (CDN, edge computing, compression)

*Philosophy*: Communication patterns define your system's behavior under stress. Choose protocols and patterns that align with your consistency and latency requirements.

### The Evolutionary Stages of System Design

Systems evolve through predictable stages. Understanding this lifecycle helps you make appropriate decisions:

#### **Stage 1: The Monolith** (0-100K users)
- Single application, single database
- Simple deployment, easy debugging
- Focus: Product-market fit
- **Philosophy**: Start simple. Premature optimization is the root of all evil.

#### **Stage 2: Vertical Scaling** (100K-500K users)
- Bigger servers, optimized queries
- Introduce caching, CDN
- Focus: Performance optimization
- **Philosophy**: Scale up before scaling out. Extract maximum value from simplicity.

#### **Stage 3: Horizontal Scaling** (500K-5M users)
- Load balancers, multiple app servers
- Database replication (read replicas)
- Service separation begins
- Focus: Reliability and availability
- **Philosophy**: Distribute load, eliminate single points of failure.

#### **Stage 4: Distributed Systems** (5M-50M users)
- Microservices architecture
- Database sharding
- Message queues, event-driven patterns
- Focus: Team autonomy, service isolation
- **Philosophy**: Embrace complexity to manage complexity. Each service is a bounded context.

#### **Stage 5: Global Scale** (50M+ users)
- Multi-region deployment
- Distributed caching (Redis cluster)
- Advanced patterns (CQRS, event sourcing)
- Focus: Low latency, high availability worldwide
- **Philosophy**: Think globally, act locally. Bring computation close to users.

### The CAP Theorem: The Immutable Law

The CAP theorem is not just a theoretical concept—it's a **fundamental law of distributed systems** that governs all design decisions:

**The Law**: In the presence of a network partition (P), you must choose between Consistency (C) and Availability (A). You cannot have all three.

**The Reality**: Network partitions are inevitable, so the real choice is always between C and A.

**The Wisdom**:
- **Choose CP** (Consistency over Availability) when correctness is non-negotiable: banking, inventory, booking systems
- **Choose AP** (Availability over Consistency) when user experience trumps immediate correctness: social feeds, recommendations, analytics

**The Nuance**: Modern systems often use **eventual consistency**—they choose AP but converge to consistency over time, providing the best of both worlds for many use cases.

### The Principle of Graceful Degradation

**Core Idea**: Systems should degrade gracefully, not catastrophically.

When components fail (and they will), your system should:
1. **Continue operating** with reduced functionality
2. **Provide clear feedback** about what's unavailable
3. **Maintain data integrity** even if features are offline
4. **Recover automatically** when dependencies return

**Examples**:
- Netflix continues playing already-loaded content when recommendations fail
- Twitter shows cached tweets when live feed is down
- E-commerce sites allow browsing when checkout is degraded

**The Philosophy**: A system that is 99% available with graceful degradation is better than one that is 99.9% available but fails catastrophically.

### The Hierarchy of Optimization

Optimize in this order—deviation leads to wasted effort:

1. **Correctness**: Does it work? (Tests, validation, monitoring)
2. **Availability**: Is it reliable? (Redundancy, failover, health checks)
3. **Latency**: Is it fast enough? (Caching, indexing, CDN)
4. **Throughput**: Can it handle the load? (Scaling, load balancing)
5. **Cost**: Is it economical? (Resource optimization, auto-scaling)

**Warning**: Optimizing out of order creates fast, scalable systems that produce wrong results, or correct systems that cost millions to operate.

### The Data Gravity Principle

**Law**: Computation moves to where data lives, not vice versa.

**Why**: Moving large datasets is expensive (bandwidth, latency, cost). It's almost always cheaper to send code to data.

**Implications**:
- Store data close to users (CDN, regional databases)
- Process data where it's generated (edge computing)
- Replicate read-heavy data, shard write-heavy data
- Use database views/materialized views instead of moving data

### The Principle of Least Surprise

**Core Idea**: Design systems that behave as users and developers expect.

- **APIs**: Follow REST conventions or GraphQL standards
- **Status Codes**: Use HTTP codes correctly (200, 404, 500)
- **Error Messages**: Be clear and actionable
- **Documentation**: Keep it updated and accurate
- **Naming**: Use intuitive, consistent names

**The Philosophy**: Surprises in production are bugs. Predictable systems are debuggable systems.

### The Observability Imperative

**Core Truth**: You cannot improve what you cannot measure. You cannot fix what you cannot see.

**The Three Pillars**:
1. **Logs**: What happened? (Events, errors, transactions)
2. **Metrics**: How much? How fast? (Counters, gauges, histograms)
3. **Traces**: Where did it go? (Distributed request tracking)

**The Practice**:
- Log with correlation IDs
- Monitor golden signals (latency, traffic, errors, saturation)
- Alert on symptoms, not causes
- Build dashboards for different audiences (business, ops, engineering)

**The Philosophy**: In distributed systems, observability is not optional—it's the only way to maintain sanity.

### The Security-First Mindset

**Core Principle**: Security is not a feature—it's a foundation.

**The Layers of Defense**:
1. **Network**: Firewalls, VPCs, security groups
2. **Application**: Authentication, authorization, input validation
3. **Data**: Encryption at rest and in transit
4. **Infrastructure**: Patching, least privilege, monitoring

**The Rules**:
- Never trust user input
- Always use HTTPS
- Store passwords hashed (bcrypt, Argon2)
- Implement rate limiting
- Use principle of least privilege
- Encrypt sensitive data
- Regular security audits

**The Philosophy**: A system breach can destroy years of work in minutes. Design with paranoia.

### The Cost-Consciousness Principle

**Reality Check**: Engineering time is expensive. Infrastructure is expensive. Downtime is expensive.

**Optimize for**:
1. **Total Cost of Ownership** (not just infrastructure)
   - Engineering time (maintenance, debugging)
   - Operational overhead
   - Infrastructure costs
   - Opportunity cost

2. **ROI of Complexity**
   - Does microservices justify operational overhead?
   - Does distributed caching justify maintenance burden?
   - Does multi-region justify complexity cost?

**The Philosophy**: The best architecture is the simplest one that meets requirements. Complexity is a tax you pay forever.

### The Testing Pyramid: Quality Assurance

**Structure** (from bottom to top):
1. **Unit Tests** (70%): Fast, isolated, abundant
2. **Integration Tests** (20%): Components together
3. **End-to-End Tests** (10%): Full user flows

**Add Layers**:
- **Contract Tests**: API compatibility
- **Performance Tests**: Load, stress, spike
- **Chaos Engineering**: Deliberate failure injection

**The Philosophy**: Quality is not accidental. Test at every layer, automate ruthlessly.

### The Human Element

**Remember**: Systems are built by humans, for humans.

**Team Considerations**:
- **Conway's Law**: System design mirrors team structure
- **Cognitive Load**: Keep systems understandable
- **On-call Burden**: Design for operational simplicity
- **Knowledge Transfer**: Document decisions and rationale

**User Considerations**:
- **Latency**: Every 100ms delay decreases conversions
- **Reliability**: Users remember failures more than successes
- **Privacy**: Respect user data as sacred
- **Accessibility**: Design for all users

### The Unified Theory of System Design

**Synthesis**: Great system design is the intersection of:

1. **Technical Excellence**: Right tools, patterns, architectures
2. **Business Alignment**: Meets actual needs, delivers value
3. **Operational Reality**: Can be monitored, debugged, maintained
4. **Human Factors**: Understandable, usable, ethical
5. **Economic Viability**: Cost-effective, sustainable

**The Meta-Principle**: Context is king. The "best" design depends entirely on:
- Scale (users, data, requests)
- Requirements (latency, consistency, features)
- Constraints (budget, team, timeline)
- Trade-offs (what you're willing to sacrifice)

**The Journey**: Mastery comes from:
1. Learning patterns and principles (theory)
2. Making mistakes and learning (practice)
3. Understanding trade-offs deeply (wisdom)
4. Knowing when to break rules (mastery)

---

## 1. Introduction to System Design

### Why Learn System Design
System design is crucial for building scalable, reliable, and maintainable software systems. It helps you:
- Understand how large-scale systems work
- Make informed architectural decisions
- Prepare for technical interviews at top tech companies
- Design systems that can handle millions of users
- Build fault-tolerant and resilient applications

### How to Learn System Design
1. **Start with fundamentals** - networking, databases, OS concepts
2. **Study existing systems** - analyze how popular services work
3. **Practice design exercises** - design systems like Twitter, Netflix, Uber
4. **Read engineering blogs** - learn from companies like Netflix, Uber, Meta
5. **Build projects** - implement scaled-down versions of real systems
6. **Review case studies** - understand trade-offs in real-world designs

### How to Approach System Design in Interviews
1. **Clarify requirements** - functional and non-functional
2. **Estimate scale** - users, requests, storage needs
3. **Define APIs** - key endpoints and data models
4. **High-level design** - major components and data flow
5. **Deep dive** - bottlenecks, scaling, and optimization
6. **Trade-offs** - discuss alternatives and their pros/cons

---

## 2. Foundational Concepts

### Client-Server Architecture

#### The Foundational Paradigm of Distributed Computing

Client-Server architecture is not merely a pattern—it's the **fundamental organizing principle** of modern computing. It represents the first great abstraction in distributed systems: the separation of **concerns** (what you want) from **capabilities** (how it's provided).

#### The Deep Theory

**Philosophical Foundation:**
At its core, client-server embodies the principle of **asymmetric responsibility**. The client owns the **interface and experience**, while the server owns the **truth and capability**. This separation allows:
- **Specialization**: Each side optimizes for its role
- **Evolution**: Clients and servers can evolve independently
- **Scaling**: Multiple clients can share server resources
- **Security**: Centralized control of critical operations

**The Trust Boundary:**
The client-server split creates the first **trust boundary** in your system. Everything on the client side is **untrusted** (can be modified, inspected, bypassed), while the server maintains **authoritative state**. This is why:
- Never trust client input (validate everything)
- Business logic belongs on the server
- Sensitive operations require server-side execution
- Client-side validations are for UX, not security

#### The State Problem

**Stateless Servers (The Ideal):**
- Each request contains all needed context
- Servers can be replaced/restarted freely
- Horizontal scaling is trivial (any server can handle any request)
- Load balancing is simple (round-robin works)
- **Trade-off**: Larger requests (repeated data), authentication overhead

**Stateful Servers (The Reality):**
- Server remembers client context (sessions)
- Better performance (no repeated data)
- Smaller requests
- **Trade-off**: Complex scaling (sticky sessions), harder failover, memory pressure

**The Modern Solution: Hybrid**
- Application servers are stateless
- State stored in external systems (Redis, databases)
- Best of both worlds: scalable servers + persistent state

#### Architectural Tiers: Evolution of Separation

**Two-Tier (Client-Server):**
```
[Client] ←→ [Server + Database]
```
- **Use Case**: Simple apps, internal tools, MVPs
- **Pros**: Simple, fast development, low latency
- **Cons**: Tight coupling, limited scalability, difficult updates
- **Example**: Desktop database applications, early web apps

**Three-Tier (Presentation-Logic-Data):**
```
[Client] ←→ [Application Server] ←→ [Database Server]
```
- **Use Case**: Most modern web applications
- **Pros**: Clear separation, independent scaling, security isolation
- **Cons**: Network latency, more complex deployment
- **The Standard**: This is the default for good reason—it balances complexity with flexibility

**N-Tier (Distributed Architecture):**
```
[Client] ←→ [Load Balancer] ←→ [API Gateway] ←→ [App Servers] ←→ [Cache] ←→ [Databases]
                                    ↓
                            [Message Queue] ←→ [Workers]
```
- **Use Case**: Large-scale, complex systems
- **Pros**: Ultimate flexibility, independent scaling, fault isolation
- **Cons**: Operational complexity, debugging challenges, network overhead
- **When**: Only when scale or complexity demands it

#### The Communication Contract: APIs

The client-server boundary is defined by **contracts** (APIs):
- **Syntax**: How to format requests (HTTP, gRPC, GraphQL)
- **Semantics**: What requests mean (REST resources, RPC methods)
- **Guarantees**: What you can expect (idempotency, atomicity)

**The API as Interface:**
Think of the API as an **interface** in object-oriented programming:
- Hides implementation details
- Defines a contract
- Allows implementation to change
- Version carefully (breaking changes hurt)

#### Request-Response Patterns

**Synchronous (Request-Response):**
```
Client: "Give me user 123"
  ↓ (waits)
Server: "Here's the data"
```
- **Use**: Queries, transactional operations, real-time needs
- **Limitation**: Client blocks, server must respond quickly

**Asynchronous (Fire-and-Forget):**
```
Client: "Process this video"
Server: "Got it, here's task ID 456"
  ↓ (client continues)
Client: "What's status of 456?"
Server: "Still processing..."
```
- **Use**: Long operations, batch processing, background tasks
- **Benefit**: Client doesn't block, server can take time

**Push (Server-Initiated):**
```
Client: "Subscribe to notifications"
  ↓ (keeps connection open)
Server: (later) "New message arrived!"
```
- **Use**: Real-time updates, live data, notifications
- **Technologies**: WebSockets, Server-Sent Events, Long Polling

#### The Scalability Implications

**Scaling Clients:**
- Essentially unlimited (users bring their own devices)
- Main concern: API rate limits, DDoS protection

**Scaling Servers:**
- **Vertical**: Bigger machines (limited, expensive)
- **Horizontal**: More machines (requires stateless design)
- **The Pattern**: Start vertical, go horizontal when needed

#### Modern Evolutions

**Thin Client (Web/Mobile Apps):**
- Client is mostly UI rendering
- All logic on server
- **Benefit**: Easy updates (server-side only), consistent logic
- **Trade-off**: Requires network, server dependency

**Thick Client (SPAs, Desktop Apps):**
- Significant logic on client
- Server is data API
- **Benefit**: Responsive UI, offline capability, reduced server load
- **Trade-off**: Complex client code, version fragmentation

**Hybrid (Progressive Web Apps):**
- Client can work offline (service workers)
- Syncs when connected
- **Best of Both**: Online performance, offline capability

#### The Fundamental Trade-offs

| Aspect | Client-Heavy | Server-Heavy |
|--------|-------------|-------------|
| **Performance** | Fast UI, network dependent | Depends on server speed |
| **Security** | Lower (code visible) | Higher (code hidden) |
| **Scalability** | Server load reduced | Server must handle all logic |
| **Updates** | Must update all clients | Update once (server) |
| **Offline** | Possible with caching | Not possible |
| **Consistency** | Harder (client versions) | Easier (single source) |

#### The Wisdom

**Start Server-Heavy:**
- Business logic on server (security, consistency)
- Thin clients (easier to update)
- Move to client only when needed (performance, offline)

**The Golden Rule:**
*"Never trust the client. Always validate on the server. The client is for user experience, the server is for truth."*

**Modern Best Practice:**
- **Presentation**: Client (React, Vue, Swift)
- **Business Logic**: Server (Node, Python, Java)
- **Data**: Databases (PostgreSQL, MongoDB)
- **State**: External store (Redis)
- **Communication**: REST/GraphQL for queries, WebSockets for real-time

### IP Addresses & Ports

#### IP Addresses: The Internet's Postal System

**IP Address**: Unique identifier for devices on a network - like a street address for computers.

##### IPv4 Architecture

**Format**: 32-bit address (4 bytes), written as dotted decimal
```
192.168.1.100
 ↓   ↓   ↓  ↓
 1   2   3  4  (octets)

Binary representation:
11000000.10101000.00000001.01100100
```

**Address Classes:**
```
Class A: 0.0.0.0      to 127.255.255.255   (16M hosts/network)
         [Network].[Host].[Host].[Host]
         Example: 10.1.2.3

Class B: 128.0.0.0    to 191.255.255.255   (65K hosts/network)
         [Network].[Network].[Host].[Host]
         Example: 172.16.1.100

Class C: 192.0.0.0    to 223.255.255.255   (254 hosts/network)
         [Network].[Network].[Network].[Host]
         Example: 192.168.1.50
```

**Private vs Public IP Addresses:**

```
Private IP Ranges (RFC 1918):
┌─────────────────────────────────────────────────┐
│ 10.0.0.0      - 10.255.255.255   (Class A)     │
│ 172.16.0.0    - 172.31.255.255   (Class B)     │
│ 192.168.0.0   - 192.168.255.255  (Class C)     │
└─────────────────────────────────────────────────┘
     ↓ Not routable on public Internet
     ↓ Used inside organizations
     ↓ NAT translates to public IP

Public IP:
     ↓ Globally unique
     ↓ Routable on Internet
     ↓ Assigned by ISP/cloud provider
```

**Real-World Example:**
```
Your Home Network:
┌──────────────────────────────────────────┐
│ Public IP: 203.0.113.45 (ISP-assigned)  │
│                                          │
│  Router (NAT)                           │
│    └─ Private Network: 192.168.1.0/24   │
│         ├─ Laptop:  192.168.1.10       │
│         ├─ Phone:   192.168.1.11       │
│         └─ Tablet:  192.168.1.12       │
└──────────────────────────────────────────┘

Outbound connection:
Laptop (192.168.1.10:5000) 
  → NAT translates to →
Public (203.0.113.45:5000)
  → Internet
```

##### IPv6: The Future (and Present)

**Format**: 128-bit address (16 bytes), written in hexadecimal
```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
  ↓ Simplified (remove leading zeros):
2001:db8:85a3:0:0:8a2e:370:7334
  ↓ Further simplified (:: for consecutive zeros):
2001:db8:85a3::8a2e:370:7334
```

**Why IPv6?**
```
IPv4 addresses: 4.3 billion (2^32)
  ↓ Exhausted in 2011
  ↓ NAT is a workaround, not a solution

IPv6 addresses: 340 undecillion (2^128)
  ↓ 340,282,366,920,938,463,463,374,607,431,768,211,456
  ↓ Enough for every grain of sand on Earth
```

**IPv6 Example:**
```
Global Unicast Address:
2001:db8:85a3:1234:5678:8a2e:370:7334
│    │   │    │    │    │    │   └── Interface ID
│    │   │    └────┴────┴────┴────── Subnet/Host
└────┴───┴────────────────────────── Network Prefix
```

#### Ports: Doorways to Applications

**Concept**: IP gets you to the building (server), port gets you to the right apartment (application).

```
Server: 192.168.1.100
┌──────────────────────────┐
│ Port 80:  Web Server     │ ← http://192.168.1.100:80
│ Port 443: HTTPS          │ ← https://192.168.1.100:443
│ Port 22:  SSH            │ ← ssh user@192.168.1.100
│ Port 3306: MySQL         │ ← mysql://192.168.1.100:3306
│ Port 5432: PostgreSQL    │ ← postgres://192.168.1.100:5432
│ Port 6379: Redis         │ ← redis://192.168.1.100:6379
└──────────────────────────┘
```

##### Port Ranges and Their Purposes

**Well-Known Ports (0-1023):** System/privileged services
```
20/21   FTP (File Transfer)
22      SSH (Secure Shell)
23      Telnet (insecure, avoid)
25      SMTP (Email sending)
53      DNS (Domain Name System)
80      HTTP (Web)
110     POP3 (Email retrieval)
143     IMAP (Email access)
443     HTTPS (Secure web)
3306    MySQL
5432    PostgreSQL
6379    Redis
27017   MongoDB
```

**Registered Ports (1024-49151):** User applications
```
3000    Node.js development
5000    Flask default
8000    Django development
8080    Alternative HTTP
8443    Alternative HTTPS
9200    Elasticsearch
```

**Dynamic/Private Ports (49152-65535):** Temporary client connections
```
Client connects:
192.168.1.10:54231 → 93.184.216.34:443
     ↑                        ↑
  Random port            HTTPS port
  (ephemeral)            (well-known)
```

##### Real-World Use Cases

**Use Case 1: Web Server**
```
Setup:
┌─────────────────────────────────┐
│ Server: example.com (1.2.3.4)  │
│   Port 80:  HTTP (redirect)    │
│   Port 443: HTTPS (main site)  │
└─────────────────────────────────┘

User types: http://example.com
  ↓ Browser resolves DNS
Connects to: 1.2.3.4:80
  ↓ Server responds
301 Redirect to https://example.com
  ↓ Browser reconnects
Connects to: 1.2.3.4:443
  ↓ Secure connection established
Serves website
```

**Use Case 2: Microservices Architecture**
```
Server: 10.0.1.50
┌──────────────────────────────────┐
│ 3000: Auth Service               │ ← JWT validation
│ 3001: User Service               │ ← User CRUD
│ 3002: Product Service            │ ← Catalog
│ 3003: Order Service              │ ← Orders
│ 6379: Redis (shared cache)       │ ← Session store
│ 5432: PostgreSQL (shared DB)     │ ← Data persistence
└──────────────────────────────────┘

API Gateway: 10.0.1.10:80
  Routes:
    /auth/*     → 10.0.1.50:3000
    /users/*    → 10.0.1.50:3001
    /products/* → 10.0.1.50:3002
    /orders/*   → 10.0.1.50:3003
```

**Use Case 3: Database Cluster**
```
PostgreSQL Cluster:
┌─────────────────────────────────────┐
│ Primary:   10.0.2.10:5432 (writes) │
│ Replica 1: 10.0.2.11:5432 (reads)  │
│ Replica 2: 10.0.2.12:5432 (reads)  │
└─────────────────────────────────────┘

Application config:
write_db = "postgresql://10.0.2.10:5432/mydb"
read_db = [
    "postgresql://10.0.2.11:5432/mydb",
    "postgresql://10.0.2.12:5432/mydb"
]
```

##### Code Example: Socket Programming

**Python Server (Listens on IP:Port):**
```python
import socket

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to IP and Port
host = '0.0.0.0'  # Listen on all network interfaces
port = 8080
server_socket.bind((host, port))

# Listen for connections
server_socket.listen(5)
print(f"Server listening on {host}:{port}")

while True:
    # Accept client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address[0]}:{client_address[1]}")
    
    # Send response
    client_socket.send(b"HTTP/1.1 200 OK\r\n\r\nHello, World!")
    client_socket.close()
```

**Python Client (Connects to IP:Port):**
```python
import socket

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
server_ip = '192.168.1.100'
server_port = 8080
client_socket.connect((server_ip, server_port))

# Send request
client_socket.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")

# Receive response
response = client_socket.recv(4096)
print(response.decode())

client_socket.close()
```

##### Network Address Translation (NAT)

**The Problem:**
Private IPs can't communicate with public internet directly.

**The Solution: NAT**
```
Internal Network                    NAT Router                 Internet
┌─────────────────┐              ┌────────────┐           ┌──────────┐
│ PC1: 192.168.1.10│──┐          │            │           │          │
│ PC2: 192.168.1.11│──┼─────────▶│  Translates │──────────▶│ Internet │
│ PC3: 192.168.1.12│──┘          │   to/from  │◀──────────│  Servers │
└─────────────────┘              │203.0.113.45│           └──────────┘
                                  └────────────┘
                                  Public IP: 203.0.113.45

NAT Translation Table:
┌──────────────────────────────────────────────────────┐
│ Internal IP:Port    │  NAT IP:Port     │ Destination │
├────────────────────────────────────────────────────────┤
│ 192.168.1.10:5000  │  203.0.113.45:5000│  8.8.8.8:53 │
│ 192.168.1.11:5001  │  203.0.113.45:5001│  1.1.1.1:443│
│ 192.168.1.12:5002  │  203.0.113.45:5002│  93.1.1.1:80│
└──────────────────────────────────────────────────────┘
```

**Outbound Request Flow:**
```
1. PC1 (192.168.1.10:5000) sends to Google (8.8.8.8:443)
   ↓
2. Router receives, creates NAT entry
   ↓
3. Router rewrites source to (203.0.113.45:5000)
   ↓
4. Google receives from (203.0.113.45:5000)
   ↓
5. Google responds to (203.0.113.45:5000)
   ↓
6. Router checks NAT table, finds PC1
   ↓
7. Router forwards to (192.168.1.10:5000)
   ↓
8. PC1 receives response
```

##### Common Networking Commands

**Find your IP address:**
```bash
# Linux/Mac
ifconfig          # Show all interfaces
ip addr show      # Modern alternative
hostname -I       # Just the IPs

# Windows
ipconfig          # Show all adapters

# Output example:
eth0: inet 192.168.1.100  netmask 255.255.255.0
      ↑ Your local IP
```

**Check which process is using a port:**
```bash
# Linux/Mac
sudo lsof -i :8080
sudo netstat -tuln | grep 8080

# Windows
netstat -ano | findstr :8080

# Output:
PID   PORT   PROCESS
1234  8080   node
```

**Test connection to IP:Port:**
```bash
# Check if port is open
telnet 192.168.1.100 8080
nc -zv 192.168.1.100 8080     # netcat

# Test HTTP endpoint
curl http://192.168.1.100:8080/health

# Scan ports on a host
nmap 192.168.1.100 -p 80,443,8080
```

##### Security Considerations

**Firewall Rules:**
```bash
# Allow specific port (iptables)
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Block all other incoming
sudo iptables -A INPUT -j DROP

# AWS Security Group example:
Inbound Rules:
┌──────────┬──────────┬─────────────┬─────────────┐
│ Type     │ Protocol │ Port        │ Source      │
├──────────┼──────────┼─────────────┼─────────────┤
│ HTTP     │ TCP      │ 80          │ 0.0.0.0/0   │
│ HTTPS    │ TCP      │ 443         │ 0.0.0.0/0   │
│ SSH      │ TCP      │ 22          │ MyIP/32     │
│ Custom   │ TCP      │ 3000        │ VPC only    │
└──────────┴──────────┴─────────────┴─────────────┘
```

**Best Practices:**
```
✓ Expose only necessary ports
✓ Use non-standard ports for SSH (e.g., 2222 instead of 22)
✓ Restrict admin ports to specific IPs
✓ Use VPN for internal service access
✓ Enable firewall on all servers
✗ Don't expose databases directly to internet
✗ Don't use default ports for sensitive services
```

### Domain Name System (DNS)

#### The Internet's Phone Book

DNS translates human-readable domain names (www.example.com) to machine-readable IP addresses (93.184.216.34). Without DNS, you'd need to memorize IP addresses for every website.

#### How DNS Resolution Works: The Complete Journey

**The 8-Step Resolution Process:**

```
User types: www.example.com in browser

1. Browser Cache Check
   ┌──────────────────┐
   │ Browser Cache    │ → "Do I know this?"
   └──────────────────┘    ↓ Cache miss

2. Operating System Cache
   ┌──────────────────┐
   │ OS DNS Cache     │ → "Do I know this?"
   └──────────────────┘    ↓ Cache miss

3. Router Cache
   ┌──────────────────┐
   │ Router Cache     │ → "Do I know this?"
   └──────────────────┘    ↓ Cache miss

4. ISP DNS Resolver (Recursive Resolver)
   ┌──────────────────┐
   │ ISP Resolver     │ → "Let me find out!"
   │ 8.8.8.8          │
   └──────────────────┘
         ↓
         ↓ Query: www.example.com?
         ↓

5. Root DNS Server
   ┌──────────────────┐
   │ Root Server      │ → "Ask .com server at 192.5.6.30"
   │ a.root-servers   │
   └──────────────────┘
         ↓
         ↓ Query: www.example.com?
         ↓

6. TLD (Top-Level Domain) Server
   ┌──────────────────┐
   │ .com TLD Server  │ → "Ask example.com's NS at 1.2.3.4"
   │ 192.5.6.30       │
   └──────────────────┘
         ↓
         ↓ Query: www.example.com?
         ↓

7. Authoritative Name Server
   ┌──────────────────┐
   │ example.com NS   │ → "www.example.com = 93.184.216.34"
   │ 1.2.3.4          │
   └──────────────────┘
         ↓
         ↓ Returns IP
         ↓

8. Back to User
   ┌──────────────────┐
   │ Browser          │ ← "93.184.216.34"
   └──────────────────┘
         ↓
   Connects to 93.184.216.34:443 (HTTPS)
```

**Timing Example:**
```
First Visit (no cache):
  Browser cache:     0ms (miss)
  OS cache:          0ms (miss)
  ISP resolver:      2ms (miss)
  Root server:       20ms
  TLD server:        30ms
  Authoritative:     25ms
  Total:            ~77ms

Second Visit (cached):
  Browser cache:     0ms (hit!)
  Total:             0ms (instant)
```

#### DNS Record Types: The Complete Reference

##### A Record (Address Record)
**Purpose**: Map domain to IPv4 address

```
DNS Query:
  example.com. IN A

DNS Response:
  example.com.  3600  IN  A  93.184.216.34
               ↑ TTL      ↑ IP Address

Meaning: "example.com is at 93.184.216.34 for 3600 seconds"
```

**Use Cases:**
```
# Main website
www.example.com → 93.184.216.34

# Subdomain for API
api.example.com → 93.184.216.35

# Multiple IPs for load balancing
www.example.com → 93.184.216.34
www.example.com → 93.184.216.35
www.example.com → 93.184.216.36
```

##### AAAA Record (IPv6 Address)
**Purpose**: Map domain to IPv6 address

```
example.com.  3600  IN  AAAA  2001:db8:85a3::8a2e:370:7334
```

**Modern Setup:**
```
# Dual-stack (both IPv4 and IPv6)
example.com.  IN  A     93.184.216.34
example.com.  IN  AAAA  2001:db8:85a3::8a2e:370:7334

Browser behavior:
1. Checks for AAAA (IPv6) first
2. Falls back to A (IPv4) if unavailable
```

##### CNAME Record (Canonical Name)
**Purpose**: Alias one domain to another

```
www.example.com.  IN  CNAME  example.com.

Resolution:
www.example.com → (CNAME) → example.com → (A) → 93.184.216.34
```

**Real-World Examples:**
```
# CDN Setup
static.example.com.  IN  CNAME  d111111abcdef8.cloudfront.net.

# Subdomain aliasing
blog.example.com.    IN  CNAME  myblog.wordpress.com.

# Environment-specific
staging.example.com. IN  CNAME  staging-server.aws.example.com.

# Load balancer
www.example.com.     IN  CNAME  lb-12345.us-east-1.elb.amazonaws.com.
```

**CNAME Limitations:**
```
✗ Can't use at root domain (example.com)
  (RFC violation, but some providers allow it)

✗ Can't coexist with other records
  example.com. CNAME  other.com.  ← Invalid
  example.com. MX     mail.com.   ← Conflict!

✓ Perfect for subdomains
  www.example.com. CNAME other.com.  ← Valid
```

##### MX Record (Mail Exchange)
**Purpose**: Specify mail servers for domain

```
example.com.  IN  MX  10  mail1.example.com.
example.com.  IN  MX  20  mail2.example.com.
                   ↑ Priority (lower = preferred)

Email to: user@example.com
  ↓
DNS lookup: example.com MX records
  ↓
Try mail1 (priority 10) first
If fails, try mail2 (priority 20)
```

**Google Workspace Example:**
```
example.com.  IN  MX  1   aspmx.l.google.com.
example.com.  IN  MX  5   alt1.aspmx.l.google.com.
example.com.  IN  MX  5   alt2.aspmx.l.google.com.
example.com.  IN  MX  10  alt3.aspmx.l.google.com.
example.com.  IN  MX  10  alt4.aspmx.l.google.com.
```

##### TXT Record (Text Information)
**Purpose**: Store arbitrary text, verification, security policies

**SPF (Sender Policy Framework) - Prevent Email Spoofing:**
```
example.com.  IN  TXT  "v=spf1 include:_spf.google.com ~all"

Meaning:
  v=spf1          → Version 1
  include:...     → Allow Google's mail servers
  ~all            → Soft fail others (probably spam)
```

**DKIM (DomainKeys Identified Mail) - Email Signature:**
```
default._domainkey.example.com.  IN  TXT  "v=DKIM1; k=rsa; p=MIGfMA0GCS..."
                                             ↑ Public key for verification
```

**DMARC (Domain-based Message Authentication):**
```
_dmarc.example.com.  IN  TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"

Meaning:
  p=reject        → Reject emails that fail SPF/DKIM
  rua=mailto:...  → Send reports to this email
```

**Domain Verification:**
```
# Google Search Console
example.com.  IN  TXT  "google-site-verification=abc123..."

# SSL Certificate Validation
_acme-challenge.example.com.  IN  TXT  "validation-token-here"
```

##### NS Record (Name Server)
**Purpose**: Delegate domain to specific DNS servers

```
example.com.  IN  NS  ns1.nameserver.com.
example.com.  IN  NS  ns2.nameserver.com.

Meaning: "Ask these servers for example.com records"
```

**Subdomain Delegation:**
```
# Main domain managed by Cloudflare
example.com.      IN  NS  ns1.cloudflare.com.

# Blog subdomain managed by WordPress
blog.example.com. IN  NS  ns1.wordpress.com.
                           ns2.wordpress.com.
```

##### Other Important Records

**SRV Record (Service Location):**
```
_service._proto.name.  TTL  IN  SRV  priority weight port target

Example (Minecraft server):
_minecraft._tcp.example.com.  IN  SRV  0 5 25565  mc.example.com.
                                       ↑ ↑   ↑      ↑
                                     Pri Wt Port  Host
```

**CAA Record (Certificate Authority Authorization):**
```
example.com.  IN  CAA  0 issue "letsencrypt.org"

Meaning: "Only Let's Encrypt can issue SSL certs for this domain"
```

#### DNS Caching: The Speed Secret

**TTL (Time To Live):**
```
example.com.  3600  IN  A  93.184.216.34
              ↑ Cache for 3600 seconds (1 hour)

TTL Strategy:
Static content:    86400  (24 hours)
Dynamic content:   300    (5 minutes)
Before migration:  60     (1 minute) ← Quick updates
After migration:   3600   (1 hour)   ← Stable
```

**Cache Hierarchy:**
```
┌─────────────────┐  TTL: Varies
│ Browser Cache   │  (respects TTL)
└────────┬────────┘
         ↓
┌─────────────────┐  TTL: Varies
│ OS Cache        │  (respects TTL)
└────────┬────────┘
         ↓
┌─────────────────┐  TTL: Varies
│ ISP Resolver    │  (might ignore TTL)
└────────┬────────┘
         ↓
┌─────────────────┐  Authoritative
│ DNS Server      │  (source of truth)
└─────────────────┘
```

#### Real-World Use Cases

**Use Case 1: Multi-Region Setup**
```
GeoDNS Routing:

User in US → DNS returns: 52.1.1.1  (US East server)
User in EU → DNS returns: 18.1.1.1  (EU West server)
User in Asia → DNS returns: 13.1.1.1 (Asia Pacific server)

Configuration (Route 53 example):
www.example.com
  ├─ US-EAST-1:  52.1.1.1   (for North America)
  ├─ EU-WEST-1:  18.1.1.1   (for Europe)
  └─ AP-SOUTHEAST-1: 13.1.1.1 (for Asia)
```

**Use Case 2: Blue-Green Deployment**
```
Before deployment:
www.example.com → 10.0.1.50 (blue environment - v1.0)

During deployment:
1. Deploy v2.0 to green: 10.0.1.51
2. Test green environment
3. Update DNS:
   www.example.com → 10.0.1.51 (green environment - v2.0)
4. Wait for TTL to expire
5. All traffic now on v2.0
6. Keep blue as rollback option

Rollback (if needed):
www.example.com → 10.0.1.50 (back to blue - v1.0)
```

**Use Case 3: CDN Configuration**
```
Setup:
┌──────────────────────────────────────┐
│ Origin Server: origin.example.com    │
│ IP: 93.184.216.34                    │
└──────────────────────────────────────┘
         ↑
         │ Pulls content
         │
┌──────────────────────────────────────┐
│ CDN: d123.cloudfront.net             │
│ Edge Locations: 200+ globally        │
└──────────────────────────────────────┘
         ↑
         │ CNAME
         │
┌──────────────────────────────────────┐
│ Public DNS:                          │
│ www.example.com → d123.cloudfront.net│
│ static.example.com → d123.cloudfront │
└──────────────────────────────────────┘
```

**Use Case 4: Failover Configuration**
```
Health Check Based Failover:

Primary:
www.example.com → 10.0.1.100 (primary server)
  ↓ Health check fails!
  ↓
Automatic Failover:
www.example.com → 10.0.2.100 (backup server)

Route 53 Config:
www.example.com
  Primary:  10.0.1.100 (healthy check every 30s)
  Secondary: 10.0.2.100 (used if primary fails)
```

#### DNS Commands & Tools

**Query DNS Records:**
```bash
# Using dig (most detailed)
dig example.com
dig example.com A
dig example.com MX
dig @8.8.8.8 example.com  # Query specific DNS server

# Using nslookup
nslookup example.com
nslookup -type=MX example.com

# Using host
host example.com
host -t MX example.com
```

**Example dig output:**
```bash
$ dig example.com

; <<>> DiG 9.10.6 <<>> example.com
;; ANSWER SECTION:
example.com.    3600    IN    A    93.184.216.34
                ↑ TTL        ↑ Type  ↑ IP

;; Query time: 23 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Sat Jan 25 10:30:00 PST 2026
```

**Flush DNS Cache:**
```bash
# macOS
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches
sudo /etc/init.d/nscd restart

# Chrome browser
chrome://net-internals/#dns → Clear host cache
```

**Check DNS Propagation:**
```bash
# Query multiple DNS servers worldwide
dig @8.8.8.8 example.com      # Google (US)
dig @1.1.1.1 example.com      # Cloudflare (Global)
dig @208.67.222.222 example.com  # OpenDNS (US)

# Online tools:
# https://www.whatsmydns.net
# https://dnschecker.org
```

#### DNS Security

**DNSSEC (DNS Security Extensions):**
```
Problem: DNS responses can be spoofed

Solution: Cryptographic signatures

1. DNS server signs responses with private key
2. Client verifies with public key (DS/DNSKEY records)
3. Chain of trust from root to your domain

Example:
example.com.  IN  DNSKEY  257 3 8 AwEAAa...
                              ↑ Public key

example.com.  IN  RRSIG   A 8 2 3600 20260201000000 ...
                              ↑ Signature
```

**DNS over HTTPS (DoH) / DNS over TLS (DoT):**
```
Traditional DNS: Plain text (can be intercepted)
  User → ISP DNS (port 53, unencrypted)

DoH/DoT: Encrypted
  User → Cloudflare 1.1.1.1 (HTTPS/TLS, encrypted)

Benefits:
  ✓ Privacy (ISP can't see queries)
  ✓ Integrity (can't be modified)
  ✓ Bypasses censorship
```

#### Common DNS Issues

**Issue 1: Propagation Delay**
```
Problem:
  Changed DNS record, but old IP still appears

Cause:
  TTL not expired, caches still have old value

Solution:
  1. Lower TTL before changes (24 hours in advance)
  2. Make changes
  3. Wait for old TTL to expire
  4. Raise TTL back to normal
```

**Issue 2: CNAME at Root**
```
Problem:
  example.com. CNAME other.com.  ← Not allowed!

Reason:
  RFC violation (conflicts with NS, MX records)

Solution:
  Use A/AAAA record at root
  Or use ALIAS/ANAME record (provider-specific)
```

**Issue 3: Multiple CNAMEs**
```
Problem:
  www → cdn → lb → server (too many hops)

Impact:
  Multiple DNS lookups = slower

Solution:
  Minimize CNAME chain depth
  Use A records when possible
```

#### Best Practices

```
✓ Use low TTL (300s) before making changes
✓ Use high TTL (3600s+) for stable records
✓ Implement DNSSEC for security
✓ Use multiple NS records (redundancy)
✓ Monitor DNS health (uptime, latency)
✓ Use GeoDNS for global applications
✓ Enable health-check based failover

✗ Don't use single DNS provider (SPOF)
✗ Don't set TTL too low permanently (load on DNS)
✗ Don't forget to update NS records when changing providers
✗ Don't use CNAME at root domain
```

### Cloud Computing
On-demand delivery of computing resources over the internet.

**Service Models:**
- **IaaS** (Infrastructure): Virtual machines, storage (AWS EC2, Azure VMs)
- **PaaS** (Platform): Managed runtime environments (Heroku, Google App Engine)
- **SaaS** (Software): Complete applications (Gmail, Salesforce)
- **FaaS** (Functions): Serverless compute (AWS Lambda, Azure Functions)

**Deployment Models:**
- **Public Cloud**: Shared infrastructure (AWS, Azure, GCP)
- **Private Cloud**: Dedicated to one organization
- **Hybrid Cloud**: Mix of public and private
- **Multi-Cloud**: Multiple cloud providers

---

## 3. Network Protocols

### Protocols
Rules and standards for network communication.

**Layer Models:**
- **OSI Model**: 7 layers (Physical, Data Link, Network, Transport, Session, Presentation, Application)
- **TCP/IP Model**: 4 layers (Network Access, Internet, Transport, Application)

### TCP Protocol (Transmission Control Protocol)

#### The Reliable Foundation of the Internet

TCP is one of the **crown jewels of computer science**—a protocol so elegant and robust that it has powered the internet for over 40 years. It represents the solution to one of computing's hardest problems: **how to guarantee reliable, ordered delivery over an unreliable network**.

#### The Deep Theory: Solving the Impossible

**The Problem TCP Solves:**
The internet is fundamentally **unreliable**:
- Packets get lost (router failures, congestion)
- Packets get corrupted (bit flips, interference)
- Packets arrive out of order (different routes)
- Network speed varies wildly (congestion, routing changes)

Yet applications need **reliability**:
- Every byte must arrive
- Bytes must be in the correct order
- No duplicates, no corruption

TCP creates **reliability from unreliability**—an almost magical transformation.

#### The Three-Way Handshake: Establishing Truth

```
Client                                Server
  |                                      |
  |-------SYN (seq=100)----------------->|
  |  "I want to talk, my sequence is 100"
  |                                      |
  |<------SYN-ACK (seq=300, ack=101)-----|
  |  "OK, my sequence is 300, I got your 100"
  |                                      |
  |-------ACK (ack=301)----------------->|
  |  "Got it, let's begin"
  |                                      |
  |  <Connection established>            |
```

**Why Three Steps?**
- **Two steps aren't enough**: Server needs to know client received its SYN-ACK
- **Prevents ghost connections**: Old duplicate packets can't create false connections
- **Synchronizes sequence numbers**: Both sides agree on starting point
- **Allocates resources**: Both sides commit to the connection

**The Philosophy:**
The handshake embodies **mutual agreement**. Both parties must explicitly agree to communicate before resources are committed. This prevents:
- SYN flood attacks (partially mitigated)
- Resource exhaustion
- Ambiguous connection state

#### Guaranteed Delivery: The Acknowledgment Dance

**How It Works:**
```
Sender                               Receiver
  |                                     |
  |----Packet 1 (seq=100, data="Hello")-|
  |                                     |
  |<---ACK 105 ("Got bytes 100-104")---|
  |                                     |
  |----Packet 2 (seq=105, data="World")-|
  |                                     |
  |  (packet lost!)                     |
  |                                     |
  |  <timeout expires>                  |
  |                                     |
  |----Packet 2 (seq=105, RETRANSMIT)---|
  |                                     |
  |<---ACK 110 ("Got bytes 105-109")---|
```

**The Mechanisms:**

1. **Sequence Numbers**: Every byte has a number
   - Allows detection of gaps (missing data)
   - Enables reordering (out-of-order arrival)
   - Prevents duplicates (ignore old sequences)

2. **Acknowledgments (ACKs)**: Receiver confirms receipt
   - **Cumulative**: ACK 1000 means "got everything up to 999"
   - **Selective** (SACK): Can acknowledge non-contiguous ranges

3. **Retransmission**: If no ACK, resend
   - **Timeout-based**: Wait for ACK, resend if timeout
   - **Adaptive timeout**: Learn network RTT, adjust timeout
   - **Fast retransmit**: Three duplicate ACKs trigger immediate resend

#### Flow Control: Respecting the Receiver

**The Problem:**
Sender can produce data faster than receiver can consume it.

**The Solution: Sliding Window**
```
Receiver: "I have 10KB buffer available" (window size = 10KB)
Sender: "Got it, I'll send max 10KB unacknowledged data"
  ↓
Sender: Sends 8KB
Receiver: Processes 3KB, ACKs and says "window = 5KB now"
Sender: "OK, I can send 5KB more"
```

**Window Size = 0:**
- Receiver buffer is full
- Sender must stop sending
- Waits for window update
- **Prevents**: Buffer overflow, data loss

**The Elegance:**
Flow control is **receiver-driven**. The receiver controls the pace, ensuring it's never overwhelmed.

#### Congestion Control: Respecting the Network

**The Problem:**
Sending too fast causes network congestion:
- Routers drop packets
- Retransmissions increase load
- Network collapse (congestion collapse)

**The Solution: Adaptive Rate Control**

TCP dynamically adjusts sending rate based on network conditions.

**Algorithms:**

1. **Slow Start** (Exponential Growth):
   ```
   Start: Send 1 packet
   Got ACK: Send 2 packets
   Got ACKs: Send 4 packets
   ... (doubles each RTT until threshold)
   ```
   - **Fast growth** from slow start
   - **Goal**: Quickly find network capacity

2. **Congestion Avoidance** (Linear Growth):
   ```
   After threshold: Increase by 1 packet per RTT
   Got ACKs: Window += 1/window
   ```
   - **Careful growth** near capacity
   - **Goal**: Avoid triggering congestion

3. **Fast Recovery** (After Packet Loss):
   ```
   Packet loss detected
   → Reduce window by half (multiplicative decrease)
   → Continue sending (don't stop)
   → Slowly increase again (additive increase)
   ```
   - **AIMD**: Additive Increase, Multiplicative Decrease
   - **Fairness**: Converges to fair share among flows

**Modern Algorithms:**
- **TCP Reno**: Classic AIMD
- **TCP Cubic**: Optimized for high-bandwidth, high-latency networks
- **TCP BBR** (Bottleneck Bandwidth and RTT): Google's modern algorithm, models network

**The Philosophy:**
Congestion control is **network-respectful**. TCP backs off when it senses congestion, preventing collapse and ensuring fairness.

#### Ordered Delivery: Sequence Numbers Save the Day

**The Challenge:**
Packets take different routes, arrive out of order.

**The Solution:**
```
Received: Packet 3, Packet 1, Packet 5, Packet 2, Packet 4
TCP: Reorders to 1, 2, 3, 4, 5
Application: Sees data in correct order
```

Sequence numbers allow TCP to:
- **Reorder**: Hold out-of-order packets until gaps fill
- **Detect gaps**: Know when packets are missing
- **Remove duplicates**: Ignore packets we've already seen

#### Connection Termination: Graceful Goodbye

**Four-Way Handshake:**
```
Client                              Server
  |                                    |
  |-------FIN ("I'm done sending")---->|
  |                                    |
  |<------ACK ("OK, got it")----------|
  |                                    |
  |<------FIN ("I'm done too")---------|
  |                                    |
  |-------ACK ("Acknowledged")-------->|
  |                                    |
  <Both sides closed>                  
```

**Why Four Steps?**
- Connection is **bidirectional**
- Each side must close independently
- Allows half-close (one side done, other still sending)

**TIME_WAIT State:**
- Client waits 2×MSL (Maximum Segment Lifetime) before full close
- **Why**: Ensure final ACK arrives; handle delayed packets
- **Trade-off**: Sockets remain in use temporarily

#### TCP Header: Every Bit Matters

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |       |C|E|U|A|P|R|S|F|                               |
| Offset| Rsrvd |W|C|R|C|S|S|Y|I|            Window             |
|       |       |R|E|G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Key Fields:**
- **Sequence Number**: Byte stream position
- **ACK Number**: Next expected byte
- **Window**: Available buffer space
- **Flags**: SYN, ACK, FIN, RST, PSH
- **Checksum**: Data integrity

#### Performance Characteristics

**Latency Components:**
- **Connection Setup**: 1 RTT (Round Trip Time) for handshake
- **Data Transfer**: 1 RTT per window (with pipelining)
- **Connection Close**: 1 RTT for termination

**Throughput:**
```
Max Throughput = Window Size / RTT
```
- **Window Size**: Limited by receiver buffer and congestion window
- **RTT**: Round trip time
- **Implication**: High RTT = lower throughput (long distance problem)

**Bandwidth-Delay Product:**
```
BDP = Bandwidth × RTT
```
- **Optimal Window Size** = BDP
- **Example**: 100 Mbps, 100ms RTT → Need 1.25 MB window
- **Problem**: Default windows too small for high-speed, long-distance links
- **Solution**: TCP Window Scaling (negotiate larger windows)

#### When TCP Shines

**Perfect For:**
- **Web browsing**: Every byte matters, order critical
- **File transfers**: Integrity non-negotiable
- **Email**: Reliability required
- **Database connections**: Transactions need guarantees
- **API calls**: Correctness over speed
- **SSH/Remote access**: Every keystroke must arrive

**The Pattern:**
When **correctness** is more important than **speed**, TCP is your friend.

#### When TCP Struggles

**Problems:**

1. **Head-of-Line Blocking**:
   - One lost packet blocks entire stream
   - Application waits for retransmission
   - **Impact**: Poor for real-time (video, gaming)

2. **Overhead**:
   - Connection setup (1 RTT)
   - Headers (20-60 bytes per packet)
   - ACKs (additional packets)
   - **Impact**: Inefficient for small, one-off requests

3. **Latency Sensitivity**:
   - Retransmissions add delay
   - Congestion control slows down proactively
   - **Impact**: Poor for ultra-low latency needs

4. **Fairness Issues**:
   - Aggressive flows get more bandwidth
   - Short flows starved by long flows
   - **Impact**: Unfair resource allocation

#### TCP Variants and Evolution

**Classic Versions:**
- **TCP Tahoe** (1988): First congestion control
- **TCP Reno** (1990): Fast retransmit and recovery
- **TCP New Reno**: Better loss handling

**Modern Versions:**
- **TCP Cubic** (Linux default): Better for high-bandwidth networks
- **TCP BBR** (Google, 2016): Model-based congestion control, higher throughput
- **TCP Fast Open**: 0-RTT connection establishment

**Optimizations:**
- **Nagle's Algorithm**: Batch small writes (reduces overhead)
- **Delayed ACK**: Wait before ACKing (reduce ACK traffic)
- **TCP Window Scaling**: Support windows > 64KB
- **Selective Acknowledgment (SACK)**: Acknowledge non-contiguous blocks

#### The Trade-offs

| Aspect | TCP | UDP |
|--------|-----|-----|
| **Reliability** | Guaranteed | Best-effort |
| **Order** | Maintained | Not guaranteed |
| **Latency** | Higher (retransmissions) | Lower (no retries) |
| **Overhead** | 20-60 bytes + ACKs | 8 bytes |
| **Connection** | Required (3-way handshake) | Connectionless |
| **Use Case** | Correctness critical | Speed critical |

#### The Wisdom

**Why TCP Won the Internet:**
1. **Reliability**: Just works, hides network complexity
2. **Fairness**: Plays nice with other flows
3. **Adaptability**: Adjusts to any network
4. **Simplicity**: Applications don't worry about loss

**The Golden Rule:**
*"Use TCP unless you have a specific reason not to. The reason is usually: real-time, multicast, or you're implementing your own reliability."*

**Modern Reality:**
- **HTTP/1.1, HTTP/2**: Over TCP (reliability matters)
- **HTTP/3**: Over QUIC/UDP (reinvents TCP at application layer)
- **Databases**: Over TCP (data integrity critical)
- **APIs**: Over TCP (correctness over speed)

**The Paradox:**
TCP's reliability mechanisms (retransmissions, ordering) can cause **more latency** than the loss they're compensating for. This is why real-time applications avoid it.

**The Legacy:**
TCP is a testament to brilliant protocol design. It's survived 40+ years because it solves fundamental problems elegantly, adapts to changing networks, and hides complexity from applications. It's not perfect, but it's **remarkably good** at what it does.

### UDP Protocol (User Datagram Protocol)
Connectionless, fast protocol without guaranteed delivery.

**Characteristics:**
- **No handshake**: Immediate transmission
- **No guaranteed delivery**: Fire and forget
- **No ordering**: Packets may arrive out of order
- **Lower overhead**: Faster than TCP
- **No congestion control**

**Use Cases:**
- Video streaming
- Online gaming
- DNS queries
- VoIP (Voice over IP)
- IoT sensors

### HTTP / HTTPS (HyperText Transfer Protocol)
Application layer protocol for web communication.

**HTTP Methods:**
- **GET**: Retrieve data
- **POST**: Submit data
- **PUT**: Update/replace resource
- **PATCH**: Partial update
- **DELETE**: Remove resource
- **HEAD**: Get headers only
- **OPTIONS**: Get supported methods

**HTTP Status Codes:**

**1xx - Informational** (Request received, processing)
```
100 Continue          → "Keep sending request body"
101 Switching Protocols → "Upgrading to WebSocket"
```

**2xx - Success** (Request succeeded)
```
200 OK                → "Success, here's your data"
201 Created           → "Resource created successfully"
202 Accepted          → "Request accepted, processing async"
204 No Content        → "Success, but no data to return"
206 Partial Content   → "Here's part of the file (resume download)"
```

**3xx - Redirection** (Further action needed)
```
301 Moved Permanently → "Resource moved, update bookmarks"
302 Found            → "Temporary redirect, try this URL"
304 Not Modified     → "Use your cached version"
307 Temporary Redirect → "Temporary, keep using original URL"
308 Permanent Redirect → "Permanent, change all references"
```

**4xx - Client Errors** (Client messed up)
```
400 Bad Request      → "Your request is malformed"
401 Unauthorized     → "You need to authenticate"
403 Forbidden        → "Authenticated but not allowed"
404 Not Found        → "Resource doesn't exist"
405 Method Not Allowed → "Can't POST to this endpoint"
409 Conflict         → "Resource state conflict"
429 Too Many Requests → "Rate limit exceeded"
```

**5xx - Server Errors** (Server messed up)
```
500 Internal Server Error → "Something broke on our end"
502 Bad Gateway          → "Upstream server error"
503 Service Unavailable  → "Temporarily down/overloaded"
504 Gateway Timeout      → "Upstream server didn't respond"
```

**Real API Example:**
```http
# Success flow
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json

{"name": "John", "email": "john@example.com"}

↓ Response:
HTTP/1.1 201 Created
Location: /api/users/123
Content-Type: application/json

{"id": 123, "name": "John", "email": "john@example.com"}

# Error flow
POST /api/users HTTP/1.1
{"name": "John"}  ← Missing email

↓ Response:
HTTP/1.1 400 Bad Request

{"error": "email is required"}
```

#### HTTPS: Security Through Encryption

**HTTP vs HTTPS:**
```
HTTP (Insecure):
Client ←─────plaintext─────→ Server
       "password123"  ← Anyone can read!
       
HTTPS (Secure):
Client ←───encrypted───→ Server
       "8x$mK9#..."  ← Gibberish to eavesdroppers
```

**TLS Handshake (How HTTPS Works):**
```
1. Client Hello
   ┌────────┐                    ┌────────┐
   │ Client │ ──────────────────→ │ Server │
   └────────┘  "Let's use TLS 1.3"└────────┘
                "Supported ciphers: ..."

2. Server Hello + Certificate
   ┌────────┐                    ┌────────┐
   │ Client │ ←────────────────── │ Server │
   └────────┘  "Use TLS 1.3"      └────────┘
                "Here's my certificate"
                "Signed by: Let's Encrypt"

3. Client Verifies Certificate
   ┌────────┐
   │ Client │ Checks:
   └────────┘   ✓ Certificate signed by trusted CA?
                ✓ Domain matches?
                ✓ Not expired?
                ✓ Not revoked?

4. Key Exchange
   ┌────────┐                    ┌────────┐
   │ Client │ ←───────────────→  │ Server │
   └────────┘  Generate shared    └────────┘
                encryption key
                (using asymmetric crypto)

5. Encrypted Communication
   ┌────────┐                    ┌────────┐
   │ Client │ ←═════════════════→ │ Server │
   └────────┘  All data encrypted └────────┘
                with shared key
```

**What HTTPS Protects Against:**

```
✓ Eavesdropping
  Attacker: Can't read passwords, credit cards, messages

✓ Tampering
  Attacker: Can't modify requests/responses

✓ Impersonation
  Attacker: Can't pretend to be your bank

✗ Doesn't protect against
  - Server being hacked
  - Client having malware
  - DNS hijacking (before connection)
  - Trust in CA system being broken
```

**SSL Certificate Example:**
```
Certificate:
  Subject: CN=example.com
  Issuer: CN=Let's Encrypt
  Valid: 2026-01-01 to 2026-04-01 (90 days)
  Public Key: RSA 2048 bits
  Signature Algorithm: SHA256-RSA
  Subject Alternative Names:
    - example.com
    - www.example.com
    - *.example.com (wildcard)
```

**Check Certificate:**
```bash
# Using OpenSSL
openssl s_client -connect example.com:443 -servername example.com

# Using curl
curl -vI https://example.com

# Browser: Click padlock icon in address bar
```

#### HTTP/1.1 vs HTTP/2 vs HTTP/3

**HTTP/1.1 (1997-2015):**
```
Limitations:
┌──────────────────────────────────────┐
│ Request 1 → Response 1               │
│ Request 2 → Response 2 (waits!)      │
│ Request 3 → Response 3 (waits!)      │
└──────────────────────────────────────┘

Problems:
- Head-of-line blocking
- 1 request at a time per connection
- Workaround: Multiple connections (6-8)
- Large headers (repeated cookies, etc.)
```

**HTTP/2 (2015):**
```
Improvements:
┌──────────────────────────────────────┐
│      Single TCP Connection           │
├─────────┬─────────┬─────────┬────────┤
│Stream 1 │Stream 2 │Stream 3 │Stream 4│
│ Request │ Request │ Request │ Request│
│Response │Response │Response │Response│
└─────────┴─────────┴─────────┴────────┘

Features:
✓ Multiplexing: Multiple requests in parallel
✓ Header Compression: HPACK algorithm
✓ Server Push: Send resources before requested
✓ Binary Protocol: More efficient parsing

Example:
Browser requests index.html
  ↓
Server pushes:
  - style.css
  - script.js
  - logo.png
Before browser even asks!
```

**HTTP/3 (2020+):**
```
Built on QUIC (over UDP, not TCP):

HTTP/2 Problem:
┌──────────────────┐
│  TCP Layer       │ ← One packet lost = all streams blocked
└──────────────────┘

HTTP/3 Solution:
┌──────────────────┐
│  QUIC (UDP)      │ ← Each stream independent
└──────────────────┘

Benefits:
✓ Faster connection setup (0-RTT)
✓ Better loss recovery (no head-of-line blocking)
✓ Connection migration (survive IP changes)
✓ Built-in encryption (TLS 1.3 mandatory)

Mobile Example:
Phone switches from WiFi to 4G
  ↓
HTTP/2: Connection drops, restart handshake (slow)
HTTP/3: Connection continues seamlessly (fast)
```

**Performance Comparison:**
```
Loading website with 100 resources:

HTTP/1.1:
├─ Connection setup: 100ms
├─ Request 1-6: parallel (200ms)
├─ Request 7-12: wait... (200ms)
├─ Request 13-18: wait... (200ms)
└─ Total: ~1.5 seconds

HTTP/2:
├─ Connection setup: 100ms
├─ All 100 requests: parallel (200ms)
└─ Total: ~300ms (5x faster!)

HTTP/3:
├─ Connection setup: 0ms (0-RTT)
├─ All 100 requests: parallel (200ms)
└─ Total: ~200ms (7.5x faster!)
```

**Adoption Status:**
```
HTTP/1.1: 100% support (fallback)
HTTP/2:   ~95% support (widely deployed)
HTTP/3:   ~70% support (growing rapidly)

Major sites using HTTP/3:
- Google
- Facebook
- Cloudflare
- Netflix
```

#### HTTP: Advantages & Disadvantages

**Advantages:**
```
✓ Universal Support
  - Works on every platform
  - Every language has HTTP libraries
  - Browser native support

✓ Simple & Human-Readable
  - Text-based protocol
  - Easy to debug (curl, browser DevTools)
  - Self-documenting (headers explain themselves)

✓ Stateless
  - Each request independent
  - Easy to scale horizontally
  - Simple load balancing

✓ Firewall-Friendly
  - Ports 80/443 usually open
  - Works through corporate proxies
  - NAT traversal easier

✓ Rich Ecosystem
  - Countless tools and libraries
  - Well-understood debugging
  - Mature best practices

✓ Flexible
  - Works with any content type
  - Extensible via headers
  - Supports various auth methods
```

**Disadvantages:**
```
✗ Overhead
  - Text format larger than binary
  - Headers repeated on every request
  - Verbose for simple operations

✗ Stateless Complexity
  - Session management needed
  - Cookies/tokens for state
  - Authentication on every request

✗ Latency
  - HTTP/1.1: Head-of-line blocking
  - Multiple round trips for handshake
  - Not ideal for real-time

✗ Security Requires HTTPS
  - Plain HTTP is insecure
  - Certificate management overhead
  - TLS adds latency

✗ Not Bidirectional (HTTP/1.1)
  - Client must initiate
  - Server can't push (until HTTP/2)
  - Polling needed for updates

✗ Resource Intensive
  - Connection overhead
  - Keep-alive helps but not perfect
  - Server resources per connection
```

#### Alternatives to HTTP

**1. WebSockets**
```
Use When:
  ✓ Bidirectional communication needed
  ✓ Real-time updates (chat, gaming)
  ✓ Continuous data stream
  ✓ Low latency critical

Advantages over HTTP:
  + Full-duplex (both directions)
  + Single persistent connection
  + Lower overhead (no headers per message)
  + Server can push anytime

Disadvantages:
  - More complex to implement
  - Harder to load balance
  - Firewall issues possible
  - Connection state management

Example:
  Chat application: HTTP → WebSocket
  Before: Poll every 1s for new messages
  After: Server pushes messages instantly
```

**2. gRPC**
```
Use When:
  ✓ Microservices communication
  ✓ Performance critical
  ✓ Strongly typed contracts needed
  ✓ Streaming required

Advantages over HTTP/REST:
  + Binary protocol (smaller, faster)
  + HTTP/2 multiplexing built-in
  + Code generation (type safety)
  + Bidirectional streaming
  + Better performance (10x faster)

Disadvantages:
  - Not browser-native
  - Less human-readable
  - Steeper learning curve
  - Limited tooling vs REST
  - Requires HTTP/2

Comparison:
  REST API: 1000 requests/sec
  gRPC: 10,000+ requests/sec (same hardware)
```

**3. GraphQL**
```
Use When:
  ✓ Complex data requirements
  ✓ Multiple client types (web, mobile)
  ✓ Avoid over-fetching
  ✓ Flexible queries needed

Advantages over REST:
  + Single endpoint
  + Request exactly what you need
  + No over-fetching or under-fetching
  + Strong typing
  + Real-time via subscriptions

Disadvantages:
  - Caching harder
  - Complexity for simple cases
  - Can expose too much
  - Query cost unpredictable
  - Learning curve

Example:
  REST: 3 endpoints, 2 KB response (over-fetch)
  GraphQL: 1 endpoint, 0.5 KB (exact data)
```

**4. Server-Sent Events (SSE)**
```
Use When:
  ✓ One-way updates (server → client)
  ✓ Simpler than WebSocket
  ✓ Auto-reconnect needed
  ✓ Text-based updates

Advantages over HTTP polling:
  + Real-time push
  + Automatic reconnection
  + Built-in event IDs
  + Simpler than WebSocket

Advantages over WebSocket:
  + Simpler (just HTTP)
  + Better browser support
  + HTTP/2 compatible

Disadvantages vs WebSocket:
  - One-way only (server → client)
  - Text only (no binary)
  - Less efficient than WebSocket

Example:
  Stock ticker: SSE perfect (server pushes prices)
  Chat: WebSocket better (bidirectional)
```

**5. Message Queues (Kafka, RabbitMQ)**
```
Use When:
  ✓ Asynchronous processing
  ✓ Decoupling services
  ✓ High throughput needed
  ✓ Reliability critical

Advantages over HTTP:
  + Guaranteed delivery
  + Buffering (handle spikes)
  + Replay capability
  + Decoupling
  + Higher throughput

Disadvantages:
  - More complex infrastructure
  - Not for synchronous requests
  - Eventual consistency
  - Additional latency

Example:
  Order processing:
  HTTP: Synchronous, fails if service down
  Kafka: Async, queued until service recovers
```

**6. UDP-based Protocols (QUIC, WebRTC)**
```
Use When:
  ✓ Real-time media (video, voice)
  ✓ Gaming
  ✓ IoT with packet loss tolerance
  ✓ Ultra-low latency needed

Advantages over HTTP/TCP:
  + Lower latency (no retransmission delays)
  + Better for real-time
  + Connection migration (HTTP/3)
  + No head-of-line blocking

Disadvantages:
  - Less reliable (no guaranteed delivery)
  - Firewall issues
  - More complex implementation
  - Not suitable for most APIs

Example:
  Video call: UDP (some frame loss acceptable)
  File download: TCP (every byte matters)
```

#### Decision Matrix: Which Protocol?

| Need | Best Choice | Why |
|------|-------------|-----|
| **REST API** | HTTP/2 | Standard, widely supported |
| **Real-time chat** | WebSocket | Bidirectional, low latency |
| **Live notifications** | SSE | Simple, auto-reconnect |
| **Microservices** | gRPC | Performance, type safety |
| **Complex queries** | GraphQL | Flexible, avoid over-fetch |
| **Async processing** | Message Queue | Reliable, decoupled |
| **Video streaming** | WebRTC/QUIC | Low latency, packet loss OK |
| **File upload** | HTTP multipart | Simple, standard |
| **Bulk data transfer** | HTTP/2 or gRPC | Streaming, efficient |

#### When NOT to Use HTTP

```
✗ Real-time gaming
  → Use UDP/WebSocket (latency critical)

✗ Video/voice calls
  → Use WebRTC (packet loss tolerable)

✗ High-frequency trading
  → Use custom binary protocol (microseconds matter)

✗ IoT sensors (millions)
  → Use MQTT (lightweight, pub/sub)

✗ Inter-service calls (microservices)
  → Consider gRPC (faster, type-safe)

✗ Large file transfers (GB+)
  → Consider BitTorrent/custom (P2P, resumable)
```

#### HTTP Best Practices

**Do's:**
```
✓ Use HTTPS everywhere (even dev)
✓ Implement proper HTTP status codes
✓ Use HTTP/2 minimum (HTTP/3 when possible)
✓ Implement caching headers
✓ Compress responses (gzip, brotli)
✓ Use connection pooling
✓ Implement rate limiting
✓ Version your APIs (/v1/, /v2/)
✓ Use idempotent methods correctly
✓ Return proper error messages
```

**Don'ts:**
```
✗ Don't use GET for state changes
✗ Don't send sensitive data in URLs
✗ Don't ignore status codes (don't return 200 for errors)
✗ Don't create new connections per request
✗ Don't send uncompressed large payloads
✗ Don't use HTTP for real-time gaming
✗ Don't expose internal error details
✗ Don't use custom headers when standard ones exist
```

### WebSockets

#### The Real-Time Communication Channel

Full-duplex, persistent connection for real-time communication.

**Features:**
- Bidirectional communication
- Low latency
- Persistent connection
- Works over HTTP (upgrades connection)

**How WebSocket Works:**
```
1. Client initiates HTTP request
   GET /chat HTTP/1.1
   Host: example.com
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==

2. Server accepts upgrade
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

3. Connection upgraded to WebSocket
   ┌────────────────────────────────┐
   │   Client ←───────────→ Server   │
   │                                │
   │   Bidirectional messages       │
   │   Both can send anytime        │
   └────────────────────────────────┘

4. Messages flow freely
   Client → Server: {type: "message", text: "Hello"}
   Server → Client: {type: "ack", id: 123}
   Server → Client: {type: "notification", data: ...}
```

**Use Cases:**
- Chat applications
- Real-time notifications
- Live sports updates
- Collaborative editing
- Online gaming
- Stock trading platforms

#### Advantages of WebSockets

```
✓ Real-Time Bidirectional Communication
  - Both client and server can send anytime
  - No need to poll for updates
  - Instant message delivery

✓ Low Latency
  - No HTTP overhead per message
  - Just data frames
  - Typical latency: 10-50ms

✓ Lower Overhead
  - No headers per message (after handshake)
  - Smaller frame headers (2-14 bytes)
  - More efficient than HTTP polling

✓ Persistent Connection
  - Single connection for lifetime
  - No repeated handshakes
  - Less server resources

✓ Server Push
  - Server can initiate messages
  - No waiting for client poll
  - Event-driven architecture

✓ Better Mobile Performance
  - Persistent connection uses less battery
  - No repeated HTTP connections
  - Lower data usage
```

**Performance Comparison:**
```
HTTP Polling (every 1s):
  Request:  200 bytes
  Response: 100 bytes
  Per hour: 300 bytes × 3600 = 1.08 MB
  
  Latency: 0.5-2 seconds (poll interval + network)

WebSocket:
  Handshake: 500 bytes (once)
  Message:   50 bytes (just data)
  Per hour:  50 bytes × 3600 = 180 KB + 500 bytes
  
  Latency: 10-50ms (instant)
  
Data Savings: ~80-90%
Latency Improvement: ~100x faster
```

#### Disadvantages of WebSockets

```
✗ Complex Implementation
  - Harder than HTTP request/response
  - Need to handle connection state
  - Reconnection logic required
  - Message queuing needed

✗ Connection Management
  - Keep-alive pings needed
  - Detect disconnections
  - Handle reconnections gracefully
  - State synchronization

✗ Scaling Challenges
  - Stateful connections
  - Sticky sessions required
  - Load balancer must support WebSocket
  - Connection limits per server

✗ Firewall/Proxy Issues
  - Some corporate firewalls block
  - Some proxies don't handle upgrades
  - May need fallback to polling

✗ Resource Intensive
  - One connection per client (always)
  - 10,000 clients = 10,000 connections
  - Memory per connection
  - File descriptor limits

✗ No HTTP Caching
  - Can't leverage HTTP cache
  - No CDN support
  - All traffic to origin

✗ Browser Compatibility
  - Old browsers don't support
  - Need fallback mechanism
  - Polyfills add complexity

✗ Security Considerations
  - CSRF protection needed
  - Authentication per message
  - Rate limiting complex
  - DDoS risk (connection exhaustion)
```

#### Alternatives to WebSockets

**1. HTTP Long Polling**
```
How it works:
  Client: Request to server (waits...)
  Server: Holds request until data available
  Server: Responds with data
  Client: Immediately requests again

Advantages over WebSocket:
  + Works everywhere (no upgrade needed)
  + Simpler fallback
  + Better firewall compatibility

Disadvantages:
  - Higher latency
  - More server resources
  - Not true bidirectional
  - Connection churn

When to use:
  → Simple updates
  → Legacy browser support needed
  → Corporate firewall issues
```

**2. Server-Sent Events (SSE)**
```
How it works:
  Client: Opens connection
  Server: Pushes events continuously
  
Advantages over WebSocket:
  + Simpler (just HTTP)
  + Auto-reconnection built-in
  + Event IDs for replay
  + Better browser support

Disadvantages:
  - One-way only (server → client)
  - Text only (no binary)
  - HTTP/1.1 connection limit (6 per domain)

When to use:
  → Server needs to push to client
  → Client doesn't need to send much
  → Simpler alternative to WebSocket
  
Example:
  Stock prices, news feeds, notifications
```

**3. HTTP/2 Server Push**
```
How it works:
  Client: Requests index.html
  Server: Pushes style.css, script.js
  
Advantages:
  + No connection upgrade
  + Uses existing HTTP infrastructure
  + Multiplexed

Disadvantages:
  - Only for initial page load
  - Not for continuous updates
  - Limited browser support

When to use:
  → Optimize page load
  → Not for real-time updates
```

**4. WebRTC Data Channels**
```
How it works:
  Peer-to-peer connection
  No server in the middle (after setup)
  
Advantages over WebSocket:
  + Peer-to-peer (no server)
  + Lower latency
  + UDP-based (configurable reliability)
  + Built-in encryption

Disadvantages:
  - Complex setup (STUN/TURN)
  - Not for server communication
  - NAT traversal issues

When to use:
  → Peer-to-peer (gaming, file sharing)
  → Video/voice calls
  → Ultra-low latency needed
```

**5. Message Queues (for backend)**
```
For server-to-server:
  Kafka, RabbitMQ, Redis Pub/Sub
  
Advantages:
  + Guaranteed delivery
  + Persistence
  + Buffering
  + Scalability

When to use:
  → Backend services communication
  → Not for client connections
```

#### When to Use WebSockets vs Alternatives

| Use Case | Best Choice | Reason |
|----------|-------------|--------|
| **Chat application** | WebSocket | Bidirectional, instant |
| **Notifications only** | SSE | Simpler, server → client |
| **Stock ticker** | SSE or WS | Server pushes updates |
| **Collaborative editing** | WebSocket | Real-time sync both ways |
| **Live dashboard** | SSE | Server pushes metrics |
| **Online gaming** | WebSocket/WebRTC | Low latency critical |
| **Video call** | WebRTC | P2P, media optimized |
| **Admin updates** | Long Polling | Simple, infrequent |
| **Live sports scores** | SSE | One-way updates |
| **IoT device control** | WebSocket/MQTT | Bidirectional control |

#### WebSocket Implementation Examples

**Client (JavaScript):**
```javascript
// Create connection
const ws = new WebSocket('wss://example.com/chat');

// Connection opened
ws.onopen = (event) => {
  console.log('Connected');
  ws.send(JSON.stringify({type: 'auth', token: 'abc123'}));
};

// Receive messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

// Handle errors
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Connection closed
ws.onclose = (event) => {
  console.log('Disconnected');
  // Reconnect logic
  setTimeout(() => {
    // Recreate connection
  }, 5000);
};

// Send message
function sendMessage(text) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({type: 'message', text}));
  }
}
```

**Server (Node.js with ws library):**
```javascript
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

const clients = new Set();

wss.on('connection', (ws) => {
  console.log('Client connected');
  clients.add(ws);
  
  // Send welcome message
  ws.send(JSON.stringify({type: 'welcome', message: 'Connected!'}));
  
  // Receive messages
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    
    // Broadcast to all clients
    clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(message));
      }
    });
  });
  
  // Handle disconnect
  ws.on('close', () => {
    console.log('Client disconnected');
    clients.delete(ws);
  });
  
  // Keep-alive ping
  const interval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.ping();
    }
  }, 30000);
  
  ws.on('close', () => clearInterval(interval));
});
```

#### WebSocket Best Practices

**Do's:**
```
✓ Use wss:// (secure WebSocket)
✓ Implement reconnection logic
✓ Send heartbeat/ping messages
✓ Authenticate connections
✓ Validate all incoming messages
✓ Implement rate limiting
✓ Handle connection limits gracefully
✓ Use message queuing for offline clients
✓ Implement proper error handling
✓ Monitor connection health
```

**Don'ts:**
```
✗ Don't assume connection is always alive
✗ Don't send huge messages (use chunking)
✗ Don't trust client-side validation
✗ Don't keep connections open indefinitely without heartbeat
✗ Don't forget to clean up resources
✗ Don't use for file uploads (use HTTP)
✗ Don't send sensitive data without encryption
✗ Don't ignore backpressure
```

#### Scaling WebSocket Servers

**The Problem:**
```
10,000 concurrent connections
× 1 server
= 10,000 connections on one server (limit!)

With load balancer:
  Client A → LB → Server 1
  Client B → LB → Server 2
  
  Problem: Client A and B can't communicate!
  (Different servers)
```

**Solutions:**

**1. Sticky Sessions (Session Affinity)**
```
Load Balancer routes same user to same server

Pros: Simple
Cons: 
  - Uneven distribution
  - No failover
  - Server restart = all clients disconnect
```

**2. Message Broker (Redis Pub/Sub, Kafka)**
```
  Server 1 ──┐
             ├─→ Redis Pub/Sub ←─┐
  Server 2 ──┘                   └── Broadcast to all servers
  
How it works:
  1. Client A sends to Server 1
  2. Server 1 publishes to Redis
  3. All servers (1, 2, 3) subscribe
  4. All servers broadcast to their clients
  
Pros:
  + Scales horizontally
  + Failover support
  + Clients can be on any server
  
Cons:
  - Added latency (Redis hop)
  - More complex
  - Redis is SPOF (use cluster)
```

**3. Dedicated WebSocket Servers**
```
Architecture:
  
  API Servers (HTTP)     WebSocket Servers
  ┌────────────┐         ┌──────────────┐
  │  Server 1  │         │   WS Server  │
  │  Server 2  │  ←────→ │   + Redis    │
  │  Server 3  │         │   Pub/Sub    │
  └────────────┘         └──────────────┘
  
Pros:
  + Separate scaling
  + Optimize each tier
  + Easier to manage
```

#### WebSocket vs HTTP: The Decision

**Use WebSocket when:**
```
✓ Real-time updates needed (<100ms)
✓ Bidirectional communication
✓ Frequent messages (>1/second)
✓ Push notifications from server
✓ Collaborative features
✓ Live data feeds
```

**Use HTTP when:**
```
✓ Request/response pattern
✓ Infrequent updates (>10 seconds)
✓ One-time data fetch
✓ Need HTTP caching
✓ Simple CRUD operations
✓ Simpler to implement/maintain
```

**Use SSE when:**
```
✓ Only server → client updates
✓ Simpler than WebSocket
✓ Auto-reconnect important
✓ Text-based data
```

---

## 4. APIs & Communication Patterns

### API (Application Programming Interface)
Interface that allows different software systems to communicate.

**Types:**
- **REST**: Resource-based, uses HTTP
- **GraphQL**: Query language for APIs
- **gRPC**: High-performance RPC framework
- **SOAP**: XML-based protocol (legacy)

### REST API (Representational State Transfer)
Architectural style using HTTP for web services.

**Principles:**
- **Stateless**: Each request contains all needed information
- **Client-Server**: Separation of concerns
- **Cacheable**: Responses can be cached
- **Uniform Interface**: Consistent resource manipulation
- **Layered System**: Hierarchical architecture

**Best Practices:**
- Use nouns for resources (`/users`, `/products`)
- Use HTTP methods correctly
- Version your API (`/v1/users`)
- Return appropriate status codes
- Use pagination for large datasets
- Implement HATEOAS (links to related resources)

**Example:**
```
GET    /api/v1/users          # List users
GET    /api/v1/users/{id}     # Get user
POST   /api/v1/users          # Create user
PUT    /api/v1/users/{id}     # Update user
DELETE /api/v1/users/{id}     # Delete user
```

#### REST API: Advantages

```
✓ Simple & Intuitive
  - Easy to understand (resources + HTTP methods)
  - Self-documenting (URLs describe resources)
  - Low learning curve
  - Standard conventions

✓ Stateless
  - Each request independent
  - Easy to scale horizontally
  - Simple load balancing
  - No server-side session management

✓ Cacheable
  - HTTP caching built-in
  - CDN support
  - Browser caching
  - Reduces server load

✓ Wide Adoption
  - Every language has HTTP libraries
  - Countless tools (Postman, curl, Swagger)
  - Large developer community
  - Abundant documentation

✓ Flexible
  - Works with any data format (JSON, XML, etc.)
  - Platform agnostic
  - Can evolve independently
  - Versioning strategies available

✓ Separation of Concerns
  - Client and server independent
  - Multiple clients (web, mobile, IoT)
  - Backend changes don't break clients
```

**Performance:**
```
Typical REST API:
  Request: 500-2000 bytes (headers + JSON)
  Response: 1000-5000 bytes
  Latency: 50-200ms
  Throughput: 1000-5000 req/sec (single server)
```

#### REST API: Disadvantages

```
✗ Over-fetching
  - Get entire user object when you only need name
  - Wastes bandwidth
  - Slower for clients
  
  Example:
  GET /users/123 returns:
  {
    "id": 123,
    "name": "John",      ← Need this
    "email": "...",      ← Don't need
    "address": {...},    ← Don't need
    "preferences": {...} ← Don't need
  }

✗ Under-fetching (N+1 Problem)
  - Need multiple requests for related data
  - More round trips = higher latency
  
  Example:
  GET /posts/1         (get post)
  GET /users/123       (get author)
  GET /posts/1/comments (get comments)
  GET /users/456       (get commenter)
  Total: 4 requests = 4 × 50ms = 200ms

✗ Multiple Endpoints
  - Need to know many URLs
  - Documentation required
  - Version management complex
  
  GET /users
  GET /posts
  GET /comments
  GET /likes
  ... (100+ endpoints for large apps)

✗ Rigid Structure
  - Fixed responses per endpoint
  - Can't customize per client
  - Mobile needs less data than web
  - One size fits all

✗ Versioning Challenges
  - Breaking changes require new version
  - /v1/ vs /v2/ endpoint proliferation
  - Deprecation management
  - Multiple versions to maintain

✗ No Built-in Real-time
  - Need polling or webhooks
  - WebSockets separate concern
  - Not event-driven
```

#### Alternatives to REST

**1. GraphQL**
```
What it solves:
  ✓ Over-fetching → Request exact fields needed
  ✓ Under-fetching → Get related data in one request
  ✓ Multiple endpoints → Single endpoint
  ✓ Versioning → No versions, evolve schema

Example:
  query {
    user(id: 123) {
      name          ← Only these fields
      posts {
        title       ← Nested in one request
      }
    }
  }

Advantages over REST:
  + Single endpoint (/graphql)
  + Request exactly what you need
  + Strongly typed schema
  + No over/under-fetching
  + Self-documenting (introspection)
  + Real-time via subscriptions

Disadvantages:
  - More complex to implement
  - Caching harder (not URL-based)
  - Learning curve
  - Query complexity management needed
  - Can expose too much data
  - Performance unpredictable (query depth)

When to use:
  → Complex data requirements
  → Multiple client types (web, mobile, IoT)
  → Rapid frontend development
  → Need flexibility

When REST is better:
  → Simple CRUD
  → Need HTTP caching
  → Team unfamiliar with GraphQL
  → Simpler is better
```

**2. gRPC**
```
What it solves:
  ✓ Performance → Binary protocol (10x faster)
  ✓ Type safety → Protobuf contracts
  ✓ Streaming → Built-in bidirectional streaming
  ✓ Code generation → Auto-generate clients

Example Protobuf:
  service UserService {
    rpc GetUser(UserRequest) returns (User);
    rpc StreamUsers(Empty) returns (stream User);
  }
  
  message User {
    int32 id = 1;
    string name = 2;
  }

Advantages over REST:
  + Much faster (binary vs JSON)
  + Smaller payloads (protobuf)
  + Type safety (compile-time checks)
  + Streaming built-in
  + HTTP/2 multiplexing
  + Code generation

Disadvantages:
  - Not browser-native (needs gRPC-web)
  - Less human-readable
  - Steeper learning curve
  - Less tooling than REST
  - Binary debugging harder

Performance:
  REST: 1,000 req/sec
  gRPC: 10,000+ req/sec

When to use:
  → Microservices communication
  → Performance critical
  → Internal APIs
  → Streaming needed

When REST is better:
  → Public APIs
  → Need browser support
  → Team unfamiliar with protobuf
  → Human-readable debugging important
```

**3. SOAP**
```
Legacy protocol (don't use for new projects)

Advantages:
  + Strict standards (WS-* specs)
  + Built-in security (WS-Security)
  + ACID transactions
  + Formal contracts (WSDL)

Disadvantages:
  - Extremely verbose (XML)
  - Complex
  - Slower than REST
  - Dated

When you see it:
  → Enterprise legacy systems
  → Banking/financial systems
  → SOAP is being phased out

Migration path: SOAP → REST or GraphQL
```

**4. tRPC (TypeScript RPC)**
```
For TypeScript full-stack:

Advantages over REST:
  + End-to-end type safety
  + No code generation
  + Autocomplete in IDE
  + Automatic API client

Example:
  // Server
  const userRouter = router({
    getById: procedure
      .input(z.number())
      .query(({ input }) => db.user.find(input))
  });
  
  // Client (fully typed!)
  const user = await trpc.user.getById.query(123);

When to use:
  → TypeScript project (frontend + backend)
  → Want type safety without GraphQL complexity
  
Limitation:
  - TypeScript only
  - Not for public APIs
```

#### REST API Best Practices

**URL Design:**
```
Good:
  GET  /users              (list)
  GET  /users/123          (get one)
  POST /users              (create)
  PUT  /users/123          (update all)
  PATCH /users/123         (update partial)
  DELETE /users/123        (delete)
  
  GET  /users/123/posts    (nested resource)
  GET  /posts?userId=123   (filter via query param)

Bad:
  GET  /getUsers           ← Don't use verbs
  POST /users/delete/123   ← Use DELETE method
  GET  /user-list          ← Use plural nouns
  GET  /USERS              ← Use lowercase
```

**Status Codes:**
```
Use correctly:
  200 OK                   ← Success with body
  201 Created              ← Resource created
  204 No Content           ← Success, no body
  
  400 Bad Request          ← Client error (validation)
  401 Unauthorized         ← Not authenticated
  403 Forbidden            ← Authenticated but not allowed
  404 Not Found            ← Resource doesn't exist
  409 Conflict             ← Duplicate, constraint violation
  422 Unprocessable        ← Semantic errors
  429 Too Many Requests    ← Rate limited
  
  500 Internal Error       ← Server error
  502 Bad Gateway          ← Upstream error
  503 Service Unavailable  ← Temporarily down
```

**Response Format:**
```
Consistent structure:
  {
    "data": {...},
    "meta": {
      "timestamp": "2026-01-25T10:30:00Z",
      "requestId": "abc123"
    }
  }

Error response:
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Invalid email format",
      "field": "email",
      "details": [...]
    }
  }

Pagination:
  {
    "data": [...],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 100,
      "totalPages": 5
    },
    "links": {
      "next": "/users?page=2",
      "prev": null
    }
  }
```

**Versioning:**
```
Option 1: URL versioning (most common)
  /api/v1/users
  /api/v2/users
  
  Pros: Clear, easy to route
  Cons: URL proliferation

Option 2: Header versioning
  GET /api/users
  Accept: application/vnd.api.v1+json
  
  Pros: Clean URLs
  Cons: Less visible

Option 3: Query parameter
  /api/users?version=1
  
  Pros: Flexible
  Cons: Pollutes query params

Recommendation: URL versioning (/v1/, /v2/)
```

**Security:**
```
✓ Use HTTPS always
✓ Authenticate with JWT/OAuth
✓ Validate all input
✓ Rate limit requests
✓ Use API keys for clients
✓ Implement CORS properly
✓ Don't expose stack traces
✓ Log security events
✓ Use OWASP guidelines
```

**Performance:**
```
✓ Implement caching headers
✓ Use gzip/brotli compression
✓ Paginate large collections
✓ Use field filtering (?fields=name,email)
✓ Implement ETags for conditional requests
✓ Use connection pooling
✓ Monitor slow endpoints
✓ Implement request timeout
```

#### When to Use REST vs Alternatives

| Scenario | Use This | Why |
|----------|----------|-----|
| **Public API** | REST | Standard, widely understood |
| **Internal microservices** | gRPC | Performance, type safety |
| **Mobile app with complex UI** | GraphQL | Avoid over/under-fetching |
| **Simple CRUD** | REST | Simplest, good enough |
| **Real-time updates** | GraphQL Subscriptions or WebSocket | Event-driven |
| **TypeScript full-stack** | tRPC | Type safety |
| **Legacy enterprise** | SOAP | Required by old systems |
| **High performance** | gRPC | 10x faster than REST |
| **Multiple client types** | GraphQL | Flexible queries |
| **File uploads** | REST (multipart) | Standard, simple |

### GraphQL
Query language that allows clients to request exactly what they need.

**Advantages:**
- Single endpoint
- No over-fetching or under-fetching
- Strongly typed schema
- Real-time updates (subscriptions)
- Better for mobile (reduces bandwidth)

**Disadvantages:**
- Complexity for simple use cases
- Caching is harder
- File upload handling
- Learning curve

**When to Use:**
- Complex data requirements
- Multiple client types (web, mobile, IoT)
- Need for flexible queries
- Frequent schema changes

### gRPC (Google Remote Procedure Call)
High-performance RPC framework using Protocol Buffers.

**Features:**
- Binary protocol (faster than JSON)
- HTTP/2 based (multiplexing, streaming)
- Strongly typed contracts
- Code generation for multiple languages
- Four types: Unary, Server streaming, Client streaming, Bidirectional

**Use Cases:**
- Microservices communication
- Real-time streaming
- High-performance APIs
- Polyglot environments

**REST vs gRPC:**
- REST: Human-readable, wider adoption, browser-friendly
- gRPC: Faster, smaller payloads, better for service-to-service

### Message Queue
Asynchronous communication pattern for decoupling services.

**Key Concepts:**
- **Producer**: Sends messages
- **Consumer**: Processes messages
- **Queue**: Stores messages
- **Topics**: Categorize messages
- **Dead Letter Queue**: Failed messages

**Popular Systems:**
- **Kafka**: High-throughput, distributed, log-based
- **RabbitMQ**: Feature-rich, supports multiple protocols
- **AWS SQS**: Managed, scalable
- **Redis Pub/Sub**: In-memory, fast

**Benefits:**
- Decoupling services
- Load leveling
- Fault tolerance
- Asynchronous processing
- Scalability

**Use Cases:**
- Order processing
- Email notifications
- Video transcoding
- Log aggregation
- Event-driven architectures

### Web Hooks
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

---

## 5. Networking & Infrastructure

### Forward Proxy
Server that sits between clients and the internet.

**Functions:**
- Anonymizes client IP
- Content filtering
- Caching
- Access control

**Use Cases:**
- Corporate networks
- VPN services
- Bypassing geo-restrictions

### Reverse Proxy
Server that sits between clients and backend servers.

**Functions:**
- Load balancing
- SSL termination
- Caching
- Request routing
- Security (hides backend)

**Popular Tools:**
- Nginx
- HAProxy
- Apache
- Envoy

### Load Balancer

#### The Traffic Conductor of Modern Infrastructure

A load balancer is far more than a "traffic splitter"—it's the **central nervous system** of scalable architectures. It's the component that transforms a cluster of fragile, individual servers into a single, resilient, high-performance system. Without load balancers, horizontal scaling would be practically impossible.

#### The Deep Theory: Why Load Balancing Exists

**The Fundamental Problem:**
A single server has finite capacity:
- **CPU**: Can process only so many requests/second
- **Memory**: Can hold only so much data
- **Network**: Can handle only so much bandwidth
- **Reliability**: Single point of failure

**The Solution: Distribute the Load**
```
                     ┌─────────────┐
                     │             │
Clients ──────────► │Load Balancer│ ◄──── Single entry point
(thousands)         │             │
                     └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐        ┌────────┐        ┌────────┐
    │Server 1│        │Server 2│        │Server 3│
    └────────┘        └────────┘        └────────┘
```

**The Magic:**
Clients see **one system**, but you have **many servers**. This abstraction enables:
- **Scalability**: Add servers without changing client code
- **Reliability**: One server fails, others continue
- **Performance**: Distribute load for better response times
- **Flexibility**: Deploy/update servers independently

#### The Algorithms: Different Strategies for Different Needs

Each algorithm embodies a different **philosophy** about fairness and optimization.

##### 1. Round Robin (The Democrat)

```
Request 1 → Server A
Request 2 → Server B  
Request 3 → Server C
Request 4 → Server A  (repeat)
```

**Philosophy**: Everyone gets equal turns.

**Pros:**
- Simple, fair, predictable
- Even distribution over time
- No state needed (stateless)
- Works well when servers are equal

**Cons:**
- Ignores server load (busy servers get same share)
- Ignores request complexity (all requests treated equal)
- Poor if servers have different capacity

**When to Use:**
- Homogeneous servers (same hardware)
- Similar request complexity
- Stateless applications
- Simple deployments

**Real-World:**
Default choice for most web applications. Simple, works surprisingly well.

##### 2. Weighted Round Robin (The Meritocrat)

```
Server A: Weight 3 (powerful)
Server B: Weight 2 (medium)
Server C: Weight 1 (weak)

Sequence: A, A, A, B, B, C, repeat
```

**Philosophy**: Distribute according to capacity.

**When to Use:**
- Heterogeneous servers (different hardware)
- Phased rollouts (send 10% to new version)
- Testing (canary deployments)

**Configuration Example:**
```yaml
servers:
  - server1: weight=5  # 50% of traffic
  - server2: weight=3  # 30% of traffic  
  - server3: weight=2  # 20% of traffic
```

##### 3. Least Connections (The Optimizer)

```
Server A: 5 active connections
Server B: 3 active connections  ← Route here
Server C: 7 active connections
```

**Philosophy**: Route to least busy server right now.

**How It Works:**
1. Track active connections per server
2. Route new request to server with fewest connections
3. Update count on connection open/close

**Pros:**
- Better for long-lived connections
- Adapts to actual load
- Handles varying request times well

**Cons:**
- Requires state (connection counts)
- More complex than round robin
- Overhead of tracking

**When to Use:**
- Long-lived connections (WebSockets, streaming)
- Variable request processing time
- Real-time applications

**Example: WebSocket Chat**
Some users chat more (long connections), some less. Least connections ensures even distribution of active users.

##### 4. Least Response Time (The Perfectionist)

```
Server A: 50ms avg response time  ← Route here (fastest)
Server B: 150ms avg response time
Server C: 200ms avg response time
```

**Philosophy**: Route to the fastest server.

**How It Works:**
1. Continuously measure response times
2. Calculate moving average per server
3. Route to server with lowest latency

**Pros:**
- Optimal user experience
- Adapts to server performance
- Handles degraded servers

**Cons:**
- Complex implementation
- Requires active monitoring
- Can create feedback loops (fast gets more load)

**When to Use:**
- Performance-critical applications
- User-facing services where latency matters
- When you have monitoring infrastructure

##### 5. IP Hash (The Consistent Router)

```
Client IP: 192.168.1.100
Hash: hash(192.168.1.100) % 3 = 1
Result: Always route to Server B
```

**Philosophy**: Same client, same server.

**How It Works:**
```python
server_index = hash(client_ip) % num_servers
```

**Pros:**
- **Session affinity**: Client always hits same server
- No need for shared session storage
- Cache locality (server caches client-specific data)

**Cons:**
- **Uneven distribution**: Hash may not distribute evenly
- **Server changes break routing**: Adding/removing servers changes hash
- **No failover**: If server down, client sessions lost

**When to Use:**
- Stateful applications (legacy apps with local sessions)
- Caching benefits from affinity
- Can't use sticky sessions (cookies)

**Modern Alternative: Consistent Hashing**
- Adding/removing servers affects minimal clients
- Better distribution
- Used by Cassandra, DynamoDB, Redis Cluster

##### 6. Random (The Gambler)

```
Request 1 → Random: Server C
Request 2 → Random: Server A
Request 3 → Random: Server A
Request 4 → Random: Server B
```

**Philosophy**: Trust in probability.

**Pros:**
- Extremely simple (one line of code)
- No state needed
- Surprisingly effective
- Avoids pathological cases

**Cons:**
- Short-term imbalance possible
- Less predictable

**When to Use:**
- Stateless applications
- Simple setups
- Microservices (service mesh)

**Surprising Truth:**
Random works better than you'd think. Over time, distribution evens out.

##### 7. Least Bandwidth (The Bandwidth Manager)

**Philosophy**: Route to server using least bandwidth.

**When to Use:**
- Media streaming
- File downloads
- Bandwidth-intensive applications

#### Layer 4 vs Layer 7: The Fundamental Choice

This choice defines **what the load balancer can see** and **how it makes decisions**.

##### Layer 4 (Transport Layer) Load Balancing

**What It Sees:**
- IP addresses (source, destination)
- Ports (source, destination)
- TCP/UDP protocol

**What It Can't See:**
- HTTP headers
- URLs
- Cookies
- Application data

**How It Works:**
```
1. Client connects to LB
2. LB chooses server based on IP/Port
3. LB forwards TCP packets to server
4. Server responds, LB forwards back
```

**Modes:**
- **NAT Mode**: LB rewrites IPs
- **Direct Server Return (DSR)**: Server responds directly to client
- **Tunnel Mode**: LB encapsulates packets

**Pros:**
- **Fast**: Minimal processing (just forward packets)
- **Protocol agnostic**: Works with any TCP/UDP application
- **Low latency**: Nanoseconds of overhead
- **High throughput**: Millions of connections/sec
- **Low resource usage**: Minimal CPU/memory

**Cons:**
- **Limited routing**: Can't route by URL, headers
- **No content-based decisions**: Treat all traffic equally
- **Basic health checks**: Just TCP connectivity

**When to Use:**
- Ultra-high performance required
- Non-HTTP protocols (databases, SSH, SMTP)
- Simple routing sufficient
- Minimizing latency critical

**Examples:**
- AWS Network Load Balancer (NLB)
- HAProxy (L4 mode)
- LVS (Linux Virtual Server)

##### Layer 7 (Application Layer) Load Balancing

**What It Sees:**
- Everything Layer 4 sees, PLUS:
- HTTP methods (GET, POST)
- URLs and paths
- Headers (cookies, user-agent)
- Request body (can inspect)
- SSL/TLS content (after termination)

**How It Works:**
```
1. Client connects to LB
2. LB terminates TCP connection
3. LB reads HTTP request completely
4. LB makes routing decision based on content
5. LB opens new connection to server
6. LB proxies request/response
```

**Routing Examples:**
```nginx
# Route by path
/api/*       → API servers
/images/*    → Image servers
/static/*    → CDN

# Route by header
User-Agent: Mobile  → Mobile backend
User-Agent: Desktop → Desktop backend

# Route by cookie
Session: premium  → Premium tier servers
Session: free     → Standard servers

# Route by query param
?version=2  → New version servers
?version=1  → Old version servers
```

**Advanced Features:**
- **SSL Termination**: LB handles HTTPS, talks HTTP to servers
- **Content Modification**: Rewrite headers, inject content
- **Compression**: Gzip responses
- **Caching**: Serve cached responses
- **WAF**: Block malicious requests
- **Rate Limiting**: Throttle clients
- **Authentication**: Validate JWT, OAuth

**Pros:**
- **Intelligent routing**: Content-aware decisions
- **Better health checks**: HTTP status, response content
- **Security**: WAF, DDoS protection, SSL
- **Observability**: Full request logging
- **Flexibility**: Transform requests/responses

**Cons:**
- **Slower**: Must parse HTTP (microseconds vs nanoseconds)
- **Higher resource usage**: CPU for parsing, memory for buffering
- **Lower throughput**: Thousands of connections/sec (vs millions)
- **HTTP only**: Won't work for other protocols
- **Complexity**: More to configure and maintain

**When to Use:**
- HTTP/HTTPS applications (most web apps)
- Need content-based routing
- Want SSL termination
- Security features required
- Microservices with path-based routing

**Examples:**
- AWS Application Load Balancer (ALB)
- Nginx
- HAProxy (L7 mode)
- Envoy
- Traefik

##### The Decision Matrix

| Need | Layer 4 | Layer 7 |
|------|---------|----------|
| **Maximum Performance** | ✓ | |
| **Non-HTTP Protocols** | ✓ | |
| **Path-based Routing** | | ✓ |
| **SSL Termination** | | ✓ |
| **Content Inspection** | | ✓ |
| **WAF/Security** | | ✓ |
| **Simple Setup** | ✓ | |
| **Microservices** | | ✓ |

**Hybrid Approach (Common):**
```
Internet
  ↓
Layer 4 LB (high performance, DDoS protection)
  ↓
Layer 7 LB (intelligent routing, SSL termination)
  ↓
Application Servers
```

#### Health Checks: Detecting Failure

A load balancer must know which servers are healthy. Dead servers get no traffic.

##### Active Health Checks (Proactive)

**How It Works:**
```
Every 5 seconds:
  For each server:
    Send HTTP GET /health
    If response 200 OK: Server healthy
    If timeout or 5xx: Mark unhealthy
    After 3 consecutive failures: Remove from pool
    After 2 consecutive successes: Add back to pool
```

**Types:**
- **TCP check**: Can establish connection?
- **HTTP check**: Returns 200 OK?
- **HTTPS check**: TLS + HTTP success?
- **Custom check**: Application-specific endpoint

**Configuration Example:**
```yaml
health_check:
  path: /health
  interval: 5s
  timeout: 2s
  healthy_threshold: 2
  unhealthy_threshold: 3
```

**Health Check Endpoint Best Practices:**
```python
# Good health check
GET /health
Response:
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected",
  "timestamp": "2026-01-25T10:30:00Z"
}
```

**What to Check:**
- ✓ Process is running
- ✓ Database connection alive
- ✓ Critical dependencies available
- ✗ Disk space (might remove all servers)
- ✗ Slow checks (should be fast <100ms)

##### Passive Health Checks (Reactive)

**How It Works:**
```
Monitor real traffic:
  If 5xx error → Increment failure count
  If success → Decrement failure count
  If failures > threshold → Mark unhealthy
```

**Pros:**
- No extra traffic
- Detects real-world issues
- Faster detection (using actual requests)

**Cons:**
- Requires real traffic
- Some requests fail before detection

**Modern Approach: Both**
- Active checks: Baseline health
- Passive checks: Faster reaction to real issues

#### Load Balancer Deployment Patterns

##### Pattern 1: Single Load Balancer
```
Clients → Load Balancer → Servers
```
- **Problem**: Load balancer is SPOF
- **Use**: Development, small deployments

##### Pattern 2: Active-Passive (HA Pair)
```
Clients → VIP (Virtual IP)
         ↙        ↘
LB 1 (Active)    LB 2 (Standby)
         ↘        ↙
          Servers
```
- **Heartbeat**: LBs monitor each other
- **Failover**: Standby takes VIP if active fails
- **Eliminates SPOF**, wastes standby resources

##### Pattern 3: Active-Active (Equal Cost Multi-Path)
```
       DNS Round Robin
      ↙              ↘
LB 1 (50%)          LB 2 (50%)
      ↘              ↙
          Servers
```
- **Both serving**: No wasted resources
- **Failover**: DNS removes failed LB
- **Problem**: DNS caching delays failover

##### Pattern 4: Cloud Native (Managed Service)
```
Clients → AWS ALB/NLB (managed, auto-scaled)
              ↓
          Servers
```
- **HA built-in**: Multiple availability zones
- **Auto-scaling**: Handles any load
- **Managed**: No server maintenance
- **Cost**: Pay for service

#### Advanced Scenarios

##### Global Load Balancing (GSLB)

Route users to nearest datacenter:
```
User in US → US Load Balancer → US Servers
User in EU → EU Load Balancer → EU Servers
User in Asia → Asia Load Balancer → Asia Servers
```

**How:**
- **DNS-based**: Return different IPs by location (AWS Route 53, Cloudflare)
- **Anycast**: Same IP, routed to nearest datacenter

**Benefits:**
- Lower latency (geographic proximity)
- Higher availability (datacenter failover)
- Compliance (data residency)

##### Session Persistence (Sticky Sessions)

Ensure user hits same server:
```
Request 1 → Server A (set cookie: server=A)
Request 2 (cookie: server=A) → Server A (same)
Request 3 (cookie: server=A) → Server A (same)
```

**Methods:**
- **Cookie-based**: LB inserts cookie
- **IP-based**: Hash client IP
- **Application session**: App sets cookie, LB reads

**When Needed:**
- Legacy apps with local sessions
- WebSocket connections
- Upload progress tracking

**Modern Alternative:**
- Store sessions in Redis/Memcached
- Any server can handle any request
- **Better**: Scales horizontally, survives server failure

##### Zero-Downtime Deployments

**Blue-Green Deployment:**
```
1. Blue (old version) serving 100%
2. Deploy Green (new version)
3. Test Green
4. Switch LB: 100% → Green
5. Keep Blue for rollback
```

**Rolling Deployment:**
```
1. Server 1: v1 → v2 (remove from LB, update, add back)
2. Server 2: v1 → v2 (repeat)
3. Server 3: v1 → v2 (repeat)
```

**Canary Deployment:**
```
1. 95% → old version
2. 5% → new version (canary)
3. Monitor metrics
4. If good: 50% → new
5. If good: 100% → new
```

#### The Critical Trade-offs

**Performance vs Features:**
- L4: Fast, simple
- L7: Slower, powerful

**Simplicity vs Intelligence:**
- Round robin: Simple, good enough
- Least response time: Complex, optimal

**Consistency vs Availability:**
- Session affinity: Consistent (same server)
- Any server: Available (survives failures)

**Cost vs Reliability:**
- Single LB: Cheap, SPOF
- HA LBs: Expensive, reliable

#### The Wisdom

**Start Simple:**
1. Single load balancer (AWS ALB/NLB)
2. Round robin algorithm
3. Active health checks
4. Stateless application (no sticky sessions)

**Add Complexity When:**
- Traffic exceeds single LB capacity → Multiple LBs
- Different server capacities → Weighted round robin
- Long connections → Least connections
- Need content routing → Layer 7
- Global users → GSLB

**The Golden Rule:**
*"Your load balancer should be the most reliable component in your system. If it fails, everything fails. Invest in HA load balancers before optimizing algorithms."*

**Modern Best Practice:**
- Use managed load balancers (AWS ALB, GCP Load Balancer)
- Layer 7 for HTTP (intelligent routing worth the cost)
- Round robin or least connections (simple, effective)
- Active health checks (fast detection)
- No sticky sessions (use external state store)
- Multiple availability zones (HA built-in)

**The Reality:**
Most applications are perfectly served by: **Layer 7 ALB + Round Robin + Health Checks**. The fancy algorithms matter only at scale or with specific workload characteristics.

### API Gateway
Single entry point for all client requests to microservices.

**Functions:**
- Request routing
- Authentication & authorization
- Rate limiting
- Request/response transformation
- Protocol translation
- Aggregation (combining multiple service calls)
- Caching
- Logging & monitoring

**Popular Solutions:**
- Kong
- AWS API Gateway
- Azure API Management
- Apigee

### CDN (Content Delivery Network)
Distributed network of servers that deliver content based on user location.

**How it Works:**
1. User requests content
2. DNS routes to nearest edge server
3. Edge server returns cached content or fetches from origin
4. Content cached for future requests

**Benefits:**
- Reduced latency
- Lower bandwidth costs
- Improved availability
- DDoS protection
- Offload origin servers

**Use Cases:**
- Static assets (images, CSS, JS)
- Video streaming
- Software downloads
- Gaming assets

**Popular CDNs:**
- Cloudflare
- Akamai
- AWS CloudFront
- Fastly

### Service Discovery
Mechanism for services to find and communicate with each other.

**Patterns:**
- **Client-side**: Client queries registry (Eureka, Consul)
- **Server-side**: Load balancer queries registry (Kubernetes)

**Components:**
- **Service Registry**: Database of service instances
- **Health Checking**: Monitor service availability
- **Load Balancing**: Distribute requests

**Tools:**
- Consul
- Eureka (Netflix)
- Zookeeper
- etcd
- Kubernetes DNS

### Service Mesh
Infrastructure layer for managing service-to-service communication.

**Features:**
- Traffic management
- Load balancing
- Service discovery
- Fault injection
- Circuit breaking
- Observability
- Security (mTLS)

**Popular Solutions:**
- Istio
- Linkerd
- Consul Connect

---

## 6. Data Storage

### Database Fundamentals
Organized collection of structured data.

**ACID Properties:**
- **Atomicity**: All or nothing transactions
- **Consistency**: Data integrity maintained
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data persists

**BASE (NoSQL alternative):**
- **Basically Available**: System available most of the time
- **Soft state**: State may change over time
- **Eventual consistency**: System becomes consistent eventually

### SQL (Relational Databases)
Structured data with predefined schema.

**Characteristics:**
- Tables with rows and columns
- ACID compliance
- Relationships (foreign keys)
- SQL query language
- Strong consistency

**Popular Databases:**
- PostgreSQL
- MySQL
- Oracle
- SQL Server
- SQLite

**When to Use:**
- Complex queries and joins
- Transactions required
- Data integrity critical
- Structured data

#### SQL Databases: Advantages

```
✓ ACID Guarantees
  - Atomicity: All or nothing transactions
  - Consistency: Data integrity maintained
  - Isolation: Concurrent transactions don't interfere
  - Durability: Committed data persists
  
  Example:
  BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
  COMMIT;  ← Both succeed or both fail

✓ Data Integrity
  - Foreign keys enforce relationships
  - Constraints prevent invalid data
  - Triggers for business logic
  - Validation at database level
  
  CREATE TABLE orders (
    user_id INT REFERENCES users(id),  ← Must be valid user
    amount DECIMAL CHECK (amount > 0)  ← Must be positive
  );

✓ Complex Queries
  - JOIN multiple tables
  - Aggregate functions (SUM, AVG, COUNT)
  - Window functions
  - Subqueries
  - CTE (Common Table Expressions)
  
  SELECT u.name, COUNT(o.id) as order_count
  FROM users u
  LEFT JOIN orders o ON u.id = o.user_id
  WHERE u.created_at > '2025-01-01'
  GROUP BY u.name
  HAVING COUNT(o.id) > 5;

✓ Mature Ecosystem
  - 40+ years of development
  - Battle-tested
  - Rich tooling (ORMs, GUI tools, monitoring)
  - Large talent pool
  - Abundant documentation

✓ Standardization
  - SQL is standard (with variations)
  - Portable knowledge
  - Similar syntax across databases
  - Industry best practices

✓ Strong Consistency
  - Always see latest data
  - No eventual consistency issues
  - Predictable behavior
  
✓ Schema Enforcement
  - Data structure defined upfront
  - Type safety
  - Documentation built-in
  - Prevents data corruption
```

#### SQL Databases: Disadvantages

```
✗ Scaling Challenges
  - Vertical scaling (bigger machine)
  - Horizontal scaling complex
  - Sharding difficult
  - Distributed joins expensive
  
  Vertical scaling limits:
  - Max: ~96 cores, 2TB RAM
  - Cost: Exponential ($$$$$)
  - Still single point of failure

✗ Schema Rigidity
  - Must define schema upfront
  - Changes require migrations
  - ALTER TABLE can lock table
  - Backwards compatibility needed
  
  Example problem:
  ALTER TABLE users ADD COLUMN preferences JSON;
  → Locks table for minutes on large dataset
  → Downtime or careful planning needed

✗ Performance Issues at Scale
  - Joins slow with large tables
  - Indexes trade-off (faster reads, slower writes)
  - Full table scans costly
  - Locking contention
  
  SELECT * FROM orders o
  JOIN users u ON o.user_id = u.id
  JOIN products p ON o.product_id = p.id;
  
  With millions of rows: seconds or minutes

✗ Limited Horizontal Scaling
  - Read replicas: Yes (easy)
  - Write scaling: No (single primary)
  - Sharding: Possible but complex
  - Cross-shard joins: Expensive

✗ Not Ideal for Unstructured Data
  - JSON/BLOB support limited
  - Hierarchical data awkward
  - Graph relationships inefficient
  
✗ High Operational Overhead
  - Backup/restore complex
  - Index maintenance
  - Query optimization needed
  - Monitoring required
```

#### SQL vs NoSQL: The Complete Comparison

| Aspect | SQL | NoSQL |
|--------|-----|-------|
| **Data Model** | Tables, rows, columns | Documents, key-value, graphs, columns |
| **Schema** | Fixed, predefined | Flexible, dynamic |
| **Scaling** | Vertical (scale up) | Horizontal (scale out) |
| **Transactions** | Full ACID | Limited (varies by DB) |
| **Consistency** | Strong | Eventual (usually) |
| **Joins** | Native, efficient | Limited or application-level |
| **Query Language** | SQL (standard) | Varies (no standard) |
| **Use Case** | Complex queries, transactions | High throughput, flexible schema |
| **Examples** | PostgreSQL, MySQL | MongoDB, Cassandra, Redis |
| **Cost at Scale** | High (bigger machines) | Lower (commodity hardware) |
| **Complexity** | Lower (mature tools) | Higher (newer, distributed) |

#### When to Choose SQL

```
✓ Financial Applications
  - Banking, payments
  - Transactions critical
  - ACID required
  - Data integrity paramount

✓ ERP / CRM Systems
  - Complex relationships
  - Multi-table joins
  - Structured workflows
  - Reporting requirements

✓ E-commerce
  - Inventory management
  - Order processing
  - Consistent pricing
  - Cannot oversell

✓ Traditional Business Apps
  - HR systems
  - Accounting software
  - Booking systems
  - Reservation systems

✓ Analytics / Reporting
  - Complex aggregations
  - Historical data analysis
  - Business intelligence
  - Data warehousing
```

#### Alternatives to Traditional SQL

**1. NewSQL (Distributed SQL)**
```
Databases: CockroachDB, Google Spanner, YugabyteDB

What it solves:
  ✓ SQL interface (familiar)
  ✓ ACID transactions (like SQL)
  ✓ Horizontal scaling (like NoSQL)
  
  "Best of both worlds"

Advantages over traditional SQL:
  + Scales horizontally
  + Multi-region support
  + High availability built-in
  + Still ACID compliant
  + SQL compatible

Disadvantages:
  - Higher latency (distributed consensus)
  - More complex operations
  - Less mature
  - Expensive (often)

When to use:
  → Need SQL + horizontal scaling
  → Global distribution required
  → Can afford latency trade-off

Example: CockroachDB
  CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT
  );
  
  → Automatically distributed across regions
  → ACID transactions across globe
```

**2. Time-Series Databases**
```
Databases: InfluxDB, TimescaleDB, Prometheus

What it solves:
  ✓ Optimized for time-series data
  ✓ High write throughput
  ✓ Automatic downsampling
  ✓ Time-based queries

Advantages over SQL:
  + Much faster for time-series
  + Compression (10-100x)
  + Built-in retention policies
  + Continuous aggregates

When to use:
  → Metrics / monitoring
  → IoT sensor data
  → Stock prices
  → Application logs

Example: InfluxDB
  INSERT temperature,location=room1 value=23.5
  
  SELECT MEAN(value) FROM temperature
  WHERE time > now() - 1h
  GROUP BY time(5m);
```

**3. NoSQL (Document, Key-Value, etc.)**
```
See detailed NoSQL section below

When NoSQL is better:
  → Flexible schema needed
  → Massive scale (billions of records)
  → Geographic distribution
  → Eventual consistency acceptable
```

**4. Multi-Model Databases**
```
Databases: ArangoDB, OrientDB

What it solves:
  ✓ Document + Graph + Key-Value in one
  ✓ Avoid data duplication across DBs
  ✓ Single query language

When to use:
  → Need multiple data models
  → Want to simplify architecture
  → Can accept trade-offs (jack of all trades)
```

### NoSQL
Flexible schema databases for unstructured/semi-structured data.

**Types:**

#### Key-Value Stores
- **Structure**: Key → Value pairs
- **Examples**: Redis, DynamoDB, Riak
- **Use Cases**: Caching, session storage, user preferences

#### Document Databases
- **Structure**: JSON-like documents
- **Examples**: MongoDB, CouchDB, Firestore
- **Use Cases**: Content management, user profiles, catalogs

#### Graph Databases
- **Structure**: Nodes, edges, properties
- **Examples**: Neo4j, Amazon Neptune, ArangoDB
- **Use Cases**: Social networks, recommendation engines, fraud detection

#### Wide Column Databases
- **Structure**: Column families
- **Examples**: Cassandra, HBase, ScyllaDB
- **Use Cases**: Time-series data, IoT, analytics

#### Time-Series Databases
- **Structure**: Timestamp-indexed data
- **Examples**: InfluxDB, TimescaleDB, Prometheus
- **Use Cases**: Metrics, monitoring, IoT sensor data

#### NoSQL: Advantages

```
✓ Horizontal Scalability
  - Add more servers easily
  - Linear scaling
  - Handle billions of records
  - Petabytes of data
  
  Example: Cassandra
  3 nodes → 6 nodes = 2x capacity
  (Just add servers, auto-rebalance)

✓ Flexible Schema
  - No predefined structure
  - Add fields on the fly
  - Each document can differ
  - Rapid iteration
  
  MongoDB:
  {"name": "John", "age": 30}
  {"name": "Jane", "age": 25, "email": "jane@example.com"}
  ↑ Different fields, no migration needed

✓ High Performance
  - Optimized for specific access patterns
  - No complex joins
  - Direct lookups (key-value)
  - Denormalized data
  
  Redis:
  GET user:123  → <1ms (in-memory)
  
  DynamoDB:
  Get by partition key → ~5ms

✓ High Availability
  - Built-in replication
  - Multi-region support
  - Auto-failover
  - No single point of failure
  
  Cassandra:
  Replication factor = 3
  → Data on 3 nodes
  → 2 nodes can fail, still available

✓ Cost-Effective at Scale
  - Commodity hardware
  - Cloud-native
  - Pay for what you use (DynamoDB)
  - Better resource utilization
  
  Traditional SQL: $10,000/month (beefy server)
  NoSQL cluster: $3,000/month (5 smaller servers)

✓ Better for Specific Use Cases
  - Caching (Redis)
  - Session storage (MongoDB)
  - Analytics (Cassandra)
  - Social graphs (Neo4j)
  - Real-time (Firebase)
```

#### NoSQL: Disadvantages

```
✗ Limited Query Flexibility
  - No ad-hoc queries
  - Must design access patterns upfront
  - No joins (or expensive)
  - Limited aggregations
  
  MongoDB:
  Can't efficiently query:
  "Find users who ordered product X and live in city Y"
  (if not designed for it)

✗ Eventual Consistency
  - Data may be stale temporarily
  - Different nodes may disagree
  - Application must handle
  - Race conditions possible
  
  Example:
  Write to Node A: user.balance = 100
  Immediately read from Node B: user.balance = 90 (stale!)
  
  After 100ms: All nodes = 100 (eventually consistent)

✗ Limited Transaction Support
  - No multi-document ACID (usually)
  - MongoDB: Single document ACID only
  - Cassandra: No transactions
  - Application-level coordination needed
  
  Can't do:
  Transfer money from Account A to B atomically
  (across documents)

✗ Learning Curve
  - Different query languages
  - New concepts (partition keys, denormalization)
  - Access pattern design critical
  - No standard like SQL

✗ Denormalization Complexity
  - Data duplication
  - Update anomalies
  - More storage needed
  - Application must maintain consistency
  
  Example:
  User data stored in:
  - users collection
  - orders.user_info
  - posts.author
  
  Update user name → Must update 3 places!

✗ Less Mature Tooling
  - Fewer GUI tools
  - Less sophisticated ORMs
  - Debugging harder
  - Smaller talent pool

✗ Operational Complexity
  - Distributed systems are complex
  - Replication lag
  - Split-brain scenarios
  - Data consistency issues
  - Monitoring more complex
```

#### When to Choose NoSQL

```
✓ High Volume, High Velocity
  - Millions of writes/sec
  - IoT sensor data
  - Log aggregation
  - Analytics events

✓ Flexible/Evolving Schema
  - Rapid development
  - Frequent schema changes
  - Heterogeneous data
  - MVP/prototyping

✓ Horizontal Scaling Needed
  - Billions of records
  - Petabytes of data
  - Geographic distribution
  - Cannot fit on one machine

✓ Specific Data Models
  - Documents: Content management
  - Key-Value: Caching, sessions
  - Graph: Social networks, recommendations
  - Wide-column: Time-series, analytics

✓ High Availability Priority
  - 99.99%+ uptime required
  - Multi-region deployment
  - Automatic failover
  - Eventual consistency acceptable
```

#### NoSQL Database Comparison

**MongoDB vs Cassandra vs Redis vs Neo4j:**

| Feature | MongoDB | Cassandra | Redis | Neo4j |
|---------|---------|-----------|-------|-------|
| **Type** | Document | Wide Column | Key-Value | Graph |
| **Best For** | General purpose | Time-series, IoT | Caching, sessions | Social networks |
| **Consistency** | Strong (tunable) | Eventual (tunable) | Strong | Strong |
| **Transactions** | Multi-doc ACID | None | Limited | Full ACID |
| **Query** | Rich queries | Limited | Key lookup | Graph traversal |
| **Scaling** | Sharding | Linear | Master-replica | Sharding hard |
| **Speed** | Medium | Very fast writes | Fastest | Medium |
| **Complexity** | Low | High | Low | Medium |
| **Use Case** | Apps, CMS | Analytics, IoT | Cache, real-time | Relationships |

#### Hybrid Approach: Polyglot Persistence

```
Modern architectures use multiple databases:

┌─────────────────────────────────────────┐
│          Application Layer             │
└─────────────┬────────────┬─────────────┘
              │            │            │
      ┌───────┼────────────┼────────────────┐
      │       │            │                │
      ▼       ▼            ▼                ▼
  ┌───────┐ ┌───────┐   ┌───────┐   ┌──────────┐
  │ Postgr│ │ MongoDB│   │ Redis │   │Elasticse│
  │  SQL  │ │ (NoSQL)│   │(Cache)│   │  arch   │
  └───────┘ └───────┘   └───────┘   └──────────┘
  │                              │               │
  Users,          User              Sessions,      Full-text
  Orders,     Preferences,          Rate          Search
  Inventory   Activity Logs       Limiting
  (ACID)      (Flexible)          (Fast)

Example E-commerce App:
✓ PostgreSQL: Orders, inventory (transactions critical)
✓ MongoDB: Product catalog (flexible attributes)
✓ Redis: Session store, cart (fast, temporary)
✓ Elasticsearch: Product search (full-text)
✓ Neo4j: Recommendations (graph relationships)
```

#### Decision Framework: SQL vs NoSQL

**Choose SQL when:**
```
1. Data is structured and relationships are important
2. ACID transactions are critical
3. Complex queries and joins needed
4. Data integrity more important than scale
5. Team familiar with SQL
6. Vertical scaling sufficient
7. Strong consistency required

Examples:
- Banking system
- E-commerce orders/inventory
- ERP/CRM
- Booking/reservation systems
```

**Choose NoSQL when:**
```
1. Massive scale (billions of records)
2. Schema frequently changes
3. Simple access patterns (key-value lookups)
4. Horizontal scaling needed
5. Eventual consistency acceptable
6. High write throughput
7. Geographic distribution

Examples:
- Social media feeds
- IoT sensor data
- Real-time analytics
- Session storage
- Caching layer
```

**Red Flags for Each:**

```
Don't use SQL if:
✗ Need to scale to billions of records
✗ Schema changes daily
✗ Write-heavy workload (1M+ writes/sec)
✗ Multi-region with low latency required

Don't use NoSQL if:
✗ Complex multi-table joins required
✗ ACID transactions critical
✗ Team has no NoSQL experience
✗ Data fits comfortably in SQL
✗ Ad-hoc queries needed frequently
```

### SQL vs NoSQL

| Aspect | SQL | NoSQL |
|--------|-----|-------|
| Schema | Fixed | Flexible |
| Scaling | Vertical | Horizontal |
| Consistency | Strong | Eventual |
| Transactions | Full ACID | Limited |
| Queries | Complex joins | Simple lookups |
| Use Case | Banking, ERP | Social media, IoT |

### Object Storage / Blob Storage
Store unstructured data as objects.

**Features:**
- Flat namespace (no hierarchy)
- Metadata attached to objects
- REST API access
- Highly scalable
- Eventually consistent

**Popular Services:**
- AWS S3
- Azure Blob Storage
- Google Cloud Storage
- MinIO (self-hosted)

**Use Cases:**
- Media files (images, videos)
- Backups and archives
- Data lakes
- Static website hosting

---

## 7. Database Optimization

### Indexing
Data structure to speed up query performance.

**Types:**
- **B-Tree**: Balanced tree, default for most databases
- **Hash**: Fast equality lookups
- **Full-Text**: Text search
- **Geospatial**: Location-based queries
- **Bitmap**: Low-cardinality columns

**Trade-offs:**
- Faster reads
- Slower writes
- Additional storage

**Best Practices:**
- Index frequently queried columns
- Index foreign keys
- Use composite indexes for multiple columns
- Avoid over-indexing
- Monitor index usage

### Replication
Copying data across multiple database servers.

**Types:**
- **Master-Slave (Primary-Replica)**: One write node, multiple read nodes
- **Master-Master (Multi-Master)**: Multiple write nodes
- **Synchronous**: Wait for all replicas (slower, consistent)
- **Asynchronous**: Don't wait (faster, eventually consistent)

**Benefits:**
- High availability
- Read scalability
- Disaster recovery
- Geo-distribution

**Challenges:**
- Replication lag
- Conflict resolution
- Increased complexity

### Sharding (Horizontal Partitioning)
Splitting data across multiple databases.

**Sharding Strategies:**
- **Range-based**: Date ranges, ID ranges
- **Hash-based**: Hash of key (even distribution)
- **Geographic**: By location
- **Directory-based**: Lookup table

**Benefits:**
- Scalability beyond single machine
- Parallel query execution
- Reduced contention

**Challenges:**
- Complex queries across shards
- Rebalancing shards
- Joins become difficult
- Transactions across shards

### Vertical Partitioning
Splitting table columns across multiple tables/databases.

**Example:**
```
Users table → Users (id, name, email) + UserProfiles (user_id, bio, avatar)
```

**Benefits:**
- Separate frequently vs rarely accessed data
- Different access patterns
- Reduce I/O

### Denormalization
Adding redundant data to optimize read performance.

**Techniques:**
- Storing computed values
- Duplicating data
- Flattening hierarchies

**Trade-offs:**
- Faster reads
- Data redundancy
- Complex updates
- Data inconsistency risk

**When to Use:**
- Read-heavy workloads
- Performance critical
- After measuring bottlenecks

---

## 8. Caching

### What is Caching?

#### The Art of Remembering: The Most Powerful Optimization

Caching is arguably the **single most impactful** optimization in system design. It's based on a profound observation about data access patterns: **locality of reference**—the same data is accessed repeatedly, and recently accessed data is likely to be accessed again soon.

#### The Deep Theory: Why Caching Works

**The Fundamental Principle:**
Accessing data has a cost—in time, money, and resources. That cost varies wildly:
```
CPU L1 Cache:      0.5 nanoseconds   (baseline)
CPU L2 Cache:      7 nanoseconds     (14x slower)
RAM:               100 nanoseconds   (200x slower)
SSD:               150,000 nanoseconds (300,000x slower)
HDD:               10,000,000 nanoseconds (20 million x slower)
Network (same DC): 500,000 nanoseconds (1 million x slower)
Network (cross-continent): 150,000,000 nanoseconds (300 million x slower)
```

**The Revelation:**
If you can serve from a faster tier, you eliminate orders of magnitude of latency. Cache a database query result in Redis:
- **Before**: 50ms database query
- **After**: 0.5ms Redis lookup
- **Speedup**: 100x faster

**The Economic Argument:**
```
Database: $1,000/month for 1000 QPS
Redis: $100/month for 100,000 QPS

90% cache hit rate:
- 900 requests from Redis: cheap
- 100 requests from DB: normal load
- Result: Handle 10x traffic at same cost
```

#### The Cache Hierarchy: Layers Upon Layers

Caching exists at every level of the stack. Understanding where each tier belongs is critical.

##### Browser Cache (Client-Side)
```
User requests logo.png
  ↓
Browser: "I have this from yesterday"
  ↓
Return from disk: 0ms network time
```

**Control via HTTP Headers:**
```http
Cache-Control: max-age=31536000, immutable  # 1 year
Cache-Control: no-cache  # Always validate
Cache-Control: no-store  # Never cache
ETag: "v1.23"  # Version-based validation
```

**Benefits:**
- Zero server load
- Zero network latency
- Scales infinitely (each user caches locally)

**Challenges:**
- Can't invalidate (stuck until expiry)
- Different versions across users
- Wasted bandwidth if user never returns

**Best For:**
- Static assets (CSS, JS, images)
- Infrequently changing content
- User-specific data (after login)

##### CDN Cache (Edge)
```
User in Tokyo requests image
  ↓
CDN Tokyo node: "I have this"
  ↓
Return from edge: 5ms (vs 200ms from US origin)
```

**How It Works:**
1. User requests file
2. CDN edge node checks cache
3. If miss: Fetch from origin, cache, return
4. If hit: Return immediately
5. Subsequent users in region: Served from cache

**Benefits:**
- Geographic proximity (low latency)
- Offloads origin servers (90%+ hit rates)
- Handles traffic spikes (DDoS protection)
- Bandwidth savings (serve from edge)

**Best For:**
- Static assets globally distributed
- Media files (images, videos)
- API responses (with care)
- Software downloads

**Advanced: Dynamic Content Caching**
Modern CDNs cache API responses:
```http
GET /api/products?category=shoes
Cache-Control: max-age=60, s-maxage=300
# Browser caches 60s, CDN caches 300s
```

##### Application Cache (In-Memory)
```
User requests user profile
  ↓
App server: Check Redis
  ↓ (hit)
Return from Redis: 1ms (vs 50ms from DB)
```

**Types:**

**1. Local Cache (In-Process)**
```python
# Cache in application memory
cache = {}

def get_user(user_id):
    if user_id in cache:
        return cache[user_id]  # 100 nanoseconds
    
    user = db.query(user_id)  # 50 milliseconds
    cache[user_id] = user
    return user
```

**Pros:**
- Extremely fast (nanoseconds)
- No network calls
- Simple implementation

**Cons:**
- Limited by server RAM
- Not shared across servers
- Invalidation is complex
- Lost on server restart

**When to Use:**
- Reference data (countries, config)
- Session data (if single server)
- Small datasets

**2. Distributed Cache (Redis, Memcached)**
```python
import redis

cache = redis.Redis()

def get_user(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)  # 1 millisecond
    
    user = db.query(user_id)  # 50 milliseconds
    cache.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

**Pros:**
- Shared across all servers
- Persistent (survives app restarts)
- Large capacity (100s of GB)
- Atomic operations

**Cons:**
- Network latency (1-2ms)
- Additional infrastructure
- Cost

**When to Use:**
- Multi-server deployments
- Large datasets
- Session management
- Rate limiting counters

##### Database Cache (Query Cache)
```sql
SELECT * FROM users WHERE id = 123;
  ↓
DB: "I executed this 1 second ago"
  ↓
Return cached result: 0.1ms (vs 10ms)
```

**Built-in Database Caching:**
- **Query cache**: Cache entire query results
- **Buffer pool**: Cache data pages in RAM
- **Prepared statements**: Cache execution plans

**Limitation:**
Invalidates on ANY write to table (too aggressive)

**Better Approach:**
Manual caching at application layer (more control)

#### The Cache Hierarchy Strategy

**The Cascade Pattern:**
```
Request comes in
  ↓
1. Check local cache (100 nanoseconds)
   Hit: Return
   Miss: ↓
2. Check Redis (1 millisecond)
   Hit: Store in local, return
   Miss: ↓
3. Check database (50 milliseconds)
   Hit: Store in Redis + local, return
   Miss: Return 404
```

**Hit Rate Multiplication:**
```
Local cache: 50% hit rate
Redis cache: 40% hit rate (of local misses)
Database: 10% of requests

Result:
- 50% served in 100ns
- 40% served in 1ms
- 10% served in 50ms
Average: 5.05ms (vs 50ms without caching)
```

### Cache Aside (Lazy Loading)
Application manages cache explicitly.

**Flow:**
1. Check cache
2. If miss, query database
3. Store in cache
4. Return data

**Pros:** Only cache what's needed
**Cons:** Cache misses add latency

### Read Through Strategy
Cache sits between application and database.

**Flow:**
1. Application queries cache
2. Cache manages database fetch on miss
3. Returns data

**Pros:** Simplified application logic
**Cons:** Initial miss penalty

### Write Through Strategy
Write to cache and database simultaneously.

**Pros:** Data consistency
**Cons:** Write latency

### Write Behind (Write Back)
Write to cache first, asynchronously to database.

**Pros:** Fast writes
**Cons:** Risk of data loss

### Write Around
Write directly to database, cache on read.

**Pros:** Reduces cache pollution
**Cons:** Read misses after writes

### Cache Invalidation
Removing stale data from cache.

**Strategies:**
- **TTL (Time To Live)**: Expire after time
- **Event-based**: Invalidate on updates
- **Manual**: Explicit invalidation

**Eviction Policies:**
- **LRU (Least Recently Used)**
- **LFU (Least Frequently Used)**
- **FIFO (First In First Out)**
- **Random**

**Popular Cache Systems:**
- Redis
- Memcached
- Hazelcast
- Ehcache

---

## 9. Scalability & Performance

### Latency & Bandwidth

**Latency**: Time for data to travel from source to destination
- Network latency
- Disk I/O latency
- Database query latency
- API response time

**Bandwidth**: Amount of data transferred per unit time
- Measured in Mbps or Gbps
- Affects throughput

**Optimization:**
- Reduce round trips
- Use CDN
- Compress data
- Optimize queries
- Use caching

### Scalability
Ability to handle increased load.

**Vertical Scaling (Scale Up):**
- Add more resources to single machine (CPU, RAM, SSD)
- **Pros**: Simple, no code changes
- **Cons**: Limited by hardware, single point of failure, expensive

**Horizontal Scaling (Scale Out):**
- Add more machines
- **Pros**: Virtually unlimited, fault tolerant, cost-effective
- **Cons**: Complex, requires distributed system design

**Factors to Consider:**
- Stateless services (easier to scale)
- Database sharding
- Load balancing
- Caching
- Async processing

### Throughput
Number of operations completed per unit time.

**Metrics:**
- Requests per second (RPS)
- Queries per second (QPS)
- Transactions per second (TPS)

**Improving Throughput:**
- Horizontal scaling
- Caching
- Connection pooling
- Batch processing
- Async operations

### Performance Optimization
- **Database**: Indexing, query optimization, connection pooling
- **Application**: Code optimization, caching, lazy loading
- **Network**: CDN, compression, HTTP/2
- **Infrastructure**: Load balancing, auto-scaling

---

## 10. Reliability & Consistency

### Availability & Reliability

**Availability**: Percentage of time system is operational
- Measured in "nines": 99.9% = 3 nines = ~8.76 hours downtime/year
- **99.9% (3 nines)**: 8.76 hours/year
- **99.99% (4 nines)**: 52.56 minutes/year
- **99.999% (5 nines)**: 5.26 minutes/year

**Reliability**: Ability to function correctly over time
- Mean Time Between Failures (MTBF)
- Mean Time To Repair (MTTR)

**Improving Availability:**
- Redundancy (multiple instances)
- Load balancing
- Failover mechanisms
- Health checks
- Geographic distribution

### Single Point of Failure (SPOF)
Component whose failure brings down entire system.

**Examples:**
- Single database
- Single load balancer
- Single data center

**Mitigation:**
- Redundancy
- Replication
- Clustering
- Multi-region deployment

### Consistency

**Strong Consistency:**
- Read returns most recent write
- All nodes see same data at same time
- Higher latency
- Example: SQL databases

**Eventual Consistency:**
- System becomes consistent over time
- Temporary inconsistency allowed
- Lower latency, higher availability
- Example: DynamoDB, Cassandra

**Consistency Levels (Cassandra example):**
- ONE: Any single node
- QUORUM: Majority of nodes
- ALL: All nodes

### CAP Theorem

#### The Immutable Law of Distributed Systems

The CAP Theorem is not a guideline or best practice—it's a **fundamental law of physics** for distributed systems, as immutable as the laws of thermodynamics. Formulated by Eric Brewer in 2000 and proven by Seth Gilbert and Nancy Lynch in 2002, it states an impossible choice:

**In a distributed system, you can guarantee at most TWO of the following three properties simultaneously:**

1. **Consistency (C)**: All nodes see the same data at the same time
2. **Availability (A)**: Every request receives a response (success or failure)
3. **Partition Tolerance (P)**: System continues operating despite network failures

#### The Deep Theory: Why CAP is Inevitable

**The Impossibility Proof (Simplified):**

Imagine a distributed database with two nodes, N1 and N2.

**Scenario: Network Partition**
```
N1 (New York)  |  NETWORK PARTITION  |  N2 (London)
   X = 10      |      (no communication)     |    X = 10
```

**User A writes to N1:**
```
N1: X = 20  |  PARTITION  |  N2: X = 10
```

N1 cannot tell N2 about the update. Now User B reads from N2.

**The Impossible Choice:**

**Option 1: Choose Consistency (CP)**
```
N2: "I can't guarantee I have the latest value"
N2: Returns ERROR or TIMEOUT
Result: Not Available (❌ A)
```

**Option 2: Choose Availability (AP)**
```
N2: "I'll return my value: X = 10"
Result: Inconsistent (wrong value!) (❌ C)
```

**Option 3: Choose CA (Ignore partitions)**
```
Assume network never fails
Result: System breaks during partition (❌ P)
```

**The Revelation:**
There is **no fourth option**. Network partitions will happen (hardware fails, cables cut, routers crash). Therefore, P is not optional—you must tolerate partitions. The real choice is **C vs A during a partition**.

#### The Three Properties: Deep Dive

##### Consistency (C)

**Formal Definition:**
Linearizability—every read receives the most recent write or an error.

**What It Means:**
```
Write(X = 5) completes at time T
  ⇓
Any Read(X) starting at or after T returns 5
  ⇓
All nodes agree on the value at any given time
```

**The Guarantee:**
- System behaves like a single, atomic unit
- No client ever sees stale data
- Operations appear to happen in a total order

**The Cost:**
- Must coordinate across nodes (slow)
- Blocks during partition (unavailable)
- Limited by speed of light (can't make network faster)

**Example: Banking**
```python
balance = 100
withdraw(50)  # Must coordinate
read_balance()  # Must see 50
```
Wrong balance = overdraft = lost money. Consistency is mandatory.

##### Availability (A)

**Formal Definition:**
Every request receives a response, without guarantee it contains the most recent write.

**What It Means:**
```
Any non-failing node must respond
  ⇓
No timeouts, no errors (except when node truly dead)
  ⇓
System stays up even during partition
```

**The Guarantee:**
- Always get an answer
- Low latency (no waiting for coordination)
- System stays operational during network issues

**The Cost:**
- Might return stale data
- Different nodes might disagree
- Must handle conflicts

**Example: Social Media Feed**
```python
post_tweet("Hello")
read_feed()  # Might not see "Hello" yet
```
Missing a tweet briefly = acceptable. Being down = unacceptable.

##### Partition Tolerance (P)

**Formal Definition:**
System continues operating despite arbitrary message loss between nodes.

**What It Means:**
```
Network can drop/delay any messages
  ⇓
System still functions (maybe degraded)
  ⇓
No assumption of reliable network
```

**The Reality:**
Partitions are not theoretical—they happen:
- Switch failure: 100s of times/year
- Fiber cut: 10s of times/year  
- Datacenter network failure: Multiple times/year
- Cross-datacenter partition: Rare but catastrophic

**The Conclusion:**
Partition tolerance is **not optional** in distributed systems. Networks fail. You must handle it.

#### The Real Choice: CP vs AP

Since P is mandatory, you choose between C and A **during a partition**.

##### CP Systems (Consistency over Availability)

**Philosophy**: "Better to be unavailable than wrong."

**Behavior During Partition:**
```
Write request arrives at partitioned node
  ↓
Node: "Can't reach other nodes to coordinate"
  ↓
Returns ERROR (503 Service Unavailable)
  ↓
Client knows operation didn't complete
```

**Characteristics:**
- Sacrifice availability during partition
- Always return correct (or no) answer
- Coordinate writes across majority
- Use consensus protocols (Paxos, Raft)

**Examples:**
- **HBase**: Requires ZooKeeper quorum
- **MongoDB** (with write concern majority): Waits for replica acknowledgment
- **Consul**: Requires consensus for writes
- **etcd**: Raft-based, requires quorum

**When to Choose CP:**
- Financial transactions (can't lose money)
- Inventory systems (can't oversell)
- Booking systems (can't double-book)
- Any system where correctness > uptime

**Real Example: Bank ATM**
```
Partition occurs
  ↓
ATM can't reach central database
  ↓
ATM displays: "Service temporarily unavailable"
  ↓
Better than dispensing cash twice or showing wrong balance
```

##### AP Systems (Availability over Consistency)

**Philosophy**: "Better to be approximately right than unavailable."

**Behavior During Partition:**
```
Write request arrives at partitioned node
  ↓
Node: "Can't reach others, but I'll accept anyway"
  ↓
Returns SUCCESS (202 Accepted)
  ↓
Will sync with others later (eventual consistency)
```

**Characteristics:**
- Always available (as long as any node works)
- Accept temporary inconsistency
- Use conflict resolution (last-write-wins, vector clocks, CRDTs)
- Eventual consistency model

**Examples:**
- **Cassandra**: Multi-master, always writable
- **DynamoDB**: Eventually consistent reads by default
- **Riak**: Anti-entropy for reconciliation
- **CouchDB**: Master-master replication

**When to Choose AP:**
- Social media (stale likes tolerable)
- Shopping cart (brief inconsistency OK)
- Analytics (approximate counts fine)
- Any system where uptime > perfect accuracy

**Real Example: Shopping Cart**
```
Partition occurs
  ↓
User adds item to cart
  ↓
Local node accepts: "Added to cart"
  ↓
Items might appear differently on different nodes briefly
  ↓
Eventually syncs (user doesn't notice)
```

#### CA Systems: The Myth

**Traditional RDBMS (Single Node):**
- **C**: Strong ACID guarantees
- **A**: Always responds (if node is up)
- **P**: Not tolerant (there's only one node)

**The Truth:**
CA systems are **not distributed**. They're single nodes. The moment you add a second node, you must choose CP or AP.

**CA Distributed Systems Don't Exist in Real Networks:**
If you try to build one, any partition breaks it entirely.

#### The Spectrum: It's Not Binary

Real systems don't make a hard choice—they offer **tunable consistency**.

##### Cassandra: The Exemplar

**Tunable Consistency Levels:**

**Write Consistency:**
```
ANY:  Success if any node acknowledges (even hinted handoff)
ONE:  Success if one replica acknowledges (AP)
QUORUM: Success if majority acknowledges (CP)
ALL:  Success if all replicas acknowledge (CP, slower)
```

**Read Consistency:**
```
ONE:  Return from first replica (fast, might be stale)
QUORUM: Read from majority, return newest (slower, consistent)
ALL:  Read from all replicas (slowest, most consistent)
```

**The Magic Formula:**
```
If (Write_Replicas + Read_Replicas) > Replication_Factor:
    Guaranteed to see latest write (Strong Consistency)

Example:
Replication = 3
Write = QUORUM (2)
Read = QUORUM (2)
2 + 2 > 3 ✓ (overlap guaranteed)
```

**Per-Request Tunability:**
```python
# Strong consistency (CP behavior)
session.execute(query, consistency_level=QUORUM)

# High availability (AP behavior)
session.execute(query, consistency_level=ONE)
```

**The Power:**
Choose C vs A **per request**:
- User login: QUORUM (security-critical)
- View post: ONE (speed matters)
- Write post: QUORUM (data important)
- Page view count: ONE (approximate OK)

#### PACELC: The CAP Extension

**CAP Only Discusses Partitions. What About Normal Operation?**

PACELC Theorem (Daniel Abadi, 2012):
```
If Partition:
    Choose between Availability and Consistency
Else (no partition):
    Choose between Latency and Consistency
```

**The Addition:**
Even without partitions, there's a trade-off:
- **High Consistency**: Coordinate across nodes (higher latency)
- **Low Latency**: Don't coordinate (eventual consistency)

**System Classification:**
- **PA/EL**: Available during partition, Low latency normally (Cassandra, DynamoDB)
- **PA/EC**: Available during partition, Consistent normally (???—rare)
- **PC/EL**: Consistent during partition, Low latency normally (???—rare)  
- **PC/EC**: Consistent during partition, Consistent normally (Traditional DBs)

#### Real-World Examples: Who Chose What?

**Google Spanner (PC/EC):**
- CP during partitions
- Strong consistency always
- Uses atomic clocks for global time
- **Trade-off**: High latency (10-100ms), complex infrastructure

**Amazon DynamoDB (PA/EL):**
- AP during partitions  
- Eventually consistent reads by default
- **Trade-off**: Can read stale data, simpler, faster

**MongoDB (PC/EC with tuning):**
- CP during partitions (write concern = majority)
- Can tune to AP (write concern = 1)
- **Trade-off**: Flexible but requires understanding

**Cassandra (PA/EL with tuning):**
- AP by default
- Can achieve CP with QUORUM reads/writes
- **Trade-off**: Maximum flexibility, maximum complexity

#### The Wisdom: How to Choose

**Ask These Questions:**

1. **What happens if I show stale data?**
   - Lost money? → CP
   - User confusion? → AP

2. **What happens if system is down?**
   - Lost sales? → AP
   - Wrong transaction? → CP

3. **Can I handle conflicts?**
   - Yes (last write wins, CRDTs) → AP
   - No (needs coordination) → CP

4. **What's more expensive: downtime or incorrectness?**
   - Downtime → AP
   - Incorrectness → CP

**Domain Examples:**

| Domain | Choice | Reason |
|--------|--------|--------|
| Banking | CP | Money can't be wrong |
| Social Media | AP | Brief staleness OK |
| E-commerce | AP | Cart inconsistency tolerable |
| Inventory | CP | Can't oversell |
| Analytics | AP | Approximate counts fine |
| DNS | AP | Eventual consistency acceptable |
| Booking | CP | No double-bookings |
| Likes/Views | AP | Exact count not critical |

**The Modern Approach: Hybrid**

Don't choose system-wide. Choose per-data-type:
```python
# Strong consistency for critical data
db.users.update(query, write_concern="majority")

# Eventual consistency for less critical
db.page_views.insert(data, write_concern="acknowledged")
```

#### The Fundamental Insight

CAP is not about databases or technologies—it's about **the nature of distributed systems**. It's a consequence of:
- The finite speed of light
- The impossibility of perfectly reliable networks  
- The fundamental trade-off between coordination and independence

You can't engineer around CAP. You can only make informed choices about which trade-offs suit your use case.

**The Meta-Lesson:**
*"In distributed systems, you can't have everything. Understanding what you can sacrifice is the key to good design."*

### PACELC Theorem
Extension of CAP:
- **If Partition**: Choose between Availability and Consistency
- **Else**: Choose between Latency and Consistency

### Fault Tolerance
System continues operating despite failures.

**Techniques:**
- Replication
- Redundancy
- Graceful degradation
- Failover
- Circuit breakers
- Retry mechanisms

### Disaster Recovery
Plan for recovering from catastrophic failures.

**Metrics:**
- **RTO (Recovery Time Objective)**: Max downtime tolerated
- **RPO (Recovery Point Objective)**: Max data loss tolerated

**Strategies:**
- Regular backups
- Multi-region replication
- Disaster recovery site
- Regular testing

---

## 11. Architecture Patterns

### Monolith Architecture
Single unified codebase and deployment.

**Pros:**
- Simple to develop and deploy
- Easy to test
- Better performance (no network calls)
- Simpler debugging

**Cons:**
- Difficult to scale
- Slower deployment
- Technology lock-in
- Poor fault isolation

**When to Use:**
- Small teams
- Simple applications
- Startups (MVP stage)

### Microservices Architecture
Application composed of small, independent services.

**Characteristics:**
- Single responsibility
- Independent deployment
- Decentralized data
- Technology diversity
- Communication via APIs

**Pros:**
- Independent scaling
- Fault isolation
- Technology flexibility
- Faster deployment
- Team autonomy

**Cons:**
- Complex infrastructure
- Distributed system challenges
- Testing complexity
- Data consistency issues
- Operational overhead

**Best Practices:**
- Domain-driven design
- API versioning
- Centralized logging
- Service mesh
- Circuit breakers

### Event-Driven Architecture
Components communicate through events.

**Components:**
- **Event Producers**: Generate events
- **Event Broker**: Routes events (Kafka, RabbitMQ)
- **Event Consumers**: Process events

**Patterns:**
- **Event Notification**: Alert other systems
- **Event-Carried State Transfer**: Full data in event
- **Event Sourcing**: Store events as source of truth
- **CQRS**: Separate read and write models

**Benefits:**
- Loose coupling
- Scalability
- Asynchronous processing
- Event replay capability

**Challenges:**
- Eventual consistency
- Event ordering
- Debugging difficulty
- Schema evolution

### Serverless Architecture
Run code without managing servers (FaaS).

**Characteristics:**
- Event-driven execution
- Auto-scaling
- Pay-per-use
- Stateless functions
- Managed by cloud provider

**Pros:**
- No server management
- Auto-scaling
- Cost-effective (no idle resources)
- Fast deployment

**Cons:**
- Cold starts
- Vendor lock-in
- Limited execution time
- Debugging challenges
- State management

**Use Cases:**
- API backends
- Data processing
- Scheduled tasks
- Webhooks

---

## 12. Performance & Resilience Patterns

### Rate Limiting
Control number of requests in time window.

**Algorithms:**
- **Fixed Window**: Count requests per fixed time window
- **Sliding Window**: Rolling time window
- **Token Bucket**: Tokens added at fixed rate
- **Leaky Bucket**: Requests processed at fixed rate

**Benefits:**
- Prevent abuse
- Ensure fair usage
- Protect backend
- Cost control

**Implementation:**
- API Gateway
- Redis
- Nginx
- Application code

### Throttling
Deliberately slow down processing to protect system.

**Types:**
- **Request throttling**: Limit incoming requests
- **Resource throttling**: Limit resource consumption
- **User throttling**: Limit per user

**Difference from Rate Limiting:**
- Rate limiting: Hard limits, reject excess
- Throttling: Slow down, queue excess

### Backpressure
Downstream component signals upstream to slow down.

**Mechanisms:**
- Bounded queues
- Reactive Streams
- TCP flow control
- HTTP/2 flow control

**Benefits:**
- Prevent system overload
- Graceful degradation
- Resource protection

### Idempotency
Multiple identical requests have same effect as single request.

**HTTP Idempotent Methods:**
- GET, PUT, DELETE, HEAD, OPTIONS
- NOT POST (creates new resource each time)

**Implementation:**
- Idempotency keys
- Database constraints
- Check before insert
- State machines

**Use Cases:**
- Payment processing
- Order submission
- Retry logic

### Circuit Breaker
Prevent cascading failures by failing fast.

**States:**
- **Closed**: Normal operation
- **Open**: Requests fail immediately
- **Half-Open**: Test if service recovered

**Benefits:**
- Fail fast
- Prevent resource exhaustion
- Allow service recovery
- Graceful degradation

**Tools:**
- Hystrix (Netflix, deprecated)
- Resilience4j
- Polly (.NET)

### Retry Mechanisms
Automatically retry failed operations.

**Strategies:**
- **Fixed delay**: Wait same time between retries
- **Exponential backoff**: Increase delay exponentially
- **Jitter**: Add randomness to avoid thundering herd

**Best Practices:**
- Set max retries
- Only retry transient failures
- Use exponential backoff
- Implement idempotency

### Bulkhead Pattern
Isolate resources to prevent cascading failures.

**Example:**
- Separate connection pools per service
- Separate thread pools
- Resource quotas

**Benefits:**
- Fault isolation
- Resource protection
- Prevent total system failure

### Health Checks
Monitor service health and availability.

**Types:**
- **Liveness**: Is service running?
- **Readiness**: Can service handle requests?
- **Startup**: Has service finished initialization?

**Implementation:**
- HTTP endpoints (`/health`, `/ready`)
- Periodic polling
- Metrics collection

**Use Cases:**
- Load balancer routing
- Auto-scaling decisions
- Container orchestration
- Service discovery

---

## 13. Security

### Authentication vs Authorization

**Authentication**: Verify identity (Who are you?)
- Username/password
- OAuth
- SAML
- Biometrics
- Multi-factor authentication (MFA)

**Authorization**: Verify permissions (What can you do?)
- Role-based (RBAC)
- Attribute-based (ABAC)
- Access control lists (ACL)

### OAuth
Open standard for delegated authorization.

**Flow (Authorization Code):**
1. User clicks "Login with Google"
2. Redirect to OAuth provider
3. User approves
4. Redirect back with code
5. Exchange code for access token
6. Use token to access resources

**OAuth 2.0 Grant Types:**
- Authorization Code (server-side apps)
- Implicit (deprecated)
- Client Credentials (service-to-service)
- Resource Owner Password (legacy)
- PKCE (mobile/SPA apps)

### JWT (JSON Web Token)
Compact, self-contained token for secure information transfer.

**Structure:**
```
Header.Payload.Signature
```

**Parts:**
- **Header**: Algorithm and type
- **Payload**: Claims (user data)
- **Signature**: Verify authenticity

**Pros:**
- Stateless
- Cross-domain
- Self-contained
- Scalable

**Cons:**
- Cannot revoke (until expiry)
- Size (larger than session ID)
- Vulnerable if stolen

**Best Practices:**
- Short expiration
- HTTPS only
- Secure storage
- Refresh tokens for long sessions

---

## 14. Observability

### Logging
Recording application events.

**Log Levels:**
- **TRACE**: Very detailed
- **DEBUG**: Diagnostic information
- **INFO**: General information
- **WARN**: Warning messages
- **ERROR**: Error events
- **FATAL**: Critical failures

**Best Practices:**
- Structured logging (JSON)
- Include correlation IDs
- Log at appropriate levels
- Don't log sensitive data
- Centralize logs

**Tools:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- Datadog
- CloudWatch

### Monitoring
Collecting and analyzing metrics.

**Types:**
- **Infrastructure**: CPU, memory, disk, network
- **Application**: Request rate, latency, errors
- **Business**: User signups, transactions, revenue

**Key Metrics (RED Method):**
- **Rate**: Requests per second
- **Errors**: Error rate
- **Duration**: Response time

**Key Metrics (USE Method):**
- **Utilization**: % time busy
- **Saturation**: Queue depth
- **Errors**: Error count

**Tools:**
- Prometheus + Grafana
- Datadog
- New Relic
- CloudWatch

### Tracing
Track requests across distributed systems.

**Distributed Tracing:**
- Trace ID across all services
- Span ID for each operation
- Parent-child relationships
- Timing information

**Tools:**
- Jaeger
- Zipkin
- AWS X-Ray
- OpenTelemetry

### Alerting
Notify team of issues.

**Best Practices:**
- Alert on symptoms, not causes
- Reduce noise
- Clear escalation policy
- Runbooks for common issues
- SLO-based alerting

---

## 15. Advanced Concepts

### CQRS (Command Query Responsibility Segregation)
Separate read and write models.

**Benefits:**
- Optimized read/write separately
- Scalability
- Different data models

**Challenges:**
- Complexity
- Eventual consistency
- Data synchronization

### Event Sourcing
Store state changes as sequence of events.

**Benefits:**
- Complete audit trail
- Replay events
- Temporal queries
- Debugging

**Challenges:**
- Storage growth
- Schema evolution
- Complexity

### Saga Pattern
Manage distributed transactions across services.

**Types:**
- **Choreography**: Services coordinate via events
- **Orchestration**: Central coordinator

**Compensation:**
- Rollback via compensating transactions
- Not true ACID

### Distributed Consensus
Agreement among distributed nodes.

**Algorithms:**
- **Paxos**: Complex, proven
- **Raft**: Simpler, understandable
- **ZAB** (ZooKeeper Atomic Broadcast)

**Use Cases:**
- Leader election
- Configuration management
- Distributed locks

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

## 16. Data Processing

### Batch Processing
Process large volumes of data at scheduled intervals.

**Characteristics:**
- High latency
- High throughput
- Scheduled execution

**Tools:**
- Apache Spark
- Hadoop MapReduce
- AWS Batch

**Use Cases:**
- Data warehousing
- Report generation
- ETL pipelines

### Stream Processing
Process data in real-time as it arrives.

**Characteristics:**
- Low latency
- Continuous processing
- Event-driven

**Tools:**
- Apache Kafka Streams
- Apache Flink
- AWS Kinesis

**Use Cases:**
- Real-time analytics
- Fraud detection
- IoT data processing

### Text-Based Search & Indexing
Full-text search capabilities.

**Features:**
- Tokenization
- Relevance scoring
- Fuzzy matching
- Faceted search

**Tools:**
- Elasticsearch
- Apache Solr
- Algolia

**Use Cases:**
- E-commerce search
- Document search
- Log analysis

---

## 17. Additional Important Concepts

### Back-of-the-Envelope Calculations
Quick estimations for system design.

**Key Numbers:**
- 1 million requests/day ≈ 12 requests/second
- 86,400 seconds in a day
- 1 KB = 1,000 bytes
- 1 MB = 1,000 KB
- 1 GB = 1,000 MB

**Latency Numbers:**
- L1 cache: 0.5 ns
- L2 cache: 7 ns
- RAM: 100 ns
- SSD: 150 μs
- HDD: 10 ms
- Network (same datacenter): 0.5 ms
- Network (cross-country): 150 ms

### Data Partitioning
Split data for scalability.

**Types:**
- **Horizontal**: Sharding (split rows)
- **Vertical**: Split columns
- **Functional**: By business domain

### Cold Start Problem
Initial delay when starting serverless functions or services.

**Mitigation:**
- Keep functions warm
- Provisioned concurrency
- Optimize initialization
- Use lighter runtimes

### Blue-Green Deployment
Two identical environments for zero-downtime deploys.

**Process:**
1. Deploy to inactive (green)
2. Test green environment
3. Switch traffic to green
4. Keep blue as fallback

### Canary Deployment
Gradual rollout to subset of users.

**Process:**
1. Deploy to small % of servers
2. Monitor metrics
3. Gradually increase %
4. Rollback if issues

### Feature Flags
Toggle features on/off without deployment.

**Benefits:**
- A/B testing
- Gradual rollout
- Quick rollback
- Environment-specific features

---

## 18. Resources & Learning

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "System Design Interview" by Alex Xu
- "Building Microservices" by Sam Newman
- "Site Reliability Engineering" by Google

### Engineering Blogs
- Netflix Tech Blog
- Uber Engineering
- Meta Engineering
- AWS Architecture Blog
- Martin Fowler's Blog

### Practice Resources
- System Design Primer (GitHub)
- LeetCode System Design
- Grokking the System Design Interview
- ByteByteGo
- HighScalability.com

### Project Ideas
1. **URL Shortener**: Like bit.ly
2. **Pastebin**: Code sharing service
3. **Rate Limiter**: API throttling service
4. **Chat Application**: Real-time messaging
5. **News Feed**: Like Twitter/Facebook
6. **File Storage**: Like Dropbox
7. **Video Streaming**: Like YouTube/Netflix
8. **Ride-Sharing**: Like Uber/Lyft
9. **E-commerce**: Like Amazon
10. **Social Network**: Like Instagram

---

## Summary: The Art and Science of System Design

### The Essential Truth

System design is fundamentally about **managing complexity through principled decision-making**. Every great system is built on a foundation of:

1. **Clear Understanding**: Know your requirements deeply
2. **Appropriate Trade-offs**: Choose wisely based on context
3. **Continuous Evolution**: Adapt as needs change
4. **Measurable Outcomes**: Validate decisions with data
5. **Human Consideration**: Design for people, not just machines

### The Core Trade-offs

Every system design decision involves balancing opposing forces:

| Dimension | Trade-off | Consideration |
|-----------|-----------|---------------|
| **CAP Theorem** | Consistency ↔ Availability | Can't have both during partitions |
| **Performance** | Latency ↔ Throughput | Fast response vs high volume |
| **Complexity** | Simplicity ↔ Features | Easy to maintain vs rich functionality |
| **Economics** | Cost ↔ Performance | Budget vs speed/reliability |
| **Data** | Normalization ↔ Denormalization | Consistency vs read performance |
| **Architecture** | Monolith ↔ Microservices | Simplicity vs scalability |
| **Consistency** | Strong ↔ Eventual | Immediate vs delayed consistency |
| **Caching** | Freshness ↔ Performance | Up-to-date vs fast |
| **Security** | Security ↔ Convenience | Protection vs user friction |
| **Deployment** | Speed ↔ Safety | Fast releases vs stability |

### The Golden Rules of System Design

1. **Start Simple, Then Scale**
   - Begin with the simplest solution that could work
   - Add complexity only when proven necessary
   - Premature optimization wastes time and money
   - *"Make it work, make it right, make it fast"* - in that order

2. **Measure Before Optimizing**
   - Intuition often misleads
   - Profile to find real bottlenecks
   - Set SLOs/SLAs based on user needs
   - Monitor continuously, alert intelligently

3. **Design for Failure**
   - Assume everything will fail
   - Build redundancy at every level
   - Implement graceful degradation
   - Test failure scenarios (chaos engineering)
   - Have runbooks for common failures

4. **Embrace Eventual Consistency** (When Appropriate)
   - Not all data needs immediate consistency
   - AP systems often provide better user experience
   - Use strong consistency only where required
   - Understand your consistency guarantees

5. **Security is Non-Negotiable**
   - Design security in from day one
   - Defense in depth (multiple layers)
   - Encrypt data at rest and in transit
   - Regular security audits and updates
   - Principle of least privilege

6. **Observability is Essential**
   - You can't fix what you can't see
   - Comprehensive logging (with correlation IDs)
   - Real-time metrics and dashboards
   - Distributed tracing for microservices
   - Proactive alerting, not reactive firefighting

7. **Keep It Maintainable**
   - Code is read 10x more than written
   - Clear documentation saves months
   - Standardize where possible
   - Reduce cognitive load
   - Think of the 3 AM on-call engineer

8. **Cost-Consciousness Matters**
   - Engineering time is expensive
   - Infrastructure costs add up
   - Technical debt compounds
   - Choose battles worth fighting
   - ROI should guide technical decisions

### The System Design Mental Model

When approaching any system design problem, use this framework:

#### **Phase 1: Understanding (Requirements & Constraints)**
```
1. Functional Requirements
   - What should the system do?
   - What are the core features?
   - What are the user flows?

2. Non-Functional Requirements
   - How many users? (Scale)
   - How fast? (Latency)
   - How reliable? (Availability)
   - How consistent? (Data guarantees)

3. Constraints
   - Budget limitations
   - Timeline (MVP vs complete)
   - Team size and expertise
   - Compliance requirements
```

#### **Phase 2: Estimation (Back-of-the-Envelope)**
```
1. Scale Calculations
   - DAU (Daily Active Users)
   - QPS (Queries Per Second)
   - Peak load (2-3x average)

2. Storage Calculations
   - Data per user/transaction
   - Growth rate
   - Retention period
   - Replication factor

3. Bandwidth Calculations
   - Request/response sizes
   - Traffic patterns
   - CDN needs
```

#### **Phase 3: Design (High-Level Architecture)**
```
1. API Design
   - Endpoints and methods
   - Request/response formats
   - Authentication mechanism

2. Data Model
   - Entities and relationships
   - Database choice (SQL vs NoSQL)
   - Partitioning strategy

3. Component Diagram
   - Client → API Gateway → Services → Databases
   - Load balancers
   - Caching layers
   - Message queues
```

#### **Phase 4: Deep Dive (Bottlenecks & Optimization)**
```
1. Identify Bottlenecks
   - Database (hot partitions, slow queries)
   - Network (latency, bandwidth)
   - Compute (CPU, memory)

2. Optimization Strategies
   - Caching (where and what)
   - Database optimization (indexing, sharding)
   - Async processing (queues)
   - CDN for static content

3. Resilience Patterns
   - Circuit breakers
   - Retries with exponential backoff
   - Rate limiting
   - Bulkheads
```

#### **Phase 5: Trade-offs (Alternatives & Justification)**
```
1. Discuss Alternatives
   - SQL vs NoSQL
   - Monolith vs Microservices
   - Push vs Pull
   - Sync vs Async

2. Justify Choices
   - Why this database?
   - Why this caching strategy?
   - Why this consistency level?

3. Address Concerns
   - Single points of failure
   - Data loss scenarios
   - Scaling limitations
```

### Interview-Specific Guidance

#### **The Interview Framework**

**1. Clarify Requirements (5 minutes)**
- "What are the core features we need to support?"
- "How many users do we expect?"
- "What's our latency requirement?"
- "Do we need strong or eventual consistency?"
- "Any specific constraints (budget, geography)?"

**2. High-Level Design (10 minutes)**
- Draw box diagram: Client → Load Balancer → App Servers → Databases
- Define API endpoints
- Sketch data model
- Discuss data flow

**3. Deep Dive (20 minutes)**
- Pick 2-3 interesting components
- Discuss trade-offs
- Optimize bottlenecks
- Add caching, sharding, etc.
- Discuss failure scenarios

**4. Wrap-up (5 minutes)**
- Address monitoring and alerting
- Discuss scaling strategies
- Mention security considerations
- Talk about metrics that matter

#### **Common Interview Questions & Approaches**

**Social Media Feed (Twitter, Instagram)**
- Focus: Fan-out, caching, real-time updates
- Key: Push vs pull model, cache warming, ranking algorithms

**Video Streaming (YouTube, Netflix)**
- Focus: CDN, adaptive bitrate, distributed storage
- Key: Video encoding, metadata management, recommendation system

**Ride Sharing (Uber, Lyft)**
- Focus: Geo-spatial indexing, real-time matching, ETA calculation
- Key: Location updates, surge pricing, driver matching

**Messaging (WhatsApp, Telegram)**
- Focus: WebSockets, message delivery, end-to-end encryption
- Key: Online presence, message queues, read receipts

**E-commerce (Amazon)**
- Focus: Inventory management, payment processing, search
- Key: Transactions, consistency, recommendation engine

**URL Shortener (bit.ly)**
- Focus: ID generation, redirection, analytics
- Key: Base62 encoding, database choice, caching

#### **Red Flags to Avoid**

❌ Jumping to solution without clarifying requirements  
❌ Ignoring scale/constraints  
❌ Not discussing trade-offs  
❌ Overengineering for a simple problem  
❌ Underengineering for a complex problem  
❌ Forgetting about monitoring/logging  
❌ Not handling failure scenarios  
❌ Ignoring security concerns  

#### **Green Flags to Exhibit**

✅ Ask clarifying questions  
✅ State assumptions explicitly  
✅ Think out loud  
✅ Consider multiple approaches  
✅ Discuss trade-offs honestly  
✅ Know when to use each pattern  
✅ Understand the "why" behind choices  
✅ Show breadth AND depth  

### The Path to Mastery

**Level 1: Novice**
- Understand basic patterns (client-server, request-response)
- Know common technologies (SQL, REST, HTTP)
- Can design simple CRUD applications

**Level 2: Intermediate**
- Understand scaling strategies (vertical, horizontal)
- Know caching and database optimization
- Can design medium-complexity systems (e-commerce, blog)

**Level 3: Advanced**
- Understand distributed systems deeply
- Know consistency models and trade-offs
- Can design complex systems (Netflix, Uber)
- Familiar with advanced patterns (CQRS, event sourcing)

**Level 4: Expert**
- Internalize all trade-offs intuitively
- Design for unprecedented scale
- Innovate new patterns for novel problems
- Mentor others effectively

**Level 5: Master**
- See patterns across domains
- Predict failure modes before they occur
- Balance technical excellence with business value
- Shape industry best practices

### The Journey Continues

System design is not a destination—it's a continuous journey of learning, adapting, and improving. Technologies change, patterns evolve, but the fundamental principles remain:

- **Understand the problem** deeply before solving it
- **Choose appropriate tools** for the context
- **Balance competing forces** through principled trade-offs
- **Build for reality** (failure, change, growth)
- **Never stop learning** from successes and failures

Remember: The best system designer is not the one who knows all the answers, but the one who asks the right questions, understands the trade-offs, and makes informed decisions that balance technical excellence with business value and human factors.

**Final Wisdom**: Every system you design is a reflection of your understanding at that moment. Embrace mistakes as learning opportunities, stay humble in the face of complexity, and always remember that you're building systems to serve people, not the other way around.

---

*"There are no solutions. There are only trade-offs."* - Thomas Sowell

*"Make it work, make it right, make it fast."* - Kent Beck

*"Premature optimization is the root of all evil."* - Donald Knuth

*"You can't improve what you don't measure."* - Peter Drucker

*"Hope is not a strategy."* - Traditional Engineering Wisdom