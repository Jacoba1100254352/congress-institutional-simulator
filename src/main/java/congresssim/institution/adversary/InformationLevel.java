package congresssim.institution.adversary;


public enum InformationLevel
{
	LOW("low"),
	MEDIUM("medium"),
	HIGH("high");

	private final String key;

	InformationLevel(String key) {
		this.key = key;
	}

	public String key() {
		return key;
	}
}
