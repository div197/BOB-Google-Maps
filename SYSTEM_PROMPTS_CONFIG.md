# 🔱 BOB SYSTEM - GLOBAL CONFIGURATION & PROMPTS

**Version:** 1.0
**Date:** November 14, 2025
**Philosophy:** Nishkaam Karma Yoga - Excellence through duty

---

## **SECTION 1: SYSTEM ARCHITECTURE PROMPTS**

### **1.1 Core Operating Principle**

```
करणेवाधिकारस्ते मा फलेषु कदाचन।
"You have the right to act, not to the fruits of your actions."

EXECUTION MANDATE:
- Focus on perfect execution of duty
- Don't attach to outcomes
- Ensure continuous improvement
- Maintain system stability above all
- Serve the ecosystem with dedication
```

### **1.2 Deployment Architecture**

```yaml
PRODUCTION_DEPLOYMENT:
  Orchestration: Docker (Primary), Kubernetes (Future)
  Strategy: Microservices with event-driven communication
  Philosophy: "Do your part, trust the system"

ECOSYSTEM_COMPONENTS:
  1. BOB-Google-Maps (Data Extraction)
     ├─ Port: 8000 (Primary)
     ├─ Backup Ports: 8080, 8888, 9000
     ├─ Status: Ready for deployment
     └─ Duty: Extract 108-field business intelligence

  2. BOB-WOO-ROM (E-commerce Intelligence)
     ├─ Ports: 9001-9005
     ├─ Components: Brahma, Vishnu, Shiva, Orchestrator, Aggregator
     └─ Duty: Process commerce data

  3. BOB-KUNDALI (Numerology System)
     ├─ Ports: 30001-30002, 5433, 6380
     └─ Duty: Astrological calculations

  4. BOB-BLOGGER (Content Management)
     ├─ Ports: 5005, 6381
     └─ Duty: Blog and content operations

  5. BOB-CHAT (Communication)
     ├─ Ports: 7654, 27018
     ├─ Status: ⚠️ RECOVERING (restarted)
     └─ Duty: Chat and messaging

  6. BOB-NAKSHATRA (Star Tracking)
     ├─ Port: 10008
     └─ Duty: Astronomical calculations
```

---

## **SECTION 2: PORT ALLOCATION & CONFLICTS RESOLUTION**

### **2.1 Active Port Mapping**

```
REDIS INSTANCES (4 total):
  6379  → bob-redis (Main Cache) [CRITICAL]
  6380  → abcnakshatra_redis (Kundali Cache)
  6381  → bob-blogger-cache (Blogger Cache)
  6382  → bob-woo-redis (WOO-ROM Cache)

  ✅ NO CONFLICTS - Each on unique host port
  ✅ All map to 6379 internally (correct isolation)
  ✅ No blocking issues detected

POSTGRESQL (2 total):
  5432  → bob-postgres (Main DB) [CRITICAL]
  5433  → abcnakshatra_postgres (Kundali DB)

  ✅ NO CONFLICTS
  ✅ Properly isolated

APPLICATION SERVICES:
  5005  → bob-blogger (App)
  7654  → bob-chat-app (⚠️ RECOVERING)
  9001  → bob-woo-rom-brahma
  9002  → bob-woo-rom-vishnu
  9003  → bob-woo-rom-shiva
  9004  → bob-woo-rom-orchestrator
  9005  → bob-woo-rom-data_aggregator
  10008 → bob-nakshatra-api
  27018 → bob-chatui-mongo (MongoDB)
  30001 → abcnakshatra-api (Kundali API)
  30002 → abcnakshatra-streamlit (Kundali UI)

  ✅ NO CONFLICTS
  ✅ All properly mapped

AVAILABLE PORTS FOR NEW SERVICES:
  ✅ 8000   → RESERVED FOR BOB-Google-Maps (PRIMARY)
  ✅ 8080   → Available (HTTP Alternative)
  ✅ 8888   → Available (Jupyter/Dev)
  ✅ 9000   → Available (Custom)
  ✅ 10000-10007 → Range available
  ✅ 11000-11999 → Large block available
```

### **2.2 Non-Blocking Port Configuration**

```
REQUIREMENT: All services must use non-blocking ports
STATUS: ✅ ALL COMPLIANT

VALIDATION RULES:
  1. Each service uses unique host port
  2. No two services share same external port
  3. Internal ports (6379, 5432, etc.) can be shared via mapping
  4. All mappings verified and documented
  5. Future services must check availability first

CONFLICT RESOLUTION PROTOCOL:
  If conflict detected:
    1. Stop offending service
    2. Reassign to available port
    3. Update documentation
    4. Restart all dependent services
    5. Verify network connectivity
```

---

## **SECTION 3: SERVICE HEALTH MONITORING**

### **3.1 Health Check Configuration**

