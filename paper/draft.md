# Default Enactment and Agenda Control

## An Agent-Based Simulation Framework for Comparing Legislative Decision Rules

### Abstract

This paper develops an agent-based simulation framework for comparing legislative institutions by separating rule productivity from cooperation, compromise, legitimacy, and agenda control. The motivating counterfactual is a default-enactment legislature in which proposed laws pass unless a two-thirds blocking coalition vetoes them. Prior work gives strong analogues for default or negative-consent procedures in negative parliamentarism, reverse-consensus international procedures, tacit-acceptance treaty amendments, silence procedures, and U.S. review-and-disapproval mechanisms, but the literature does not appear to contain a close mainstream analogue for broad ordinary lawmaking. The simulator therefore treats default enactment as an institutional design pattern whose effects depend on proposal rights, proposal costs, committee gatekeeping, information processing, and voting thresholds.

The current model is intentionally austere: legislators have one-dimensional ideal points and heterogeneous sensitivities to party, constituency, lobbying, reputation, and compromise; bills are generated around proposers; enacted bills update a scalar status quo; and institutional rules are implemented as modular processes. Across the current v1 campaign, open default enactment produces much higher throughput than ordinary majority systems, averaging 0.840 productivity and 81.818 enacted bills per run, but also produces high low-support passage, policy shift, and proposer gain. Agenda guardrails sharply reduce those risks but at a large productivity cost. A new proposal-cost screen reduces floor load and enactments, but the current cost formula selects for high proposer value and positive lobby pressure, showing that proposal costs are themselves a design variable rather than an automatic safeguard. The paper argues that the next research contribution is not a claim that one institution is best, but a reproducible way to test when default enactment produces coordination and when it magnifies agenda-setter power.

### 1. Introduction

Legislative design usually treats passage as an affirmative act: a proposal becomes law only if supporters assemble a sufficient winning coalition. This paper studies an inverse rule: a proposal becomes law by default unless opponents assemble a two-thirds blocking coalition. The rule is interesting because it attacks gridlock directly, but it also changes the identity of the pivotal actors. Under a normal majority rule, the central question is whether the proposal can beat the status quo. Under default enactment, the central question is whether opponents can coordinate strongly enough to block the proposal.

That reversal makes raw productivity a dangerous evaluation target. A system that passes many laws may be efficient, but it may also be captured, volatile, or weakly legitimate. The core design problem is therefore not simply whether default enactment passes more bills. It is whether default enactment can produce higher cooperation and compromise under credible agenda safeguards.

The project builds a modular simulator for that question. The simulator compares institutions under common generated worlds, reports multiple metrics, and treats proposals as objects that pass through agenda institutions before final yes/no votes. The current implementation includes unicameral majority rule, 60 percent supermajority passage, default passage unless two-thirds block, bicameral majority rule, presidential veto, proposal-access screens, committee gatekeeping, committee information review, committee composition presets, and proposal-cost screens.

The central thesis of this draft is narrow: default enactment cannot be evaluated apart from agenda structure. Proposal rights, proposal volume, screening costs, committee information, and gatekeeping determine whether the rule looks like a coordination device or a mechanism for flooding the agenda with low-consensus proposals.

### 2. Prior Work and Positioning

The prior-art report found no single mature legislative simulator that should be copied wholesale. Instead, it identifies four relevant bodies of work:

1. Agent-based modeling as a method for heterogeneous interacting political actors.
2. Formal legislative theory, including spatial voting, bargaining, veto-player theory, pivotal politics, and agenda control.
3. Empirical measurement infrastructure, including roll-call ideology, bill progression, lobbying data, and legislative effectiveness scores.
4. Institutional analogues for default or negative-consent decisions.

The formal theory matters most for the model design. Spatial voting and status-quo comparison motivate the scalar policy state. Legislative bargaining and agenda-setter theory motivate proposal identity and proposer gain. Veto-player and pivotal-politics theories motivate comparing ordinary majority rules, supermajority rules, bicameralism, and executive vetoes. Cox and McCubbins-style agenda control motivates modeling what never reaches the floor. The key design choice is to model floor voting as only one stage in a larger agenda process.

Default enactment has several analogues as a decision pattern. Negative parliamentarism lets governments take or retain office unless a majority votes against them. WTO reverse consensus adopts certain decisions unless members coordinate to reject them. EU reverse qualified-majority and comitology procedures shift the burden toward rejection in some implementation contexts. Tacit-acceptance and silence procedures allow certain decisions to take effect unless objections are raised by a deadline. U.S. review-and-disapproval structures, including the Congressional Review Act and BRAC-style processes, also use default implementation in constrained contexts.

