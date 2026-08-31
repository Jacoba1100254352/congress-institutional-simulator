# Presidential-Choice Transport Study: Locked Pre-Fit Specification

Status: locked after source construction and descriptive source audit, before
estimator implementation or model fitting.

Lock date: 2026-08-30.

## Purpose and Status

This specification fixes a narrow temporal transport study for presidential
veto choice among measures presented to the President. The study asks whether
a small set of pre-decision institutional and final-vote signals improves
probability forecasts over a training-period veto-rate baseline in a later,
whole-Congress cohort.

This is not a blinded or prospective preregistration. Before this document was
locked, the source panels, veto labels, event counts, vote-recording coverage,
and descriptive strata had already been inspected to verify source integrity
and define the study boundary. No regression model has been implemented or fit,
and no candidate penalty, feature set, or acceptance threshold has been compared
using fitted results. The later Congress is therefore a frozen temporal test
cohort, but not an outcome-blind test cohort.

The study is predictive and descriptive. It does not estimate the causal effect
of divided government, sponsorship, chamber support, or party support on veto
choice. It also does not validate the simulator's welfare, representation, or
institutional-ranking claims.

## Frozen Source Population

The unit of observation is one H.R., S., H.J.Res., or S.J.Res. measure presented
to the President during the 108th through 118th Congresses.

Decision records come from:

- `data/validation/raw/govinfo_executive_action_panel.csv` for H.R. and S.
  measures;
- `data/validation/raw/govinfo_joint_resolution_panel.csv` for H.J.Res. and
  S.J.Res. measures; and
- `data/validation/raw/govinfo_final_chamber_vote_panel.csv` for the selected
  final House and Senate approval actions and any corresponding official roll
  calls.

The two decision panels contain 4,208 presentments: 4,021 H.R./S. bills and 187
joint resolutions. They contain 47 initial veto decisions and six later
overrides. The final-vote panel contains exactly two rows per presentment, one
for each chamber. It identifies 310 measures with final recorded votes in both
chambers, 1,065 with one recorded final vote, and 2,833 with no recorded final
vote. A voice vote, unanimous-consent action, or other nonrecorded final
approval is not replaced with an earlier recorded vote.

The outcome is `vetoed`, defined at the initial presidential decision. A veto
later overridden remains a veto outcome. Override is not modeled because there
are only six overrides; override counts and rates remain separate descriptive
results.

The study must fail before fitting if any of these conditions is not satisfied:

1. The decision panels contain 4,208 unique bill IDs and 47 vetoes.
2. The final-vote panel contains exactly two valid rows for every decision bill
   ID, one House row and one Senate row.
3. Official recorded-vote rows pass their source-hash, bill-match, arithmetic,
   and party-subtotal integrity checks.
4. No nonrecorded final approval has an imputed support value.
5. Every decision row has a Congress from 108 through 118 and a valid binary
   veto label.

## Temporal Splits

The primary test is fixed as follows:

- training cohort: 108th through 117th Congresses, 3,921 measures and 34
  vetoes;
- test cohort: 118th Congress, 287 measures and 13 vetoes.

A secondary earlier transport check is fixed as follows:

- training cohort: 108th through 115th Congresses, 3,203 measures and 24
  vetoes;
- test cohort: 116th Congress, 353 measures and 10 vetoes.

The two split-specific models are fit independently using only their stated
training Congresses. The 116th-Congress result may not alter the features,
penalty, solver, metrics, or acceptance rule used for the 118th-Congress test.
The implementation will produce both fixed evaluations in one deterministic
run.

## Frozen Predictors

The reference category is an H.R./S. measure under unified government with a
same-party sponsor and no recorded final chamber vote. All predictors are known
by presentment. This temporal ordering does not make their associations causal.

### Structural Model M1

M1 contains an intercept and these six predictors:

1. `joint_resolution`: 1 for H.J.Res. or S.J.Res.; 0 for H.R. or S.
2. `divided_government`: 1 when `government_control` is `divided`; otherwise 0.
3. `opposition_party_sponsor`: 1 when both the President and sponsor have a
   major-party label in {D, R} and the labels differ; otherwise 0.
4. `other_or_unknown_sponsor`: 1 when the sponsor party is missing or is not in
   {D, R}; otherwise 0. A same-party major-party sponsor is the omitted sponsor
   category.
5. `any_final_roll_call`: 1 when either chamber's selected final approval is an
   official recorded roll call; otherwise 0.
6. `both_final_roll_calls`: 1 when both chambers' selected final approvals are
   official recorded roll calls; otherwise 0.

### Support Model M2

M2 is the primary model. It contains every M1 term plus exactly two support
predictors:

7. `minimum_observed_final_support`: among chambers with an official selected
   final roll call, the minimum `yea / (yea + nay)` support share minus 2/3. If
   neither chamber has a recorded final roll call, this predictor is 0.
8. `minimum_observed_opposition_support`: among chambers with an official
   selected final roll call, the minimum support share among members of the
   major party opposite the President minus 1/2. If neither chamber has a
   recorded final roll call, this predictor is 0.

