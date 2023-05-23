# Unstability.ai Scripts

## Why?
I don't know.
I just fill the gaps they didn't take care of.
### 1 - History Downloader
Downloads your Image history to a subfolder
Skips Duplicates (if its ran twice)
Downloads all batchinfos (settings, promts)

  pip install asyncio aiohttp tqdm
  
  python history_dl.py 516a2cq1-5871-41ag-h1c6-en22aa66c118

You need to supply your AuthToken (the funny letters above)
How to get them?

1. Go to unstability.ai and login
2. Press F12
3. Navigate to your Storage Tab in Firefox (Chrome noobs have to go to "Application")
4. Go to Cookies and select the "__Secure-next-auth.session-token" Copy the value. Thats your AuthToken

# Idiot Disclaimer: DO NOT SHARE THAT TOKEN WITH ANYONE
