package congresssim.calibration;

import java.util.List;

public final class CalibrationTargetCatalog {
    private CalibrationTargetCatalog() {
    }

    public static List<CalibrationTarget> standardTargets() {
        return List.of(
                new CalibrationTarget(
                        "voteview-party-unity",
                        "Voteview roll-call votes",
                        "party-unity rates and coalition-size distributions by Congress",
                        "averageEnactedSupport, party-position spread, chamber vote shares",
                        "Tune generated party loyalty and polarization so ordinary majority scenarios produce plausible coalition patterns.",
                        "This target supports representation and compromise calibration, not normative scoring."
                ),
                new CalibrationTarget(
                        "congressgov-bill-attrition",
                        "Congress.gov and govinfo bill histories",
                        "introduced, referred, reported, passed, vetoed, and enacted bill counts",
                        "floorConsiderationRate, accessDenialRate, committeeRejectionRate, productivity, vetoes",
                        "Check whether ordinary procedural baselines produce plausible attrition before testing counterfactual institutions.",
                        "Topic-specific attrition should be checked separately once issue domains are calibrated."
                ),
                new CalibrationTarget(
                        "comparative-agendas-topic-throughput",
                        "Comparative Agendas Project",
                        "agenda attention and policy-topic throughput over time",
                        "issue-domain bill shares, enacted bill diversity, welfarePerSubmittedBill",
                        "Calibrate issue-domain generation and topic throughput so simulated campaigns are not dominated by one generated domain.",
                        "The current simulator has abstract domains; this is a mapping target for later empirical work."
                ),
                new CalibrationTarget(
                        "parlgov-party-system",
                        "ParlGov party-system data",
                        "party counts, governing-party concentration, and party-family seat shares",
                        "partySystemProfile, partySystemWeight, party seat shares, party-position spread",
                        "Ground weighted party-system sensitivity cases instead of treating two-party and multiparty assumptions equally.",
                        "This is especially relevant for v18-style weighted cases."
                ),
                new CalibrationTarget(
                        "lobbying-disclosure-spend",
                        "U.S. lobbying disclosure data",
                        "client, issue, and sector lobbying expenditure distributions",
                        "lobbySpendPerBill, defensiveLobbyingShare, channel spend shares, captureReturnOnSpend",
                        "Constrain explicit lobby-group budgets and channel reallocations before making claims about anti-capture designs.",
                        "The simulator should compare spending distributions, not infer causality from disclosure totals alone."
                ),
                new CalibrationTarget(
                        "effective-lawmaking-sponsor-success",
                        "Center for Effective Lawmaking",
                        "sponsor effectiveness and bill-advancement success by member and chamber",
                        "proposerAccessGini, welfarePerSubmittedBill, enacted bills by proposer",
                        "Check whether proposer access and success concentration look plausible in conventional baselines.",
                        "This target helps interpret earned credits and proposal bonds."
                ),
                new CalibrationTarget(
                        "v-dem-institutional-constraints",
                        "V-Dem institutional indicators",
                        "executive constraints, party institutionalization, and deliberative components",
                        "scenario case weights, veto frequency, legitimacyScore, publicAlignmentScore",
                        "Use broad cross-national indicators for sensitivity analysis rather than direct U.S.-Congress validation.",
                        "This is a coarse external-context target."
                )
        );
    }
}
