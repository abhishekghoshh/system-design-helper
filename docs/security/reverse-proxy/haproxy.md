# HAProxy basics

## Theory

HAProxy is a high-performance TCP and HTTP load balancer and reverse proxy commonly used for edge routing, TLS termination, and backend failover.
It matters because a single HAProxy config often defines how thousands of concurrent connections are accepted, inspected, routed, and retried across a whole service tier.
Key subtopics: `frontend`/`backend`/`listen` blocks, ACL-based L7 routing, TCP versus HTTP modes, health checks, TLS and mTLS termination, and stickiness.

HAProxy sits in front of your application servers and decides what every client connection becomes. Browsers
and APIs talk to HAProxy, and HAProxy talks to backends — Node, Python, Go, or Java processes that never see
the raw internet. That single hop is where TCP connections are accepted and queued, where TLS is terminated,
where ACLs route by SNI hostname, path, or header to the right backend, where health checks eject sick servers,
and where retries, timeouts, and queue limits are enforced before traffic ever reaches application code.

Think of HAProxy the way you think of an airport control tower. Planes never land wherever they want;
they announce intent on a shared frequency, and the tower sequences them to the right runway, holds overflow
in a pattern, and diverts traffic when a runway closes. HAProxy behaves the same way: `frontend` blocks own
the listening sockets and accept rules, ACLs classify each connection or request, and `backend` blocks own the
server pools with load-balancing algorithms, health checks, and retry policy. Backends stay focused on business
logic while the edge handles protocol, policy, and protection.

This page teaches you to reason about HAProxy before you memorize directives. You will learn how HAProxy works
as both an L4 TCP proxy and an L7 HTTP reverse proxy, how requests flow through `frontend`, ACL, and `backend`
selection in order, how to write `frontend`/`backend`/`listen` blocks that preserve client identity without
breaking TLS or timeouts, how to route with ACLs and verify backends with health checks, how to terminate TLS
and enforce mTLS with client certificates, when HAProxy beats Nginx for raw balancing versus content serving,
which misconfigurations attackers exploit, and how to answer the HAProxy questions interviewers always ask.

> Scope note: this page is the interview-ready overview for the HAProxy reverse-proxy guide — proxy
> behavior, `frontend`/`backend`/`listen` routing, ACLs and health checks, TLS and mTLS termination,
> HAProxy versus Nginx, threats, best practices, and Q&A. Deep mechanics live in companion pages
> (load balancing algorithms, TLS certificate deployment, forward proxy and egress control, caching
> and CDN strategy). It assumes basic HTTP and TLS and focuses on the decisions interviewers probe:
> routing correctness, mode and timeout discipline, edge security, failover behavior, and
> HAProxy-versus-Nginx trade-offs.

### Topics Covered

