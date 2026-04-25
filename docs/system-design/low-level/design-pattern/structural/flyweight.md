# Flyweight Design Pattern

## Blogs and websites

## Medium

## Youtube

- [30. Design Word Processor using Flyweight Design Pattern | Low Level System Design FlyWeight Pattern](https://www.youtube.com/watch?v=Mwm6tB3x1do)

## Theory

### What is Flyweight Pattern?

Uses sharing to support large numbers of fine-grained objects efficiently. Minimizes memory usage by sharing common data between multiple objects.

**Why it's used:**
- When an application uses a large number of similar objects
- When storage costs are high because of the quantity of objects
- When most object state can be made extrinsic (separated from the object)
- When object identity is not important

**Key Concept:** Intrinsic state (shared) vs Extrinsic state (unique to each instance)

---

### Diagram

```
FlyweightFactory
      ↓
   [Pool of Flyweights]
      ↓
   Flyweight (intrinsic state)
      +
   Context (extrinsic state)
```

---

### Implementation

Check which are the intrinsic and which are extrinsic properties, move out the extrinsic properties and make intrinsic properties as immutable.

---

### Real-Life Examples

- **Text Editors:** Character objects sharing font, color, style data (intrinsic) with position being extrinsic
- **Game Development:** Particle systems sharing texture, color data for thousands of bullets/particles
- **String Pooling:** Java String interning, Python string interning for memory optimization
- **Database Connection Pools:** Reusing connection objects instead of creating new ones
- **UI Icon Caching:** Sharing icon image data across multiple UI elements
- **Map Rendering:** Google Maps sharing tile images for same locations across multiple views

---

### Advantages

- Significantly reduces memory usage when many similar objects are needed
- Improves performance by reducing object creation overhead
- Centralizes state management for shared objects
- Scalable for large numbers of objects

---

### Disadvantages

- Increases complexity by separating intrinsic and extrinsic state
- Runtime costs for computing/maintaining extrinsic state
- Can make code harder to understand and maintain
- Thread-safety concerns when sharing objects

---

### When to Use

- Application uses large numbers of similar objects
- Storage costs are high due to quantity of objects
- Most object state can be made extrinsic
- Application doesn't depend on object identity
- Memory optimization is a critical requirement

---

### Pitfalls and Best Practices

**Pitfall:** Using flyweight when object count isn't a problem
**Best Practice:** Only apply when profiling shows memory/performance issues with large object counts

**Pitfall:** Incorrectly classifying state as intrinsic vs extrinsic
**Best Practice:** Carefully analyze which state is truly shared and immutable

---

### Testing Flyweight Pattern

- Verify object sharing works correctly
- Test thread-safety for shared objects
- Validate intrinsic vs extrinsic state separation
- Verify memory savings with profiling tools

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | **Reduced** (sharing) |
| **Runtime Cost** | Medium (state management) |
| **Scalability** | **Very High** |
