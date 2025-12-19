# Meeting Automation Guide

## Quick Start

Adding a new meeting to your website now takes **one command**:

```bash
cd /Users/JonathanFranko/Documents/Claude/pulaski-transparency-site/

python3 add_meeting.py \
  --date 2025-12-01 \
  --audio https://your-cloudflare-url.com/2025-12-meeting.mp3 \
  --transcript /path/to/transcript.txt
```

That's it! The script will:
1. ✅ Copy transcript to `assets/transcripts/`
2. ✅ Parse summary sections from transcript
3. ✅ Generate meeting page in `meetings/`
4. ✅ Update `index.html` with new meeting card
5. ✅ Show you next steps

## What It Does Automatically

### Transcript Parsing
The script automatically extracts summary sections from your transcript if formatted like:

```
## Key Topics:
- Topic 1
- Topic 2

## Department Reports:

Fire Department:
- Report item 1
- Report item 2

Police Department:
- Report item 1

## Public Concerns:
- Concern 1
- Concern 2

## Decisions or Agreements:
- Decision 1

## Notable Moments:
- Notable item 1
```

### HTML Generation
- Creates collapsible sections for each category
- Formats meeting date properly
- Links to audio and transcript files
- Updates homepage with new meeting card

## Command Options

### Required Arguments:
- `--date` - Meeting date in YYYY-MM-DD format (e.g., 2025-12-01)
- `--audio` - Full URL to audio file on Cloudflare
- `--transcript` - Path to transcript text file

### Optional Arguments:
- `--site-dir` - Custom site directory path (defaults to current)
- `--no-index-update` - Skip updating index.html (for testing)

## Examples

### Basic Usage
```bash
python3 add_meeting.py \
  --date 2025-12-01 \
  --audio https://cloudflare.../meeting.mp3 \
  --transcript transcripts/dec-2025.txt
```

### Test Mode (No Index Update)
```bash
python3 add_meeting.py \
  --date 2025-12-01 \
  --audio https://cloudflare.../meeting.mp3 \
  --transcript transcripts/dec-2025.txt \
  --no-index-update
```

### Custom Site Directory
```bash
python3 add_meeting.py \
  --date 2025-12-01 \
  --audio https://cloudflare.../meeting.mp3 \
  --transcript transcripts/dec-2025.txt \
  --site-dir /path/to/website
```

## Integration with Your RTK Bot

You can integrate this with your existing `pulaski_rtk_bot.py`:

```python
# At the end of your bot, after transcription and summary:

import subprocess

# After you have:
# - meeting_date (YYYY-MM-DD format)
# - audio_url (Cloudflare URL)
# - transcript_file (path to transcript)

subprocess.run([
    'python3',
    '/Users/JonathanFranko/Documents/Claude/pulaski-transparency-site/add_meeting.py',
    '--date', meeting_date,
    '--audio', audio_url,
    '--transcript', transcript_file
])
```

## Workflow Example

### Old Way (Manual - 20 minutes):
1. Copy `_TEMPLATE.html` to new file
2. Edit all placeholders by hand
3. Paste in transcript
4. Format summary sections
5. Update index.html manually
6. Test in browser
7. Fix typos and formatting

### New Way (Automated - 2 minutes):
```bash
python3 add_meeting.py --date 2025-12-01 --audio https://... --transcript transcript.txt
# Review output
# Deploy
```

## After Running the Script

The script tells you exactly what to do next:

```
✅ Meeting page generation complete!

Next steps:
1. Review the generated page: meetings/2025-12-december.html
2. Check index.html for the new meeting card
3. Test in browser: open index.html
4. Deploy: git add . && git commit -m 'Add December 2025 meeting' && git push
```

## Troubleshooting

### Error: Template not found
- Make sure you're in the website directory
- Or use `--site-dir` to specify location

### Error: Transcript file not found
- Check the path to your transcript file
- Use absolute path if needed

### Warning: Could not find meeting-grid
- Your index.html might have been modified
- Manually add the meeting card from the output

### Summary sections not parsing correctly
- Check your transcript formatting
- Sections need headers like "## Key Topics:"
- Items need to start with "- " or "* "

## Time Savings

**Before automation:**
- 20 minutes per meeting
- Error-prone manual copying
- Inconsistent formatting

**After automation:**
- 2 minutes per meeting
- Zero copy-paste errors  
- Perfect consistency

**Annual savings:**
- 12 meetings × 18 minutes saved = 216 minutes (3.6 hours)
- Plus: zero formatting issues to fix later

## Future Enhancements

Possible additions for the future:

1. **Auto-deployment**: Add git commit and push to script
2. **Email notification**: Send email when meeting is posted
3. **Social media**: Auto-post to Facebook when meeting added
4. **Analytics**: Track which meetings get most views
5. **RSS feed**: Auto-update RSS when meeting added

For now, the manual deployment step gives you a chance to review before going live.

---

**Questions?** Contact jon@doubletreeindustries.com
