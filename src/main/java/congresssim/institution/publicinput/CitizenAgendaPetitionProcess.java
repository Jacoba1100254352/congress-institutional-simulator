package congresssim.institution.publicinput;


import congresssim.behavior.VoteContext;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.lobbying.LobbyCaptureScoring;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.Map;


public final class CitizenAgendaPetitionProcess implements LegislativeProcess
{
	private final String name;
	private final LegislativeProcess ordinaryProcess;
	private final LegislativeProcess petitionBypassProcess;
	private final double petitionThreshold;
	private final double salienceThreshold;
	private final double capturePenaltyWeight;
	private final double publicSignalBoost;
	private final double agendaDelayCost;
	
	public CitizenAgendaPetitionProcess(
			String name,
			LegislativeProcess ordinaryProcess,
			LegislativeProcess petitionBypassProcess,
			double petitionThreshold,
			double salienceThreshold,
			double capturePenaltyWeight,
			double publicSignalBoost,
			double agendaDelayCost
	) {
		Values.requireRange("petitionThreshold", petitionThreshold, 0.0, 1.0);
		Values.requireRange("salienceThreshold", salienceThreshold, 0.0, 1.0);
		Values.requireRange("capturePenaltyWeight", capturePenaltyWeight, 0.0, 1.0);
		Values.requireRange("publicSignalBoost", publicSignalBoost, 0.0, 1.0);
		Values.requireRange("agendaDelayCost", agendaDelayCost, 0.0, 1.0);
		this.name = name;
		this.ordinaryProcess = ordinaryProcess;
		this.petitionBypassProcess = petitionBypassProcess;
		this.petitionThreshold = petitionThreshold;
		this.salienceThreshold = salienceThreshold;
		this.capturePenaltyWeight = capturePenaltyWeight;
		this.publicSignalBoost = publicSignalBoost;
		this.agendaDelayCost = agendaDelayCost;
	}
	
	private static double captureDistortion(Bill bill) {
		return Values.clamp(
				(0.58 * LobbyCaptureScoring.captureRisk(bill))
						+ (0.16 * Math.max(0.0, bill.privateGain() - bill.publicBenefit()))
						+ (0.14 * bill.publicCampaignSpend() / 10.0)
						+ (0.12 * bill.agendaLobbySpend() / 10.0),
				0.0,
				1.0
		);
	}
	
	private static double costlyParticipationSignal(Bill bill) {
		double affectedUrgency = AffectedGroupScoring.minorityHarm(bill) * (1.0 - bill.affectedGroupSupport());
		double antiCapturePersistence = bill.antiLobbyingReform() ? 0.18 : 0.0;
		return Values.clamp(
				(0.42 * bill.salience())
						+ (0.30 * affectedUrgency)
						+ (0.18 * bill.publicSupport())
						+ antiCapturePersistence
						- (0.12 * Math.max(0.0, bill.publicCampaignSpend() - bill.agendaLobbySpend()) / 10.0),
				0.0,
				1.0
		);
	}
	
	private static double cheapSignalDistortion(Bill bill) {
		return Values.clamp(
				(0.45 * LobbyCaptureScoring.captureRisk(bill))
						+ (0.28 * bill.publicCampaignSpend() / 10.0)
						+ (0.17 * bill.agendaLobbySpend() / 10.0)
						+ (0.10 * Math.max(0.0, bill.privateGain() - bill.publicBenefit())),
				0.0,
				1.0
		);
	}
	
	@Override
	public String name() {
		return name;
	}
	
	@Override
	public BillOutcome consider(Bill bill, VoteContext context) {
		double signal = petitionSignal(bill, context);
		double distortion = captureDistortion(bill);
		double costlyParticipation = costlyParticipationSignal(bill);
		double cheapSignalDistortion = cheapSignalDistortion(bill);
		boolean qualifies = signal >= petitionThreshold && bill.salience() >= salienceThreshold;
		OutcomeSignals signals = OutcomeSignals.diagnostics(Map.of(
				"citizenAgendaPetitionRate", qualifies ? 1.0 : 0.0,
				"petitionMandateStrength", qualifies ? signal : 0.0,
				"petitionCaptureDistortion", qualifies ? distortion : 0.0,
				"costlyPublicMandateSignal", qualifies ? costlyParticipation : 0.0,
				"cheapSignalDistortion", qualifies ? cheapSignalDistortion : 0.0,
				"publicMandateIntensity", qualifies ? bill.salience() * signal : 0.0
		));
		
		if (!qualifies) {
			return ordinaryProcess.consider(bill, context).withSignals(signals);
		}
		
		double revisedSupport = Values.clamp(
				bill.publicSupport() + (publicSignalBoost * (signal - bill.publicSupport())),
				0.0,
				1.0
		);
		Bill petitionedBill = bill.withPublicSignal(
				revisedSupport,
				Values.clamp(bill.salience() + 0.07 + (0.04 * signal), 0.0, 1.0)
		).withAttentionSpend(agendaDelayCost * (1.0 + distortion));
		
		OutcomeSignals publicWillSignals = OutcomeSignals.publicWill(
				Math.abs(revisedSupport - bill.publicSupport()),
				Values.clamp(1.0 - Math.abs(signal - bill.publicSupport()), 0.0, 1.0)
		);
		return petitionBypassProcess.consider(petitionedBill, context).withSignals(signals.plus(publicWillSignals));
	}
	
	private double petitionSignal(Bill bill, VoteContext context) {
		double affectedUrgency = AffectedGroupScoring.minorityHarm(bill) * (1.0 - bill.affectedGroupSupport());
		double costlyParticipation = costlyParticipationSignal(bill);
		double cheapDistortion = cheapSignalDistortion(bill);
		double reformSignal = bill.antiLobbyingReform() ? 0.08 : 0.0;
		double noise = context.random().nextGaussian() * 0.018;
		return Values.clamp(
				(0.42 * bill.publicSupport())
						+ (0.18 * bill.salience())
						+ (0.16 * bill.publicBenefit())
						+ (0.13 * costlyParticipation)
						+ (0.10 * affectedUrgency)
						+ reformSignal
						- (capturePenaltyWeight * LobbyCaptureScoring.captureRisk(bill))
						- (0.12 * cheapDistortion)
						+ noise,
				0.0,
				1.0
		);
	}
}
