# Scalability & Performance

## Blogs and websites


## Medium

- [How I Redesigned The Backend To Quickly Handle Millions Of Reads (And Writes)](https://blog.bitsrc.io/how-i-redesigned-the-backend-to-quickly-handle-millions-of-reads-and-writes-58cfe989e6f8)
- [Horizontal vs Vertical Scaling: Scalability (System Design)](https://medium.com/@ayush_mittal/horizontal-vs-vertical-scaling-scalability-system-design-d10658b7f94e)

## Youtube


## Theory

Scalability is the ability of a system to handle a growing amount of work by adding resources. Performance is how well the system responds under a given load. Together they determine whether your system can serve 100 users or 100 million.

**The Core Question:** If traffic doubles tomorrow, does your system handle it gracefully — or does it fall over?

**Vertical vs Horizontal Scaling:**
```
Vertical Scaling (Scale Up):
  Small Server → Bigger Server (more CPU, RAM, SSD)
  ✓ Simple, no code changes
  ✗ Hard limit (biggest machine available)
  ✗ Single point of failure
  ✗ Exponentially expensive

Horizontal Scaling (Scale Out):
  1 Server → 10 Servers → 100 Servers
  ✓ Virtually unlimited
  ✓ Fault tolerant (one fails, others continue)
  ✓ Cost-effective (commodity hardware)
  ✗ Requires stateless design
  ✗ Distributed system complexity
```

**The Performance Optimization Hierarchy:**
Optimize in this order — each level has the highest ROI at the top:

1. **Algorithm & Data Structure**: O(n²) → O(n log n) is the biggest win possible
2. **Database Queries**: Add indexes, avoid N+1 queries, optimize slow queries
3. **Caching**: Reduce repeated work (Redis, CDN, browser cache)
4. **Concurrency**: Async I/O, connection pooling, parallel processing
5. **Infrastructure**: Load balancing, auto-scaling, CDN
6. **Hardware**: Vertical scaling as a last resort

---

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
