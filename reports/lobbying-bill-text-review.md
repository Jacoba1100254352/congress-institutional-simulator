# LDA Bill Text Review

This report reviews the official LDA activity text for rows that already contain exact current-bill identifiers. It classifies text signals in the activity description; it is not evidence that lobbying changed any committee, roll-call, or enactment outcome.

- Cached exact LDA activity-text match rows represented: 484
- Rows with bill reference located in stored activity text: 484
- Rows needing full activity-text refetch before text review: 0
- Public-law bill IDs represented: 26
- Unique LDA filing IDs represented: 404
- Unique LDA clients represented: 220
- Rows with explicit support text signal: 46
- Rows with explicit opposition text signal: 3
- Rows with mixed support/opposition text signal: 2
- Rows with position/activity text signal but no direction: 104
- Rows with bill-list or title-only text: 329
- Rows with disclosed House or Senate entity context: 474

Claim boundary: Official LDA activity-text review for exact bill mentions only; support, opposition, position, or bill-list text signals describe phrases in the disclosed filing text and do not show sponsor/member targeting, committee-action influence, roll-call influence, legislative-outcome causality, public benefit, welfare, causal capture, or model validation.

Text review statuses:
- exact_bill_text_bill_list_or_title_only: 329
- exact_bill_text_with_explicit_opposition_signal: 3
- exact_bill_text_with_explicit_support_signal: 46
- exact_bill_text_with_mixed_support_opposition_signal: 2
- exact_bill_text_with_position_or_activity_signal: 104

| Bill | Public law | Policy area | Rows | Visible refs | Needs refetch | Clients | Support rows | Opposition rows | Position rows | List-only rows | Possible member/committee refs |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `117-hr-5376` | `117-169` | Economics and Public Finance | 55 | 55 | 0 | 37 | 5 | 1 | 23 | 26 | 0 |
| `117-s-516` | `117-203` | Transportation and Public Works | 40 | 40 | 0 | 12 | 1 | 0 | 1 | 38 | 0 |
| `117-hr-4346` | `117-167` | Science, Technology, Communications | 39 | 39 | 0 | 22 | 2 | 0 | 4 | 33 | 0 |
| `117-s-558` | `117-316` | Public Lands and Natural Resources | 39 | 39 | 0 | 7 | 2 | 0 | 6 | 31 | 0 |
| `117-s-270` | `117-123` | Public Lands and Natural Resources | 28 | 28 | 0 | 2 | 0 | 0 | 0 | 28 | 0 |
| `117-hr-1437` | `117-229` | Economics and Public Finance | 27 | 27 | 0 | 6 | 8 | 0 | 12 | 7 | 0 |
| `117-s-2089` | `117-158` | Agriculture and Food | 26 | 26 | 0 | 13 | 3 | 0 | 0 | 23 | 0 |
| `117-hr-6833` | `117-180` | Economics and Public Finance | 25 | 25 | 0 | 20 | 0 | 0 | 14 | 11 | 0 |
| `117-hr-7776` | `117-263` | Armed Forces and National Security | 25 | 25 | 0 | 24 | 3 | 1 | 4 | 17 | 1 |
| `117-s-4900` | `117-183` | Commerce | 25 | 25 | 0 | 24 | 2 | 0 | 3 | 20 | 1 |
| `117-s-3580` | `117-146` | Transportation and Public Works | 24 | 24 | 0 | 22 | 2 | 1 | 11 | 10 | 0 |
| `117-s-3373` | `117-168` | Armed Forces and National Security | 23 | 23 | 0 | 14 | 7 | 0 | 3 | 11 | 0 |
| `117-hr-1652` | `117-27` | Crime and Law Enforcement | 13 | 13 | 0 | 4 | 0 | 0 | 1 | 12 | 0 |
| `117-hr-3113` | `117-114` | Public Lands and Natural Resources | 12 | 12 | 0 | 4 | 0 | 0 | 0 | 12 | 0 |
| `117-s-2520` | `117-150` | Emergency Management | 12 | 12 | 0 | 4 | 8 | 0 | 0 | 4 | 0 |
| `117-s-4458` | `117-174` | Armed Forces and National Security | 12 | 12 | 0 | 7 | 0 | 0 | 3 | 9 | 0 |
| `117-hr-8404` | `117-228` | Civil Rights and Liberties, Minority Issues | 9 | 9 | 0 | 5 | 2 | 0 | 2 | 5 | 0 |
| `117-hr-8454` | `117-215` | Crime and Law Enforcement | 8 | 8 | 0 | 6 | 1 | 0 | 2 | 5 | 0 |
| `117-s-2687` | `117-136` | Armed Forces and National Security | 7 | 7 | 0 | 2 | 0 | 0 | 2 | 5 | 0 |
| `117-hr-2472` | `117-269` | Government Operations and Politics | 6 | 6 | 0 | 1 | 0 | 0 | 6 | 0 | 0 |
| `117-hr-6943` | `117-172` | Crime and Law Enforcement | 6 | 6 | 0 | 2 | 0 | 0 | 0 | 6 | 0 |
| `117-s-233` | `117-115` | Government Operations and Politics | 6 | 6 | 0 | 1 | 0 | 0 | 6 | 0 | 0 |
| `117-s-3157` | `117-210` | Immigration | 5 | 5 | 0 | 2 | 0 | 0 | 0 | 5 | 0 |
| `117-hr-6604` | `117-297` | Armed Forces and National Security | 4 | 4 | 0 | 1 | 0 | 0 | 0 | 4 | 0 |
| `117-hr-7132` | `117-223` | Science, Technology, Communications | 4 | 4 | 0 | 2 | 0 | 0 | 1 | 3 | 0 |
| `117-s-3522` | `117-118` | International Affairs | 4 | 4 | 0 | 1 | 0 | 0 | 0 | 4 | 0 |

