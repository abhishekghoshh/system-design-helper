# Data Serialization

## Blogs and websites


## Medium

- [JSON is incredibly slow: Here's What's Faster!](https://medium.com/data-science-community-srm/json-is-incredibly-slow-heres-what-s-faster-ca35d5aaf9e8)

## Youtube


## Theory

### What is Data Serialization?

**Data serialization** is the process of converting structured data (objects, data structures) into a format that can be stored, transmitted, and reconstructed later. **Deserialization** is the reverse — converting the stored/transmitted format back into usable data structures.

**Why It Matters:**
```
Application A (Python)                    Application B (Java)
  user = {name: "Alice", age: 30}
           ↓ serialize
      {"name":"Alice","age":30}  ──network──→  deserialize ↓
                                              User(name="Alice", age=30)
```
Different systems, languages, and services need to agree on a common format to exchange data. Serialization is the bridge.

### Common Serialization Formats

**1. JSON (JavaScript Object Notation)**
```json
{
  "name": "Alice",
  "age": 30,
  "active": true,
  "tags": ["admin", "user"]
}
```
- **Type**: Text-based
- **Human-readable**: Yes
- **Size**: Medium (verbose due to field names)
- **Speed**: Medium (text parsing)
- **Schema**: None (self-describing)
- **Use case**: REST APIs, configuration files, browser communication
- **Supported by**: Every language natively

**2. Protocol Buffers (Protobuf)**
```protobuf
message User {
  string name = 1;
  int32 age = 2;
  bool active = 3;
  repeated string tags = 4;
}
```
```
Binary output: [0A 05 41 6C 69 63 65 10 1E 18 01 ...]
→ ~60-80% smaller than JSON
```
- **Type**: Binary
- **Human-readable**: No
- **Size**: Small (field numbers instead of names, varint encoding)
- **Speed**: Very fast (compiled serializers/deserializers)
- **Schema**: Required (.proto files, code generation)
- **Use case**: gRPC, microservices, high-performance APIs
- **Created by**: Google

**3. MessagePack**
```
Same JSON structure → binary encoding
→ ~30-50% smaller than JSON, faster to parse
```
- **Type**: Binary
- **Human-readable**: No
- **Schema**: None (like binary JSON)
- **Use case**: When you want JSON-like flexibility but faster/smaller
- **Example users**: Redis (internal), Fluentd

**4. Avro**
```json
Schema: {"type": "record", "name": "User", "fields": [
  {"name": "name", "type": "string"},
  {"name": "age", "type": "int"}
]}
```
- **Type**: Binary (with JSON schema)
- **Schema**: Required (embedded in data or stored separately)
- **Schema evolution**: Excellent (add/remove fields without breaking)
- **Use case**: Kafka, Hadoop, data pipelines
- **Created by**: Apache (Hadoop ecosystem)

**5. XML**
```xml
<user>
  <name>Alice</name>
  <age>30</age>
</user>
```
- **Type**: Text-based
- **Human-readable**: Yes (but verbose)
- **Size**: Large (opening + closing tags)
- **Use case**: Legacy systems, SOAP APIs, configuration (Maven, Android)
- **Status**: Being replaced by JSON/YAML in most new systems

**6. YAML**
```yaml
name: Alice
age: 30
active: true
tags:
  - admin
  - user
```
- **Type**: Text-based
- **Human-readable**: Very (designed for humans)
- **Use case**: Configuration files (Docker Compose, Kubernetes, CI/CD)
- **Gotcha**: Indentation-sensitive, implicit type coercion (`"no"` → `false`)

**7. CSV**
```csv
name,age,active
Alice,30,true
Bob,25,false
```
- **Type**: Text-based
- **Use case**: Data export/import, spreadsheets, simple tabular data
- **Limitation**: No nested structures, no types, delimiter conflicts

### Format Comparison

| Format | Type | Size | Speed | Schema | Human-Readable | Best For |
|--------|------|------|-------|--------|----------------|----------|
| **JSON** | Text | Medium | Medium | No | Yes | REST APIs, config |
| **Protobuf** | Binary | Small | Fast | Required | No | gRPC, microservices |
| **Avro** | Binary | Small | Fast | Required | No | Kafka, data pipelines |
| **MessagePack** | Binary | Small | Fast | No | No | Perf-sensitive JSON alternative |
| **XML** | Text | Large | Slow | Optional (XSD) | Yes | Legacy, SOAP |
| **YAML** | Text | Medium | Medium | No | Very | Config files |
| **CSV** | Text | Small | Fast | No | Yes | Tabular data |

### When to Choose What

```
Building a public REST API?          → JSON (universal, self-documenting)
Microservices talking to each other? → Protobuf/gRPC (fast, typed, small)
Kafka event streaming?               → Avro (schema evolution, compact)
Configuration files?                 → YAML or JSON
Need maximum performance?            → Protobuf or FlatBuffers
Working with legacy enterprise?      → XML/SOAP
Exporting tabular data?              → CSV or Parquet
```

### Serialization Trade-offs

**Text vs Binary:**
- Text (JSON, XML): Easy to debug, larger, slower
- Binary (Protobuf, Avro): Hard to inspect, smaller, faster

**Schema vs Schema-less:**
- Schema (Protobuf, Avro): Type safety, validation, code generation, but less flexible
- Schema-less (JSON, MessagePack): Flexible, quick iteration, but no compile-time checks

**Size vs Readability:**
- JSON: 100 bytes → human can read it
- Protobuf: 40 bytes → need tooling to decode

### Security Considerations
- **Deserialization attacks**: Never deserialize untrusted data with language-native serializers (e.g., Python's `pickle`, Java's `ObjectInputStream`)
- **Use safe formats**: JSON, Protobuf, MessagePack are safe by design (no code execution)
- **Validate schemas**: Reject data that doesn't match expected schema
- **Size limits**: Set max payload sizes to prevent memory exhaustion
