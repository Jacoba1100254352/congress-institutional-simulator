# Simulation Backlog

This file lists the exact simulations that should be added before treating the paper draft as more than an exploratory working paper.

## Immediate Priority

### 1. Challenge-Voucher Parameter Sweep

Purpose: determine whether scarce contestation rights can preserve default-pass throughput while reducing low-support passage, policy shift, and proposer gain.

Add campaign `v3-challenge-sweep` with:

- `tokensPerParty`: 3, 6, 10, 15, 25
- `challengeThreshold`: 0.50, 0.65, 0.82, 1.00, 1.25
- allocation mode: per-party fixed, per-party proportional to seats, minority bonus, per-legislator
- challenged path: simple majority active vote, 60 percent active vote, committee review, committee information plus active vote

Run for:

- baseline
- two-party
- multi-party
- high-polarization
- high-proposal-pressure
- extreme-proposal-pressure
- lobby-fueled-flooding
- low-compromise-flooding

Report:

- productivity
- enacted/run
- challengeRate
- low-support passage
- policy shift
- proposer gain
- welfare
- token exhaustion by party or bloc
- false-negative pass rate once a welfare/legitimacy classifier exists

Decision target:

- identify whether challenge vouchers work best as fixed scarce rights, proportional rights, or minority-protection rights.

### 2. Proposal-Cost Parameter Sweep

Purpose: determine whether the current proposal-cost finding is robust or an artifact of one cost formula.

Add campaign `v4-cost-sweep` with:

- `baseCost`: 0.05, 0.15, 0.25, 0.34, 0.45, 0.60
- `publicCreditWeight`: 0.00, 0.15, 0.30, 0.50
- `lobbyCreditWeight`: 0.00, 0.10, 0.25, 0.50
- Scenarios: default-pass, default-pass-cost, default-pass-cost-guarded
- Cases: baseline, high-proposal-pressure, extreme-proposal-pressure, high-lobbying, lobby-fueled-flooding, low-compromise-flooding
- Runs: at least 300 per cell after code is stable

Report:

- enacted/run
- floor/run
- productivity
- low-support passage
- policy shift
- proposer gain
- welfare
- lobby-skew metric once implemented

Decision target:

- identify cost settings that reduce floor load without increasing low-support passage or proposer gain.

### 3. Proposal-Cost Mechanism Variants

Purpose: compare different definitions of "cost" instead of only tuning one threshold.

Add these `ProposalAccessRule` variants:

- `fixed-cost`: current rule.
- `public-interest-waiver`: cost falls as public benefit or public support rises.
- `lobby-surcharge`: cost rises with positive lobby pressure rather than treating lobbying as credit.
- `member-quota`: each legislator has limited proposal slots per session.
- `signature-threshold`: floor access requires cosponsors across ideological or party distance.
- `refundable-deposit`: proposals pay a cost that is refunded if public support, welfare, or bipartisan support clears a target.
- `calendar-scarcity`: only the top N proposals by agenda score reach floor consideration.

Add scenarios:

- `default-pass-cost-fixed`
- `default-pass-cost-public-waiver`
- `default-pass-cost-lobby-surcharge`
- `default-pass-member-quota`
- `default-pass-signature-threshold`
- `default-pass-refundable-deposit`
- `default-pass-calendar-scarcity`

### 4. Proposal-Flooding Severity Sweep

Purpose: separate rule behavior at normal proposal volume from behavior under flood conditions.

Add campaign cases with potential bills per run:

- 60, 120, 180, 300, 600

Run for:

- simple-majority
- supermajority-60
- default-pass
- default-pass-access
- default-pass-cost variants
- default-pass-informed-guarded

Report all percentage metrics plus absolute load metrics. The key output is a curve showing whether each institution scales linearly, saturates, or collapses under high proposal volume.

### 5. Agenda Order-of-Operations Sweep

Purpose: determine whether order matters when multiple guardrails exist.

Compare:

- cost -> access -> information -> committee -> floor
- access -> cost -> information -> committee -> floor
- information -> access -> cost -> committee -> floor
- committee -> information -> cost -> floor
- calendar scarcity -> information -> floor

