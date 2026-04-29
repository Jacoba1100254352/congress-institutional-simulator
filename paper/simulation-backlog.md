# Simulation Backlog

This file lists the exact simulations that should be added before treating the paper draft as more than an exploratory working paper.

## Completed Simulation Increments

### 1. Challenge-Voucher Parameter Sweep

Purpose: determine whether scarce contestation rights can preserve default-pass throughput while reducing low-support passage, policy shift, and proposer gain.

Implemented campaign `simulation-campaign-v3` with:

- `tokensPerParty`: 3, 6, 10, 15, 25
- `challengeThreshold`: 0.50, 0.65, 0.82, 1.00, 1.25
- allocation mode: fixed per-party and per-legislator
- tokenless q-member escalation at q=6, q=12, and q=20
- challenged path: simple majority active vote

Run for the full v1/v2 assumption set:

- baseline
- low-polarization
- high-polarization
- low-party-loyalty
- high-party-loyalty
- low-compromise
- high-compromise
- low-lobbying
- high-lobbying
- weak-constituency
- two-party
- multi-party
- high-proposal-pressure
- extreme-proposal-pressure
- lobby-fueled-flooding
- low-compromise-flooding

Reported:

- productivity
- enacted/run
- challengeRate
- low-support passage
- policy shift
- proposer gain
- welfare

Current finding:

- fixed party-token budgets produce a throughput/safety frontier. Three tokens per party preserves high throughput but barely reduces low-support passage. Ten tokens per party is the middle path. Higher party-token budgets, per-legislator tokens, and q-member escalation reduce low-support passage and policy shift much more, but at costs that approach heavy review.

Still not implemented:

- per-party proportional tokens
- minority-bonus token allocation
- challenged paths using 60 percent vote, committee review, or committee information plus active vote
- token exhaustion by party or bloc
- false-negative pass rate once a welfare/legitimacy classifier exists

### 2. Cross-Bloc Cosponsorship Gate

Purpose: test whether proposal access based on coalition breadth reduces proposer gain without relying on committee gatekeeping or scalar costs.

Implemented campaign `simulation-campaign-v4` with:

- `default-pass-cross-bloc`
- `default-pass-cross-bloc-strong`
- `default-pass-cross-bloc-challenge`

Reported:

- floor/run
- productivity
- access-denial rate
- low-support passage
- policy shift
- proposer gain
- public welfare
- challenge rate for the combined gate/challenge scenario

Current finding:

- cross-bloc cosponsorship is a strong upstream screen. The default gate reduced floor consideration by 0.789 and low-support passage by 0.240 relative to open default-pass, while improving enacted-bill welfare from 0.469 to 0.646. The strong gate raised welfare further to 0.740 but admitted only 0.069 productivity, so coalition breadth needs either softer parameters or adaptive routing.

Still not implemented:

- explicit cosponsor lists on bills
- cross-party or cross-bloc admission-rate metric separate from access denial
- reciprocity or fake cosponsorship trading
- agenda-credit discounts for broader sponsorship
- affected-group sponsorship as distinct from party-bloc sponsorship

### 3. Adaptive Procedural Tracks

Purpose: stop treating all bills as identical procedural objects.

Implemented campaign `simulation-campaign-v5` with:

- `default-pass-adaptive-track`
- `default-pass-adaptive-track-challenge`

Routing criteria:

- salience
- public support
- policy shift
- lobby pressure
- generated public benefit
- generated public-support/public-benefit disagreement as an uncertainty proxy

Reported:

- floor/run
- productivity
- access-denial rate
- committee-rejection rate
- challenge rate
- low-support passage
- policy shift
- proposer gain
- public welfare

Current finding:

- adaptive tracks provide a middle path between open default-pass and heavy agenda gates. The non-challenge adaptive track reduced productivity by 0.418 relative to open default-pass, but reduced low-support passage by 0.192, policy shift by 0.474, and proposer gain by 0.278 while keeping floor consideration at 0.925. The challenge-middle-lane variant preserved more productivity, 0.566, but left more low-support passage, 0.367.

Still not implemented:

