MAIN_SOURCES := $(shell find src/main/java -name '*.java')
TEST_SOURCES := $(shell find src/test/java -name '*.java')
JAVA_RELEASE ?= 21
JAVA_PROPS ?= -Dcongresssim.javaRelease=$(JAVA_RELEASE)
APP_JAR := out/congresssim.jar
APP_CP := $(APP_JAR)
PAPER_MAIN_TEX := paper/acm-ci-framework/acm-ci-framework.tex
PAPER_MAIN_PDF := paper/acm-ci-framework/acm-ci-framework.pdf
PAPER_APPENDIX_TEX := paper/technical-appendix/odd-d-appendix.tex
PAPER_APPENDIX_PDF := paper/technical-appendix/odd-d-appendix.pdf

.PHONY: check-java build run calibrate calibration-check campaign paper-campaign main-campaign campaign-v0 campaign-v1 campaign-v2 campaign-v3 campaign-v4 campaign-v5 campaign-v6 campaign-v7 campaign-v8 campaign-v9 campaign-v10 campaign-v11 campaign-v12 campaign-v13 campaign-v14 campaign-v15 campaign-v16 campaign-v17 campaign-v18 campaign-v19 campaign-v20 campaign-v21-paper chamber-structure chamber-structure-summary seed-robustness seed-robustness-check family-screen family-champions catalog-breadth findings-validation validation-readiness validation-gap-report empirical-boundary-check raw-source-manifest fetch-validation-samples build-bill-progression-raw build-govinfo-bill-census-raw build-govinfo-billstatus-linkage-raw build-core-raw-validation build-sponsor-bill-linkage-raw build-voteview-member-context-raw build-voteview-bill-linkage-raw build-lobbying-issue-linkage-raw build-lobbying-bill-mentions-raw build-bill-finance-lobbying-external-lda-search-raw build-bill-finance-lobbying-committee-action-source-raw build-campaign-finance-raw build-campaign-finance-linkage-raw build-campaign-finance-member-context-raw build-campaign-finance-issue-context-raw build-district-public-opinion-raw build-district-public-opinion-linkage-raw build-district-public-opinion-policy-context-raw build-district-public-opinion-census-denominators-raw build-district-public-opinion-acs-context-raw build-court-review-raw build-court-law-linkage-raw build-rulemaking-implementation-raw build-rulemaking-implementation-linkage-raw build-rulemaking-authority-linkage-raw build-rulemaking-history-linkage-raw build-rulemaking-comment-metadata-raw build-rulemaking-comment-records-raw build-rulemaking-comment-text-review-raw build-law-revision-raw build-law-revision-bill-linkage-raw build-statutory-lineage-source-scan-raw build-statutory-lineage-olrc-current-scan-raw build-statutory-lineage-olrc-historical-scan-raw build-statutory-lineage-olrc-annual-text-diff-raw build-statutory-lineage-adjudication-raw build-statutory-lineage-target-review-packets-raw build-comparative-institutions-raw build-comparative-institution-linkage-raw empirical-validation empirical-bridge empirical-flow-heldout empirical-data-inventory empirical-linkage-report empirical-linkage-roadmap govinfo-bill-census govinfo-billstatus-linkage sponsor-bill-linkage court-law-linkage comparative-institution-linkage rulemaking-authority-linkage rulemaking-history-linkage rulemaking-comment-metadata rulemaking-comment-records rulemaking-comment-text-review bill-law-evidence-spine bill-law-lifecycle-readiness court-public-law-review-queue court-public-law-temporal-triage court-public-law-direct-review bill-law-lifecycle-next-actions bill-law-lifecycle-corpus bill-finance-lobbying-review-queue bill-finance-lobbying-local-context-review bill-finance-lobbying-external-search-review bill-finance-lobbying-external-lda-mention-review bill-finance-lobbying-campaign-finance-target-scope-review bill-finance-lobbying-committee-action-context bill-finance-lobbying-committee-action-source-review bill-finance-lobbying-source-acquisition-queue statutory-lineage-review-queue statutory-lineage-source-scan statutory-lineage-no-target-review statutory-lineage-target-section-triage statutory-lineage-olrc-current-scan statutory-lineage-olrc-historical-scan statutory-lineage-adjudication statutory-lineage-target-review-packets statutory-lineage-target-section-diff-review statutory-lineage-target-lifecycle-bridge statutory-lineage-codified-progress statutory-lineage-effective-text-review statutory-lineage-public-law-attribution-review statutory-lineage-completion-queue statutory-lineage-complete-lineage-expansion-queue statutory-lineage-target-packet-expansion-queue statutory-lineage-target-packet-source-gap-queue statutory-lineage-target-packet-source-gap-review statutory-lineage-target-reference-resolution-candidates campaign-finance-district-context campaign-finance-member-context campaign-finance-issue-context campaign-finance-sponsor-bill-context district-public-opinion-policy-context district-public-opinion-bill-topic-readiness district-public-opinion-source-packets district-public-opinion-census-denominators district-public-opinion-acs-context district-public-opinion-survey-source-crosswalk district-public-opinion-survey-item-proxy-review district-public-opinion-ces-source-freshness voteview-member-context voteview-bill-linkage lobbying-issue-linkage lobbying-bill-policy-context lobbying-bill-mention-review lobbying-bill-action-context lobbying-bill-text-review lobbying-bill-disposition-review lobbying-bill-manual-disposition-review lobbying-bill-medium-disposition-packets lobbying-bill-medium-directional-packet-review lobbying-bill-medium-position-activity-packet-review ablation-analysis manipulation-stress mechanism-diagnostics public-provenance paper-assets paper paper-word-count paper-checks reproduce-paper-offline paper-freshness-check paper-anonymity-check figure-label-check pdf-render-check pdf-manifest-check table-figure-consistency-check supplement-anonymous supplement-anonymous-current clean-regeneration-check paper-clean test ci github-ci clean
.PHONY: statutory-lineage-olrc-annual-text-diff build-bill-finance-lobbying-roll-call-source-raw build-bill-finance-lobbying-member-vote-target-raw bill-finance-lobbying-roll-call-source-review bill-finance-lobbying-member-vote-target-review failure-trace-report adversary-catalog adversarial-stress adversarial-pilot-cell-map adversarial-stress-manifest
.PHONY: build-district-public-opinion-ces-policy-item-candidates-raw district-public-opinion-ces-policy-item-candidate-review build-district-public-opinion-ces-policy-item-response-distributions-raw district-public-opinion-ces-policy-item-response-distribution-review build-district-public-opinion-ces-policy-item-codebook-direction-raw district-public-opinion-ces-policy-item-codebook-direction-review
.PHONY: build-district-public-opinion-bill-text-context-raw district-public-opinion-bill-item-alignment-review build-district-public-opinion-bill-topic-support-raw district-public-opinion-bill-topic-support
.PHONY: adversarial-replication-a1-a8 adversarial-replication-a9 robustness-evidence legislative-lifecycle-calibration legislative-executive-action-diagnostic legislative-lifecycle-temporal-replication govinfo-executive-action-panel govinfo-joint-resolution-panel govinfo-final-chamber-vote-panel govinfo-bill-census-116 govinfo-bill-census-118 govinfo-bill-census-check build-govinfo-executive-action-panel-raw build-govinfo-joint-resolution-panel-raw build-govinfo-final-chamber-vote-panel-raw build-govinfo-bill-census-116-raw build-govinfo-bill-census-118-raw