1. [HAProxy as L4/L7 Proxy](#1-haproxy-as-l4l7-proxy)
2. [frontend, backend, and listen](#2-frontend-backend-and-listen)
3. [ACLs, Health Checks, and mTLS](#3-acls-health-checks-and-mtls)
4. [HAProxy vs Nginx](#4-haproxy-vs-nginx)
5. [Threats and Mitigations](#5-threats-and-mitigations)
6. [Best Practices](#6-best-practices)
7. [Interview Questions and Answers](#7-interview-questions-and-answers)

### 1. HAProxy as L4/L7 Proxy

A reverse proxy receives client connections on behalf of backend servers and forwards them upstream,
then relays responses back. Clients think they are talking to your domain; they never learn how many
backends exist, which ports they listen on, or which one answered. That indirection is the whole point:
it lets you change, scale, and protect backends without changing what clients see.

The contrast that opens every interview is L4 versus L7 proxying. An L4 proxy forwards TCP bytes without
understanding HTTP — it sees source and destination IPs, ports, and optionally TLS SNI, and it balances
by connection. An L7 proxy terminates and parses HTTP — it sees Host, path, headers, and cookies, and it
balances by request. HAProxy does both in one binary: `mode tcp` for raw streams, `mode http` for
request-aware routing. If you mix them up, say it plainly: L4 for connections, L7 for requests.

HAProxy implements both roles on a single-process, event-driven engine famous for zero-copy forwarding
and precise queueing. One process accepts tens of thousands of concurrent TCP connections, parks excess
in per-backend queues with `maxconn` and `timeout queue`, and splices bytes kernel-to-kernel where possible.
That is why HAProxy is the default answer for connection-heavy edge workloads, gaming and MQTT fleets, and
API tiers where one slow backend must never stall the whole frontend — a pattern called queue-aware
load balancing that Nginx only approximates.

What HAProxy does, end to end:

- **Terminates client-facing concerns once.** TCP accept, TLS handshake, HTTP parsing, header
  normalization, and access logging happen at the edge so every backend inherits them for free.
- **Routes by connection or by request.** In `mode tcp` it picks a backend by IP, port, or SNI; in
  `mode http` it further picks by Host, path, header, or cookie via ACLs before selecting a server.
- **Queues and reuses backend capacity.** `maxconn`, `timeout queue`, keepalive, and connection reuse
  decouple client slowness from backend thread occupancy and GC pressure.
- **Enforces edge policy cheaply.** ACL deny rules, TLS requirements, rate caps via stick-tables, redirects,
  and maintenance modes reject or answer traffic without waking application code.
- **Absorbs failure gracefully.** Active health checks with `rise`/`fall`, `redispatch`, `retry`, slow-start,
  and drain-on-reload keep one bad pod from failing the hostname.

```mermaid
flowchart LR
    C["Client<br/>browser / API caller"] -->|"TCP + TLS :80/:443"| F["HAProxy frontend<br/>bind + mode + ACLs"]
    F -->|"terminate TLS<br/>inspect SNI / Host / path"| D{"Route decision"}
    D -->|"acl host_api path /api/| B1["Backend: apiservers<br/>balance roundrobin + checks"]
    D -->|"acl host_static| B2["Backend: static<br/>separate pool"]
    D -->|"mode tcp SNI db| B3["Backend: tcp-db<br/>raw TCP forward"]
    B1 -->|"forward + X-Forwarded-For"| A1["App instance 1"]
    B1 -->|"forward + X-Forwarded-For"| A2["App instance 2"]
    B2 -->|"forward"| S["Static backend"]
    B3 -->|"splice bytes"| T["TCP service"]
    A1 -->|"response"| F
    A2 -->|"response"| F
    S -->|"response"| F
    T -->|"bytes"| F
    F -->|"filtered response"| C
```

*The diagram above shows the edge funnel: HAProxy accepts on frontends, terminates TLS, classifies with
ACLs, queues to API, static, or raw-TCP backends, balances across healthy servers, and returns a single
coherent response to the client.*

Two request-path habits separate senior answers. First, always state the selection order: connection to
`bind` socket, `mode` decision for TCP versus HTTP parsing, ACL evaluation on SNI then Host then path
then headers, `use_backend` match or `default_backend` fallback, then server selection by balancing
algorithm excluding DOWN servers. Second, name what the backend must still verify: `X-Forwarded-For`,
`X-Forwarded-Proto`, and `X-SSL-Client-CN` are claims from the proxy, so the app must trust only known
proxy IPs, must never treat `X-Forwarded-For` as authentication, and must re-check mTLS identity from
forwarded headers only when the proxy stripped direct access.

### 2. frontend, backend, and listen

Routing in HAProxy is three composable blocks evaluated on every connection in a fixed order. The
`frontend` answers which socket and protocol this connection belongs to. ACLs answer which backend it
deserves. The `backend` answers which server handles it and with what balancing, health, timeout, and
retry rules. A fourth block, `listen`, combines all three for single-port services. Misrouting bugs are
almost always one block answering a question meant for another — for example, putting path logic in a
TCP-mode frontend or balancing logic in an ACL.

Start with `frontend`: each block owns one or more `bind` lines plus a `mode`. `bind *:80` accepts
plaintext, `bind *:443 ssl crt ...` terminates TLS with the named certificate bundle, and
`http-request redirect scheme https unless { ssl_fc }` closes the downgrade path the plaintext socket
opened. `default_backend` is the fallback when no `use_backend` ACL matches, so every frontend needs one.
Backends never see the raw handshake when the frontend terminates it — they see clean HTTP plus
forwarded identity headers.

Next comes `backend`: each block owns a server pool with `balance`, `option`, `timeout`, and `server`
lines. `balance roundrobin` spreads requests evenly, `leastconn` favors emptiest queues for long-lived
connections, and `source` hashes client IP for stickiness without cookies. `option forwardfor` appends
`X-Forwarded-For`, `option http-server-close` balances per-request keepalive against server idle cost,
and `timeout connect/client/server/queue` split responsibility the way Nginx splits connect/read/send.
`server echo 127.0.0.1:8000 check` names one peer; without `check` it is never probed and never ejected.

`listen` merges both for compact services — one port, one pool, one stanza. `defaults` sets the shared
baseline every block inherits unless overridden. The common production mistake is mode drift: a `mode tcp`
frontend cannot run `http-request` rules, and a `mode http` backend cannot splice raw MySQL bytes. Pick
the mode per traffic shape, declare it in `defaults` and repeat it in each block until the habit is
automatic.

The two preserved configs below show the pattern end to end. Read the first as the minimal edge: one
frontend, two binds, one redirect, one backend name. Read the second as the mTLS edge: full defaults,
TLS bundle with client verification, ALPN negotiation, and identity forwarded as headers.

## config file

**Create a cfg file and add the following contents**

Sample config — minimal frontend that redirects HTTP to HTTPS and forwards traffic to the `apiservers` backend:
```text
frontend https-in
    bind *:80
    bind *:443  ssl crt server-cert.crt verify required ca-file intermediate-client-ca.crt ca-verify-file client-root-ca.crt
    http-request redirect scheme https unless { ssl_fc }
    default_backend apiservers
```

The snippet above is explained line by line. The two `bind` lines split plaintext from TLS on one
frontend so port 80 exists only to redirect. The `ssl crt ... verify required ca-file ...` fragment
loads the server certificate and demands a client certificate chained to the intermediate plus root —
mTLS at the edge, before any backend wakes. The `http-request redirect` uses the `ssl_fc` fetch to test
whether this connection actually negotiated TLS, and `default_backend apiservers` sends everything that
survives to one named pool defined elsewhere in the file.

Advanced config with certificates — full TLS-terminating frontend that requires client certs (mTLS) and forwards the verified identity to the backend as headers:
```text
defaults
   mode http
   timeout connect 5000
   timeout client 50000
   timeout server 50000

frontend echo-frontend
   bind *:443 ssl crt server-cert.pem verify required ca-file intermediate.crt alpn h2,http/1.1
   mode http
   default_backend echo-backend
   option forwardfor
   option http-server-close
   http-request set-header X-Client-Certificate %[ssl_c_der,base64]
   http-request set-header X-SSL-Client-Cert          %{+Q}[ssl_c_der,base64]
   http-request set-header X-SSL-Client-CN            %{+Q}[ssl_c_s_dn(cn)]
   http-request set-header X-SSL-Client-Verify        %[ssl_c_verify]

backend echo-backend
   mode http
   server echo 127.0.0.1:8000
```

The snippet above is explained directive by directive. The `defaults` set `mode http` plus connect,
client, and server timeouts every later block inherits — fail fast on dead peers, tolerate slow phones
and apps up to fifty seconds. The `bind` terminates TLS with `server-cert.pem`, requires verified client
certs against `intermediate.crt`, and negotiates `h2` or HTTP/1.1 via ALPN. `option forwardfor` preserves
client IP, `option http-server-close` lets the frontend close per-request while reusing backend idles,
and the four `http-request set-header` lines forward the verified DER certificate, common name, and
verify status so the backend can authorize without re-validating the chain. The backend is deliberately
minimal — one server, HTTP mode — because TLS, verification, and identity plumbing already happened up
front.

Two companion rules complete the routing skill. First, name every pool and default explicitly: a frontend
without `default_backend` drops unmatched ACL traffic, and a backend without `balance` silently inherits
roundrobin whether you meant it or not. Second, never trust forwarding headers from the internet:
`option forwardfor` appends the real chain only when clients cannot reach backends directly, so firewall
backends to the proxy subnet and treat any client-supplied `X-Forwarded-For` as logging input, never as
auth or rate-limit identity.

### 3. ACLs, Health Checks, and mTLS

ACLs, health checks, and mTLS are the three controls that turn a dumb TCP forwarder into a secure edge.
ACLs classify each request after the handshake. Health checks continuously prove which servers deserve
traffic. mTLS proves which clients deserve access at all. The three compose in one order — verify the
client, classify the request, send only to proven servers — and every production frontend should read in
that order.

ACLs are named boolean tests evaluated with `use_backend` in file order. Host, path, header, method, and
TLS fetches combine with AND/OR/NOT into routing policy without touching application code:

```haproxy
# L7 routing: classify by Host, path, and method, then pick the pool.
frontend edge
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/combined.pem alpn h2,http/1.1 # <-- one bundle, many SANs
    http-request redirect scheme https unless { ssl_fc }                # <-- close port-80 downgrade
    acl host_api hdr(host) -i api.example.com                           # <-- tenant by Host header
    acl path_v2 path_beg /v2/                                           # <-- version prefix match
    acl is_post method POST                                             # <-- method match for write pool
    acl internal_src src 10.0.0.0/8                                     # <-- network match, never auth alone
    http-request deny if !host_api                                      # <-- unknown Hosts die at the edge
    use_backend api_v2 if host_api path_v2                              # <-- first match wins, order matters
    use_backend api_write if host_api is_post                           # <-- writes get their own queue
    default_backend api_default                                         # <-- fallback, always defined
```

The snippet above is explained choice by choice. Host ACLs isolate tenants sharing one IP the way Nginx
`server_name` does. `path_beg` splits versions so `/v2/` can drain independently of `/v1/`. Method ACLs
separate idempotent GETs from non-idempotent POSTs so retries apply only where safe. `src` matches
networks for maintenance or internal routes but never as sole authentication — IPs spoof and NATs share.
First-match `use_backend` order is the interview detail: put the most specific combination first and the
`default_backend` last, and log `%[var(txn.backend)]` or backend name so misroutes show in timelines.

Health checks move failover from passive observation to active proof. Each `server` line gains `check`,
`inter`, `rise`, `fall`, and optionally an HTTP assertion, while the backend gains redispatch and queue
policy:

```haproxy
# Failover: prove health actively, eject fast, redispatch cleanly.
backend apiservers
    mode http
    balance roundrobin                                                 # <-- even spread for stateless APIs
    option httpchk GET /healthz                                        # <-- every peer must answer 200 fast
    http-check expect status 200                                       # <-- any other code is a failure
    default-server inter 2s fall 3 rise 2 slowstart 30s                # <-- 2s probe, 3 fails out, 2 ok back
    timeout queue 10s                                                  # <-- bound waiting, then 503 not hang
    timeout connect 5s                                                 # <-- dead peer fails fast
    timeout server 30s                                                 # <-- hung handler ceiling before retry
    retries 2                                                          # <-- at most one retry, bounds tail
    option redispatch                                                  # <-- retry picks a different server
    server api1 10.0.1.11:8000 check maxconn 500                       # <-- cap per-server queue depth
    server api2 10.0.1.12:8000 check maxconn 500 backup                # <-- backup only when primaries down
    server api3 10.0.1.13:8000 check maxconn 500 disabled              # <-- staged deploy, enable on signal
```

The snippet above is explained as the failover order. `option httpchk` plus `expect status 200` turns
TCP up into application ready — a socket that accepts but returns 500s leaves the pool. `inter/fall/rise`
quantify trust: check every two seconds, eject after three consecutive failures, readmit after two
consecutive passes with a thirty-second `slowstart` ramp so a cold JVM never takes full flood. `timeout
queue` plus `maxconn` bound waiting instead of queueing forever, `retries` plus `redispatch` retry once
on a different peer, and `backup`/`disabled` encode deploy intent directly in the pool.

mTLS closes the loop by verifying clients with certificates before ACLs or backends run. The frontend
demands and validates the chain, extracts identity fetches, and forwards them as headers the backend can
authorize on:

```haproxy
# mTLS edge: require client certs, verify chain, forward identity.
frontend mtls-in
    bind *:443 ssl crt /etc/haproxy/certs/server.pem verify required ca-file /etc/haproxy/certs/intermediate.crt ca-verify-file /etc/haproxy/certs/root.crt # <-- full chain verify
    acl client_verified ssl_c_verify 0                                 # <-- 0 means chain verified OK
    http-request deny unless client_verified                            # <-- unverified clients die here
    http-request set-header X-SSL-Client-CN %{+Q}[ssl_c_s_dn(cn)]       # <-- identity claim for backend
    http-request set-header X-SSL-Client-Verify %[ssl_c_verify]         # <-- proof flag for audit logs
    default_backend apiservers
```

The snippet above is explained as the trust order. `verify required` plus `ca-file`/`ca-verify-file`
pins which intermediates and roots may sign clients — without both, any public CA could mint access.
`ssl_c_verify` is the gate: zero proceeds, anything else is denied before ACL routing burns cycles.
Forwarded CN and verify headers are claims, not proof, so the backend must accept them only from this
proxy subnet and must re-deny when the verify flag is not zero rather than trusting CN alone.

### Sample blogs and configs
- [test.cfg](https://github.com/hnasr/javascript_playground/blob/master/proxy/test.cfg)
- [Restrict API Access With Client Certificates (mTLS)](https://www.haproxy.com/blog/restrict-api-access-with-client-certificates-mtls)
- [Client Certificate Authentication with HAProxy](https://www.loadbalancer.org/blog/client-certificate-authentication-with-haproxy/)

### Youtube videos
- [HAProxy Basics](https://www.youtube.com/playlist?list=PLfnwKJbklIxwxXKiPv5nAgWwmaUvDjW_t)
- [HAProxy](https://www.youtube.com/playlist?list=PLQnljOFTspQUhgfvpgfxc-uFlWElKIBr-)

### 4. HAProxy vs Nginx

HAProxy and Nginx both terminate TLS and route HTTP, but they grew from opposite ends. HAProxy grew
from TCP load balancing toward L7: connection scheduling, health checking, and failover observability
are its home turf. Nginx grew from web serving toward proxying: static files, caching, and rewrite
logic are native. Interviews reward picking by workload shape, not by brand loyalty.

| Dimension | HAProxy | Nginx | When it decides the pick |
|---|---|---|---|
| Primary strength | L4/L7 load balancer: scheduling, health, stickiness | L7 web edge: static, cache, rewrite, gzip, auth | Pure balancing favors HAProxy; content edge favors Nginx |
| TCP and L4 | First-class TCP, splicing, PROXY protocol depth | `stream` module exists but secondary | Raw TCP, MQTT, gaming, L4 passthrough picks HAProxy |
| Health checking | Best-in-class active checks, rise/fall, agent checks | Passive `max_fails` plus commercial active checks | Fine-grained failover SLOs pick HAProxy |
| Observability | Stats socket, per-server states, queue depths | Access/error logs, stub status, Prometheus exporters | Queue-aware autoscaling stories pick HAProxy |
| Static content | Not a file server; needs a backend | Native `root`/`alias`, `try_files`, sendfile | Any image, asset, or SPA host points to Nginx |
| Caching | No content cache (relies on Varnish/CDN) | Built-in `proxy_cache`, stale-while-revalidate | Edge-cache requirement picks Nginx |
| Routing expressiveness | ACLs plus header/path rules, precise but leaner | Rich location, rewrite, map, subrequests, njs/Lua | Complex rewrites and auth flows pick Nginx |
| Config and ecosystem | Cleaner proxy grammar, strict validation | One syntax for web plus proxy, huge snippet corpus | Team familiarity often outweighs technical delta |

Two scenarios show how to narrate the choice. First, a TCP-heavy fleet with gRPC streams, per-server
queue SLOs, and drain-on-deploy semantics: HAProxy's active checks and queue introspection schedule
around deploys more precisely, with Nginx (or Envoy) kept at the outer TLS edge if static and cache
still matter. Second, a content-heavy API with versioned JS bundles, public GETs worth caching for a
minute, and OAuth callbacks needing rewrites: Nginx terminates TLS, serves `/static/`, caches anonymous
GETs, and proxies the rest — HAProxy would need two more hops for the same result.

### 5. Threats and Mitigations

HAProxy stops entire attack classes only while modes, ACLs, TLS verification, headers, and timeouts are
all honored together. Learn the failure set as pairs — how the bypass works in one sentence, which
control kills the class — and every HAProxy incident becomes pattern matching rather than recall.

| Threat | How it works | Mitigation that kills the class |
|---|---|---|
| Cleartext downgrade | Attacker keeps victims on port 80 while TLS exists | Redirect `unless { ssl_fc }`, HSTS with preload, test both ports |
| Weak TLS / old protocols | TLS 1.0 accepted, traffic sniffed or downgraded | `ssl-min-ver TLSv1.2`, PFS ciphers, ALPN `h2,http/1.1` only |
| Incomplete chain outage | Leaf-only bundle fails cold clients while warm browsers pass | Serve combined bundle, probe with `openssl s_client -showcerts` plus mobile |
| mTLS bypass | Optional verify lets attackers through without certs | `verify required` plus `ca-file`/`ca-verify-file`, deny unless `ssl_c_verify 0` |
| Spoofed `X-Forwarded-For` | Client injects private IP to fake allowlist or log identity | `option forwardfor` only behind firewall, never use header for auth |
| ACL order bypass | Broad `use_backend` shadows strict rule, admin path misrouted | Most-specific first, explicit `default_backend`, test Host plus path matrix |
| Mode confusion | HTTP rules in `mode tcp` silently ignored, policy never runs | Declare mode per block, `haproxy -c` in CI, separate TCP and HTTP frontends |
| Unchecked backend takeover | Sick server keeps receiving traffic, errors spike | `option httpchk` plus `expect status 200`, `fall 3` eject, `redispatch` retry |
| Retry storm amplification | Retries replay non-idempotent POSTs across all peers | `retries 2`, retry only idempotent failures, separate write backend |
| Queue exhaustion / slowloris | Cheap connections fill `maxconn`, legit users get 503 | `maxconn` per server plus frontend, `timeout queue`, stick-table rate caps |
| Info leak via stats socket | Public stats page exposes topology and server states | Bind stats to loopback, require auth, never expose stats frontend publicly |
| Stale peer after deploy | Old config keeps routing to drained pods | `disabled` plus graceful reload (`-sf`), slowstart ramp, verify via stats socket |

Two scenarios show how to narrate an answer. First, the mTLS bypass: the frontend used `verify optional`
so health probes passed, but attackers without certs reached the backend because no deny rule checked
`ssl_c_verify`. State both controls in one breath — switch to `verify required` with pinned CA files and
`http-request deny unless { ssl_c_verify 0 }` — plus detection: log `%[ssl_c_verify]` and CN on every
request and alert on non-zero verifies hitting protected backends. Second, suspected ACL shadow bypass:
`/api/admin` matched a broad `path_beg /api/` pool before the stricter admin rule, so the auth check
downstream never fired. Fix by ordering most-specific `use_backend` first, adding a deny-by-default for
unknown Hosts, and testing the rewritten path with `curl -H "Host: ..."` against a staging mirror.

### 6. Best Practices

- **One frontend per entry shape, one backend per pool intent.** Keep public HTTPS, internal mTLS, and
  raw-TCP frontends separate with their own binds, modes, and ACLs, and let unknown Hosts hit a deny or
  maintenance backend instead of a real pool.
- **Declare mode everywhere and mean it.** Set `mode` in `defaults` and repeat it in each `frontend` and
  `backend`, keep TCP splicing and HTTP header rules in different blocks, and fail the build on warnings.
- **Order every frontend as verify, classify, route.** Check TLS and mTLS first, evaluate ACLs next, then
  `use_backend` most-specific to least with an explicit `default_backend` last, and comment the order.
- **Terminate TLS modern-only.** Serve combined bundles, allow TLS 1.2 plus 1.3 with PFS ciphers, enable
  session cache and OCSP stapling equivalents, redirect port 80, and ship HSTS with a long max-age.
- **Forward identity, then verify it.** Use `option forwardfor` plus explicit CN/verify headers, firewall
  backends to the proxy subnet, and require the app to rebuild redirects and audit logs from those values
  in staging tests.
- **Prove health actively.** Give every server `check` with `inter/fall/rise`, assert `http-check expect
  status 200` on a real readiness endpoint, ramp returns with `slowstart`, and encode deploys with
  `backup` and `disabled`.
- **Bound every wait.** Set `connect`, `client`, `server`, and `queue` timeouts per traffic type —
  seconds for APIs, longer for websockets and TCP streams — cap with `retries 2` plus `redispatch`, and
  cap depth with per-server `maxconn`.
- **Validate config like code.** Run `haproxy -c -f` on every change, reload gracefully without dropping
  connections, version configs in git, diff staged versus live, and canary ACL changes behind a weighted
  split or backup pool.
- **Log for forensics, monitor for SLOs.** Log frontend, backend, server, timings, queue depth, TLS
  version, and verify status, alert on 5xx rate, queue time, 503 volume, cert expiry at 30/14/3 days, and
  DOWN flaps from the stats socket.
- **Harden the control plane.** Bind the stats socket to loopback with limited exposure, rotate certs and
  keys like restores, rehearse CA rollover for mTLS fleets, and deny dotfiles and hidden admin paths at
  the edge before they reach apps.

### 7. Interview Questions and Answers

**Q1 (Beginner): L4 versus L7 proxy — which is HAProxy here?**
An L4 proxy forwards TCP bytes by connection without parsing HTTP. An L7 proxy parses requests by Host,
path, and headers. HAProxy is both: `mode tcp` balances connections for databases, MQTT, and gaming,
while `mode http` balances requests for APIs and webs. This guide uses `mode http` so ACLs, redirects,
and header forwarding apply.

**Q2 (Beginner): How does a request flow through frontend, ACL, and backend?**
By socket, then classification, then pool. HAProxy accepts on a `bind` line, applies the block's `mode`,
evaluates ACLs in file order on SNI, Host, path, and headers, picks the first matching `use_backend` or
falls back to `default_backend`, then selects one UP server by the balance algorithm. Only after all five
does the server see the request.

**Q3 (Intermediate): What do `frontend`, `backend`, and `listen` each own?**
The `frontend` owns binds, modes, TLS, ACLs, and routing rules. The `backend` owns servers, balancing,
health checks, timeouts, and retries. `listen` combines both for single-port services, and `defaults`
sets the inherited baseline. Put accept logic only in frontends and pool logic only in backends.

**Q4 (Intermediate): How do ACLs route, and why does order matter?**
ACLs are named tests like `hdr(host)`, `path_beg`, `method`, or `src` combined into `use_backend` lines
evaluated top to bottom, first match wins. Put the most specific combination first and the default last,
because a broad early rule shadows stricter later ones and silently misroutes admin or versioned paths.

**Q5 (Intermediate): How do health checks eject a sick server?**
Actively, not passively. Each server gets `check` with `inter` probe interval, `fall` consecutive
failures to eject, `rise` passes to readmit, and `slowstart` ramp. `option httpchk` plus `http-check
expect status 200` requires application readiness, while `redispatch` plus `retries` moves the failed
request to a different peer instead of failing the client.

**Q6 (Intermediate): How do you terminate TLS and enforce mTLS correctly?**
Serve a combined bundle on `bind *:443 ssl crt ...`, pin minimum TLS 1.2 with PFS ciphers, redirect port
80 with `unless { ssl_fc }`, and for mTLS add `verify required` with `ca-file` plus `ca-verify-file`.
Gate with `http-request deny unless { ssl_c_verify 0 }` and forward CN and verify status as headers the
backend authorizes on. Verify from a cold client so missing intermediates cannot hide.

**Q7 (Senior): Upstream p99 spikes when one pod slows — how do you bound it?**
Split timeouts by cause with connect for dead peers, server for hung handlers, and queue for waiting,
cap depth with per-server `maxconn`, retry at most once with `retries 2` plus `redispatch` to a different
peer, eject flapping peers with `fall 3`, ramp returns with `slowstart`, and alert on per-server queue
time rather than global averages.

**Q8 (Senior): Unverified clients reach a protected backend — what is missing?**
The verify gate was optional or unchecked. Fix with `verify required` pinned to the right CA files, deny
before routing unless `ssl_c_verify` is zero, forward the verify flag alongside the CN so the backend can
re-deny, firewall the backend to the proxy so headers cannot be forged directly, and log verify status on
every request to catch rollouts that silently downgrade.

**Q9 (Senior): When do you pick HAProxy versus Nginx?**
Pick HAProxy when the job is pure L4/L7 balancing with precise health checks, queue visibility, and drain
semantics — TCP fleets, gRPC streams, connection-heavy APIs. Pick Nginx when the edge must serve, rewrite,
cache, or enforce L7 content policy — static assets, cacheable GETs, OAuth rewrites — in one hop. Name
the workload shape, then justify the pair when both appear with HAProxy balancing behind an Nginx edge.


