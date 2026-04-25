# Sharding (Horizontal Partitioning)
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

# Vertical Partitioning
Splitting table columns across multiple tables/databases.

**Example:**
```
Users table → Users (id, name, email) + UserProfiles (user_id, bio, avatar)
```

**Benefits:**
- Separate frequently vs rarely accessed data
- Different access patterns
- Reduce I/O
