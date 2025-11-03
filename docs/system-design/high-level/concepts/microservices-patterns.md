# Microservices patterns



## Youtube

- [3. Microservices Design Patterns | Part1: Introduction and Decomposition Pattern | HLD](https://www.youtube.com/watch?v=l1OCmsBnQ3g)
- [4. SAGA Pattern | Strangler Pattern | CQRS | Microservices Design Patterns | System Design](https://www.youtube.com/watch?v=qGlUKtjqaEQ)




## Theory

### Introduction - Part 1

- This is part 3 of the video series on high-level design.
- The previous two videos have already covered earlier topics.
- This part covers:
    - Monolithic vs. microservices architectures
    - Key microservices patterns
    - Notes that this topic can lead to around 15 interview questions

### Disadvantages of Monolithic Architecture

- **Tight Coupling**
    - Changing one line can impact other components.
    - Requires testing and deploying the entire application for a single change.
- **Difficult to Scale**
    - Scaling one component requires scaling the entire application.
- **Expensive Deployments and Rollbacks**
    - Redeployment of the whole application is needed for small changes.
- **Large Codebase**
    - All code resides in a single application.
    - The codebase grows large over time, making changes and impact analysis difficult.

### Why Microservices?

- Designed to overcome the disadvantages of monolithic architectures.
- Splits a large application into smaller, independent services.

### Advantages of Microservices

- Better separation of concerns
- Loose coupling between services
- Independent deployment of services
- Easier to scale specific services
- Faster release cycles

### Disadvantages of Microservices

- Defining proper service boundaries and decomposition is challenging.
- Inter-service communication is complex:
    - Requires monitoring calls across services
    - Needs robust failure handling
- Distributed transaction management is difficult, especially across multiple databases.

### Microservices Design Phases

- Decomposition patterns
- Database patterns
- Communication patterns
- Integration patterns
- Deployment patterns
- Cross-cutting concerns (e.g., monitoring, logging)

### Decomposition Patterns

- **By Business Capability**
    - Split based on business functions (e.g., order management, inventory).
- **By Subdomain (Domain-Driven Design)**
    - Divide large domains into multiple services (e.g., splitting the payment domain).

---

### Introduction - Part 2

- This video continues from Part 1, which discussed the "Decompose by Medium Position Pattern".
- Focuses on three important patterns:
    - **Strangler Pattern:** Used for refactoring a monolithic service into microservices.
    - **Saga Pattern:** Addresses distributed transactions across multiple databases.
    - **CQRS (Command Query Responsibility Segregation):** Separates command (write) and query (read) operations for improved performance and scalability.

### Strangler Pattern

- **Purpose:** Gradually refactor a monolithic application into microservices.
- **How it Works:**
    - Introduce a controller to handle incoming requests.
    - Initially, the controller forwards all traffic to the monolithic application.
    - Gradually extract specific functionalities into microservices, updating the controller to route relevant traffic.
    - Over time, more traffic is routed to microservices, reducing reliance on the monolith.
- **Advantages:**
    - Minimizes disruption to existing services.
    - Enables a gradual transition to microservices.
- **Example:**
    - In an e-commerce website, the controller initially directs all traffic to the monolith.
    - Gradually, functionalities like order placement, inventory management, and payment processing are moved to microservices.
    - The controller routes more traffic to these microservices, eventually phasing out the monolith.

### Data Management in Microservices

- **Two Approaches:**
    - **Database per Service:** Each microservice has its own dedicated database, promoting autonomy and isolation.
    - **Shared Database:** All microservices share a single database, simplifying data access but introducing complexities.
- **Why Database per Service is Preferred:**
    - **Scalability:** Enables independent scaling of services.
    - **Isolation:** Changes in one service's database do not affect others.
    - **Technology Flexibility:** Each service can choose the most suitable database technology.
- **Advantages of Shared Database:**
    - Easier to perform join queries
    - Supports transactional (ACID) properties
- **Drawbacks of Shared Database:**
    - Performance bottlenecks due to increased contention
    - Complexity in managing dependencies and consistency
    - Limited scalability, as the entire database must be scaled even if only one service needs more resources

### Saga Pattern

- **Purpose:** Manage distributed transactions across multiple databases, ensuring data consistency even if some operations fail.
- **How it Works:**
    - A sequence of local transactions is executed within each participating microservice.
    - Each transaction updates its database and publishes an event.
    - Subsequent transactions listen for these events and proceed accordingly.
    - In case of failure, compensation events are published to undo completed operations and maintain consistency.
- **Types of Sagas:**
    - **Choreography:** Each service manages its own transactions and listens to events from other services.
    - **Orchestration:** A centralized orchestrator manages the transaction flow and compensation logic.
- **Example:**
    - An order processing saga involving order creation, inventory management, and payment processing services.
    - If the payment service fails, compensation events are triggered to cancel the order and update inventory.
- **Advantages:**
    - Ensures data consistency in distributed systems.
    - Provides mechanisms for handling failures and rollbacks.
    - Allows flexibility in service interactions.
- **Disadvantages:**
    - Increased complexity compared to local transactions.
    - Requires careful design and implementation.
- **Interview Question Example:**
    - How would you handle a transaction involving transferring money between two users in a microservices architecture?

### CQRS Pattern

- **Purpose:** Separate read (query) operations from write (command) operations for better performance and scalability.
- **How it Works:**
    - The system maintains separate models for read and write operations.
    - Write operations are performed through commands, updating the write model.
    - Read operations access the read model, which is optimized for fast retrieval.
- **Advantages:**
    - **Performance:** Optimized read models handle queries efficiently.
    - **Scalability:** Read and write models can be scaled independently.
    - **Flexibility:** Allows different data structures and query languages for reads and writes.
- **Example:**
    - In a blog application, write operations use a relational database, while read operations access a denormalized view optimized for fast search.
- **Challenges:**
    - Maintaining consistency between the read and write models.
    - Ensuring the read model is up-to-date with changes in the write model.