Sample reviewed contexts:

| Bill | Client | Period | Status | Trigger phrases | Context |
| --- | --- | --- | --- | --- | --- |
| `117-hr-1437` | AMERICAN SOCIETY OF CIVIL ENGINEERS | 2021 1st Quarter (Jan 1 - Mar 31) | exact_bill_text_with_explicit_support_signal | supporting | FLOODS Act (H.R. 1438) PRECIP Act (H.R. 1437) H.R.1319, American Rescue Plan Act of 2021 FY22 Appropriations National Science Foundation for the Future Act HR 2225 H.R.144 - Supporting Early-Career Researchers Act... |
| `117-hr-1437` | AMERICAN SOCIETY OF CIVIL ENGINEERS | 2022 1st Quarter (Jan 1 - Mar 31) | exact_bill_text_with_explicit_support_signal | supporting | FLOODS Act (H.R. 1438) PRECIP Act (H.R. 1437) H.R.1319, American Rescue Plan Act of 2021 FY22 Appropriations (H.R. 2471) National Science Foundation for the Future Act HR 2225 H.R.144 - Supporting Early-Career Rese... |
| `117-hr-1437` | AMERICAN SOCIETY OF CIVIL ENGINEERS | 2022 2nd Quarter (Apr 1 - June 30) | exact_bill_text_with_explicit_support_signal | supporting | FLOODS Act (H.R. 1438) PRECIP Act (H.R. 1437) H.R.1319, American Rescue Plan Act of 2021 FY22 Appropriations (H.R. 2471) National Science Foundation for the Future Act HR 2225 H.R.144 - Supporting Early-Career Rese... |
| `117-hr-1437` | AMERICAN SOCIETY OF CIVIL ENGINEERS | 2022 3rd Quarter (July 1 - Sep 30) | exact_bill_text_with_explicit_support_signal | supporting | FLOODS Act (H.R. 1438) PRECIP Act (H.R. 1437) H.R.1319, American Rescue Plan Act of 2021 FY22 Appropriations (H.R. 2471) National Science Foundation for the Future Act HR 2225 H.R.144 - Supporting Early-Career Rese... |
| `117-hr-1437` | AMERICAN SOCIETY OF CIVIL ENGINEERS | 2022 4th Quarter (Oct 1 - Dec 31) | exact_bill_text_with_explicit_support_signal | supporting | FLOODS Act (H.R. 1438) PRECIP Act (H.R. 1437) H.R.1319, American Rescue Plan Act of 2021 FY22 Appropriations (H.R. 2471) National Science Foundation for the Future Act HR 2225 H.R.144 - Supporting Early-Career Rese... |
| `117-hr-1437` | AMERICAN SOCIETY OF CIVIL ENGINEERS | 2021 2nd Quarter (Apr 1 - June 30) | exact_bill_text_with_explicit_support_signal | supporting | FLOODS Act (H.R. 1438) PRECIP Act (H.R. 1437) H.R.1319, American Rescue Plan Act of 2021 FY22 Appropriations National Science Foundation for the Future Act HR 2225 H.R.144 - Supporting Early-Career Researchers Act... |
| `117-hr-1437` | AMERICAN SOCIETY OF CIVIL ENGINEERS | 2021 3rd Quarter (July 1 - Sep 30) | exact_bill_text_with_explicit_support_signal | supporting | FLOODS Act (H.R. 1438) PRECIP Act (H.R. 1437) H.R.1319, American Rescue Plan Act of 2021 FY22 Appropriations National Science Foundation for the Future Act HR 2225 H.R.144 - Supporting Early-Career Researchers Act... |
| `117-hr-1437` | AMERICAN SOCIETY OF CIVIL ENGINEERS | 2021 4th Quarter (Oct 1 - Dec 31) | exact_bill_text_with_explicit_support_signal | supporting | FLOODS Act (H.R. 1438) PRECIP Act (H.R. 1437) H.R.1319, American Rescue Plan Act of 2021 FY22 Appropriations National Science Foundation for the Future Act HR 2225 H.R.144 - Supporting Early-Career Researchers Act... |
| `117-hr-4346` | COLORADO STATE UNIVERSITY FOUNDATION | 2021 2nd Quarter (Apr 1 - June 30) | exact_bill_text_with_explicit_support_signal | support_for | ...tive institutes HR 4432 Defense Appropriations - support for university research partnerships Energy and Water Appropriations - support for LaserNetUS and flood research HR 4346 Interior/Environment Appropriations - support for university funding Labor/HHS/Education appropriations - support for an engineering research partnership FY 22 appropria... |
| `117-hr-4346` | COLORADO STATE UNIVERSITY FOUNDATION | 2021 3rd Quarter (July 1 - Sep 30) | exact_bill_text_with_explicit_support_signal | support_for | ...tive institutes HR 4432 Defense Appropriations - support for university research partnerships Energy and Water Appropriations - support for LaserNetUS and flood research HR 4346 Interior/Environment Appropriations - support for university funding Labor/HHS/Education appropriations - support for engineering research partnership FY 22 appropriatio... |
| `117-hr-5376` | AMERICAN SMALL MANUFACTURERS COALITION | 2021 3rd Quarter (July 1 - Sep 30) | exact_bill_text_with_explicit_support_signal | in_support_of | ...to Manufacturing Extension Partnership funding. HR 5305 - Extending Government Funding and Delivering Emergency Assistance Act - in support of continued funding for MEP. HR 5376 - Build Back Better Act in support of MEP program funding. |
| `117-hr-5376` | BUILDING AND CONSTRUCTION TRADES DEPT AFL-CIO | 2021 3rd Quarter (July 1 - Sep 30) | exact_bill_text_with_explicit_support_signal | advocacy_for; lobbied_for_or_on | ...- House Fiscal Year 2022 Energy and Water Appropriations - Lobbied for the full funding of advanced nuclear programs, energy related projects, and nuclear cleanup sites. HR 5376 - The Build Back Better Act - Advocated for the inclusion of energy provisions and labor policies. No bill number. Lobbied on inclusion of school construction funding fo... |
| `117-hr-5376` | BUILDING AND CONSTRUCTION TRADES DEPT AFL-CIO | 2022 1st Quarter (Jan 1 - Mar 31) | exact_bill_text_with_explicit_support_signal | advocacy_for; lobbied_for_or_on | ...It increases the permissible stock ownership and constructive stock ownership percentage in a REIT to 50% and modifies rules for taxable REIT subsidiaries. Bill in full. HR 5376 - The Build Back Better Act - Advocated for the inclusion of energy provisions and labor protections. Bill in full. No bill number - Justice 40 Initiative - Lobbied for... |
| `117-hr-5376` | OREGON STATE UNIVERSITY | 2021 3rd Quarter (July 1 - Sep 30) | exact_bill_text_with_explicit_support_signal | support_for | ...cy Assistance Act) Support for agriculture, oceans, wildfire related climate research investment to NSF, NOAA, Agriculture (HR 3684 Infrastructure Investment & Jobs Act; HR 5376 Build Back Better Act) |
| `117-hr-5376` | OREGON STATE UNIVERSITY | 2021 3rd Quarter (July 1 - Sep 30) | exact_bill_text_with_explicit_support_signal | support_for | Support for statutory solution for DACA (HR 5376 Build Back Better Act) |
| `117-hr-7776` | CITY OF WACO | 2022 2nd Quarter (Apr 1 - June 30) | exact_bill_text_with_explicit_support_signal | in_support_of | ...ter Appropriations Bill and for consideration in the Interior and Environment Appropriations bill. Advocate in support of passage of the Water Resources Development Act, HR 7776. |
| `117-hr-7776` | RAYMOND BASIN MANAGEMENT BOARD | 2022 2nd Quarter (Apr 1 - June 30) | exact_bill_text_with_explicit_support_signal | in_support_of | Reauthorization of the Water Resources Development Act 2022 HR 7776 and working with Chairwoman Grace Napolitano in support of HR 7776. |
| `117-hr-7776` | SAN GABRIEL VALLEY WATER ASSOCIATION | 2022 2nd Quarter (Apr 1 - June 30) | exact_bill_text_with_explicit_support_signal | supporting | The House version of the Water Resources Development Act which is going through a reauthorization process. The legislation is HR 7776. Supporting continuing rehabilitation of the Whittier Narrows Dam. Worked with Congresswoman Napolitano. |
| `117-hr-8404` | LOG CABIN REPUBLICANS | 2022 3rd Quarter (July 1 - Sep 30) | exact_bill_text_with_explicit_support_signal | in_support_of | HR 8404 - The Respect for Marriage Act ; in support of the bill to codify marriage equality and interracial marriage in to law, repealing the Defense of Marriage Act. |
| `117-hr-8404` | LOG CABIN REPUBLICANS | 2022 4th Quarter (Oct 1 - Dec 31) | exact_bill_text_with_explicit_support_signal | in_support_of | HR 8404 - The Respect for Marriage Act ; in support of the bill to codify marriage equality and interracial marriage in to law, repealing the Defense of Marriage Act. |