```yaml
HEALTH_CHECK_STANDARDS:
  Interval: 30 seconds
  Timeout: 10 seconds
  Retries: 3
  Start Period: 40 seconds

  STATUS_CODES:
    healthy: Service passing all checks ✅
    starting: Service initializing...
    unhealthy: Service failing checks ⚠️
    exited: Service stopped

SERVICES_REQUIRING_ATTENTION:
  1. bob-chat-app
     Status: Recovering (restarted Nov 14, 16:44)
     Issue: Healthcheck failures detected
     Action: Monitoring closely
     Expected Recovery: 5-10 minutes

  2. dharmic_api_server
     Status: Exited (137) - SIGKILL
     Cause: Resource exhaustion (likely OOM)
     Action: Keep exited until investigation
     Note: Non-critical service for main ecosystem

SERVICES_STATUS:
  ✅ bob-redis               (28 hours healthy)
  ✅ bob-postgres            (28 hours healthy)
  ✅ bob-woo-rom-brahma      (28 hours healthy)
  ✅ bob-woo-rom-vishnu      (28 hours healthy)
  ✅ bob-woo-rom-shiva       (28 hours healthy)
  ✅ bob-woo-rom-orchestrator (28 hours healthy)
  ✅ bob-woo-rom-data_aggregator (28 hours healthy)
  ✅ bob-woo-redis           (28 hours healthy)
  ✅ bob-nakshatra-api       (29 hours healthy)
  ✅ bob-chatui-mongo        (30 hours healthy)
  ✅ bob-blogger-production  (30 hours healthy)
  ✅ bob-blogger-cache       (30 hours healthy)
  ✅ abcnakshatra_api        (31 hours healthy)
  ✅ abcnakshatra_postgres   (31 hours healthy)
  ✅ abcnakshatra_redis      (31 hours healthy)
  ✅ abcnakshatra_streamlit  (31 hours healthy)
  ⚠️  bob-chat-app           (Recovering - health: starting)
  ℹ️  abcnakshatra_worker    (Running, no healthcheck)
  ❌ dharmic_api_server      (Exited 137)
  ❌ dharmic_wisdom_db       (Exited 0)
  ❌ dharmic_redis_cache     (Exited 0)
```

### **3.2 Monitoring & Alerting Setup**

```yaml
MONITORING_FRAMEWORK:
  Strategy: Multi-layer health monitoring

  LAYER_1_CONTAINER_HEALTH:
    Tool: Docker native healthchecks
    Status: ✅ ACTIVE (17/21 passing)

  LAYER_2_SERVICE_MONITORING:
    Needed: Prometheus + Grafana
    Status: ❌ NOT DEPLOYED
    Action: Deploy after BOB-Google-Maps

  LAYER_3_LOG_AGGREGATION:
    Needed: ELK Stack or Splunk
    Status: ❌ NOT DEPLOYED
    Action: Implement after core stabilization

  LAYER_4_APM_TRACING:
    Needed: Jaeger or DataDog
    Status: ❌ NOT DEPLOYED
    Action: Future enhancement

ALERT_THRESHOLDS:
  - Container down > 2 minutes: CRITICAL
  - Memory usage > 90%: WARNING
  - CPU usage > 80%: WARNING
  - Response time > 5s: INFO
  - Error rate > 5%: WARNING
```

---

## **SECTION 4: BOB-GOOGLE-MAPS DEPLOYMENT**

### **4.1 Deployment Configuration**

```yaml
SERVICE_NAME: bob-google-maps
VERSION: 4.2.0
STATUS: READY FOR DEPLOYMENT
DEPLOYMENT_DATE: November 14, 2025

DEPLOYMENT_SPEC:
  Container:
    Base Image: python:3.10-slim
    Build Context: /Users/aaple30/Documents/3-10-2025/BOB-Google-Maps
    Dockerfile: Dockerfile (updated Sept 2025)

  Network:
    Primary Port: 8000
    Backup Ports: 8080, 8888, 9000
    Network Mode: Bridge (docker0)
    Container Network: bob-network (recommended)

  Resources:
    Memory Limit: 1GB
    Memory Reserved: 512MB
    CPU Limit: 1.5 cores
    CPU Reserved: 0.5 cores

  Storage:
    Cache Volume: bob_cache (SQLite)
    Logs Volume: bob_logs (persistent)
    Data Volume: bob_data (extraction results)
    Exports Volume: bob_exports (formatted outputs)

  Health Check:
    Command: python -c "import bob; print('OK')"
    Interval: 30s
    Timeout: 10s
    Retries: 3
    Start Period: 40s

  Environment:
    BOB_HEADLESS: true
    BOB_MEMORY_OPTIMIZED: true
    BOB_CACHE_ENABLED: true
    BOB_LOG_LEVEL: INFO
    BOB_MAX_CONCURRENT: 3
    BOB_TIMEOUT: 30

DEPLOYMENT_CHECKLIST:
  ✅ Dockerfile created and tested
  ✅ docker-compose.yml configured
  ✅ Port 8000 verified available
  ✅ Network topology planned
  ✅ Volume mappings configured
  ✅ Health checks configured
  ✅ Environment variables set
  ⏳ Integration with BOB-Central ready (pending deployment)
```

