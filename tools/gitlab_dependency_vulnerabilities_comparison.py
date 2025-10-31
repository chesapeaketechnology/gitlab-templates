import json
from pathlib import Path
import sys

def load_vulnerabilities(path):
    """Load vulnerabilities from a GitLab dependency scanning JSON report."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    vulns = {}
    for v in data.get("vulnerabilities", []):
        loc = v.get("location", {})
        dep = loc.get("dependency", {})
        pkg = dep.get("package", {}).get("name")
        version = dep.get("version") or dep.get("package", {}).get("version")
        cve = v.get("id") or v.get("identifiers", [{}])[0].get("value")
        cve_id = None
        cve_url = None
        identifiers = v.get("identifiers", [])
        for idf in identifiers:
            if idf.get("type") == "cve":
                cve_id = idf.get("value")
                cve_url = idf.get("url")
                break
        if not cve_id:
            if identifiers:
                cve_id = identifiers[0].get("value")
                cve_url = identifiers[0].get("url")
            else:
                cve_id = v.get("id", "UNKNOWN")
                cve_url = None
        severity = v.get("severity", "").lower()
        vulns.setdefault(pkg, {}).update({
            cve: {
                "version": version,
                "severity": severity,
                "message": v.get("message"),
                "url": cve_url
            }
        })
    return vulns


def compare(old_file, new_file, output_file="dependency_comparison_results.txt"):
    old = load_vulnerabilities(old_file)
    new = load_vulnerabilities(new_file)

    all_packages = set(old.keys()) | set(new.keys())
    lines = []

    total_new_cves = 0
    total_new_cves_version_change = 0
    total_new_cves_new_dependency = 0
    total_fixed_cves = 0
    total_changed_packages = 0

    for pkg in sorted(all_packages):
        old_vulns = old.get(pkg, {})
        new_vulns = new.get(pkg, {})

        old_cves = set(old_vulns.keys())
        new_cves = set(new_vulns.keys())

        added_cves = new_cves - old_cves
        fixed_cves = old_cves - new_cves
        version_changed = False

        old_versions = set(v["version"] for v in old_vulns.values())
        new_versions = set(v["version"] for v in new_vulns.values())
        if old_versions != new_versions:
            version_changed = True

        if added_cves or fixed_cves or version_changed:
            total_changed_packages += 1

            # Count new CVEs by type, from an added or upgraded dependency.
            if pkg in old:
                total_new_cves_version_change += len(added_cves)
            else:
                total_new_cves_new_dependency += len(added_cves)
            total_new_cves += len(added_cves)
            total_fixed_cves += len(fixed_cves)

            lines.append(f"\n{'='*80}")
            lines.append(f"Package: {pkg}")
            lines.append(f"Old version(s): {', '.join(old_versions) if old_versions else 'N/A'}")
            lines.append(f"New version(s): {', '.join(new_versions) if new_versions else 'N/A'}")

            if fixed_cves:
                lines.append(f"  Fixed CVEs ({len(fixed_cves)}):")
                for cve in sorted(fixed_cves):
                    info = old_vulns[cve]        # Get metadata for this CVE
                    url = info.get("url")        # May be None
                    line = cve
                    if url:
                        line += f": {url}"
                    lines.append(f"    {line}")
            if added_cves:
                source_label = "version upgrade" if pkg in old else "new dependency"
                lines.append(f"\n  New CVEs ({len(added_cves)}) ({source_label}):")
                for cve in sorted(added_cves):
                    info = new_vulns[cve]        # Get metadata for this CVE
                    url = info.get("url")        # May be None
                    line = cve
                    if url:
                        line += f": {url}"
                    lines.append(f"    {line}")

    lines.append("\n" + "="*80)
    lines.append("SUMMARY")
    lines.append("="*80)
    lines.append(f"Total packages changed: {total_changed_packages}")
    lines.append(f"Total new CVEs: {total_new_cves} "
                 f"({total_new_cves_version_change} due to version upgrades, "
                 f"{total_new_cves_new_dependency} from new dependencies)")
    lines.append(f"Total fixed/resolved CVEs: {total_fixed_cves}")
    lines.append("")

    Path(output_file).write_text("\n".join(lines))
    print(f"Comparison complete. Results written to: {output_file}\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python gitlab_dependency_vulnerabilities_comparison.py old.json new.json [results.txt]")
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "dependency_comparison_results.txt"

    compare(old_file, new_file, output_file)
