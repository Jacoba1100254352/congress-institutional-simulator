package congresssim.experiment;

import congresssim.institution.chamber.Chamber;

import congresssim.simulation.Scenario;
import congresssim.simulation.catalog.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.MetricDefinition;
import congresssim.simulation.PartySystemProfile;
import congresssim.simulation.ProposalShockProfile;
import congresssim.simulation.WorldSpec;
import congresssim.reporting.ReportProvenance;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public final class CampaignRunner {
    private static final List<String> CORE_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-access",
            "default-pass-committee",
            "default-pass-guarded",
            "default-pass-informed-guarded",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> FLOODING_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-cost",
            "default-pass-access",
            "default-pass-committee",
            "default-pass-guarded",
            "default-pass-informed-guarded",
            "default-pass-cost-guarded",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> CHALLENGE_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-challenge",
            "default-pass-challenge-info",
            "default-pass-cost",
            "default-pass-informed-guarded",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> CHALLENGE_SWEEP_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082",
            "current-system"
    );
    private static final List<String> CROSS_BLOC_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-cross-bloc-strong",
            "default-pass-cross-bloc-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082",
            "current-system"
    );
    private static final List<String> ADAPTIVE_TRACK_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-cross-bloc-strong",
            "default-pass-cross-bloc-challenge",
            "default-pass-adaptive-track",
            "default-pass-adaptive-track-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082",
            "current-system"
    );
    private static final List<String> SUNSET_TRIAL_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-cross-bloc-strong",
            "default-pass-cross-bloc-challenge",
            "default-pass-adaptive-track",
            "default-pass-adaptive-track-challenge",
            "default-pass-sunset-trial",
            "default-pass-sunset-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082",
            "current-system"
    );
    private static final List<String> PROPOSAL_CREDIT_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-cross-bloc-strong",
            "default-pass-cross-bloc-challenge",
            "default-pass-adaptive-track",
            "default-pass-adaptive-track-challenge",
            "default-pass-sunset-trial",
            "default-pass-sunset-challenge",
            "default-pass-earned-credits",
            "default-pass-earned-credits-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082",
            "current-system"
    );
    private static final List<String> ANTI_CAPTURE_SCENARIOS = List.of(
            "simple-majority",
            "simple-majority-lobby-firewall",
            "supermajority-60",
            "default-pass",
            "default-pass-lobby-firewall",
            "default-pass-lobby-transparency",
            "default-pass-public-interest-screen",
            "default-pass-lobby-audit",
            "default-pass-anti-capture-bundle",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "default-pass-sunset-trial",
            "default-pass-earned-credits",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> BUDGETED_LOBBYING_SCENARIOS = List.of(
            "simple-majority",
            "simple-majority-lobby-firewall",
            "supermajority-60",
            "default-pass",
            "default-pass-budgeted-lobbying",
            "default-pass-budgeted-lobbying-transparency",
            "default-pass-budgeted-lobbying-bundle",
            "default-pass-lobby-transparency",
            "default-pass-public-interest-screen",
            "default-pass-lobby-audit",
            "default-pass-anti-capture-bundle",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "default-pass-sunset-trial",
            "default-pass-earned-credits",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> MEDIATION_SCENARIOS = List.of(
            "simple-majority",
            "simple-majority-mediation",
            "simple-majority-lobby-firewall",
            "supermajority-60",
            "default-pass",
            "default-pass-mediation",
            "default-pass-budgeted-lobbying",
            "default-pass-budgeted-lobbying-mediation",
            "default-pass-budgeted-lobbying-transparency",
            "default-pass-budgeted-lobbying-bundle",
            "default-pass-anti-capture-bundle",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "default-pass-sunset-trial",
            "default-pass-earned-credits",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> DISTRIBUTIONAL_HARM_SCENARIOS = List.of(
            "simple-majority",
            "simple-majority-mediation",
            "supermajority-60",
            "default-pass",
            "default-pass-mediation",
            "default-pass-harm-threshold",
            "default-pass-compensation",
            "default-pass-affected-consent",
            "default-pass-budgeted-lobbying",
            "default-pass-budgeted-lobbying-mediation",
            "default-pass-anti-capture-bundle",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "default-pass-sunset-trial",
            "default-pass-earned-credits",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> LAW_REGISTRY_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-mediation",
            "default-pass-harm-threshold",
            "default-pass-compensation",
            "default-pass-affected-consent",
            "default-pass-sunset-trial",
            "default-pass-sunset-challenge",
            "default-pass-law-registry",
            "default-pass-law-registry-challenge",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "default-pass-earned-credits",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> POLICY_TOURNAMENT_SCENARIOS = List.of(
            "simple-majority",
            "simple-majority-alternatives-pairwise",
            "supermajority-60",
            "default-pass",
            "default-pass-mediation",
            "default-pass-harm-threshold",
            "default-pass-compensation",
            "default-pass-affected-consent",
            "default-pass-alternatives-benefit",
            "default-pass-alternatives-support",
            "default-pass-alternatives-median",
            "default-pass-alternatives-pairwise",
            "default-pass-obstruction-substitute",
            "default-pass-law-registry",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "default-pass-earned-credits",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> LOBBYING_DEPTH_SCENARIOS = List.of(
            "simple-majority",
            "simple-majority-lobby-firewall",
            "supermajority-60",
            "default-pass",
            "default-pass-mediation",
            "default-pass-budgeted-lobbying",
            "default-pass-budgeted-lobbying-transparency",
            "default-pass-budgeted-lobbying-bundle",
            "default-pass-democracy-vouchers",
            "default-pass-public-advocate",
            "default-pass-blind-lobby-review",
            "default-pass-defensive-lobby-cap",
            "default-pass-lobby-channel-bundle",
            "default-pass-anti-capture-bundle",
            "default-pass-compensation",
            "default-pass-affected-consent",
            "default-pass-alternatives-benefit",
            "default-pass-alternatives-median",
            "default-pass-alternatives-pairwise",
            "default-pass-law-registry",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> CITIZEN_PANEL_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-citizen-certificate",
            "default-pass-citizen-active-routing",
            "default-pass-citizen-threshold",
            "default-pass-citizen-agenda",
            "default-pass-informed-guarded",
            "default-pass-public-interest-screen",
            "default-pass-lobby-channel-bundle",
            "default-pass-alternatives-pairwise",
            "default-pass-law-registry",
            "default-pass-compensation",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> AGENDA_SCARCITY_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-weighted-agenda-lottery",
            "default-pass-random-agenda-lottery",
            "default-pass-quadratic-attention",
            "default-pass-public-objection",
            "default-pass-repeal-window",
            "default-pass-earned-credits",
            "default-pass-challenge",
            "default-pass-informed-guarded",
            "default-pass-public-interest-screen",
            "default-pass-citizen-certificate",
            "default-pass-cross-bloc",
            "default-pass-adaptive-track",
            "default-pass-alternatives-pairwise",
            "default-pass-law-registry",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> ROADMAP_COMPLETION_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-constituent-public-will",
            "default-pass-constituent-citizen-panel",
            "default-pass-proposal-bonds",
            "default-pass-proposal-bonds-challenge",
            "default-pass-cross-bloc-credit-discount",
            "default-pass-affected-sponsor-gate",
            "default-pass-multiround-mediation",
            "default-pass-multiround-mediation-challenge",
            "default-pass-alternatives-pairwise",
            "default-pass-alternatives-strategic",
            "default-pass-adaptive-proposers",
            "default-pass-adaptive-proposers-lobbying",
            "default-pass-strategic-lobbying",
            "default-pass-challenge",
            "default-pass-challenge-party-proportional",
            "default-pass-challenge-minority-bonus",
            "default-pass-challenge-supermajority",
            "default-pass-challenge-committee",
            "default-pass-challenge-info-active",
            "default-pass-adaptive-track",
            "default-pass-adaptive-track-lenient",
            "default-pass-adaptive-track-strict",
            "default-pass-adaptive-track-citizen-high-risk",
            "default-pass-adaptive-track-supermajority-high-risk",
            "default-pass-law-registry",
            "default-pass-law-registry-fast-review",
            "default-pass-law-registry-slow-review",
            "default-pass-cost",
            "default-pass-cost-public-waiver",
            "default-pass-cost-lobby-surcharge",
            "default-pass-member-quota",
            "default-pass-weighted-agenda-lottery",
            "default-pass-public-objection",
            "bicameral-majority",
            "presidential-veto",
            "current-system"
    );
    private static final List<String> TIMELINE_SCENARIOS = List.of(
            "current-system",
            "simple-majority",
            "supermajority-60",
            "bicameral-majority",
            "presidential-veto",
            "leadership-cartel-majority",
            "committee-regular-order",
            "cloture-conference-review",
            "parliamentary-coalition-confidence",
            "citizen-initiative-referendum",
            "district-population-majority",
            "simple-majority-alternatives-pairwise",
            "citizen-assembly-threshold",
            "package-bargaining-majority",
            "omnibus-bargaining-majority",
            "risk-routed-majority",
            "expanded-portfolio-hybrid-legislature",
            "norm-erosion-majority",
            "default-pass",
            "default-pass-challenge",
            "default-pass-multiround-mediation-challenge"
    );
    private static final List<String> STRATEGY_CALIBRATION_SCENARIOS = List.of(
            "current-system",
            "simple-majority",
            "supermajority-60",
            "bicameral-majority",
            "presidential-veto",
            "default-pass",
            "default-pass-budgeted-lobbying",
            "default-pass-strategic-lobbying",
            "default-pass-adaptive-proposers",
            "default-pass-adaptive-proposers-lobbying",
            "default-pass-deep-strategy-bundle",
            "default-pass-multiround-mediation",
            "default-pass-multiround-mediation-challenge",
            "default-pass-constituent-citizen-panel",
            "default-pass-alternatives-pairwise",
            "default-pass-public-objection",
            "default-pass-law-registry"
    );
    private static final List<String> PAPER_SCENARIOS = List.of(
            "current-system",
            "simple-majority",
            "supermajority-60",
            "bicameral-majority",
            "presidential-veto",
            "leadership-cartel-majority",
            "committee-regular-order",
            "cloture-conference-review",
            "constitutional-court-architecture-majority",
            "parliamentary-coalition-confidence",
            "citizen-initiative-referendum",
            "district-population-majority",
            "simple-majority-alternatives-pairwise",
            "citizen-assembly-threshold",
            "public-interest-majority",
            "agenda-lottery-majority",
            "quadratic-attention-majority",
            "proposal-bond-majority",
            "harm-weighted-majority",
            "compensation-majority",
            "package-bargaining-majority",
            "multidimensional-package-majority",
            "omnibus-bargaining-majority",
            "law-registry-majority",
            "public-objection-majority",
            "anti-capture-majority-bundle",
            "influence-system-majority",
            "risk-routed-majority",
            "portfolio-hybrid-legislature",
            "expanded-portfolio-hybrid-legislature",
            "norm-erosion-majority",
            "long-horizon-learning-majority",
            "default-pass",
            "default-pass-challenge",
            "default-pass-multiround-mediation-challenge"
    );
    private static final List<String> CHAMBER_STRUCTURE_SCENARIOS = List.of(
            "simple-majority",
            "bicameral-majority",
            "current-system",
            "equal-population-unicameral",
            "proportional-house-majority",
            "chamber-incongruence-pr-upper",
            "malapportioned-upper-chamber",
            "appointed-upper-chamber",
            "asymmetric-senate-cloture",
            "conference-malapportioned-upper",
            "house-origin-routing",
            "senate-origin-routing",
            "emergency-lower-fast-routing",
            "proposer-chamber-origin-routing",
            "leadership-routed-origin",
            "principles-resolution-routing",
            "second-chamber-preclearance",
            "revision-council-upper",
            "suspensive-veto-upper",
            "limited-navette-upper",
            "joint-sitting-upper",
            "upper-amendment-only",
            "upper-absolute-veto",
            "upper-territorial-veto",
            "mediation-committee-upper",
            "last-offer-bargaining-upper",
            "lower-override-upper",
            "committee-regular-order",
            "balanced-committee-majority",
            "lottery-committee-majority",
            "expert-lottery-committee-majority",
            "opposition-chaired-committee-majority",
            "committee-deadline-discharge-majority",
            "committee-minority-hearing-majority",
            "committee-amendment-majority",
            "minority-veto-committee-majority",
            "mixed-citizen-committee-majority",
            "committee-priority-queue-majority",
            "committee-veto-player-majority",
            "committee-fast-track-certifier-majority",
            "committee-scrutiny-audit-majority",
            "committee-public-accounts-majority",
            "committee-legal-drafting-majority",
            "committee-discharge-target-majority",
            "eligibility-expertise-majority",
            "appointment-retention-majority",
            "recusal-cooling-off-majority",
            "exante-advisory-majority",
            "exante-clearance-majority",
            "independent-insulation-majority"
    );
    private static final List<String> ABLATION_SCENARIOS = List.of(
            "current-system",
            "simple-majority",
            "simple-majority-mediation",
            "simple-majority-lobby-firewall",
            "public-interest-majority",
            "simple-majority-alternatives-pairwise",
            "risk-routed-majority",
            "risk-routed-no-citizen-majority",
            "harm-weighted-majority",
            "compensation-majority",
            "affected-consent-majority",
            "package-bargaining-majority",
            "multidimensional-package-majority",
            "law-registry-majority",
            "anti-capture-majority-bundle"
    );
    private static final List<String> MANIPULATION_STRESS_SCENARIOS = List.of(
            "current-system",
            "simple-majority",
            "simple-majority-alternatives-pairwise",
            "simple-majority-alternatives-strategic",
            "citizen-assembly-threshold",
            "citizen-assembly-manipulation-stress",
            "agenda-lottery-majority",
            "public-objection-majority",
            "public-objection-astroturf-majority",
            "harm-weighted-majority",
            "harm-weighted-loose-claims-majority",
            "anti-capture-majority-bundle",
            "default-pass"
    );

    private CampaignRunner() {
    }

    public static CampaignResult runV0(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v0",
                "simulation-campaign-v0",
                outputDir,
                v0Cases(legislators, bills),
                CORE_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV1(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v1",
                "simulation-campaign-v1",
                outputDir,
                v1Cases(legislators, bills),
                FLOODING_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV2(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v2",
                "simulation-campaign-v2",
                outputDir,
                v1Cases(legislators, bills),
                CHALLENGE_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV3(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v3",
                "simulation-campaign-v3",
                outputDir,
                v1Cases(legislators, bills),
                CHALLENGE_SWEEP_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV4(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v4",
                "simulation-campaign-v4",
                outputDir,
                v1Cases(legislators, bills),
                CROSS_BLOC_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV5(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v5",
                "simulation-campaign-v5",
                outputDir,
                v1Cases(legislators, bills),
                ADAPTIVE_TRACK_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV6(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v6",
                "simulation-campaign-v6",
                outputDir,
                v1Cases(legislators, bills),
                SUNSET_TRIAL_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV7(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v7",
                "simulation-campaign-v7",
                outputDir,
                v1Cases(legislators, bills),
                PROPOSAL_CREDIT_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV8(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v8",
                "simulation-campaign-v8",
                outputDir,
                v8Cases(legislators, bills),
                ANTI_CAPTURE_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV9(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v9",
                "simulation-campaign-v9",
                outputDir,
                v8Cases(legislators, bills),
                BUDGETED_LOBBYING_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV10(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v10",
                "simulation-campaign-v10",
                outputDir,
                v8Cases(legislators, bills),
                MEDIATION_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV11(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v11",
                "simulation-campaign-v11",
                outputDir,
                v8Cases(legislators, bills),
                DISTRIBUTIONAL_HARM_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV12(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v12",
                "simulation-campaign-v12",
                outputDir,
                v8Cases(legislators, bills),
                LAW_REGISTRY_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV13(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v13",
                "simulation-campaign-v13",
                outputDir,
                v8Cases(legislators, bills),
                POLICY_TOURNAMENT_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV14(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v14",
                "simulation-campaign-v14",
                outputDir,
                v8Cases(legislators, bills),
                LOBBYING_DEPTH_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV15(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v15",
                "simulation-campaign-v15",
                outputDir,
                v8Cases(legislators, bills),
                CITIZEN_PANEL_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV16(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v16",
                "simulation-campaign-v16",
                outputDir,
                v8Cases(legislators, bills),
                AGENDA_SCARCITY_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV17(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v17",
                "simulation-campaign-v17",
                outputDir,
                v8Cases(legislators, bills),
                ROADMAP_COMPLETION_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV18(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v18",
                "simulation-campaign-v18",
                outputDir,
                v18Cases(legislators, bills),
                ROADMAP_COMPLETION_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV19(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v19 Timeline",
                "simulation-campaign-v19",
                outputDir,
                v19Cases(legislators, bills),
                TIMELINE_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV20(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v20 Strategy and Calibration",
                "simulation-campaign-v20",
                outputDir,
                v8Cases(legislators, bills),
                STRATEGY_CALIBRATION_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV21Paper(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Main Comparison Campaign",
                "simulation-campaign-v21-paper",
                outputDir,
                v21PaperCases(legislators, bills),
                PAPER_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runAblationAnalysis(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        List<ExperimentCase> cases = new ArrayList<>(v8Cases(legislators, bills));
        cases.addAll(v21AdversarialCases(legislators, bills));
        return run(
                "Mechanism Ablation Analysis",
                "simulation-ablation-analysis",
                outputDir,
                cases,
                ABLATION_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runManipulationStress(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Manipulation Stress Campaign",
                "simulation-manipulation-stress",
                outputDir,
                manipulationStressCases(legislators, bills),
                MANIPULATION_STRESS_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runChamberStructure(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        List<ExperimentCase> cases = new ArrayList<>(v21PaperCases(legislators, bills));
        cases.addAll(v21AdversarialCases(legislators, bills));
        return run(
                "Chamber Structure Campaign",
                "simulation-chamber-structure",
                outputDir,
                cases,
                CHAMBER_STRUCTURE_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    private static CampaignResult run(
            String name,
            String fileStem,
            Path outputDir,
            List<ExperimentCase> cases,
            List<String> scenarioKeys,
            int runs,
            int legislators,
            int baseBills,
            long seed
    ) throws IOException {
        Files.createDirectories(outputDir);

        List<Scenario> scenarios = ScenarioCatalog.scenariosForKeys(scenarioKeys);
        Simulator simulator = new Simulator();
        List<CampaignRow> rows = new ArrayList<>();

        for (int caseIndex = 0; caseIndex < cases.size(); caseIndex++) {
            ExperimentCase experimentCase = cases.get(caseIndex);
            List<ScenarioReport> reports = simulator.compare(
                    scenarios,
                    experimentCase.worldSpec(),
                    runs,
                    seed + (10_000L * caseIndex)
            );
            for (int scenarioIndex = 0; scenarioIndex < reports.size(); scenarioIndex++) {
                rows.add(new CampaignRow(
                        experimentCase.key(),
                        experimentCase.name(),
                        experimentCase.description(),
                        experimentCase.caseWeight(),
                        scenarioKeys.get(scenarioIndex),
                        reports.get(scenarioIndex)
                ));
            }
        }

        CampaignResult result = new CampaignResult(
                name,
                rows,
                outputDir.resolve(fileStem + ".csv"),
                outputDir.resolve(fileStem + ".md"),
                outputDir.resolve(fileStem + "-manifest.json")
        );
        Files.writeString(result.csvPath(), csv(result, runs));
        Files.writeString(result.markdownPath(), markdown(result, runs, legislators, baseBills, seed, scenarioKeys.size()));
        ReportProvenance.write(
                result.manifestPath(),
                result.name(),
                runs,
                legislators,
                baseBills,
                seed,
                caseCount(result.rows()),
                scenarioKeys.size(),
                List.of(result.csvPath(), result.markdownPath())
        );
        return result;
    }

    private static List<ExperimentCase> v0Cases(int legislators, int bills) {
        return List.of(
                experiment("baseline", "Baseline", "Moderately polarized three-party legislature.",
                        legislators, bills, 3, 0.72, 0.68, 0.48, 0.64, 0.52),
                experiment("low-polarization", "Low Polarization", "Legislators are less ideologically clustered.",
                        legislators, bills, 3, 0.25, 0.55, 0.48, 0.64, 0.62),
                experiment("high-polarization", "High Polarization", "Legislators are tightly clustered into ideological camps.",
                        legislators, bills, 3, 0.92, 0.80, 0.48, 0.58, 0.34),
                experiment("low-party-loyalty", "Low Party Loyalty", "Party pressure is weak and legislators act more independently.",
                        legislators, bills, 3, 0.72, 0.25, 0.48, 0.64, 0.52),
                experiment("high-party-loyalty", "High Party Loyalty", "Party pressure is strong.",
                        legislators, bills, 3, 0.72, 0.90, 0.48, 0.64, 0.52),
                experiment("low-compromise", "Low Compromise Culture", "Members are less inclined toward moderate, incremental bills.",
                        legislators, bills, 3, 0.72, 0.68, 0.48, 0.64, 0.18),
                experiment("high-compromise", "High Compromise Culture", "Members are more inclined toward moderate, incremental bills.",
                        legislators, bills, 3, 0.72, 0.55, 0.38, 0.70, 0.86),
                experiment("low-lobbying", "Low Lobbying Pressure", "Lobby pressure is weak.",
                        legislators, bills, 3, 0.72, 0.68, 0.12, 0.64, 0.52),
                experiment("high-lobbying", "High Lobbying Pressure", "Lobby pressure is strong.",
                        legislators, bills, 3, 0.72, 0.68, 0.88, 0.54, 0.44),
                experiment("weak-constituency", "Weak Constituency Pressure", "Members are less responsive to public support.",
                        legislators, bills, 3, 0.72, 0.68, 0.48, 0.20, 0.52),
                experiment("two-party", "Two-Party System", "Generated legislators sort into two broad parties.",
                        legislators, bills, 2, 0.72, 0.72, 0.48, 0.64, 0.52),
                experiment("multi-party", "Multi-Party System", "Generated legislators sort into five parties.",
                        legislators, bills, 5, 0.72, 0.58, 0.48, 0.64, 0.58)
        );
    }

    private static List<ExperimentCase> v1Cases(int legislators, int bills) {
        List<ExperimentCase> cases = new ArrayList<>(v0Cases(legislators, bills));
        cases.add(experiment("high-proposal-pressure", "High Proposal Pressure", "Three times as many potential proposals reach the institutional system.",
                legislators, bills * 3, 3, 0.72, 0.68, 0.48, 0.64, 0.52));
        cases.add(experiment("extreme-proposal-pressure", "Extreme Proposal Pressure", "Five times as many potential proposals reach the institutional system.",
                legislators, bills * 5, 3, 0.72, 0.68, 0.48, 0.64, 0.52));
        cases.add(experiment("lobby-fueled-flooding", "Lobby-Fueled Flooding", "High proposal pressure with strong lobbying and weaker constituency pressure.",
                legislators, bills * 3, 3, 0.72, 0.70, 0.88, 0.42, 0.38));
        cases.add(experiment("low-compromise-flooding", "Low-Compromise Flooding", "High proposal pressure in a low-compromise legislature.",
                legislators, bills * 3, 3, 0.82, 0.76, 0.52, 0.54, 0.16));
        return cases;
    }

    private static List<ExperimentCase> v8Cases(int legislators, int bills) {
        List<ExperimentCase> cases = new ArrayList<>(v1Cases(legislators, bills));
        cases.add(experiment("capture-crisis", "Capture Crisis", "High lobbying, weak constituency pressure, low compromise, and high proposal pressure.",
                legislators, bills * 3, 3, 0.78, 0.76, 0.94, 0.34, 0.28));
        cases.add(experiment("popular-anti-lobbying-push", "Popular Anti-Lobbying Push", "High lobbying pressure with stronger public responsiveness and more appetite for reform.",
                legislators, bills * 2, 3, 0.62, 0.58, 0.86, 0.82, 0.68));
        return cases;
    }

    private static List<ExperimentCase> v18Cases(int legislators, int bills) {
        return List.of(
                experiment("party-system-two-party", "Weighted Two-Party Baseline",
                        "Classic two-party legislature with ideological left/right sorting.",
                        legislators, bills, 2, 0.72, 0.72, 0.48, 0.64, 0.52,
                        PartySystemProfile.IDEOLOGICAL_BINS, 0.25),
                experiment("party-system-two-major-minors", "Weighted Two Major Plus Minors",
                        "Five-party legislature with two large ideological parties and smaller minor parties.",
                        legislators, bills, 5, 0.72, 0.66, 0.48, 0.64, 0.55,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 0.40),
                experiment("party-system-fragmented", "Weighted Fragmented Multiparty",
                        "Seven-party legislature with more even fragmentation across the ideological range.",
                        legislators, bills, 7, 0.64, 0.54, 0.48, 0.66, 0.60,
                        PartySystemProfile.FRAGMENTED_MULTIPARTY, 0.20),
                experiment("party-system-dominant", "Weighted Dominant-Party Legislature",
                        "Four-party legislature with one large center-weighted party and smaller opposition parties.",
                        legislators, bills, 4, 0.66, 0.70, 0.48, 0.62, 0.48,
                        PartySystemProfile.DOMINANT_PARTY, 0.15)
        );
    }

    private static List<ExperimentCase> v19Cases(int legislators, int bills) {
        return List.of(
                experiment("era-1-low-contention", "Era 1 Low Contention",
                        "Stylized low-contention legislature with several parties, high compromise culture, lower lobbying, and stronger constituency responsiveness.",
                        legislators, bills, 4, 0.35, 0.45, 0.30, 0.74, 0.82,
                        PartySystemProfile.FRAGMENTED_MULTIPARTY, 1.0),
                experiment("era-2-normal", "Era 2 Normal Contention",
                        "Stylized ordinary-contention legislature with two major parties plus minors and moderate party loyalty.",
                        legislators, bills, 5, 0.50, 0.55, 0.40, 0.68, 0.70,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0),
                experiment("era-3-polarizing", "Era 3 Polarizing",
                        "Stylized rising-contention legislature with stronger ideological clustering, party loyalty, and lobbying pressure.",
                        legislators, bills, 5, 0.65, 0.66, 0.52, 0.62, 0.56,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0),
                experiment("era-4-high-contention", "Era 4 High Contention",
                        "Stylized high-contention legislature with more proposal pressure, higher polarization, and weaker compromise culture.",
                        legislators, Math.max(1, bills * 5 / 4), 3, 0.78, 0.78, 0.64, 0.55, 0.40,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0),
                experiment("era-5-capture-contention", "Era 5 Capture Contention",
                        "Stylized capture-contention legislature with two-party sorting, higher proposal pressure, strong lobbying, and lower public responsiveness.",
                        legislators, Math.max(1, bills * 3 / 2), 2, 0.88, 0.86, 0.78, 0.46, 0.28,
                        PartySystemProfile.IDEOLOGICAL_BINS, 1.0),
                experiment("era-6-crisis", "Era 6 Crisis",
                        "Stylized crisis-contention legislature with severe polarization, high party loyalty, intense lobbying, weak constituency responsiveness, and doubled proposal pressure.",
                        legislators, Math.max(1, bills * 2), 2, 0.94, 0.92, 0.90, 0.38, 0.18,
                        PartySystemProfile.IDEOLOGICAL_BINS, 1.0)
        );
    }

    private static List<ExperimentCase> v21PaperCases(int legislators, int bills) {
        List<ExperimentCase> cases = new ArrayList<>(v8Cases(legislators, bills));
        cases.addAll(v18Cases(legislators, bills));
        cases.addAll(v19Cases(legislators, bills));
        cases.addAll(v21AdversarialCases(legislators, bills));
        return cases;
    }

    private static List<ExperimentCase> v21AdversarialCases(int legislators, int bills) {
        return List.of(
                experiment("adversarial-high-benefit-extreme", "Adversarial High-Benefit Extreme Reform",
                        "Extreme proposals can have high generated public benefit but lower initial support and high uncertainty.",
                        legislators, bills, 4, 0.72, 0.64, 0.38, 0.66, 0.46,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0, ProposalShockProfile.HIGH_BENEFIT_EXTREME_REFORM),
                experiment("adversarial-popular-harmful", "Adversarial Popular Harmful Bill",
                        "Popular proposals can have low generated public benefit, private upside, and concentrated harm.",
                        legislators, bills, 3, 0.66, 0.66, 0.72, 0.62, 0.52,
                        PartySystemProfile.IDEOLOGICAL_BINS, 1.0, ProposalShockProfile.POPULAR_HARMFUL_BILL),
                experiment("adversarial-moderate-capture", "Adversarial Moderate Capture",
                        "Moderate-looking proposals can have low public benefit and high organized-interest capture.",
                        legislators, bills, 3, 0.52, 0.62, 0.84, 0.54, 0.58,
                        PartySystemProfile.IDEOLOGICAL_BINS, 1.0, ProposalShockProfile.LOW_BENEFIT_MODERATE_CAPTURE),
                experiment("adversarial-delayed-benefit", "Adversarial Delayed-Benefit Reform",
                        "Beneficial reforms can have low immediate support because benefits are delayed and uncertain.",
                        legislators, bills, 4, 0.62, 0.58, 0.34, 0.60, 0.50,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0, ProposalShockProfile.DELAYED_BENEFIT_REFORM),
                experiment("adversarial-rights-harm", "Adversarial Concentrated Rights Harm",
                        "Proposals can be broadly supported while imposing severe concentrated rights-like harm.",
                        legislators, bills, 4, 0.70, 0.70, 0.52, 0.66, 0.44,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0, ProposalShockProfile.CONCENTRATED_RIGHTS_HARM),
                experiment("adversarial-anti-lobbying-backlash", "Adversarial Anti-Lobbying Backlash",
                        "Anti-lobbying reforms are more common, but face stronger defensive lobbying and lower observed support.",
                        legislators, bills, 4, 0.64, 0.64, 0.90, 0.70, 0.50,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0, ProposalShockProfile.ANTI_LOBBYING_BACKLASH)
        );
    }

    private static List<ExperimentCase> manipulationStressCases(int legislators, int bills) {
        return List.of(
                experiment("baseline", "Baseline",
                        "Ordinary synthetic legislature used as the stress reference point.",
                        legislators, bills, 3, 0.62, 0.64, 0.48, 0.64, 0.52,
                        PartySystemProfile.IDEOLOGICAL_BINS, 1.0),
                experiment("proposal-flooding", "Proposal Flooding",
                        "Three times as many proposals reach the institutional process.",
                        legislators, Math.max(1, bills * 3), 3, 0.66, 0.68, 0.58, 0.58, 0.42,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0),
                experiment("capture-flooding", "Capture And Flooding",
                        "High proposal pressure, strong lobbying, weaker public responsiveness, and lower compromise culture.",
                        legislators, Math.max(1, bills * 3), 2, 0.84, 0.84, 0.92, 0.44, 0.28,
                        PartySystemProfile.IDEOLOGICAL_BINS, 1.0),
                experiment("clone-decoy-pressure", "Clone/Decoy Tournament Pressure",
                        "Highly polarized, low-compromise environment intended to expose alternative-selection manipulation.",
                        legislators, Math.max(1, bills * 2), 4, 0.80, 0.76, 0.62, 0.54, 0.24,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0),
                experiment("rights-harm-pressure", "Rights-Harm Pressure",
                        "Broadly supported proposals can impose concentrated rights-like harm.",
                        legislators, bills, 4, 0.70, 0.70, 0.52, 0.66, 0.44,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0, ProposalShockProfile.CONCENTRATED_RIGHTS_HARM),
                experiment("popular-harmful-pressure", "Popular Harmful Pressure",
                        "Popular proposals can carry low generated welfare and concentrated harm.",
                        legislators, bills, 3, 0.66, 0.66, 0.72, 0.62, 0.52,
                        PartySystemProfile.IDEOLOGICAL_BINS, 1.0, ProposalShockProfile.POPULAR_HARMFUL_BILL),
                experiment("anti-lobbying-backlash", "Anti-Lobbying Backlash",
                        "Anti-lobbying reforms are more common but face stronger defensive organized-interest pressure.",
                        legislators, bills, 4, 0.64, 0.64, 0.90, 0.70, 0.50,
                        PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES, 1.0, ProposalShockProfile.ANTI_LOBBYING_BACKLASH)
        );
    }

    private static ExperimentCase experiment(
            String key,
            String name,
            String description,
            int legislators,
            int bills,
            int parties,
            double polarization,
            double partyLoyalty,
            double lobbying,
            double constituency,
            double compromise
    ) {
        return experiment(
                key,
                name,
                description,
                legislators,
                bills,
                parties,
                polarization,
                partyLoyalty,
                lobbying,
                constituency,
                compromise,
                PartySystemProfile.IDEOLOGICAL_BINS,
                1.0
        );
    }

    private static ExperimentCase experiment(
            String key,
            String name,
            String description,
            int legislators,
            int bills,
            int parties,
            double polarization,
            double partyLoyalty,
            double lobbying,
            double constituency,
            double compromise,
            PartySystemProfile partySystemProfile,
            double caseWeight
    ) {
        return experiment(
                key,
                name,
                description,
                legislators,
                bills,
                parties,
                polarization,
                partyLoyalty,
                lobbying,
                constituency,
                compromise,
                partySystemProfile,
                caseWeight,
                ProposalShockProfile.BASELINE
        );
    }

    private static ExperimentCase experiment(
            String key,
            String name,
            String description,
            int legislators,
            int bills,
            int parties,
            double polarization,
            double partyLoyalty,
            double lobbying,
            double constituency,
            double compromise,
            PartySystemProfile partySystemProfile,
            double caseWeight,
            ProposalShockProfile proposalShockProfile
    ) {
        return new ExperimentCase(
                key,
                name,
                description,
                caseWeight,
                new WorldSpec(
                        legislators,
                        bills,
                        parties,
                        polarization,
                        partyLoyalty,
                        lobbying,
                        constituency,
                        compromise,
                        partySystemProfile,
                        caseWeight,
                        proposalShockProfile
                )
        );
    }

    private static String csv(CampaignResult result, int runs) {
        StringBuilder builder = new StringBuilder();
        builder.append("caseKey,caseName,caseDescription,caseWeight,scenarioKey,scenario,totalBills,potentialBillsPerRun,enactedBills,enactedPerRun,floorPerRun,directionalScore,representativeQuality,riskControl,administrativeFeasibility,productivity,floor,avgSupport,welfare,cooperation,compromise,gridlock,accessDenied,committeeRejected,challengeRate,lowSupport,weakPublicMandatePassage,popularFail,policyShift,proposerGain,lobbyCapture,publicAlignment,antiLobbyingSuccess,privateGainRatio,lobbySpendPerBill,defensiveLobbyingShare,captureReturnOnSpend,publicPreferenceDistortion,administrativeCost,amendmentRate,amendmentMovement,minorityHarm,concentratedHarmPassage,compensationRate,legitimacy,activeLawWelfare,reversalRate,timeToCorrectBadLaw,statusQuoVolatility,lowSupportActiveLawShare,selectedAlternativeMedianDistance,proposerAgendaAdvantage,alternativeDiversity,statusQuoWinRate,publicBenefitPerLobbyDollar,directLobbySpendShare,agendaLobbySpendShare,informationLobbySpendShare,publicCampaignSpendShare,litigationThreatSpendShare,citizenReviewRate,citizenCertificationRate,citizenLegitimacy,attentionSpendPerBill,objectionWindowRate,repealWindowReversalRate,fastLaneRate,middleLaneRate,highRiskLaneRate,challengeExhaustionRate,falseNegativePassRate,publicWillReviewRate,publicSignalMovement,districtAlignment,crossBlocAdmissionRate,affectedGroupSponsorshipRate,averageCosponsors,proposalBondForfeiture,strategicDecoyRate,proposerAccessGini,welfarePerSubmittedBill,vetoes,overriddenVetoes,interChamberConflictRate,secondChamberKillRate,conferenceRate,conferenceSuccessRate,routingDelayCost,shuttleRoundsToAgreement,suspensiveOverrideRate,bicameralDeadlockRate,dischargePetitionRate,committeeOverrideRate,committeeHearingRate,committeeQueueDelay,committeeAmendmentValueAdded,populationSeatDistortion,democraticResponsiveness,seatVoteDistortion,constituencyServiceConcentration,regionalTransferBias");
        for (String key : ScenarioReport.SUPPLEMENTAL_METRIC_KEYS) {
            builder.append(',').append(key);
        }
        builder.append('\n');
        for (CampaignRow row : result.rows()) {
            ScenarioReport report = row.report();
            builder.append(csvValue(row.caseKey())).append(',')
                    .append(csvValue(row.caseName())).append(',')
                    .append(csvValue(row.caseDescription())).append(',')
                    .append(format(row.caseWeight())).append(',')
                    .append(csvValue(row.scenarioKey())).append(',')
                    .append(csvValue(report.scenarioName())).append(',')
                    .append(report.totalBills()).append(',')
                    .append(format((double) report.totalBills() / runs)).append(',')
                    .append(report.enactedBills()).append(',')
                    .append(format((double) report.enactedBills() / runs)).append(',')
                    .append(format((report.totalBills() * report.floorConsiderationRate()) / runs)).append(',')
                    .append(format(report.directionalScore())).append(',')
                    .append(format(report.representativeQualityScore())).append(',')
                    .append(format(report.riskControlScore())).append(',')
                    .append(format(report.administrativeFeasibilityScore())).append(',')
                    .append(format(report.productivity())).append(',')
                    .append(format(report.floorConsiderationRate())).append(',')
                    .append(format(report.averageEnactedSupport())).append(',')
                    .append(format(report.averagePublicBenefit())).append(',')
                    .append(format(report.cooperationScore())).append(',')
                    .append(format(report.compromiseScore())).append(',')
                    .append(format(report.gridlockRate())).append(',')
                    .append(format(report.accessDenialRate())).append(',')
                    .append(format(report.committeeRejectionRate())).append(',')
                    .append(format(report.challengeRate())).append(',')
                    .append(format(report.controversialPassageRate())).append(',')
                    .append(format(report.weakPublicMandatePassageRate())).append(',')
                    .append(format(report.popularBillFailureRate())).append(',')
                    .append(format(report.averagePolicyShift())).append(',')
                    .append(format(report.averageProposerGain())).append(',')
                    .append(format(report.lobbyCaptureIndex())).append(',')
                    .append(format(report.publicAlignmentScore())).append(',')
                    .append(format(report.antiLobbyingSuccessRate())).append(',')
                    .append(format(report.privateGainRatio())).append(',')
                    .append(format(report.lobbySpendPerBill())).append(',')
                    .append(format(report.defensiveLobbyingShare())).append(',')
                    .append(format(report.captureReturnOnSpend())).append(',')
                    .append(format(report.publicPreferenceDistortion())).append(',')
                    .append(format(report.administrativeCostIndex())).append(',')
                    .append(format(report.amendmentRate())).append(',')
                    .append(format(report.averageAmendmentMovement())).append(',')
                    .append(format(report.minorityHarmIndex())).append(',')
                    .append(format(report.concentratedHarmPassageRate())).append(',')
                    .append(format(report.compensationRate())).append(',')
                    .append(format(report.legitimacyScore())).append(',')
                    .append(format(report.activeLawWelfare())).append(',')
                    .append(format(report.reversalRate())).append(',')
                    .append(format(report.timeToCorrectBadLaw())).append(',')
                    .append(format(report.statusQuoVolatility())).append(',')
                    .append(format(report.lowSupportActiveLawShare())).append(',')
                    .append(format(report.selectedAlternativeMedianDistance())).append(',')
                    .append(format(report.proposerAgendaAdvantage())).append(',')
                    .append(format(report.alternativeDiversity())).append(',')
                    .append(format(report.statusQuoWinRate())).append(',')
                    .append(format(report.publicBenefitPerLobbyDollar())).append(',')
                    .append(format(report.directLobbySpendShare())).append(',')
                    .append(format(report.agendaLobbySpendShare())).append(',')
                    .append(format(report.informationLobbySpendShare())).append(',')
                    .append(format(report.publicCampaignSpendShare())).append(',')
                    .append(format(report.litigationThreatSpendShare())).append(',')
                    .append(format(report.citizenReviewRate())).append(',')
                    .append(format(report.citizenCertificationRate())).append(',')
                    .append(format(report.citizenLegitimacy())).append(',')
                    .append(format(report.attentionSpendPerBill())).append(',')
                    .append(format(report.objectionWindowRate())).append(',')
                    .append(format(report.repealWindowReversalRate())).append(',')
                    .append(format(report.fastLaneRate())).append(',')
                    .append(format(report.middleLaneRate())).append(',')
                    .append(format(report.highRiskLaneRate())).append(',')
                    .append(format(report.challengeExhaustionRate())).append(',')
                    .append(format(report.falseNegativePassRate())).append(',')
                    .append(format(report.publicWillReviewRate())).append(',')
                    .append(format(report.publicSignalMovement())).append(',')
                    .append(format(report.districtAlignment())).append(',')
                    .append(format(report.crossBlocAdmissionRate())).append(',')
                    .append(format(report.affectedGroupSponsorshipRate())).append(',')
                    .append(format(report.averageCosponsors())).append(',')
                    .append(format(report.proposalBondForfeiture())).append(',')
                    .append(format(report.strategicDecoyRate())).append(',')
                    .append(format(report.proposerAccessGini())).append(',')
                    .append(format(report.welfarePerSubmittedBill())).append(',')
                    .append(report.vetoes()).append(',')
                    .append(report.overriddenVetoes()).append(',')
                    .append(format(report.interChamberConflictRate())).append(',')
                    .append(format(report.secondChamberKillRate())).append(',')
                    .append(format(report.conferenceRate())).append(',')
                    .append(format(report.conferenceSuccessRate())).append(',')
                    .append(format(report.routingDelayCost())).append(',')
                    .append(format(report.shuttleRoundsToAgreement())).append(',')
                    .append(format(report.suspensiveOverrideRate())).append(',')
                    .append(format(report.bicameralDeadlockRate())).append(',')
                    .append(format(report.dischargePetitionRate())).append(',')
                    .append(format(report.committeeOverrideRate())).append(',')
                    .append(format(report.committeeHearingRate())).append(',')
                    .append(format(report.committeeQueueDelay())).append(',')
                    .append(format(report.committeeAmendmentValueAdded())).append(',')
                    .append(format(report.populationSeatDistortion())).append(',')
                    .append(format(report.democraticResponsiveness())).append(',')
                    .append(format(report.seatVoteDistortion())).append(',')
                    .append(format(report.constituencyServiceConcentration())).append(',')
                    .append(format(report.regionalTransferBias()));
            for (String key : ScenarioReport.SUPPLEMENTAL_METRIC_KEYS) {
                builder.append(',').append(format(report.supplementalMetric(key)));
            }
            builder.append('\n');
        }
        return builder.toString();
    }

    private static String markdown(
            CampaignResult result,
            int runs,
            int legislators,
            int bills,
            long seed,
            int scenarioCount
    ) {
        Map<String, ScenarioAggregate> aggregateByScenario = aggregateByScenario(result.rows(), runs);
        StringBuilder builder = new StringBuilder();
        builder.append("# ").append(result.name()).append("\n\n");
        builder.append("Deterministic batch campaign for comparing institutional regimes across assumption sweeps.\n\n");
        builder.append("## Run Configuration\n\n");
        builder.append("- runs per case: ").append(runs).append('\n');
        builder.append("- legislators: ").append(legislators).append('\n');
        builder.append("- base bills per run: ").append(bills).append('\n');
        builder.append("- base seed: ").append(seed).append('\n');
        builder.append("- scenarios per case: ").append(scenarioCount).append('\n');
        builder.append("- experiment cases: ").append(caseCount(result.rows())).append("\n\n");
        if (hasWeightedCases(result.rows())) {
            builder.append("## Case Weights\n\n");
            builder.append("Scenario averages in this campaign are weighted by the case likelihood column below.\n\n");
            builder.append("| Case | Weight | Description |\n");
            builder.append("| --- | ---: | --- |\n");
            for (CampaignRow row : firstRowsByCase(result.rows())) {
                builder.append("| ")
                        .append(row.caseName()).append(" | ")
                        .append(format(row.caseWeight())).append(" | ")
                        .append(row.caseDescription()).append(" |\n");
            }
            builder.append('\n');
        }

        builder.append("## Headline Findings\n\n");
        appendHeadlineFindings(builder, result.rows(), aggregateByScenario);

        builder.append("## Metric Direction Legend\n\n");
        builder.append("- `↑` means a higher raw value is usually better.\n");
        builder.append("- `↓` means a lower raw value is usually better; directional scores invert these metrics before combining them.\n");
        builder.append("- `diag.` means the metric is context-dependent and should be read as institutional activity or risk context, not as automatically good or bad.\n");
        builder.append("- `Directional score` is a reading aid, not a final institutional verdict. It averages productivity, representative quality, risk control, and administrative feasibility. Representative quality averages welfare, enacted support, compromise, public alignment, and legitimacy. Risk control inverts chamber low-support passage, weak public-mandate passage, minority harm, lobby capture, public-preference distortion, concentrated-harm passage, proposer gain, and policy shift.\n\n");

        builder.append("## Scenario Averages Across Cases\n\n");
        builder.append("| Scenario | Directional score ↑ | Quality ↑ | Risk control ↑ | Admin feas. ↑ | Productivity ↑ | Enacted/run | Floor/run diag. | Welfare ↑ | Low-support ↓ | Weak public mandate ↓ | Admin cost ↓ | Minority harm ↓ | Legitimacy ↑ | Policy shift diag. | Proposer gain ↓ | Capture ↓ | Lobby spend diag. | Defensive spend diag. | Amend rate diag. | Compensation diag. | Anti-lobby pass ↑ | Challenge diag. | Floor diag. |\n");
        builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
        aggregateByScenario.values()
                .stream()
                .sorted(Comparator.comparing(ScenarioAggregate::scenarioKey))
                .forEach(summary -> builder.append("| ")
                        .append(summary.scenarioName()).append(" | ")
                        .append(format(summary.directionalScore())).append(" | ")
                        .append(format(summary.representativeQuality())).append(" | ")
                        .append(format(summary.riskControl())).append(" | ")
                        .append(format(summary.administrativeFeasibility())).append(" | ")
                        .append(format(summary.productivity())).append(" | ")
                        .append(format(summary.enactedPerRun())).append(" | ")
                        .append(format(summary.floorPerRun())).append(" | ")
                        .append(format(summary.welfare())).append(" | ")
                        .append(format(summary.lowSupport())).append(" | ")
                        .append(format(summary.weakPublicMandatePassage())).append(" | ")
                        .append(format(summary.administrativeCost())).append(" | ")
                        .append(format(summary.minorityHarm())).append(" | ")
                        .append(format(summary.legitimacy())).append(" | ")
                        .append(format(summary.policyShift())).append(" | ")
                        .append(format(summary.proposerGain())).append(" | ")
                        .append(format(summary.lobbyCapture())).append(" | ")
                        .append(format(summary.lobbySpendPerBill())).append(" | ")
                        .append(format(summary.defensiveLobbyingShare())).append(" | ")
                        .append(format(summary.amendmentRate())).append(" | ")
                        .append(format(summary.compensationRate())).append(" | ")
                        .append(format(summary.antiLobbyingSuccess())).append(" | ")
                        .append(format(summary.challengeRate())).append(" | ")
                        .append(format(summary.floor())).append(" |\n"));
        builder.append('\n');

        if (hasTimelineCases(result.rows())) {
            appendTimelineSection(builder, result.rows());
        }

        if (aggregateByScenario.containsKey("default-pass-challenge")) {
            builder.append("## Default-Pass Side Note: Challenge-Voucher Deltas\n\n");
            builder.append("Default enactment is no longer the main paper frame, but the campaign keeps this burden-shifting side comparison. Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.\n\n");
            builder.append("| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String caseKey : caseKeys(result.rows())) {
                CampaignRow open = find(result.rows(), caseKey, "default-pass");
                CampaignRow challenge = find(result.rows(), caseKey, "default-pass-challenge");
                if (open != null && challenge != null) {
                    builder.append("| ")
                            .append(open.caseName()).append(" | ")
                            .append(format(enactedPerRun(challenge, runs) - enactedPerRun(open, runs))).append(" | ")
                            .append(format(challenge.report().productivity() - open.report().productivity())).append(" | ")
                            .append(format(challenge.report().averagePublicBenefit() - open.report().averagePublicBenefit())).append(" | ")
                            .append(format(challenge.report().controversialPassageRate() - open.report().controversialPassageRate())).append(" | ")
                            .append(format(challenge.report().averagePolicyShift() - open.report().averagePolicyShift())).append(" | ")
                            .append(format(challenge.report().averageProposerGain() - open.report().averageProposerGain())).append(" | ")
                            .append(format(challenge.report().challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-challenge-party-t3-s082")
                || aggregateByScenario.containsKey("default-pass-escalation-q6-s082")) {
            builder.append("## Challenge Sweep Summary\n\n");
            builder.append("Delta values compare each challenge variant against open `default-pass` across all cases. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity deltas show the throughput cost or gain.\n\n");
            builder.append("| Scenario | Productivity delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: |\n");
            for (ScenarioAggregate summary : aggregateByScenario.values()) {
                if (summary.scenarioKey().startsWith("default-pass-challenge")
                        || summary.scenarioKey().startsWith("default-pass-escalation")) {
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - aggregateByScenario.get("default-pass").productivity())).append(" | ")
                            .append(format(summary.lowSupport() - aggregateByScenario.get("default-pass").lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - aggregateByScenario.get("default-pass").policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - aggregateByScenario.get("default-pass").proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-cross-bloc")) {
            builder.append("## Cross-Bloc Cosponsorship Deltas\n\n");
            builder.append("Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.\n\n");
            builder.append("| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-cross-bloc",
                    "default-pass-cross-bloc-strong",
                    "default-pass-cross-bloc-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.floor() - open.floor())).append(" | ")
                            .append(format(summary.accessDenied() - open.accessDenied())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-adaptive-track")) {
            builder.append("## Adaptive Track Deltas\n\n");
            builder.append("Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.\n\n");
            builder.append("| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-adaptive-track",
                    "default-pass-adaptive-track-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.floor() - open.floor())).append(" | ")
                            .append(format(summary.accessDenied())).append(" | ")
                            .append(format(summary.committeeRejected())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-sunset-trial")) {
            builder.append("## Sunset Trial Deltas\n\n");
            builder.append("Delta values compare provisional enactment with automatic review against open `default-pass` across all cases. The trial process expires risky enacted bills that fail review, rolling the status quo back.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-sunset-trial",
                    "default-pass-sunset-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-law-registry")) {
            builder.append("## Law-Registry Deltas\n\n");
            builder.append("Delta values compare delayed multi-session review against open `default-pass`. The registry keeps provisional laws active, reviews them after a delay, and can roll back bad enactments.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Reversal rate | Correction delay | Active-law welfare | Low-support active laws | Status-quo volatility delta |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-law-registry",
                    "default-pass-law-registry-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.reversalRate())).append(" | ")
                            .append(format(summary.timeToCorrectBadLaw())).append(" | ")
                            .append(format(summary.activeLawWelfare())).append(" | ")
                            .append(format(summary.lowSupportActiveLawShare())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-earned-credits")) {
            builder.append("## Earned Proposal-Credit Deltas\n\n");
            builder.append("Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.\n\n");
            builder.append("| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-earned-credits",
                    "default-pass-earned-credits-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.floor() - open.floor())).append(" | ")
                            .append(format(summary.accessDenied())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-anti-capture-bundle")) {
            builder.append("## Anti-Capture Deltas\n\n");
            builder.append("Delta values compare anti-capture mechanisms against open `default-pass` across all cases. Negative capture and private-gain-ratio deltas are desirable; anti-lobby pass is the share of generated anti-lobbying reform bills enacted.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Capture delta | Public-alignment delta | Anti-lobby pass delta | Private-gain-ratio delta | Low-support delta |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-lobby-firewall",
                    "default-pass-lobby-transparency",
                    "default-pass-public-interest-screen",
                    "default-pass-lobby-audit",
                    "default-pass-anti-capture-bundle"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lobbyCapture() - open.lobbyCapture())).append(" | ")
                            .append(format(summary.publicAlignment() - open.publicAlignment())).append(" | ")
                            .append(format(summary.antiLobbyingSuccess() - open.antiLobbyingSuccess())).append(" | ")
                            .append(format(summary.privateGainRatio() - open.privateGainRatio())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-budgeted-lobbying")) {
            builder.append("## Budgeted Lobbying Deltas\n\n");
            builder.append("Delta values compare explicit budgeted lobbying scenarios against open `default-pass` across all cases. Lobby spend is normalized per potential bill; defensive spend is the share of lobbying spend aimed at anti-lobbying reform bills.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Capture delta | Lobby spend/bill | Defensive spend share | Capture return/spend | Anti-lobby pass delta | Public-distortion delta |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-budgeted-lobbying",
                    "default-pass-budgeted-lobbying-transparency",
                    "default-pass-budgeted-lobbying-bundle"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lobbyCapture() - open.lobbyCapture())).append(" | ")
                            .append(format(summary.lobbySpendPerBill())).append(" | ")
                            .append(format(summary.defensiveLobbyingShare())).append(" | ")
                            .append(format(summary.captureReturnOnSpend())).append(" | ")
                            .append(format(summary.antiLobbyingSuccess() - open.antiLobbyingSuccess())).append(" | ")
                            .append(format(summary.publicPreferenceDistortion() - open.publicPreferenceDistortion())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-lobby-channel-bundle")
                && aggregateByScenario.containsKey("default-pass-budgeted-lobbying")) {
            builder.append("## Lobbying-Channel Deltas\n\n");
            builder.append("Delta values compare channel-specific lobbying safeguards against explicit budgeted lobbying. Spend-share columns show where lobby budgets are going after each scenario's constraints.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Capture delta | Public-benefit/lobby dollar | Anti-lobby pass delta | Direct | Agenda | Info | Public | Litigation |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            ScenarioAggregate baseLobbying = aggregateByScenario.get("default-pass-budgeted-lobbying");
            for (String scenarioKey : List.of(
                    "default-pass-democracy-vouchers",
                    "default-pass-public-advocate",
                    "default-pass-blind-lobby-review",
                    "default-pass-defensive-lobby-cap",
                    "default-pass-lobby-channel-bundle"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - baseLobbying.productivity())).append(" | ")
                            .append(format(summary.welfare() - baseLobbying.welfare())).append(" | ")
                            .append(format(summary.lobbyCapture() - baseLobbying.lobbyCapture())).append(" | ")
                            .append(format(summary.publicBenefitPerLobbyDollar())).append(" | ")
                            .append(format(summary.antiLobbyingSuccess() - baseLobbying.antiLobbyingSuccess())).append(" | ")
                            .append(format(summary.directLobbySpendShare())).append(" | ")
                            .append(format(summary.agendaLobbySpendShare())).append(" | ")
                            .append(format(summary.informationLobbySpendShare())).append(" | ")
                            .append(format(summary.publicCampaignSpendShare())).append(" | ")
                            .append(format(summary.litigationThreatSpendShare())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-citizen-certificate")) {
            builder.append("## Citizen-Panel Deltas\n\n");
            builder.append("Delta values compare deliberative mini-public review variants against open `default-pass`. Review rate is the share of potential bills reviewed by the synthetic panel; certification rate is the share of reviews receiving a positive certificate.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Low-support delta | Legitimacy delta | Review rate | Certification | Citizen legitimacy |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            ScenarioAggregate open = aggregateByScenario.get("default-pass");
            for (String scenarioKey : List.of(
                    "default-pass-citizen-certificate",
                    "default-pass-citizen-active-routing",
                    "default-pass-citizen-threshold",
                    "default-pass-citizen-agenda"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.legitimacy() - open.legitimacy())).append(" | ")
                            .append(format(summary.citizenReviewRate())).append(" | ")
                            .append(format(summary.citizenCertificationRate())).append(" | ")
                            .append(format(summary.citizenLegitimacy())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-weighted-agenda-lottery")) {
            builder.append("## Agenda-Scarcity Deltas\n\n");
            builder.append("Delta values compare agenda-scarcity variants against open `default-pass`. Floor and access-denial columns show direct attention rationing; objection and repeal columns show public contestation windows.\n\n");
            builder.append("| Scenario | Productivity delta | Floor delta | Access-denial delta | Welfare delta | Low-support delta | Attention spend | Objection window | Repeal reversals |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            ScenarioAggregate open = aggregateByScenario.get("default-pass");
            for (String scenarioKey : List.of(
                    "default-pass-weighted-agenda-lottery",
                    "default-pass-random-agenda-lottery",
                    "default-pass-quadratic-attention",
                    "default-pass-public-objection",
                    "default-pass-repeal-window",
                    "default-pass-earned-credits",
                    "default-pass-challenge",
                    "default-pass-informed-guarded"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.floor() - open.floor())).append(" | ")
                            .append(format(summary.accessDenied() - open.accessDenied())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.attentionSpendPerBill())).append(" | ")
                            .append(format(summary.objectionWindowRate())).append(" | ")
                            .append(format(summary.repealWindowReversalRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-constituent-public-will")) {
            builder.append("## Roadmap-Completion Diagnostics\n\n");
            builder.append("These scenarios cover the remaining planned gaps: constituent-grounded public signals, refundable proposal bonds, richer cosponsorship gates, multi-round mediation, strategic alternatives, challenge allocation/path variants, adaptive route sensitivity, and proposal-cost variants.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Low-support delta | False-negative pass | Public-will review | Public signal move | District alignment | Bond forfeiture | Cross-bloc admission | Cosponsors | Route fast/mid/high | Challenge exhaustion | Strategic decoys | Proposer access Gini | Welfare/submitted |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |\n");
            ScenarioAggregate open = aggregateByScenario.get("default-pass");
            for (String scenarioKey : List.of(
                    "default-pass-constituent-public-will",
                    "default-pass-constituent-citizen-panel",
                    "default-pass-proposal-bonds",
                    "default-pass-proposal-bonds-challenge",
                    "default-pass-cross-bloc-credit-discount",
                    "default-pass-affected-sponsor-gate",
                    "default-pass-multiround-mediation",
                    "default-pass-multiround-mediation-challenge",
                    "default-pass-alternatives-strategic",
                    "default-pass-adaptive-proposers",
                    "default-pass-adaptive-proposers-lobbying",
                    "default-pass-strategic-lobbying",
                    "default-pass-challenge-party-proportional",
                    "default-pass-challenge-minority-bonus",
                    "default-pass-challenge-supermajority",
                    "default-pass-challenge-committee",
                    "default-pass-challenge-info-active",
                    "default-pass-adaptive-track-lenient",
                    "default-pass-adaptive-track-strict",
                    "default-pass-adaptive-track-citizen-high-risk",
                    "default-pass-adaptive-track-supermajority-high-risk",
                    "default-pass-law-registry-fast-review",
                    "default-pass-law-registry-slow-review",
                    "default-pass-cost-public-waiver",
                    "default-pass-cost-lobby-surcharge",
                    "default-pass-member-quota"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary == null) {
                    continue;
                }
                builder.append("| ")
                        .append(summary.scenarioName()).append(" | ")
                        .append(format(summary.productivity() - open.productivity())).append(" | ")
                        .append(format(summary.welfare() - open.welfare())).append(" | ")
                        .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                        .append(format(summary.falseNegativePassRate())).append(" | ")
                        .append(format(summary.publicWillReviewRate())).append(" | ")
                        .append(format(summary.publicSignalMovement())).append(" | ")
                        .append(format(summary.districtAlignment())).append(" | ")
                        .append(format(summary.proposalBondForfeiture())).append(" | ")
                        .append(format(summary.crossBlocAdmissionRate())).append(" | ")
                        .append(format(summary.averageCosponsors())).append(" | ")
                        .append(format(summary.fastLaneRate())).append("/")
                        .append(format(summary.middleLaneRate())).append("/")
                        .append(format(summary.highRiskLaneRate())).append(" | ")
                        .append(format(summary.challengeExhaustionRate())).append(" | ")
                        .append(format(summary.strategicDecoyRate())).append(" | ")
                        .append(format(summary.proposerAccessGini())).append(" | ")
                        .append(format(summary.welfarePerSubmittedBill())).append(" |\n");
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-mediation")) {
            builder.append("## Mediation Deltas\n\n");
            builder.append("Delta values compare structured amendment mediation against the matching non-mediated scenario. Amendment rate is the share of potential bills whose policy position moved before final voting.\n\n");
            builder.append("| Scenario | Baseline | Productivity delta | Welfare delta | Compromise delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Amendment rate | Amendment movement |\n");
            builder.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            appendMediationDelta(builder, aggregateByScenario, "default-pass-mediation", "default-pass");
            appendMediationDelta(builder, aggregateByScenario, "default-pass-budgeted-lobbying-mediation", "default-pass-budgeted-lobbying");
            appendMediationDelta(builder, aggregateByScenario, "simple-majority-mediation", "simple-majority");
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-compensation")) {
            builder.append("## Distributional-Harm Deltas\n\n");
            builder.append("Delta values compare harm guardrails against open `default-pass` across all cases. Lower minority harm and higher legitimacy are desirable; compensation rate measures how often the proposal content was amended to reduce concentrated loss.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Minority-harm delta | Legitimacy delta | Concentrated-harm passage | Compensation rate | Low-support delta |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-harm-threshold",
                    "default-pass-compensation",
                    "default-pass-affected-consent"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.minorityHarm() - open.minorityHarm())).append(" | ")
                            .append(format(summary.legitimacy() - open.legitimacy())).append(" | ")
                            .append(format(summary.concentratedHarmPassage())).append(" | ")
                            .append(format(summary.compensationRate())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-alternatives-pairwise")) {
            builder.append("## Policy-Tournament Deltas\n\n");
            builder.append("Delta values compare competing-alternative scenarios against open `default-pass` across all cases. Alternative diversity is the average number of alternatives/status quo options considered; status-quo win rate is the share of tournaments where no alternative advanced to final ratification.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Median distance | Proposer agenda advantage | Alternative diversity | Status-quo win |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "simple-majority-alternatives-pairwise",
                    "default-pass-alternatives-benefit",
                    "default-pass-alternatives-support",
                    "default-pass-alternatives-median",
                    "default-pass-alternatives-pairwise",
                    "default-pass-obstruction-substitute"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.selectedAlternativeMedianDistance())).append(" | ")
                            .append(format(summary.proposerAgendaAdvantage())).append(" | ")
                            .append(format(summary.alternativeDiversity())).append(" | ")
                            .append(format(summary.statusQuoWinRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-cost")) {
            builder.append("## Proposal-Cost Deltas\n\n");
            builder.append("Delta values compare `default-pass-cost` against open `default-pass` in the same case. Negative enacted-per-run, floor-per-run, low-support, and policy-shift deltas show the proposal-cost screen reducing flooding and volatility.\n\n");
            builder.append("| Case | Enacted/run delta | Floor/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String caseKey : caseKeys(result.rows())) {
                CampaignRow open = find(result.rows(), caseKey, "default-pass");
                CampaignRow cost = find(result.rows(), caseKey, "default-pass-cost");
                if (open != null && cost != null) {
                    builder.append("| ")
                            .append(open.caseName()).append(" | ")
                            .append(format(enactedPerRun(cost, runs) - enactedPerRun(open, runs))).append(" | ")
                            .append(format(floorPerRun(cost, runs) - floorPerRun(open, runs))).append(" | ")
                            .append(format(cost.report().productivity() - open.report().productivity())).append(" | ")
                            .append(format(cost.report().averagePublicBenefit() - open.report().averagePublicBenefit())).append(" | ")
                            .append(format(cost.report().controversialPassageRate() - open.report().controversialPassageRate())).append(" | ")
                            .append(format(cost.report().averagePolicyShift() - open.report().averagePolicyShift())).append(" | ")
                            .append(format(cost.report().averageProposerGain() - open.report().averageProposerGain())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-informed-guarded")) {
            builder.append("## Default-Pass Guardrail Deltas\n\n");
            builder.append("Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.\n\n");
            builder.append("| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: |\n");
            for (String caseKey : caseKeys(result.rows())) {
                CampaignRow open = find(result.rows(), caseKey, "default-pass");
                CampaignRow guarded = find(result.rows(), caseKey, "default-pass-informed-guarded");
                if (open != null && guarded != null) {
                    builder.append("| ")
                            .append(open.caseName()).append(" | ")
                            .append(format(guarded.report().productivity() - open.report().productivity())).append(" | ")
                            .append(format(guarded.report().averagePublicBenefit() - open.report().averagePublicBenefit())).append(" | ")
                            .append(format(guarded.report().controversialPassageRate() - open.report().controversialPassageRate())).append(" | ")
                            .append(format(guarded.report().averagePolicyShift() - open.report().averagePolicyShift())).append(" | ")
                            .append(format(guarded.report().averageProposerGain() - open.report().averageProposerGain())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        builder.append("## Case Highlights\n\n");
        builder.append("| Case | Best welfare | Most productive | Lowest weak public-mandate passage |\n");
        builder.append("| --- | --- | --- | --- |\n");
        for (String caseKey : caseKeys(result.rows())) {
            List<CampaignRow> caseRows = rowsForCase(result.rows(), caseKey);
            CampaignRow bestWelfare = max(caseRows, Comparator.comparingDouble(row -> row.report().averagePublicBenefit()));
            CampaignRow mostProductive = max(caseRows, Comparator.comparingDouble(row -> row.report().productivity()));
            CampaignRow lowestWeakMandate = min(caseRows, Comparator.comparingDouble(row -> row.report().weakPublicMandatePassageRate()));
            builder.append("| ")
                    .append(caseRows.get(0).caseName()).append(" | ")
                    .append(bestWelfare.report().scenarioName()).append(" (").append(format(bestWelfare.report().averagePublicBenefit())).append(") | ")
                    .append(mostProductive.report().scenarioName()).append(" (").append(format(mostProductive.report().productivity())).append(") | ")
                    .append(lowestWeakMandate.report().scenarioName()).append(" (").append(format(lowestWeakMandate.report().weakPublicMandatePassageRate())).append(") |\n");
        }
        builder.append('\n');

        builder.append("## Interpretation\n\n");
        if (aggregateByScenario.containsKey("committee-regular-order")
                && aggregateByScenario.containsKey("risk-routed-majority")) {
            builder.append("- This is a breadth-first paper campaign. Default pass is retained as one burden-shifting stress test, while the main comparison spans conventional thresholds, committee-first regular order, coalition confidence, policy tournaments, citizen review, agenda scarcity, proposal accountability, harm/compensation rules, anti-capture safeguards, adaptive risk routing, and law-registry review.\n");
            builder.append("- Open default-pass remains the throughput extreme, but its high weak public-mandate passage and policy movement make it a diagnostic endpoint rather than the project focus.\n");
            builder.append("- Policy tournaments and risk-routed majority systems occupy a promising compromise/productivity middle ground in this synthetic campaign, but tournament variants remain sensitive to clone, decoy, and overload stress; committee-first, public-interest, citizen, and parliamentary-style gates control risk but give up substantial throughput.\n");
            builder.append("- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality, and generated welfare remains conditional on model assumptions.\n");
            builder.append("- The next model extension should deepen non-default families beyond their current prototypes: multidimensional package bargaining, judicial/court intervention, executive emergency/delegated rulemaking, direct-democracy routes, electoral feedback, and media/information ecosystems.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-constituent-public-will")) {
            builder.append("- Roadmap-completion scenarios add district-grounded public signals, refundable proposal bonds, richer cosponsorship diagnostics, multi-round mediation, strategic alternatives, adaptive proposer behavior, strategic lobby-channel learning, challenge allocation/path variants, adaptive-route rates, and proposal-cost variants.\n");
            builder.append("- The next model extension should deepen endogeneity: challengers, amendment coalitions, constituent publics, and alternative drafters should adapt to the institutional rules over repeated sessions.\n\n");
        } else if (hasTimelineCases(result.rows())) {
            builder.append("- Timeline scenarios are stylized stress paths, not historical calibration. They increase polarization, party loyalty, lobbying pressure, and proposal pressure while reducing compromise culture and constituency responsiveness.\n");
            builder.append("- The timeline comparison should be read as a degradation test: institutions that preserve compromise and productivity under later-era assumptions are more robust than systems that only work in low-contention settings.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-weighted-agenda-lottery")) {
            builder.append("- Agenda-scarcity variants test non-committee ways to ration floor attention, including weighted/random lotteries, quadratic credits, and public objection or repeal windows.\n");
            builder.append("- The next model extension should add richer constituent and affected-group structure so public objection and citizen-panel signals are grounded in represented districts rather than generated bill fields.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-citizen-certificate")) {
            builder.append("- Citizen-panel scenarios test whether an independent mini-public can add information and legitimacy without reproducing standing committee control.\n");
            builder.append("- The next model extension should add agenda-scarcity variants, because the simulator now has independent review but still needs non-committee ways to ration floor attention and public objection capacity.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-lobby-channel-bundle")) {
            builder.append("- Lobbying-depth scenarios split organized-interest influence into direct pressure, agenda access, information distortion, public campaigns, litigation threats, and defensive spending against reform.\n");
            builder.append("- The next model extension should add deliberative citizen review, because the simulator now has richer organized-interest pressure but still lacks an independent public legitimacy screen.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-alternatives-pairwise")) {
            builder.append("- Policy-tournament scenarios test whether agenda-setter power falls when multiple alternatives compete before a final yes/no ratification vote.\n");
            builder.append("- The next model extension should add deliberative citizen review or richer lobbying channels, because the simulator now has agenda competition, harm guardrails, law review, and mediation but still lacks an independent public legitimacy screen.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-mediation")) {
            builder.append("- Structured mediation scenarios let a bounded amendment stage move bills toward the chamber median/status quo before the final yes/no vote.\n");
            builder.append("- The next model extension should add richer constituent and affected-group structure, because compromise quality should be judged against public will and concentrated harms rather than only chamber support.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-budgeted-lobbying")) {
            builder.append("- Budgeted lobbying scenarios make organized interests explicit actors with budgets, issue targets, and defensive spending against anti-lobbying reform.\n");
            builder.append("- The next model extension should add structured amendment or mediation, because capture controls and agenda screens still rarely turn narrow bills into better compromises before the final yes/no choice.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-anti-capture-bundle")) {
            builder.append("- Anti-capture mechanisms test lobbying as institutional pressure: anti-lobbying bills now face organized opposition, while high-private-gain bills create measurable capture risk.\n");
            builder.append("- The next model extension should make lobbying groups explicit actors with budgets, issue targets, defensive spending against anti-lobbying bills, and separate channels for money, information, litigation threat, and public campaigns.\n\n");
        } else if (aggregateByScenario.containsKey("default-pass-challenge-party-t3-s082")) {
            builder.append("- The challenge sweep compares token budgets, challenge thresholds, party-held tokens, member-held tokens, and tokenless q-member escalation.\n");
            if (aggregateByScenario.containsKey("default-pass-cross-bloc")) {
                builder.append("- Cross-bloc cosponsorship tests coalition breadth as a pre-floor agenda gate, before default-pass or challenge mechanics can operate.\n");
                if (aggregateByScenario.containsKey("default-pass-adaptive-track")) {
                    builder.append("- Adaptive procedural tracks test whether low-risk bills can stay in a fast lane while high-risk bills receive stronger review.\n");
                    if (aggregateByScenario.containsKey("default-pass-sunset-trial")) {
                        builder.append("- Sunset trial rules test whether risky default enactments can be made reversible after automatic review.\n");
                        if (aggregateByScenario.containsKey("default-pass-earned-credits")) {
                            builder.append("- Earned proposal credits test whether agenda access can learn from proposer track records instead of using only fixed up-front costs.\n");
                            builder.append("- The next model extension should add explicit anti-capture systems, because lobbying currently appears mostly as bill-level pressure rather than as self-protective institutional influence.\n\n");
                        } else {
                            builder.append("- The next model extension should add earned proposal credits, because agenda access still does not learn from proposer track records.\n\n");
                        }
                    } else {
                        builder.append("- The next model extension should add sunset trial legislation, because the remaining risk is bad-law persistence after enactment.\n\n");
                    }
                } else {
                    builder.append("- The next model extension should add adaptive procedural tracks, because the agenda system now needs to route bills by risk rather than screening every bill with one rule.\n\n");
                }
            } else {
                builder.append("- The next model extension should add coalition-breadth proposal access, because challenge mechanics still operate after a bill enters the agenda.\n\n");
            }
        } else {
            builder.append("- The next model extension should sweep challenge-token budgets, challenge thresholds, and proposal-cost mechanisms, because agenda screening is now the central default-pass tradeoff.\n\n");
        }
        builder.append("## Reproduction\n\n");
        builder.append("```sh\nmake campaign\n```\n");
        return builder.toString();
    }

    private static void appendTimelineSection(StringBuilder builder, List<CampaignRow> rows) {
        builder.append("## Timeline Contention Path\n\n");
        builder.append("This campaign is a stylized longitudinal stress path, not a calibrated history. The contention index is computed as `0.50 * gridlock + 0.30 * (1 - compromise) + 0.20 * weakPublicMandatePassage`, so it rises when a system blocks more, compromises less, or enacts more bills with generated public support below majority.\n\n");
        builder.append("| Era | Scenario | Productivity | Compromise | Gridlock | Weak public mandate | Contention index |\n");
        builder.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |\n");
        for (CampaignRow eraRow : firstRowsByCase(rows)) {
            for (String scenarioKey : List.of(
                    "current-system",
                    "simple-majority",
                    "committee-regular-order",
                    "parliamentary-coalition-confidence",
                    "simple-majority-alternatives-pairwise",
                    "citizen-assembly-threshold",
                    "risk-routed-majority",
                    "portfolio-hybrid-legislature",
                    "expanded-portfolio-hybrid-legislature",
                    "default-pass",
                    "default-pass-multiround-mediation-challenge"
            )) {
                CampaignRow row = find(rows, eraRow.caseKey(), scenarioKey);
                if (row == null) {
                    continue;
                }
                ScenarioReport report = row.report();
                builder.append("| ")
                        .append(row.caseName()).append(" | ")
                        .append(report.scenarioName()).append(" | ")
                        .append(format(report.productivity())).append(" | ")
                        .append(format(report.compromiseScore())).append(" | ")
                        .append(format(report.gridlockRate())).append(" | ")
                        .append(format(report.weakPublicMandatePassageRate())).append(" | ")
                        .append(format(contentionIndex(report))).append(" |\n");
            }
        }
        builder.append('\n');
    }

    private static void appendHeadlineFindings(
            StringBuilder builder,
            List<CampaignRow> rows,
            Map<String, ScenarioAggregate> aggregateByScenario
    ) {
        ScenarioAggregate openDefault = aggregateByScenario.get("default-pass");
        ScenarioAggregate informedGuarded = aggregateByScenario.get("default-pass-informed-guarded");
        ScenarioAggregate proposalCost = aggregateByScenario.get("default-pass-cost");
        ScenarioAggregate challenge = aggregateByScenario.get("default-pass-challenge");
        ScenarioAggregate crossBloc = aggregateByScenario.get("default-pass-cross-bloc");
        ScenarioAggregate adaptive = aggregateByScenario.get("default-pass-adaptive-track");
        ScenarioAggregate sunset = aggregateByScenario.get("default-pass-sunset-trial");
        ScenarioAggregate credits = aggregateByScenario.get("default-pass-earned-credits");
        ScenarioAggregate antiCaptureBundle = aggregateByScenario.get("default-pass-anti-capture-bundle");
        ScenarioAggregate budgetedLobbying = aggregateByScenario.get("default-pass-budgeted-lobbying");
        ScenarioAggregate channelBundle = aggregateByScenario.get("default-pass-lobby-channel-bundle");
        ScenarioAggregate citizenCertificate = aggregateByScenario.get("default-pass-citizen-certificate");
        ScenarioAggregate weightedLottery = aggregateByScenario.get("default-pass-weighted-agenda-lottery");
        ScenarioAggregate quadraticAttention = aggregateByScenario.get("default-pass-quadratic-attention");
        ScenarioAggregate publicObjection = aggregateByScenario.get("default-pass-public-objection");
        ScenarioAggregate repealWindow = aggregateByScenario.get("default-pass-repeal-window");
        ScenarioAggregate pairwiseAlternatives = aggregateByScenario.get("default-pass-alternatives-pairwise");
        ScenarioAggregate simpleMajority = aggregateByScenario.get("simple-majority");
        ScenarioAggregate bestWelfare = aggregateByScenario.values()
                .stream()
                .max(Comparator.comparingDouble(ScenarioAggregate::welfare))
                .orElseThrow();
        ScenarioAggregate bestDirectional = aggregateByScenario.values()
                .stream()
                .max(Comparator.comparingDouble(ScenarioAggregate::directionalScore))
                .orElseThrow();
        ScenarioAggregate bestProductivity = aggregateByScenario.values()
                .stream()
                .max(Comparator.comparingDouble(ScenarioAggregate::productivity))
                .orElseThrow();
        ScenarioAggregate bestCompromise = aggregateByScenario.values()
                .stream()
                .max(Comparator.comparingDouble(ScenarioAggregate::compromise))
                .orElseThrow();
        if (aggregateByScenario.containsKey("committee-regular-order")
                && aggregateByScenario.containsKey("risk-routed-majority")) {
            ScenarioAggregate currentSystem = aggregateByScenario.get("current-system");
            builder.append("- The main comparison campaign is breadth-first: ")
                    .append(aggregateByScenario.size())
                    .append(" scenario families are compared across the same synthetic worlds, with default enactment retained as one stress-test family rather than the organizing case.\n");
            builder.append("- The scalar directional score is productivity-sensitive: its highest value came from ")
                    .append(bestDirectional.scenarioName())
                    .append(" at ")
                    .append(format(bestDirectional.directionalScore()))
                    .append(", which is why the report treats the score as a profile aid rather than a recommendation.\n");
            builder.append("- Highest average welfare came from ")
                    .append(bestWelfare.scenarioName())
                    .append(" at ")
                    .append(format(bestWelfare.welfare()))
                    .append("; highest compromise came from ")
                    .append(bestCompromise.scenarioName())
                    .append(" at ")
                    .append(format(bestCompromise.compromise()))
                    .append(".\n");
            builder.append("- Highest productivity came from ")
                    .append(bestProductivity.scenarioName())
                    .append(" at ")
                    .append(format(bestProductivity.productivity()))
                    .append(".\n");
            if (openDefault != null) {
                builder.append("- Open default-pass averaged ")
                        .append(format(openDefault.productivity()))
                        .append(" productivity, ")
                        .append(format(openDefault.weakPublicMandatePassage()))
                        .append(" weak public-mandate passage, and ")
                        .append(format(openDefault.policyShift()))
                        .append(" policy shift, so it functions as a throughput/risk endpoint.\n");
            }
            if (currentSystem != null) {
                builder.append("- The stylized U.S.-like conventional benchmark averaged ")
                        .append(format(currentSystem.productivity()))
                        .append(" productivity and ")
                        .append(format(currentSystem.welfare()))
                        .append(" welfare: it protects quality in the synthetic generator partly by allowing few proposals through.\n");
            }
            ScenarioAggregate portfolio = aggregateByScenario.get("portfolio-hybrid-legislature");
            ScenarioAggregate expandedPortfolio = aggregateByScenario.get("expanded-portfolio-hybrid-legislature");
            ScenarioAggregate pairwise = aggregateByScenario.get("simple-majority-alternatives-pairwise");
            ScenarioAggregate riskRouted = aggregateByScenario.get("risk-routed-majority");
            if (portfolio != null && pairwise != null && riskRouted != null) {
                builder.append("- The portfolio hybrid combines risk routing, pairwise alternatives, citizen/harm review, proposal bonds, anti-capture safeguards, and law review. It averaged ")
                        .append(format(portfolio.productivity()))
                        .append(" productivity, ")
                        .append(format(portfolio.compromise()))
                        .append(" compromise, ")
                        .append(format(portfolio.riskControl()))
                        .append(" risk control, and ")
                        .append(format(portfolio.directionalScore()))
                        .append(" directional score, situating it between pairwise alternatives and risk routing rather than replacing the tradeoff frontier.\n");
            }
            if (expandedPortfolio != null) {
                builder.append("- The expanded portfolio hybrid adds district-public, long-horizon strategy, omnibus bargaining, influence-system, and constitutional-court architecture proxies. It averaged ")
                        .append(format(expandedPortfolio.productivity()))
                        .append(" productivity, ")
                        .append(format(expandedPortfolio.compromise()))
                        .append(" compromise, ")
                        .append(format(expandedPortfolio.riskControl()))
                        .append(" risk control, and ")
                        .append(format(expandedPortfolio.directionalScore()))
                        .append(" directional score; its value is diagnostic because extra safeguards also increase complexity.\n");
            }
            builder.append('\n');
            return;
        }
        if (openDefault == null) {
            builder.append("- This focused campaign does not include the open default-pass baseline, so relative headline deltas are reported in the diagnostic sections below.\n");
            builder.append("- Highest average welfare in this campaign came from ")
                    .append(bestWelfare.scenarioName())
                    .append(" at ")
                    .append(format(bestWelfare.welfare()))
                    .append(".\n");
            builder.append("- Highest productivity came from ")
                    .append(bestProductivity.scenarioName())
                    .append(" at ")
                    .append(format(bestProductivity.productivity()))
                    .append(", while highest compromise came from ")
                    .append(bestCompromise.scenarioName())
                    .append(" at ")
                    .append(format(bestCompromise.compromise()))
                    .append(".\n");
            builder.append("- Highest directional score, where lower-better risk metrics are inverted, came from ")
                    .append(bestDirectional.scenarioName())
                    .append(" at ")
                    .append(format(bestDirectional.directionalScore()))
                    .append(".\n\n");
            return;
        }

        builder.append("- Open default-pass averaged ")
                .append(format(openDefault.productivity()))
                .append(" productivity");
        if (simpleMajority != null) {
            builder.append(", versus ")
                    .append(format(simpleMajority.productivity()))
                    .append(" for simple majority");
        }
        builder.append(".\n");
        builder.append("- Open default-pass also averaged ")
                .append(format(openDefault.weakPublicMandatePassage()))
                .append(" weak public-mandate passage and ")
                .append(format(openDefault.policyShift()))
                .append(" policy shift.\n");
        builder.append("- Highest directional score, where lower-better risk metrics are inverted before combination, came from ")
                .append(bestDirectional.scenarioName())
                .append(" at ")
                .append(format(bestDirectional.directionalScore()))
                .append(".\n");
        if (informedGuarded != null) {
            double lowSupportReduction = openDefault.lowSupport() - informedGuarded.lowSupport();
            double policyShiftReduction = openDefault.policyShift() - informedGuarded.policyShift();
            double productivityChange = informedGuarded.productivity() - openDefault.productivity();
            builder.append("- Informed guarded default-pass reduced low-support passage by ")
                    .append(format(lowSupportReduction))
                    .append(" and reduced policy shift by ")
                    .append(format(policyShiftReduction))
                    .append(", while changing productivity by ")
                    .append(format(productivityChange))
                    .append(".\n");
        }
        if (proposalCost != null) {
            builder.append("- Proposal-cost screening reduced floor load by ")
                    .append(format(openDefault.floorPerRun() - proposalCost.floorPerRun()))
                    .append(" bills/run and enactments by ")
                    .append(format(openDefault.enactedPerRun() - proposalCost.enactedPerRun()))
                    .append(" bills/run, but raised proposer gain by ")
                    .append(format(proposalCost.proposerGain() - openDefault.proposerGain()))
                    .append(".\n");
        }
        if (challenge != null) {
            builder.append("- Challenge vouchers averaged ")
                    .append(format(challenge.challengeRate()))
                    .append(" challenge use, changed productivity by ")
                    .append(format(challenge.productivity() - openDefault.productivity()))
                    .append(", and changed low-support passage by ")
                    .append(format(challenge.lowSupport() - openDefault.lowSupport()))
                    .append(" relative to open default-pass.\n");
        }
        if (crossBloc != null) {
            builder.append("- Cross-bloc cosponsorship changed productivity by ")
                    .append(format(crossBloc.productivity() - openDefault.productivity()))
                    .append(", floor consideration by ")
                    .append(format(crossBloc.floor() - openDefault.floor()))
                    .append(", and low-support passage by ")
                    .append(format(crossBloc.lowSupport() - openDefault.lowSupport()))
                    .append(" relative to open default-pass.\n");
        }
        if (adaptive != null) {
            builder.append("- Adaptive tracks changed productivity by ")
                    .append(format(adaptive.productivity() - openDefault.productivity()))
                    .append(", low-support passage by ")
                    .append(format(adaptive.lowSupport() - openDefault.lowSupport()))
                    .append(", and policy shift by ")
                    .append(format(adaptive.policyShift() - openDefault.policyShift()))
                    .append(" relative to open default-pass.\n");
        }
        if (sunset != null) {
            builder.append("- Sunset trial review changed productivity by ")
                    .append(format(sunset.productivity() - openDefault.productivity()))
                    .append(", welfare by ")
                    .append(format(sunset.welfare() - openDefault.welfare()))
                    .append(", and policy shift by ")
                    .append(format(sunset.policyShift() - openDefault.policyShift()))
                    .append(" relative to open default-pass.\n");
        }
        if (credits != null) {
            builder.append("- Earned proposal credits denied ")
                    .append(format(credits.accessDenied()))
                    .append(" of potential proposals, changed welfare by ")
                    .append(format(credits.welfare() - openDefault.welfare()))
                    .append(", and changed proposer gain by ")
                    .append(format(credits.proposerGain() - openDefault.proposerGain()))
                    .append(" relative to open default-pass.\n");
        }
        if (antiCaptureBundle != null) {
            builder.append("- The anti-capture bundle changed lobby capture by ")
                    .append(format(antiCaptureBundle.lobbyCapture() - openDefault.lobbyCapture()))
                    .append(", anti-lobbying reform passage by ")
                    .append(format(antiCaptureBundle.antiLobbyingSuccess() - openDefault.antiLobbyingSuccess()))
                    .append(", and private-gain ratio by ")
                    .append(format(antiCaptureBundle.privateGainRatio() - openDefault.privateGainRatio()))
                    .append(" relative to open default-pass.\n");
        }
        if (budgetedLobbying != null) {
            builder.append("- Budgeted lobbying spent ")
                    .append(format(budgetedLobbying.lobbySpendPerBill()))
                    .append(" per potential bill, with ")
                    .append(format(budgetedLobbying.defensiveLobbyingShare()))
                    .append(" of spend aimed defensively at anti-lobbying reform bills.\n");
        }
        if (channelBundle != null && budgetedLobbying != null) {
            builder.append("- The channel anti-capture bundle changed public benefit per lobby dollar by ")
                    .append(format(channelBundle.publicBenefitPerLobbyDollar() - budgetedLobbying.publicBenefitPerLobbyDollar()))
                    .append(" and anti-lobbying reform passage by ")
                    .append(format(channelBundle.antiLobbyingSuccess() - budgetedLobbying.antiLobbyingSuccess()))
                    .append(" relative to budgeted lobbying.\n");
        }
        if (citizenCertificate != null) {
            builder.append("- Citizen certificate review certified ")
                    .append(format(citizenCertificate.citizenCertificationRate()))
                    .append(" of reviewed bills, changed low-support passage by ")
                    .append(format(citizenCertificate.lowSupport() - openDefault.lowSupport()))
                    .append(", and changed legitimacy by ")
                    .append(format(citizenCertificate.legitimacy() - openDefault.legitimacy()))
                    .append(" relative to open default-pass.\n");
        }
        if (weightedLottery != null) {
            builder.append("- Weighted agenda lotteries changed floor consideration by ")
                    .append(format(weightedLottery.floor() - openDefault.floor()))
                    .append(", productivity by ")
                    .append(format(weightedLottery.productivity() - openDefault.productivity()))
                    .append(", and welfare by ")
                    .append(format(weightedLottery.welfare() - openDefault.welfare()))
                    .append(" relative to open default-pass.\n");
        }
        if (quadraticAttention != null) {
            builder.append("- Quadratic attention budgets spent ")
                    .append(format(quadraticAttention.attentionSpendPerBill()))
                    .append(" credits per potential bill and changed low-support passage by ")
                    .append(format(quadraticAttention.lowSupport() - openDefault.lowSupport()))
                    .append(" relative to open default-pass.\n");
        }
        if (publicObjection != null) {
            builder.append("- Public objection windows triggered on ")
                    .append(format(publicObjection.objectionWindowRate()))
                    .append(" of potential bills and changed low-support passage by ")
                    .append(format(publicObjection.lowSupport() - openDefault.lowSupport()))
                    .append(" relative to open default-pass.\n");
        }
        if (repealWindow != null) {
            builder.append("- Public repeal windows triggered on ")
                    .append(format(repealWindow.objectionWindowRate()))
                    .append(" of potential bills; triggered windows reversed ")
                    .append(format(repealWindow.repealWindowReversalRate()))
                    .append(" of those enactments.\n");
        }
        if (pairwiseAlternatives != null) {
            builder.append("- Pairwise policy tournaments changed proposer agenda advantage by ")
                    .append(format(pairwiseAlternatives.proposerAgendaAdvantage() - openDefault.proposerAgendaAdvantage()))
                    .append(", policy shift by ")
                    .append(format(pairwiseAlternatives.policyShift() - openDefault.policyShift()))
                    .append(", and status-quo wins averaged ")
                    .append(format(pairwiseAlternatives.statusQuoWinRate()))
                    .append(" relative to open default-pass.\n");
        }
        ScenarioAggregate mediation = aggregateByScenario.get("default-pass-mediation");
        if (mediation != null) {
            builder.append("- Mediated default-pass amended ")
                    .append(format(mediation.amendmentRate()))
                    .append(" of potential bills and changed compromise by ")
                    .append(format(mediation.compromise() - openDefault.compromise()))
                    .append(" relative to open default-pass.\n");
        }
        builder.append("- Highest average welfare in this campaign came from ")
                .append(bestWelfare.scenarioName())
                .append(" at ")
                .append(format(bestWelfare.welfare()))
                .append(".\n\n");
    }

    private static void appendMediationDelta(
            StringBuilder builder,
            Map<String, ScenarioAggregate> aggregateByScenario,
            String mediatedKey,
            String baselineKey
    ) {
        ScenarioAggregate mediated = aggregateByScenario.get(mediatedKey);
        ScenarioAggregate baseline = aggregateByScenario.get(baselineKey);
        if (mediated == null || baseline == null) {
            return;
        }
        builder.append("| ")
                .append(mediated.scenarioName()).append(" | ")
                .append(baseline.scenarioName()).append(" | ")
                .append(format(mediated.productivity() - baseline.productivity())).append(" | ")
                .append(format(mediated.welfare() - baseline.welfare())).append(" | ")
                .append(format(mediated.compromise() - baseline.compromise())).append(" | ")
                .append(format(mediated.lowSupport() - baseline.lowSupport())).append(" | ")
                .append(format(mediated.policyShift() - baseline.policyShift())).append(" | ")
                .append(format(mediated.proposerGain() - baseline.proposerGain())).append(" | ")
                .append(format(mediated.amendmentRate())).append(" | ")
                .append(format(mediated.amendmentMovement())).append(" |\n");
    }

    private static Map<String, ScenarioAggregate> aggregateByScenario(List<CampaignRow> rows, int runs) {
        Map<String, ScenarioAggregate> byScenario = new LinkedHashMap<>();
        for (CampaignRow row : rows) {
            byScenario.computeIfAbsent(
                    row.scenarioKey(),
                    key -> new ScenarioAggregate(key, row.report().scenarioName())
            ).add(row.report(), runs, row.caseWeight());
        }
        return byScenario;
    }

    private static boolean hasWeightedCases(List<CampaignRow> rows) {
        for (CampaignRow row : rows) {
            if (Math.abs(row.caseWeight() - 1.0) > 0.000_001) {
                return true;
            }
        }
        return false;
    }

    private static boolean hasTimelineCases(List<CampaignRow> rows) {
        for (CampaignRow row : rows) {
            if (row.caseKey().startsWith("era-")) {
                return true;
            }
        }
        return false;
    }

    private static List<CampaignRow> firstRowsByCase(List<CampaignRow> rows) {
        Map<String, CampaignRow> byCase = new LinkedHashMap<>();
        for (CampaignRow row : rows) {
            byCase.putIfAbsent(row.caseKey(), row);
        }
        return new ArrayList<>(byCase.values());
    }

    private static int caseCount(List<CampaignRow> rows) {
        return caseKeys(rows).size();
    }

    private static List<String> caseKeys(List<CampaignRow> rows) {
        List<String> keys = new ArrayList<>();
        for (CampaignRow row : rows) {
            if (!keys.contains(row.caseKey())) {
                keys.add(row.caseKey());
            }
        }
        return keys;
    }

    private static CampaignRow find(List<CampaignRow> rows, String caseKey, String scenarioKey) {
        for (CampaignRow row : rows) {
            if (row.caseKey().equals(caseKey) && row.scenarioKey().equals(scenarioKey)) {
                return row;
            }
        }
        return null;
    }

    private static List<CampaignRow> rowsForCase(List<CampaignRow> rows, String caseKey) {
        List<CampaignRow> caseRows = new ArrayList<>();
        for (CampaignRow row : rows) {
            if (row.caseKey().equals(caseKey)) {
                caseRows.add(row);
            }
        }
        return caseRows;
    }

    private static CampaignRow max(List<CampaignRow> rows, Comparator<CampaignRow> comparator) {
        return rows.stream().max(comparator).orElseThrow();
    }

    private static CampaignRow min(List<CampaignRow> rows, Comparator<CampaignRow> comparator) {
        return rows.stream().min(comparator).orElseThrow();
    }

    private static double enactedPerRun(CampaignRow row, int runs) {
        return (double) row.report().enactedBills() / runs;
    }

    private static double floorPerRun(CampaignRow row, int runs) {
        return (row.report().totalBills() * row.report().floorConsiderationRate()) / runs;
    }

    private static double contentionIndex(ScenarioReport report) {
        return (0.50 * report.gridlockRate())
                + (0.30 * (1.0 - report.compromiseScore()))
                + (0.20 * report.weakPublicMandatePassageRate());
    }

    private static String csvValue(String value) {
        if (value.contains(",") || value.contains("\"") || value.contains("\n")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }

    private static String format(double value) {
        return String.format(Locale.ROOT, "%.3f", value);
    }

    private record ExperimentCase(String key, String name, String description, double caseWeight, WorldSpec worldSpec) {
    }

    private static final class ScenarioAggregate {
        private final String scenarioKey;
        private final String scenarioName;
        private double weightTotal;
        private double productivity;
        private double avgSupport;
        private double welfare;
        private double compromise;
        private double lowSupport;
        private double weakPublicMandatePassage;
        private double policyShift;
        private double proposerGain;
        private double lobbyCapture;
        private double publicAlignment;
        private double antiLobbyingSuccess;
        private double privateGainRatio;
        private double lobbySpendPerBill;
        private double defensiveLobbyingShare;
        private double captureReturnOnSpend;
        private double publicPreferenceDistortion;
        private double administrativeCost;
        private double amendmentRate;
        private double amendmentMovement;
        private double minorityHarm;
        private double concentratedHarmPassage;
        private double compensationRate;
        private double legitimacy;
        private double activeLawWelfare;
        private double reversalRate;
        private double timeToCorrectBadLaw;
        private double lowSupportActiveLawShare;
        private double selectedAlternativeMedianDistance;
        private double proposerAgendaAdvantage;
        private double alternativeDiversity;
        private double statusQuoWinRate;
        private double publicBenefitPerLobbyDollar;
        private double directLobbySpendShare;
        private double agendaLobbySpendShare;
        private double informationLobbySpendShare;
        private double publicCampaignSpendShare;
        private double litigationThreatSpendShare;
        private double citizenReviewRate;
        private double citizenCertificationRate;
        private double citizenLegitimacy;
        private double attentionSpendPerBill;
        private double objectionWindowRate;
        private double repealWindowReversalRate;
        private double fastLaneRate;
        private double middleLaneRate;
        private double highRiskLaneRate;
        private double challengeExhaustionRate;
        private double falseNegativePassRate;
        private double publicWillReviewRate;
        private double publicSignalMovement;
        private double districtAlignment;
        private double crossBlocAdmissionRate;
        private double affectedGroupSponsorshipRate;
        private double averageCosponsors;
        private double proposalBondForfeiture;
        private double strategicDecoyRate;
        private double proposerAccessGini;
        private double welfarePerSubmittedBill;
        private double challengeRate;
        private double floor;
        private double accessDenied;
        private double committeeRejected;
        private double enactedPerRun;
        private double floorPerRun;

        private ScenarioAggregate(String scenarioKey, String scenarioName) {
            this.scenarioKey = scenarioKey;
            this.scenarioName = scenarioName;
        }

        private void add(ScenarioReport report, int runs, double weight) {
            weightTotal += weight;
            productivity += report.productivity() * weight;
            avgSupport += report.averageEnactedSupport() * weight;
            welfare += report.averagePublicBenefit() * weight;
            compromise += report.compromiseScore() * weight;
            lowSupport += report.controversialPassageRate() * weight;
            weakPublicMandatePassage += report.weakPublicMandatePassageRate() * weight;
            policyShift += report.averagePolicyShift() * weight;
            proposerGain += report.averageProposerGain() * weight;
            lobbyCapture += report.lobbyCaptureIndex() * weight;
            publicAlignment += report.publicAlignmentScore() * weight;
            antiLobbyingSuccess += report.antiLobbyingSuccessRate() * weight;
            privateGainRatio += report.privateGainRatio() * weight;
            lobbySpendPerBill += report.lobbySpendPerBill() * weight;
            defensiveLobbyingShare += report.defensiveLobbyingShare() * weight;
            captureReturnOnSpend += report.captureReturnOnSpend() * weight;
            publicPreferenceDistortion += report.publicPreferenceDistortion() * weight;
            administrativeCost += report.administrativeCostIndex() * weight;
            amendmentRate += report.amendmentRate() * weight;
            amendmentMovement += report.averageAmendmentMovement() * weight;
            minorityHarm += report.minorityHarmIndex() * weight;
            concentratedHarmPassage += report.concentratedHarmPassageRate() * weight;
            compensationRate += report.compensationRate() * weight;
            legitimacy += report.legitimacyScore() * weight;
            activeLawWelfare += report.activeLawWelfare() * weight;
            reversalRate += report.reversalRate() * weight;
            timeToCorrectBadLaw += report.timeToCorrectBadLaw() * weight;
            lowSupportActiveLawShare += report.lowSupportActiveLawShare() * weight;
            selectedAlternativeMedianDistance += report.selectedAlternativeMedianDistance() * weight;
            proposerAgendaAdvantage += report.proposerAgendaAdvantage() * weight;
            alternativeDiversity += report.alternativeDiversity() * weight;
            statusQuoWinRate += report.statusQuoWinRate() * weight;
            publicBenefitPerLobbyDollar += report.publicBenefitPerLobbyDollar() * weight;
            directLobbySpendShare += report.directLobbySpendShare() * weight;
            agendaLobbySpendShare += report.agendaLobbySpendShare() * weight;
            informationLobbySpendShare += report.informationLobbySpendShare() * weight;
            publicCampaignSpendShare += report.publicCampaignSpendShare() * weight;
            litigationThreatSpendShare += report.litigationThreatSpendShare() * weight;
            citizenReviewRate += report.citizenReviewRate() * weight;
            citizenCertificationRate += report.citizenCertificationRate() * weight;
            citizenLegitimacy += report.citizenLegitimacy() * weight;
            attentionSpendPerBill += report.attentionSpendPerBill() * weight;
            objectionWindowRate += report.objectionWindowRate() * weight;
            repealWindowReversalRate += report.repealWindowReversalRate() * weight;
            fastLaneRate += report.fastLaneRate() * weight;
            middleLaneRate += report.middleLaneRate() * weight;
            highRiskLaneRate += report.highRiskLaneRate() * weight;
            challengeExhaustionRate += report.challengeExhaustionRate() * weight;
            falseNegativePassRate += report.falseNegativePassRate() * weight;
            publicWillReviewRate += report.publicWillReviewRate() * weight;
            publicSignalMovement += report.publicSignalMovement() * weight;
            districtAlignment += report.districtAlignment() * weight;
            crossBlocAdmissionRate += report.crossBlocAdmissionRate() * weight;
            affectedGroupSponsorshipRate += report.affectedGroupSponsorshipRate() * weight;
            averageCosponsors += report.averageCosponsors() * weight;
            proposalBondForfeiture += report.proposalBondForfeiture() * weight;
            strategicDecoyRate += report.strategicDecoyRate() * weight;
            proposerAccessGini += report.proposerAccessGini() * weight;
            welfarePerSubmittedBill += report.welfarePerSubmittedBill() * weight;
            challengeRate += report.challengeRate() * weight;
            floor += report.floorConsiderationRate() * weight;
            accessDenied += report.accessDenialRate() * weight;
            committeeRejected += report.committeeRejectionRate() * weight;
            enactedPerRun += ((double) report.enactedBills() / runs) * weight;
            floorPerRun += ((report.totalBills() * report.floorConsiderationRate()) / runs) * weight;
        }

        private String scenarioKey() {
            return scenarioKey;
        }

        private String scenarioName() {
            return scenarioName;
        }

        private double productivity() {
            return productivity / weightTotal;
        }

        private double representativeQuality() {
            return MetricDefinition.average(
                    welfare(),
                    avgSupport(),
                    compromise(),
                    publicAlignment(),
                    legitimacy()
            );
        }

        private double riskControl() {
            return MetricDefinition.average(
                    MetricDefinition.lowerIsBetter(lowSupport()),
                    MetricDefinition.lowerIsBetter(weakPublicMandatePassage()),
                    MetricDefinition.lowerIsBetter(minorityHarm()),
                    MetricDefinition.lowerIsBetter(lobbyCapture()),
                    MetricDefinition.lowerIsBetter(publicPreferenceDistortion()),
                    MetricDefinition.lowerIsBetter(concentratedHarmPassage()),
                    MetricDefinition.lowerIsBetter(proposerGain(), 2.0),
                    MetricDefinition.lowerIsBetter(policyShift(), 2.0)
            );
        }

        private double administrativeFeasibility() {
            return MetricDefinition.lowerIsBetter(administrativeCost());
        }

        private double directionalScore() {
            return MetricDefinition.average(
                    productivity(),
                    representativeQuality(),
                    riskControl(),
                    administrativeFeasibility()
            );
        }

        private double welfare() {
            return welfare / weightTotal;
        }

        private double avgSupport() {
            return avgSupport / weightTotal;
        }

        private double lowSupport() {
            return lowSupport / weightTotal;
        }

        private double weakPublicMandatePassage() {
            return weakPublicMandatePassage / weightTotal;
        }

        private double policyShift() {
            return policyShift / weightTotal;
        }

        private double proposerGain() {
            return proposerGain / weightTotal;
        }

        private double lobbyCapture() {
            return lobbyCapture / weightTotal;
        }

        private double publicAlignment() {
            return publicAlignment / weightTotal;
        }

        private double antiLobbyingSuccess() {
            return antiLobbyingSuccess / weightTotal;
        }

        private double privateGainRatio() {
            return privateGainRatio / weightTotal;
        }

        private double compromise() {
            return compromise / weightTotal;
        }

        private double lobbySpendPerBill() {
            return lobbySpendPerBill / weightTotal;
        }

        private double defensiveLobbyingShare() {
            return defensiveLobbyingShare / weightTotal;
        }

        private double captureReturnOnSpend() {
            return captureReturnOnSpend / weightTotal;
        }

        private double publicPreferenceDistortion() {
            return publicPreferenceDistortion / weightTotal;
        }

        private double administrativeCost() {
            return administrativeCost / weightTotal;
        }

        private double amendmentRate() {
            return amendmentRate / weightTotal;
        }

        private double amendmentMovement() {
            return amendmentMovement / weightTotal;
        }

        private double minorityHarm() {
            return minorityHarm / weightTotal;
        }

        private double concentratedHarmPassage() {
            return concentratedHarmPassage / weightTotal;
        }

        private double compensationRate() {
            return compensationRate / weightTotal;
        }

        private double legitimacy() {
            return legitimacy / weightTotal;
        }

        private double activeLawWelfare() {
            return activeLawWelfare / weightTotal;
        }

        private double reversalRate() {
            return reversalRate / weightTotal;
        }

        private double timeToCorrectBadLaw() {
            return timeToCorrectBadLaw / weightTotal;
        }

        private double lowSupportActiveLawShare() {
            return lowSupportActiveLawShare / weightTotal;
        }

        private double selectedAlternativeMedianDistance() {
            return selectedAlternativeMedianDistance / weightTotal;
        }

        private double proposerAgendaAdvantage() {
            return proposerAgendaAdvantage / weightTotal;
        }

        private double alternativeDiversity() {
            return alternativeDiversity / weightTotal;
        }

        private double statusQuoWinRate() {
            return statusQuoWinRate / weightTotal;
        }

        private double publicBenefitPerLobbyDollar() {
            return publicBenefitPerLobbyDollar / weightTotal;
        }

        private double directLobbySpendShare() {
            return directLobbySpendShare / weightTotal;
        }

        private double agendaLobbySpendShare() {
            return agendaLobbySpendShare / weightTotal;
        }

        private double informationLobbySpendShare() {
            return informationLobbySpendShare / weightTotal;
        }

        private double publicCampaignSpendShare() {
            return publicCampaignSpendShare / weightTotal;
        }

        private double litigationThreatSpendShare() {
            return litigationThreatSpendShare / weightTotal;
        }

        private double citizenReviewRate() {
            return citizenReviewRate / weightTotal;
        }

        private double citizenCertificationRate() {
            return citizenCertificationRate / weightTotal;
        }

        private double citizenLegitimacy() {
            return citizenLegitimacy / weightTotal;
        }

        private double attentionSpendPerBill() {
            return attentionSpendPerBill / weightTotal;
        }

        private double objectionWindowRate() {
            return objectionWindowRate / weightTotal;
        }

        private double repealWindowReversalRate() {
            return repealWindowReversalRate / weightTotal;
        }

        private double fastLaneRate() {
            return fastLaneRate / weightTotal;
        }

        private double middleLaneRate() {
            return middleLaneRate / weightTotal;
        }

        private double highRiskLaneRate() {
            return highRiskLaneRate / weightTotal;
        }

        private double challengeExhaustionRate() {
            return challengeExhaustionRate / weightTotal;
        }

        private double falseNegativePassRate() {
            return falseNegativePassRate / weightTotal;
        }

        private double publicWillReviewRate() {
            return publicWillReviewRate / weightTotal;
        }

        private double publicSignalMovement() {
            return publicSignalMovement / weightTotal;
        }

        private double districtAlignment() {
            return districtAlignment / weightTotal;
        }

        private double crossBlocAdmissionRate() {
            return crossBlocAdmissionRate / weightTotal;
        }

        private double affectedGroupSponsorshipRate() {
            return affectedGroupSponsorshipRate / weightTotal;
        }

        private double averageCosponsors() {
            return averageCosponsors / weightTotal;
        }

        private double proposalBondForfeiture() {
            return proposalBondForfeiture / weightTotal;
        }

        private double strategicDecoyRate() {
            return strategicDecoyRate / weightTotal;
        }

        private double proposerAccessGini() {
            return proposerAccessGini / weightTotal;
        }

        private double welfarePerSubmittedBill() {
            return welfarePerSubmittedBill / weightTotal;
        }

        private double challengeRate() {
            return challengeRate / weightTotal;
        }

        private double floor() {
            return floor / weightTotal;
        }

        private double accessDenied() {
            return accessDenied / weightTotal;
        }

        private double committeeRejected() {
            return committeeRejected / weightTotal;
        }

        private double enactedPerRun() {
            return enactedPerRun / weightTotal;
        }

        private double floorPerRun() {
            return floorPerRun / weightTotal;
        }
    }
}
