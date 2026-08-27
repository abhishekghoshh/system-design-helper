# Taste
- For large multi-file documentation projects, the user explicitly requested parallel multi-agent delegation ("use 10 agent to do this") rather than sequential one-file-at-a-time work without subagents; however, may still prefer sequential work for other task types. Confidence: 0.8
- Chunked writes: large files must be created in ≤250-line chunks (write_file for the first chunk, then edit_file appends) to avoid output limits; a single ~1300-line write_file call fails. Confidence: 0.85
- Use a completed gold-standard file as the template/reference when enhancing other files in the same directory (e.g., key-value-store.md for the advanced directory). Confidence: 0.8
- Uses Java with Spring Boot for code examples. Confidence: 0.9
- Prefers documentation code examples written as Spring Boot beans (`@Service`/`@Component`) rather than plain Java utility classes, with external configuration injected via `@Value`. Confidence: 0.7
- Uses `BigDecimal` for all money calculations in code examples. Confidence: 0.85
- Uses Java records for DTOs and constructor injection (not field injection) in Spring Boot examples. Confidence: 0.8
- Includes comprehensive Spring ecosystem features in code examples: Bean Validation (`@Valid`, `@NotBlank`, `@DecimalMin`), `@ControllerAdvice` exception handling, `@Transactional`, `@Scheduled`, `@Version` for optimistic locking, `@TransactionalEventListener`, and JPA entities for data-modeling. Confidence: 0.75
