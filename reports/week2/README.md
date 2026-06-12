# Week 2 Report – Traffic Processor (TP)

## Project Information

**Project Name:** Traffic Processor (TP)  
**Short Description:** A network visibility and control tool that captures live packet counters, per-connection statistics, traffic history, and supports blocking, tunneling, and failover behaviours.  
**Root LICENSE:** [LICENSE](/LICENSE)

---

## User Stories

- [User Stories (reports/week2/user-stories.md)](./user-stories.md)

---

## Selected Prototype and Interface Artifacts

This project currently defines a **graphical web interface** as the primary user-facing artifact.

- **Interactive Prototype (Figma / Balsamiq / etc.):**  
  [Link to interactive prototype – replace with actual URL]  
  *Example:* `https://www.figma.com/proto/...`

*Note:* For an API interface, the following would be provided:  
- OpenAPI specification  
- Swagger UI  
- Accessible implementation/mock  
- Postman collection  

For a non-graphical interface:  
- Interactive mock/demonstration  
- [docs/interface.md](/docs/interface.md)

---

## MVP v0

- [MVP v0 Report (reports/week2/mvp-v0-report.md)](./mvp-v0-report.md)
- **Deployed MVP v0 or Runnable Artifact:**  
  [Link to deployment / runnable artifact – replace with actual URL]  
  *Example:* `http://localhost:8080` or `https://tp-mvp-v0.herokuapp.com`
- **Run Instructions:**  
  ```bash
  git clone <repo-url>
  cd traffic-processor
  npm install
  npm start

  - **Public Video Demonstration:**  
  [Link to YouTube / Loom – replace with actual URL]

---

## Pull Request Template & Reviewed PRs

- **Minimal PR/MR Template:**  
  [Link to `.gitlab/merge_request_templates/default.md` or `.github/pull_request_template.md`]
- **Reviewed PRs/MRs created during Week 2:**  
  - [PR #1 – Add basic packet counting](replace-with-actual-url)  
  - [PR #2 – Web dashboard skeleton](replace-with-actual-url)  
  *(Add actual links as needed)*

---

## Lychee Link Checking

- **Lychee Configuration:**  
  [Link to `.lychee.toml` or similar config file]
- **Latest successful protected‑default‑branch run:**  
  [Link to CI/CD pipeline run – replace with actual URL]

### Excluded Lychee Links

The following links are intentionally excluded from Lychee checks with justification:

| Excluded Link | Justification |
|---------------|----------------|
| `http://localhost:8080` | Local development server, not publicly accessible |
| `https://internal-corpo-network/*` | Internal network resources (example) |
| *(Add others as needed)* | |

✅ **Manual verification performed:** Each excluded link has been visited in a browser and confirmed accessible before submission.

---

## Screenshots

*(All screenshots stored in `reports/week2/images/` as PNG files)*

### 1. Protected Default Branch Settings

![Protected Branch Settings](./images/protected-branch-settings.png)

### 2. Example Reviewed PR/MR (Review by another team member)

![Reviewed PR Example](./images/reviewed-pr-example.png)

### 3. Selected Prototype and Interface Artifacts

![Prototype Screenshot](./images/prototype-screenshot.png)

### 4. Deployed MVP v0 or Runnable Artifact

![MVP v0 Running](./images/mvp-v0-running.png)

---

## Coverage

### Stable IDs Covered by the Prototype

- **US-01** – Basic Packet Counting  
- **US-02** – Web Dashboard  
- **US-04** – Collect and Display Per‑Connection Statistics  
- **US-06** – Traffic Statistics History  

### Selected Prototype Artifacts

The interactive prototype (Figma) covers the **graphical dashboard** and **packet/connection statistics view**, representing US-01, US-02, US-04, and US-06. It demonstrates the layout, data tables, and real-time counter elements without backend integration.

### MVP v0 Foundation

[MVP v0 Report](./mvp-v0-report.md) explains the MVP v0 foundation (e.g., project scaffolding, basic web server, dummy packet counter endpoint). It documents a repeatable smoke‑check scenario.

### Stable User‑Story IDs Represented by MVP v0

MVP v0 establishes the foundational infrastructure for:
- **US-01** (Basic Packet Counting) – dummy endpoint in place  
- **US-02** (Web Dashboard) – HTML skeleton served  
- **US-09** (Monitor TP Health) – health check endpoint included  

*Note:* MVP v0 is a product foundation and does not yet fully implement any complete user story.

---

## Customer Meeting

- **Published Customer Transcript (if publication permitted):**  
  [Customer Meeting Transcript](./customer-meeting-transcript.md)

- **Customer Meeting Notes (if recording or private sharing refused):**  
  [Customer Meeting Notes](./customer-meeting-notes.md)

- **Customer Meeting Summary:**  
  [Customer Meeting Summary](./customer-meeting-summary.md)

*Note:* If the transcript is included only in Moodle with the customer's permission, please state that here.

---

## Week 2 Analysis

[Week 2 Analysis](./analysis.md)

---

## LLM Report

[LLM Report](./llm-report.md)