check-java:
	@actual="$$(javac -version 2>&1 | awk '{print $$2}' | cut -d. -f1)"; \
	if [ "$$actual" != "$(JAVA_RELEASE)" ]; then \
		echo "Expected javac $(JAVA_RELEASE), found $$actual. Set Java $(JAVA_RELEASE) on PATH before running this Makefile."; \
		echo "macOS: export JAVA_HOME=\$$(/usr/libexec/java_home -v $(JAVA_RELEASE)); export PATH=\$$JAVA_HOME/bin:\$$PATH"; \
		exit 1; \
	fi

build: check-java
	rm -rf out/main $(APP_JAR)
	mkdir -p out/main
	javac --release $(JAVA_RELEASE) -d out/main $(MAIN_SOURCES)
	jar --create --file $(APP_JAR) -C out/main .

run: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main $(ARGS)

calibrate: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --calibrate --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

calibration-check: calibrate
	python3 scripts/checks/check_calibration.py reports/calibration-baseline.csv

campaign: paper-campaign

paper-campaign: campaign-v21-paper

main-campaign: paper-campaign

campaign-v21-paper: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v21-paper --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v20: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v20 --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v19: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v19 --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v18: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v18 --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v17: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v17 --runs 80 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v16: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v16 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v15: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v15 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v14: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v14 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v13: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v13 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v12: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v12 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v11: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v11 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v10: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v10 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v9: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v9 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v8: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v8 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v7: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v7 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v6: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v6 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v5: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v5 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v4: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v4 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v3: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v3 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v2: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v2 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v1: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v1 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v0: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign v0 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

chamber-structure: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign chamber-structure --runs 80 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)
	python3 scripts/reporting/summarize_chamber_structure.py

chamber-structure-summary:
	python3 scripts/reporting/summarize_chamber_structure.py

seed-robustness: build
	APP_CP="$(APP_CP)" JAVA_PROPS="$(JAVA_PROPS)" python3 scripts/reporting/run_seed_robustness.py

seed-robustness-check: seed-robustness
	python3 scripts/checks/check_seed_robustness.py

family-champions: build
	APP_CP="$(APP_CP)" JAVA_PROPS="$(JAVA_PROPS)" python3 scripts/reporting/run_family_champions.py

family-screen: family-champions

catalog-breadth: build
	python3 scripts/reporting/report_catalog_breadth.py

findings-validation: paper-campaign
	python3 scripts/validation/write_findings_validation.py

validation-readiness:
	python3 scripts/validation/validate_empirical_inputs.py

validation-gap-report: validation-readiness empirical-bridge empirical-flow-heldout empirical-data-inventory empirical-linkage-report empirical-linkage-roadmap govinfo-bill-census govinfo-joint-resolution-panel govinfo-final-chamber-vote-panel legislative-lifecycle-calibration legislative-lifecycle-temporal-replication govinfo-billstatus-linkage sponsor-bill-linkage court-law-linkage rulemaking-authority-linkage rulemaking-history-linkage rulemaking-comment-metadata rulemaking-comment-records rulemaking-comment-text-review statutory-lineage-adjudication statutory-lineage-target-review-packets statutory-lineage-target-section-diff-review statutory-lineage-no-target-review bill-law-evidence-spine bill-law-lifecycle-readiness court-public-law-review-queue court-public-law-temporal-triage court-public-law-direct-review bill-law-lifecycle-next-actions bill-law-lifecycle-corpus bill-finance-lobbying-review-queue bill-finance-lobbying-local-context-review bill-finance-lobbying-external-search-review bill-finance-lobbying-external-lda-mention-review bill-finance-lobbying-campaign-finance-target-scope-review bill-finance-lobbying-committee-action-context bill-finance-lobbying-source-acquisition-queue bill-finance-lobbying-roll-call-source-review bill-finance-lobbying-member-vote-target-review lobbying-bill-mention-review lobbying-bill-action-context lobbying-bill-text-review lobbying-bill-disposition-review lobbying-bill-manual-disposition-review lobbying-bill-medium-disposition-packets lobbying-bill-medium-directional-packet-review lobbying-bill-medium-position-activity-packet-review statutory-lineage-target-lifecycle-bridge statutory-lineage-review-queue statutory-lineage-source-scan statutory-lineage-target-section-triage statutory-lineage-olrc-current-scan statutory-lineage-olrc-historical-scan statutory-lineage-olrc-annual-text-diff statutory-lineage-codified-progress statutory-lineage-effective-text-review statutory-lineage-public-law-attribution-review statutory-lineage-completion-queue statutory-lineage-complete-lineage-expansion-queue statutory-lineage-target-packet-expansion-queue statutory-lineage-target-packet-source-gap-queue statutory-lineage-target-packet-source-gap-review statutory-lineage-target-reference-resolution-candidates campaign-finance-district-context campaign-finance-member-context campaign-finance-issue-context campaign-finance-sponsor-bill-context district-public-opinion-policy-context district-public-opinion-bill-topic-readiness district-public-opinion-source-packets district-public-opinion-census-denominators district-public-opinion-acs-context district-public-opinion-survey-source-crosswalk district-public-opinion-survey-item-proxy-review district-public-opinion-ces-policy-item-candidate-review district-public-opinion-ces-policy-item-response-distribution-review district-public-opinion-ces-policy-item-codebook-direction-review district-public-opinion-bill-topic-support voteview-member-context voteview-bill-linkage lobbying-issue-linkage lobbying-bill-policy-context raw-source-manifest
	python3 scripts/validation/write_bill_finance_lobbying_source_acquisition_queue.py
	python3 scripts/validation/write_empirical_linkage_report.py
	python3 scripts/validation/write_empirical_linkage_roadmap.py
	python3 scripts/validation/write_validation_gap_report.py

