# Observability

## Logging
Recording application events.

**Log Levels:**
- **TRACE**: Very detailed
- **DEBUG**: Diagnostic information
- **INFO**: General information
- **WARN**: Warning messages
- **ERROR**: Error events
- **FATAL**: Critical failures

**Best Practices:**
- Structured logging (JSON)
- Include correlation IDs
- Log at appropriate levels
- Don't log sensitive data
- Centralize logs

**Tools:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- Datadog
- CloudWatch

## Monitoring
Collecting and analyzing metrics.

**Types:**
- **Infrastructure**: CPU, memory, disk, network
- **Application**: Request rate, latency, errors
- **Business**: User signups, transactions, revenue

**Key Metrics (RED Method):**
- **Rate**: Requests per second
- **Errors**: Error rate
- **Duration**: Response time

**Key Metrics (USE Method):**
- **Utilization**: % time busy
- **Saturation**: Queue depth
- **Errors**: Error count

**Tools:**
- Prometheus + Grafana
- Datadog
- New Relic
- CloudWatch

## Tracing
Track requests across distributed systems.

**Distributed Tracing:**
- Trace ID across all services
- Span ID for each operation
- Parent-child relationships
- Timing information

**Tools:**
- Jaeger
- Zipkin
- AWS X-Ray
- OpenTelemetry

## Alerting
Notify team of issues.

**Best Practices:**
- Alert on symptoms, not causes
- Reduce noise
- Clear escalation policy
- Runbooks for common issues
- SLO-based alerting
