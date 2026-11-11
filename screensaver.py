"""Online English vocabulary screensaver. Python 3.10+, standard library only."""
from __future__ import annotations

import json
import queue
import random
import sys
import threading
import time
import tkinter as tk
from dataclasses import dataclass
from tkinter import font, messagebox
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

INTERVAL = 20
USER_AGENT = "EnglishTermsScreensaver/1.0 (educational desktop dictionary client)"
CATEGORIES = ["en:Computing", "en:Mathematics", "en:Physics", "en:Engineering", "en:Chemistry"]


def get_json(url):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request, timeout=12) as response:
        return json.load(response)


@dataclass(frozen=True)
class Entry:
    word: str
    pronunciation: str
    definition: str
    source: str


def lookup(word):
    """Only accept entries with both a definition and a real IPA transcription."""
    try:
        data = get_json("https://api.dictionaryapi.dev/api/v2/entries/en/" + quote(word, safe=""))
    except HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    if not isinstance(data, list):
        return None
    for item in data:
        ipa = item.get("phonetic") or next(
            (p["text"] for p in item.get("phonetics", []) if p.get("text")), "")
        definitions = [d["definition"] for m in item.get("meanings", [])
                       for d in m.get("definitions", []) if d.get("definition")]
        if ipa and definitions:
            sources = item.get("sourceUrls", [])
            source = sources[0] if sources else "https://en.wiktionary.org/wiki/" + quote(word)
            return Entry(item.get("word", word), ipa.strip("/[]"),
                         min(definitions, key=len), source)
    return None


def candidates(category):
    """Sample a category at a random alphabetical position, without downloading a corpus."""
    params = {"action": "query", "list": "categorymembers", "format": "json",
              "cmtitle": "Category:" + category, "cmtype": "page", "cmlimit": 40,
              "cmnamespace": 0, "cmsort": "sortkey",
              "cmstartsortkeyprefix": random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
    data = get_json("https://en.wiktionary.org/w/api.php?" + urlencode(params))
    if "error" in data:
        raise RuntimeError(data["error"].get("info", "Wiktionary API error"))
    words = [p["title"] for p in data.get("query", {}).get("categorymembers", [])]
    random.shuffle(words)
    return words


def download(stop, results, status):
    recent = []
    while not stop.is_set():
        try:
            if results.full():
                stop.wait(1)
                continue
            words = candidates(random.choice(CATEGORIES))
            if not words:
                status[0] = "Waiting for dictionary entries..."
                stop.wait(4)
                continue
            for word in words:
                if stop.is_set() or results.full():
                    break
                if word in recent:
                    continue
                entry = lookup(word)
                if entry:
                    results.put_nowait(entry)
                    recent.append(word)
                    recent[:] = recent[-500:]
                    status[0] = ""
                stop.wait(1.5)
            stop.wait(2)
        except Exception:
            # A transient network failure must never close or freeze the screen.
            status[0] = "Dictionary unavailable. Check your internet connection. Retrying..."
            stop.wait(15)


def mode(args):
    if not args:
        return "show"
    first = args[0].lower()
    if first.startswith(("/c", "-c")):
        return "config"
    if first.startswith(("/p", "-p")):
        return "preview"
    return "show"


class Screensaver:
    def __init__(self, root):
        self.root = root
        self.stop = threading.Event()
        self.results = queue.Queue(maxsize=8)
        self.status = ["Connecting to online dictionary..."]
        self.next_change = 0
        self.current = None
        self.started = time.monotonic()
        self.pointer = None
        root.title("English Terms Screensaver")
        root.configure(bg="black", cursor="none")
        root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        root.bind("<Key>", self.close)
        root.bind("<Button>", self.close)
        root.bind("<Motion>", self.motion)
        root.bind("<Configure>", lambda event: self.draw())
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.after(100, root.focus_force)
        threading.Thread(target=download, args=(self.stop, self.results, self.status), daemon=True).start()
        self.tick()

    def close(self, event=None):
        self.stop.set()
        self.root.destroy()

    def motion(self, event):
        point = (event.x_root, event.y_root)
        if time.monotonic() - self.started < 1:
            self.pointer = point
        elif self.pointer is None:
            self.pointer = point
        elif max(abs(point[i] - self.pointer[i]) for i in (0, 1)) > 8:
            self.close()

    def tick(self):
        now = time.monotonic()
        if now >= self.next_change:
            try:
                self.current = self.results.get_nowait()
                self.next_change = now + INTERVAL
            except queue.Empty:
                pass
        self.draw()
        self.root.after(500, self.tick)

    def draw(self):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if w < 10 or h < 10:
            return
        if not self.current:
            c.create_text(w / 2, h / 2, text=self.status[0] or "Loading words...",
                          fill="white", width=w * .8, justify="center", font=("Segoe UI", 22))
            return
        item = self.current
        size = max(16, min(56, int(w / 24), int(h / 12)))
        ipa = " (" + item.pronunciation + ")"
        while size > 10:
            term_font = font.Font(family="Segoe UI", size=size, weight="bold")
            ipa_font = font.Font(family="Segoe UI", size=size)
            total = term_font.measure(item.word) + ipa_font.measure(ipa)
            if total < w * .9:
                break
            size -= 1
        x = (w - total) / 2
        # Measure the wrapped definition so the complete group stays centered.
        definition_id = c.create_text(w / 2, 0, text=item.definition, fill="white",
                                     width=w * .82, justify="center", anchor="n",
                                     font=("Segoe UI", max(12, int(size * .65))))
        bounds = c.bbox(definition_id)
        definition_height = bounds[3] - bounds[1]
        top = max(15, (h - term_font.metrics("linespace") - 24 - definition_height) / 2)
        c.create_text(x, top, anchor="nw", text=item.word, fill="white", font=term_font)
        c.create_text(x + term_font.measure(item.word), top, anchor="nw",
                      text=ipa, fill="#ffd84d", font=ipa_font)
        c.coords(definition_id, w / 2, top + term_font.metrics("linespace") + 24)
        footer = "Wiktionary via Free Dictionary API | " + item.source
        if self.status[0]:
            footer += "\n" + self.status[0]
        c.create_text(w / 2, h - 18, anchor="s", text=footer, fill="#999999",
                      width=w * .9, justify="center", font=("Segoe UI", 10))


def main():
    selected = mode(sys.argv[1:])
    # Windows invokes /p with a parent HWND. Return cleanly instead of opening
    # an unwanted full-screen window inside the Settings preview.
    if selected == "preview":
        return
    root = tk.Tk()
    if selected == "config":
        root.withdraw()
        messagebox.showinfo("English Terms Screensaver",
                            "Online English vocabulary. Words change every 20 seconds.\n"
                            "Internet connection required. No API key or database needed.\n"
                            "Press any key or move the mouse to exit.")
        root.destroy()
        return
    Screensaver(root)
    root.mainloop()


if __name__ == "__main__":
    main()