empirical-boundary-check: validation-gap-report empirical-linkage-report empirical-linkage-roadmap govinfo-billstatus-linkage sponsor-bill-linkage court-law-linkage rulemaking-authority-linkage rulemaking-history-linkage rulemaking-comment-metadata rulemaking-comment-records rulemaking-comment-text-review statutory-lineage-adjudication statutory-lineage-target-review-packets statutory-lineage-target-section-diff-review statutory-lineage-no-target-review bill-law-evidence-spine bill-law-lifecycle-readiness court-public-law-review-queue court-public-law-temporal-triage court-public-law-direct-review bill-law-lifecycle-next-actions bill-law-lifecycle-corpus bill-finance-lobbying-review-queue bill-finance-lobbying-local-context-review bill-finance-lobbying-external-search-review bill-finance-lobbying-external-lda-mention-review bill-finance-lobbying-campaign-finance-target-scope-review bill-finance-lobbying-committee-action-context bill-finance-lobbying-source-acquisition-queue bill-finance-lobbying-roll-call-source-review bill-finance-lobbying-member-vote-target-review lobbying-bill-mention-review lobbying-bill-action-context lobbying-bill-text-review lobbying-bill-disposition-review lobbying-bill-manual-disposition-review lobbying-bill-medium-disposition-packets lobbying-bill-medium-directional-packet-review lobbying-bill-medium-position-activity-packet-review statutory-lineage-target-lifecycle-bridge statutory-lineage-review-queue statutory-lineage-source-scan statutory-lineage-target-section-triage statutory-lineage-olrc-current-scan statutory-lineage-olrc-historical-scan statutory-lineage-olrc-annual-text-diff statutory-lineage-codified-progress statutory-lineage-effective-text-review statutory-lineage-public-law-attribution-review statutory-lineage-completion-queue statutory-lineage-complete-lineage-expansion-queue statutory-lineage-target-packet-expansion-queue statutory-lineage-target-packet-source-gap-queue statutory-lineage-target-packet-source-gap-review statutory-lineage-target-reference-resolution-candidates campaign-finance-district-context campaign-finance-member-context campaign-finance-issue-context campaign-finance-sponsor-bill-context district-public-opinion-policy-context district-public-opinion-bill-topic-readiness district-public-opinion-source-packets district-public-opinion-census-denominators district-public-opinion-acs-context district-public-opinion-survey-source-crosswalk district-public-opinion-survey-item-proxy-review district-public-opinion-ces-policy-item-candidate-review district-public-opinion-ces-policy-item-response-distribution-review district-public-opinion-ces-policy-item-codebook-direction-review district-public-opinion-bill-topic-support voteview-member-context voteview-bill-linkage lobbying-issue-linkage lobbying-bill-policy-context raw-source-manifest
	python3 scripts/checks/check_empirical_boundary.py
	python3 scripts/checks/check_govinfo_bill_census.py

fetch-validation-samples:
	python3 scripts/validation/fetch_public_api_samples.py $(ARGS)

build-bill-progression-raw:
	python3 scripts/validation/build_bill_progression_dataset.py $(ARGS)

build-govinfo-bill-census-raw:
	python3 scripts/validation/build_govinfo_bill_census_dataset.py $(ARGS)

build-govinfo-executive-action-panel-raw:
	python3 scripts/validation/build_govinfo_executive_action_panel.py $(ARGS)

build-govinfo-joint-resolution-panel-raw:
	python3 scripts/validation/build_govinfo_executive_action_panel.py --bill-types hjres,sjres --veto-reference data/validation/reference/senate_joint_resolution_veto_reference_108_118.csv --output data/validation/raw/govinfo_joint_resolution_panel.csv --metadata-output data/validation/raw/govinfo_joint_resolution_panel.metadata.md $(ARGS)

build-govinfo-final-chamber-vote-panel-raw:
	python3 scripts/validation/build_govinfo_final_vote_panel.py $(ARGS)

build-govinfo-bill-census-116-raw:
	python3 scripts/validation/build_govinfo_bill_census_dataset.py --congress 116 --output data/validation/raw/govinfo_bill_census_116.csv --metadata-output data/validation/raw/govinfo_bill_census_116.metadata.md $(ARGS)

build-govinfo-bill-census-118-raw:
	python3 scripts/validation/build_govinfo_bill_census_dataset.py --congress 118 --output data/validation/raw/govinfo_bill_census_118.csv --metadata-output data/validation/raw/govinfo_bill_census_118.metadata.md $(ARGS)

build-govinfo-billstatus-linkage-raw:
	python3 scripts/validation/build_govinfo_billstatus_linkage_dataset.py $(ARGS)

build-core-raw-validation:
	python3 scripts/validation/build_core_raw_validation_datasets.py $(ARGS)

build-sponsor-bill-linkage-raw:
	python3 scripts/validation/build_sponsor_bill_linkage_dataset.py $(ARGS)

build-voteview-member-context-raw:
	python3 scripts/validation/build_voteview_member_context_dataset.py $(ARGS)

build-voteview-bill-linkage-raw:
	python3 scripts/validation/build_voteview_bill_linkage_dataset.py $(ARGS)

build-lobbying-issue-linkage-raw:
	python3 scripts/validation/build_lobbying_issue_linkage_dataset.py $(ARGS)

build-lobbying-bill-mentions-raw:
	python3 scripts/validation/build_lobbying_bill_mention_dataset.py $(ARGS)