Those analogues are not ordinary open-ended legislation. Most work because the proposal source is constrained, the subject matter is bounded, objection windows exist, or a commission, agency, or executive actor has already screened the proposal. That makes the simulator's agenda modules central rather than auxiliary.

Working citation targets for a later formal bibliography include Pluchino et al. on parliament ABMs, de Marchi and Page on agent-based political modeling, Downs on spatial democracy, Baron and Ferejohn on legislative bargaining, Tsebelis on veto players, Krehbiel on pivotal politics, Cox and McCubbins on agenda control, Carey on legislative voting and accountability, and Volden and Wiseman on legislative effectiveness. The current draft should not be submitted until those references are converted into formal citations and the model is validated against at least coarse empirical targets.

### 3. Model Overview

The simulator is an agent-based institutional model. Each run creates a legislature, a bill stream, a status quo, and an institutional process.

Legislators have:

- ideology from -1.0 to 1.0
- party label
- party loyalty
- constituency sensitivity
- lobby susceptibility
- reputation sensitivity
- compromise preference

Bills have:

- proposer identity
- proposer ideology
- policy position from -1.0 to 1.0
- public support
- public-benefit score
- lobby pressure
- salience

The status quo is scalar. When a bill is enacted, the status quo moves to the enacted bill's policy position. Votes are therefore not abstract preferences over isolated bills; they are evaluations of a proposal relative to current policy.

The institutional process is modular. A bill may pass through proposal access, proposal cost, committee information, committee gatekeeping, chamber voting, bicameral approval, and presidential veto. Each final floor choice is still yes or no, but the incentives and agenda path leading to that choice vary by scenario.

### 4. Metrics

The simulator reports a dashboard rather than a single score:

- Productivity: share of potential bills enacted.
- Floor consideration: share of potential bills reaching a floor vote.
- Enacted bills per run: absolute throughput.
- Floor bills per run: institutional load.
- Average enacted support: coalition breadth among enacted bills.
- Welfare: average public-benefit score of enacted bills.
- Cooperation: productivity weighted by enacted support.
- Compromise: moderation, support, and distance from proposer advantage.
- Gridlock: share of potential bills not enacted.
- Access denial and committee rejection: agenda filtering rates.
- Low-support passage: enacted bills with less than 50 percent yes support.
- Popular failure: high-public-support bills that fail.
- Policy shift: average absolute movement from the status quo.
- Proposer gain: enacted movement toward the proposer's ideal point.
- Veto and override counts.

This distinction matters because default enactment can dominate productivity while performing poorly on low-support passage, policy volatility, or proposer gain.

### 5. Experimental Design

The current campaign is `simulation-campaign-v1`. It uses:

- 150 runs per case.
- 101 legislators.
- 60 base bills per run.
- Seed 20260428.
- 16 assumption cases.
- 11 institutional scenarios per case.

The institutional scenarios are:

- Unicameral simple majority.
- Unicameral 60 percent passage.
- Default pass unless two-thirds block.
- Default pass plus proposal-access screen.
- Default pass plus representative committee gate.
- Default pass plus access and committee.
- Default pass plus informed guarded committee.
- Default pass plus proposal costs.
- Default pass plus proposal costs and informed guardrails.
- Bicameral simple majority.
- Bicameral majority plus presidential veto and override.

The assumption cases include baseline, low and high polarization, low and high party loyalty, low and high compromise culture, low and high lobbying, weak constituency pressure, two-party and multiparty systems, high proposal pressure, extreme proposal pressure, lobby-fueled flooding, and low-compromise flooding.

### 6. Current Findings

The first finding is that open default enactment is consistently the throughput leader. Across v1, it averages 0.840 productivity, 81.818 enacted bills per run, and 97.500 floor bills per run. By comparison, unicameral simple majority averages 0.245 productivity and 22.961 enacted bills per run, while the 60 percent supermajority rule averages 0.081 productivity and 7.284 enacted bills per run.

The second finding is that throughput comes with obvious risk signals. Open default enactment averages 0.455 low-support passage, 0.688 policy shift, and 0.686 proposer gain. In this model, the rule is not merely reducing gridlock; it is also letting many proposals pass without majority support and moving policy substantially toward proposers.

The third finding is that informed guardrails greatly reduce those risks. Default pass with access screening, committee information, and committee gatekeeping averages 0.198 productivity, 18.643 enacted bills per run, 0.610 welfare, 0.220 low-support passage, 0.065 policy shift, and 0.247 proposer gain. Relative to open default-pass, that is a 0.236 reduction in low-support passage and a 0.623 reduction in policy shift, but also a 0.643 productivity loss.

