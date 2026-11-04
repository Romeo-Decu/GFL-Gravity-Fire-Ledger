# External Audit and Cloud Governance — FiF v0.1

- **Status:** Adopted project process
- **Date:** 2026-11-04

## 1. Purpose

Independent model audits and cloud resources can improve FiF quality and verification coverage. They are supporting capabilities, not authorities that can silently change scientific conclusions, code or project scope.

The FiF Project Manager coordinates the process. The repository owner retains control of account authorization, protected branches and final merge decisions.

## 2. Independent external audit

### 2.1 Claude — final independent auditor

Claude is designated as the planned external auditor for a comprehensive audit after feature freeze and before release candidate approval.

The audit package will include:
- a pinned repository snapshot and commit SHA;
- scientific source register and source-to-claim traceability;
- combustion framework, assumptions and equations;
- physical comparability and transferability rules;
- schemas, engine, tests, test logs and known limitations;
- explicit questions and an audit report template.

Claude's scope:
1. Scientific correctness and dimensional consistency.
2. Source fidelity, attribution and provenance.
3. Combustion-regime assumptions and validity boundaries.
4. Transferability logic, inference profiles and abstention behavior.
5. Software architecture, deterministic behavior and test coverage.
6. Contradictions, missing evidence, unsupported claims and failure modes.
7. Reproducibility, security and operational limitations.
8. Prioritized defects and actionable remediation proposals.

Claude must distinguish confirmed defects, plausible concerns, missing evidence and optional improvements. It must cite exact files/lines or source locations and provide reproducible reasoning.

### 2.2 Mistral — adversarial review

The Mistral Adversarial Auditor role is suitable for a separate red-team review. It should challenge assumptions, attempt counterexamples, test whether rules can be gamed, and search for false confidence or invalid transfer conclusions.

For independence:
- Claude and Mistral receive the same frozen snapshot and audit questions.
- Each submits its findings before seeing the other's report.
- Neither has authority to merge changes or rewrite the scientific record.
- The FiF team triages findings, records accept/reject/defer decisions with reasons, and tests accepted fixes.

### 2.3 Access model

Preferred access order:
1. Frozen source bundle or read-only repository access.
2. Read-only GitHub collaborator permission if required.
3. No write access, secrets, cloud credentials, billing permissions or branch administration for auditors.

Do not connect external auditors during active implementation merely for convenience. Early consultation may be used for a narrowly defined question, but the formal audit occurs after feature freeze.

## 3. Azure and AWS resources

Azure for Startups and AWS Startup acceptance are valuable options for later platform verification. They do not automatically grant this assistant direct access to either account.

Use cloud resources only after:
- the relevant service and test purpose are documented;
- budget limits, quotas and shutdown policies are defined;
- credentials are provisioned through the provider's secure identity/secret mechanisms;
- least-privilege access is applied;
- no secrets are committed to Git or pasted into chat;
- cloud use is reproducible and logged.

Initial use cases:
- clean Windows and Linux compatibility testing;
- reproducible CI runners and environment matrices;
- controlled performance/load tests when local or GitHub-hosted runners are insufficient;
- later deployment prototypes, only after the application architecture and security model are stable.

Do not provision always-on infrastructure for the current documentation/engine milestone. Prefer ephemeral runners and short-lived test resources.

## 4. Cloud execution strategy

- GitHub Actions remains the default CI system for software tests.
- Azure and AWS are optional test environments, not competing sources of truth.
- Use workload identity federation/OIDC where supported rather than long-lived access keys.
- Store any required secrets in GitHub Actions or the cloud provider's secret manager.
- Set explicit spend alerts, hard limits where available, resource tags and automatic teardown.
- Test on one cloud first; add the second only when a distinct requirement justifies it.

## 5. Decision authority

External audits provide findings and recommendations, not binding decisions. Cloud providers provide infrastructure, not scientific validation. The PM coordinates triage and implementation; the repository owner retains final account and merge authorization.

No external agent may silently alter source evidence, overwrite raw measurements, or convert an unresolved issue into a resolved scientific assertion.
