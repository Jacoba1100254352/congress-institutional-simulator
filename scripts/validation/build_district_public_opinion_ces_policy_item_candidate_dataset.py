#!/usr/bin/env python3
"""Build official CES policy-preference item candidates for public-opinion packets."""

from __future__ import annotations

import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DATASET_DOI = "10.7910/DVN/OSXDQO"
DATASET_URL = (
    "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:"
    f"{DATASET_DOI}"
)
DATASET_API_URL = (
    "https://dataverse.harvard.edu/api/datasets/:persistentId/"
    f"?persistentId=doi:{DATASET_DOI}"
)
DATA_FILE_ID = "6898233"
GUIDE_FILE_ID = "6898232"
DATA_DOWNLOAD_URL = f"https://dataverse.harvard.edu/api/access/datafile/{DATA_FILE_ID}"
GUIDE_DOWNLOAD_URL = f"https://dataverse.harvard.edu/api/access/datafile/{GUIDE_FILE_ID}"
OUT_CSV = Path("data/validation/raw/district_public_opinion_ces_policy_item_candidates.csv")
OUT_METADATA = Path(
    "data/validation/raw/district_public_opinion_ces_policy_item_candidates.metadata.md"
)

CLAIM_BOUNDARY = (
    "Official CES policy-preference item-candidate metadata only; rows record "
    "Dataverse source metadata, official tabular-header variable IDs, and "
    "guide-derived candidate policy constructs. They are not bill-topic public "
    "support estimates, not MRP or small-area estimates, not bill-text-specific "
    "affected-population definitions, not affected-group support or harm, not "
    "public-benefit evidence, and not model validation."
)

MISSING_LINKS = (
    "bill_topic_public_opinion; exact_bill_topic_item_wording_review; "
    "MRP_or_small_area_estimate; respondent_geography_merge; "
    "bill_text_specific_affected_population_denominator; "
    "issue_specific_affected_group_support; affected_group_harm; public_benefit; "
    "causal_representation; model_validation"
)

EVIDENCE_LAYERS = (
    "official_dataverse_policy_preferences_metadata; "
    "official_policy_preferences_tabular_header; "
    "ces_policy_preferences_guide_candidate_item_review"
)

FIELDNAMES = [
    "source_family",
    "source_name",
    "dataset_doi",
    "dataset_version",
    "dataset_release_time",
    "dataset_license",
    "data_file_id",
    "data_file_label",
    "data_file_md5",
    "guide_file_id",
    "guide_file_label",
    "guide_file_md5",
    "variable_id",
    "issue_area",
    "short_label",
    "policy_area_targets",
    "candidate_construct_terms",
    "official_header_present",
    "source_url",
    "api_url",
    "data_download_url",
    "guide_download_url",
    "evidence_layers",
    "missing_links",
    "claim_boundary",
]

