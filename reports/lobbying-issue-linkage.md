# Lobbying Issue Linkage

This report derives a bounded issue-taxonomy bridge from cached Senate LDA issue labels to cached Congress.gov policy-area topic aggregates. It is issue context, not bill-level lobbying validation.

- LDA issue labels represented: 48
- LDA activity rows represented: 146
- LDA activity rows with issue-topic context: 144
- Sum of issue-level unique-client counts: 142
- Issue-level disclosed amount represented: 45000.00

Claim boundary: this report links public LDA issue labels to broad local policy-area topic labels. It does not link lobbying clients to bills, sponsors, committees, roll calls, legislative outcomes, public benefit, welfare, causal capture, or model validation.

Linkage statuses:
- issue_topic_crosswalk: 47
- unmatched_issue: 1

Mapped topics:
- Agriculture and Food: 2
- Armed Forces and National Security: 4
- Commerce: 9
- Crime and Law Enforcement: 1
- Economics and Public Finance: 2
- Education: 1
- Emergency Management: 1
- Energy: 3
- Environmental Protection: 2
- Finance and Financial Sector: 3
- Government Operations and Politics: 1
- Health: 3
- Housing and Community Development: 1
- International Affairs: 1
- Native Americans: 1
- Public Lands and Natural Resources: 1
- Science, Technology, Communications: 4
- Social Welfare: 1
- Taxation: 1
- Transportation and Public Works: 5

| LDA issue | Topic | Status | LDA rows | Clients | Amount | Missing links |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Budget/Appropriations | Economics and Public Finance | issue_topic_crosswalk | 22 | 21 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Defense | Armed Forces and National Security | issue_topic_crosswalk | 10 | 10 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Taxation/Internal Revenue Code | Taxation | issue_topic_crosswalk | 9 | 9 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Health Issues | Health | issue_topic_crosswalk | 7 | 7 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Financial Institutions/Investments/Securities | Finance and Financial Sector | issue_topic_crosswalk | 6 | 6 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Science/Technology | Science, Technology, Communications | issue_topic_crosswalk | 6 | 6 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Agriculture | Agriculture and Food | issue_topic_crosswalk | 5 | 5 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Manufacturing | Commerce | issue_topic_crosswalk | 5 | 4 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Economics/Economic Development | Economics and Public Finance | issue_topic_crosswalk | 4 | 4 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Education | Education | issue_topic_crosswalk | 4 | 4 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Energy/Nuclear | Energy | issue_topic_crosswalk | 4 | 4 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Environment/Superfund | Environmental Protection | issue_topic_crosswalk | 4 | 4 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Natural Resources | Public Lands and Natural Resources | issue_topic_crosswalk | 4 | 4 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Trade (domestic/foreign) | Commerce | issue_topic_crosswalk | 4 | 4 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Transportation | Transportation and Public Works | issue_topic_crosswalk | 4 | 4 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Consumer Issues/Safety/Products | Commerce | issue_topic_crosswalk | 3 | 3 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Government Issues | Government Operations and Politics | issue_topic_crosswalk | 3 | 2 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Medicare/Medicaid | Health | issue_topic_crosswalk | 3 | 3 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Telecommunications | Science, Technology, Communications | issue_topic_crosswalk | 3 | 3 | 30000.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Automotive Industry | Commerce | issue_topic_crosswalk | 2 | 2 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Chemicals/Chemical Industry | Commerce | issue_topic_crosswalk | 2 | 2 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Food Industry (safety, labeling, etc.) | Agriculture and Food | issue_topic_crosswalk | 2 | 2 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Law Enforcement/Crime/Criminal Justice | Crime and Law Enforcement | issue_topic_crosswalk | 2 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Media (information/publishing) | Science, Technology, Communications | issue_topic_crosswalk | 2 | 2 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Roads/Highway | Transportation and Public Works | issue_topic_crosswalk | 2 | 2 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Uncoded | --- | unmatched_issue | 2 | 2 | 0.00 | topic_policy_area; bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Aerospace | Armed Forces and National Security | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Aviation/Airlines/Airports | Transportation and Public Works | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Banking | Finance and Financial Sector | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Beverage Industry | Commerce | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Clean Air and Water (quality) | Environmental Protection | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Computer Industry | Science, Technology, Communications | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Disaster Planning/Emergencies | Emergency Management | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Foreign Relations | International Affairs | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Fuel/Gas/Oil | Energy | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Housing | Housing and Community Development | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Indian/Native American Affairs | Native Americans | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Insurance | Finance and Financial Sector | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Intelligence | Armed Forces and National Security | issue_topic_crosswalk | 1 | 1 | 15000.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Marine/Maritime/Boating/Fisheries | Transportation and Public Works | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Pharmacy | Health | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Railroads | Transportation and Public Works | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Small Business | Commerce | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Tobacco | Commerce | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Travel/Tourism | Commerce | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Utilities | Energy | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Veterans | Armed Forces and National Security | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
| Welfare | Social Welfare | issue_topic_crosswalk | 1 | 1 | 0.00 | bill_id; sponsor_or_member_id; committee_of_jurisdiction; legislative_outcome; causal_capture_validation; model_validation |