- explicit route-rate metrics for fast, middle, and high-risk lanes
- calibrated uncertainty field on bills
- adaptive thresholds swept over low-risk and high-risk cut points
- high-risk lanes using expert review, citizen panels, or supermajority active votes

### 4. Sunset Trial Legislation

Purpose: test whether reversibility reduces the permanent harm of weakly supported default enactments.

Implemented campaign `simulation-campaign-v6` with:

- `default-pass-sunset-trial`
- `default-pass-sunset-challenge`

Reported:

- enacted/run
- productivity
- public welfare
- low-support passage
- policy shift
- proposer gain
- challenge rate for the combined sunset/challenge scenario

Current finding:

- sunset review improves enacted-bill welfare and reduces volatility without a front-end agenda gate. The basic sunset trial reduced productivity by 0.394 relative to open default-pass, but increased welfare by 0.114, reduced low-support passage by 0.075, reduced policy shift by 0.427, and reduced proposer gain by 0.208. Combining sunset review with challenge vouchers reduced policy shift by 0.500 and proposer gain by 0.279, but productivity fell to 0.368.

Still not implemented:

- active law registry with delayed review after multiple rounds
- explicit repeal or nonrenewal metric separate from failed enactment
- active-law welfare and low-support active-law share
- review-period sensitivity sweep
- partial rollback or amendment instead of full rollback

### 5. Earned Proposal Credits

Purpose: replace the scalar proposal-cost rule with agenda rights earned or lost through prior proposal quality.

Implemented campaign `simulation-campaign-v7` with:

- `default-pass-earned-credits`
- `default-pass-earned-credits-challenge`

Reported:

- floor/run
- access-denial rate
- low-support passage
- policy shift
- proposer gain
- public welfare
- challenge rate for the combined credit/challenge scenario

Current finding:

- earned proposal credits are a mild agenda-accountability layer. The base credit scenario denied 0.200 of potential proposals, reduced productivity by 0.166 relative to open default-pass, increased welfare by 0.015, reduced low-support passage by 0.010, reduced policy shift by 0.159, and reduced proposer gain by 0.032. Combining credits with challenge vouchers is much stricter: productivity falls by 0.398 relative to open default-pass, but low-support passage falls by 0.101, policy shift by 0.416, and proposer gain by 0.191.

Still not implemented:

- proposer concentration or access-gini metrics
- party-level or coalition-level credit pools
- refundable public-benefit bonds
- credit transfers, hoarding, or collusion
- welfare per submitted bill

## Immediate Priority

### 6. Structured Amendment and Mediation

Purpose: add bargaining over bill content before the final yes/no vote.

Add scenarios:

- `default-pass-mediated-amendments`
- `default-pass-mediated-amendments-challenge`
- `adaptive-track-mediated-middle`
- `sunset-trial-mediated-review`

Report:

- compromise movement toward chamber median
- compromise movement toward public median
- amendment success rate
- low-support passage
- policy shift
- proposer gain
- welfare
- amendment load

## Later Priority

### 7. Proposal-Cost Parameter Sweep

Purpose: determine whether the current proposal-cost finding is robust or an artifact of one cost formula.

Add campaign `v7-cost-sweep` with:

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

### 8. Proposal-Cost Mechanism Variants

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

### 9. Proposal-Flooding Severity Sweep

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

### 10. Agenda Order-of-Operations Sweep

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

### 11. Robustness and Uncertainty Reporting

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

### 12. Endogenous Proposal Strategy

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

### 13. Lobbying as Proposal Shaping

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

### 14. Amendment and Negotiation Rounds

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

### 15. Minority-Protection Guardrails

Purpose: test whether default enactment can be paired with rights-preserving mechanisms.

Add scenarios:

- `default-pass-minority-veto`: veto by affected minority bloc above threshold.
- `default-pass-objection-window`: delay plus superminority objection sends bill to ordinary majority vote.
- `default-pass-rights-review`: simulated court or rights panel blocks high-harm bills.
- `default-pass-citizen-review`: citizen panel can require ordinary floor passage for low-support bills.

### 16. Sunset and Delay Rules

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

### 17. U.S.-Style Baseline Calibration

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

### 18. Comparative Institution Baselines

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