build-bill-finance-lobbying-external-lda-search-raw:
	python3 scripts/validation/build_bill_finance_lobbying_external_lda_search_dataset.py $(ARGS)

build-bill-finance-lobbying-committee-action-source-raw: bill-finance-lobbying-committee-action-context
	python3 scripts/validation/build_bill_finance_lobbying_committee_action_source_dataset.py $(ARGS)

build-bill-finance-lobbying-roll-call-source-raw: bill-finance-lobbying-committee-action-source-review
	python3 scripts/validation/build_bill_finance_lobbying_roll_call_source_dataset.py $(ARGS)

build-bill-finance-lobbying-member-vote-target-raw: bill-finance-lobbying-roll-call-source-review bill-finance-lobbying-campaign-finance-target-scope-review campaign-finance-member-context
	python3 scripts/validation/build_bill_finance_lobbying_member_vote_target_dataset.py $(ARGS)

build-campaign-finance-raw:
	python3 scripts/validation/build_campaign_finance_dataset.py $(ARGS)

build-campaign-finance-linkage-raw:
	python3 scripts/validation/build_campaign_finance_linkage_dataset.py $(ARGS)

build-campaign-finance-member-context-raw:
	python3 scripts/validation/build_campaign_finance_member_context_dataset.py $(ARGS)

build-campaign-finance-issue-context-raw:
	python3 scripts/validation/build_campaign_finance_issue_context_dataset.py $(ARGS)

build-district-public-opinion-raw:
	python3 scripts/validation/build_district_public_opinion_dataset.py $(ARGS)

build-district-public-opinion-linkage-raw:
	python3 scripts/validation/build_district_public_opinion_linkage_dataset.py $(ARGS)

build-district-public-opinion-policy-context-raw:
	python3 scripts/validation/build_district_public_opinion_policy_context_dataset.py $(ARGS)

build-district-public-opinion-census-denominators-raw: district-public-opinion-source-packets
	python3 scripts/validation/build_district_public_opinion_census_denominator_dataset.py $(ARGS)

build-district-public-opinion-acs-context-raw: district-public-opinion-source-packets
	python3 scripts/validation/build_district_public_opinion_acs_context_dataset.py $(ARGS)

build-court-review-raw:
	python3 scripts/validation/build_court_review_dataset.py $(ARGS)

build-court-law-linkage-raw:
	python3 scripts/validation/build_court_law_linkage_dataset.py $(ARGS)

build-rulemaking-implementation-raw:
	python3 scripts/validation/build_rulemaking_implementation_dataset.py $(ARGS)

build-rulemaking-implementation-linkage-raw:
	python3 scripts/validation/build_rulemaking_implementation_linkage_dataset.py $(ARGS)

build-rulemaking-authority-linkage-raw:
	python3 scripts/validation/build_rulemaking_authority_linkage_dataset.py $(ARGS)

build-rulemaking-history-linkage-raw:
	python3 scripts/validation/build_rulemaking_history_linkage_dataset.py $(ARGS)

build-rulemaking-comment-metadata-raw: rulemaking-history-linkage
	python3 scripts/validation/build_rulemaking_comment_metadata_dataset.py $(ARGS)

build-rulemaking-comment-records-raw: rulemaking-comment-metadata
	python3 scripts/validation/build_rulemaking_comment_records_dataset.py $(ARGS)

build-rulemaking-comment-text-review-raw: rulemaking-comment-records
	python3 scripts/validation/build_rulemaking_comment_text_review_dataset.py $(ARGS)

build-law-revision-raw:
	python3 scripts/validation/build_law_revision_history_dataset.py $(ARGS)

build-law-revision-bill-linkage-raw:
	python3 scripts/validation/build_law_revision_bill_linkage_dataset.py $(ARGS)

build-statutory-lineage-source-scan-raw: statutory-lineage-review-queue
	python3 scripts/validation/build_statutory_lineage_source_scan_dataset.py $(ARGS)

build-statutory-lineage-no-target-review-raw: statutory-lineage-source-scan
	python3 scripts/validation/build_statutory_lineage_no_target_review_dataset.py

build-statutory-lineage-olrc-current-scan-raw: statutory-lineage-target-section-triage
	python3 scripts/validation/build_statutory_lineage_olrc_current_scan_dataset.py $(ARGS)

build-statutory-lineage-olrc-historical-scan-raw: statutory-lineage-olrc-current-scan
	python3 scripts/validation/build_statutory_lineage_olrc_historical_scan_dataset.py $(ARGS)

build-statutory-lineage-olrc-annual-text-diff-raw: statutory-lineage-olrc-historical-scan
	python3 scripts/validation/build_statutory_lineage_olrc_annual_text_diff_dataset.py $(ARGS)

build-statutory-lineage-adjudication-raw: statutory-lineage-olrc-annual-text-diff
	python3 scripts/validation/build_statutory_lineage_adjudication_dataset.py $(ARGS)

build-statutory-lineage-target-review-packets-raw: statutory-lineage-adjudication
	python3 scripts/validation/build_statutory_lineage_target_review_packet_dataset.py $(ARGS)

build-statutory-lineage-target-section-diff-review-raw: build-statutory-lineage-target-review-packets-raw
	python3 scripts/validation/build_statutory_lineage_target_section_diff_review_dataset.py

build-comparative-institutions-raw:
	python3 scripts/validation/build_comparative_institutions_dataset.py $(ARGS)

build-comparative-institution-linkage-raw:
	python3 scripts/validation/build_comparative_institution_linkage_dataset.py $(ARGS)

empirical-validation:
	python3 scripts/validation/run_empirical_validation.py

empirical-bridge: empirical-validation
	python3 scripts/validation/run_empirical_bridge.py

empirical-flow-heldout:
	python3 scripts/validation/run_empirical_flow_heldout.py

empirical-data-inventory: validation-readiness empirical-bridge empirical-flow-heldout
	python3 scripts/validation/write_empirical_data_inventory.py

empirical-linkage-report: empirical-data-inventory sponsor-bill-linkage court-law-linkage comparative-institution-linkage campaign-finance-issue-context campaign-finance-sponsor-bill-context district-public-opinion-policy-context lobbying-bill-policy-context statutory-lineage-target-section-diff-review
	python3 scripts/validation/write_empirical_linkage_report.py

