import os
import re
import json
import sys
import bibtexparser

def extract_cited_keys(latex_folder):
    cited_keys = set()
    citation_patterns = [
        r'\\cite\{([^}]+)\}',
        r'\\parencite\{([^}]+)\}',
        r'\\textcite\{([^}]+)\}',
        r'\\autocite\{([^}]+)\}',
        r'\\citep\{([^}]+)\}',
        r'\\citet\{([^}]+)\}'
    ]

    for root, _, files in os.walk(latex_folder):
        for file in files:
            if file.endswith('.tex'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in citation_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            keys = [key.strip() for key in match.split(',')]
                            cited_keys.update(keys)

    return cited_keys

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

def main(bib_path, latex_folder):
    if not os.path.isfile(bib_path):
        print(f"ERROR: BibTeX file '{bib_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(latex_folder):
        print(f"ERROR: LaTeX folder '{latex_folder}' does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(bib_path, 'r', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    cited_keys = extract_cited_keys(latex_folder)

    if not cited_keys:
        print("Warning: No citations found in LaTeX files. Running health check on entire BibTeX file.")

    # Filter only cited entries
    filtered_entries = [entry for entry in bib_database.entries if entry.get('ID') in cited_keys]

    results = []
    for entry in filtered_entries:
        citation_key = entry.get('ID', 'UNKNOWN')
        issues = check_apa_inconsistencies(entry)
        if issues:
            results.append({"citation_key": citation_key, "issues": issues})

    # Minimal console summary only
    print(f"Entries checked: {len(filtered_entries)}")
    print(f"Entries with issues: {len(results)}")

    # Write full detailed file
    os.makedirs("./temp", exist_ok=True)
    with open("./temp/bib_health_report.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    if results:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_bib_health.py path/to/your.bib path/to/latex_folder", file=sys.stderr)
        sys.exit(1)

    bib_path = sys.argv[1]
    latex_folder = sys.argv[2]
    main(bib_path, latex_folder)