Report:

- floor/run
- committee workload
- access denial
- committee rejection
- low-support passage
- welfare
- proposer gain

### 6. Robustness and Uncertainty Reporting

Purpose: make paper claims statistically defensible.

Add campaign infrastructure for:

- repeated seed batches
- mean
- standard deviation
- 5th, 50th, and 95th percentiles
- 95 percent confidence intervals where appropriate
- scenario ranking stability

Minimum for paper draft:

- 50 seed batches for the final tables.
- 1,000 runs per scenario/case for the final main campaign if runtime allows.

## Near-Term Model Additions

### 7. Endogenous Proposal Strategy

Purpose: stop treating proposal flooding as only an exogenous bill-count multiplier.

Add proposer strategies:

- `sincere`: propose near own ideal point.
- `compromise-seeking`: propose near expected median or blocking pivot.
- `flooding`: submit multiple variants around own ideal point.
- `lobby-backed`: propose where lobby pressure is strongest.
- `credit-claiming`: propose high-salience items even if passage quality is weak.

Report:

- proposals attempted per legislator
- proposals reaching floor per legislator
- enacted proposer concentration
- proposer gain by strategy
- welfare by strategy

### 8. Lobbying as Proposal Shaping

Purpose: model lobbying before the vote, not only as vote pressure.

Add:

- lobbyist budget
- choice between drafting subsidy, coalition subsidy, and reputation defense
- policy-position shift from public-benefit optimum toward private-benefit optimum

Compare:

- no lobbying
- vote-pressure-only lobbying
- proposal-shaping lobbying
- coalition-subsidy lobbying

### 9. Amendment and Negotiation Rounds

Purpose: model compromise as a process rather than only as a voting disposition.

Add:

- amendment offer stage
- proposer accepts or rejects amendment
- committee substitute bill
- minority amendment right
- median-pivot amendment
- bipartisan amendment requirement

Metrics:

- amendment count
- distance moved toward chamber median
- distance moved toward affected minority
- final coalition breadth
- welfare change after amendment

### 10. Minority-Protection Guardrails

Purpose: test whether default enactment can be paired with rights-preserving mechanisms.

Add scenarios:

- `default-pass-minority-veto`: veto by affected minority bloc above threshold.
- `default-pass-objection-window`: delay plus superminority objection sends bill to ordinary majority vote.
- `default-pass-rights-review`: simulated court or rights panel blocks high-harm bills.
- `default-pass-citizen-review`: citizen panel can require ordinary floor passage for low-support bills.

### 11. Sunset and Delay Rules

Purpose: test default enactment with reversible or time-limited policy changes.

Add:

- automatic sunset after N sessions
- delayed enactment period
- renewal vote threshold
- pilot-program rule for high-uncertainty bills

Metrics:

- policy volatility
- bad-law duration
- reversal rate
- welfare over time

## Validation Simulations

### 12. U.S.-Style Baseline Calibration

Purpose: make the simulator credible before using counterfactuals.

Target approximate reproduction of:

- party unity rates
- roll-call coalition sizes
- bill progression from introduction to floor
- enacted-law rate
- veto and override frequency
- ideology distribution

Data targets:

- Voteview for ideology and roll calls.
- Congress.gov or govinfo for bill histories.
- Center for Effective Lawmaking for productivity comparison.

### 13. Comparative Institution Baselines

Purpose: avoid overfitting to one U.S.-style baseline.

Add stylized baselines for:

- parliamentary majority government
- minority government under negative parliamentarism
- multiparty coalition legislature
- consensus-oriented council
- technocratic commission proposal plus legislative disapproval

Use these as institutional analogues rather than exact country models until calibrated data are added.

## Paper Readiness Gate

The paper should not make strong claims until these are complete:

- challenge-voucher sweep implemented and reported.
- proposal-cost sweep implemented and reported.
- uncertainty reporting implemented.
- at least one validation baseline attempted.
- formal references cleaned up from the prior-art report.
- sensitivity checks show that main conclusions survive plausible parameter changes.
