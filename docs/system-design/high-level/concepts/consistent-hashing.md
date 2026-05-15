# Consistent hashing

## Blogs and websites

- [Design Consistent Hashing](https://bytebytego.com/courses/system-design-interview/design-consistent-hashing)
- [Consistent Hashing Explained](https://bytebytego.com/guides/consistent-hashing/)

## Medium


## Youtube

- [Consistent Hashing - System Design](https://www.youtube.com/watch?v=IC5Y1EE-aj4)
- [6. Consistent Hashing in Hindi with Example | System Design - Consistent Hashing | High Level design](https://www.youtube.com/watch?v=jqUNbqfsnuw)

## Theory

### Consistent Hashing: Detailed Notes

---

#### 1. Understanding Hash Functions

A **hash function** is a mathematical function that maps an input (of arbitrary size) to a fixed-size output, called a **hash** or **digest**. Hash functions are the foundation of data distribution in distributed systems.

**Properties of a Good Hash Function:**

| Property | Description |
|---|---|
| **Deterministic** | Same input always produces the same output |
| **Uniform Distribution** | Outputs are evenly spread across the output space |
| **Fast Computation** | Can be computed efficiently for any input |
| **Avalanche Effect** | A small change in input produces a drastically different output |
| **Minimized Collisions** | Different inputs rarely produce the same output |

**Common Hash Functions Used in Distributed Systems:**

| Hash Function | Output Size | Speed | Use Case |
|---|---|---|---|
| MD5 | 128-bit | Fast | Legacy caching (not cryptographically secure) |
| SHA-1 | 160-bit | Moderate | Git commit hashing |
| SHA-256 | 256-bit | Slower | Blockchain, security-critical |
| MurmurHash3 | 32/128-bit | Very Fast | General-purpose hashing in distributed systems |
| xxHash | 32/64/128-bit | Extremely Fast | High-throughput data processing |
| FNV-1a | 32/64-bit | Very Fast | Hash tables, simple lookups |
| CityHash | 64/128-bit | Very Fast | Google internal systems |
| SipHash | 64-bit | Fast | Hash table DoS prevention |

**Example — Hashing in Python:**

```python
import hashlib

def hash_key(key: str) -> int:
    """Hash a string key to an integer using SHA-256."""
    digest = hashlib.sha256(key.encode('utf-8')).hexdigest()
    return int(digest, 16)

# Example
print(hash_key("user:1001"))   # Large integer
print(hash_key("user:1002"))   # Completely different integer
print(hash_key("user:1001"))   # Same as first call — deterministic
```

```java
import java.security.MessageDigest;
import java.math.BigInteger;

public class HashExample {
    public static BigInteger hashKey(String key) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] digest = md.digest(key.getBytes("UTF-8"));
        return new BigInteger(1, digest);
    }

    public static void main(String[] args) throws Exception {
        System.out.println(hashKey("user:1001"));
        System.out.println(hashKey("user:1002"));
    }
}
```

---

#### 2. Normal Hashing (Modulo-Based Hashing)

**How it works:**

Given `N` servers numbered `0` to `N-1`, data is assigned using:

$$\text{Server Index} = \text{Hash}(\text{key}) \mod N$$

**Example with 3 servers:**

```
Hash("key-A") = 1234567  →  1234567 % 3 = 0  →  Server 0
Hash("key-B") = 2345678  →  2345678 % 3 = 2  →  Server 2
Hash("key-C") = 3456789  →  3456789 % 3 = 0  →  Server 0
Hash("key-D") = 4567890  →  4567890 % 3 = 0  →  Server 0
Hash("key-E") = 5678901  →  5678901 % 3 = 0  →  Server 0
```

**Diagram — Modulo-Based Hashing:**

```
                    ┌─────────────┐
                    │ Hash(key)   │
                    │   mod N     │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Server 0 │ │ Server 1 │ │ Server 2 │
        │ key-A    │ │          │ │ key-B    │
        │ key-C    │ │          │ │          │
        │ key-D    │ │          │ │          │
        └──────────┘ └──────────┘ └──────────┘
```

**What happens when we add Server 3 (N becomes 4)?**

```
Hash("key-A") = 1234567  →  1234567 % 4 = 3  →  Server 3  ← MOVED from Server 0!
Hash("key-B") = 2345678  →  2345678 % 4 = 2  →  Server 2  ← Same
Hash("key-C") = 3456789  →  3456789 % 4 = 1  →  Server 1  ← MOVED from Server 0!
Hash("key-D") = 4567890  →  4567890 % 4 = 2  →  Server 2  ← MOVED from Server 0!
Hash("key-E") = 5678901  →  5678901 % 4 = 1  →  Server 1  ← MOVED from Server 0!
```

**4 out of 5 keys moved!** That's 80% remapping. In general, with modulo hashing, when `N` changes to `N+1`, approximately $\frac{N}{N+1}$ of all keys must be reassigned.

**Challenges of Modulo-Based Hashing:**

| Problem | Impact |
|---|---|
| **Massive remapping** | ~80-95% of keys move when adding/removing a server |
| **Cache stampede** | All cache misses hit the database simultaneously |
| **Downtime risk** | Requires coordinated rebalancing across all nodes |
| **Not elastic** | Adding/removing servers is extremely expensive |
| **Thundering herd** | Simultaneous cache rebuilds can overwhelm backends |

---

#### 3. The Rebalancing Problem in Depth

**Rebalancing** is the process of redistributing data (keys) across servers when the set of servers changes. It is the fundamental problem that consistent hashing solves.

**Quantifying the Cost of Rebalancing:**

For `K` keys and `N` servers with modulo hashing:

- **Adding 1 server:** ~$K \times \frac{N}{N+1}$ keys move
- **Removing 1 server:** ~$K \times \frac{N-1}{N}$ keys move

| Servers (N) | Keys (K) | Keys Moved (Add 1 Server) | % Moved |
|---|---|---|---|
| 3 | 1,000,000 | ~750,000 | 75% |
| 10 | 1,000,000 | ~909,091 | 90.9% |
| 100 | 1,000,000 | ~990,099 | 99% |
| 1000 | 1,000,000 | ~999,001 | 99.9% |

The more servers you have, the worse it gets! This is catastrophic for large-scale distributed systems.

**Real-World Impact of Rebalancing:**

```
Timeline of a Naive Rebalancing Event:

T=0s    Server added to cluster
        │
T=0.1s  ┌─────────────────────────────────────┐
        │  90% of cache lookups now miss       │
        │  All misses hit the database         │
        └──────────────┬──────────────────────┘
                       │
T=0.5s  ┌─────────────────────────────────────┐
        │  Database CPU spikes to 100%         │
        │  Query latencies jump from 5ms→500ms │
        └──────────────┬──────────────────────┘
                       │
T=2s    ┌─────────────────────────────────────┐
        │  Database connection pool exhausted  │
        │  Requests start timing out           │
        └──────────────┬──────────────────────┘
                       │
T=5s    ┌─────────────────────────────────────┐
        │  Cascading failure across services   │
        │  OUTAGE                              │
        └─────────────────────────────────────┘
```

**Ideal Rebalancing:**

With consistent hashing, only $\frac{K}{N}$ keys move (where K = total keys, N = total servers). For 1M keys and 10 servers, that's ~100,000 keys instead of ~909,091.

---

#### 4. Introduction to Consistent Hashing

**Consistent hashing** was introduced by **David Karger et al. in 1997** in their paper *"Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web"*.

The core idea: instead of using `hash(key) mod N`, place both **servers** and **keys** on a circular hash space (a **ring**), and each key is served by the nearest server in the clockwise direction.

**Key Properties:**

| Property | Description |
|---|---|
| **Minimal Disruption** | Adding/removing a server only reassigns ~$\frac{1}{N}$ of total keys |
| **Monotonicity** | When new servers are added, keys only move from existing servers to the new one — never between existing servers |
| **Balance** | With virtual nodes, keys are approximately evenly distributed |
| **Spread** | A given key is not stored on too many different servers across views |
| **Load** | No server is responsible for too many keys |
| **Smoothness** | As servers are added, the load shifts smoothly with minimal disruption |

**Mathematical Guarantee:**

When adding a server to a ring with `N` existing servers:

$$\text{Expected keys moved} = \frac{K}{N+1}$$

where `K` is the total number of keys. Compare this with modulo hashing where $\frac{K \times N}{N+1}$ keys move.

**Comparison:**

| Metric | Modulo Hashing | Consistent Hashing |
|---|---|---|
| Keys remapped on add/remove | ~$\frac{N}{N+1} \times K$ | ~$\frac{K}{N+1}$ |
| With 10 servers, 1M keys | ~909K moved | ~91K moved |
| With 100 servers, 1M keys | ~990K moved | ~10K moved |
| Complexity to find server | O(1) | O(log N) with binary search |
| Even distribution guarantee | Yes (by design) | Needs virtual nodes |

---

#### 5. How Consistent Hashing Works — Step by Step

**Step 1: Create the Hash Ring**

Map the hash output space to a circular ring. If using a hash function with output range `[0, 2^32 - 1]`, the ring has positions from `0` to `2^32 - 1`, where position `2^32` wraps around to position `0`.

```
                        0
                    ┌───●───┐
                   /         \
                  /           \
          2^30  ●              ● 2^30 × 3
                 \            /
                  \          /
                   \        /
                    └───●──┘
                      2^31
```

**Step 2: Place Servers on the Ring**

Hash each server's identifier (IP address, hostname, etc.) to determine its position on the ring.

```
Hash("Server-A") = 15    →  Position 15 on ring
Hash("Server-B") = 45    →  Position 45 on ring
Hash("Server-C") = 80    →  Position 80 on ring
```

```
                     0
                 ┌───────┐
                /    15    \
               /   ●(S-A)  \
              │              │
         80 ● │              │ ● 45
          (S-C)              (S-B)
              │              │
               \            /
                \          /
                 └────────┘
```

**Step 3: Assign Keys to Servers**

Each key is hashed and placed on the ring. It is then assigned to the **first server encountered moving clockwise** from its position.

```
Hash("key1") = 10  →  Next server clockwise = Server-A (15)  ✓
Hash("key2") = 20  →  Next server clockwise = Server-B (45)  ✓
Hash("key3") = 50  →  Next server clockwise = Server-C (80)  ✓
Hash("key4") = 85  →  Next server clockwise = Server-A (15)  ✓ (wraps around!)
Hash("key5") = 42  →  Next server clockwise = Server-B (45)  ✓
```

```
                       0
                  ┌──────────┐
                 / 10(key1)   \
                /  ↓           \
               / 15●(S-A)      \
              │   20(key2)→     │
        85 ○──┤   ↓             │
       (key4) │              45●(S-B)
              │   42(key5)→  ↗  │
         80●──┤  (S-C)         │
        (S-C) │↗                │
               \ 50(key3)      /
                \             /
                 └───────────┘

    Assignments:
    ┌─────────┬──────────┬──────────────────────┐
    │ Key     │ Position │ Assigned To           │
    ├─────────┼──────────┼──────────────────────┤
    │ key1    │ 10       │ Server-A (pos 15)     │
    │ key2    │ 20       │ Server-B (pos 45)     │
    │ key5    │ 42       │ Server-B (pos 45)     │
    │ key3    │ 50       │ Server-C (pos 80)     │
    │ key4    │ 85       │ Server-A (pos 15)     │
    └─────────┴──────────┴──────────────────────┘
```

**Step 4: Adding a New Server**

When `Server-D` is added at position `30`, only the keys between `Server-A (15)` and `Server-D (30)` need to move.

```
Before:                              After:
key2(20) → Server-B(45)             key2(20) → Server-D(30) ← MOVED
key5(42) → Server-B(45)             key5(42) → Server-B(45) ← Same

Only key2 moves! (from Server-B to Server-D)
All other keys stay exactly where they are.
```

```
                       0
                  ┌──────────┐
                 / 10(key1)   \
                /  ↓           \
               / 15●(S-A)      \
              │   20(key2)      │
              │   ↓             │
              │  30●(S-D) ←NEW  │
              │                 │
              │   42(key5)→  45●(S-B)
         80●──┤                 │
        (S-C) │                 │
               \ 50(key3)      /
                \   85(key4)  /
                 └───────────┘
```

**Step 5: Removing a Server**

When `Server-B (45)` is removed, only the keys assigned to `Server-B` need to be reassigned to the next server clockwise.

```
key2(20) was on Server-B → Now goes to Server-C(80)
key5(42) was on Server-B → Now goes to Server-C(80)

All other keys remain untouched!
```

---

#### 6. Virtual Nodes (vNodes) — Solving the Balance Problem

**The Problem Without Virtual Nodes:**

With only physical nodes on the ring, the distribution of keys can be extremely uneven, especially with a small number of servers.

```
Unbalanced Ring (3 servers, poor hash placement):

                     0
                ┌────────┐
               /  ●S-A(5) \
              /   ●S-B(10) \
             │               │
             │               │
             │               │
              \             /
               \ ●S-C(350)/
                └────────┘

  Server-A handles: positions 351-5    = ~15 positions (1.5%)
  Server-B handles: positions 6-10     = ~5 positions  (0.5%)
  Server-C handles: positions 11-350   = ~340 positions (98%)
  
  ⚠️ Server-C is massively overloaded!
```

**The Solution — Virtual Nodes:**

Instead of placing each server at a single point on the ring, place it at **multiple points** using different hash functions or suffixes.

```
Physical Server → Multiple Virtual Nodes:

Server-A → Hash("Server-A#1") = 15
            Hash("Server-A#2") = 120
            Hash("Server-A#3") = 250

Server-B → Hash("Server-B#1") = 45
            Hash("Server-B#2") = 180
            Hash("Server-B#3") = 310

Server-C → Hash("Server-C#1") = 80
            Hash("Server-C#2") = 210
            Hash("Server-C#3") = 350
```

```
Ring with Virtual Nodes (3 servers × 3 vnodes each = 9 points):

                         0
                    ┌────────┐
                   / A1(15)   \
                  /  B1(45)    \
                 / C1(80)       \
                │ A2(120)        │
                │  B2(180)       │
                │   C2(210)      │
                 \ A3(250)      /
                  \ B3(310)    /
                   \ C3(350)  /
                    └────────┘

  Now each server handles ~33% of the ring!
  Much more balanced distribution.
```

**Impact of Virtual Node Count on Balance:**

| Virtual Nodes per Server | Standard Deviation of Load | Balance Quality |
|---|---|---|
| 1 | ~77% | Very Poor |
| 10 | ~25% | Poor |
| 50 | ~11% | Acceptable |
| 100 | ~7% | Good |
| 150 | ~6% | Very Good |
| 200+ | ~5% | Excellent |

**Trade-offs of Virtual Nodes:**

| Advantage | Disadvantage |
|---|---|
| Better load balance | More memory to store ring positions |
| Smoother scaling | Slightly higher lookup time (more points to search) |
| Handles heterogeneous hardware | More complex implementation |
| Finer-grained rebalancing | Ring metadata becomes larger |

**Weighted Virtual Nodes for Heterogeneous Hardware:**

Different servers can have different numbers of virtual nodes based on their capacity:

```
Server-A (16 GB RAM, 8 cores)  → 200 virtual nodes
Server-B (8 GB RAM, 4 cores)   → 100 virtual nodes  
Server-C (32 GB RAM, 16 cores) → 400 virtual nodes

Server-C handles ~4x the load of Server-B — matching its capacity!
```

---

#### 7. Complete Implementation

**Python Implementation:**

```python
import hashlib
from bisect import bisect_right, insort
from collections import defaultdict
from typing import Optional


class ConsistentHashRing:
    """
    A consistent hash ring implementation with virtual nodes.

    Each physical node is mapped to multiple virtual nodes on the ring
    to ensure even distribution of keys.
    """

    def __init__(self, num_virtual_nodes: int = 150):
        self.num_virtual_nodes = num_virtual_nodes
        self.ring: dict[int, str] = {}       # hash_value → physical_node
        self.sorted_keys: list[int] = []     # sorted hash positions
        self.nodes: set[str] = set()         # physical nodes

    def _hash(self, key: str) -> int:
        """Generate a consistent hash for a key using SHA-256."""
        digest = hashlib.sha256(key.encode('utf-8')).hexdigest()
        return int(digest, 16) % (2**32)

    def add_node(self, node: str) -> list[str]:
        """
        Add a physical node to the ring with virtual nodes.
        Returns list of keys that would need to be migrated (conceptual).
        """
        if node in self.nodes:
            return []

        self.nodes.add(node)

        for i in range(self.num_virtual_nodes):
            virtual_key = f"{node}#vnode{i}"
            hash_val = self._hash(virtual_key)
            self.ring[hash_val] = node
            insort(self.sorted_keys, hash_val)

        return []

    def remove_node(self, node: str) -> None:
        """Remove a physical node and all its virtual nodes from the ring."""
        if node not in self.nodes:
            return

        self.nodes.discard(node)

        keys_to_remove = []
        for hash_val, mapped_node in self.ring.items():
            if mapped_node == node:
                keys_to_remove.append(hash_val)

        for key in keys_to_remove:
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key: str) -> Optional[str]:
        """
        Find the server responsible for a given key.

        The key is hashed and the first server found clockwise
        on the ring is returned.
        """
        if not self.sorted_keys:
            return None

        hash_val = self._hash(key)

        # Binary search for the first server clockwise
        idx = bisect_right(self.sorted_keys, hash_val)

        # Wrap around to the beginning of the ring
        if idx == len(self.sorted_keys):
            idx = 0

        return self.ring[self.sorted_keys[idx]]

    def get_distribution(self, keys: list[str]) -> dict[str, int]:
        """Show how keys are distributed across nodes."""
        distribution: dict[str, int] = defaultdict(int)
        for key in keys:
            node = self.get_node(key)
            if node:
                distribution[node] += 1
        return dict(distribution)


# --- Demo ---
if __name__ == "__main__":
    ring = ConsistentHashRing(num_virtual_nodes=150)

    # Add servers
    ring.add_node("server-1")
    ring.add_node("server-2")
    ring.add_node("server-3")

    # Generate sample keys
    keys = [f"user:{i}" for i in range(10000)]

    # Check distribution
    dist = ring.get_distribution(keys)
    print("Distribution with 3 servers:")
    for node, count in sorted(dist.items()):
        print(f"  {node}: {count} keys ({count/100:.1f}%)")

    # Lookup specific keys
    print(f"\n'session:abc' → {ring.get_node('session:abc')}")
    print(f"'session:xyz' → {ring.get_node('session:xyz')}")

    # Add a new server — minimal redistribution
    print("\n--- Adding server-4 ---")
    ring.add_node("server-4")
    new_dist = ring.get_distribution(keys)
    print("Distribution with 4 servers:")
    for node, count in sorted(new_dist.items()):
        print(f"  {node}: {count} keys ({count/100:.1f}%)")

    # Count how many keys actually moved
    moved = 0
    for key in keys:
        old = None
        # Simulate: remove server-4, check old assignment
        ring_temp = ConsistentHashRing(num_virtual_nodes=150)
        ring_temp.add_node("server-1")
        ring_temp.add_node("server-2")
        ring_temp.add_node("server-3")
        old = ring_temp.get_node(key)
        new = ring.get_node(key)
        if old != new:
            moved += 1
    print(f"\nKeys moved after adding server-4: {moved}/{len(keys)} ({moved/100:.1f}%)")
```

**Java Implementation:**

```java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class ConsistentHashRing<T> {

    private final int numVirtualNodes;
    private final TreeMap<Long, T> ring = new TreeMap<>();
    private final Set<T> physicalNodes = new HashSet<>();

    public ConsistentHashRing(int numVirtualNodes) {
        this.numVirtualNodes = numVirtualNodes;
    }

    private long hash(String key) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] digest = md.digest(key.getBytes(StandardCharsets.UTF_8));
            // Use first 8 bytes for a long hash
            long h = 0;
            for (int i = 0; i < 8; i++) {
                h = (h << 8) | (digest[i] & 0xFF);
            }
            return h & Long.MAX_VALUE; // Ensure positive
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Add a physical node with its virtual nodes to the ring.
     */
    public void addNode(T node) {
        if (physicalNodes.contains(node)) return;
        physicalNodes.add(node);
        for (int i = 0; i < numVirtualNodes; i++) {
            long hashVal = hash(node.toString() + "#vnode" + i);
            ring.put(hashVal, node);
        }
    }

    /**
     * Remove a physical node and all its virtual nodes.
     */
    public void removeNode(T node) {
        if (!physicalNodes.contains(node)) return;
        physicalNodes.remove(node);
        for (int i = 0; i < numVirtualNodes; i++) {
            long hashVal = hash(node.toString() + "#vnode" + i);
            ring.remove(hashVal);
        }
    }

    /**
     * Find the server responsible for a given key.
     * Uses ceiling entry for O(log N) clockwise lookup.
     */
    public T getNode(String key) {
        if (ring.isEmpty()) return null;

        long hashVal = hash(key);

        // Find the first node clockwise (>=) on the ring
        Map.Entry<Long, T> entry = ring.ceilingEntry(hashVal);

        // Wrap around if we've gone past the highest point
        if (entry == null) {
            entry = ring.firstEntry();
        }

        return entry.getValue();
    }

    /**
     * Get distribution of keys across nodes.
     */
    public Map<T, Integer> getDistribution(List<String> keys) {
        Map<T, Integer> dist = new HashMap<>();
        for (String key : keys) {
            T node = getNode(key);
            dist.merge(node, 1, Integer::sum);
        }
        return dist;
    }

    public int getRingSize() {
        return ring.size();
    }

    public static void main(String[] args) {
        ConsistentHashRing<String> ring = new ConsistentHashRing<>(150);

        ring.addNode("server-1");
        ring.addNode("server-2");
        ring.addNode("server-3");

        List<String> keys = new ArrayList<>();
        for (int i = 0; i < 10000; i++) {
            keys.add("user:" + i);
        }

        Map<String, Integer> dist = ring.getDistribution(keys);
        System.out.println("Distribution with 3 servers:");
        dist.entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .forEach(e -> System.out.printf("  %s: %d keys (%.1f%%)%n",
                e.getKey(), e.getValue(), e.getValue() / 100.0));

        System.out.println("\nLookup 'session:abc' → " + ring.getNode("session:abc"));

        ring.addNode("server-4");
        Map<String, Integer> newDist = ring.getDistribution(keys);
        System.out.println("\nDistribution with 4 servers:");
        newDist.entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .forEach(e -> System.out.printf("  %s: %d keys (%.1f%%)%n",
                e.getKey(), e.getValue(), e.getValue() / 100.0));
    }
}
```

**Go Implementation:**

```go
package consistenthash

import (
	"crypto/sha256"
	"encoding/binary"
	"fmt"
	"sort"
	"sync"
)

// Ring represents a consistent hash ring with virtual nodes.
type Ring struct {
	mu              sync.RWMutex
	numVirtualNodes int
	ring            map[uint32]string // hash → physical node
	sortedKeys      []uint32          // sorted hash positions
	nodes           map[string]bool   // physical nodes
}

// New creates a consistent hash ring with the given number of virtual nodes.
func New(numVirtualNodes int) *Ring {
	return &Ring{
		numVirtualNodes: numVirtualNodes,
		ring:            make(map[uint32]string),
		nodes:           make(map[string]bool),
	}
}

func (r *Ring) hash(key string) uint32 {
	h := sha256.Sum256([]byte(key))
	return binary.BigEndian.Uint32(h[:4])
}

// AddNode adds a physical node with virtual nodes to the ring.
func (r *Ring) AddNode(node string) {
	r.mu.Lock()
	defer r.mu.Unlock()

	if r.nodes[node] {
		return
	}
	r.nodes[node] = true

	for i := 0; i < r.numVirtualNodes; i++ {
		vKey := fmt.Sprintf("%s#vnode%d", node, i)
		h := r.hash(vKey)
		r.ring[h] = node
		r.sortedKeys = append(r.sortedKeys, h)
	}

	sort.Slice(r.sortedKeys, func(i, j int) bool {
		return r.sortedKeys[i] < r.sortedKeys[j]
	})
}

// RemoveNode removes a physical node and all its virtual nodes.
func (r *Ring) RemoveNode(node string) {
	r.mu.Lock()
	defer r.mu.Unlock()

	if !r.nodes[node] {
		return
	}
	delete(r.nodes, node)

	for i := 0; i < r.numVirtualNodes; i++ {
		vKey := fmt.Sprintf("%s#vnode%d", node, i)
		h := r.hash(vKey)
		delete(r.ring, h)
	}

	// Rebuild sorted keys
	r.sortedKeys = r.sortedKeys[:0]
	for h := range r.ring {
		r.sortedKeys = append(r.sortedKeys, h)
	}
	sort.Slice(r.sortedKeys, func(i, j int) bool {
		return r.sortedKeys[i] < r.sortedKeys[j]
	})
}

// GetNode finds the server responsible for a given key using binary search.
func (r *Ring) GetNode(key string) string {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if len(r.sortedKeys) == 0 {
		return ""
	}

	h := r.hash(key)

	// Binary search for the first position >= h
	idx := sort.Search(len(r.sortedKeys), func(i int) bool {
		return r.sortedKeys[i] >= h
	})

	// Wrap around
	if idx == len(r.sortedKeys) {
		idx = 0
	}

	return r.ring[r.sortedKeys[idx]]
}

// GetDistribution returns key count per node.
func (r *Ring) GetDistribution(keys []string) map[string]int {
	dist := make(map[string]int)
	for _, key := range keys {
		node := r.GetNode(key)
		dist[node]++
	}
	return dist
}
```

---

#### 8. Lookup Algorithm — Finding the Right Server

The key operation in consistent hashing is finding which server a key maps to. This is done via **binary search** on the sorted ring positions.

**Algorithm:**

```
FUNCTION find_server(key):
    hash_value = hash(key)
    
    # Binary search for the first ring position >= hash_value
    idx = binary_search(sorted_ring_positions, hash_value)
    
    # If past the end, wrap around to position 0
    IF idx == len(sorted_ring_positions):
        idx = 0
    
    RETURN ring[sorted_ring_positions[idx]]
```

**Time Complexity Analysis:**

| Operation | Time Complexity | Space Complexity |
|---|---|---|
| Lookup (find server for key) | $O(\log(N \times V))$ | — |
| Add node | $O(V \times \log(N \times V))$ | $O(V)$ |
| Remove node | $O(V \times \log(N \times V))$ | — |
| Get all keys for a node | $O(K)$ | $O(K)$ |

Where `N` = number of physical nodes, `V` = virtual nodes per server, `K` = total keys.

**Why Binary Search?**

A linear scan through all ring positions would be $O(N \times V)$. With 100 servers and 150 virtual nodes each, that's 15,000 positions to scan. Binary search brings it down to $\log_2(15000) \approx 14$ steps.

---

#### 9. Replication with Consistent Hashing

In production systems, data is **replicated** across multiple servers for fault tolerance. Consistent hashing naturally supports this.

**Strategy: Replicate to the Next N Clockwise Servers**

For a replication factor of 3, a key is stored on the server it maps to **plus** the next 2 distinct physical servers clockwise on the ring.

```
Ring with Replication Factor = 3:

                       0
                  ┌──────────┐
                 /  A1(15)    \
                /   B1(45)    \
               /   C1(80)     \
              │   A2(120)      │
              │    B2(180)     │
              │     C2(210)    │
               \   A3(250)    /
                \  B3(310)   /
                 \ C3(350)  /
                  └────────┘

key "user:42" hashes to position 30:
  Primary:   Server-B (pos 45)   ← First clockwise
  Replica 1: Server-C (pos 80)   ← Second clockwise (different physical)
  Replica 2: Server-A (pos 120)  ← Third clockwise (different physical)
```

**Implementation — Finding Replica Nodes:**

```python
def get_replicas(self, key: str, num_replicas: int = 3) -> list[str]:
    """
    Get N distinct physical nodes for a key (primary + replicas).
    Walks clockwise on the ring, skipping virtual nodes of
    already-selected physical servers.
    """
    if not self.sorted_keys:
        return []

    hash_val = self._hash(key)
    idx = bisect_right(self.sorted_keys, hash_val)

    replicas = []
    seen_nodes = set()

    for i in range(len(self.sorted_keys)):
        pos = (idx + i) % len(self.sorted_keys)
        node = self.ring[self.sorted_keys[pos]]

        if node not in seen_nodes:
            replicas.append(node)
            seen_nodes.add(node)

        if len(replicas) == num_replicas:
            break

    return replicas
```

```java
public List<T> getReplicas(String key, int numReplicas) {
    if (ring.isEmpty()) return Collections.emptyList();

    long hashVal = hash(key);
    List<T> replicas = new ArrayList<>();
    Set<T> seen = new HashSet<>();

    // Start from the ceiling entry and walk clockwise
    Long current = ring.ceilingKey(hashVal);
    if (current == null) current = ring.firstKey();

    NavigableMap<Long, T> tail = ring.tailMap(current, true);
    for (Map.Entry<Long, T> entry : tail.entrySet()) {
        if (seen.add(entry.getValue())) {
            replicas.add(entry.getValue());
        }
        if (replicas.size() == numReplicas) return replicas;
    }

    // Wrap around from the beginning
    for (Map.Entry<Long, T> entry : ring.entrySet()) {
        if (seen.add(entry.getValue())) {
            replicas.add(entry.getValue());
        }
        if (replicas.size() == numReplicas) return replicas;
    }

    return replicas;
}
```

---

#### 10. Bounded-Load Consistent Hashing

Standard consistent hashing can still produce **hotspots** where one server gets disproportionately more traffic. **Bounded-load consistent hashing** (proposed by Google in 2017) enforces an upper bound on the load any single server can handle.

**The Idea:**

Each server has a capacity limit: $\text{max\_load} = \lceil \frac{\text{avg\_load} \times (1 + \epsilon)}{1} \rceil$

where $\epsilon$ is a small constant (e.g., 0.25). If a server is at capacity, the key overflows to the next server clockwise.

```
Example with ε = 0.25, 4 servers, 100 keys:
  Average load = 25 keys per server
  Max load per server = ceil(25 × 1.25) = 32 keys

  If Server-A already has 32 keys:
    New key that hashes to Server-A → Overflow to Server-B
```

**Implementation Sketch:**

```python
class BoundedLoadConsistentHash(ConsistentHashRing):
    """
    Consistent hashing with bounded load.
    No server handles more than (1 + epsilon) * average_load keys.
    """

    def __init__(self, num_virtual_nodes: int = 150, epsilon: float = 0.25):
        super().__init__(num_virtual_nodes)
        self.epsilon = epsilon
        self.load: dict[str, int] = defaultdict(int)  # current load per node
        self.total_keys = 0

    def _max_load(self) -> int:
        if not self.nodes:
            return 0
        avg = self.total_keys / len(self.nodes)
        return int(avg * (1 + self.epsilon)) + 1

    def get_node_bounded(self, key: str) -> Optional[str]:
        """Find server for key, respecting load bounds."""
        if not self.sorted_keys:
            return None

        hash_val = self._hash(key)
        idx = bisect_right(self.sorted_keys, hash_val)
        max_load = self._max_load()

        for i in range(len(self.sorted_keys)):
            pos = (idx + i) % len(self.sorted_keys)
            node = self.ring[self.sorted_keys[pos]]

            if self.load[node] < max_load:
                self.load[node] += 1
                self.total_keys += 1
                return node

        # Fallback: all servers at capacity (shouldn't happen in normal conditions)
        node = self.ring[self.sorted_keys[idx % len(self.sorted_keys)]]
        self.load[node] += 1
        self.total_keys += 1
        return node
```

---

#### 11. Jump Consistent Hashing

**Jump consistent hash** is an alternative algorithm by Google (Lamping & Veach, 2014) that is simpler, faster, and produces perfectly even distribution — but only works when servers are numbered `0` to `N-1`.

**Properties:**

| Feature | Ring-based | Jump Hash |
|---|---|---|
| Lookup speed | $O(\log N)$ | $O(\log N)$ |
| Memory | $O(N \times V)$ | $O(1)$ |
| Named servers | Yes | No (numeric only) |
| Arbitrary add/remove | Yes | Only add/remove from end |
| Distribution | Good with vnodes | Perfect |
| Implementation | Complex | Very Simple (~5 lines) |

**The Algorithm (remarkably simple):**

```python
def jump_consistent_hash(key: int, num_buckets: int) -> int:
    """
    Jump consistent hash: maps key to bucket in [0, num_buckets).
    O(log N) time, O(1) space, perfect balance.
    """
    b, j = -1, 0
    while j < num_buckets:
        b = j
        key = ((key * 2862933555777941757) + 1) & 0xFFFFFFFFFFFFFFFF
        j = int((b + 1) * (1 << 31) / ((key >> 33) + 1))
    return b
```

```go
func JumpConsistentHash(key uint64, numBuckets int) int {
    var b, j int64
    b, j = -1, 0
    for j < int64(numBuckets) {
        b = j
        key = key*2862933555777941757 + 1
        j = int64(float64(b+1) * (float64(int64(1)<<31) / float64((key>>33)+1)))
    }
    return int(b)
}
```

```java
public static int jumpConsistentHash(long key, int numBuckets) {
    long b = -1, j = 0;
    while (j < numBuckets) {
        b = j;
        key = key * 2862933555777941757L + 1;
        j = (long) ((b + 1) * (Long.divideUnsigned(1L << 31, (key >>> 33) + 1)));
    }
    return (int) b;
}
```

**When to Use Jump Hash:**

- Servers are numbered sequentially (0, 1, 2, ...)
- You only add/remove servers from the end of the list
- You need perfect balance without virtual nodes
- Memory efficiency is critical (e.g., embedded systems)

---

#### 12. Rendezvous Hashing (Highest Random Weight)

**Rendezvous hashing** is another alternative where each key computes a hash with **every** server, and the server with the highest hash wins.

```
For key "user:42":
  score("user:42", "server-A") = hash("user:42" + "server-A") = 847293
  score("user:42", "server-B") = hash("user:42" + "server-B") = 291047
  score("user:42", "server-C") = hash("user:42" + "server-C") = 993041  ← HIGHEST
  
  → "user:42" is assigned to Server-C
```

**Implementation:**

```python
def rendezvous_hash(key: str, servers: list[str]) -> str:
    """
    Rendezvous hashing: key goes to the server with 
    the highest combined hash score.
    """
    best_server = None
    best_score = -1

    for server in servers:
        combined = f"{key}:{server}"
        score = int(hashlib.sha256(combined.encode()).hexdigest(), 16)
        if score > best_score:
            best_score = score
            best_server = server

    return best_server
```

**Comparison with Ring-Based Consistent Hashing:**

| Feature | Ring-Based | Rendezvous |
|---|---|---|
| Lookup time | $O(\log(N \times V))$ | $O(N)$ |
| Memory | $O(N \times V)$ | $O(N)$ |
| Balance | Good with vnodes | Naturally perfect |
| Add/remove server | Only ~$\frac{K}{N}$ keys move | Only ~$\frac{K}{N}$ keys move |
| Implementation | Moderate | Very simple |
| Best for | Large N (100+ servers) | Small N (<50 servers) |

---

#### 13. Data Migration During Scaling

When nodes are added or removed, some keys must move. A production system needs a migration strategy.

**Migration Flow When Adding a Node:**

```
Step 1: Add new node to the ring (with virtual nodes)

Step 2: Identify affected key ranges
         ┌──────────────────────────────────────────────┐
         │ For each virtual node V_new of the new node: │
         │   Find predecessor node V_pred on ring       │
         │   Keys in range (V_pred, V_new] must migrate │
         │   FROM the old successor of V_pred           │
         │   TO the new node                            │
         └──────────────────────────────────────────────┘

Step 3: Copy data for affected keys to new node
         (dual-write during migration for consistency)

Step 4: Update routing to use new node for migrated ranges

Step 5: Delete migrated data from old node (async cleanup)
```

**Zero-Downtime Migration Strategy:**

```
┌─────────────────────────────────────────────────────┐
│                 Migration Timeline                   │
│                                                     │
│  Phase 1: PREPARE                                   │
│  ├─ New node joins ring but doesn't serve traffic   │
│  ├─ Identify keys that need migration               │
│  └─ Begin background copy                           │
│                                                     │
│  Phase 2: DUAL-WRITE                                │
│  ├─ New writes go to BOTH old and new node          │
│  ├─ Reads still from old node                       │
│  └─ Background copy continues                       │
│                                                     │
│  Phase 3: SWITCH                                    │
│  ├─ Reads switch to new node                        │
│  ├─ Writes still go to both (brief period)          │
│  └─ Verify data consistency                         │
│                                                     │
│  Phase 4: CLEANUP                                   │
│  ├─ Stop dual-writes                                │
│  ├─ Delete migrated data from old node              │
│  └─ Migration complete ✓                            │
└─────────────────────────────────────────────────────┘
```

---

#### 14. Handling Hotspots and Hot Keys

Even with consistent hashing and virtual nodes, certain **hot keys** (extremely popular data) can overload a single server.

**Strategies for Hot Key Mitigation:**

**1. Key Splitting / Sharding Hot Keys:**

```
Instead of:
  "trending:post:12345" → Server-A  (overloaded!)

Split into:
  "trending:post:12345#shard0" → Server-A
  "trending:post:12345#shard1" → Server-B
  "trending:post:12345#shard2" → Server-C

Client picks a random shard for reads, writes go to all shards.
```

**2. Local Caching + Short TTL:**

```
Client → Check Local Cache (TTL: 1-5 seconds)
  HIT  → Return immediately (no network call)
  MISS → Consistent hash → Server → Cache locally → Return
```

**3. Read Replicas for Hot Keys:**

```
Hot key detected (>1000 QPS):
  ┌──────────────┐
  │ Monitoring    │ ──→ Detect hot key
  │ System        │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │ Replicate to │ ──→ Copy to 2-3 additional servers
  │ more nodes   │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │ Spread reads  │ ──→ Random selection among replicas
  │ across nodes  │
  └──────────────┘
```

---

#### 15. Real-World Usage

| System | How It Uses Consistent Hashing |
|---|---|
| **Amazon DynamoDB** | Partitions data across storage nodes; each key maps to a coordinator node via consistent hashing |
| **Apache Cassandra** | Uses a token ring (consistent hash ring) to distribute data; each node owns a range of tokens |
| **Memcached** | Client-side consistent hashing to choose which cache server stores a key |
| **Redis Cluster** | Uses hash slots (16384 slots) — a variation of consistent hashing where ranges are pre-defined |
| **Riak** | Consistent hashing with vnodes for data placement and replication |
| **Akamai CDN** | Original use case from Karger's 1997 paper — routing web requests to nearby cache servers |
| **Discord** | Routes users to specific gateway servers using consistent hashing |
| **Netflix** | EVCache uses consistent hashing for distributed caching |
| **Vimeo** | Video chunk distribution across storage servers |
| **Nginx (upstream)** | `hash $request_uri consistent` directive for upstream load balancing |
| **HAProxy** | Consistent hashing for server selection in backend pools |

**Amazon DynamoDB Architecture (Simplified):**

```
Client Request (key: "user:42")
         │
         ▼
  ┌──────────────────┐
  │  Request Router   │
  │  (Consistent Hash │
  │   → Coordinator)  │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐    Replication
  │  Coordinator Node │──────────────────┐
  │  (Primary for key)│                  │
  └────────┬─────────┘                  │
           │                             │
     ┌─────┴──────┐              ┌──────┴──────┐
     │ Replica 1   │              │ Replica 2   │
     │ (Next CW    │              │ (2nd CW     │
     │  on ring)   │              │  on ring)   │
     └─────────────┘              └─────────────┘
```

**Apache Cassandra Token Ring:**

```
                    Token Range: 0 to 2^63-1

                         0
                    ┌────●────┐
                   /  Node A   \
                  /  (0–25%)    \
                 /               \
         Node D ●                 ● Node B
       (75-100%) \               / (25-50%)
                  \             /
                   \  Node C   /
                    └──●──────┘
                     (50-75%)

  Key with token 30% → Node B (owns 25-50%)
  Key with token 80% → Node D (owns 75-100%)
  
  Replication Factor = 3:
  Token 30% → Node B (primary), Node C (replica), Node D (replica)
```

**Nginx Configuration:**

```nginx
upstream backend {
    hash $request_uri consistent;
    
    server 10.0.0.1:8080 weight=5;
    server 10.0.0.2:8080 weight=3;
    server 10.0.0.3:8080 weight=2;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
    }
}
```

---

#### 16. Consistent Hashing vs. Other Partitioning Strategies

| Strategy | How It Works | Pros | Cons |
|---|---|---|---|
| **Modulo Hashing** | `hash(key) % N` | Simple, O(1) lookup | Massive remapping on resize |
| **Range Partitioning** | Key ranges assigned to servers (A-F→S1, G-M→S2) | Range queries efficient | Hot spots on popular ranges |
| **Consistent Hashing** | Hash ring with clockwise assignment | Minimal remapping (~1/N) | Uneven without vnodes |
| **Consistent Hashing + vnodes** | Multiple ring positions per server | Even distribution + minimal remapping | More memory, complex |
| **Jump Consistent Hash** | Deterministic jump algorithm | Perfect balance, O(1) memory | Sequential servers only |
| **Rendezvous Hashing** | Highest-score wins per key-server pair | Perfect balance, simple | O(N) per lookup |
| **Hash Slot (Redis style)** | Fixed 16384 slots assigned to nodes | Explicit control, easy migration | Manual slot management |

**Decision Tree for Choosing a Partitioning Strategy:**

```
Need to partition data across servers?
│
├─ Servers change frequently?
│   │
│   ├─ Yes → Need minimal key movement
│   │   │
│   │   ├─ Servers are named (IPs/hostnames)?
│   │   │   │
│   │   │   ├─ Yes → Consistent Hashing with vnodes
│   │   │   │
│   │   │   └─ No (numbered 0..N-1, add/remove from end only)
│   │   │       → Jump Consistent Hash
│   │   │
│   │   └─ Few servers (<50)?
│   │       → Rendezvous Hashing (simpler)
│   │
│   └─ No (fixed server count)
│       → Simple Modulo Hashing
│
└─ Need range queries?
    │
    ├─ Yes → Range Partitioning
    │
    └─ No → Consistent Hashing or Modulo
```

---

#### 17. Common Interview Questions

**Q1: What happens if all virtual nodes of a server cluster together on the ring?**

With a good hash function (SHA-256, MurmurHash3), this is statistically extremely unlikely. The hash function distributes virtual nodes uniformly across the ring. With 150+ virtual nodes per server, the probability of significant clustering is negligible. However, if it does happen, you can re-seed the virtual node naming scheme (e.g., change from `server#vnode0` to `server#replica0`).

**Q2: How does consistent hashing handle server failures?**

When a server fails, its portion of the ring is automatically absorbed by the next clockwise server(s). With replication factor > 1, the data is already available on replica nodes, so there's no data loss — only a brief routing change. Health checks detect the failure, the failed node is removed from the ring, and traffic is rerouted.

**Q3: How many virtual nodes should you use?**

It depends on the number of physical servers:

- **Few servers (3-10):** 150-200 virtual nodes per server
- **Medium clusters (10-50):** 100-150 virtual nodes per server
- **Large clusters (50+):** 50-100 virtual nodes per server (many physical nodes already provide good distribution)

The goal is to keep standard deviation of load below ~5-10%.

**Q4: Can consistent hashing be used for stateful services?**

Yes. It's ideal for routing sticky sessions, sharding stateful databases, and assigning long-lived connections. If the server for a session goes down, the session naturally migrates to the next clockwise server, and the application can rebuild state from persistent storage.

**Q5: What's the difference between consistent hashing and hash slots (Redis)?**

Redis Cluster uses 16,384 fixed hash slots. Each key maps to a slot via `CRC16(key) % 16384`, and slots are assigned to servers. This is a form of consistent hashing where the "ring" is pre-divided into fixed segments. The advantage is explicit control over which slots go to which server, making manual rebalancing straightforward.
