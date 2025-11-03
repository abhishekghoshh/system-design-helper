# Consistent hashing

## Youtube

- [Consistent Hashing - System Design](https://www.youtube.com/watch?v=IC5Y1EE-aj4)

- [6. Consistent Hashing in Hindi with Example | System Design - Consistent Hashing | High Level design](https://www.youtube.com/watch?v=jqUNbqfsnuw)
- [Consistent Hashing (English Dubbed) | Better with 1.25x playback speed](https://www.youtube.com/watch?v=NHvGbXB46qU)


## Website

- [Design Consistent Hashing](https://bytebytego.com/courses/system-design-interview/design-consistent-hashing)
- [Consistent Hashing Explained](https://bytebytego.com/guides/consistent-hashing/)


## Theory

### Consistent Hashing: Detailed Notes

#### 1. Understanding Hash Functions

A hash function takes an input and maps it to a specific output.  
It is commonly used for distributing data efficiently in load balancing, caching, and sharding.

#### 2. Normal Hashing (Modulo-Based Hashing)

**How it works:**  
Given N servers, data is assigned using:  
`Server Index = Hash(input) mod N`

**Example:**  
If N = 3 servers and input is X:  
`Server Index = Hash(X) mod 3`  
The result determines which server handles the request.

**Challenges:**  
When a new server is added, the modulo changes to (N+1).  
This causes cache misses because data previously mapped to a server may now map to a different one, requiring rebalancing.

#### 3. Problem of Rebalancing

Rebalancing means redistributing data when servers are added or removed.  
With normal hashing, most data must be reassigned.  
**Consistent Hashing** minimizes rebalancing.

#### 4. Introduction to Consistent Hashing

The goal is to minimize the number of keys (data) that need reassignment when a server is added or removed.  
In a well-designed system, only about `1/N` of the total data needs to be reassigned.

**Key Properties:**

- **Minimal Rebalancing:**  
    Only `1/N × (Total Number of Records)` needs reassignment when servers change, where N is the number of servers.
- **Dynamic Scaling:**  
    Suitable for environments where servers are frequently added or removed.  
    Ideal for load balancing and database sharding.

#### 5. How Consistent Hashing Works

- **Virtual Ring Structure:**  
    Servers and data are arranged on a circular (virtual) hash ring (e.g., a ring with 12 positions).  
    Each server is mapped to specific points on the ring.
- **Data Assignment:**  
    A key is mapped to a position on the ring and assigned to the next available server in a clockwise direction.
- **Adding/Removing Servers:**  
    A new server takes over responsibility for a small portion of the ring.  
    Only the affected portion of data is reassigned.

#### 6. Virtual Nodes in Consistent Hashing

**Issue:** Uneven data distribution if servers are not evenly spaced.  
**Solution:** Use virtual nodes—each server is mapped to multiple points on the ring, ensuring balanced distribution.

#### 7. Use Cases

- **Load Balancing:**  
    Distributes requests evenly across servers, minimizing disruption when scaling.
- **Distributed Caching:**  
    Used in systems like Redis and Memcached to efficiently map data to cache nodes and prevent frequent cache misses.
- **Database Sharding:**  
    Enables dynamic assignment of data to different database partitions for horizontal scaling.
