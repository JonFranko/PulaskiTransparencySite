#!/usr/bin/env python3
"""
RTK Request Form Generator for Residents
This script generates pre-filled RTK request forms for Pulaski Township residents
"""

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyMuPDF'])
    import fitz


class ResidentRTKFormGenerator:
    """Generate RTK request forms for residents"""
    
    def __init__(self, template_path):
        self.template_path = Path(template_path)
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
    
    def format_meeting_date(self, meeting_date_str):
        """Convert YYYY-MM format to 'Month YYYY'"""
        year, month = meeting_date_str.split('-')
        date_obj = datetime(int(year), int(month), 1)
        return date_obj.strftime('%B %Y')
    
    def generate_form_from_json(self, json_path, output_path=None):
        """Generate filled RTK form from JSON data"""
        
        # Load resident data
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Set default output path if not provided
        if output_path is None:
            meeting_date = data['meetingDate'].replace('-', '_')
            output_path = f"RTK_Request_{data['fullName'].replace(' ', '_')}_{meeting_date}.pdf"
        
        # Open the PDF template
        doc = fitz.open(self.template_path)
        page = doc[0]  # Assuming single page form
        
        # Format the meeting date
        meeting_text = self.format_meeting_date(data['meetingDate'])
        records_request = f"I would like a copy of the recording of the {meeting_text} supervisors meeting"
        
        # Try to fill form fields if they exist
        if page.widgets():
            print("Filling form fields...")
            for widget in page.widgets():
                field_name = widget.field_name.lower() if widget.field_name else ""
                
                # Map form fields to data
                if 'name' in field_name and 'agency' not in field_name:
                    widget.field_value = data['fullName']
                    widget.update()
                elif 'email' in field_name:
                    widget.field_value = data['email']
                    widget.update()
                elif 'address' in field_name or 'street' in field_name:
                    widget.field_value = data['address']
                    widget.update()
                elif 'city' in field_name:
                    widget.field_value = data['city']
                    widget.update()
                elif 'state' in field_name:
                    widget.field_value = data['state']
                    widget.update()
                elif 'zip' in field_name or 'postal' in field_name:
                    widget.field_value = data['zip']
                    widget.update()
                elif 'phone' in field_name or 'telephone' in field_name:
                    if data.get('phone'):
                        widget.field_value = data['phone']
                        widget.update()
                elif 'agency' in field_name:
                    widget.field_value = "Pulaski Township"
                    widget.update()
                elif 'record' in field_name or 'request' in field_name or 'description' in field_name:
                    widget.field_value = records_request
                    widget.update()
                elif 'date' in field_name and 'meeting' not in field_name:
                    widget.field_value = datetime.now().strftime('%m/%d/%Y')
                    widget.update()
        
        # Also add text overlays as backup (in case form fields don't work)
        # These coordinates would need to be adjusted based on your actual form
        overlay_data = {
            'Agency Name': (150, 100, "Pulaski Township"),
            'Your Name': (150, 150, data['fullName']),
            'Email': (150, 180, data['email']),
            'Address': (150, 210, data['address']),
            'City': (150, 240, data['city']),
            'State': (380, 240, data['state']),
            'ZIP': (450, 240, data['zip']),
            'Phone': (150, 270, data.get('phone', '')),
            'Date': (150, 300, datetime.now().strftime('%m/%d/%Y')),
            'Records Request': (150, 400, records_request),
        }
        
        # Note: You'll need to adjust coordinates based on your actual form
        # This is a template - coordinates should be customized
        
        # Save the filled PDF
        doc.save(output_path)
        doc.close()
        
        print(f"✓ Generated form: {output_path}")
        return output_path
    
    def generate_form_from_dict(self, data_dict, output_path=None):
        """Generate filled RTK form from dictionary data"""
        # Create temporary JSON file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data_dict, f)
            temp_json = f.name
        
        try:
            result = self.generate_form_from_json(temp_json, output_path)
            return result
        finally:
            Path(temp_json).unlink()


def main():
    """Command line interface for generating forms"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate RTK request forms for Pulaski Township residents'
    )
    parser.add_argument(
        'json_file',
        help='JSON file with resident information (from website form)'
    )
    parser.add_argument(
        '--template',
        default='RTK_Request_Form_Template.pdf',
        help='Path to blank RTK form template (default: RTK_Request_Form_Template.pdf)'
    )
    parser.add_argument(
        '--output',
        help='Output PDF path (default: auto-generated)'
    )
    
    args = parser.parse_args()
    
    try:
        generator = ResidentRTKFormGenerator(args.template)
        output_path = generator.generate_form_from_json(args.json_file, args.output)
        
        print(f"\n✓ Success! Generated RTK request form:")
        print(f"  {output_path}")
        print(f"\nResident should:")
        print(f"  1. Review and sign the form")
        print(f"  2. Mail to: Pulaski Township, 3478 Perry Highway, Hadley, PA 16130")
        print(f"  3. Or deliver in person during office hours")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