ITEMS: dict[str, tuple[str, str, str]] = {
    "abortion_20weeks": ("Abortion", "Ban abortion after 20 weeks", "abortion; pregnancy; 20 weeks"),
    "abortion_always": ("Abortion", "Always allow abortion", "abortion access; choice"),
    "abortion_conditional": (
        "Abortion",
        "Allow abortion only under certain cases",
        "abortion exceptions; rape; incest; life of mother",
    ),
    "abortion_coverage": (
        "Abortion",
        "Employer coverage of abortion",
        "abortion insurance coverage; employer coverage",
    ),
    "abortion_expenditures": (
        "Abortion",
        "Prohibit expenditures for abortion",
        "abortion funding; federal expenditures",
    ),
    "abortion_prohibition": ("Abortion", "Total prohibition of abortion", "abortion prohibition"),
    "abortion_scale": ("Abortion", "Support scale for access to abortion", "abortion scale"),
    "enviro_airwateracts": (
        "Environment",
        "Strengthen the Clean Air Act and Clean Water Act",
        "clean air; clean water; environmental regulation",
    ),
    "enviro_carbon": (
        "Environment",
        "Allow EPA to regulate carbon dioxide emissions",
        "carbon dioxide; EPA; climate regulation",
    ),
    "enviro_mpg_raise": (
        "Environment",
        "Raise average fuel-efficiency standards",
        "fuel efficiency; vehicle emissions",
    ),
    "enviro_renewable": (
        "Environment",
        "Require more electricity from renewable sources",
        "renewable electricity; energy standards",
    ),
    "enviro_scale": (
        "Environment",
        "Opposition scale to climate change action",
        "climate change; environmental policy",
    ),
    "enviro_vs_jobs": (
        "Environment",
        "Preference between environmental protection and job availability",
        "environment; jobs; regulation tradeoff",
    ),
    "guns_assaultban": ("Guns", "Ban assault rifles", "assault weapons; firearm regulation"),
    "guns_bgchecks": (
        "Guns",
        "Background checks for guns for all sales",
        "background checks; firearm sales",
    ),
    "guns_names": (
        "Guns",
        "Prohibit publishing gun owner names",
        "gun owner names; publication limits",
    ),
    "guns_permits": (
        "Guns",
        "Allow concealed-carry permits",
        "concealed carry; firearm permits",
    ),
    "guns_scale": ("Guns", "Restriction scale on gun sales", "gun sales; firearm restrictions"),
    "healthcare_aca": ("Health Care", "Affordable Care Act support", "ACA; health insurance"),
    "healthcare_acamandate": (
        "Health Care",
        "Affordable Care Act individual mandate support",
        "ACA mandate; health insurance requirement",
    ),
    "healthcare_medicare": (
        "Health Care",
        "Medicare expansion support",
        "Medicare; public health insurance",
    ),
    "healthcare_medicareage": (
        "Health Care",
        "Lower Medicare eligibility age",
        "Medicare age; public health insurance",
    ),
    "immig_border": (
        "Immigration",
        "Increase border patrols on the U.S.-Mexican border",
        "border patrol; border enforcement",
    ),
    "immig_deport": (
        "Immigration",
        "Identify and deport undocumented immigrants",
        "deportation; undocumented immigrants",
    ),
    "immig_employer": (
        "Immigration",
        "Sanction employers hiring undocumented immigrants",
        "employer sanctions; undocumented workers",
    ),
    "immig_legalize": (
        "Immigration",
        "Grant legal status to undocumented immigrants",
        "legalization; undocumented immigrants",
    ),
    "immig_police": (
        "Immigration",
        "Allow police questioning of suspected undocumented immigrants",
        "police questioning; immigration enforcement",
    ),
    "immig_reduce": (
        "Immigration",
        "Reduce legal immigration",
        "legal immigration; immigration levels",
    ),
    "immig_report": (
        "Immigration",
        "Withhold funding from police failing to report undocumented immigrants",
        "local police; immigration reporting; federal funding",
    ),
    "immig_services": (
        "Immigration",
        "Prohibit services for undocumented immigrants",
        "public services; undocumented immigrants",
    ),
    "immig_wall": (
        "Immigration",
        "Increase spending on border security including a wall",
        "border wall; border security spending",
    ),
    "military_democracy": (
        "Military",
        "Approve of military action to assist democracy",
        "military action; democracy promotion",
    ),
    "military_genocide": (
        "Military",
        "Approve of military action to intervene in genocide or civil war",
        "military intervention; genocide; civil war",
    ),
    "military_helpun": (
        "Military",
        "Approve of military action to help the United Nations",
        "United Nations; military support",
    ),
    "military_oil": (
        "Military",
        "Approve of military action to ensure oil supply",
        "oil supply; military action",
    ),
    "military_protectallies": (
        "Military",
        "Approve of military action to protect allies",
        "allies; military action",
    ),
    "military_terroristcamp": (
        "Military",
        "Approve of military action to destroy terrorist camps",
        "terrorist camps; military action",
    ),
    "affirmativeaction": (
        "Other",
        "Support affirmative action",
        "affirmative action; civil rights",
    ),
    "affirmativeaction_scale": (
        "Other",
        "Scale on affirmative action support",
        "affirmative action scale; civil rights",
    ),
    "gaymarriage_ban": (
        "Other",
        "Support banning gay marriage",
        "same-sex marriage; marriage ban",
    ),
    "gaymarriage_legalize": (
        "Other",
        "Support legalizing gay marriage",
        "same-sex marriage; marriage equality",
    ),
    "gaymarriage_scale": (
        "Other",
        "Scale on gay marriage support",
        "same-sex marriage scale; marriage equality",
    ),
    "incometax_vs_salestax": (
        "Other",
        "Preference between income tax and sales tax",
        "income tax; sales tax",
    ),
    "spending_cuts_least": (
        "Spending",
        "Least preferred spending cut option",
        "spending cuts; defense; domestic spending; taxes",
    ),
    "spending_cuts_most": (
        "Spending",
        "Most preferred spending cut option",
        "spending cuts; defense; domestic spending; taxes",
    ),
    "spending_education": (
        "Spending",
        "Spending preferences on education",
        "education spending; state spending",
    ),
    "spending_healthcare": (
        "Spending",
        "Spending preferences on health care",
        "health care spending; state spending",
    ),
    "spending_infrastructure": (
        "Spending",
        "Spending preferences on transportation and infrastructure",
        "transportation spending; infrastructure spending",
    ),
    "spending_police": (
        "Spending",
        "Spending preferences on law enforcement",
        "police spending; law enforcement spending",
    ),
    "spending_vs_tax": (
        "Spending",
        "Preference between tax increases and spending cuts",
        "tax increases; spending cuts",
    ),
    "spending_welfare": (
        "Spending",
        "Spending preferences on welfare",
        "welfare spending; state spending",
    ),
    "trade_canmex_except": (
        "Trade",
        "Trade policy toward Canada and Mexico excluding some sectors",
        "trade; Canada; Mexico",
    ),
    "trade_canmex_include": (
        "Trade",
        "Trade policy toward Canada and Mexico including more sectors",
        "trade; Canada; Mexico",
    ),
    "trade_china": ("Trade", "Trade policy toward China", "trade; China"),
}

