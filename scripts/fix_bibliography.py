#!/usr/bin/env python3
"""
Script to verify and fix missing bibliography entries in LaTeX files.

This script:
1. Extracts all citation keys from .tex files
2. Checks which ones exist in .bib files (with various naming conventions)
3. Automatically updates .tex files with correct citation keys
4. Reports truly missing entries that need to be added
"""

import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class BibliographyFixer:
    def __init__(self, thesis_dir: str, bib_files: List[str]):
        self.thesis_dir = Path(thesis_dir)
        self.bib_files = [self.thesis_dir / bib for bib in bib_files]
        self.bib_entries = {}  # Maps lowercase key -> actual key
        self.citation_map = {}  # Maps incorrect key -> correct key
        self.missing_citations = set()

    def load_bibliography_entries(self):
        """Load all bibliography entries from .bib files."""
        print("📚 Loading bibliography entries...")

        for bib_file in self.bib_files:
            if not bib_file.exists():
                print(f"⚠️  Warning: {bib_file} not found")
                continue

            with open(bib_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find all @type{key, entries
            matches = re.finditer(r'@\w+\{([^,\s]+)', content)
            for match in matches:
                key = match.group(1)
                # Store both the key and a normalized version for fuzzy matching
                self.bib_entries[key.lower()] = key

        print(f"✓ Loaded {len(self.bib_entries)} bibliography entries")

    def extract_citations_from_file(self, tex_file: Path) -> Set[str]:
        """Extract all citation keys from a .tex file."""
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()

        citations = set()

        # Match \cite{key}, \citep{key}, \citet{key}, etc.
        cite_pattern = r'\\cite[a-z]*\{([^}]+)\}'
        matches = re.finditer(cite_pattern, content)

        for match in matches:
            keys_str = match.group(1)
            # Split by comma for multiple citations
            keys = [k.strip() for k in keys_str.split(',')]
            citations.update(keys)

        return citations

    def find_matching_key(self, citation_key: str) -> Tuple[str, str]:
        """
        Try to find a matching bibliography entry for a citation key.

        Returns:
            Tuple of (status, matched_key)
            status can be: 'exact', 'fuzzy', 'missing'
        """
        # Exact match (case-insensitive)
        if citation_key.lower() in self.bib_entries:
            actual_key = self.bib_entries[citation_key.lower()]
            if actual_key == citation_key:
                return 'exact', citation_key
            else:
                return 'fuzzy', actual_key

        # Try variations: underscores <-> hyphens, camelCase, etc.
        variations = [
            citation_key.replace('_', '-'),
            citation_key.replace('-', '_'),
            citation_key.replace('_', ''),
            citation_key.replace('-', ''),
        ]

        for variant in variations:
            if variant.lower() in self.bib_entries:
                return 'fuzzy', self.bib_entries[variant.lower()]

        # Try partial matching for common patterns
        # e.g., author_topic_year -> authorTopicYear or AuthorTopicYear
        parts = re.split(r'[_-]', citation_key)

        # Try CamelCase
        camel_case = ''.join(p.capitalize() for p in parts)
        if camel_case.lower() in self.bib_entries:
            return 'fuzzy', self.bib_entries[camel_case.lower()]

        # Try first part + year pattern
        if len(parts) >= 2:
            for actual_key in self.bib_entries.values():
                # Check if it's a similar author-year pattern
                if parts[0].lower() in actual_key.lower() and parts[-1] in actual_key:
                    # Do a more thorough check
                    if self._keys_similar(citation_key, actual_key):
                        return 'fuzzy', actual_key

        return 'missing', citation_key

    def _keys_similar(self, key1: str, key2: str) -> bool:
        """Check if two keys are semantically similar."""
        # Extract author and year
        def extract_parts(key):
            parts = re.split(r'[_-]', key.lower())
            year_match = re.search(r'(19|20)\d{2}', key)
            year = year_match.group(0) if year_match else None
            author = parts[0] if parts else None
            return author, year

        author1, year1 = extract_parts(key1)
        author2, year2 = extract_parts(key2)

        # If author and year match, likely the same reference
        return (author1 and author2 and author1 in author2.lower() and
                year1 and year2 and year1 == year2)

    def analyze_citations(self, tex_files: List[Path]):
        """Analyze all citations and build a mapping of fixes."""
        print("\n🔍 Analyzing citations...")

        all_citations = set()
        for tex_file in tex_files:
            citations = self.extract_citations_from_file(tex_file)
            all_citations.update(citations)

        exact_matches = 0
        fuzzy_matches = 0

        for citation in sorted(all_citations):
            status, matched_key = self.find_matching_key(citation)

            if status == 'exact':
                exact_matches += 1
            elif status == 'fuzzy':
                self.citation_map[citation] = matched_key
                fuzzy_matches += 1
            elif status == 'missing':
                self.missing_citations.add(citation)

        print(f"✓ Exact matches: {exact_matches}")
        print(f"🔧 Fuzzy matches (need fixing): {fuzzy_matches}")
        print(f"❌ Missing entries: {len(self.missing_citations)}")

    def fix_tex_file(self, tex_file: Path, dry_run: bool = False) -> int:
        """Fix citations in a .tex file. Returns number of fixes made."""
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        fixes_made = 0

        # Replace citations with correct keys
        for old_key, new_key in self.citation_map.items():
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(old_key) + r'\b'

            # Count occurrences
            count = len(re.findall(pattern, content))
            if count > 0:
                content = re.sub(pattern, new_key, content)
                fixes_made += count

        if content != original_content:
            if not dry_run:
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Fixed {fixes_made} citations in {tex_file.name}")
            else:
                print(f"  [DRY RUN] Would fix {fixes_made} citations in {tex_file.name}")

        return fixes_made

    def print_report(self):
        """Print a detailed report of findings."""
        print("\n" + "="*70)
        print("📊 BIBLIOGRAPHY REPORT")
        print("="*70)

        if self.citation_map:
            print("\n🔧 CITATION KEYS TO FIX:")
            print("-" * 70)
            for old_key, new_key in sorted(self.citation_map.items()):
                print(f"  {old_key:45} → {new_key}")

        if self.missing_citations:
            print("\n❌ MISSING BIBLIOGRAPHY ENTRIES:")
            print("-" * 70)
            print("These entries are not found in any .bib file and need to be added:")
            for citation in sorted(self.missing_citations):
                print(f"  - {citation}")

        if not self.citation_map and not self.missing_citations:
            print("\n✅ All citations are correct!")

    def run(self, tex_files: List[Path], dry_run: bool = False, auto_fix: bool = False):
        """Main execution flow."""
        self.load_bibliography_entries()
        self.analyze_citations(tex_files)
        self.print_report()

        if self.citation_map:
            if auto_fix:
                print("\n🔧 Applying fixes...")
                total_fixes = 0
                for tex_file in tex_files:
                    fixes = self.fix_tex_file(tex_file, dry_run=dry_run)
                    total_fixes += fixes

                if total_fixes > 0:
                    if dry_run:
                        print(f"\n[DRY RUN] Would make {total_fixes} total fixes")
                    else:
                        print(f"\n✅ Successfully fixed {total_fixes} citations!")
            else:
                print("\n💡 Run with --fix to apply these changes automatically")
                print("   or --dry-run to preview changes without modifying files")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify and fix bibliography citations in LaTeX files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --check                    # Check for issues without fixing
  %(prog)s --dry-run                  # Preview what would be changed
  %(prog)s --fix                      # Apply fixes to all files
  %(prog)s --fix sources/chapters/intro.tex  # Fix specific file
        """
    )

    parser.add_argument(
        'files',
        nargs='*',
        help='Specific .tex files to process (default: all in sources/chapters/)'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix citation keys'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Only check for issues, do not fix'
    )
    parser.add_argument(
        '--bib-files',
        nargs='+',
        default=['bibliography.bib', 'weak_supervision.bib', 'synthetic-coling2024.bib'],
        help='Bibliography files to check against'
    )

    args = parser.parse_args()

    # Determine thesis directory
    thesis_dir = Path.cwd()

    # Find .tex files to process
    if args.files:
        tex_files = [Path(f) for f in args.files]
    else:
        chapters_dir = thesis_dir / 'sources' / 'chapters'
        if chapters_dir.exists():
            tex_files = list(chapters_dir.glob('*.tex'))
        else:
            print(f"❌ Error: {chapters_dir} not found")
            sys.exit(1)

    # Validate files exist
    for f in tex_files:
        if not f.exists():
            print(f"❌ Error: {f} not found")
            sys.exit(1)

    # Create fixer instance
    fixer = BibliographyFixer(thesis_dir, args.bib_files)

    # Run with appropriate mode
    if args.check:
        fixer.run(tex_files, dry_run=True, auto_fix=False)
    elif args.dry_run:
        fixer.run(tex_files, dry_run=True, auto_fix=True)
    elif args.fix:
        fixer.run(tex_files, dry_run=False, auto_fix=True)
    else:
        # Default: just check
        fixer.run(tex_files, dry_run=True, auto_fix=False)
        print("\n💡 Use --fix to apply changes, --dry-run to preview, or --check for report only")


if __name__ == '__main__':
    main()
