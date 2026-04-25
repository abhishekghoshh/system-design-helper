# Back-of-the-Envelope Calculations
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

---

# Back of Envelope Calculation


## Youtube

- [Back of Envelope Calculation - System Design Concept](https://www.youtube.com/watch?v=DwqTon7ZS_s)
- [8. Back-Of-The-Envelope Estimation for System Design Interview | Capacity Planning of Facebook | HLD](https://www.youtube.com/watch?v=WZjSFNPS9Lo)


## Websites

- [Back-of-the-envelope Estimation](https://bytebytego.com/courses/system-design-interview/back-of-the-envelope-estimation)



## Theory

Back of envelope calculation is a technique used to quickly estimate values and check the feasibility of a system design. It involves making reasonable approximations and simplifying assumptions to get rough, order-of-magnitude answers.

Some common approximations:

- **Seconds in a day:**  
    $24 \times 60 \times 60 = 86,400 \approx 100,000$ (1 Lakh)

- **Bytes and Bits:**  
    $1$ Byte $= 8$ bits (sometimes approximated as $10$ bits for easier calculations)

These quick calculations help engineers estimate storage, bandwidth, or processing requirements without needing precise numbers. The goal is to validate ideas and catch obvious issues early in the design process.