empirical-linkage-roadmap: empirical-linkage-report
	python3 scripts/validation/write_empirical_linkage_roadmap.py

govinfo-billstatus-linkage: empirical-linkage-report
	python3 scripts/validation/write_govinfo_billstatus_linkage_report.py

govinfo-bill-census:
	python3 scripts/validation/write_govinfo_bill_census_report.py

govinfo-bill-census-116:
	python3 scripts/validation/write_govinfo_bill_census_116_report.py

govinfo-bill-census-118:
	python3 scripts/validation/write_govinfo_bill_census_118_report.py

govinfo-executive-action-panel:
	python3 scripts/validation/build_govinfo_executive_action_panel.py --offline

govinfo-joint-resolution-panel:
	python3 scripts/validation/build_govinfo_executive_action_panel.py --bill-types hjres,sjres --veto-reference data/validation/reference/senate_joint_resolution_veto_reference_108_118.csv --output data/validation/raw/govinfo_joint_resolution_panel.csv --metadata-output data/validation/raw/govinfo_joint_resolution_panel.metadata.md --offline

govinfo-final-chamber-vote-panel:
	python3 scripts/validation/build_govinfo_final_vote_panel.py --offline

legislative-lifecycle-calibration: build govinfo-bill-census
	APP_CP="$(APP_CP)" JAVA_PROPS="$(JAVA_PROPS)" python3 scripts/validation/write_legislative_lifecycle_calibration.py

legislative-executive-action-diagnostic: legislative-lifecycle-calibration govinfo-executive-action-panel govinfo-joint-resolution-panel govinfo-final-chamber-vote-panel
	python3 scripts/validation/write_legislative_executive_action_diagnostic.py

legislative-lifecycle-temporal-replication: legislative-executive-action-diagnostic
	python3 scripts/validation/write_legislative_lifecycle_temporal_replication.py

govinfo-bill-census-check: legislative-lifecycle-temporal-replication
	python3 scripts/checks/check_govinfo_bill_census.py

sponsor-bill-linkage:
	python3 scripts/validation/write_sponsor_bill_linkage_report.py

court-law-linkage:
	python3 scripts/validation/write_court_law_linkage_report.py

comparative-institution-linkage:
	python3 scripts/validation/write_comparative_institution_linkage_report.py

rulemaking-authority-linkage: empirical-linkage-report
	python3 scripts/validation/write_rulemaking_authority_linkage_report.py

rulemaking-history-linkage: rulemaking-authority-linkage
	python3 scripts/validation/write_rulemaking_history_linkage_report.py

rulemaking-comment-metadata: rulemaking-history-linkage
	python3 scripts/validation/write_rulemaking_comment_metadata_report.py

rulemaking-comment-records: rulemaking-comment-metadata
	python3 scripts/validation/write_rulemaking_comment_records_report.py

rulemaking-comment-text-review: rulemaking-comment-records
	python3 scripts/validation/write_rulemaking_comment_text_review_report.py

bill-law-evidence-spine: empirical-linkage-report court-law-linkage rulemaking-authority-linkage rulemaking-history-linkage rulemaking-comment-metadata rulemaking-comment-records statutory-lineage-target-section-diff-review
	python3 scripts/validation/write_bill_law_evidence_spine.py

bill-law-lifecycle-readiness: bill-law-evidence-spine
	python3 scripts/validation/write_bill_law_lifecycle_readiness.py

court-public-law-review-queue: court-law-linkage bill-law-lifecycle-readiness
	python3 scripts/validation/write_court_public_law_review_queue.py

court-public-law-temporal-triage: court-public-law-review-queue bill-law-evidence-spine
	python3 scripts/validation/write_court_public_law_temporal_triage.py

court-public-law-direct-review: court-public-law-temporal-triage
	python3 scripts/validation/write_court_public_law_direct_review_report.py
	python3 scripts/validation/write_bill_law_lifecycle_readiness.py

bill-law-lifecycle-next-actions: bill-law-lifecycle-readiness court-public-law-direct-review
	python3 scripts/validation/write_bill_law_lifecycle_next_actions.py

bill-law-lifecycle-corpus: bill-law-lifecycle-next-actions bill-law-evidence-spine court-public-law-direct-review district-public-opinion-survey-item-proxy-review district-public-opinion-bill-topic-support bill-finance-lobbying-local-context-review bill-finance-lobbying-external-search-review bill-finance-lobbying-external-lda-mention-review bill-finance-lobbying-campaign-finance-target-scope-review statutory-lineage-codified-progress statutory-lineage-target-lifecycle-bridge rulemaking-comment-text-review
	python3 scripts/validation/write_bill_law_lifecycle_corpus.py

bill-finance-lobbying-review-queue: bill-law-lifecycle-next-actions bill-law-evidence-spine campaign-finance-sponsor-bill-context lobbying-bill-policy-context
	python3 scripts/validation/write_bill_finance_lobbying_review_queue.py

bill-finance-lobbying-local-context-review: bill-finance-lobbying-review-queue
	python3 scripts/validation/write_bill_finance_lobbying_local_context_review.py

bill-finance-lobbying-external-search-review: bill-finance-lobbying-local-context-review
	python3 scripts/validation/write_bill_finance_lobbying_external_search_review.py

bill-finance-lobbying-external-lda-mention-review: bill-finance-lobbying-external-search-review
	python3 scripts/validation/write_bill_finance_lobbying_external_lda_mention_review.py

bill-finance-lobbying-campaign-finance-target-scope-review: bill-finance-lobbying-external-search-review campaign-finance-sponsor-bill-context campaign-finance-member-context campaign-finance-district-context campaign-finance-issue-context
	python3 scripts/validation/write_bill_finance_lobbying_campaign_finance_target_scope_review.py

bill-finance-lobbying-committee-action-context: bill-finance-lobbying-external-lda-mention-review bill-finance-lobbying-campaign-finance-target-scope-review
	python3 scripts/validation/write_bill_finance_lobbying_committee_action_context.py

