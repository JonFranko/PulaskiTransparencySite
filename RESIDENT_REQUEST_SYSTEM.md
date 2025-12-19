# Resident Request System - Setup Guide

## Overview

This system allows Pulaski Township residents to generate their own RTK request forms for meeting recordings. This serves multiple strategic purposes:

1. **Demonstrates public demand** for transparency
2. **Puts pressure on the township** to post recordings proactively
3. **Creates documentation** that residents are exercising their rights
4. **Reduces your workload** by empowering residents to request directly
5. **Builds the case** that the township should either:
   - Host recordings themselves, OR
   - Pay you to manage their transparency infrastructure

## Current Status: Phase 1 (Manual Processing)

Right now, the system works like this:

1. Resident fills out form on `request.html`
2. System downloads a JSON file with their info
3. Resident emails you the JSON file
4. You run the Python script to generate their PDF
5. You email them the completed PDF
6. They mail it to the township

This is a good start because it:
- Costs you nothing to host
- Requires no backend server
- Works immediately
- Builds momentum for transparency

## Files Created

```
pulaski-transparency-site/
├── request.html                    ← New resident request page
├── generate_resident_form.py       ← Script to generate PDFs
└── [existing files...]
```

## How to Use (Current Phase 1)

### For Residents (Website Instructions)

1. Visit `request.html` on your site
2. Fill out their contact information
3. Select which meeting they want
4. Click "Generate My Request Form"
5. Save the JSON file
6. Email it to you at jon@doubletreeindustries.com

### For You (Processing Requests)

When a resident sends you a JSON file:

```bash
# Navigate to your site directory
cd /Users/JonathanFranko/Documents/Claude/pulaski-transparency-site/

# Generate their PDF (make sure you have the RTK template in this folder)
python3 generate_resident_form.py resident-request.json --template path/to/RTK_Form.pdf

# Email the resulting PDF back to them
```

The script will create a PDF named like:
`RTK_Request_Jane_Doe_2025_12.pdf`

## Future Phases

### Phase 2: Automated PDF Generation (When You Deploy)

When you're ready to add a backend server:

**Option A: Simple Serverless (Cloudflare Workers)**
- Free tier: 100,000 requests/day
- Can run Python script
- Generates PDF and returns download link
- No server maintenance

**Option B: Python Flask API**
- Hosted on your existing infrastructure
- Full control
- Can add email delivery
- Database tracking of requests

### Phase 3: Subscription Service (Future)

Eventually, you could offer:

**Monthly Subscription ($5-10/month)**
- Automatically generates and files RTK request every month
- Emails resident when recording is received
- Maintains their request history
- Premium: Includes transcript delivery

This creates:
1. Revenue stream for you
2. Sustained pressure on township
3. Documentation of consistent public demand
4. Justification for township to host recordings themselves

## Integration with Your Existing Bot

Your `pulaski_rtk_bot.py` already has the logic for:
- Date calculations (first Monday of month)
- Form field mapping
- PDF generation

The `generate_resident_form.py` script is adapted from your bot to:
- Accept resident info instead of hard-coded info
- Process JSON input from website
- Use same PDF filling technique

## Strategic Positioning

### The Pitch to the Township

Once you have 10-20 residents regularly requesting recordings:

> "Supervisor Zinga,
> 
> Over the past [X] months, [Y] residents have filed RTK requests for meeting recordings. This is creating administrative burden for the township and demonstrates clear public demand.
>  
> I propose two solutions:
> 
> 1. **Township hosts recordings** on your website (I can provide technical assistance)
> 2. **Contract my services** to manage transparency infrastructure ($XXX/month)
> 
> Either way, proactive posting would:
> - Eliminate RTK request paperwork
> - Fulfill your campaign promises
> - Save township staff time
> - Serve residents better
> 
> Let's discuss."

### The Business Model

If the township contracts you:

**Monthly Fee: $500-1,000**
- Post meeting recordings within 48 hours
- Provide transcripts and summaries
- Manage transparency portal
- Handle RTK requests
- Monthly transparency reports

**Cost to township:** Less than dealing with RTK requests
**Value to you:** Sustainable income + you're doing it anyway
**Win for residents:** Professional, reliable transparency

## Next Steps

### Immediate (This Week)
1. ✅ Add request form to website
2. Test the form and Python script
3. Add clear instructions for residents
4. Update navigation to include "Request Recordings"

### Short Term (This Month)
1. Deploy website with request form
2. Promote the request feature to residents
3. Process first few requests manually
4. Track how many residents use it

### Medium Term (Next 3 Months)
1. Collect data on request volume
2. Build case with documentation
3. Approach township with proposal
4. Consider adding automated backend

### Long Term (6-12 Months)
1. Either township takes over, or
2. Township contracts you, or
3. You launch subscription service

## Technical Notes

### Current Limitations

**Phase 1 (Current):**
- Manual processing required
- No automated PDF generation
- No email delivery
- JSON file exchange

**Why this is OK:**
- Zero hosting costs
- No security concerns
- Simple to maintain
- Proves demand first

### When to Upgrade

Add automated backend when:
- You're processing 10+ requests/week, OR
- Township shows interest in contracting, OR  
- You want to launch subscription service

## Support

For questions or issues:
- Email: jon@doubletreeindustries.com
- Website: doubletreeindustries.com

---

**Current Phase**: ✓ Manual JSON → PDF generation
**Next Phase**: Automated backend (when demand warrants)
**End Goal**: Township hosts or pays you to manage