The fourth finding is that proposal costs reveal agenda load more clearly than percentage metrics alone. In high proposal pressure, open default-pass enacts 151.140 bills per run and considers 180.000 bills per run. Under extreme proposal pressure, it enacts 251.533 and considers 300.000. A productivity percentage by itself hides the institutional burden.

The fifth finding is mixed and important: the first proposal-cost rule reduces volume but does not automatically increase legitimacy. Across v1, default pass plus proposal costs averages 47.774 enacted bills per run and 50.204 floor bills per run, versus 81.818 and 97.500 under open default-pass. It reduces average policy shift from 0.688 to 0.607. But low-support passage rises from 0.455 to 0.492, and proposer gain rises from 0.686 to 1.124. That is not a bug in the research program; it is a substantive finding. If the cost function can be cleared by proposer private gain or favorable lobby pressure, costs may screen out low-value proposals while preserving or amplifying agenda-setter advantage.

The sixth finding is that stacking costs and guardrails may overcorrect. Default pass with costs plus informed guardrails averages only 0.053 productivity, 5.067 enacted bills per run, and 5.090 floor bills per run. It produces higher welfare and lower policy shift, but it is less productive than the 60 percent supermajority baseline in the campaign average.

### 7. Interpretation

The current evidence supports the report's warning about proposal-set dependence. Default enactment is not one rule; it is a family of regimes defined by who can propose, how many proposals can enter, what screening costs exist, what information committees provide, and who can block the floor.

The proposal-cost result is especially useful because it prevents an overly simple conclusion. One might expect costs to solve proposal flooding. In the current model, costs do reduce flooding. But the cost rule also changes the composition of the surviving agenda. Because expected value includes proposer policy gain and lobby credit, the surviving bills are not necessarily more legitimate or more cooperative. They are more worth proposing under the cost formula.

That means the next research step should test cost mechanisms, not merely cost levels. A legislature might charge time, attention, sponsorship signatures, refundable deposits, public-interest bonds, committee review capacity, or political capital. Each mechanism selects a different proposal set.

### 8. Limitations

This is not yet a validated model of Congress. The current simulator has a one-dimensional policy space, generated legislators, stylized public support, stylized public benefit, simplified lobbying, no elections, no amendments, no strategic bargaining, no bicameral asymmetry, and no topic-specific policy domains. The results should therefore be read as mechanism exploration, not empirical prediction.

The largest limitation is endogeneity. Real proposers choose bills strategically based on expected institutional response. The current model mostly generates proposals exogenously around proposer ideal points. That is acceptable for early comparative work, but default-pass regimes especially require endogenous proposal generation.

The second limitation is calibration. Before making stronger claims, the simulator should reproduce rough empirical patterns for ordinary legislative systems: coalition sizes, party unity, roll-call ideology distribution, bill progression rates, veto frequencies, and policy-topic throughput.

The third limitation is welfare specification. Public benefit is generated inside the model rather than estimated from real outcomes. It is useful for comparing scenarios under common assumptions, but it should not be treated as a real social-welfare measure.

### 9. Contribution

The plausible academic contribution is a methodological and theoretical one:

- A modular simulator that compares legislative rules across shared generated worlds.
- A default-enactment counterfactual tied to real institutional analogues but not falsely presented as a standard constitutional model.
- A metric suite that separates productivity from cooperation, compromise, volatility, minority protection, and agenda-setter advantage.
- A demonstration that default enactment's performance depends on agenda control and proposal-cost design.
- A research path toward calibration using Voteview, Congress.gov or govinfo, Comparative Agendas Project, lobbying data, and legislative-effectiveness measures.

The paper would be strongest as a computational institutional-design paper, not as a normative claim that default enactment should be adopted.

### 10. Next Simulations

The next simulations are specified in `paper/simulation-backlog.md`. The immediate additions should be:

- Proposal-cost parameter sweeps.
- Alternative proposal-cost mechanisms.
- Proposal flooding severity sweeps.
- Agenda order-of-operations comparisons.
- Robustness runs with confidence intervals.
- Endogenous proposal strategy.
- Validation baselines against ordinary U.S.-style legislative patterns.

### 11. Provisional Conclusion

Default enactment is a serious institutional design idea because it directly attacks status quo bias and obstruction. The first simulations show why it is also dangerous to evaluate in isolation. Open default-pass rules generate high throughput, but the same mechanism can generate low-support enactments, large policy shifts, and agenda-setter advantage. Guardrails can reduce those risks, but at large productivity cost. Proposal costs reduce institutional load, but their design determines which bills survive. The paper's core claim should therefore be conditional: default enactment may improve coordination only when agenda rights, screening costs, information institutions, and blocking rights are designed together.
