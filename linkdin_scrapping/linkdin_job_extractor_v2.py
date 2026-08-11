import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# REMOVED inner double quotes so search is broader and actually returns posts
SEARCH_KEYWORDS = [
    '"Machine Learning Remote Job"',
    '"AI ML Remote Job"',
    '"Generative AI Remote Job"',
    '"Agentic AI Remote Job"',
    '"Data Scientist Remote Job"',
    '"AI Developer Remote Job"',
    '"Python Developer Remote Job"'
]

BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "output"
AUTH_DIR = BASE_DIR / "playwright" / ".auth"
AUTH_FILE = AUTH_DIR / "linkedin_user.json"

CSV_OUTPUT_FILE = OUTPUT_DIR / "job_posts.csv"
JSON_OUTPUT_FILE = OUTPUT_DIR / "job_posts.json"

SCROLL_PAUSE_SECONDS = 3
MAX_SCROLL_ROUNDS = 20
PAGE_TIMEOUT_MS = 600000

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AUTH_DIR.mkdir(parents=True, exist_ok=True)


def normalize_email(email: str) -> str:
    email = email.strip()
    email = re.sub(r"[)\]}>.,;:!?]+$", "", email)
    return email


def deobfuscate_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\s*[\(\[\{]\s*at\s*[\)\]\}]\s*", "@", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*[\(\[\{]\s*dot\s*[\)\]\}]\s*", ".", text, flags=re.IGNORECASE)
    return text


def find_emails(text: str) -> list[str]:
    clean_text = deobfuscate_text(text)
    raw_matches = EMAIL_REGEX.findall(clean_text or "")
    emails = set()
    for m in raw_matches:
        norm = normalize_email(m)
        if norm:
            emails.add(norm)
    return sorted(list(emails))


def save_jobs_data(job_records: list[dict]):
    fieldnames = [
        "keyword",
        "author_name",
        "author_url",
        "post_url",
        "date_posted",
        "emails",
        "post_text",
    ]

    with open(CSV_OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(job_records)

    with open(JSON_OUTPUT_FILE, mode="w", encoding="utf-8") as f:
        json.dump(job_records, f, indent=2, ensure_ascii=False)


def is_logged_in(page) -> bool:
    selectors = [
        'input[placeholder*="Search"]',
        'input[aria-label*="Search"]',
        '[data-test-global-nav-search-input]',
        'a[href*="/feed/"]',
    ]
    for selector in selectors:
        try:
            page.locator(selector).first.wait_for(state="visible", timeout=4000)
            return True
        except Exception:
            pass
    return False


def wait_for_manual_login(page, context):
    page.goto("https://www.linkedin.com/", wait_until="domcontentloaded", timeout=PAGE_TIMEOUT_MS)

    if is_logged_in(page):
        context.storage_state(path=str(AUTH_FILE))
        return

    print("\nPlease log in to LinkedIn manually in the opened browser window.")
    print("When login is complete and home page is visible, press ENTER here.\n")
    input()

    page.wait_for_load_state("domcontentloaded")
    if not is_logged_in(page):
        print("Login not detected. Exiting.")
        sys.exit(1)

    context.storage_state(path=str(AUTH_FILE))


def go_to_posts_search(page, keyword: str):
    # Clean Search URL that LinkedIn natively supports
    url = f"https://www.linkedin.com/search/results/content/?keywords={quote(keyword)}"
    page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT_MS)
    page.wait_for_timeout(4000)


def expand_post_if_needed(post):
    more_selectors = [
        'button:has-text("see more")',
        'button:has-text("See more")',
        'span:has-text("see more")',
        'span:has-text("See more")',
    ]
    for selector in more_selectors:
        try:
            more_btn = post.locator(selector).first
            if more_btn.is_visible(timeout=300):
                more_btn.click(timeout=800)
                post.page.wait_for_timeout(300)
                return True
        except Exception:
            pass
    return False


def extract_post_details(post, keyword: str) -> dict:
    expand_post_if_needed(post)

    try:
        post_text = post.inner_text(timeout=2000).strip()
    except Exception:
        post_text = ""

    emails = find_emails(post_text)

    # Post URL or URN
    urn = post.get_attribute("data-urn") or post.get_attribute("data-chameleon-result-urn") or ""
    post_url = ""
    if urn and "activity:" in urn:
        act_id = urn.split("activity:")[-1]
        post_url = f"https://www.linkedin.com/feed/update/urn:li:activity:{act_id}/"
    else:
        try:
            link_loc = post.locator('a[href*="/feed/update/"]').first
            if link_loc.is_visible(timeout=500):
                raw_href = link_loc.get_attribute("href") or ""
                post_url = raw_href.split("?")[0]
        except Exception:
            pass

    # Author Name & Profile Link
    author_name = "Unknown"
    author_url = ""
    try:
        actor_link = post.locator('a[href*="/in/"], a[href*="/company/"]').first
        if actor_link.count() > 0:
            author_url = (actor_link.get_attribute("href") or "").split("?")[0]
            raw_text = actor_link.inner_text(timeout=500).split("\n")[0].strip()
            if raw_text:
                author_name = raw_text
    except Exception:
        pass

    # Date Posted
    date_posted = ""
    try:
        sub_desc = post.locator('.update-components-actor__sub-description, .feed-shared-actor__sub-description').first
        if sub_desc.count() > 0:
            date_posted = sub_desc.inner_text(timeout=500).split("\n")[0].strip()
    except Exception:
        pass

    return {
        "keyword": keyword,
        "author_name": author_name,
        "author_url": author_url,
        "post_url": post_url or urn or "N/A",
        "date_posted": date_posted,
        "emails": ", ".join(emails),
        "post_text": post_text,
    }