bill-finance-lobbying-committee-action-source-review: bill-finance-lobbying-committee-action-context
	python3 scripts/validation/write_bill_finance_lobbying_committee_action_source_review.py

bill-finance-lobbying-roll-call-source-review: bill-finance-lobbying-committee-action-source-review
	python3 scripts/validation/write_bill_finance_lobbying_roll_call_source_review.py

bill-finance-lobbying-member-vote-target-review: build-bill-finance-lobbying-member-vote-target-raw
	python3 scripts/validation/write_bill_finance_lobbying_member_vote_target_review.py

bill-finance-lobbying-source-acquisition-queue: bill-finance-lobbying-committee-action-context bill-finance-lobbying-committee-action-source-review bill-finance-lobbying-roll-call-source-review bill-finance-lobbying-member-vote-target-review govinfo-billstatus-linkage voteview-bill-linkage
	python3 scripts/validation/write_bill_finance_lobbying_source_acquisition_queue.py

statutory-lineage-review-queue: bill-law-lifecycle-next-actions
	python3 scripts/validation/write_statutory_lineage_review_queue.py

statutory-lineage-source-scan: statutory-lineage-review-queue
	python3 scripts/validation/write_statutory_lineage_source_scan_report.py

statutory-lineage-no-target-review: build-statutory-lineage-no-target-review-raw
	python3 scripts/validation/write_statutory_lineage_no_target_review_report.py

statutory-lineage-target-section-triage: statutory-lineage-source-scan
	python3 scripts/validation/write_statutory_lineage_target_section_triage.py

statutory-lineage-olrc-current-scan: statutory-lineage-target-section-triage
	python3 scripts/validation/write_statutory_lineage_olrc_current_scan_report.py

statutory-lineage-olrc-historical-scan: statutory-lineage-olrc-current-scan
	python3 scripts/validation/write_statutory_lineage_olrc_historical_scan_report.py

statutory-lineage-olrc-annual-text-diff: statutory-lineage-olrc-historical-scan
	python3 scripts/validation/write_statutory_lineage_olrc_annual_text_diff_report.py

statutory-lineage-adjudication:
	python3 scripts/validation/write_statutory_lineage_adjudication_report.py

statutory-lineage-target-review-packets: build-statutory-lineage-target-review-packets-raw build-statutory-lineage-target-section-diff-review-raw
	python3 scripts/validation/write_statutory_lineage_target_review_packet_report.py

statutory-lineage-target-section-diff-review: statutory-lineage-target-review-packets
	python3 scripts/validation/write_statutory_lineage_target_section_diff_review_report.py

statutory-lineage-target-lifecycle-bridge: statutory-lineage-target-section-diff-review bill-law-evidence-spine court-public-law-direct-review
	python3 scripts/validation/write_statutory_lineage_target_lifecycle_bridge.py

statutory-lineage-codified-progress: bill-law-lifecycle-next-actions statutory-lineage-source-scan statutory-lineage-no-target-review statutory-lineage-target-section-triage statutory-lineage-target-section-diff-review statutory-lineage-target-lifecycle-bridge
	python3 scripts/validation/write_statutory_lineage_codified_progress.py

statutory-lineage-effective-text-review: statutory-lineage-target-section-diff-review statutory-lineage-olrc-current-scan statutory-lineage-olrc-annual-text-diff
	python3 scripts/validation/write_statutory_lineage_effective_text_review.py

statutory-lineage-public-law-attribution-review: statutory-lineage-target-section-diff-review statutory-lineage-effective-text-review statutory-lineage-olrc-annual-text-diff statutory-lineage-source-scan
	python3 scripts/validation/write_statutory_lineage_public_law_attribution_review.py

statutory-lineage-completion-queue: bill-law-lifecycle-corpus statutory-lineage-codified-progress statutory-lineage-target-section-diff-review statutory-lineage-target-lifecycle-bridge statutory-lineage-effective-text-review statutory-lineage-public-law-attribution-review
	python3 scripts/validation/write_statutory_lineage_completion_queue.py

statutory-lineage-complete-lineage-expansion-queue: statutory-lineage-completion-queue statutory-lineage-source-scan statutory-lineage-target-section-triage statutory-lineage-target-review-packets statutory-lineage-target-section-diff-review statutory-lineage-effective-text-review statutory-lineage-public-law-attribution-review
	python3 scripts/validation/write_statutory_lineage_complete_lineage_expansion_queue.py

statutory-lineage-target-packet-expansion-queue: statutory-lineage-complete-lineage-expansion-queue statutory-lineage-source-scan statutory-lineage-target-section-triage statutory-lineage-target-review-packets
	python3 scripts/validation/write_statutory_lineage_target_packet_expansion_queue.py

statutory-lineage-target-packet-source-gap-queue: statutory-lineage-target-packet-expansion-queue statutory-lineage-olrc-current-scan statutory-lineage-olrc-historical-scan statutory-lineage-olrc-annual-text-diff statutory-lineage-adjudication statutory-lineage-target-review-packets
	python3 scripts/validation/write_statutory_lineage_target_packet_source_gap_queue.py

statutory-lineage-target-packet-source-gap-review: statutory-lineage-target-packet-source-gap-queue
	python3 scripts/validation/write_statutory_lineage_target_packet_source_gap_review.py

statutory-lineage-target-reference-resolution-candidates: statutory-lineage-target-packet-source-gap-queue statutory-lineage-source-scan
	python3 scripts/validation/write_statutory_lineage_target_reference_resolution_candidates.py

campaign-finance-district-context: empirical-linkage-report
	python3 scripts/validation/write_campaign_finance_district_context.py

campaign-finance-member-context: empirical-linkage-report
	python3 scripts/validation/write_campaign_finance_member_context_report.py

campaign-finance-issue-context:
	python3 scripts/validation/write_campaign_finance_issue_context_report.py

campaign-finance-sponsor-bill-context:
	python3 scripts/validation/write_campaign_finance_sponsor_bill_context_report.py

district-public-opinion-policy-context:
	python3 scripts/validation/write_district_public_opinion_policy_context_report.py

district-public-opinion-bill-topic-readiness: district-public-opinion-policy-context bill-law-lifecycle-next-actions
	python3 scripts/validation/write_district_public_opinion_bill_topic_readiness.py

