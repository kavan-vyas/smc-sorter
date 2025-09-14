# Web Page to PDF Converter Setup


## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install WeasyPrint system dependencies:**
   
   **On Windows:**
   - WeasyPrint should work out of the box with the pip installation
   
   **On macOS:**
   ```bash
   brew install cairo pango gdk-pixbuf libffi
   ```
   
   **On Ubuntu/Debian:**
   ```bash
   sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
   ```

## Folder Structure

Create your project folder structure like this:

```
your_project/
├── main.py                 # The main script
├── requirements.txt        # Python dependencies
├── questions_folder/       # Your GIF files go here
│   ├── 1234.gif           # Question GIF
│   ├── 1234s.gif          # Answer GIF (note the 's' suffix)
│   ├── 5678.gif           # Another question
│   ├── 5678s.gif          # Its answer
│   ├── 789.gif            # 3-digit question
│   ├── 789s.gif           # 3-digit answer
│   └── ...
└── output_pdfs/           # Generated PDFs will be saved here (auto-created)
```

## Usage

### Process All Questions
Run the script to convert all question-answer pairs:
```bash
python main.py
```

### Process All Questions from Custom Folder
```bash
python main.py my_custom_folder
```

### Process Single Question
Convert just one specific question:
```bash
python main.py questions_folder 1234
```

## File Naming Convention

- **Question GIFs:** `1234.gif`, `5678.gif`, `789.gif` (any number of digits)
- **Answer GIFs:** `1234s.gif`, `5678s.gif`, `789s.gif` (same number + 's' suffix)

## Output

- PDFs are generated in the `output_pdfs/` folder
- Each PDF contains:
  - Question GIF at the top
  - Answer GIF at the bottom
  - Clean formatting optimized for OneNote
- Files are named as `question_1234.pdf`, `question_5678.pdf`, etc.

## Features

- ✅ Supports 3-digit and 4-digit question numbers
- ✅ Embeds GIFs directly in PDF (no external dependencies)
- ✅ Clean, professional formatting
- ✅ A4 page size with proper margins
- ✅ Optimized for OneNote integration
- ✅ Batch processing of all questions
- ✅ Individual question processing
- ✅ Error handling and progress reporting

## Troubleshooting

1. **Installation much is simpler now:**
   - Only need: `pip3 install reportlab pillow`
   - No system dependencies required!

2. **If images don't appear correctly:**
   - Try using `--simple` flag for basic PDF generation
   - Check that GIF files are not corrupted

3. **GIF not found errors:**
   - Ensure your GIF files follow the naming convention exactly
   - Check file extensions are `.gif` (lowercase)

4. **Memory issues with large GIFs:**
   - ReportLab handles images more efficiently than WeasyPrint
   - Consider compressing very large GIF files if needed

5. **PDF layout issues:**
   - Use `--simple` mode for maximum compatibility
   - Images are automatically resized to fit pages

## OneNote Integration

1. Open OneNote
2. Navigate to the page where you want to add the PDF
3. Go to Insert → File Attachment
4. Select your generated PDF file
5. Choose whether to insert as attachment or print to page

The PDFs are optimized for OneNote's PDF viewing, with clean formatting and appropriate sizing.
