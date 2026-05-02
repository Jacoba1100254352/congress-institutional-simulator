package congresssim.simulation;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public record MetricDefinition(
        String key,
        String label,
        MetricDirection direction,
        String note
) {
    private static final List<MetricDefinition> DEFINITIONS = List.of(
            new MetricDefinition("productivity", "Productivity", MetricDirection.HIGHER_IS_BETTER, "Share of potential bills enacted."),
            new MetricDefinition("avgSupport", "Average enacted support", MetricDirection.HIGHER_IS_BETTER, "Average yes share among enacted bills."),
            new MetricDefinition("welfare", "Generated welfare", MetricDirection.HIGHER_IS_BETTER, "Average generated public-benefit score for enacted bills."),
            new MetricDefinition("cooperation", "Cooperation", MetricDirection.HIGHER_IS_BETTER, "Throughput weighted by enacted support."),
            new MetricDefinition("compromise", "Compromise", MetricDirection.HIGHER_IS_BETTER, "Moderation, support, and distance from proposer advantage."),
            new MetricDefinition("publicAlignment", "Public alignment", MetricDirection.HIGHER_IS_BETTER, "How closely enacted support tracks generated public support."),
            new MetricDefinition("legitimacy", "Legitimacy", MetricDirection.HIGHER_IS_BETTER, "Public, chamber, and affected-group support net of harm."),
            new MetricDefinition("antiLobbyingSuccess", "Anti-lobbying success", MetricDirection.HIGHER_IS_BETTER, "Share of generated anti-lobbying reforms enacted."),
            new MetricDefinition("citizenCertificationRate", "Citizen certification", MetricDirection.HIGHER_IS_BETTER, "Share of reviewed bills certified by a citizen panel."),
            new MetricDefinition("districtAlignment", "District alignment", MetricDirection.HIGHER_IS_BETTER, "Alignment between district/public signals and final action."),
            new MetricDefinition("welfarePerSubmittedBill", "Welfare per submitted bill", MetricDirection.HIGHER_IS_BETTER, "Public-benefit yield per proposal opportunity."),
            new MetricDefinition("publicBenefitPerLobbyDollar", "Public benefit per lobby dollar", MetricDirection.HIGHER_IS_BETTER, "Generated benefit per unit of explicit lobby spend."),
            new MetricDefinition("gridlock", "Gridlock", MetricDirection.LOWER_IS_BETTER, "Share of introduced bills that fail."),
            new MetricDefinition("lowSupport", "Low-support passage", MetricDirection.LOWER_IS_BETTER, "Enacted bills with less than majority yes support."),
            new MetricDefinition("weakPublicMandatePassage", "Weak public-mandate passage", MetricDirection.LOWER_IS_BETTER, "Enacted bills with generated public support below majority."),
            new MetricDefinition("popularFail", "Popular failure", MetricDirection.LOWER_IS_BETTER, "High-public-support bills that fail."),
            new MetricDefinition("lobbyCapture", "Lobby capture", MetricDirection.LOWER_IS_BETTER, "Capture risk from lobby pressure, private gain, and weak public value."),
            new MetricDefinition("publicPreferenceDistortion", "Public-preference distortion", MetricDirection.LOWER_IS_BETTER, "Gap between enacted yes share and generated public support."),
            new MetricDefinition("minorityHarm", "Minority harm", MetricDirection.LOWER_IS_BETTER, "Concentrated harm weighted by affected-group opposition."),
            new MetricDefinition("concentratedHarmPassage", "Concentrated-harm passage", MetricDirection.LOWER_IS_BETTER, "High-harm bills enacted."),
            new MetricDefinition("proposerGain", "Proposer gain", MetricDirection.LOWER_IS_BETTER, "Movement toward proposer ideal, normalized for directional scores."),
            new MetricDefinition("lowSupportActiveLawShare", "Low-support active-law share", MetricDirection.LOWER_IS_BETTER, "Persistent enacted law stock with weak support."),
            new MetricDefinition("falseNegativePassRate", "False-negative default passage", MetricDirection.LOWER_IS_BETTER, "Risky default enactments that passed unchallenged."),
            new MetricDefinition("privateGainRatio", "Private-gain ratio", MetricDirection.LOWER_IS_BETTER, "Private gain relative to generated public benefit."),
            new MetricDefinition("captureReturnOnSpend", "Capture return on spend", MetricDirection.LOWER_IS_BETTER, "Capture risk per unit of explicit lobby spend."),
            new MetricDefinition("administrativeCost", "Administrative cost", MetricDirection.LOWER_IS_BETTER, "Estimated procedural load from attention spending, review, challenge, amendment, and alternative selection."),
            new MetricDefinition("floor", "Floor consideration", MetricDirection.DIAGNOSTIC, "Institutional load and access, not inherently good or bad."),
            new MetricDefinition("accessDenied", "Access denied", MetricDirection.DIAGNOSTIC, "Proposal-screening intensity."),
            new MetricDefinition("committeeRejected", "Committee rejected", MetricDirection.DIAGNOSTIC, "Committee gatekeeping intensity."),
            new MetricDefinition("challengeRate", "Challenge rate", MetricDirection.DIAGNOSTIC, "Contestation activity."),
            new MetricDefinition("amendmentRate", "Amendment rate", MetricDirection.DIAGNOSTIC, "Revision activity."),
            new MetricDefinition("compensationRate", "Compensation rate", MetricDirection.DIAGNOSTIC, "Affected-group compensation activity."),
            new MetricDefinition("reversalRate", "Reversal rate", MetricDirection.DIAGNOSTIC, "Correction activity, but also possible instability."),
            new MetricDefinition("attentionSpendPerBill", "Attention spend per bill", MetricDirection.DIAGNOSTIC, "Scarce attention use."),
            new MetricDefinition("objectionWindowRate", "Objection-window rate", MetricDirection.DIAGNOSTIC, "Public contestation activity."),
            new MetricDefinition("policyShift", "Policy shift", MetricDirection.DIAGNOSTIC, "Substantive movement; risky when uncontrolled, useful when reform is needed."),
            new MetricDefinition("interChamberConflictRate", "Inter-chamber conflict", MetricDirection.DIAGNOSTIC, "How often the first two chamber votes disagree."),
            new MetricDefinition("secondChamberKillRate", "Second-chamber kill", MetricDirection.DIAGNOSTIC, "How often the first chamber passes and the second chamber blocks."),
            new MetricDefinition("conferenceRate", "Conference rate", MetricDirection.DIAGNOSTIC, "Share of bills receiving a conference or mediation-style final report."),
            new MetricDefinition("conferenceSuccessRate", "Conference success", MetricDirection.DIAGNOSTIC, "Share of conference attempts that enact a final report."),
            new MetricDefinition("routingDelayCost", "Routing delay cost", MetricDirection.LOWER_IS_BETTER, "Estimated procedural delay from bicameral routing and disagreement resolution."),
            new MetricDefinition("shuttleRoundsToAgreement", "Shuttle rounds", MetricDirection.DIAGNOSTIC, "Average shuttle/navette rounds among successful agreements."),
            new MetricDefinition("suspensiveOverrideRate", "Suspensive override", MetricDirection.DIAGNOSTIC, "Share of bicameral bills where a suspensive veto is overridden."),
            new MetricDefinition("bicameralDeadlockRate", "Bicameral deadlock", MetricDirection.LOWER_IS_BETTER, "Share of bicameral bills ending in unresolved chamber conflict."),
            new MetricDefinition("dischargePetitionRate", "Discharge petition", MetricDirection.DIAGNOSTIC, "Share of committee-power reviews that bypass committee burial."),
            new MetricDefinition("committeeOverrideRate", "Committee override", MetricDirection.DIAGNOSTIC, "Share of committee burials or near-burials that are overridden."),
            new MetricDefinition("committeeHearingRate", "Committee hearing", MetricDirection.DIAGNOSTIC, "Share of committee-power reviews with minority or affected-group hearing rights."),
            new MetricDefinition("committeeQueueDelay", "Committee queue delay", MetricDirection.LOWER_IS_BETTER, "Estimated delay from committee queue power."),
            new MetricDefinition("committeeAmendmentValueAdded", "Committee amendment value", MetricDirection.HIGHER_IS_BETTER, "Estimated support and harm-reduction value added by committee amendments."),
            new MetricDefinition("populationSeatDistortion", "Population-seat distortion", MetricDirection.LOWER_IS_BETTER, "Mismatch between population share and seat share."),
            new MetricDefinition("democraticResponsiveness", "Democratic responsiveness", MetricDirection.HIGHER_IS_BETTER, "Elected share, low malapportionment, and proportional representation proxy."),
            new MetricDefinition("seatVoteDistortion", "Seat-vote distortion", MetricDirection.LOWER_IS_BETTER, "Party-share gap between chamber seats and generated electorate."),
            new MetricDefinition("constituencyServiceConcentration", "Constituency-service concentration", MetricDirection.DIAGNOSTIC, "How strongly representation is concentrated in small districts."),
            new MetricDefinition("regionalTransferBias", "Regional transfer bias", MetricDirection.DIAGNOSTIC, "Overrepresentation of lower-population territorial units."),
            new MetricDefinition("malapportionmentIndex", "Malapportionment index", MetricDirection.LOWER_IS_BETTER, "Average chamber-level population malapportionment."),
            new MetricDefinition("smallConstituencyVetoRate", "Small-constituency veto", MetricDirection.LOWER_IS_BETTER, "Bills blocked by a smaller or more territorial second chamber."),
            new MetricDefinition("populationSupportedButBlockedRate", "Population-supported block", MetricDirection.LOWER_IS_BETTER, "Bills with generated public support that are blocked by chamber conflict."),
            new MetricDefinition("firstMoverWinRate", "First-mover win", MetricDirection.DIAGNOSTIC, "How often originating-chamber passage survives final resolution."),
            new MetricDefinition("amendmentSurvivalRate", "Amendment survival", MetricDirection.DIAGNOSTIC, "How often revised bills enact after disagreement handling."),
            new MetricDefinition("mediatorAddedTextShare", "Mediator-added text", MetricDirection.DIAGNOSTIC, "Proxy for the amount of mediated text added during chamber conflict."),
            new MetricDefinition("upperHouseAmendmentRetentionRate", "Upper amendment retention", MetricDirection.DIAGNOSTIC, "Share of upper-house revisions retained in final passage."),
            new MetricDefinition("suspensiveDelayUseRate", "Suspensive delay use", MetricDirection.DIAGNOSTIC, "Use of suspensive-delay disagreement handling."),
            new MetricDefinition("committeeAgendaConcentration", "Committee agenda concentration", MetricDirection.LOWER_IS_BETTER, "Party concentration in committee agenda control."),
            new MetricDefinition("committeeCaptureIndex", "Committee capture", MetricDirection.LOWER_IS_BETTER, "Lobby and private-gain exposure inside committee review."),
            new MetricDefinition("committeeExpertiseScore", "Committee expertise", MetricDirection.HIGHER_IS_BETTER, "Expertise and independence proxy for committee membership."),
            new MetricDefinition("minorityCommitteeAccessRate", "Minority committee access", MetricDirection.HIGHER_IS_BETTER, "Minority or affected-group access to committee review."),
            new MetricDefinition("committeeFalsePositiveRate", "Committee false positive", MetricDirection.LOWER_IS_BETTER, "High-value bills blocked by committee review."),
            new MetricDefinition("committeeFalseNegativeRate", "Committee false negative", MetricDirection.LOWER_IS_BETTER, "Low-value or captured bills advanced by committee review."),
            new MetricDefinition("reportedBillSponsorDiversity", "Reported sponsor diversity", MetricDirection.HIGHER_IS_BETTER, "Sponsor diversity among bills advanced by committee review."),
            new MetricDefinition("oppositionAmendmentSuccessRate", "Opposition amendment success", MetricDirection.HIGHER_IS_BETTER, "Opposition or minority amendments that improve bills."),
            new MetricDefinition("hearingDiversity", "Hearing diversity", MetricDirection.HIGHER_IS_BETTER, "Diversity proxy for public or minority hearings."),
            new MetricDefinition("auditFollowThroughRate", "Audit follow-through", MetricDirection.HIGHER_IS_BETTER, "Audit/scrutiny committees acting on high-risk bills."),
            new MetricDefinition("scandalDetectionRate", "Scandal detection", MetricDirection.HIGHER_IS_BETTER, "Detection proxy for high-capture or high-private-gain bills."),
            new MetricDefinition("appointmentCaptureRisk", "Appointment capture risk", MetricDirection.LOWER_IS_BETTER, "Capture risk under appointed or mixed-selection members."),
            new MetricDefinition("eligibilityExclusionRate", "Eligibility exclusion", MetricDirection.DIAGNOSTIC, "Share of candidate pool excluded by eligibility rules."),
            new MetricDefinition("expertiseRepresentationGap", "Expertise representation gap", MetricDirection.LOWER_IS_BETTER, "Gap between expertise gains and constituency accountability."),
            new MetricDefinition("constituencyAccountability", "Constituency accountability", MetricDirection.HIGHER_IS_BETTER, "Constituency sensitivity and elected-member share."),
            new MetricDefinition("selectorCaptureIndex", "Selector capture", MetricDirection.LOWER_IS_BETTER, "Capture exposure from selector body and appointment mode."),
            new MetricDefinition("legislatorExperienceStock", "Experience stock", MetricDirection.HIGHER_IS_BETTER, "Institutional memory from terms, renewal, and retention."),
            new MetricDefinition("electoralResponsiveness", "Electoral responsiveness", MetricDirection.HIGHER_IS_BETTER, "Responsiveness retained after selection and eligibility filters."),
            new MetricDefinition("turnoverOutsideInfluenceShift", "Turnover influence shift", MetricDirection.LOWER_IS_BETTER, "Outside-influence risk from turnover or thin candidate pools."),
            new MetricDefinition("candidatePoolDiversity", "Candidate-pool diversity", MetricDirection.HIGHER_IS_BETTER, "Ideological and party diversity after eligibility filters."),
            new MetricDefinition("contestedSeatRate", "Contested seat rate", MetricDirection.HIGHER_IS_BETTER, "Proxy for contested availability after eligibility filters."),
            new MetricDefinition("vacancyRate", "Vacancy rate", MetricDirection.LOWER_IS_BETTER, "Unfilled seats caused by restrictive eligibility filters."),
            new MetricDefinition("renewalStaggeringIndex", "Renewal staggering", MetricDirection.DIAGNOSTIC, "Calendar dispersion across renewal cohorts."),
            new MetricDefinition("nearTermRenewalShare", "Near-term renewal share", MetricDirection.DIAGNOSTIC, "Members facing renewal within the next two modeled rounds."),
            new MetricDefinition("recusalRate", "Recusal rate", MetricDirection.DIAGNOSTIC, "Participation removed by conflict or sector-specific recusal."),
            new MetricDefinition("conflictDisclosureRate", "Conflict disclosure", MetricDirection.HIGHER_IS_BETTER, "Share of recusal/conflict risk made visible."),
            new MetricDefinition("revolvingDoorTransitionRate", "Revolving-door transition", MetricDirection.LOWER_IS_BETTER, "Immediate post-office influence transition proxy."),
            new MetricDefinition("sponsorIndustryAlignment", "Sponsor-industry alignment", MetricDirection.LOWER_IS_BETTER, "Alignment between sponsor incentives and sector-specific bills."),
            new MetricDefinition("exAnteReviewRate", "Ex ante review", MetricDirection.DIAGNOSTIC, "Share of bills receiving pre-enactment legal/institutional review."),
            new MetricDefinition("reviewDelay", "Review delay", MetricDirection.LOWER_IS_BETTER, "Delay from ex ante review or independent institutions."),
            new MetricDefinition("exPostInvalidationRate", "Ex post invalidation", MetricDirection.LOWER_IS_BETTER, "Residual rights/legal reversals after pre-enactment review."),
            new MetricDefinition("draftingErrorRate", "Drafting error", MetricDirection.LOWER_IS_BETTER, "Legal or technical drafting risk after review."),
            new MetricDefinition("referralPartisanSkew", "Referral partisan skew", MetricDirection.LOWER_IS_BETTER, "Partisan skew in optional review referrals."),
            new MetricDefinition("forecastError", "Forecast error", MetricDirection.LOWER_IS_BETTER, "Public-benefit or fiscal forecast error proxy."),
            new MetricDefinition("publicationCompliance", "Publication compliance", MetricDirection.HIGHER_IS_BETTER, "Transparency compliance by review institutions."),
            new MetricDefinition("informationRequestFulfillment", "Information fulfillment", MetricDirection.HIGHER_IS_BETTER, "Independent institution access to required information."),
            new MetricDefinition("institutionOverrideFrequency", "Institution override", MetricDirection.DIAGNOSTIC, "How often legislative override defeats institutional objections."),
            new MetricDefinition("oppositionTrustProxy", "Opposition trust", MetricDirection.HIGHER_IS_BETTER, "Opposition trust proxy from transparency and independence."),
            new MetricDefinition("independenceInsulationScore", "Independence insulation", MetricDirection.HIGHER_IS_BETTER, "Institutional insulation from appointment, funding, and removal pressure."),
            new MetricDefinition("quietCaptureRisk", "Quiet capture risk", MetricDirection.LOWER_IS_BETTER, "Capture risk hidden behind formally independent institutions."),
            new MetricDefinition("districtPreferenceVariance", "District preference variance", MetricDirection.DIAGNOSTIC, "Within-district generated preference spread."),
            new MetricDefinition("turnoutSkewIndex", "Turnout skew", MetricDirection.LOWER_IS_BETTER, "How strongly attention weighting favors high-intensity extremes."),
            new MetricDefinition("affectedGroupRepresentationGap", "Affected-group gap", MetricDirection.LOWER_IS_BETTER, "Gap between affected-group exposure and representation in public-signal estimation."),
            new MetricDefinition("constituentAttentionIndex", "Constituent attention", MetricDirection.DIAGNOSTIC, "Generated constituent attention and salience intensity."),
            new MetricDefinition("publicWillPolarization", "Public-will polarization", MetricDirection.LOWER_IS_BETTER, "Distance between constituent samples and proposal position."),
            new MetricDefinition("strategyLearningPressure", "Strategy learning pressure", MetricDirection.DIAGNOSTIC, "How strongly repeated outcomes push strategic adjustment."),
            new MetricDefinition("strategicTimingDelayRate", "Strategic timing delay", MetricDirection.DIAGNOSTIC, "Bills delayed by adaptive timing."),
            new MetricDefinition("riskySubmissionRate", "Risky submission", MetricDirection.LOWER_IS_BETTER, "Risky proposals submitted despite learned risk."),
            new MetricDefinition("ruleLearningGain", "Rule learning gain", MetricDirection.HIGHER_IS_BETTER, "Change in learned proposer trust or strategy quality."),
            new MetricDefinition("strategyModerationRate", "Strategy moderation", MetricDirection.DIAGNOSTIC, "Policy movement caused by strategic adaptation."),
            new MetricDefinition("adaptiveCoalitionSeekingRate", "Adaptive coalition seeking", MetricDirection.HIGHER_IS_BETTER, "Strategic attempts to seek outside-bloc support."),
            new MetricDefinition("packageDealDepth", "Package-deal depth", MetricDirection.DIAGNOSTIC, "Extent of cross-issue package construction."),
            new MetricDefinition("sidePaymentLoad", "Side-payment load", MetricDirection.LOWER_IS_BETTER, "Distributional side-payment burden inside omnibus bargains."),
            new MetricDefinition("omnibusComplexity", "Omnibus complexity", MetricDirection.LOWER_IS_BETTER, "Implementation and transparency cost from package size."),
            new MetricDefinition("jurisdictionalTradeRate", "Jurisdictional trade", MetricDirection.DIAGNOSTIC, "Cross-issue or cross-jurisdiction bargains."),
            new MetricDefinition("distributiveBargainShare", "Distributive bargain share", MetricDirection.DIAGNOSTIC, "How much compromise relies on distributive bargains."),
            new MetricDefinition("multidimensionalCompromiseGain", "Multidimensional compromise gain", MetricDirection.HIGHER_IS_BETTER, "Support gain from package bargaining."),
            new MetricDefinition("shadowLobbyingShare", "Shadow lobbying share", MetricDirection.LOWER_IS_BETTER, "Influence spending not detected by disclosure and watchdogs."),
            new MetricDefinition("campaignFinanceCaptureIndex", "Campaign-finance capture", MetricDirection.LOWER_IS_BETTER, "Capture pressure from campaign-finance-like influence."),
            new MetricDefinition("watchdogDetectionRate", "Watchdog detection", MetricDirection.HIGHER_IS_BETTER, "Detected share of organized influence pressure."),
            new MetricDefinition("enforcementDeterrence", "Enforcement deterrence", MetricDirection.HIGHER_IS_BETTER, "Disclosure and watchdog deterrence against hidden influence."),
            new MetricDefinition("publicMatchingOffset", "Public matching offset", MetricDirection.HIGHER_IS_BETTER, "Public financing offset to private influence."),
            new MetricDefinition("influenceSystemResilience", "Influence-system resilience", MetricDirection.HIGHER_IS_BETTER, "Combined detection, deterrence, and public-financing resilience."),
            new MetricDefinition("courtIndependenceScore", "Court independence", MetricDirection.HIGHER_IS_BETTER, "Insulation, transparency, size, and en banc review proxy."),
            new MetricDefinition("courtConstraintIndex", "Court constraint", MetricDirection.HIGHER_IS_BETTER, "Emergency-docket and invalidation-procedure constraints."),
            new MetricDefinition("shadowDocketUseRate", "Emergency docket use", MetricDirection.LOWER_IS_BETTER, "Use of emergency or shadow-docket-like review."),
            new MetricDefinition("emergencyOrderExpirationRate", "Emergency-order expiration", MetricDirection.HIGHER_IS_BETTER, "Emergency-order constraint and expiration proxy."),
            new MetricDefinition("signedOpinionDisclosureRate", "Signed-opinion disclosure", MetricDirection.HIGHER_IS_BETTER, "Transparency of court decisions."),
            new MetricDefinition("constitutionalInvalidationRate", "Constitutional invalidation", MetricDirection.DIAGNOSTIC, "Share of enacted bills invalidated by court architecture."),
            new MetricDefinition("courtReviewPressure", "Court review pressure", MetricDirection.DIAGNOSTIC, "Rights, capture, uncertainty, and policy-shock pressure for review.")
    );

    private static final Map<String, MetricDefinition> BY_KEY = DEFINITIONS.stream()
            .collect(Collectors.toUnmodifiableMap(MetricDefinition::key, Function.identity()));

    public static List<MetricDefinition> definitions() {
        return DEFINITIONS;
    }

    public static MetricDefinition require(String key) {
        MetricDefinition definition = BY_KEY.get(key);
        if (definition == null) {
            throw new IllegalArgumentException("Unknown metric: " + key);
        }
        return definition;
    }

    public static double clamp01(double value) {
        return Math.clamp(value, 0.0, 1.0);
    }

    public static double higherIsBetter(double value) {
        return clamp01(value);
    }

    public static double lowerIsBetter(double value) {
        return 1.0 - clamp01(value);
    }

    public static double lowerIsBetter(double value, double maxValue) {
        if (maxValue <= 0.0) {
            return lowerIsBetter(value);
        }
        return 1.0 - clamp01(value / maxValue);
    }

    public static double average(double... values) {
        if (values.length == 0) {
            return 0.0;
        }
        double sum = 0.0;
        for (double value : values) {
            sum += clamp01(value);
        }
        return sum / values.length;
    }
}
