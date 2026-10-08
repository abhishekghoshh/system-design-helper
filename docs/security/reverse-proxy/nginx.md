# Nginx

## Theory

Nginx is a high-performance reverse proxy and web server commonly used for TLS termination, static file serving, and load balancing.
It matters because a single Nginx config often defines routing, cert handling, and upstream failover for a whole service tier.
Key subtopics: `server`/`location` blocks, `proxy_pass` upstreams, TLS and cert config, rate limiting, and caching.

Nginx sits in front of your application servers and decides what every client request becomes. Browsers
and APIs talk to Nginx, and Nginx talks to upstreams — Node, Python, Go, or Java processes that never see
the raw internet. That single hop is where TLS is terminated, where hostnames and URL paths are routed to
the right backend, where retries and timeouts are enforced, and where static files, cached responses, and
rate-limit rejections short-circuit before they ever reach application code.

Think of Nginx the way you think of a hotel front desk. Guests never walk straight into the kitchen;
they state a name and a request at the desk, and the desk routes them to the right room, turns away
visitors without reservations, and handles checkout centrally. Nginx behaves the same way: `server`
blocks pick the virtual host by IP, port, and SNI hostname, `location` blocks pick the handler by URL
prefix or regex, and `proxy_pass` forwards the rewritten request to an upstream pool with added headers.
Backends stay focused on business logic while the edge handles protocol, policy, and protection.

This page teaches you to reason about Nginx before you memorize directives. You will learn how a reverse
proxy differs from a forward proxy and a load balancer, how requests flow through `server`, `location`,
and `upstream` selection in order, how to write `proxy_pass` blocks that preserve client identity without
breaking redirects or timeouts, how to terminate TLS with modern protocols and certificates, when to rate
limit and cache at the edge versus in the app, how Nginx compares to HAProxy for L7 routing versus raw
TCP performance, which misconfigurations attackers exploit, and how to answer the Nginx questions
interviewers always ask.

> Scope note: this page is the interview-ready overview for the Nginx reverse-proxy guide — proxy
> behavior, `server`/`location`/`proxy_pass` routing, TLS termination, rate limiting and caching,
> Nginx versus HAProxy, threats, best practices, and Q&A. Deep mechanics live in companion pages
> (load balancing algorithms, TLS certificate deployment, forward proxy and egress control, caching
> and CDN strategy). It assumes basic HTTP and TLS and focuses on the decisions interviewers probe:
> routing correctness, header and timeout discipline, edge security, failover behavior, and
> Nginx-versus-HAProxy trade-offs.

### Topics Covered

