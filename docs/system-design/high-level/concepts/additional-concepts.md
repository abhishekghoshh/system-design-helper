# Data Partitioning

Split data for scalability.

**Types:**
- **Horizontal**: Sharding (split rows)
- **Vertical**: Split columns
- **Functional**: By business domain

# Cold Start Problem
Initial delay when starting serverless functions or services.

**Mitigation:**
- Keep functions warm
- Provisioned concurrency
- Optimize initialization
- Use lighter runtimes

# Blue-Green Deployment
Two identical environments for zero-downtime deploys.

**Process:**
1. Deploy to inactive (green)
2. Test green environment
3. Switch traffic to green
4. Keep blue as fallback

# Canary Deployment
Gradual rollout to subset of users.

**Process:**
1. Deploy to small % of servers
2. Monitor metrics
3. Gradually increase %
4. Rollback if issues

# Feature Flags
Toggle features on/off without deployment.

**Benefits:**
- A/B testing
- Gradual rollout
- Quick rollback
- Environment-specific features
