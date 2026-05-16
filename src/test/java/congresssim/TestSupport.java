package congresssim;


import congresssim.behavior.VoteContext;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.model.Bill;
import congresssim.model.Legislator;

import java.util.List;


final class TestSupport
{
	private TestSupport() {
	}
	
	static Legislator legislator(String id) {
		return new Legislator(id, "Test", 0.0, 0.5, 0.5, 0.5, 0.5, 0.5);
	}
	
	static LegislativeProcess labeledProcess(String label) {
		return new LegislativeProcess()
		{
			@Override
			public String name() {
				return label;
			}
			
			@Override
			public BillOutcome consider(Bill bill, VoteContext context) {
				return new BillOutcome(
						bill,
						context.currentPolicyPosition(),
						context.currentPolicyPosition(),
						false,
						List.of(),
						congresssim.institution.chamber.PresidentialAction.none(),
						label
				);
			}
		};
	}
	
	static void assertTrue(boolean condition, String message) {
		if (!condition) {
			throw new AssertionError(message);
		}
	}
	
	static void assertFalse(boolean condition, String message) {
		assertTrue(!condition, message);
	}
	
	static void assertThrows(Runnable action, String message) {
		try {
			action.run();
		} catch (RuntimeException expected) {
			return;
		}
		throw new AssertionError(message);
	}
	
	static void assertRatio(double value, String message) {
		assertTrue(Double.isFinite(value) && value >= 0.0 && value <= 1.0, message + " Actual: " + value);
	}
	
	static void assertNonNegativeFinite(double value, String message) {
		assertTrue(Double.isFinite(value) && value >= 0.0, message + " Actual: " + value);
	}
	
	static int csvColumnCount(String line) {
		int columns = 1;
		boolean quoted = false;
		for (int index = 0; index < line.length(); index++) {
			char current = line.charAt(index);
			if (current == '"') {
				if (quoted && index + 1 < line.length() && line.charAt(index + 1) == '"') {
					index++;
				} else {
					quoted = !quoted;
				}
			} else if (current == ',' && !quoted) {
				columns++;
			}
		}
		return columns;
	}
}