1. [Nginx as a Reverse Proxy](#1-nginx-as-a-reverse-proxy)
2. [server, location, and proxy_pass](#2-server-location-and-proxy_pass)
3. [TLS, Rate Limiting, and Caching](#3-tls-rate-limiting-and-caching)
4. [Nginx vs HAProxy](#4-nginx-vs-haproxy)
5. [Threats and Mitigations](#5-threats-and-mitigations)
6. [Best Practices](#6-best-practices)
7. [Interview Questions and Answers](#7-interview-questions-and-answers)

### 1. Nginx as a Reverse Proxy

A reverse proxy receives client connections on behalf of backend servers and forwards them upstream,
then relays responses back. Clients think they are talking to your domain; they never learn how many
upstreams exist, which ports they listen on, or which one answered. That indirection is the whole point:
it lets you change, scale, and protect backends without changing what clients see.

The contrast that opens every interview is forward versus reverse proxy. A forward proxy sits near the
client and serves the client — corporate egress proxies, browser-configured proxies, and VPN-adjacent
filters hide who is asking. A reverse proxy sits near the server and serves the server — it hides who is
answering. One controls outbound access, the other controls inbound traffic. If you mix them up, say it
plainly: forward for clients, reverse for services.

Nginx implements the reverse-proxy role on an asynchronous, event-driven architecture. A small number of
worker processes each handle thousands of keepalive connections without one thread per connection, which
is why Nginx is the default choice for C10K-style edge workloads, static file fan-out, and slow-client
shielding. Slow clients finish their handshake and body upload against Nginx buffers while fast upstreams
only ever see complete, well-formed requests — a pattern called shielding that prevents a phone on a
train from holding an application thread hostage.

What a reverse proxy does, end to end:

- **Terminates client-facing concerns once.** TLS handshake, HTTP/2 and HTTP/3 framing, request limits,
  header normalization, and access logging happen at the edge so every upstream inherits them for free.
- **Routes by hostname and path.** `server` picks the tenant via `listen` plus `server_name`, `location`
  picks the handler via prefix or regex, and only then does `proxy_pass` choose the upstream pool.
- **Shields and reuses upstream capacity.** Buffering, keepalive to upstreams, connection pooling, and
  timeouts decouple client slowness from backend thread occupancy and GC pressure.
- **Enforces edge policy cheaply.** Rate limits, WAF-style deny rules, basic auth, allowlists, static
  serving, redirects, and cache hits reject or answer traffic without waking application code.
- **Absorbs failure gracefully.** Health-aware upstream selection, `proxy_next_upstream` retries,
  fail timeouts, and staged maintenance (`down`, draining) keep one bad pod from failing the hostname.

```mermaid
flowchart LR
    C["Client<br/>browser / API caller"] -->|"HTTPS :443"| N["Nginx reverse proxy<br/>server + location routing"]
    N -->|"TLS terminate<br/>rate limit / cache check"| R{"Route decision"}
    R -->|"location /api/| U1["Upstream: api<br/>127.0.0.1:3000"]
    R -->|"location /static/| S["Static / cache<br/>root + proxy_cache"]
    R -->|"location /ws/| U2["Upstream: realtime<br/>websocket upgrade"]
    U1 -->|"proxy_pass + headers"| A1["App instance 1"]
    U1 -->|"proxy_pass + headers"| A2["App instance 2"]
    U2 -->|"Upgrade: websocket"| W["App: ws handler"]
    A1 -->|"response"| N
    A2 -->|"response"| N
    S -->|"hit: serve"| N
    W -->|"frames"| N
    N -->|"filtered response"| C
```

*The diagram above shows the edge funnel: Nginx terminates TLS, applies limit and cache policy, routes
by location to API, static, or websocket handlers, load-balances across upstream instances, and returns
a single coherent response to the client.*

Two request-path habits separate senior answers. First, always state the selection order: connection to
`listen` socket, TLS SNI to `server` block via `server_name`, path to `location` by longest-prefix then
regex priority, rewrite phase, then `proxy_pass` with URI replacement rules. Second, name what the
backend must still verify: `X-Forwarded-For`, `X-Forwarded-Proto`, and `Host` are claims from the proxy,
so the app must trust only known proxy IPs via `set_real_ip_from` plus `real_ip_header` and must never
treat `X-Forwarded-For` as authentication.

### 2. server, location, and proxy_pass

Routing in Nginx is three nested choices, evaluated on every request in a fixed order. The `server`
block answers which hostname and port this connection belongs to. The `location` block answers which
URL subtree handles it. The `proxy_pass` directive answers where it goes next and which headers,
timeouts, and retry rules travel with it. Misrouting bugs are almost always one level answering a
question meant for another — for example, putting hostname logic in locations or path logic in servers.

Start with `server`: each block binds a socket via `listen` and a set of hostnames via `server_name`.
Nginx picks one server per request using IP plus port first, then SNI hostname for TLS or `Host`
header for plaintext, falling back to the `default_server`. Name-based virtual hosting lets dozens of
domains share one IP: `api.example.com` and `app.example.com` resolve to the same address but land in
different blocks with different certs, logs, and upstreams.

Next comes `location`, matched against the normalized URI after the hostname is fixed. Prefix locations
(`location /api/`) win by longest match; regex locations (`location ~ \.php$`) are tested in file order
and beat prefixes unless the prefix uses `^~`. Exact matches (`location = /healthz`) short-circuit
everything and are ideal for probes. The common production mistake is trailing-slash drift: `/api` and
`/api/` are different prefixes, and a missing slash changes both matching and `proxy_pass` URI splicing.

```nginx
# Edge virtual host: one hostname, three behaviors (API proxy, static, health).
# Lines ending in # <-- explain the interview-relevant decision, not just syntax.

upstream api_backend {
    zone api 64k;                    # <-- shared-memory zone so all workers share counters
    server 127.0.0.1:3001 max_fails=3 fail_timeout=30s; # <-- eject after 3 fails for 30s
    server 127.0.0.1:3002 max_fails=3 fail_timeout=30s;
    keepalive 32;                    # <-- reusable upstream connections (needs proxy_http_version 1.1)
}

server {
    listen 80;                                          # <-- plaintext entry, only redirects
    listen [::]:80;
    server_name api.example.com;                        # <-- this block owns one hostname
    return 301 https://$host$request_uri;               # <-- no app logic on port 80, just HSTS path
}

server {
    listen 443 ssl;                                     # <-- real entry point, TLS here
    listen [::]:443 ssl;
    server_name api.example.com;

    # (TLS directives covered in Section 3; assume ssl_certificate already set.)

    location = /healthz {                               # <-- exact match, cheapest probe path
        access_log off;                                 # <-- keep health checks out of access logs
        return 200 'ok\n';                              # <-- answered by Nginx, upstream never wakes
    }

    location /static/ {                                 # <-- longest-prefix match for assets
        alias /var/www/static/;                         # <-- alias maps URI subtree to directory
        expires 30d;                                    # <-- far-future cache for versioned files
        add_header Cache-Control "public, immutable";
    }

    location /api/ {                                 # <-- main app traffic enters here
        proxy_pass http://api_backend/;              # <-- trailing slash: strip /api/ before forward
        proxy_http_version 1.1;                      # <-- required for keepalive + websockets
        proxy_set_header Host $host;                 # <-- preserve original host for vhost-aware apps
        proxy_set_header X-Real-IP $remote_addr;      # <-- real client IP (app trusts only this proxy)
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # <-- append chain, don't overwrite
        proxy_set_header X-Forwarded-Proto $scheme;  # <-- http/https so app builds correct redirects
        proxy_set_header Connection "";              # <-- clear hop header so upstream keepalive works
        proxy_connect_timeout 5s;                    # <-- fail fast on dead upstream, then retry next
        proxy_read_timeout 30s;                      # <-- slow app response ceiling before 504
        proxy_send_timeout 30s;                      # <-- slow app read ceiling
        proxy_next_upstream error timeout http_502 http_503; # <-- retry idempotent fails on next peer
        proxy_next_upstream_tries 2;                 # <-- at most one retry: bounds tail latency
        proxy_buffering on;                          # <-- shield upstream from slow clients
        proxy_buffers 8 16k;                         # <-- spool response while client drains slowly
    }

    location /ws/ {                                   # <-- stateful upgrade path, different policy
        proxy_pass http://api_backend;                # <-- no slash: preserve full URI for router
        proxy_http_version 1.1;                       # <-- upgrades require HTTP/1.1
        proxy_set_header Upgrade $http_upgrade;       # <-- forward websocket handshake verbatim
        proxy_set_header Connection "upgrade";        # <-- complete the 101 Switching Protocols pair
        proxy_set_header Host $host;
        proxy_read_timeout 1h;                        # <-- idle frames, not short HTTP responses
        proxy_send_timeout 1h;
        proxy_next_upstream off;                      # <-- never retry upgrades: not idempotent
    }
}
```

The snippet above is explained directive by directive. The trailing slash on `proxy_pass` is the
most-tested interview detail: with a URI part (`proxy_pass http://api_backend/;`) Nginx replaces the
matched location prefix, so `/api/users` becomes `/users` upstream; without it, the full URI is
forwarded unchanged. `proxy_http_version 1.1` plus cleared `Connection` enables keepalive to upstreams,
cutting handshake churn. The four `proxy_set_header` lines are identity plumbing — without them the app
sees the proxy's IP and `http` scheme and generates wrong redirects, broken OAuth callbacks, and useless
audit logs. Timeouts split responsibility: `connect` guards dead peers, `read` guards hung handlers, and
`send` guards backpressured clients. `proxy_next_upstream` plus `tries` bounds retries so one slow peer
costs one retry, not a retry storm, and buffering plus `proxy_buffers` lets the upstream finish fast
while Nginx trickles bytes to slow phones.

Two companion rules complete the routing skill. First, match priority is exact (`=`) over longest
prefix over file-order regex (`~`) unless a prefix uses `^~` to preempt regex — put hot API prefixes
as plain locations, reserve regex for extensions, and benchmark any regex that runs on every request.
Second, never trust forwarding headers from the internet: combine `set_real_ip_from <proxy-CIDR>` with
`real_ip_header X-Forwarded-For` so `$remote_addr` is rewritten only for known proxies, and treat any
client-supplied `X-Forwarded-For` as untrusted input for logging, never for auth or rate-limit keys.

### 3. TLS, Rate Limiting, and Caching

Nginx terminates TLS so upstreams never handle certificates, negotiates modern protocols once, and
reuses sessions across thousands of clients. Rate limiting rejects abuse at the edge before it burns
application threads. Caching answers repeatable GETs from memory or disk without waking backends. The
three compose in one order — handshake, limit check, cache lookup, proxy — and every production config
should read in that order.

TLS termination centers on three choices: which certificate bundle to serve, which protocol versions
and ciphers to allow, and how to staple revocation and resume sessions cheaply:

```nginx
# TLS termination: modern protocols, strong ciphers, cheap resumption.
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/nginx/certs/api.example.com.fullchain.pem; # <-- leaf + intermediates
    ssl_certificate_key /etc/nginx/certs/api.example.com.key;       # <-- chmod 600, service user only
    ssl_protocols TLSv1.2 TLSv1.3;                   # <-- no TLS 1.0/1.1, ever
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:TLS-AES-128-GCM-SHA256; # <-- PFS only
    ssl_prefer_server_ciphers off;                   # <-- TLS 1.3 clients pick; 1.2 honors client order
    ssl_session_cache shared:SSL:10m;                # <-- 10 MB cache shared across workers
    ssl_session_timeout 10m;                         # <-- resume window, bounds replay value
    ssl_stapling on;                                 # <-- attach fresh OCSP so clients skip OCSP fetch
    ssl_stapling_verify on;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always; # <-- HSTS
}
```

The snippet above is explained choice by choice. The `fullchain` bundle must include leaf plus
intermediates — serving leaf-only is the classic outage where desktops succeed from cache while mobile
and curl fail unknown-issuer. Protocols pin to 1.2 plus 1.3 with PFS-only ciphers so captured traffic
stays unreadable after key rotation. The shared session cache plus timeout trades resumption speed
against replay window. OCSP stapling moves revocation checks server-side so handshakes stay fast and
private. HSTS with long max-age plus preload closes the HTTP-downgrade path the redirect block opened.

Rate limiting and caching apply after the handshake, with zones sized and keyed deliberately:

```nginx
# Edge policy: limits run before cache, cache runs before proxy.
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=20r/s;  # <-- 10 MB holds ~160k IPs
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;           # <-- concurrent connections per IP
proxy_cache_path /var/cache/nginx/api levels=1:2 keys_zone=api_cache:50m max_size=5g inactive=10m; # <-- disk cache

server {
    listen 443 ssl;
    server_name api.example.com;

    location /api/ {
        limit_req zone=api_limit burst=40 nodelay;   # <-- allow bursts, reject sustained floods with 503
        limit_conn conn_limit 20;                    # <-- cap parallel connections per IP
        limit_req_status 429; limit_conn_status 429; # <-- return 429 so clients back off correctly
        proxy_cache api_cache;                       # <-- cache zone from proxy_cache_path
        proxy_cache_valid 200 1m;                    # <-- cache only successes, briefly
        proxy_cache_valid 404 10s;                   # <-- absorb negative-cache stampedes briefly
        proxy_cache_key "$scheme$host$request_uri";  # <-- never key on attacker headers
        proxy_cache_bypass $http_authorization;      # <-- authenticated responses stay private
        proxy_no_cache $http_authorization;
        add_header X-Cache-Status $upstream_cache_status; # <-- HIT/MISS/BYPASS for debugging
        proxy_pass http://api_backend/;
    }
}
```

The snippet above is explained as the edge order. `limit_req_zone` keys on binary IP to save memory
and sets a refill rate plus a burst that absorbs human double-clicks while `nodelay` keeps p99 flat;
sustained bots get 429 instead of backend threads. Connection limits catch slowloris-style fan-out that
request rates miss. Cache directives whitelist only safe responses — short TTLs for 200s, tiny negative
TTL for 404s — with keys built from scheme, host, and URI so a poisoned header cannot split the cache.
`proxy_cache_bypass` plus `no_cache` on `Authorization` prevents one user's JSON from serving to the
next. The `X-Cache-Status` header makes HIT versus MISS visible in every incident timeline.

### 4. Nginx vs HAProxy

Nginx and HAProxy both terminate TLS and load-balance, but they grew from opposite ends. Nginx grew
from web serving toward proxying: static files, caching, and L7 rewriting are native. HAProxy grew
from TCP load balancing toward L7: connection scheduling, health checking, and failover observability
are its home turf. Interviews reward picking by workload shape, not by brand loyalty.

| Dimension | Nginx | HAProxy | When it decides the pick |
|---|---|---|---|
| Primary strength | L7 web edge: static, cache, rewrite, gzip, auth | L4/L7 load balancer: scheduling, health, stickiness | Static plus cache favors Nginx; pure balancing favors HAProxy |
| Static content | Native `root`/`alias`, `try_files`, sendfile | Not a file server; needs a backend | Any image, asset, or SPA host points to Nginx |
| Caching | Built-in `proxy_cache`, stale-while-revalidate | No content cache (relies on Varnish/CDN) | Edge-cache requirement picks Nginx |
| Routing expressiveness | Rich location, rewrite, map, subrequests, njs/Lua | ACLs plus header/path rules, precise but leaner | Complex rewrites and auth flows pick Nginx |
| TCP and L4 | `stream` module exists but secondary | First-class TCP, splicing, PROXY protocol depth | Raw TCP, MQTT, gaming, L4 passthrough picks HAProxy |
| Health checking | Passive `max_fails` plus commercial active checks | Best-in-class active checks, rise/fall, agent checks | Fine-grained failover SLOs pick HAProxy |
| Observability | Access/error logs, stub status, Prometheus exporters | Stats socket, per-server states, queue depths | Queue-aware autoscaling stories pick HAProxy |
| Config and ecosystem | One syntax for web plus proxy, huge snippet corpus | Cleaner proxy grammar, strict validation | Team familiarity often outweighs technical delta |

Two scenarios show how to narrate the choice. First, a content-heavy API with versioned JS bundles,
public GETs worth caching for a minute, and OAuth callbacks needing rewrites: Nginx terminates TLS,
serves `/static/`, caches anonymous GETs, and proxies the rest — HAProxy would need two more hops for
the same result. Second, a TCP-heavy fleet with gRPC streams, per-server queue SLOs, and drain-on-deploy
semantics: HAProxy's active checks and queue introspection schedule around deploys more precisely, with
Nginx (or Envoy) kept at the outer TLS edge if static and cache still matter.
### 5. Threats and Mitigations

Nginx stops entire attack classes only while routing, headers, TLS, limits, and cache scope are all
honored together. Learn the failure set as pairs — how the bypass works in one sentence, which control
kills the class — and every Nginx incident becomes pattern matching rather than recall.

| Threat | How it works | Mitigation that kills the class |
|---|---|---|
| Host-header / vhost confusion | Attacker sends a victim Host to a default server with permissive routing | Explicit `server_name` per tenant, `default_server` returns 444, test SNI plus Host matrices |
| `proxy_pass` trailing-slash mismatch | `/api/users` forwarded as `/api/api/users` or stripped wrong, bypassing auth prefixes | Pin slash semantics per location, integration-test rewritten URIs, alert on upstream 404 spikes |
| Untrusted `X-Forwarded-For` spoofing | Client injects `X-Forwarded-For: 10.0.0.1` to fake allowlist or rate-limit identity | `set_real_ip_from` for known proxies only, `real_ip_header`, never use header for auth |
| Missing TLS / weak protocols | Plaintext HTTP or TLS 1.0 accepted, traffic sniffed or downgraded | Redirect 80 to 443, `ssl_protocols TLSv1.2 TLSv1.3`, PFS ciphers, HSTS with preload |
| Incomplete chain outage | Leaf-only bundle fails cold clients while warm browsers pass | Serve fullchain, probe with `openssl s_client -showcerts` plus mobile, monitor chain depth |
| L7 flood and slowloris | Cheap requests or slow bodies exhaust workers and upstreams | `limit_req` plus `limit_conn` with 429, `client_body_timeout`, buffering, upstream timeouts |
| Retry storm amplification | `proxy_next_upstream` retries non-idempotent POSTs across all peers | Retry only `error timeout http_502 http_503`, `tries 2`, `off` for ws and POST payment paths |
| Cache poisoning / cross-user leak | Attacker header splits cache key or authed JSON cached publicly | Key on `$scheme$host$request_uri`, `proxy_cache_bypass` on `Authorization` and `Cookie` |
| Path traversal via `alias` | `location /static/` plus `alias` missing slash serves `/etc/passwd` | Trailing-slash discipline, `try_files`, deny `..`, filesystem perms, block hidden files |
| Clickjacking / MIME sniffing | Framed admin UI or sniffed upload executes script | `X-Frame-Options`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy`, separate upload domain |
| Version disclosure and info leak | `Server: nginx/1.x` plus verbose errors aid fingerprinting | `server_tokens off`, custom error pages, structured logs shipped off-box, no stack traces |
| Stale cache serving after deploy | Old bundle served for hours after rollback window | Versioned asset names, `proxy_cache_valid` short TTLs, `proxy_cache_use_stale` only for errors, purge runbook |

Two scenarios show how to narrate an answer. First, the trailing-slash auth bypass: `/api/admin`
matches `location /api/` but `proxy_pass http://backend;` without slash forwards `/api/admin` while
the auth check upstream expects `/admin`, so the admin handler never fires. State both controls in one
breath — normalize slash semantics and test the rewritten URI with `curl -H "Host: ..."` against a
staging mirror — plus detection: log `$request_uri` versus `$upstream_uri` and alert on prefix drift.
Second, suspected spoofed-IP allowlist bypass: the app trusted `X-Forwarded-For` for an internal admin
check and an attacker appended a private IP. Fix with `set_real_ip_from` scoped to VPC plus CDN ranges,
rewrite `$remote_addr` from the header only there, move admin checks to mTLS or VPN, and treat the
header as logging input everywhere else.

### 6. Best Practices

- **One hostname per `server`, one purpose per `location`.** Keep virtual hosts narrow, give health,
  static, API, and websocket paths their own blocks with their own timeouts and limits, and let the
  default server drop unknown Hosts with `return 444`.
- **Pin `proxy_pass` URI semantics deliberately.** Use the trailing slash when you mean strip-the-prefix
  and omit it when you mean preserve-the-path, comment the choice inline, and cover both with URI
  rewrite tests in CI.
- **Forward identity, then verify it.** Always set `Host`, `X-Real-IP`, `X-Forwarded-For`, and
  `X-Forwarded-Proto`, use `set_real_ip_from` for known proxies, and require the app to build redirects
  and audit logs from those values in staging tests.
- **Terminate TLS modern-only.** Serve fullchain bundles, allow TLS 1.2 plus 1.3 with PFS ciphers,
  enable session cache and OCSP stapling, redirect port 80, and ship HSTS with a long max-age.
- **Limit before you proxy, cache before you compute.** Order every location as rate check, cache
  lookup, then `proxy_pass`; key caches on scheme plus host plus URI; bypass on auth; expose
  `$upstream_cache_status` for incident timelines.
- **Bound every wait.** Set `connect`, `read`, and `send` timeouts per location type — seconds for APIs,
  hours for websockets — cap retries with `proxy_next_upstream_tries`, and disable retries for
  non-idempotent routes.
- **Shield slow clients from fast backends.** Keep `proxy_buffering on` for HTTP, size `proxy_buffers`
  for p99 response bodies, enable upstream keepalive with HTTP/1.1, and monitor upstream queue time
  separately from client time.
- **Validate config like code.** Run `nginx -t` on every change, `nginx -s reload` for zero-downtime
  rollout, version configs in git, diff staged versus live with `nginx -T` dumps, and canary location
  changes behind a weighted split.
- **Log for forensics, monitor for SLOs.** Keep access logs with request ID, cache status, upstream
  address and time, alert on 5xx rate, p99 latency, 429 volume, cert expiry at 30/14/3 days, and chain
  depth changes.
- **Harden the edge headers and tokens.** Set `server_tokens off`, add frame, content-type, and CSP
  headers, deny dotfiles, cap `client_max_body_size`, and rehearse cert rotation plus key revocation
  the way you rehearse restores.

### 7. Interview Questions and Answers

**Q1 (Beginner): Forward proxy versus reverse proxy — which is Nginx here?**
A forward proxy sits near the client and hides who is asking, controlling outbound access. A reverse
proxy sits near the server and hides who is answering, controlling inbound traffic. Nginx in this guide
is a reverse proxy: clients reach one hostname and Nginx routes, terminates TLS, and balances across
upstreams they never address directly.

**Q2 (Beginner): How does Nginx pick a `server` and then a `location`?**
By socket plus name then by path. Nginx matches `listen` IP and port first, then SNI hostname or Host
header against `server_name` with fallback to `default_server`. Inside that server it matches the URI:
exact `=` wins, then longest prefix, then file-order regex `~` unless a prefix used `^~` to preempt.
Only after both does `proxy_pass` forward.

**Q3 (Intermediate): What does the trailing slash in `proxy_pass` change?**
Whether the matched prefix is replaced. With `location /api/` plus `proxy_pass http://backend/;` the
prefix is stripped so `/api/users` becomes `/users`. Without the slash it is preserved so `/api/users`
stays `/api/users`. Getting it wrong either double-prefixes or misroutes auth checks — test rewritten
URIs explicitly.

**Q4 (Intermediate): Which headers must you forward, and which must you distrust?**
Forward `Host`, `X-Real-IP`, `X-Forwarded-For` via `$proxy_add_x_forwarded_for`, and
`X-Forwarded-Proto` via `$scheme`, so the app builds correct redirects and logs real IPs. Distrust any
of them when they arrive from the internet: rewrite `$remote_addr` only for CIDRs in
`set_real_ip_from`, and never key auth or rate limits on a client-supplied forwarding header.

**Q5 (Intermediate): How do you terminate TLS correctly at Nginx?**
Serve the fullchain bundle with a 600-permission key, allow only TLS 1.2 and 1.3 with PFS ciphers,
share a session cache across workers, enable OCSP stapling, redirect port 80 to 443, and send long
HSTS. Verify from a cold client with `openssl s_client -showcerts` so missing intermediates cannot
hide behind desktop cache.

**Q6 (Intermediate): Where do rate limiting and caching sit in the request path?**
After the handshake, before the proxy: limit check, then cache lookup, then upstream. Key limits on
`$binary_remote_addr` with burst plus `nodelay` returning 429, key caches on scheme plus host plus URI
with short TTLs, bypass on `Authorization`, and expose `X-Cache-Status` so HIT versus MISS is visible
in every debug trace.

**Q7 (Senior): Upstream p99 spikes when one pod slows — how do you bound it?**
Split timeouts by cause with `proxy_connect_timeout` for dead peers and `proxy_read_timeout` for hung
handlers, retry only idempotent failures with `proxy_next_upstream error timeout http_502 http_503`
capped at two tries, eject flapping peers with `max_fails` plus `fail_timeout`, keep buffering on so
slow clients never pin app threads, and alert on per-upstream latency rather than global averages.

**Q8 (Senior): Websockets work over curl but drop through Nginx — what is missing?**
The upgrade handshake was not proxied as HTTP/1.1 with both headers. Fix with `proxy_http_version
1.1` plus `proxy_set_header Upgrade $http_upgrade` and `Connection "upgrade"`, extend read and send
timeouts to hours for idle frames, turn `proxy_next_upstream off` because upgrades are not retryable,
and pin the route to its own `/ws/` location.

**Q9 (Senior): When do you pick Nginx versus HAProxy?**
Pick Nginx when the edge must serve, rewrite, cache, or enforce L7 policy — static assets, cacheable
GETs, OAuth rewrites, header auth — in one hop. Pick HAProxy when the job is pure L4/L7 balancing with
precise health checks, queue visibility, and drain semantics, adding Nginx or a CDN in front only if
static and cache return. Name the workload shape, not the logo, and justify the pair when both appear.

## Youtube

- [Wait... Nginx can do WHAT?!](https://www.youtube.com/watch?v=OEFZUj_RQKc)
- [nginx personal](https://www.youtube.com/playlist?list=PL67qvtIf7Oxt4hJj0AKWIsEGyCatfP91Z)


## Udemy

- [NGINX Fundamentals: High Performance Servers from Scratch](https://udemy.com/course/nginx-fundamentals)


## Others

- [Nginx UI](https://nginxui.com/)
- [Nginx Playground](https://nginx-playground.wizardzines.com/)
- Docker Images
  - nginx
  - nginx:alpine
  - nginx:alpine-slim
