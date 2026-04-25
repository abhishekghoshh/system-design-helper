# Availability & Reliability

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

# Single Point of Failure (SPOF)
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
