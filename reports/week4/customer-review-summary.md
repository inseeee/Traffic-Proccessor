# Customer Review Summary — Week 4

**Date:** 2026-06-28

**Participants:**
- **Customer:** Mikhail Kuskov
- **Team:** Aidar Badykov, Timur Likhunov, Alan Usanov, Alexandr Voronin

**Artifacts demonstrated:**
- Updated Traffic Processor running in Docker containers
- Web interface showing packet counters
- User Acceptance Tests

---

## Sprint Goal Reviewed

**Sprint Goal:** Deliver the updated Traffic Processor, verify all user acceptance tests pass, and prepare the next development direction based on customer feedback.

**Short scope summary:**
- Updated TP is accepted by the customer
- Customer verified all three user acceptance test scenarios
- Future development vector should be explicitly discussed

---

## Delivered Increment Discussed

1. **Income/outcome separation** — The team demonstrated that the TP now separates traffic in both directions. The separation works first at the IP level and then at the MAC address level. IPv6 is not yet supported.

2. **Docker-based deployment** — The project runs on Docker, and the team demonstrated container control and ping tests.

3. **Relevant UI/UX improvments** - The web interface matches new functionality.

---

## UAT Results

| Test Scenario | Result | Notes |
|---------------|--------|-------|
| Ping from inside container | Pass | Packet generation observed every ~2 seconds |
| External ping to remote server | Pass | Tested with 4 packets to 1.1.1.1 |
| Traffic counting verification | Pass | Data persisted and visible; counters do not auto-reset |

**Customer observation:** Packets appear every 2 seconds instead of 1, which is unexpected but acceptable.

---

## Quality Evidence Discussed

- **Unit tests** — Available in `src/Traffic_Processor/test_TP+CN.py`
- **CI pipeline** — Configured in `.github/workflows/main.yml`
- **Definition of Done** — Documented
- **Quality requirements** — Documented with corresponding tests
- **User acceptance tests** — Documented
- **Protected branch** — Branch protection rules in place

---

## Feedback

### Positive Feedback
- Protocol separation works correctly in both directions
- The current functionality is good and useful
- The three test scenarios are appropriate

### Requested Changes / Improvements

1. **Reset button for counters** — The customer noted that refreshing the page does not reset counters. A reset button (or automatic reset on page load) is a **high‑priority** addition.

2. **Update delay fix** — Bug with 2-seconds update better be fixed.

---

## Approvals

- **New functionality is approved**
- **UATs are approved**

---

## Risks

| Risk | Mitigation |
|------|------------|
| File‑based communication creates tight coupling between components | Network‑based communication planned for future sprints |
| Timing issues between file writes and reads | To be fixed |
| Loop traffic counts only as incoming, but should increment both counters | Backlog item for future sprint |
| No persistent history / database | Identified as one of three future directions |

---

## Action Points

1. **Add reset button for counters** — High priority
2. **Team discussion** on whether to pursue physical hardware (Raspberry Pi) or focus on the three functional directions

---

## Resulting Product Backlog / Scope Changes

### New / Confirmed Backlog Items

| Priority | Item | Source |
|----------|------|--------|
| **Should** | Add reset button for counters | Week 4 feedback |
| **Should** | Network‑based communication (replace file‑based) | Week 3 feedback |
| **Could** | IPv6 support | Week 4 discussion |
| **To be decided** | Database for historical data | Week 4 discussion |

### Three Future Directions (Customer‑prioritized, equal priority)

1. **Traffic modification** — Blocking/allowing packets, enabling/disabling interfaces
2. **Advanced statistics** — Second screen with port‑based breakdown, IP‑based filtering, application‑level distinction
3. **Historical data** — Database integration to show traffic dynamics over time

### Approximate next sprint Scope
- Replace file‑based communication with network‑based communication
- Bidirectional traffic visualization
- Database integration

---
- SemVer release mapped to the Assignment 4 Sprint increment【9†L38–L39】

---

*This summary was prepared based on the customer review transcript from 2026-06-28 and previous week reports.*
