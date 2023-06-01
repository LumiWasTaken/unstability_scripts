# Unstability.ai Scripts

## Why?
I don't know.

I just fill the gaps they didn't take care of.

## What is Python, How do i get it?
### Python is a programming language.
- To use this Script you need to have Python installed on your PC. 
- I have tested it with Python 3.10 (Link: https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe)
- Download and install python
- IMPORTANT: CHECK "ADD TO PATH"
- (follow below)

### 1 - History Downloader (Have python installed)
- Downloads your Image history to a subfolder
- Skips Duplicates (if its ran twice)
- Downloads all batchinfos (settings, prompts)

    pip install asyncio aiohttp tqdm
  
    python history_dl.py 516a2cq1-5871-41ag-h1c6-en22aa66c118

You need to supply your AuthToken (the funny letters above)
How to get them?

1. Go to unstability.ai and login
2. Press F12
3. Navigate to your Storage Tab in Firefox (Chrome noobs have to go to "Application")
4. Go to Cookies and select the "__Secure-next-auth.session-token" Copy the value. Thats your AuthToken

# Idiot Disclaimer: DO NOT SHARE THAT TOKEN WITH ANYONE

# Examples:
![History_Folder](https://github.com/LumiWasTaken/unstability_scripts/assets/49376128/188113c6-0ee9-4ea9-9733-0d118ec4f1c8)
![Image_Folder](https://github.com/LumiWasTaken/unstability_scripts/assets/49376128/9ddc1927-6506-4154-abc5-949bcc23be1b)
![Image_Prompt](https://github.com/LumiWasTaken/unstability_scripts/assets/49376128/28174c56-b6c7-47bf-aaf3-a82712614101)
