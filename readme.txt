# Vodafone TV Linear Channel Extractor

This project provides a Python script to parse Vodafone TV channel lists from various European territories and aggregate them into a single Excel file. The output Excel file contains all linear channels available via Vodafone TV, with columns for the different territories (AL, CZ, DE, IE, PT, RO, GR). Each cell contains a 1 (channel available in that country) or 0 (not available).

## Data Sourcing Strategy

Channel lists were sourced from official Vodafone websites and PDFs for each territory. The data was manually or semi-automatically extracted from the following sources:

- **Germany (DE):**
  - https://www.vodafone.de/media/downloads/pdf/tv_channel_overview/senderuebersicht_online_giga_tv_homebox.pdf
- **Portugal (PT):**
  - https://www.vodafone.pt/pacotes/televisao/lista-canais.html
- **Romania (RO):**
  - https://www.vodafone.ro/serviciifixe/grila-canale
- **Greece (GR):**
  - https://www.vodafone.gr/tv/tv-channels
- **Czech Republic (CZ):**
  - https://www.vodafone.cz/televize/programy/
- **Albania (AL):**
  - https://www.vodafone.al/vodafone-tv/
- **Ireland (IE):**
  - https://n.vodafone.ie/shop/tv/tv-channels.html
- **General Info:**
  - https://www.vodafone.com/about-vodafone/what-we-do/vodafone-tv

For some territories, channel lists were extracted from PDFs or web pages using a combination of manual copy-paste, PDF parsing, and (where necessary) OCR or AI-based extraction from screenshots.

## Limitations & Data Extraction Difficulties

- **Germany (DE):**
  - PDF available and structured, so extraction was straightforward using PDF parsing tools.
- **Portugal (PT), Ireland (IE):**
  - Channel lists were available as web pages with copyable logos and channel names, making extraction relatively easy.
- **Romania (RO):**
  - Channel list was available as a web page, but not all logo+channel pairs were displayed at once. The extracted list may be incomplete.
- **Greece (GR):**
  - No downloadable PDF or structured table was available. Channel list was extracted from a screenshot of channel logos using OCR/AI, which may introduce minor inaccuracies or inconsistencies in channel naming.
- **Czech Republic (CZ), Albania (AL):**
  - PDFs were available and used for extraction, but required manual or semi-automated parsing due to formatting.
- **General:**
  - Channel names may differ slightly between territories due to language, branding, or formatting differences. Deduplication and normalization were applied where possible, but some manual review may be required for perfect alignment.

## Usage

1. Place all input `.txt` files for each territory in the `inputs/` folder. Each file should be named according to its territory code (e.g., `de.txt`, `pt.txt`, `ro.txt`, `gr.txt`, `cz.txt`, `al.txt`, `ie.txt`).
2. Run the script with the desired territories, e.g.:

   ```bash
   python get_vodafone_linear_channels.py DE=inputs/de.txt PT=inputs/pt.txt RO=inputs/ro.txt GR=inputs/gr.txt CZ=inputs/cz.txt IE=inputs/ie.txt AL=inputs/al.txt outputs/output_all.xlsx
   ```

3. The output Excel file will be saved in the `outputs/` folder.

## File Formats

- Each territory's input file may have a different format. The script includes custom parsers for each country to handle these differences.
- See the script and the `inputs/` folder for examples.

## License

This project is for research and non-commercial use. Channel lists are the property of Vodafone and their respective content providers.
