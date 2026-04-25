# Object Storage / Blob Storage

## Blogs and websites


## Medium


## Youtube

### Single Videos

- [File Storage VS Object Storage | System Design](https://www.youtube.com/watch?v=AV4Ei1qW89o)
- [Design a Scalable BLOB Store | System Design](https://www.youtube.com/watch?v=lWnQtOIWiUY)
- [How do BLOB Stores Scale? (S3, GCS, MinIO) | System Design](https://www.youtube.com/watch?v=gzUJ0N6jIb4)

## Theory

### Distributed Storage

Distributed storage systems spread data across multiple machines or data centers, providing scalability, fault tolerance, and high availability that a single server cannot achieve.

**Types of Storage Systems:**
```
Block Storage:
  └─ Raw disk blocks, low-level
  └─ Used by: VMs, databases
  └─ Examples: AWS EBS, Azure Disk

File Storage:
  └─ Hierarchical directory structure
  └─ Used by: Shared file systems, NAS
  └─ Examples: AWS EFS, Azure Files, NFS

Object Storage:
  └─ Flat namespace, key-value with metadata
  └─ Used by: Media, backups, data lakes
  └─ Examples: AWS S3, Azure Blob, GCS, MinIO
```

**Why Object Storage Dominates Modern Systems:**
- **Virtually unlimited scale**: S3 handles exabytes of data
- **Cheap**: Pennies per GB/month with storage tiers (hot, warm, cold, archive)
- **Durable**: 99.999999999% (11 nines) durability — data is replicated across facilities
- **Simple API**: PUT, GET, DELETE via HTTP REST
- **Metadata-rich**: Attach custom metadata to each object

**How Object Storage Works:**
```
Object = Key + Data + Metadata

PUT object:
  Key:      "images/profile/user-123.jpg"
  Data:     <binary image data>
  Metadata: {content-type: "image/jpeg", uploaded-by: "user-123"}

GET object:
  GET https://bucket.s3.amazonaws.com/images/profile/user-123.jpg
  → Returns the image with metadata in headers
```

**Storage Tiers (Cost vs Access Speed):**
- **Hot/Standard**: Frequent access, highest cost
- **Infrequent Access**: Lower cost, retrieval fee
- **Archive/Glacier**: Cheapest storage, minutes-to-hours retrieval

---

### Quick Reference

Store unstructured data as objects.

**Features:**
- Flat namespace (no hierarchy)
- Metadata attached to objects
- REST API access
- Highly scalable
- Eventually consistent

**Popular Services:**
- AWS S3
- Azure Blob Storage
- Google Cloud Storage
- MinIO (self-hosted)

**Use Cases:**
- Media files (images, videos)
- Backups and archives
- Data lakes
- Static website hosting

---

### Process related things
