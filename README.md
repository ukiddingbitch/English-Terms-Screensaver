# English Terms Screensaver

Learn English technical vocabulary while your screen is idle.

A Python screensaver that displays technical terms, IPA pronunciation, and short English definitions on a clean black background. Words are fetched online, so there is no large dictionary database to download.

## Features

- English technical vocabulary from computing, mathematics, physics, engineering, and chemistry.
- White terms with yellow pronunciation in parentheses.
- Smaller white definitions beneath each term.
- New terms every 20 seconds when entries are available.
- Background fetching to keep the interface responsive.
- No API keys or accounts.
- No additional Python packages required to run from source.
- Build a standalone Windows `.scr` that runs without Python installed.

## Quick start

### Run from source

1. Install **Python 3.10 or later** from [python.org](https://www.python.org/downloads/).
2. Include **Tcl/Tk** and enable **Add Python to PATH** during installation.
3. Download this repository using **Code → Download ZIP**.
4. Extract the ZIP.
5. Double-click **`start_screensaver.bat`**.

Alternatively, run:

```bash
python screensaver.py
```

An internet connection is required. A loading message appears until the first suitable entry is available.

Press any key, click, or move the mouse to exit.

## Build a standalone Windows screensaver

The source repository does not include a compiled `.scr` file.

### Build with GitHub Actions

1. Upload the project to GitHub, including the `.github` directory.
2. Open the repository's **Actions** tab.
3. Select **Build Windows screensaver**.
4. Click **Run workflow**.
5. Once the build finishes, download the **EnglishTermsScreensaver-Windows** artifact.
6. Extract `EnglishTermsScreensaver.scr`.

The workflow also runs when a tag matching `v*` is pushed. It uploads a build artifact; it does not automatically publish a GitHub Release.

### Build locally

On Windows with Python installed, double-click:

```text
build_windows.bat
```

The build script creates an isolated virtual environment and installs PyInstaller. The resulting screensaver is saved to:

```text
dist/EnglishTermsScreensaver.scr
```

The compiled file includes Python and the application. It does not require the original source files, but it still needs internet access to retrieve dictionary entries.

## Use as a Windows screensaver

Keep the compiled `.scr` file in a permanent location.

- **Double-click** to run it.
- **Right-click → Install** to open Windows screensaver settings.

Copying the file to `System32` is unnecessary.

### Windows arguments

| Argument | Behavior |
|----------|----------|
| `/s` | Runs the screensaver |
| `/c` | Displays application information |
| `/p HWND` | Exits without opening a window |

The embedded preview inside Windows settings is not implemented. Use the full-screen **Preview** button to try the screensaver.

## How it works

1. The application samples candidate terms from technical categories on English Wiktionary.
2. It requests definitions and pronunciation from the Free Dictionary API.
3. Entries without both a definition and IPA pronunciation are skipped.
4. Suitable entries are buffered in memory and displayed in sequence.

The shortest available definition is selected. Definitions are not automatically simplified or translated, and a word's selected definition may describe a nontechnical meaning.

## Configuration

Edit the constants near the beginning of `screensaver.py`.

### Display interval

The interval is measured in seconds:

```python
INTERVAL = 20
```

### Vocabulary categories

```python
CATEGORIES = [
    "en:Computing",
    "en:Mathematics",
    "en:Physics",
    "en:Engineering",
    "en:Chemistry",
]
```

Category names must correspond to existing English Wiktionary categories.

Rebuild the `.scr` after changing the source.

## Requirements and limitations

- Source execution requires Python 3.10+ with Tkinter.
- Standalone `.scr` builds require Windows.
- Internet access is required to retrieve new entries.
- No fixed vocabulary size is guaranteed; this is not a bundled database of 200,000 words.
- Availability depends on category membership, API coverage, and pronunciation data.
- Sampling is alphabetical rather than uniform across the entire dictionary.
- If no new entry is ready, the current word remains visible beyond the configured interval.
- During a network outage, the application keeps the last entry visible and retries.
- Vocabulary is stored only in memory and discarded when the application closes.
- The application uses the primary display.
- Dictionary content has no built-in content filter.
- The screensaver does not replace Windows screen locking.

## Development

Run the application:

```bash
python screensaver.py
```

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

The application uses the Python standard library and Tkinter. PyInstaller is required only for building the standalone Windows version.

## Validation status

Four automated tests have passed, covering dictionary response parsing, missing pronunciation, HTTP error handling, and Windows argument parsing.

Live dictionary retrieval, the compiled `.scr`, Windows installation, and full-screen visual behavior remain unverified. See [VALIDATION.md](VALIDATION.md) for details.

## Data sources

- [English Wiktionary](https://en.wiktionary.org/)
- [MediaWiki API](https://www.mediawiki.org/wiki/API:Categorymembers)
- [Free Dictionary API](https://dictionaryapi.dev/)

Each displayed entry includes a source link. External services may impose request limits or change their interfaces.

## License

The application source code is licensed under the [MIT License](LICENSE).

Dictionary content is subject to its original licenses and provider terms, separately from the application code. See [Wiktionary copyrights](https://en.wiktionary.org/wiki/Wiktionary:Copyrights) and the [Free Dictionary API project](https://github.com/meetDeveloper/freeDictionaryAPI).