district-public-opinion-source-packets: district-public-opinion-bill-topic-readiness
	python3 scripts/validation/write_district_public_opinion_source_packets.py

district-public-opinion-census-denominators: build-district-public-opinion-census-denominators-raw district-public-opinion-source-packets
	python3 scripts/validation/write_district_public_opinion_census_denominator_report.py

district-public-opinion-acs-context: build-district-public-opinion-acs-context-raw district-public-opinion-source-packets district-public-opinion-census-denominators
	python3 scripts/validation/write_district_public_opinion_acs_context_report.py

district-public-opinion-survey-source-crosswalk: district-public-opinion-source-packets district-public-opinion-census-denominators district-public-opinion-acs-context
	python3 scripts/validation/write_district_public_opinion_survey_source_crosswalk.py

district-public-opinion-survey-item-proxy-review: district-public-opinion-survey-source-crosswalk
	python3 scripts/validation/write_district_public_opinion_survey_item_proxy_review.py

build-district-public-opinion-ces-policy-item-candidates-raw:
	python3 scripts/validation/build_district_public_opinion_ces_policy_item_candidate_dataset.py $(ARGS)

district-public-opinion-ces-policy-item-candidate-review: district-public-opinion-survey-source-crosswalk build-district-public-opinion-ces-policy-item-candidates-raw
	python3 scripts/validation/write_district_public_opinion_ces_policy_item_candidate_review.py

build-district-public-opinion-ces-policy-item-response-distributions-raw: build-district-public-opinion-ces-policy-item-candidates-raw
	python3 scripts/validation/build_district_public_opinion_ces_policy_item_response_distribution_dataset.py

district-public-opinion-ces-policy-item-response-distribution-review: district-public-opinion-ces-policy-item-candidate-review build-district-public-opinion-ces-policy-item-response-distributions-raw
	python3 scripts/validation/write_district_public_opinion_ces_policy_item_response_distribution_review.py

build-district-public-opinion-ces-policy-item-codebook-direction-raw: build-district-public-opinion-ces-policy-item-response-distributions-raw
	python3 scripts/validation/build_district_public_opinion_ces_policy_item_codebook_direction_dataset.py

district-public-opinion-ces-policy-item-codebook-direction-review: district-public-opinion-ces-policy-item-response-distribution-review build-district-public-opinion-ces-policy-item-codebook-direction-raw
	python3 scripts/validation/write_district_public_opinion_ces_policy_item_codebook_direction_review.py

build-district-public-opinion-bill-text-context-raw: district-public-opinion-source-packets
	python3 scripts/validation/build_district_public_opinion_bill_text_context_dataset.py $(ARGS)

district-public-opinion-bill-item-alignment-review: build-district-public-opinion-bill-text-context-raw district-public-opinion-ces-policy-item-codebook-direction-review
	python3 scripts/validation/write_district_public_opinion_bill_item_alignment_review.py

build-district-public-opinion-bill-topic-support-raw: district-public-opinion-bill-item-alignment-review
	python3 scripts/validation/build_district_public_opinion_bill_topic_support_dataset.py $(ARGS)

district-public-opinion-bill-topic-support: build-district-public-opinion-bill-topic-support-raw
	python3 scripts/validation/write_district_public_opinion_bill_topic_support_report.py
	python3 scripts/validation/write_district_public_opinion_bill_item_alignment_review.py
	python3 scripts/validation/write_district_public_opinion_bill_topic_readiness.py
	python3 scripts/validation/write_district_public_opinion_source_packets.py

district-public-opinion-ces-source-freshness:
	python3 scripts/validation/write_district_public_opinion_ces_source_freshness.py

voteview-member-context: empirical-linkage-report
	python3 scripts/validation/write_voteview_member_context_report.py

voteview-bill-linkage: empirical-linkage-report
	python3 scripts/validation/write_voteview_bill_linkage_report.py

lobbying-issue-linkage: empirical-linkage-report
	python3 scripts/validation/write_lobbying_issue_linkage_report.py

lobbying-bill-policy-context:
	python3 scripts/validation/write_lobbying_bill_policy_context_report.py

lobbying-bill-mention-review: bill-finance-lobbying-review-queue
	python3 scripts/validation/write_lobbying_bill_mention_review_report.py

lobbying-bill-action-context: lobbying-bill-mention-review
	python3 scripts/validation/write_lobbying_bill_action_context_report.py

lobbying-bill-text-review: lobbying-bill-action-context
	python3 scripts/validation/write_lobbying_bill_text_review_report.py

lobbying-bill-disposition-review: lobbying-bill-text-review
	python3 scripts/validation/write_lobbying_bill_disposition_review.py

lobbying-bill-manual-disposition-review: lobbying-bill-disposition-review
	python3 scripts/validation/write_lobbying_bill_manual_disposition_review.py

lobbying-bill-medium-disposition-packets: lobbying-bill-disposition-review
	python3 scripts/validation/write_lobbying_bill_medium_disposition_packets.py

lobbying-bill-medium-directional-packet-review: lobbying-bill-medium-disposition-packets
	python3 scripts/validation/write_lobbying_bill_medium_directional_packet_review.py

lobbying-bill-medium-position-activity-packet-review: lobbying-bill-medium-disposition-packets
	python3 scripts/validation/write_lobbying_bill_medium_position_activity_packet_review.py

raw-source-manifest:
	python3 scripts/validation/write_raw_source_manifest.py

ablation-analysis: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign ablation-analysis --runs 64 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)
	python3 scripts/reporting/summarize_ablation_analysis.py

manipulation-stress: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign manipulation-stress --runs 64 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)
	python3 scripts/reporting/summarize_manipulation_stress.py

failure-trace-report: manipulation-stress
	python3 scripts/reporting/write_adversarial_failure_trace_index.py

adversary-catalog: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.AdversaryCatalogExporter reports

adversarial-stress: adversary-catalog
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A1CloneDecoyAdversarialStressRunner reports
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A2PoisonPillAdversarialStressRunner reports
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A3PublicInputAdversarialStressRunner reports
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A4BadFaithHarmClaimAdversarialStressRunner reports
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A5ProposalFloodingAdversarialStressRunner reports
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A6LobbyingCamouflageAdversarialStressRunner reports
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A7AdministrativeOverloadAdversarialStressRunner reports
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A8PublicSupportDistortionAdversarialStressRunner reports
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.institution.adversary.A9MixedAdversaryPortfolioStressRunner reports

