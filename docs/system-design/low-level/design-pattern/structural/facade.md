# Facade Design Pattern

## Blogs and websites

## Medium

## Youtube

- [25. Facade Design Pattern with Example | Facade Low Level Design Pattern | Facade Pattern LLD Java](https://www.youtube.com/watch?v=GYaBXK54eLo)

## Theory

### What is Facade Pattern?

Provides a unified, simplified interface to a set of interfaces in a subsystem. Makes the subsystem easier to use by providing a higher-level interface.

**Why it's used:**
- To provide a simple interface to a complex subsystem
- To reduce dependencies between clients and subsystem classes
- To layer your subsystems and define entry points to each level
- To make libraries easier to use and understand

---

### Diagram

```text
      Client
        ↓
      Facade
        ↓
    ┌───┼───┐
   [A] [B] [C]
 (Complex Subsystem)
```
*Clients call the single facade, which coordinates the subsystem classes behind it.*

---

### Real-Life Examples

- **E-commerce Checkout:** OrderService facade hiding payment, inventory, shipping, notification subsystems
- **Spring Boot Starter:** Simplified configuration hiding complex auto-configuration logic
- **AWS SDK:** High-level clients (S3Client) hiding low-level API complexity
- **Video Encoding:** FFmpeg wrappers providing simple API over complex encoding operations
- **Home Automation:** Smart home hub providing unified control over lights, thermostat, security, entertainment
- **Compiler Front-end:** Simple compile() method hiding lexical analysis, parsing, semantic analysis

---

### Advantages

- Shields clients from complex subsystem components
- Promotes weak coupling between subsystems and clients
- Easier to use, understand, and test
- Provides a simple default view that's sufficient for most clients
- Doesn't prevent advanced users from accessing subsystem classes directly

---

### Disadvantages

- Can become a god object coupled to all subsystem classes
- May provide limited functionality if trying to stay simple
- Additional layer may impact performance slightly

---

### When to Use

- You want to provide a simple interface to a complex subsystem
- There are many dependencies between clients and implementation classes
- You want to layer your subsystems
- You need to decouple subsystem from clients and other subsystems

---

### Pitfalls and Best Practices

**Pitfall:** Creating a god object that does too much
**Best Practice:** Keep facade focused; multiple facades for different client needs is acceptable

**Pitfall:** Facade hiding too much, making debugging difficult
**Best Practice:** Allow direct access to subsystem classes when needed

---

### Testing Facade Pattern

- Mock subsystem components
- Test facade methods independently
- Verify error propagation from subsystems
- Test that facade correctly orchestrates subsystem calls

---

### Performance Considerations

| Aspect | Impact |
|--------|--------|
| **Memory** | Low |
| **Runtime Cost** | Low |
| **Scalability** | High |

---

### Java Example

*The facade offers one simple method hiding the payment, inventory, and shipping subsystems.*

```java
class OrderFacade {                                  // Facade: single entry point
    private final PaymentService payments = new PaymentService();
    private final InventoryService stock = new InventoryService();
    private final ShippingService shipping = new ShippingService();
    public void placeOrder(Order order) {            // Hides subsystem orchestration
        payments.charge(order); stock.reserve(order); shipping.dispatch(order);
    }
}
```

---

### Real-World Java Example: Video Conversion Library

*FFmpeg-style libraries expose dozens of codec, filter, and container classes. A `VideoConverterFacade` offers one `convertToMp4()` method that hides bitrate selection, audio normalisation, and muxing from the caller.*

```java
// Subsystem classes: powerful but complicated to use directly
class CodecExtractor {
    String extractTrack(String file) {
        return "video-track-of:" + file; // demux source file
    }
}

class Transcoder {
    String transcode(String track, String targetCodec) {
        return track + "->" + targetCodec; // re-encode frames
    }
}

class AudioNormalizer {
    String normalize(String track) {
        return track + "+normalized-audio"; // loudness correction
    }
}

class Muxer {
    String mux(String video, String container) {
        return "final." + container + "{" + video + "}"; // pack A/V streams
    }
}

// Facade: one simple method hiding the whole pipeline
class VideoConverterFacade {
    private final CodecExtractor extractor = new CodecExtractor();
    private final Transcoder transcoder = new Transcoder();
    private final AudioNormalizer audio = new AudioNormalizer();
    private final Muxer muxer = new Muxer();

    // Client calls this single method; ordering and wiring stay inside
    public String convertToMp4(String sourceFile) {
        String track = extractor.extractTrack(sourceFile);
        String recoded = transcoder.transcode(track, "h264");
        String withAudio = audio.normalize(recoded);
        return muxer.mux(withAudio, "mp4");
    }

    public String convertToWebm(String sourceFile) {
        String track = extractor.extractTrack(sourceFile);
        String recoded = transcoder.transcode(track, "vp9");
        return muxer.mux(audio.normalize(recoded), "webm");
    }
}

// Client: three lines instead of orchestrating four subsystems
class UploadController {
    private final VideoConverterFacade videos = new VideoConverterFacade();

    void onUpload(String file) {
        String mp4 = videos.convertToMp4(file);
        System.out.println("Ready to stream: " + mp4);
    }
}
```

*Why this is a good Facade:*
- Callers such as `UploadController` never import codec or muxer classes, so subsystem upgrades do not ripple outward.
- The correct step ordering (extract, transcode, normalise, mux) lives in exactly one place instead of being copy-pasted.
- Power users can still bypass the facade and use subsystem classes directly when they need fine control.

---

### Facade vs Mediator

*Both simplify communication, but Facade streamlines calls from the outside into a subsystem, while Mediator coordinates chatty peers on the inside so they stop referencing each other directly.*

| Aspect | Facade | Mediator |
|--------|--------|----------|
| **Intent** | Provide one simplified entry point to a subsystem | Centralise communication between many peer objects |
| **Direction** | Outside-in: clients call the facade instead of internals | Inside-out: colleagues talk through the mediator |
| **Subsystem knowledge** | Facade knows the subsystem; subsystems know nothing of it | Mediator knows all colleagues; colleagues know the mediator |
| **Reuse of internals** | Subsystem classes remain usable on their own | Colleagues are usually useless without their mediator |
| **Typical example** | `VideoConverterFacade` hiding codecs and muxers | Air-traffic-control mediator between planes, chatroom hub |

*Rule of thumb: if the pain is a complicated library with too many steps, write a Facade; if the pain is a web of objects calling each other, introduce a Mediator.*

---

### Interview Questions

**Q1: Does Facade hide the subsystem or replace it?**

Facade only hides complexity; it does not replace or encapsulate the subsystem. Subsystem classes stay public and directly usable, which is what distinguishes Facade from a wrapper that forbids bypass. This matters for layering: beginners can use `convertToMp4()` while experts drop down to `Transcoder` for custom bitrates. A good facade therefore never traps power users or duplicates every subsystem feature.

**Q2: How is Facade different from Adapter?**

Adapter changes an interface so incompatible code can connect, while Facade simplifies an already-compatible subsystem into fewer calls. An adapter translates method signatures; a facade orchestrates correct call sequences. You can tell them apart by asking what would break without the wrapper: without an adapter the code does not compile, but without a facade the code still works and is merely verbose and error-prone.

**Q3: Can a Facade become a God object?**

Yes, and that is the most common failure mode. A facade that grows every convenience method eventually knows too much and changes for every subsystem tweak. Prevent this by keeping one facade per subsystem or use case (`VideoConverterFacade` vs `ThumbnailFacade`), delegating rather than reimplementing logic, and returning subsystem types instead of wrapping the world. If the facade holds mutable state or business rules, split those out.

**Q4: How do you test Facade code?**

Test the facade as an integration seam: mock the subsystem classes and verify the facade calls them in the right order with the right arguments. Then add a thin end-to-end test with real subsystems to prove the pipeline actually converts a sample file. Keep client tests (`UploadController`) on a mocked facade so controller logic is independent of transcoding details. Finally, assert that subsystem exceptions are translated into meaningful facade-level errors rather than leaking codec internals.