POLICY_AREA_ITEMS = {
    "Armed Forces and National Security": {
        "military_democracy",
        "military_genocide",
        "military_helpun",
        "military_oil",
        "military_protectallies",
        "military_terroristcamp",
        "spending_cuts_least",
        "spending_cuts_most",
    },
    "Civil Rights and Liberties, Minority Issues": {
        "affirmativeaction",
        "affirmativeaction_scale",
        "gaymarriage_ban",
        "gaymarriage_legalize",
        "gaymarriage_scale",
    },
    "Commerce": {
        "trade_canmex_except",
        "trade_canmex_include",
        "trade_china",
    },
    "Crime and Law Enforcement": {
        "guns_assaultban",
        "guns_bgchecks",
        "guns_names",
        "guns_permits",
        "guns_scale",
        "spending_police",
    },
    "Economics and Public Finance": {
        "incometax_vs_salestax",
        "spending_cuts_least",
        "spending_cuts_most",
        "spending_education",
        "spending_healthcare",
        "spending_infrastructure",
        "spending_vs_tax",
        "spending_welfare",
    },
    "Finance and Financial Sector": {
        "incometax_vs_salestax",
        "spending_cuts_least",
        "spending_cuts_most",
        "spending_vs_tax",
    },
    "Immigration": {
        "immig_border",
        "immig_deport",
        "immig_employer",
        "immig_legalize",
        "immig_police",
        "immig_reduce",
        "immig_report",
        "immig_services",
        "immig_wall",
    },
    "International Affairs": {
        "military_democracy",
        "military_genocide",
        "military_helpun",
        "military_oil",
        "military_protectallies",
        "military_terroristcamp",
        "trade_canmex_except",
        "trade_canmex_include",
        "trade_china",
    },
    "Public Lands and Natural Resources": {
        "enviro_airwateracts",
        "enviro_carbon",
        "enviro_mpg_raise",
        "enviro_renewable",
        "enviro_scale",
        "enviro_vs_jobs",
    },
}


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CongressInstitutionalSimulator/policy-item-candidate-audit"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_header(url: str) -> set[str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CongressInstitutionalSimulator/policy-item-candidate-audit"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        header = response.readline().decode("utf-8").strip()
    if not header:
        raise SystemExit("Official CES policy-preferences data file header was empty.")
    return set(header.split("\t"))


def latest_version(payload: dict[str, Any]) -> dict[str, Any]:
    version = payload.get("data", {}).get("latestVersion")
    if not isinstance(version, dict):
        raise SystemExit("Dataverse response did not include data.latestVersion.")
    return version


def version_label(version: dict[str, Any]) -> str:
    number = version.get("versionNumber")
    minor = version.get("versionMinorNumber")
    if number is None:
        return ""
    if minor is None:
        return str(number)
    return f"{number}.{minor}"


def checksum(data_file: dict[str, Any]) -> str:
    if data_file.get("md5"):
        return str(data_file["md5"])
    nested = data_file.get("checksum")
    if isinstance(nested, dict):
        return str(nested.get("value", ""))
    return ""


def file_metadata(version: dict[str, Any], expected_id: str) -> dict[str, str]:
    for wrapper in version.get("files", []):
        data_file = wrapper.get("dataFile", {})
        file_id = str(data_file.get("id", ""))
        if file_id == expected_id:
            return {
                "id": file_id,
                "label": str(wrapper.get("label") or data_file.get("filename", "")),
                "md5": checksum(data_file),
            }
    raise SystemExit(f"Dataverse latest version did not include file id {expected_id}.")


