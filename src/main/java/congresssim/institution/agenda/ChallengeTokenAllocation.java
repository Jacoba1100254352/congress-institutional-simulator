package congresssim.institution.agenda;

import congresssim.model.Legislator;

public enum ChallengeTokenAllocation {
    PARTY {
        @Override
        String ownerOf(Legislator legislator) {
            return legislator.party();
        }

        @Override
        String labelFor(Legislator legislator) {
            return legislator.party();
        }
    },
    PARTY_PROPORTIONAL {
        @Override
        String ownerOf(Legislator legislator) {
            return legislator.party();
        }

        @Override
        String labelFor(Legislator legislator) {
            return legislator.party();
        }
    },
    PARTY_MINORITY_BONUS {
        @Override
        String ownerOf(Legislator legislator) {
            return legislator.party();
        }

        @Override
        String labelFor(Legislator legislator) {
            return legislator.party();
        }
    },
    LEGISLATOR {
        @Override
        String ownerOf(Legislator legislator) {
            return legislator.id();
        }

        @Override
        String labelFor(Legislator legislator) {
            return legislator.id();
        }
    };

    abstract String ownerOf(Legislator legislator);

    abstract String labelFor(Legislator legislator);
}