adversarial-pilot-cell-map: failure-trace-report adversary-catalog adversarial-stress
	python3 scripts/reporting/write_adversarial_pilot_cell_map.py

adversarial-stress-manifest: adversarial-pilot-cell-map

adversarial-replication-a1-a8: build
	APP_CP="$(APP_CP)" JAVA_PROPS="$(JAVA_PROPS)" python3 scripts/reporting/run_a1_a8_seed_replication.py

adversarial-replication-a9: build
	APP_CP="$(APP_CP)" JAVA_PROPS="$(JAVA_PROPS)" python3 scripts/reporting/run_a9_seed_replication.py

robustness-evidence: adversarial-stress-manifest adversarial-replication-a1-a8 adversarial-replication-a9

mechanism-diagnostics: empirical-bridge ablation-analysis manipulation-stress
	python3 scripts/reporting/write_paper_diagnostics.py

public-provenance:
	python3 scripts/reporting/write_public_provenance.py

paper-assets: paper-campaign family-screen mechanism-diagnostics chamber-structure validation-gap-report
	python3 paper/scripts/generate_figures.py

paper: paper-assets
	cd paper/acm-ci-framework && TEXINPUTS=..:../figures: BIBINPUTS=..: BSTINPUTS=..: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build/acm-ci-framework acm-ci-framework.tex
	cd paper/technical-appendix && TEXINPUTS=..:../figures: BIBINPUTS=..: BSTINPUTS=..: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build/technical-appendix odd-d-appendix.tex
	cp paper/build/acm-ci-framework/acm-ci-framework.pdf $(PAPER_MAIN_PDF)
	cp paper/build/technical-appendix/odd-d-appendix.pdf $(PAPER_APPENDIX_PDF)
	python3 paper/scripts/write_pdf_manifest.py

paper-word-count: paper
	python3 paper/scripts/check_word_count.py $(PAPER_MAIN_PDF) --max 6000

paper-checks: paper
	python3 paper/scripts/check_word_count.py $(PAPER_MAIN_PDF) --max 6000
	python3 scripts/checks/check_paper_anonymity.py $(PAPER_MAIN_PDF) $(PAPER_APPENDIX_PDF)
	python3 scripts/checks/check_figure_labels.py
	python3 scripts/checks/check_table_figure_consistency.py
	python3 scripts/checks/check_empirical_boundary.py
	python3 scripts/checks/check_govinfo_bill_census.py
	python3 scripts/checks/check_pdf_render.py $(PAPER_MAIN_PDF) $(PAPER_APPENDIX_PDF)
	python3 paper/scripts/write_pdf_manifest.py --check

reproduce-paper-offline: paper-checks

paper-freshness-check: paper-assets
	python3 paper/scripts/check_word_count.py $(PAPER_MAIN_PDF) --max 6000
	python3 scripts/checks/check_paper_anonymity.py $(PAPER_MAIN_PDF) $(PAPER_APPENDIX_PDF)
	python3 scripts/checks/check_figure_labels.py
	python3 scripts/checks/check_table_figure_consistency.py
	python3 scripts/checks/check_empirical_boundary.py
	python3 scripts/checks/check_govinfo_bill_census.py
	python3 scripts/checks/check_pdf_render.py $(PAPER_MAIN_PDF) $(PAPER_APPENDIX_PDF)
	python3 paper/scripts/write_pdf_manifest.py --check

paper-anonymity-check: paper
	python3 scripts/checks/check_paper_anonymity.py $(PAPER_MAIN_PDF) $(PAPER_APPENDIX_PDF)

figure-label-check: paper
	python3 scripts/checks/check_figure_labels.py

pdf-render-check: paper
	python3 scripts/checks/check_pdf_render.py $(PAPER_MAIN_PDF) $(PAPER_APPENDIX_PDF)

pdf-manifest-check: paper
	python3 paper/scripts/write_pdf_manifest.py --check

table-figure-consistency-check: paper
	python3 scripts/checks/check_table_figure_consistency.py

supplement-anonymous: paper
	python3 scripts/packaging/build_anonymous_supplement.py

supplement-anonymous-current:
	python3 scripts/packaging/build_anonymous_supplement.py

clean-regeneration-check:
	# PDF bytes vary across TeX/font environments; paper/pdf-manifest.json tracks stable PDF freshness.
	git diff --no-ext-diff --exit-code -- . ':(exclude)$(PAPER_MAIN_PDF)' ':(exclude)$(PAPER_APPENDIX_PDF)'

paper-clean:
	cd paper/acm-ci-framework && latexmk -C -outdir=../build/acm-ci-framework acm-ci-framework.tex
	cd paper/technical-appendix && latexmk -C -outdir=../build/technical-appendix odd-d-appendix.tex
	rm -rf paper/build

test: build
	mkdir -p out/test
	javac --release $(JAVA_RELEASE) -cp $(APP_CP) -d out/test $(TEST_SOURCES)
	java $(JAVA_PROPS) -cp $(APP_CP):out/test congresssim.SimulatorTests
	python3 scripts/validation/test_reproducible_metadata.py
	python3 scripts/validation/test_govinfo_bill_census.py
	python3 scripts/validation/test_govinfo_executive_action_panel.py
	python3 scripts/validation/test_govinfo_final_vote_panel.py
	python3 scripts/validation/test_district_public_opinion_census_denominator.py
	python3 scripts/validation/test_district_public_opinion_bill_text_context.py
	python3 scripts/validation/test_district_public_opinion_bill_topic_support.py
	python3 scripts/reporting/test_run_a1_a8_seed_replication.py
	python3 scripts/reporting/test_run_a9_seed_replication.py

ci: test calibration-check seed-robustness-check validation-gap-report catalog-breadth paper-checks supplement-anonymous clean-regeneration-check

github-ci: test calibration-check seed-robustness-check validation-gap-report catalog-breadth paper-freshness-check supplement-anonymous-current clean-regeneration-check

clean:
	rm -rf out
