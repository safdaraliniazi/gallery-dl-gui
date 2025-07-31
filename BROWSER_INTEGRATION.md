# Browser Integration Setup (Optional)

The Gallery-DL GUI now includes enhanced web preview functionality. For the best experience, you may want to install additional packages for better browser integration.

## Current Implementation

The web preview currently uses:
- **Built-in HTML generation**: Creates HTML pages with embedded iframes
- **Temporary file system**: Generates preview files that open in your default browser
- **Direct browser integration**: "Open Preview in Browser" buttons for real website viewing

## Optional Enhancements

For even better integration, you can install:

### 1. CEF Python (Chrome Embedded Framework)
```bash
pip install cefpython3
```
This would allow embedding a real Chrome browser directly in the application.

### 2. Tkinter HTML
```bash
pip install tkinter-html
```
For basic HTML rendering within tkinter.

### 3. WebView2 (Windows only)
```bash
pip install webview
```
For Windows-specific web integration.

## Current Features (No additional packages required)

✅ **Real Website Previews**: Click any supported site to see preview
✅ **Browser Integration**: "Open in Browser" and "Open Preview in Browser" buttons  
✅ **Responsive Layout**: 40/60 split with resizable panes
✅ **Better Space Usage**: Compact info section, full-height sites list
✅ **Enhanced UI**: Simplified columns, better organization

## How It Works

1. **Site Selection**: Click any site in the list
2. **HTML Generation**: Creates a preview HTML page with:
   - Site information and URL
   - Embedded iframe of the actual website
   - Usage instructions for Gallery-DL
   - Quick action buttons
3. **Browser Preview**: Opens the generated HTML in your default browser
4. **Direct Access**: Option to open the site directly

The current implementation provides excellent functionality without requiring any additional dependencies!
