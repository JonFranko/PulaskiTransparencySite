#!/usr/bin/env python3
"""
Meeting Page Generator for Pulaski Transparency Website

This script automates the process of adding new meeting pages to the website.
It generates HTML files from templates and updates the index.html meeting list.

Usage:
    python3 add_meeting.py --date 2025-12-01 --audio https://cloudflare.../meeting.mp3 --transcript transcript.txt

Author: Jon Franko / Doubletree Industries
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


class MeetingPageGenerator:
    """Generate meeting pages and update website"""
    
    def __init__(self, site_dir=None):
        """Initialize with site directory"""
        if site_dir is None:
            site_dir = Path(__file__).parent
        else:
            site_dir = Path(site_dir)
        
        self.site_dir = site_dir
        self.meetings_dir = site_dir / 'meetings'
        self.template_path = self.meetings_dir / '_TEMPLATE.html'
        self.index_path = site_dir / 'index.html'
        
        # Verify paths exist
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        if not self.index_path.exists():
            raise FileNotFoundError(f"Index not found: {self.index_path}")
    
    def parse_summary(self, transcript_text):
        """
        Extract summary sections from transcript.
        
        Looks for sections like:
        ## Key Topics:
        - Topic 1
        - Topic 2
        
        Returns dict with parsed sections.
        """
        sections = {
            'topics': [],
            'departments': {},
            'public_concerns': [],
            'decisions': [],
            'notable': []
        }
        
        # Split into lines
        lines = transcript_text.split('\n')
        current_section = None
        current_dept = None
        
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            if line.lower().startswith('## key topics') or line.lower().startswith('key discussion topics'):
                current_section = 'topics'
                continue
            elif line.lower().startswith('## department reports') or 'department' in line.lower():
                current_section = 'departments'
                continue
            elif line.lower().startswith('## public concerns') or 'public' in line.lower():
                current_section = 'public_concerns'
                continue
            elif line.lower().startswith('## decisions') or 'decisions' in line.lower():
                current_section = 'decisions'
                continue
            elif line.lower().startswith('## notable') or 'notable' in line.lower():
                current_section = 'notable'
                continue
            
            # Detect department sub-headers
            if current_section == 'departments' and line.endswith(':') and not line.startswith('-'):
                current_dept = line.rstrip(':')
                sections['departments'][current_dept] = []
                continue
            
            # Parse bullet points
            if line.startswith('- ') or line.startswith('* '):
                item = line[2:].strip()
                
                if current_section == 'topics':
                    sections['topics'].append(item)
                elif current_section == 'departments' and current_dept:
                    sections['departments'][current_dept].append(item)
                elif current_section == 'public_concerns':
                    sections['public_concerns'].append(item)
                elif current_section == 'decisions':
                    sections['decisions'].append(item)
                elif current_section == 'notable':
                    sections['notable'].append(item)
        
        return sections
    
    def generate_topics_summary(self, topics):
        """Create brief topic summary for index card"""
        if not topics:
            return "Meeting summary available"
        
        # Take first 3-4 topics, make them concise
        summary_topics = []
        for topic in topics[:4]:
            # Shorten if too long
            if len(topic) > 60:
                topic = topic[:57] + '...'
            summary_topics.append(topic)
        
        return ', '.join(summary_topics)
    
    def create_collapsible_section(self, title, items, subsections=None):
        """Create HTML for a collapsible section"""
        html = f'            <button class="collapsible">{title}</button>\n'
        html += '            <div class="content">\n'
        html += '                <div class="content-inner">\n'
        
        if subsections:
            # Handle department-style sections with sub-headers
            for subheader, subitems in subsections.items():
                html += f'                    <h4>{subheader}</h4>\n'
                if subitems:
                    html += '                    <ul>\n'
                    for item in subitems:
                        html += f'                        <li>{item}</li>\n'
                    html += '                    </ul>\n'
        elif items:
            # Simple list
            html += '                    <ul>\n'
            for item in items:
                html += f'                        <li>{item}</li>\n'
            html += '                    </ul>\n'
        else:
            html += '                    <p><em>No information available for this section.</em></p>\n'
        
        html += '                </div>\n'
        html += '            </div>\n\n'
        
        return html
    
    def create_meeting_page(self, date_str, audio_url, transcript_path, summary=None):
        """
        Generate new meeting page from template.
        
        Args:
            date_str: Meeting date in YYYY-MM-DD format
            audio_url: Full URL to audio file on Cloudflare
            transcript_path: Path to transcript text file
            summary: Optional pre-parsed summary dict
        
        Returns:
            tuple: (output_filename, topics_summary)
        """
        # Parse date
        date = datetime.strptime(date_str, '%Y-%m-%d')
        month_name = date.strftime('%B')
        year = date.year
        month_num = date.month
        
        # Create filename
        filename = f"{year}-{month_num:02d}-{month_name.lower()}.html"
        output_path = self.meetings_dir / filename
        
        # Read transcript
        transcript_text = Path(transcript_path).read_text()
        
        # Parse summary if not provided
        if summary is None:
            summary = self.parse_summary(transcript_text)
        
        # Read template
        template = self.template_path.read_text()
        
        # Replace basic placeholders
        page_content = template.replace('[MONTH YEAR]', f'{month_name} {year}')
        page_content = page_content.replace('[Month Day, Year]', date.strftime('%B %d, %Y'))
        page_content = page_content.replace('YYYY-MM-month.mp3', audio_url)
        page_content = page_content.replace('YYYY-MM-month.txt', f'../assets/transcripts/{year}-{month_num:02d}-{month_name.lower()}.txt')
        
        # Build summary sections HTML
        summary_html = ''
        
        if summary['topics']:
            summary_html += self.create_collapsible_section('Key Discussion Topics', summary['topics'])
        
        if summary['departments']:
            summary_html += self.create_collapsible_section('Department Reports', None, summary['departments'])
        
        if summary['public_concerns']:
            summary_html += self.create_collapsible_section('Public Concerns', summary['public_concerns'])
        
        if summary['decisions']:
            summary_html += self.create_collapsible_section('Decisions or Agreements', summary['decisions'])
        
        if summary['notable']:
            summary_html += self.create_collapsible_section('Other Notable Moments', summary['notable'])
        
        # Replace summary section in template
        # Find the summary section and replace it
        summary_pattern = r'(<button class="collapsible">Key Discussion Topics</button>.*?</div>\n\n\s*</div>)'
        
        if re.search(summary_pattern, page_content, re.DOTALL):
            # Replace existing summary sections
            page_content = re.sub(
                r'<button class="collapsible">.*?</div>\n\n\s*</div>',
                summary_html.rstrip(),
                page_content,
                count=0,
                flags=re.DOTALL
            )
        else:
            # Insert after summary heading
            page_content = page_content.replace(
                '<section id="summary">\n            <h2>Meeting Summary</h2>',
                f'<section id="summary">\n            <h2>Meeting Summary</h2>\n\n{summary_html}'
            )
        
        # Replace transcript placeholder
        page_content = page_content.replace(
            '<p><em>Full transcript will be available here once processed.</em></p>\n                    <p>[Or paste full transcript here]</p>',
            f'<pre style="white-space: pre-wrap; font-family: inherit; font-size: 0.95em;">{transcript_text}</pre>'
        )
        
        # Write the page
        output_path.write_text(page_content)
        print(f"✓ Created meeting page: {output_path}")
        
        # Generate topic summary for index card
        topics_summary = self.generate_topics_summary(summary['topics'])
        
        return filename, topics_summary
    
    def update_index(self, month, year, meeting_filename, topics_summary):
        """
        Add new meeting card to index.html
        
        Inserts at the beginning of the meeting grid (most recent first).
        """
        index_content = self.index_path.read_text()
        
        # Create new meeting card HTML
        new_card = f'''                <div class="meeting-card">
                    <h3>{month} {year}</h3>
                    <p>Topics: {topics_summary}</p>
                    <a href="meetings/{meeting_filename}">View Meeting →</a>
                </div>
                
'''
        
        # Find the meeting grid and insert at beginning
        grid_pattern = r'(<div class="meeting-grid">)\s*\n'
        
        if re.search(grid_pattern, index_content):
            # Insert after opening meeting-grid div
            index_content = re.sub(
                grid_pattern,
                r'\1\n' + new_card,
                index_content,
                count=1
            )
            
            # Write back
            self.index_path.write_text(index_content)
            print(f"✓ Updated index.html with {month} {year} meeting card")
        else:
            print("⚠ Warning: Could not find meeting-grid in index.html")
            print("  You may need to manually add the meeting card to index.html")
    
    def save_transcript(self, transcript_path, date_str):
        """
        Copy transcript to assets/transcripts folder with proper naming.
        """
        date = datetime.strptime(date_str, '%Y-%m-%d')
        month_name = date.strftime('%B')
        year = date.year
        month_num = date.month
        
        transcript_filename = f"{year}-{month_num:02d}-{month_name.lower()}.txt"
        dest_path = self.site_dir / 'assets' / 'transcripts' / transcript_filename
        
        # Copy transcript
        transcript_text = Path(transcript_path).read_text()
        dest_path.write_text(transcript_text)
        
        print(f"✓ Saved transcript to: {dest_path}")


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Generate meeting page for Pulaski Transparency Website',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add December 2025 meeting
  python3 add_meeting.py --date 2025-12-01 \\
      --audio https://cloudflare.../2025-12-meeting.mp3 \\
      --transcript transcripts/december-2025.txt
  
  # Specify custom site directory
  python3 add_meeting.py --date 2025-12-01 \\
      --audio https://... --transcript transcript.txt \\
      --site-dir /path/to/site
        """
    )
    
    parser.add_argument(
        '--date',
        required=True,
        help='Meeting date in YYYY-MM-DD format (e.g., 2025-12-01)'
    )
    parser.add_argument(
        '--audio',
        required=True,
        help='Full URL to audio file (e.g., https://cloudflare.../meeting.mp3)'
    )
    parser.add_argument(
        '--transcript',
        required=True,
        help='Path to transcript text file'
    )
    parser.add_argument(
        '--site-dir',
        help='Path to website directory (default: current directory)'
    )
    parser.add_argument(
        '--no-index-update',
        action='store_true',
        help='Skip updating index.html (useful for testing)'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate date format
        date = datetime.strptime(args.date, '%Y-%m-%d')
        
        # Validate transcript exists
        if not Path(args.transcript).exists():
            print(f"❌ Error: Transcript file not found: {args.transcript}")
            return 1
        
        # Initialize generator
        generator = MeetingPageGenerator(args.site_dir)
        
        # Save transcript to assets
        generator.save_transcript(args.transcript, args.date)
        
        # Generate meeting page
        meeting_filename, topics_summary = generator.create_meeting_page(
            args.date,
            args.audio,
            args.transcript
        )
        
        # Update index unless disabled
        if not args.no_index_update:
            month_name = date.strftime('%B')
            generator.update_index(month_name, date.year, meeting_filename, topics_summary)
        
        print("\n✅ Meeting page generation complete!")
        print(f"\nNext steps:")
        print(f"1. Review the generated page: meetings/{meeting_filename}")
        print(f"2. Check index.html for the new meeting card")
        print(f"3. Test in browser: open index.html")
        print(f"4. Deploy: git add . && git commit -m 'Add {date.strftime('%B %Y')} meeting' && git push")
        
    except ValueError as e:
        print(f"❌ Error: Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-01)")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
