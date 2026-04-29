package congresssim.experiment;

import java.nio.file.Path;
import java.util.List;

public record CampaignResult(
        String name,
        List<CampaignRow> rows,
        Path csvPath,
        Path markdownPath
) {
    public CampaignResult {
        rows = List.copyOf(rows);
    }
}

