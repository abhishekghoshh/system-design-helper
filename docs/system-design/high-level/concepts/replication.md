# Replication

## Blogs and websites


## Medium


## Youtube


## Theory

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
