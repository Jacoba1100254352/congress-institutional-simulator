# Breakout Paper Plan

This folder keeps publication-splitting notes inside the paper workspace without
turning the ACM CI manuscript into an umbrella paper.

## Primary ACM CI Paper

Working title: `A Modular Simulation Framework for Stress-Testing Legislative Collective-Decision Mechanisms`

Focus: modular simulator architecture, generator assumptions, metric dashboard,
one main tradeoff display, one metric-profile display, one robustness summary,
and a narrow empirical flow sanity-check table.

Audience: ACM Collective Intelligence / HCOMP and CSCW-adjacent reviewers.

## Political Science Simulation Paper

Focus: deeper legislative bargaining, agenda control, vetoes, committees,
lobbying, public-support proxies, and empirical calibration/validation.

Needed before drafting: stronger validation datasets, tighter benchmark
fairness controls, and clearer institutional-theory framing.

Current validation progress: complete source-pinned 116th-, 117th-, and
118th-Congress H.R./S. lifecycle censuses now support two external-Congress
no-refit temporal tests. Five of six cohort-metric cells pass; 118th-Congress
enactment misses its tolerance. A compact 108th-118th-Congress panel separately
shows a 47.266-fold conditional veto-rate mismatch across 4,021 H.R./S.
presidential decisions, so executive choice remains a stress mechanism rather
than a U.S.-calibrated model. This strengthens the empirical boundary but does
not remove the broader drafting gate.

## Robustness And Failure-Mode Paper

Focus: clone/decoy attacks, astroturf objection, bad-faith harm claims,
proposal flooding, lobbying camouflage, and adversarial mechanism gaming.

Needed before drafting: stronger adversary models and worst-case rather than
average degradation reporting.

## Chamber-Structure Paper

Focus: apportionment, bicameralism, committee assignment, review architecture,
selection and retention filters, and representation tradeoffs.

Needed before drafting: expanded chamber scenarios and a separate validation
plan for representation architecture.
