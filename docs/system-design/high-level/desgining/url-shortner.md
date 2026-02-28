# Design Tiny Url or bit.ly



## Youtube

- [How Does a URL Shortener Work?](https://www.youtube.com/watch?v=HHUi8F_qAXM)
- [Tiny URL - System Design Interview Question (URL shortener)](https://www.youtube.com/watch?v=Cg3XIqs_-4c)
- [System Design Interview Question: Design URL Shortener](https://www.youtube.com/watch?v=16d35un5a9Q)

- [TinyURL System Design | URL Shortner System Design Interview Question | Bitly System Design](https://www.youtube.com/watch?v=AVztRY77xxA)
- [7. Design URL Shortening Service like TinyURL | Design URL Shortener | System design interview quest](https://www.youtube.com/watch?v=C7_--hAhiaM)
- [Design a URL Shortener (Bitly) - System Design Interview](https://www.youtube.com/watch?v=qSJAvd5Mgio)



- [Design a URL Shortener (TinyURL, Bit.ly) | Systems Design Questions 3.0 With Ex-Google SWE](https://www.youtube.com/watch?v=xFeWVugaouk)
- [Beginner System Design Interview: Design Bitly w/ a Ex-Meta Staff Engineer](https://www.youtube.com/watch?v=iUU4O1sWtJA)


- [Create a Custom URL Shortener using Node.JS and MongoDB](https://www.youtube.com/watch?v=4WvX9dBjiJo)



## Website

- [Tiny URL (URL Shortener)](https://www.techprep.app/system-design/high-level-design/tiny-url/solution)



## Theory


### Approach 1

- To determine the length of the short url we need to know the traffic
- Save it for next 10 years
- Seconds in a year => 60 * 60 * 24 * 365 = 31.5 Million
- Total years in sec => 31.5 * 10 => 315 Million
- Assumining 1000 write req per second => so at least we need to save 1000 * 315 Million => 315 Billion
- use 0-9,A-Z,a-z meaning in total we have 62 numbers
- 62 ^ 6 is 56 Billion, 62 ^ 7 is 3.5 Trillion, so we will use 7 characters
- Data usages
  - short urls 7 bytes
  - long urls 100 bytes
  - user metadata 500 bytes
  - Total rounding off => 1000 bytes
- Total data usage would be 315 Billion * 1000 bytes => 315 TB of data 
- POST **doman_name/url** for creating the Tiny URLs and GET **doman_name/short_url_id** for getting the long url
  - for POST the response would be simple 201 created or 400 bad request or 409 conflict
  - for GET the response would be either 301 permenantly moved redirection, 302 temporarily moved redirection, 404 not found, 410 gone
- If we are expecting 1000 writes per sec then read could be 10 to 100x of this 
- Here nosql like cassandra is prefferable as we need availabilty and we need to scale
- For database we might need to scale so we will need sharding on short urls
- If we do not use cassandra then we need a master slave architecture with multiple read replicas
- for popular url we need caching to read the long url fast read with TTL and LRU or LFU
- URL shortner algorithm
  - Hash function with first 7 char but it might create collision
  - Auto Increment ID but then might create url predictibilty, hackers may use it for DDos attack
  - custom algorithm
- For url creation we can use these uppoer 2 approaches
  - We would could a proper hash function
    - For every long url we will hash it and take the first 7 letters and then we will check it in database if it is already used or not
    - if it is already used then we will use a predetermied suffix and append it to the short url and will rehash it and again check it to the database
    - but it could potentially impact database 
    - we could use a bloom filter to check if the url is used or not rather than checking it in the DB
    - This approach is little time taking but the URL creation is non deterministic
  - We could something like URL range service or maybe a redis
    - the entire range will be divided into multiple ranges(0-3.5T)
    - At the startup our core service will ask for a range and start assigning short urls to long urls
    - once the url range is about to finish then it will ask for a new range
    - We could loose some ranges if server crashes, but that is fine as our requirement is 315 Billion and we have 3.5 Trillion entries
    - When we get the incremented unique ID then we will do the Base62 encoding to make it alphaneumeric
    - This approach is fast but the URL creation is determinitic
    - This is by far looks promising to me but any other way could also be usefull
- For observability we will save the metrics temporarily in the service to consume some bandwidth, at some interval we will push asynchronusly it to the kafka, and then ultimately it will be stored to the Metrics database
- Carefull consideration
  - Input url validation
  - rate limitting like token bucket
  - Https enabling
- Additional requests
  - If user wants to have custom alias then we could use some thing like a bloom filter or a simple database look up to verify if that already assigned or not
  - also user could supply the expiration time


### Approach 2

- In the previous approach our scale was pretty high
- so the data usage is less than 500 bytes
- write scale is 200-300 per sec
- and total data usage required is less then few dozen of TB then we could use a single postgres server sharding and replication
- A single PostgreSQL server can comfortably handle dozens of terabytes of data and billions of rows, provided it is supported by sufficient hardware (high RAM, fast NVMe I/O). While individual table sizes are limited to 32 TB, the database instance can manage multiple tables
- Citus is a sharding implementation of postgres, we could use this also
- Here we would follow B+ tree based indexing with single leader multiple replicas database, this would be ACID complaince
- We could also use something like LSM(Log-Structured Merge-tree) based solution like cassandra, with that we would find highly available sharded, leaderless db, easy for read, Also we could use region based sharding/replication to serve the user from its closest server
- Again this is a url shortner, we would not need a stong consitency here (use Cassandra), even a single leader solution (use Postgres) could work here too. If the write is down for few hour, that would not destroy the world
- And for popular urls we could use a cache in front of db, a read through caching would work also, but we need a custom implemntation like spring caching