import json
import re
import subprocess
from difflib import SequenceMatcher

PDF_DIR = "pdf"
POSTS_FILE = "/Users/mariabusueva/Documents/Maria/life/tg/jetmetrics_posts.md"
DATA_FILE = "data.json"
OUT_FILE = "tg_match_review.md"
JSON_OUT = "tg_match_results.json"

FOOTER_MARKERS = ("jetmetrics.io", "dmitry nekrasov", "pro-workspace", "t.me/jetmetrics")
HEADLINE_LINES = 4
# Roundup/digest posts that briefly name-drop many cheatsheets — never a canonical match.
EXCLUDE_POST_NUMS = {243, 349}


def extract_headline(path):
    result = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True)
    lines = [l.strip() for l in result.stdout.split("\n") if l.strip()]
    lines = [l for l in lines if not any(m in l.lower() for m in FOOTER_MARKERS)]
    # drop decorative lines that are just digits/emoji/symbols, no letters
    def has_letters(s):
        return bool(re.search(r"[a-zA-Zа-яА-ЯёЁ]{2,}", s))
    lines = [l for l in lines if has_letters(l)]
    return " ".join(lines[:HEADLINE_LINES])


def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-zа-яё0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_posts(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"\n## Пост #", content)
    posts = []
    for block in blocks[1:]:
        header, _, body = block.partition("\n")
        m = re.match(r"(\d+)\s*—\s*(.+)", header)
        if not m:
            continue
        num = int(m.group(1))
        date = m.group(2).strip()
        text = body.strip()
        if text.rstrip().endswith("---"):
            text = text.rstrip()[:-3].strip()
        if num in EXCLUDE_POST_NUMS:
            continue
        posts.append({"num": num, "date": date, "text": text, "norm": norm(text)})
    return posts


def coverage(headline_norm, post_norm):
    if not headline_norm:
        return 0.0
    sm = SequenceMatcher(None, headline_norm, post_norm, autojunk=False)
    blocks = sm.get_matching_blocks()
    covered = sum(b.size for b in blocks if b.size >= 3)
    return covered / len(headline_norm)


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    items = data["items"]

    posts = parse_posts(POSTS_FILE)

    results = []
    for item in items:
        pdf_path = f"{PDF_DIR}/{item['id']}.pdf"
        headline = norm(extract_headline(pdf_path))

        scored = []
        for p in posts:
            s = coverage(headline, p["norm"])
            scored.append((s, p))
        scored.sort(key=lambda x: -x[0])

        top3 = scored[:3]
        results.append({
            "id": item["id"],
            "title": item["title"],
            "headline_extracted": headline,
            "candidates": [
                {
                    "post_num": p["num"],
                    "date": p["date"],
                    "score": round(s, 3),
                    "snippet": p["text"][:280].replace("\n", " "),
                }
                for s, p in top3
            ],
        })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("# TG post matching — top 3 candidates per cheatsheet (for manual review)\n\n")
        for r in results:
            f.write(f"## {r['id']} — {r['title']}\n")
            f.write(f"Заголовок из PDF: {r['headline_extracted']}\n\n")
            for c in r["candidates"]:
                f.write(f"- score={c['score']} **#{c['post_num']}** ({c['date']}) https://t.me/jetmetrics/{c['post_num']}\n")
                f.write(f"  > {c['snippet']}\n")
            f.write("\n---\n\n")

    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Wrote top-3 candidates for", len(results), "items to", OUT_FILE)


if __name__ == "__main__":
    main()
