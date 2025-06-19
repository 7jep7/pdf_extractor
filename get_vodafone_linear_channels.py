import os
import sys
import pandas as pd
from typing import List, Dict

# Optional: for PDF parsing
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

TERRITORIES = ['AL', 'CZ', 'DE', 'IE', 'PT', 'RO', 'GR']

def parse_txt_file(filepath: str) -> List[tuple]:
    """Parse a TXT file and return a list of (index, channel name) tuples."""
    import re
    channels = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Match lines starting with an integer index
            match = re.match(r'^(\d+)\s+(.+)$', line)
            if match:
                idx, name = match.groups()
                channels.append((int(idx), name.strip()))
    return channels

def parse_pt_txt_file(filepath: str) -> List[tuple]:
    """Parse a PT TXT file and return a list of (index, channel name) tuples."""
    import re
    channels = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Match lines starting with an integer index
            match = re.match(r'^(\d+)\s+(.+?)(?:\s+x.*)?$', line)
            if match:
                idx, name = match.groups()
                channels.append((int(idx), name.strip()))
    return channels

def parse_pdf_file(filepath: str) -> List[str]:
    """Parse a PDF file and return a list of channel names."""
    if not PyPDF2:
        raise ImportError("PyPDF2 is required for PDF parsing. Install with 'pip install PyPDF2'.")
    reader = PyPDF2.PdfReader(filepath)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    # TODO: Implement actual parsing logic
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return lines

def parse_ro_txt_file(filepath: str) -> List[tuple]:
    """Parse a RO TXT file and return a list of (index, channel name) tuples."""
    import re
    channels = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    i = 0
    while i < len(lines):
        # Look for a line that is just a number (the index)
        if re.match(r'^\d+$', lines[i]):
            idx = int(lines[i])
            i += 1
            # Skip any '+ONLINE' or 'channel logo' lines
            while i < len(lines) and (lines[i] == '+ONLINE' or lines[i].lower() == 'channel logo'):
                i += 1
            # The next non-empty line is the channel name
            if i < len(lines):
                name = lines[i].strip()
                channels.append((idx, name))
        i += 1
    # Remove duplicates (same index and name)
    seen = set()
    unique_channels = []
    for idx, name in channels:
        key = (idx, name)
        if key not in seen:
            unique_channels.append((idx, name))
            seen.add(key)
    return unique_channels

def parse_gr_txt_file(filepath: str) -> List[tuple]:
    """Parse a GR TXT file and return a list of (index, channel name) tuples. Index is always 0."""
    channels = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            name = line.strip()
            if name:
                channels.append((0, name))
    return channels

def parse_cz_txt_file(filepath: str) -> List[tuple]:
    """Parse a CZ TXT file and return a list of (index, channel name) tuples."""
    import re
    channels = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Match lines starting with an integer index
            match = re.match(r'^(\d+)\s+(.+)$', line)
            if match:
                idx, name = match.groups()
                channels.append((int(idx), name.strip()))
    return channels

def parse_ie_txt_file(filepath: str) -> List[tuple]:
    channels = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    # Only take every other line (assuming first is logo, second is channel name)
    for i in range(1, len(lines), 2):
        channels.append((0, lines[i]))
    return channels

def parse_al_txt_file(filepath: str) -> List[tuple]:
    """Parse an AL TXT file and return a list of (index, channel name) tuples."""
    import re
    channels = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    i = 0
    while i < len(lines):
        # Look for a line that is just a number (the index)
        if re.match(r'^\d+$', lines[i]):
            idx = int(lines[i])
            i += 1
            # The next non-empty line is the channel name
            if i < len(lines):
                name = lines[i].strip()
                channels.append((idx, name))
        i += 1
    # Remove duplicates (same index and name)
    seen = set()
    unique_channels = []
    for idx, name in channels:
        key = (idx, name)
        if key not in seen:
            unique_channels.append((idx, name))
            seen.add(key)
    return unique_channels

def main(input_files: Dict[str, str], output_excel: str):
    """
    input_files: dict mapping territory code to file path
    output_excel: path to output Excel file
    """
    all_channels = dict()  # key: (index, name), value: {territory: 1/0}

    for territory, filepath in input_files.items():
        if territory == 'PT' and filepath.lower().endswith('.txt'):
            channels = parse_pt_txt_file(filepath)
        elif territory == 'RO' and filepath.lower().endswith('.txt'):
            channels = parse_ro_txt_file(filepath)
        elif territory == 'GR' and filepath.lower().endswith('.txt'):
            channels = parse_gr_txt_file(filepath)
        elif territory == 'CZ' and filepath.lower().endswith('.txt'):
            channels = parse_cz_txt_file(filepath)
        elif territory == 'IE' and filepath.lower().endswith('.txt'):
            channels = parse_ie_txt_file(filepath)
        elif territory == 'AL' and filepath.lower().endswith('.txt'):
            channels = parse_al_txt_file(filepath)
        elif filepath.lower().endswith('.txt'):
            channels = parse_txt_file(filepath)
        else:
            print(f"Unsupported file type: {filepath}")
            continue
        for idx, name in channels:
            key = (idx, name)
            if key not in all_channels:
                all_channels[key] = {t: 0 for t in TERRITORIES}
            all_channels[key][territory] = 1

    # Sort by index, then name
    sorted_channels = sorted(all_channels.keys())
    data = []
    for idx, name in sorted_channels:
        row = [idx, name]
        for t in TERRITORIES:
            row.append(all_channels[(idx, name)][t])
        data.append(row)

    columns = ['Index', 'Channel'] + TERRITORIES
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(output_excel, index=False)
    print(f"Excel file written to {output_excel}")

if __name__ == "__main__":
    # Example usage: python get_vodafone_linear_channels.py AL=inputs/albania.txt DE=inputs/germany.txt ... outputs/output.xlsx
    if len(sys.argv) < 3:
        print("Usage: python get_vodafone_linear_channels.py AL=inputs/albania.txt DE=inputs/germany.txt ... outputs/output.xlsx")
        sys.exit(1)
    *file_args, output_excel = sys.argv[1:]
    input_files = {}
    for arg in file_args:
        if '=' not in arg:
            print(f"Invalid argument: {arg}")
            sys.exit(1)
        territory, path = arg.split('=', 1)
        if territory not in TERRITORIES:
            print(f"Unknown territory: {territory}")
            sys.exit(1)
        input_files[territory] = path
    main(input_files, output_excel)