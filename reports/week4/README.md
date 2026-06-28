# Traffic Processor (TP)

## Project Information

**Project Name:** Traffic Processor (TP)  
**Short Description:** A network visibility and control tool that captures live packet counters, per-connection statistics, traffic history, and supports blocking, tunneling, and failover behaviours.  
**Root LICENSE:** [LICENSE](/LICENSE)

- [Product backlog](https://github.com/SWP-Team-46/Traffic-Proccessor/issues)
- [Sprint backlog](https://github.com/orgs/SWP-Team-46/projects/1)
- [Sprint milestone](https://github.com/SWP-Team-46/Traffic-Proccessor/milestone/2)
- 1) Sprint Goal: Unite CN and TP, implement separate counters for incoming/outgoing packets, and improve documentation.
  2) Sprint Dates: 22/06/2026 – 28/06/2026
  3) Scope Summary: Combine cn.py and tproc.py into a single script (tproc.py), add separate counters for incoming/outgoing traffic, and produce comprehensive documentation for the release.
- Total story point in this sprint is **11**
- TP and CN are now united, TP now counts incoming/outcoming packets, more documentation
- [Deployed Product](http://147.45.234.218:8080)
- [README](/README.md)
- Customer feedback resulted in creation of [#36](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/36) and [#35](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/35) and [#74](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/74)
- All the provided feedback was addressed
- [Roadmap](/docs/roadmap.md)
- [Definition of done](/docs/definition-of-done.md)
- [Quality requirements description](/docs/quality-requirements.md)
- [Quality requirements tests](/docs/quality-requirements-tests.md)
- [Testing](/docs/testing.md)
- [User acceptance tests](/docs/user-acceptance-tests.md)
- The project uses the ISO/IEC 25010 quality model, with the following sub‑characteristics selected for the current sprint:
   Quality Requirement	ISO/IEC 25010 Sub‑characteristic
   - QR‑001 – Dashboard metric update delay	Time behaviour
   - QR‑002 – Traffic Processor startup time	Time behaviour
   - QR‑003 – Traffic Processor throughput capacity	Performance efficiency
- Testing status summary, including critical modules and per-module line coverage status.
   - Unit Tests: [test_TP+CN.py](/src/Traffic_Processor/test_TP+CN.py)
   - Quality Requirement Tests: [qr_test.py](/src/qr_test.py)
   - Coverage Report: Generated in CI as coverage-report artifact
   - CI Test Logs: [Available in GitHub Actions workflow runs](https://github.com/SWP-Team-46/Traffic-Proccessor/actions/runs/28325503855/job/83914700451)
- [TP unit tests](/src/Traffic_Processor/test_TP+CN.py)
- [Integration tests](/src/cnss/tests/cnss_test.py)
- [Quality requirement tests](/src/qr_test.py)
- [CI pipeline](/.github/workflows/main.yml)
- [Protected-default-branch CI run](https://github.com/SWP-Team-46/Traffic-Proccessor/actions/runs/28325503855)
- Main is protected by the following ruleset:
  - Require a pull request before merging
  - Block force pushes
  - Require conversation resolution before merging
  - Require 1 approval
- Screenshots or report links for linting, coverage, tests, and the additional QA check.
- The CI pipeline, test suite, and coverage thresholds established in Assignment 4 will become mandatory gates for every future pull request blocking merges if linting, unit tests, or coverage requirements fail. As new features are added, the test suite must grow alongside them to prevent regressions and maintain the coverage baseline. Finally, the Definition of Done will formally tie story completion to passing all CI checks and smoke tests, ensuring that "done" always means "production-ready"
- [v1.1.0](https://github.com/SWP-Team-46/Traffic-Proccessor/releases/tag/1.1.0)
- [CHANGELOG](/CHANGELOG.md)
- [Public sanitized demo video](https://drive.google.com/file/d/1iLPz6sNQj9lF-MKAiMHPLB9ERJgTGxWr/view?usp=drive_link)
- UAT results summary:

| UAT | Description | Result |
|-------|--------|-------|
| UAT‑001 | Verify Web Interface Displays Live Traffic Statistic | Passed |
| UAT‑002 | Verify Traffic Processor Operation via Docker | Passed |
| UAT‑003 | Verify Directional Traffic Classification | Passed |

No blocking issues were observed; only minor improvements to UAT‑003 instructions were noted and have been applied

- [Meeting transcript](/reports/week4/customer-review-transcript.md)
- [Meeting summary](/reports/week4/customer-review-summary.md)
- [Reflection](/reports/week4/reflection.md)
- [Retrospective](/reports/week4/retrospective.md)
- [LLM report](/reports/week4/llm-report.md)
- The Traffic Processor is now unified with the Communication Node into a single script. It correctly counts incoming and outgoing packets separately and displays these statistics via a web dashboard. The system is containerised with Docker Compose and passes all unit, quality, and user acceptance tests. The current release is v1.1.0
- Summary of the next steps:
  - Sprint 3 (29/06/2026 – 5/07/2026): Begin work on additional features (to be defined)
  - Sprint 4 (6/07/2026 – 12/07/2026): Further enhancements and polish
- Contribution traceability table mapping each team member to issues, PRs/MRs, review activity, testing, quality, automation, or documentation work:
  
| Team member | Issues authored | PRs authored | PRs reviewed | Testing work | Quality work | Automation / DevOps | Documentation work | Primary contribution areas |
|---|---:|---:|---:|---|---|---|---|---|
| `mrZom49` | 12 | 23 | 15 | PR #62 added unit tests; PR #73 created `qr_test.py`; PR #79 added coverage parameters; issues #57 and #65 tracked unit tests and test documentation. | Quality-requirement testing, coverage measurement and issue #24 addressing CN/TP data mismatch. | PR #47 added a Python workflow; PRs #55 and #56 implemented CI/CD; PR #66 added Lychee link checking. | PRs #81, #77 and #53 updated the README; PR #52 updated the changelog; PR #58 added transcript timestamps; PRs #20 and #2 added repository templates. | Backend and CN integration, CI/CD, testing, repository governance and documentation |
| `jan-ajata` | 7 | 9 | 13 | Issues #41-#43 defined latency and throughput test targets. No authored test-implementation PR was identified. | PR #37 created `quality-requirements.md`; issues #41–#43 specified measurable quality requirements. | No directly evidenced authored automation PR was identified. | PR #34 updated the README and images; PR #37 documented quality requirements; PR #31 added assignment material. | Frontend, frontend/backend integration, quality requirements and documentation |
| `inseeee` | 1 | 6 | 3 | Issue #18 defined manual system testing. No authored test-code PR was identified. | Reflection and retrospective records contributed to process-quality improvement. | No directly evidenced authored automation PR was identified. | PRs #29, #30, #59, #60, #71 and #72 created or updated reflection and retrospective documents. | Process documentation, retrospectives, reflection and manual-testing planning |
| `LimpingCoronation` | 1 | 4 | 1 | Issue #82 and open PR #83 added integration tests. | Integration-test implementation provided direct quality-assurance evidence. | PR #44 contained a DevOps update. | No clearly documentation-specific authored PR was identified. | CNSS/control-status server, DevOps and integration testing |
| `TimLih-h` | 1 | 10 | 21 | PRs #50 and #54 maintained the testing branch; PR #51 prepared the Traffic Processor for testing; open PR #84 finalized quality-requirement tests. | PR #84 mapped quality tests to issues #41–#43; issue #21 tracked design reworking. | No directly evidenced authored automation PR was identified. | PR #78 completed missing `/docs` and week-report documentation; PR #26 added a customer-review summary; PR #84 documented quality tests. | Traffic Processor implementation, testing, quality evidence, documentation and extensive review activity |
| **Total** | **22** | **52** | **53** |  |  |  |  |  |

- Screenshots:

  ![Milestone](./images/Milestone.jpg)
  ![Latest protected-default-branch CI run](./images/CI_pipeline_test_run.png)
  ![Branch protection or rules evidence](./images/Branch_protection.png)
  ![Coverage or test report](./images/test_report.png)
  ![Additional QA check result](./images/smoke_test.png)
  ![SemVer release](./images/Release.png)
  ![Example reviewed issue-linked PR/MR](./images/reviewed_issue-linked_PR.png)

<!--Include:

1. Project name and short description.
2. Link to the Product Backlog board/view.
3. Link to the Sprint Backlog board/table.
4. Link to the Assignment 4 Sprint milestone.
5. Sprint Goal, Sprint dates, and short scope summary.
6. Total Sprint size in Story Points.
7. Summary of delivered product changes.
8. Link to the deployed product, hosted artifact, package, or runnable product.
9. Link to current access or run instructions.
10. Customer feedback response table with feedback points and resulting PBIs or issues.
11. Explanation of feedback not addressed.
12. Link to `docs/roadmap.md`.
13. Link to `docs/definition-of-done.md`.
14. Link to `docs/quality-requirements.md`.
15. Link to `docs/quality-requirement-tests.md`.
16. Link to `docs/testing.md`.
17. Link to `docs/user-acceptance-tests.md`.
18. Summary of the quality model used and selected ISO/IEC 25010 sub-characteristics.
19. Testing status summary, including critical modules and per-module line coverage status.
20. Links to unit tests.
21. Links to integration tests.
22. Links to automated quality requirement tests.
23. Link to the CI pipeline.
24. Link to the latest protected-default-branch CI run.
25. Branch protection or rules evidence for the protected default branch.
26. Screenshots or report links for linting, coverage, tests, and the additional QA check.
27. Short explanation of how the Assignment 4 tests, CI checks, quality requirement tests, and Definition of Done will continue to govern later project work.
28. Link to the SemVer release mapped to the Assignment 4 Sprint increment.
29. Link to `CHANGELOG.md`.
30. Public sanitized demo video shorter than two minutes.
31. Optional link to `reports/week4/presentation.pdf` if the team publishes a sanitized public copy of the presentation slides.
32. Public sanitized UAT results summary.
33. Link to the published customer review transcript; state that the transcript is shared only through Moodle or an equivalent private instructor-sharing channel if public publication was refused but private sharing was permitted; or link to the customer review notes if recording or private sharing was refused.
34. Link to `reports/week4/customer-review-summary.md`.
35. Link to `reports/week4/reflection.md`.
36. Link to `reports/week4/retrospective.md`.
37. Link to `reports/week4/llm-report.md`.
38. Summary of the current product status.
39. Summary of the next steps.
40. Contribution traceability table mapping each team member to issues, PRs/MRs, review activity, testing, quality, automation, or documentation work.
41. Embedded screenshots from `reports/week4/images/` for:

    * Sprint milestone
    * Latest protected-default-branch CI run
    * Branch protection or rules evidence
    * Coverage or test report
    * Additional QA check result
    * SemVer release
    * Example reviewed issue-linked PR/MR

42. Include Product Backlog, Sprint Backlog, deployed product, or runnable artifact screenshots where relevant or where public links may not be inspectable by graders.-->
