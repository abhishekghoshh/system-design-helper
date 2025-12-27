# Scaling to One Million



## Youtube

- [5. Scale from ZERO to MILLION Users (Hindi) | System design interview: Scale to 1million users](https://www.youtube.com/watch?v=rExh5cPMZcI)
- [15. Design High Availability & Resilience System, HLD | Active Passive & Active Active Architecture](https://www.youtube.com/watch?v=iL7_8TmrePM)




## Theory

### Introduction

- This video is part of a series on system design concepts, focusing on scaling from 0 to 1 million users.
- It covers concepts such as sharding, horizontal and vertical scaling, load balancing, caching, and messaging queues.

### Steps for Scaling

1. **Single Server**
    - Basic setup with a single server handling the application, database, and client.
    - Suitable for the initial stage with zero users.

2. **Application and Database Separation**
    - Introduces a separate application server layer for business logic.
    - Database server manages data storage and retrieval.
    - Allows independent scaling of application and database.

3. **Load Balancing and Multiple Application Servers**
    - Adds a load balancer to distribute incoming requests across multiple application servers.
    - Load balancer enhances security and privacy.
    - Efficiently handles increased traffic by distributing workload.

4. **Database Replication**
    - Implements master-slave configuration for the database.
    - Master database handles write operations; slave databases handle read operations.
    - Improves performance and provides redundancy in case of failure.

5. **Caching**
    - Adds a caching layer to store frequently accessed data in memory.
    - Application server checks cache before accessing the database.
    - Reduces database load and improves response time.
    - Uses time-to-live (TTL) to manage cache expiry.

6. **Content Delivery Network (CDN)**
    - Uses a distributed network of servers to cache static content closer to users.
    - Reduces latency and improves performance for global users.
    - Handles requests for static content (images, videos, JavaScript).
    - On cache miss, CDN checks neighboring CDN nodes before querying the origin database.

7. **Multiple Data Centers**
    - Distributes application and database across multiple data centers.
    - Reduces load on individual centers and improves reliability.
    - Enables geographically distributed access with minimal latency.
    - Load balancer routes requests based on user location.

8. **Messaging Queues**
    - Uses messaging queues for asynchronous tasks (e.g., notifications, emails).
    - Decouples tasks from the main application flow.
    - Improves performance and reliability for high-volume tasks.
    - Examples: RabbitMQ, Kafka.

9. **Database Scaling**
    - **Vertical Scaling:** Increase the capacity of existing database servers by adding more CPU, RAM, or storage. This approach is straightforward but eventually limited by hardware constraints and cost.
    - **Horizontal Scaling / Data Sharding:** Distribute the database across multiple servers or shards to handle larger datasets and higher traffic.
        - **Horizontal Sharding:** Split data by rows, such as dividing users by user ID ranges. Each shard contains a subset of the data, allowing parallel processing and improved scalability.
        - **Vertical Sharding:** Split data by columns, separating different types of data (e.g., user profiles vs. transactions) into different databases or tables. This can optimize performance for specific queries.
    - Sharding strategies help reduce bottlenecks, improve fault tolerance, and enable scaling beyond the limits of a single server.
    - Proper shard key selection and balancing are critical to avoid hotspots and ensure even distribution of data and workload.