def policy_area_targets(variable_id: str) -> str:
    targets = sorted(
        policy_area
        for policy_area, variable_ids in POLICY_AREA_ITEMS.items()
        if variable_id in variable_ids
    )
    return "; ".join(targets)


def build_rows() -> list[dict[str, str]]:
    payload = fetch_json(DATASET_API_URL)
    version = latest_version(payload)
    data_file = file_metadata(version, DATA_FILE_ID)
    guide_file = file_metadata(version, GUIDE_FILE_ID)
    header_variables = fetch_header(DATA_DOWNLOAD_URL)

    missing_defined = sorted(set(ITEMS) - header_variables)
    if missing_defined:
        raise SystemExit(
            "Official CES policy-preferences header is missing expected variables: "
            + ", ".join(missing_defined)
        )

    extra_policy_variables = sorted(
        variable
        for variable in header_variables - {"year", "case_id"}
        if variable not in ITEMS
    )
    if extra_policy_variables:
        raise SystemExit(
            "Official CES policy-preferences header has unclassified variables: "
            + ", ".join(extra_policy_variables)
        )

    version_text = version_label(version)
    license_info = version.get("license", {})
    license_name = str(license_info.get("name", "")) if isinstance(license_info, dict) else ""
    release_time = str(version.get("releaseTime") or version.get("lastUpdateTime") or "")
    rows: list[dict[str, str]] = []
    for variable_id in sorted(ITEMS):
        issue_area, short_label, candidate_terms = ITEMS[variable_id]
        rows.append({
            "source_family": "District public opinion and affected groups",
            "source_name": "Cumulative CES Policy Preferences",
            "dataset_doi": DATASET_DOI,
            "dataset_version": version_text,
            "dataset_release_time": release_time,
            "dataset_license": license_name,
            "data_file_id": data_file["id"],
            "data_file_label": data_file["label"],
            "data_file_md5": data_file["md5"],
            "guide_file_id": guide_file["id"],
            "guide_file_label": guide_file["label"],
            "guide_file_md5": guide_file["md5"],
            "variable_id": variable_id,
            "issue_area": issue_area,
            "short_label": short_label,
            "policy_area_targets": policy_area_targets(variable_id),
            "candidate_construct_terms": candidate_terms,
            "official_header_present": "1" if variable_id in header_variables else "0",
            "source_url": DATASET_URL,
            "api_url": DATASET_API_URL,
            "data_download_url": DATA_DOWNLOAD_URL,
            "guide_download_url": GUIDE_DOWNLOAD_URL,
            "evidence_layers": EVIDENCE_LAYERS,
            "missing_links": MISSING_LINKS,
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_metadata(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit("No CES policy-preferences candidate rows built.")
    policy_targets = sorted(
        {
            target
            for row in rows
            for target in row["policy_area_targets"].split("; ")
            if target
        }
    )
    issue_areas = sorted({row["issue_area"] for row in rows})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    first = rows[0]
    OUT_METADATA.write_text(
        "\n".join([
            "# District Public Opinion CES Policy Item Candidate Metadata",
            "",
            f"Generated: {now}.",
            f"- Source family: {first['source_family']}.",
            f"- Source name: {first['source_name']}.",
            f"- Dataset DOI: {first['dataset_doi']}.",
            f"- Dataset version: {first['dataset_version']}.",
            f"- Dataset release time: {first['dataset_release_time']}.",
            f"- Dataset license: {first['dataset_license']}.",
            f"- Data file: {first['data_file_label']} (Dataverse file id {first['data_file_id']}).",
            f"- Guide file: {first['guide_file_label']} (Dataverse file id {first['guide_file_id']}).",
            f"- Official policy variables reviewed: {len(rows)}.",
            f"- Issue areas represented: {len(issue_areas)} ({'; '.join(issue_areas)}).",
            f"- Local policy areas with at least one candidate item: {len(policy_targets)} ({'; '.join(policy_targets)}).",
            "",
            f"Claim boundary: {CLAIM_BOUNDARY}",
            "",
            "Source URLs:",
            f"- {DATASET_URL}",
            f"- {DATASET_API_URL}",
            f"- {DATA_DOWNLOAD_URL}",
            f"- {GUIDE_DOWNLOAD_URL}",
        ])
        + "\n"
    )


def main() -> int:
    rows = build_rows()
    if not rows:
        raise SystemExit("No CES policy-preferences candidate rows built.")
    write_csv(rows)
    write_metadata(rows)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_METADATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
