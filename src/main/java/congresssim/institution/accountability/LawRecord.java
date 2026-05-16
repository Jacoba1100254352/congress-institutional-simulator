package congresssim.institution.accountability;


import congresssim.model.Bill;


record LawRecord(
		Bill sourceBill,
		double previousStatusQuo,
		double enactedPosition,
		int enactedRound,
		int effectiveRound,
		int reviewDueRound,
		double implementationCapacity,
		boolean underfunded,
		boolean nonenforced,
		boolean stayed,
		double renewalLobbyPressure,
		boolean active
)
{
	LawRecord withReviewDueRound(int revisedReviewDueRound) {
		return new LawRecord(
				sourceBill,
				previousStatusQuo,
				enactedPosition,
				enactedRound,
				effectiveRound,
				revisedReviewDueRound,
				implementationCapacity,
				underfunded,
				nonenforced,
				stayed,
				renewalLobbyPressure,
				active
		);
	}
	
	LawRecord deactivate() {
		return new LawRecord(
				sourceBill,
				previousStatusQuo,
				enactedPosition,
				enactedRound,
				effectiveRound,
				reviewDueRound,
				implementationCapacity,
				underfunded,
				nonenforced,
				stayed,
				renewalLobbyPressure,
				false
		);
	}
}
