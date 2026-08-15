# Design a Video Streaming Platform (Youtube)

## Blogs and websites

## Medium

## Youtube

### Introduction

- [How Does Live Streaming Platform Work? (YouTube live, Twitch, TikTok Live)](https://www.youtube.com/watch?v=7AMRfNKwuYo)
- [Design a Video Streaming Protocol (HLS, DASH) | System Design](https://www.youtube.com/watch?v=v6qvrIY5Tgs)
- [How Video Streaming Works on Scale - System Design](https://www.youtube.com/watch?v=-JtjQ-OA7XE)


### Video Streaming internals

- [Netflix Doesn't Want You To Know This Architecture](https://www.youtube.com/watch?v=naQ-E1rzYv0)
- [HLS Adaptive Bitrate Streaming - System Design](https://www.youtube.com/watch?v=6JTV4PwisoQ)
  - [piyushgarg-dev/hls-streaming](https://github.com/piyushgarg-dev/hls-streaming)
- [How I Built Video Transcoding Service From Scratch | System Design](https://www.youtube.com/watch?v=wcdaIQjtWQI)


### Design Toktok

- [System Design: How TikTok serves Viral video to 1B Users ?](https://www.youtube.com/watch?v=LSPjhWBTAlY)



### Design Hotstar

- [How Hotstar Application Scaled 25 Million Concurrent Users | Performance Testing | Load Testing](https://www.youtube.com/watch?v=9b7HNzBB3OQ)
- [The CRAZIEST Livestream Architecture Ever Built](https://www.youtube.com/watch?v=Q9LC-WN9X4k)
- [How JioCinema live streams IPL to 20 million concurrent devices w/ Prachi Sharma | Ep 7](https://www.youtube.com/watch?v=36N1Bz7qW0A)
- [How Disney Hotstar Captures One Billion Emojis!](https://www.youtube.com/watch?v=UN1kW5AHid4)


### Design youtube

- [No One Can Build a Second YouTube (Why?!)](https://www.youtube.com/watch?v=xSkAzr7VyTI)
- [System Design: Design YouTube](https://www.youtube.com/watch?v=jWRW2xGMqSw)
- [Design Youtube - System Design Interview](https://www.youtube.com/watch?v=jPKTo1iGQiE)
- [System Design Interview: Design YouTube w/ a Ex-Meta Staff Engineer](https://www.youtube.com/watch?v=IUrQ5_g3XKs)
- [Master Youtube System Design](https://www.youtube.com/watch?v=WlMTxHcm4Qs)
- [Video Streaming & Sharing Service (YouTube) - System Design Interview Question](https://www.youtube.com/watch?v=XAZqmLXy4kY)
- [5: Netflix + YouTube | Systems Design Interview Questions With Ex-Google SWE](https://www.youtube.com/watch?v=43bB7oSn190)
- [YouTube High Level System Design with @harkirat1 !!](https://www.youtube.com/watch?v=l3AOubKFB1U)
- [Netflix System Design | YouTube System Design | System Design Interview Question](https://www.youtube.com/watch?v=lYoSd2WCJTo)


---

## Theory

### Common Streaming Protocols

- **RTMP (Real-Time Messaging Protocol):** Created by Adobe, commonly used for ingesting live streams from broadcasters to servers.
- **RTSP (Real-Time Streaming Protocol):** Developed by RealNetworks, used for establishing and controlling media sessions between endpoints.
- **HLS (HTTP Live Streaming):** Developed by Apple, segments video into small chunks and uses an index file (`.m3u8`) to store metadata about available streams and resolutions.
- **MPEG-DASH (Dynamic Adaptive Streaming over HTTP):** An open standard similar to HLS, uses a manifest file (`.mpd`) to describe available content and bitrates.

### Adaptive Bitrate Streaming

- Video is transcoded into multiple resolutions and bitrates.
- Each version is split into small chunks (e.g., 2-10 seconds).
- The client downloads the index/manifest file and selects the appropriate chunk based on current network conditions, enabling smooth playback with minimal buffering.

### Video Processing

- **Transcoding:** Tools like FFmpeg are used to convert uploaded videos into multiple formats and resolutions.
- **Chunking:** Videos are divided into small segments for adaptive streaming.
- **Storage:** Chunks and manifest files are stored on CDN or object storage for efficient delivery.

### Key Concepts

- **Manifest/Index Files:** (`.m3u8` for HLS, `.mpd` for DASH) list available video qualities and chunk locations.
- **CDN (Content Delivery Network):** Distributes video chunks closer to users for low-latency streaming.
- **Player Logic:** The video player dynamically switches between different quality streams based on real-time bandwidth measurements.

---

**Summary:**  
Modern video streaming platforms like Youtube use adaptive bitrate streaming with protocols such as HLS and MPEG-DASH. Videos are transcoded, chunked, and delivered via CDN, allowing seamless playback across varying network conditions.