For a measure with only one recorded chamber, that chamber supplies each
minimum. Present, not-voting, paired, and other non-yea/non-nay categories are
excluded from support-share denominators. The explicit roll-call indicators
identify whether the zero support deviations represent missing/nonrecorded
votes. Support is never imputed from an earlier vote, another bill, party
composition, passage mode, or the outcome.

No interactions, policy-area terms, origin-chamber terms, administration or
Congress fixed effects, time trend, ideal points, public-opinion variables, or
post-presidential-decision variables are permitted. Sponsor-party relation is
metadata, not a policy-distance measure.

## Scaling

Within each temporal split and model, every non-intercept predictor is
standardized using the training-cohort mean and population standard deviation
(denominator `n`). The same training values are applied to the test cohort.

A predictor with exactly zero training standard deviation is omitted from that
split's fit and reported as `omitted_zero_training_variance`. It is not replaced
or combined with another predictor. The intercept is neither standardized nor
penalized.

## Frozen Comparators

The study reports four probability forecasts:

- M0, training prevalence: every test row receives the veto rate in that
  split's training cohort;
- M1, the structural penalized logistic model;
- M2, the primary support penalized logistic model; and
- simulator constant: every row receives the frozen simulator conditional veto
  rate, 647 / 2,621 = 0.246852... .

The simulator constant is a scale diagnostic, not a fitted bill-level model and
not a candidate selected against M0, M1, or M2. M1 is a fixed ablation. Model
choice may not depend on which model performs best.

## Frozen Estimator

M1 and M2 use logistic regression with a fixed L2 penalty. For coefficient
vector `(alpha, beta)`, the maximized objective is:

```text
sum_i [y_i * eta_i - log(1 + exp(eta_i))]
    - (lambda / 2) * sum_j beta_j^2
```

where `eta_i = alpha + x_i beta`, the intercept `alpha` is unpenalized, and
`lambda = 0.16`. On the standardized slope scale, this penalty corresponds to
independent zero-centered Normal priors with standard deviation 2.5. Lambda is
fixed and is not tuned.

The implementation must use a deterministic damped Newton/IRLS solver with:

- all coefficients initialized to zero;
- a direct partial-pivoting linear solve for each Newton step, with a pivot
  magnitude below `1e-14` treated as singular;
- an Armijo backtracking line search beginning at step size 1 and halving as
  needed, using constant `1e-4` and at most 50 halvings;
- an infinity-norm gradient tolerance of `1e-9`;
- an infinity-norm accepted-step tolerance of `1e-10`;
- at most 200 iterations; and
- a hard error for a singular system, failed line search, nonfinite value, or
  failure to converge.

After an accepted step, convergence requires both the new gradient infinity
norm and the accepted-step infinity norm to meet their stated tolerances.

The implementation must use stable log-sum-exp and sigmoid calculations.
Probabilities may be clipped to `[1e-12, 1 - 1e-12]` only where needed to
evaluate logarithms in reported loss. There is no class weighting, resampling,
cross-validation, threshold optimization, variable selection, or penalty
tuning.

## Frozen Evaluation

Metrics are computed separately for the 116th- and 118th-Congress test cohorts
using unrounded probabilities:

1. mean log loss, the primary scoring rule;
2. Brier score, a secondary scoring rule;
3. calibration-in-the-large, defined as mean predicted veto probability minus
   the observed veto rate;
4. observed veto count and rate; and
5. mean, minimum, and maximum predicted probability.

No classification threshold, accuracy, precision, recall, F score, ROC AUC,
coefficient-sign gate, statistical-significance test, or post hoc subgroup gate
is part of the study.

The primary 118th-Congress transport gate passes only if M2 satisfies both of
these conditions using full-precision metrics:

1. M2 mean log loss is strictly lower than M0 mean log loss.
2. The absolute M2 calibration-in-the-large is at most 0.020.

The two-percentage-point calibration tolerance is fixed before fitting. Brier
score is reported but does not determine the gate. M1 and the 116th-Congress
check are descriptive fixed comparisons and do not determine the gate.

All model and comparator results must be reported whether the gate passes or
fails. A failure must be retained as evidence that this fixed model does not
transport under the stated rule; it may not be tuned away in the same study.

## Required Outputs and Reproducibility

The implementation must write, at minimum:

- a machine-readable metric table with one row per split and model;
- a coefficient table with split, model, feature, scaling, coefficient, and
  omission status;
- row-level test predictions with bill ID, Congress, observed outcome, and all
  four forecast probabilities;
- a human-readable report that states the primary gate result and limitations;
  and
- metadata containing SHA-256 hashes for this specification and all three
  source panels.

The study builder, tests, hard checker, and Make target must run with the
repository's standard-library Python workflow. Outputs must be deterministic
and rebuild offline from the committed source panels.

After fitting, any correction to this specification requires a visibly
versioned amendment that preserves this document, identifies the reason, and
reports the original locked result. Source-integrity or implementation bugs may
be corrected, but the affected original output must not be silently replaced.

## Claim Boundary

A passing result would show only that this fixed, low-dimensional probability
model improves one temporal forecasting comparison and meets one aggregate
calibration tolerance. A failing result would show that it does not meet that
fixed comparison. Neither result identifies a causal presidential-choice
mechanism, recovers unobserved support behind nonrecorded approvals, validates
the simulator's veto process, or supports institutional-design recommendations.
