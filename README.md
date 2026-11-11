# English Terms Screensaver

A Python screensaver that displays English technical terms, pronunciation, and a short English definition. It uses a black background, white terms, yellow pronunciation in parentheses, and smaller white definitions. A new term appears every **20 seconds**.

## Run with a double-click

1. Install **Python 3.10 or later** from [python.org](https://www.python.org/downloads/), including Tcl/Tk. Enable **Add Python to PATH** during installation.
2. Download the repository using **Code → Download ZIP** and extract it.
3. Double-click `start_screensaver.bat`.

No additional Python packages or large dictionary database are required. An internet connection is required. The first word appears once a suitable entry has been retrieved; a connection status message is shown while loading. Press any key, click, or move the mouse to exit.

## Standalone Windows `.scr` without Python

The source ZIP does not include a compiled `.scr` file. You can build one in either of these ways:

- **On GitHub:** upload the project, including `.github`, then open **Actions → Build Windows screensaver → Run workflow**. After a successful build, download and extract the **EnglishTermsScreensaver-Windows** artifact.
- **Locally on Windows:** with Python installed, double-click `build_windows.bat`. The first build downloads PyInstaller into a dedicated virtual environment. The output is `dist/EnglishTermsScreensaver.scr`.

The resulting `.scr` includes Python and the application. It does not require adjacent `.py` or `.bat` files or paths to the original computer. It still requires internet access for the dictionary. Double-click it to run, or right-click → **Install** to open Windows screensaver settings. Keep the file in a permanent location. Copying it to System32 is unnecessary.

Supported Windows arguments: `/s` runs the screensaver and `/c` shows information. `/p HWND` exits without opening a window: the embedded preview in Windows settings is not implemented yet. The full-screen **Preview** button uses `/s`.

## Dictionary and limitations

- Candidate words come from technical categories on English [Wiktionary](https://en.wiktionary.org/) through the [MediaWiki API](https://www.mediawiki.org/wiki/API:Categorymembers): computing, mathematics, physics, engineering, and chemistry.
- Pronunciation and definitions come from the [Free Dictionary API](https://dictionaryapi.dev/). Only entries containing both a definition and IPA pronunciation are accepted. The shortest available definition is selected; definitions are not automatically translated or simplified.
- This is not a bundled database of 200,000 words. The available selection depends on the categories and coverage of both services; no specific count or exclusively technical meaning is guaranteed. Candidates are sampled alphabetically rather than uniformly across the entire dictionary. Words may have multiple meanings.
- No API keys, accounts, or persistent dictionary storage are required. Memory holds up to eight prepared entries and a history of the last 500 words. These are discarded when the application closes.
- Network requests run in a separate thread. During an outage, the last word remains visible while the application retries. If no new entry is ready, the current word stays longer than 20 seconds. Starting without internet access displays a status message.
- External services may limit requests or change their interfaces. The application waits between requests and after errors. Edit `CATEGORIES` to change the selection and `INTERVAL` to change the timing at the beginning of `screensaver.py`.
- The screensaver uses the primary display. It does not replace Windows screen locking and has no built-in dictionary content filter.

## Development

```console
python screensaver.py
python -m unittest discover -s tests -v
```

The application uses only the Python standard library and Tkinter. Building a `.scr` requires Windows. The GitHub workflow runs manually or when a `v*` tag is pushed; it saves the result as an artifact and does not automatically publish a GitHub Release.

## Content and licensing

The project's source files are provided under the license in `LICENSE`. Dictionary data is not covered by that license. Each displayed entry includes a source link; any further use of the data must respect the original content licenses and provider terms. See [Wiktionary copyright](https://en.wiktionary.org/wiki/Wiktionary:Copyrights) and the [Free Dictionary API](https://github.com/meetDeveloper/freeDictionaryAPI).
