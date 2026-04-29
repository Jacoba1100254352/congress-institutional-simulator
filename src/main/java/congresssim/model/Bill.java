package congresssim.model;

import congresssim.util.Values;

public record Bill(
        String id,
        String title,
        String proposerId,
        double proposerIdeology,
        double ideologyPosition,
        double publicSupport,
        double publicBenefit,
        double lobbyPressure,
        double salience,
        double privateGain,
        boolean antiLobbyingReform,
        String issueDomain,
        double lobbySpend,
        double defensiveLobbySpend,
        double originalIdeologyPosition,
        double amendmentMovement,
        String affectedGroup,
        double affectedGroupSupport,
        double concentratedHarm,
        double compensationCost,
        boolean compensationAdded,
        double directLobbySpend,
        double agendaLobbySpend,
        double informationLobbySpend,
        double publicCampaignSpend,
        double litigationThreatSpend,
        double citizenPanelLegitimacy,
        boolean citizenCertified,
        double attentionSpend
) {
    public Bill {
        Values.requireRange("proposerIdeology", proposerIdeology, -1.0, 1.0);
        Values.requireRange("ideologyPosition", ideologyPosition, -1.0, 1.0);
        Values.requireRange("publicSupport", publicSupport, 0.0, 1.0);
        Values.requireRange("publicBenefit", publicBenefit, 0.0, 1.0);
        Values.requireRange("lobbyPressure", lobbyPressure, -1.0, 1.0);
        Values.requireRange("salience", salience, 0.0, 1.0);
        Values.requireRange("privateGain", privateGain, 0.0, 1.0);
        Values.requireRange("lobbySpend", lobbySpend, 0.0, 100.0);
        Values.requireRange("defensiveLobbySpend", defensiveLobbySpend, 0.0, 100.0);
        Values.requireRange("originalIdeologyPosition", originalIdeologyPosition, -1.0, 1.0);
        Values.requireRange("amendmentMovement", amendmentMovement, 0.0, 10.0);
        Values.requireRange("affectedGroupSupport", affectedGroupSupport, 0.0, 1.0);
        Values.requireRange("concentratedHarm", concentratedHarm, 0.0, 1.0);
        Values.requireRange("compensationCost", compensationCost, 0.0, 1.0);
        Values.requireRange("directLobbySpend", directLobbySpend, 0.0, 100.0);
        Values.requireRange("agendaLobbySpend", agendaLobbySpend, 0.0, 100.0);
        Values.requireRange("informationLobbySpend", informationLobbySpend, 0.0, 100.0);
        Values.requireRange("publicCampaignSpend", publicCampaignSpend, 0.0, 100.0);
        Values.requireRange("litigationThreatSpend", litigationThreatSpend, 0.0, 100.0);
        Values.requireRange("citizenPanelLegitimacy", citizenPanelLegitimacy, 0.0, 1.0);
        Values.requireRange("attentionSpend", attentionSpend, 0.0, 100.0);
    }

    public Bill(
            String id,
            String title,
            String proposerId,
            double proposerIdeology,
            double ideologyPosition,
            double publicSupport,
            double publicBenefit,
            double lobbyPressure,
            double salience
    ) {
        this(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                Math.max(0.0, lobbyPressure),
                false,
                "general",
                0.0,
                0.0,
                ideologyPosition,
                0.0,
                "general",
                publicSupport,
                0.0,
                0.0,
                false,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                false,
                0.0
        );
    }

    public Bill(
            String id,
            String title,
            String proposerId,
            double proposerIdeology,
            double ideologyPosition,
            double publicSupport,
            double publicBenefit,
            double lobbyPressure,
            double salience,
            double privateGain,
            boolean antiLobbyingReform
    ) {
        this(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                antiLobbyingReform,
                antiLobbyingReform ? "democracy" : "general",
                0.0,
                0.0,
                ideologyPosition,
                0.0,
                "general",
                publicSupport,
                0.0,
                0.0,
                false,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                false,
                0.0
        );
    }

    public Bill(
            String id,
            String title,
            String proposerId,
            double proposerIdeology,
            double ideologyPosition,
            double publicSupport,
            double publicBenefit,
            double lobbyPressure,
            double salience,
            double privateGain,
            boolean antiLobbyingReform,
            String issueDomain,
            double lobbySpend,
            double defensiveLobbySpend
    ) {
        this(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                antiLobbyingReform,
                issueDomain,
                lobbySpend,
                defensiveLobbySpend,
                ideologyPosition,
                0.0,
                "general",
                publicSupport,
                0.0,
                0.0,
                false,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                false,
                0.0
        );
    }

    public Bill(
            String id,
            String title,
            String proposerId,
            double proposerIdeology,
            double ideologyPosition,
            double publicSupport,
            double publicBenefit,
            double lobbyPressure,
            double salience,
            double privateGain,
            boolean antiLobbyingReform,
            String issueDomain,
            double lobbySpend,
            double defensiveLobbySpend,
            String affectedGroup,
            double affectedGroupSupport,
            double concentratedHarm,
            double compensationCost
    ) {
        this(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                antiLobbyingReform,
                issueDomain,
                lobbySpend,
                defensiveLobbySpend,
                ideologyPosition,
                0.0,
                affectedGroup,
                affectedGroupSupport,
                concentratedHarm,
                compensationCost,
                false,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                false,
                0.0
        );
    }

    public Bill withPublicSignal(double revisedPublicSupport, double revisedSalience) {
        return copy(
                ideologyPosition,
                revisedPublicSupport,
                publicBenefit,
                lobbyPressure,
                revisedSalience,
                privateGain,
                lobbySpend,
                defensiveLobbySpend,
                amendmentMovement,
                affectedGroup,
                affectedGroupSupport,
                concentratedHarm,
                compensationCost,
                compensationAdded,
                directLobbySpend,
                agendaLobbySpend,
                informationLobbySpend,
                publicCampaignSpend,
                litigationThreatSpend,
                citizenPanelLegitimacy,
                citizenCertified,
                attentionSpend
        );
    }

    public Bill withLobbySignal(double revisedLobbyPressure, double revisedPublicSupport) {
        return copy(
                ideologyPosition,
                revisedPublicSupport,
                publicBenefit,
                revisedLobbyPressure,
                salience,
                privateGain,
                lobbySpend,
                defensiveLobbySpend,
                amendmentMovement,
                affectedGroup,
                affectedGroupSupport,
                concentratedHarm,
                compensationCost,
                compensationAdded,
                directLobbySpend,
                agendaLobbySpend,
                informationLobbySpend,
                publicCampaignSpend,
                litigationThreatSpend,
                citizenPanelLegitimacy,
                citizenCertified,
                attentionSpend
        );
    }

    public Bill withLobbyActivity(
            double revisedLobbyPressure,
            double revisedPublicSupport,
            double revisedPrivateGain,
            double addedLobbySpend,
            double addedDefensiveLobbySpend
    ) {
        return withLobbyActivity(
                revisedLobbyPressure,
                revisedPublicSupport,
                revisedPrivateGain,
                addedLobbySpend,
                addedDefensiveLobbySpend,
                addedLobbySpend,
                0.0,
                0.0,
                0.0,
                0.0
        );
    }

    public Bill withLobbyActivity(
            double revisedLobbyPressure,
            double revisedPublicSupport,
            double revisedPrivateGain,
            double addedLobbySpend,
            double addedDefensiveLobbySpend,
            double addedDirectSpend,
            double addedAgendaSpend,
            double addedInformationSpend,
            double addedPublicCampaignSpend,
            double addedLitigationThreatSpend
    ) {
        return copy(
                ideologyPosition,
                revisedPublicSupport,
                publicBenefit,
                revisedLobbyPressure,
                salience,
                revisedPrivateGain,
                lobbySpend + addedLobbySpend,
                defensiveLobbySpend + addedDefensiveLobbySpend,
                amendmentMovement,
                affectedGroup,
                affectedGroupSupport,
                concentratedHarm,
                compensationCost,
                compensationAdded,
                directLobbySpend + addedDirectSpend,
                agendaLobbySpend + addedAgendaSpend,
                informationLobbySpend + addedInformationSpend,
                publicCampaignSpend + addedPublicCampaignSpend,
                litigationThreatSpend + addedLitigationThreatSpend,
                citizenPanelLegitimacy,
                citizenCertified,
                attentionSpend
        );
    }

    public Bill withAmendment(
            double revisedIdeologyPosition,
            double revisedPublicSupport,
            double revisedPublicBenefit
    ) {
        return copy(
                revisedIdeologyPosition,
                revisedPublicSupport,
                revisedPublicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                lobbySpend,
                defensiveLobbySpend,
                amendmentMovement + Math.abs(revisedIdeologyPosition - ideologyPosition),
                affectedGroup,
                affectedGroupSupport,
                concentratedHarm,
                compensationCost,
                compensationAdded,
                directLobbySpend,
                agendaLobbySpend,
                informationLobbySpend,
                publicCampaignSpend,
                litigationThreatSpend,
                citizenPanelLegitimacy,
                citizenCertified,
                attentionSpend
        );
    }

    public Bill withCompensation(double revisedPublicBenefit, double revisedAffectedGroupSupport, double revisedConcentratedHarm) {
        return copy(
                ideologyPosition,
                publicSupport,
                revisedPublicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                lobbySpend,
                defensiveLobbySpend,
                amendmentMovement,
                affectedGroup,
                revisedAffectedGroupSupport,
                revisedConcentratedHarm,
                compensationCost,
                true,
                directLobbySpend,
                agendaLobbySpend,
                informationLobbySpend,
                publicCampaignSpend,
                litigationThreatSpend,
                citizenPanelLegitimacy,
                citizenCertified,
                attentionSpend
        );
    }

    public Bill withAffectedGroup(
            String revisedAffectedGroup,
            double revisedAffectedGroupSupport,
            double revisedConcentratedHarm,
            double revisedCompensationCost
    ) {
        return copy(
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                lobbySpend,
                defensiveLobbySpend,
                amendmentMovement,
                revisedAffectedGroup,
                revisedAffectedGroupSupport,
                revisedConcentratedHarm,
                revisedCompensationCost,
                compensationAdded,
                directLobbySpend,
                agendaLobbySpend,
                informationLobbySpend,
                publicCampaignSpend,
                litigationThreatSpend,
                citizenPanelLegitimacy,
                citizenCertified,
                attentionSpend
        );
    }

    public Bill withCitizenPanel(double revisedPublicSupport, double revisedPublicBenefit, double legitimacy, boolean certified) {
        return copy(
                ideologyPosition,
                revisedPublicSupport,
                revisedPublicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                lobbySpend,
                defensiveLobbySpend,
                amendmentMovement,
                affectedGroup,
                affectedGroupSupport,
                concentratedHarm,
                compensationCost,
                compensationAdded,
                directLobbySpend,
                agendaLobbySpend,
                informationLobbySpend,
                publicCampaignSpend,
                litigationThreatSpend,
                legitimacy,
                certified,
                attentionSpend
        );
    }

    public Bill withAttentionSpend(double addedAttentionSpend) {
        return copy(
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                lobbySpend,
                defensiveLobbySpend,
                amendmentMovement,
                affectedGroup,
                affectedGroupSupport,
                concentratedHarm,
                compensationCost,
                compensationAdded,
                directLobbySpend,
                agendaLobbySpend,
                informationLobbySpend,
                publicCampaignSpend,
                litigationThreatSpend,
                citizenPanelLegitimacy,
                citizenCertified,
                attentionSpend + addedAttentionSpend
        );
    }

    private Bill copy(
            double revisedIdeologyPosition,
            double revisedPublicSupport,
            double revisedPublicBenefit,
            double revisedLobbyPressure,
            double revisedSalience,
            double revisedPrivateGain,
            double revisedLobbySpend,
            double revisedDefensiveLobbySpend,
            double revisedAmendmentMovement,
            String revisedAffectedGroup,
            double revisedAffectedGroupSupport,
            double revisedConcentratedHarm,
            double revisedCompensationCost,
            boolean revisedCompensationAdded,
            double revisedDirectLobbySpend,
            double revisedAgendaLobbySpend,
            double revisedInformationLobbySpend,
            double revisedPublicCampaignSpend,
            double revisedLitigationThreatSpend,
            double revisedCitizenPanelLegitimacy,
            boolean revisedCitizenCertified,
            double revisedAttentionSpend
    ) {
        return new Bill(
                id,
                title,
                proposerId,
                proposerIdeology,
                revisedIdeologyPosition,
                revisedPublicSupport,
                revisedPublicBenefit,
                revisedLobbyPressure,
                revisedSalience,
                revisedPrivateGain,
                antiLobbyingReform,
                issueDomain,
                revisedLobbySpend,
                revisedDefensiveLobbySpend,
                originalIdeologyPosition,
                revisedAmendmentMovement,
                revisedAffectedGroup,
                revisedAffectedGroupSupport,
                revisedConcentratedHarm,
                revisedCompensationCost,
                revisedCompensationAdded,
                revisedDirectLobbySpend,
                revisedAgendaLobbySpend,
                revisedInformationLobbySpend,
                revisedPublicCampaignSpend,
                revisedLitigationThreatSpend,
                revisedCitizenPanelLegitimacy,
                revisedCitizenCertified,
                revisedAttentionSpend
        );
    }
}
