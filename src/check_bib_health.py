import os
import json
import sys
import bibtexparser

def check_apa_inconsistencies(entry):
    issues = []
    entry_type = entry.get('ENTRYTYPE', '').lower()

    mandatory_fields = {
        'article': ['author', 'year', 'title', 'journal'],
        'book': ['author', 'year', 'title', 'publisher'],
        'inproceedings': ['author', 'year', 'title', 'booktitle'],
        'misc': ['author', 'year', 'title'],
    }

    required_fields = mandatory_fields.get(entry_type, [])
    for field in required_fields:
        if field not in entry:
            issues.append(f"Missing mandatory field: {field}")

    title = entry.get('title', '')
    if title:
        words = title.strip().split()
        if words and words[0][0].islower():
            issues.append("First word of title should be capitalized")
        if not title.endswith('.'):
            issues.append("Title should end with a period (.)")

    if 'author' in entry:
        authors = entry['author']
        if not all(',' in a for a in authors.split(' and ')):
            issues.append("Author names likely not formatted correctly (surname first, initials after comma)")

    if entry_type == 'article' and 'doi' not in entry:
        issues.append("Missing DOI for article entry (recommended)")

    return issues

def main(bib_path):
    if not os.path.isfile(bib_path):
        print(f"ERROR: BibTeX file '{bib_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(bib_path, 'r', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    results = []
    for entry in bib_database.entries:
        citation_key = entry.get('ID', 'UNKNOWN')
        issues = check_apa_inconsistencies(entry)
        if issues:
            results.append({"citation_key": citation_key, "issues": issues})

    # Console summary
    if results:
        print(f"\n=== BIB Health Report ===")
        print(f"Entries checked: {len(bib_database.entries)}")
        print(f"Entries with issues: {len(results)}")
        for r in results:
            print(f" - {r['citation_key']}: {len(r['issues'])} issue(s)")
        print(f"Detailed report written to './temp/bib_health_report.json'\n")
    else:
        print("\n=== BIB Health Report ===")
        print(f"Entries checked: {len(bib_database.entries)}")
        print("No issues found. Your library looks healthy!\n")

    # Write full detailed file
    os.makedirs("./temp", exist_ok=True)
    with open("./temp/bib_health_report.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Exit with code based on results
    if results:
        sys.exit(1)  # Problems found
    else:
        sys.exit(0)  # All good

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_bib_health.py path/to/your.bib", file=sys.stderr)
        sys.exit(1)

    bib_path = sys.argv[1]
    main(bib_path)
