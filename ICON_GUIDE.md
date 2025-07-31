# Creating an Executable Icon (Optional)

To include a custom icon in your Windows executable, you need an `.ico` file.

## Quick Icon Creation

### Option 1: Online Converter
1. Find or create a PNG/JPG image (preferably 256x256 or 512x512)
2. Use an online converter like:
   - https://convertio.co/png-ico/
   - https://www.icoconvert.com/
   - https://favicon.io/favicon-converter/
3. Save as `icon.ico` in the project root

### Option 2: Using Python (Pillow)
```python
from PIL import Image

# Convert PNG to ICO
img = Image.open('your_image.png')
img.save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
```

### Option 3: Default Icon
If no `icon.ico` file is present, PyInstaller will use the default Python icon.

## Icon Requirements
- Format: ICO (Windows Icon)
- Recommended sizes: 16x16, 32x32, 48x48, 64x64, 128x128, 256x256
- For best results, start with a square image at least 256x256 pixels
