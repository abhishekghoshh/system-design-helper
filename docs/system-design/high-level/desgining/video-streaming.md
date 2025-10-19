# Design a Video Streaming Platform (Youtube)


## Youtube

- [Design a Video Streaming Protocol (HLS, DASH) | System Design](https://www.youtube.com/watch?v=v6qvrIY5Tgs)
- [How Video Streaming Works on Scale - System Design](https://www.youtube.com/watch?v=-JtjQ-OA7XE)
- [HLS Adaptive Bitrate Streaming - System Design](https://www.youtube.com/watch?v=6JTV4PwisoQ)
  - [piyushgarg-dev/hls-streaming](https://github.com/piyushgarg-dev/hls-streaming)
- [How I Built Video Transcoding Service From Scratch | System Design](https://www.youtube.com/watch?v=wcdaIQjtWQI)

- [System Design: Design YouTube](https://www.youtube.com/watch?v=jWRW2xGMqSw)


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