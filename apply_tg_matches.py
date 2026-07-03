import json

# id -> post number, or None if no confident match found
MATCHES = {
    "cs-001": 260, "cs-002": 261, "cs-003": None, "cs-004": 266, "cs-005": None,
    "cs-006": 269, "cs-007": 272, "cs-008": None, "cs-009": 273, "cs-010": None,
    "cs-011": 279, "cs-012": 282, "cs-013": 278, "cs-014": 284, "cs-015": 283,
    "cs-016": 290, "cs-017": 285, "cs-018": None, "cs-019": None, "cs-020": 296,
    "cs-021": 297, "cs-022": 298, "cs-023": 299, "cs-024": 308, "cs-025": None,
    "cs-026": 302, "cs-027": None, "cs-028": None, "cs-029": 306, "cs-030": 309,
    "cs-031": 318, "cs-032": 319, "cs-033": 120, "cs-034": 322, "cs-035": 323,
    "cs-036": 324, "cs-037": 328, "cs-038": 330, "cs-039": 331, "cs-040": 335,
    "cs-041": 336, "cs-042": 337, "cs-043": None, "cs-044": 360, "cs-045": 362,
    "cs-046": 410, "cs-047": 365, "cs-048": 389, "cs-049": None, "cs-050": 387,
    "cs-051": 388, "cs-052": None, "cs-053": 404, "cs-054": 406, "cs-055": 407,
    "cs-056": 408, "cs-057": None, "cs-058": 413, "cs-059": 412, "cs-060": 417,
    "cs-061": 418, "cs-062": 420, "cs-063": 422, "cs-064": 431, "cs-065": 432,
    "cs-066": None, "cs-067": None, "cs-068": None, "cs-069": None, "cs-070": None,
    "cs-071": None, "cs-072": None, "cs-073": None, "cs-074": None, "cs-075": 436,
    "cs-076": 437, "cs-077": 439, "cs-078": None, "cs-079": None, "cs-080": 211,
    "cs-081": 263, "cs-082": 237, "cs-083": None, "cs-084": None, "cs-085": None,
    "cs-086": None, "cs-087": None, "cs-088": None, "cs-089": 214, "cs-090": None,
    "cs-091": 244, "cs-092": None, "cs-093": 403, "cs-094": None, "cs-095": None,
    "cs-096": 225, "cs-097": 253, "cs-098": 251, "cs-099": 235, "cs-100": 257,
    "cs-101": 231,
}

with open("data.json", encoding="utf-8") as f:
    data = json.load(f)

matched, unmatched = 0, []
for item in data["items"]:
    post_num = MATCHES.get(item["id"])
    if post_num:
        item["tg_post"] = f"https://t.me/jetmetrics/{post_num}"
        matched += 1
    else:
        item["tg_post"] = None
        unmatched.append(f"{item['id']} — {item['title']}")

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Matched: {matched}/{len(data['items'])}")
print("\nUnmatched:")
for u in unmatched:
    print(" -", u)
