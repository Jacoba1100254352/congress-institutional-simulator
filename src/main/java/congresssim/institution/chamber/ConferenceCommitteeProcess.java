package congresssim.institution.chamber;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.List;

public final class ConferenceCommitteeProcess implements LegislativeProcess {
    private final String name;
    private final Chamber firstChamber;
    private final Chamber secondChamber;
    private final double conferenceTrigger;
    private final double revisionTarget;
    private final double revisionRate;
    private final double dealCost;

    public ConferenceCommitteeProcess(
            String name,
            Chamber firstChamber,
            Chamber secondChamber,
            double conferenceTrigger,
            double revisionTarget,
            double revisionRate,
            double dealCost
    ) {
        Values.requireRange("conferenceTrigger", conferenceTrigger, 0.0, 1.0);
        Values.requireRange("revisionTarget", revisionTarget, -1.0, 1.0);
        Values.requireRange("revisionRate", revisionRate, 0.0, 1.0);
        Values.requireRange("dealCost", dealCost, 0.0, 1.0);
        this.name = name;
        this.firstChamber = firstChamber;
        this.secondChamber = secondChamber;
        this.conferenceTrigger = conferenceTrigger;
        this.revisionTarget = revisionTarget;
        this.revisionRate = revisionRate;
        this.dealCost = dealCost;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        ChamberVoteResult firstResult = firstChamber.voteOn(bill, context);
        ChamberVoteResult secondResult = secondChamber.voteOn(bill, context);
        double statusQuoBefore = context.currentPolicyPosition();
        if (firstResult.passed() && secondResult.passed()) {
            return new BillOutcome(
                    bill,
                    statusQuoBefore,
                    bill.ideologyPosition(),
                    true,
                    List.of(firstResult, secondResult),
                    PresidentialAction.none(),
                    "passed both chambers before conference"
            );
        }

        double conferenceSupport = (firstResult.yayShare() + secondResult.yayShare()) / 2.0;
        if (conferenceSupport < conferenceTrigger) {
            return new BillOutcome(
                    bill,
                    statusQuoBefore,
                    statusQuoBefore,
                    false,
                    List.of(firstResult, secondResult),
                    PresidentialAction.none(),
                    "failed before conference threshold"
            );
        }

        Bill conferenceBill = conferenceRevision(bill);
        ChamberVoteResult firstConference = firstChamber.voteOn(conferenceBill, context);
        ChamberVoteResult secondConference = secondChamber.voteOn(conferenceBill, context);
        boolean enacted = firstConference.passed() && secondConference.passed();
        return new BillOutcome(
                conferenceBill,
                statusQuoBefore,
                enacted ? conferenceBill.ideologyPosition() : statusQuoBefore,
                enacted,
                List.of(firstResult, secondResult, firstConference, secondConference),
                PresidentialAction.none(),
                enacted ? "conference report passed both chambers" : "conference report failed"
        );
    }

    private Bill conferenceRevision(Bill bill) {
        double revisedPosition = Values.clamp(
                bill.ideologyPosition() + (revisionRate * (revisionTarget - bill.ideologyPosition())),
                -1.0,
                1.0
        );
        double movement = Math.abs(revisedPosition - bill.ideologyPosition());
        double supportGain = movement * 0.16;
        double benefitCost = dealCost * (0.06 + (0.08 * bill.publicBenefitUncertainty()));
        double revisedSupport = Values.clamp(bill.publicSupport() + supportGain, 0.0, 1.0);
        double revisedBenefit = Values.clamp(bill.publicBenefit() - benefitCost, 0.0, 1.0);
        return bill.withAmendment(revisedPosition, revisedSupport, revisedBenefit);
    }
}
