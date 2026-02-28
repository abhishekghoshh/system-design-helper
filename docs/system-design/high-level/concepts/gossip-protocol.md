# Gossip Protocol



## Youtube

- [Google SWE teaches systems design | EP18: Gossip Protocol](https://www.youtube.com/watch?v=8dz0riI13j8)

- [Gossip Protocol System Design](https://www.youtube.com/watch?v=TUc_hPtxyf8)
- [Implementing Gossip Protocol in JavaScript - System Design](https://www.youtube.com/watch?v=FioXLLl7TkY)




## Blogs

- [Gossip Protocol Explained](https://highscalability.com/gossip-protocol-explained/)


## Medium

- [Gossip Protocol in distributed systems](https://medium.com/nerd-for-tech/gossip-protocol-in-distributed-systems-e2b0665c7135)


## Theory

## Theory

### Overview
A gossip protocol (also known as epidemic protocol) is a method for spreading information through a distributed system. Each node randomly selects other nodes and shares state information, similar to how gossip spreads in a social network. This approach ensures eventual consistency without requiring centralized coordination.

**Key characteristics:**
- Decentralized: No central authority needed
- Resilient: Tolerates node failures and network partitions
- Scalable: Works well with large numbers of nodes
- Simple: Easy to understand and implement

### How it works
1. Each node maintains a list of peers
2. At regular intervals, a node selects k random peers
3. The node sends its state to those peers
4. Peers receive and merge the information into their own state
5. Information gradually propagates through the entire system

### Code explaination

#### Structs

| Struct | Purpose |
|--------|---------|
| `Server` | Represents a peer node in the network. Stores the node's unique `ID`, network `Address`, `Port`, `LastSeen` timestamp, and `FailCount` to track consecutive failures before removal. |
| `GossipNode` | The main gossip node that manages the membership list. Contains `id` (this node's identifier), `address` (this node's address), `port` (this node's port), `friends` (map of known peers), `mu` (mutex for thread-safe access), `k` (number of peers to contact per round), `interval` (gossip frequency), `timeout` (HTTP request timeout), and `maxFailures` (threshold before marking a node as dead). |
| `GossipResponse` | JSON response structure returned by `/gossip` endpoint. Contains `NodeID` (responding node's ID) and `Friends` (list of all known peers). |

#### Functions

| Function | Purpose |
|----------|---------|
| `NewGossipNode(id, addr, port string, k int)` | Constructor function that creates and initializes a new `GossipNode`. Sets default gossip interval to 5 seconds, request timeout to 3 seconds, and max failures to 3. Returns a pointer to the new node. |
| `main()` | Entry point. Creates a gossip node with ID "node-1" on port 8080, registers the `/gossip` HTTP handler, starts the background gossip loop goroutine, and starts the HTTP server. |

#### Methods

| Method | Purpose |
|--------|---------|
| `GossipHandler(w, r)` | HTTP handler for the `/gossip` endpoint. When receiving a request: (1) extracts sender's `id`, `addr`, `port` from query params, (2) adds/updates the sender in `friends` map, (3) responds with this node's complete membership list as JSON. This enables bidirectional state exchange. |
| `StartGossip()` | The core gossip loop. Runs on a ticker every `interval` seconds. Each tick: (1) copies the friends list, (2) randomly selects up to `k` peers using Fisher-Yates shuffle, (3) spawns goroutines to gossip with each selected peer by calling their `/gossip` endpoint, (4) cleans up dead nodes. |
| `gossipWith(server)` | Performs an HTTP GET to the peer's `/gossip` endpoint, passing this node's identity. If successful: (1) parses the returned membership list, (2) merges new peers into local `friends` map, (3) resets the peer's `FailCount`. If failed: increments `FailCount` and logs the failure. |
| `mergeFriendsLocked(newFriends)` | Takes a list of servers received from a peer and merges them into the local `friends` map. Only adds servers that are not already known (avoids overwriting existing `LastSeen`/`FailCount`). Must be called with mutex already locked. |
| `removeDeadNodes()` | Cleanup method that iterates through all friends and removes any with `FailCount >= maxFailures`. Called after each gossip round to evict unreachable nodes. |

#### Data Flow

```
                    ┌─────────────────────────────────────────────────┐
                    │                 GossipNode                      │
                    │                                                 │
  GET /gossip?      │   ┌───────────────┐    ┌──────────────────┐    │
  id=X&addr=Y    ───┼──▶│ GossipHandler │──▶│  friends map     │    │
  &port=Z           │   └───────┬───────┘    │  {id: Server}    │    │
                    │           │            └────────┬─────────┘    │
                    │           │ responds with       │              │
                    │           │ membership list     │              │
                    │           ▼                     │              │
                    │   ┌─────────────────┐           │              │
                    │   │ JSON response:  │           │              │
                    │   │ {"friends":[...]}│          │              │
                    │   └─────────────────┘           │              │
                    │                                 │              │
                    │   ┌─────────────┐               │              │
                    │   │ StartGossip │ (every 5s)    │              │
                    │   │   loop      │◀──────────────┘              │
                    │   └──────┬──────┘                              │
                    │          │ selects k random peers              │
                    │          ▼                                     │
                    │   ┌─────────────┐    GET /gossip               │
                    │   │ gossipWith  │ ──────────────▶ Peer Node   │
                    │   └──────┬──────┘                              │
                    │          │                                     │
                    │          ▼                                     │
                    │   OK: merge friends, reset FailCount          │
                    │   FAIL: increment FailCount                   │
                    │         if FailCount >= 3: remove node        │
                    └─────────────────────────────────────────────────┘
```

### Code implementation in GO
```go
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"sync"
	"time"
)

// Server represents a peer node in the gossip network
type Server struct {
	ID        string    `json:"id"`        // Unique identifier for the node
	Address   string    `json:"address"`   // IP address or hostname
	Port      string    `json:"port"`      // Port number the node is listening on
	LastSeen  time.Time `json:"last_seen"` // Timestamp of last successful contact
	FailCount int       `json:"-"`         // Number of consecutive failures (not shared)
}

// GossipNode is the main struct that manages gossip protocol
type GossipNode struct {
	id          string             // This node's unique identifier
	address     string             // This node's address
	port        string             // This node's port
	friends     map[string]*Server // Map of known peers (id -> Server)
	mu          sync.RWMutex       // Mutex for thread-safe access to friends map
	k           int                // Number of random peers to contact per gossip round
	interval    time.Duration      // How often to run gossip (e.g., every 5 seconds)
	timeout     time.Duration      // HTTP request timeout for gossip calls
	maxFailures int                // Max consecutive failures before removing a node
}

// GossipResponse is the JSON response returned by /gossip endpoint
type GossipResponse struct {
	NodeID  string    `json:"node_id"`  // ID of the responding node
	Friends []*Server `json:"friends"` // List of all known peers
}

// NewGossipNode creates and initializes a new gossip node
func NewGossipNode(id, address, port string, k int) *GossipNode {
	return &GossipNode{
		id:          id,
		address:     address,
		port:        port,
		friends:     make(map[string]*Server),
		k:           k,                  // Number of peers to gossip with each round
		interval:    5 * time.Second,    // Gossip every 5 seconds
		timeout:     3 * time.Second,    // 3 second timeout for HTTP requests
		maxFailures: 3,                  // Remove node after 3 consecutive failures
	}
}

// GossipHandler handles incoming gossip requests at /gossip endpoint
// It receives the sender's info, adds them to friends, and returns our membership list
func (gn *GossipNode) GossipHandler(w http.ResponseWriter, r *http.Request) {
	// Extract sender's information from query parameters
	senderID := r.URL.Query().Get("id")
	senderAddr := r.URL.Query().Get("addr")
	senderPort := r.URL.Query().Get("port")

	// Validate required parameters
	if senderID == "" || senderAddr == "" || senderPort == "" {
		http.Error(w, "missing required params: id, addr, port", http.StatusBadRequest)
		return
	}

	// Add or update the sender in our friends list
	gn.mu.Lock()
	if existing, ok := gn.friends[senderID]; ok {
		// Update existing friend's last seen time and reset fail count
		existing.LastSeen = time.Now()
		existing.FailCount = 0
	} else {
		// Add new friend to our membership list
		gn.friends[senderID] = &Server{
			ID:        senderID,
			Address:   senderAddr,
			Port:      senderPort,
			LastSeen:  time.Now(),
			FailCount: 0,
		}
		log.Printf("[%s] New peer discovered: %s at %s:%s", gn.id, senderID, senderAddr, senderPort)
	}
	gn.mu.Unlock()

	// Build response with our complete membership list
	gn.mu.RLock()
	friendList := make([]*Server, 0, len(gn.friends))
	for _, server := range gn.friends {
		friendList = append(friendList, server)
	}
	gn.mu.RUnlock()

	// Send back our membership list so the sender can merge it
	response := GossipResponse{
		NodeID:  gn.id,
		Friends: friendList,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// StartGossip begins the periodic gossip loop
// Every interval, it selects k random peers and exchanges membership info
func (gn *GossipNode) StartGossip() {
	ticker := time.NewTicker(gn.interval)
	defer ticker.Stop()

	log.Printf("[%s] Starting gossip loop (interval: %v, k: %d)", gn.id, gn.interval, gn.k)

	for range ticker.C {
		// Get a snapshot of current friends
		gn.mu.RLock()
		if len(gn.friends) == 0 {
			gn.mu.RUnlock()
			continue // No peers to gossip with
		}

		friends := make([]*Server, 0, len(gn.friends))
		for _, s := range gn.friends {
			friends = append(friends, s)
		}
		gn.mu.RUnlock()

		// Randomly select up to k peers to gossip with
		numToSelect := gn.k
		if numToSelect > len(friends) {
			numToSelect = len(friends)
		}

		// Shuffle and pick first k peers (Fisher-Yates shuffle)
		rand.Shuffle(len(friends), func(i, j int) {
			friends[i], friends[j] = friends[j], friends[i]
		})

		// Gossip with selected peers concurrently
		for i := 0; i < numToSelect; i++ {
			go gn.gossipWith(friends[i])
		}

		// Cleanup dead nodes after gossip round
		gn.removeDeadNodes()
	}
}

// gossipWith contacts a peer's /gossip endpoint and exchanges membership information
func (gn *GossipNode) gossipWith(server *Server) {
	// Build the gossip URL with our identity
	url := fmt.Sprintf("http://%s:%s/gossip?id=%s&addr=%s&port=%s",
		server.Address, server.Port, gn.id, gn.address, gn.port)

	client := &http.Client{Timeout: gn.timeout}
	resp, err := client.Get(url)

	gn.mu.Lock()
	defer gn.mu.Unlock()

	// Check if the server still exists in our map (might have been removed)
	peer, exists := gn.friends[server.ID]
	if !exists {
		return
	}

	if err != nil {
		// Network error - increment failure count
		peer.FailCount++
		log.Printf("[%s] Failed to reach %s (attempt %d/%d): %v",
			gn.id, server.ID, peer.FailCount, gn.maxFailures, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		// Non-200 response - increment failure count
		peer.FailCount++
		log.Printf("[%s] Bad response from %s: %d (attempt %d/%d)",
			gn.id, server.ID, resp.StatusCode, peer.FailCount, gn.maxFailures)
		return
	}

	// Success! Parse the response and merge their membership list
	var gossipResp GossipResponse
	if err := json.NewDecoder(resp.Body).Decode(&gossipResp); err != nil {
		log.Printf("[%s] Failed to decode response from %s: %v", gn.id, server.ID, err)
		return
	}

	// Reset failure count on successful contact
	peer.LastSeen = time.Now()
	peer.FailCount = 0

	// Merge their friends into our list (done inside the lock)
	gn.mergeFriendsLocked(gossipResp.Friends)

	log.Printf("[%s] Gossiped with %s, received %d peers",
		gn.id, server.ID, len(gossipResp.Friends))
}

// mergeFriendsLocked merges a list of servers from a peer into our friends map
// MUST be called with gn.mu already locked
func (gn *GossipNode) mergeFriendsLocked(newFriends []*Server) {
	for _, server := range newFriends {
		// Don't add ourselves
		if server.ID == gn.id {
			continue
		}

		// Only add if we don't already know this node
		// (avoid overwriting our own failure tracking)
		if _, exists := gn.friends[server.ID]; !exists {
			gn.friends[server.ID] = &Server{
				ID:        server.ID,
				Address:   server.Address,
				Port:      server.Port,
				LastSeen:  time.Now(),
				FailCount: 0,
			}
			log.Printf("[%s] Learned about new peer: %s at %s:%s",
				gn.id, server.ID, server.Address, server.Port)
		}
	}
}

// removeDeadNodes removes any nodes that have exceeded the max failure threshold
func (gn *GossipNode) removeDeadNodes() {
	gn.mu.Lock()
	defer gn.mu.Unlock()

	for id, server := range gn.friends {
		if server.FailCount >= gn.maxFailures {
			log.Printf("[%s] Removing dead node: %s (failed %d times)",
				gn.id, id, server.FailCount)
			delete(gn.friends, id)
		}
	}
}

func main() {
	// Configuration for this node
	nodeID := "node-1"
	address := "localhost"
	port := "8080"
	k := 3 // Number of peers to gossip with each round

	// Create the gossip node
	node := NewGossipNode(nodeID, address, port, k)

	// Register the /gossip endpoint
	// This is the single endpoint that handles all gossip communication
	http.HandleFunc("/gossip", node.GossipHandler)

	// Start the gossip loop in a background goroutine
	go node.StartGossip()

	// Start the HTTP server
	log.Printf("[%s] Gossip node starting on %s:%s", nodeID, address, port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
```

