package congresssim.institution.lobbying;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.LobbyGroup;
import congresssim.util.Values;

import java.util.List;
import java.util.Map;

public final class InfluenceSystemProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<LobbyGroup> lobbyGroups;
    private final double disclosureEnforcement;
    private final double publicMatchingStrength;
    private final double watchdogCapacity;
    private final double shadowLobbyTolerance;

    public InfluenceSystemProcess(
            String name,
            LegislativeProcess innerProcess,
            List<LobbyGroup> lobbyGroups,
            double disclosureEnforcement,
            double publicMatchingStrength,
            double watchdogCapacity,
            double shadowLobbyTolerance
    ) {
        Values.requireRange("disclosureEnforcement", disclosureEnforcement, 0.0, 1.0);
        Values.requireRange("publicMatchingStrength", publicMatchingStrength, 0.0, 1.0);
        Values.requireRange("watchdogCapacity", watchdogCapacity, 0.0, 1.0);
        Values.requireRange("shadowLobbyTolerance", shadowLobbyTolerance, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.lobbyGroups = List.copyOf(lobbyGroups);
        this.disclosureEnforcement = disclosureEnforcement;
        this.publicMatchingStrength = publicMatchingStrength;
        this.watchdogCapacity = watchdogCapacity;
        this.shadowLobbyTolerance = shadowLobbyTolerance;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        InfluenceResult result = applyInfluence(bill);
        return innerProcess.consider(result.bill(), context)
                .withSignals(OutcomeSignals.diagnostics(Map.of(
                        "shadowLobbyingShare", result.shadowShare(),
                        "campaignFinanceCaptureIndex", result.captureIndex(),
                        "watchdogDetectionRate", result.detectionRate(),
                        "enforcementDeterrence", result.deterrence(),
                        "publicMatchingOffset", result.publicOffset(),
                        "influenceSystemResilience", result.resilience()
                )));
    }

    private InfluenceResult applyInfluence(Bill bill) {
        double observedSpend = 0.0;
        double shadowSpend = 0.0;
        double pressure = bill.lobbyPressure();
        double publicSupport = bill.publicSupport();
        double publicBenefit = bill.publicBenefit();
        double privateGain = bill.privateGain();

        for (LobbyGroup group : lobbyGroups) {
            double preference = bill.antiLobbyingReform()
                    ? Math.max(0.40, group.preferenceFor("democracy"))
                    : group.preferenceFor(bill.issueDomain());
            if (preference <= 0.000001) {
                continue;
            }
            double threatMultiplier = bill.antiLobbyingReform()
                    ? group.defensiveMultiplier() * (0.70 + bill.salience())
                    : 0.80 + (0.40 * Math.max(0.0, bill.privateGain() - bill.publicBenefit()));
            double intent = group.budget() * preference * group.influenceIntensity() * threatMultiplier * 0.22;
            double shadowShare = Values.clamp(
                    shadowLobbyTolerance
                            * (0.35 + (0.35 * group.informationBias()) + (0.30 * Math.max(0.0, bill.lobbyPressure()))),
                    0.0,
                    0.92
            );
            double detectedShare = Values.clamp(disclosureEnforcement * watchdogCapacity * (0.40 + (0.60 * bill.salience())), 0.0, 1.0);
            double hiddenSpend = intent * shadowShare * (1.0 - detectedShare);
            double visibleSpend = intent - hiddenSpend;
            observedSpend += visibleSpend;
            shadowSpend += hiddenSpend;
            double netPressure = (visibleSpend * 0.10) + (hiddenSpend * 0.18);
            if (bill.antiLobbyingReform()) {
                pressure -= netPressure;
                publicSupport -= hiddenSpend * 0.05;
                publicBenefit -= hiddenSpend * 0.025;
            } else {
                pressure += netPressure;
                publicSupport += visibleSpend * group.publicCampaignSkill() * 0.025;
                publicSupport -= hiddenSpend * 0.030 * (1.0 - publicMatchingStrength);
                publicBenefit -= hiddenSpend * group.informationBias() * 0.025;
                privateGain += intent * 0.035;
            }
        }

        double totalSpend = observedSpend + shadowSpend;
        double detectionRate = totalSpend == 0.0 ? 0.0 : observedSpend / totalSpend;
        double publicOffset = publicMatchingStrength * Math.max(0.0, publicBenefit - privateGain) * 0.18;
        pressure -= Math.max(0.0, pressure) * publicMatchingStrength * 0.16;
        publicSupport += publicOffset;
        privateGain -= privateGain * publicMatchingStrength * 0.05;
        double captureIndex = Values.clamp(
                (0.36 * Math.max(0.0, pressure))
                        + (0.24 * privateGain)
                        + (0.20 * (1.0 - detectionRate))
                        + (0.20 * (totalSpend / Math.max(1.0, lobbyGroups.size() * 2.0))),
                0.0,
                1.0
        );
        double deterrence = Values.clamp(disclosureEnforcement * watchdogCapacity * (1.0 - shadowLobbyTolerance), 0.0, 1.0);
        double resilience = Values.clamp((0.40 * detectionRate) + (0.30 * deterrence) + (0.30 * publicMatchingStrength), 0.0, 1.0);
        Bill revised = bill.withLobbyActivity(
                Values.clamp(pressure, -1.0, 1.0),
                Values.clamp(publicSupport, 0.0, 1.0),
                Values.clamp(publicBenefit, 0.0, 1.0),
                Values.clamp(privateGain, 0.0, 1.0),
                totalSpend,
                bill.antiLobbyingReform() ? totalSpend : 0.0,
                observedSpend * 0.34,
                observedSpend * 0.22,
                observedSpend * 0.18,
                observedSpend * 0.18,
                shadowSpend * 0.60
        );
        return new InfluenceResult(
                revised,
                totalSpend == 0.0 ? 0.0 : shadowSpend / totalSpend,
                captureIndex,
                detectionRate,
                deterrence,
                publicOffset,
                resilience
        );
    }

    private record InfluenceResult(
            Bill bill,
            double shadowShare,
            double captureIndex,
            double detectionRate,
            double deterrence,
            double publicOffset,
            double resilience
    ) {
    }
}