def process_new_posts(page, keyword: str, all_job_records: list[dict], seen_ids: set):
    # UPDATED: Added modern LinkedIn search result selectors
    post_selectors = [
        "li.reusable-search__result-container",
        "ul.search-results__list > li",
        "div.search-results-container div.feed-shared-update-v2",
        "div.feed-shared-update-v2",
        "div.occludable-update",
        "div[data-urn]",
    ]

    post_locator = None
    for selector in post_selectors:
        try:
            loc = page.locator(selector)
            if loc.count() > 0:
                post_locator = loc
                break
        except Exception:
            pass

    if not post_locator:
        return

    count = post_locator.count()
    for i in range(count):
        try:
            post = post_locator.nth(i)
            
            # Extract basic text first to generate deduplication signature
            raw_text = post.inner_text(timeout=1000)
            if not raw_text or len(raw_text.strip()) < 15:
                continue

            unique_id = raw_text[:100]

            if unique_id in seen_ids:
                continue

            seen_ids.add(unique_id)
            record = extract_post_details(post, keyword)

            all_job_records.append(record)
            save_jobs_data(all_job_records)

            if record["emails"]:
                print(f" -> Found Post WITH EMAIL ({record['emails']}) by {record['author_name']}")
            else:
                print(f" -> Saved Post by {record['author_name']}")

        except Exception:
            pass


def click_show_more_results(page):
    actions = [
        lambda: page.locator('button:has-text("Show more results")').first.click(timeout=2000),
        lambda: page.locator('button:has-text("See more results")').first.click(timeout=2000),
    ]
    for action in actions:
        try:
            action()
            page.wait_for_timeout(2000)
            return True
        except Exception:
            pass
    return False


def scroll_and_collect(page, keyword: str, all_job_records: list[dict], seen_ids: set):
    scroll_round = 0
    print(f" -> Scraping job posts for '{keyword}'...")

    # Focus body to enable scroll
    try:
        page.locator("body").click(timeout=2000)
    except Exception:
        pass

    while scroll_round < MAX_SCROLL_ROUNDS:
        scroll_round += 1
        process_new_posts(page, keyword, all_job_records, seen_ids)

        # Smooth scroll
        try:
            page.mouse.wheel(0, 1000)
        except Exception:
            pass

        page.wait_for_timeout(int(SCROLL_PAUSE_SECONDS * 1000))
        click_show_more_results(page)

        print(f"    Round {scroll_round}/{MAX_SCROLL_ROUNDS} | Total Job Posts Saved: {len(all_job_records)}", end="\r")

    print()


def create_context(browser):
    if AUTH_FILE.exists():
        return browser.new_context(storage_state=str(AUTH_FILE))
    return browser.new_context()


def main():
    ensure_dirs()

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False, slow_mo=100)
        context = create_context(browser)
        page = context.new_page()

        page.goto("https://www.linkedin.com/", wait_until="domcontentloaded", timeout=PAGE_TIMEOUT_MS)
        if not is_logged_in(page):
            wait_for_manual_login(page, context)
            context.close()
            context = create_context(browser)
            page = context.new_page()

        all_job_records = []
        seen_ids = set()

        try:
            for keyword in SEARCH_KEYWORDS:
                print(f"\nRunning search for: {keyword}")
                go_to_posts_search(page, keyword)
                scroll_and_collect(page, keyword, all_job_records, seen_ids)
        except KeyboardInterrupt:
            print("\nStopped by user.")
        except PlaywrightTimeoutError as ex:
            print(f"Timeout error: {ex}")
        except Exception as ex:
            print(f"Error: {ex}")
        finally:
            save_jobs_data(all_job_records)
            print("\n" + "=" * 50)
            print("Done!")
            print(f"Total job posts scraped: {len(all_job_records)}")
            print(f"CSV saved to:  {CSV_OUTPUT_FILE}")
            print(f"JSON saved to: {JSON_OUTPUT_FILE}")
            print("=" * 50)

            context.storage_state(path=str(AUTH_FILE))
            context.close()
            browser.close()


if __name__ == "__main__":
    main()