# Pulaski Township Transparency Project - Website

This is the HTML/CSS version of your Pulaski Township Transparency website, migrated from Canva.

## 📁 Structure

```
pulaski-transparency-site/
├── index.html              # Home page
├── css/
│   └── style.css          # All styling
├── meetings/              # Individual meeting pages
│   ├── 2025-02-february.html
│   ├── 2025-03-march.html
│   ├── 2025-04-april.html
│   └── 2025-06-june.html
└── assets/                # Media files (you'll add these)
    ├── audio/            # Meeting recordings (.mp3)
    └── transcripts/      # Full text transcripts (.txt)
```

## 🚀 How to View

1. **Open locally**: Just double-click `index.html` in Finder to open in your browser
2. **Test navigation**: Click through the meeting cards to see each meeting page
3. **Interactive elements**: The collapsible sections work with JavaScript

## 📝 What's Included

✅ Full migration of your Canva content
✅ Clean, professional design
✅ Responsive (works on mobile)
✅ Collapsible sections for easy reading
✅ Audio player integration with Cloudflare hosting
✅ Download links for recordings and transcripts
✅ **NEW: Resident request form** for RTK requests

## 🔧 Next Steps

### To Complete the Site:

1. **Add Audio Files**
   - Place meeting recordings in `assets/audio/`
   - Name them: `2025-02-february.mp3`, etc.

2. **Add Transcripts**
   - Place full text transcripts in `assets/transcripts/`
   - Name them: `2025-02-february.txt`, etc.

3. **Update Contact Info**
   - Edit `index.html` and add your email in the Contact section

4. **Add More Meetings**
   - Copy any meeting HTML file as a template
   - Update the date, content, and links
   - Add it to the meeting grid on `index.html`

### To Deploy Online:

**Option 1: GitHub Pages (Recommended)**
1. Create a GitHub account (free)
2. Create a new repository called "pulaski-transparency"
3. Upload all files
4. Enable GitHub Pages in repository settings
5. Your site will be live at: `yourusername.github.io/pulaski-transparency`

**Option 2: Cloudflare Pages**
1. Create a Cloudflare account (free)
2. Connect your GitHub repo (or upload files directly)
3. Deploy with one click
4. Get custom domain if desired

## 🔄 Integration with Your Transparency Bot

You can automate updates by having your Python scripts:
1. Generate new meeting HTML from templates
2. Commit/push to GitHub
3. Site updates automatically

## 🎨 Customization

- **Colors**: Edit the `:root` variables in `css/style.css`
- **Layout**: Modify the grid in `css/style.css`
- **Content**: Update any HTML file directly

## 📱 Mobile Friendly

The site automatically adjusts for:
- Desktop computers
- Tablets
- Mobile phones

## ⚖️ Legal Notes

- All content is already properly disclaimed
- Meeting recordings are public records
- Attribution is built into the footer

## 🆘 Need Help?

If you need to:
- Add new features
- Integrate with your RTK automation
- Create the request form for residents
- Deploy to hosting

Just let me know and we'll tackle it next!

---

**Current Status**: ✅ Ready for your review and testing
**Next Phase**: Add audio files, deploy online, build request form