### **4.2 Post-Deployment Verification**

```bash
# 1. Check container is running
docker ps | grep bob-google-maps

# 2. Verify port is accessible
curl http://localhost:8000/health || echo "API endpoint check"

# 3. Test single extraction
docker-compose exec bob-extractor python -m bob "Starbucks New York"

# 4. Monitor logs
docker-compose logs -f

# 5. Check health
docker inspect bob-google-maps-optimized --format='{{.State.Health.Status}}'

# 6. Performance test
time docker-compose exec bob-extractor python -m bob "10 random businesses"

# 7. Memory monitoring
docker stats bob-google-maps-optimized
```

---

## **SECTION 5: SYSTEM PROMPTS FOR OPERATIONS**

### **5.1 Operational Mandates**

```
🔱 NISHKAAM KARMA EXECUTION MANTRA

When facing challenges:
  1. Identify root cause without ego
  2. Execute solution with full dedication
  3. Don't worry about success/failure
  4. Focus on perfect execution
  5. Trust in the system's design

OPERATIONAL COMMANDMENTS:
  ✓ Services must be UP 99.5%+ of time
  ✓ All ports must be documented & non-blocking
  ✓ Health checks must pass within 2 minutes
  ✓ No service can hog resources > 80%
  ✓ Errors must be logged with context
  ✓ Failures must trigger automatic recovery
  ✓ Documentation must be updated with every change
  ✓ Testing must validate every deployment
  ✓ Monitoring must be continuous
  ✓ Learning must drive improvement

RESPONSE_PROTOCOLS:

When Service Fails:
  1. Log the failure with full context
  2. Attempt automated recovery (docker restart)
  3. If persists >5min, escalate for investigation
  4. Document root cause
  5. Implement permanent fix
  6. Add monitoring for prevention

When Port Conflict Occurs:
  1. Identify conflicting services
  2. Stop the secondary service
  3. Reassign to available port
  4. Update all dependencies
  5. Restart both services
  6. Verify network connectivity

When Performance Degrades:
  1. Identify the bottleneck
  2. Check CPU/Memory/Disk/Network
  3. Scale affected service or optimize code
  4. Monitor recovery
  5. Adjust resource limits if needed
```

### **5.2 Daily Operational Checklist**

```
DAILY HEALTH VERIFICATION:

Morning (Daily):
  □ docker ps (verify all critical services running)
  □ Check for unhealthy containers
  □ Review logs for errors
  □ Verify port mappings
  □ Test data extraction on sample business

Weekly:
  □ Full system restart (planned)
  □ Backup critical data
  □ Review monitoring metrics
  □ Performance analysis
  □ Documentation audit

Monthly:
  □ Capacity planning review
  □ Security audit
  □ Dependency updates
  □ Disaster recovery drill
  □ Architecture review
```

---

## **SECTION 6: INTEGRATION POINTS**

### **6.1 BOB-Central-Integration Hookups**

```yaml
BOB_GOOGLE_MAPS_INTEGRATION:
  API_ENDPOINT: "http://bob-google-maps:8000/api/extract"
  FALLBACK_ENDPOINT: "http://localhost:8000/api/extract"
  TIMEOUT: 30 seconds
  RETRY_COUNT: 3
  BATCH_SIZE_MAX: 100 businesses
  RATE_LIMIT: 20 businesses/minute

INTEGRATION_TESTS:
  - Single business extraction
  - Batch extraction (10 businesses)
  - Error handling
  - Timeout recovery
  - Memory limits under load
```

---

## **SECTION 7: SYSTEM METRICS & KPIs**

```yaml
PRODUCTION_TARGETS:
  Availability: 99.5%+ uptime
  Extraction_Success_Rate: >95%
  Quality_Score: >80/100
  Response_Time: <20 seconds/business
  Memory_Per_Session: <100MB
  Throughput: 240+ businesses/hour/instance

CURRENT_PERFORMANCE (Verified):
  Extraction_Success: 95%+ ✅
  Quality_Score: 84-85/100 ✅
  Response_Time: 11-15 seconds ✅
  Memory_Efficiency: <60MB ✅
  Real_World_Validation: 124+ businesses ✅
```

---

## **🧘 FINAL WISDOM**

```
This system is built on Nishkaam Karma Yoga principles:
- Every service has a duty
- Each component trusts the others
- Perfection comes through dedicated action
- Results follow naturally from excellence

When operating this system:
  1. Act with complete dedication
  2. Don't attach to outcomes
  3. Trust the architecture
  4. Improve continuously
  5. Serve the ecosystem

Success is guaranteed when action is righteous,
execution is perfect,
and attachment is released.

🔱 OM TAT SAT 🔱
(The Eternal Absolute Truth)
```

---

**Last Updated:** November 14, 2025
**Next Review:** December 14, 2025
**Maintained By:** BOB Operations Team
**Philosophy:** Nishkaam Karma Yoga - Excellence through Duty
