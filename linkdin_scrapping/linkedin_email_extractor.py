import re
import sys
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

SEARCH_KEYWORDS = [
    # '"Machine Learning Remote Job"',
    # '"AI ML Remote Job"',
    # '"Generative AI Remote Job"',
    # '"Agentic AI Remote Job"',
    '"Data Scientist Remote"',
    # '"AI Developer Remote Job"',
    # '"Python Developer Remote"'
]

BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "output"
AUTH_DIR = BASE_DIR / "playwright" / ".auth"
AUTH_FILE = AUTH_DIR / "linkedin_user.json"
OUTPUT_FILE = OUTPUT_DIR / "emails.txt"

SCROLL_PAUSE_SECONDS = 3
MAX_SCROLL_ROUNDS = 10  # Set limit so multi-keyword search actually moves to the next keyword
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
    """Converts obfuscated emails like name[at]domain[dot]com to standard email text."""
    if not text:
        return ""
    text = re.sub(r"\s*[\(\[\{]\s*at\s*[\)\]\}]\s*", "@", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*[\(\[\{]\s*dot\s*[\)\]\}]\s*", ".", text, flags=re.IGNORECASE)
    return text


def save_emails_live(email_set: set):
    emails = sorted(email_set, key=lambda x: x.lower())
    # Using newlines instead of commas makes output cleaner
    OUTPUT_FILE.write_text("\n".join(emails), encoding="utf-8")
    return emails


def add_email(email_set: set, email: str):
    email = normalize_email(email)
    if email and email not in email_set:
        email_set.add(email)
        save_emails_live(email_set)
        print(f" -> Found: {email}")


def extract_emails_from_text(text: str, email_set: set):
    clean_text = deobfuscate_text(text)
    for match in EMAIL_REGEX.findall(clean_text or ""):
        add_email(email_set, match)


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
    # Added sortBy=%22date_posted%22 URL param directly to skip UI filter clicking
    url = f"https://www.linkedin.com/search/results/content/?keywords={quote(keyword)}&sortBy=%22date_posted%22"
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
            if more_btn.is_visible(timeout=500):
                more_btn.click(timeout=1000)
                post.page.wait_for_timeout(500)
                return True
        except Exception:
            pass
    return False


def process_new_posts(page, email_set: set, seen_post_ids: set):
    """Processes only unread posts to prevent slow re-parsing of old DOM elements."""
    post_selectors = [
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
        # Fallback to general body text
        try:
            extract_emails_from_text(page.locator("body").inner_text(timeout=3000), email_set)
        except Exception:
            pass
        return

    count = post_locator.count()
    for i in range(count):
        try:
            post = post_locator.nth(i)
            # Create unique identifier using text snippet or URN attribute
            post_urn = post.get_attribute("data-urn") or post.inner_text(timeout=1000)[:60]
            
            if post_urn in seen_post_ids:
                continue  # Skip already processed posts

            seen_post_ids.add(post_urn)
            expand_post_if_needed(post)

            # Extract from raw text
            post_text = post.inner_text(timeout=2000)
            extract_emails_from_text(post_text, email_set)

            # Extract from mailto links
            hrefs = post.locator('a[href^="mailto:"]').evaluate_all(
                "(anchors) => anchors.map(a => a.getAttribute('href') || '')"
            )
            for href in hrefs:
                email = re.sub(r"^mailto:", "", href, flags=re.IGNORECASE).strip()
                if email:
                    add_email(email_set, email)

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


def scroll_and_collect(page, email_set: set):
    seen_post_ids = set()
    scroll_round = 0

    print(" -> Scraping posts...")

    while scroll_round < MAX_SCROLL_ROUNDS:
        scroll_round += 1
        process_new_posts(page, email_set, seen_post_ids)

        # Scroll mouse wheel down
        try:
            page.mouse.wheel(0, 1200)
        except Exception:
            pass

        page.wait_for_timeout(int(SCROLL_PAUSE_SECONDS * 1000))
        click_show_more_results(page)

        print(f"    Round {scroll_round}/{MAX_SCROLL_ROUNDS} | Emails found so far: {len(email_set)}", end="\r")

    print()  # newline after keyword finish


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

        # Ensure active logged-in state regardless of auth file presence
        page.goto("https://www.linkedin.com/", wait_until="domcontentloaded", timeout=PAGE_TIMEOUT_MS)
        if not is_logged_in(page):
            wait_for_manual_login(page, context)
            context.close()
            context = create_context(browser)
            page = context.new_page()

        emails = set()

        try:
            for keyword in SEARCH_KEYWORDS:
                print(f"\nRunning search for: {keyword}")
                go_to_posts_search(page, keyword)
                scroll_and_collect(page, emails)
        except KeyboardInterrupt:
            print("\nStopped by user.")
        except PlaywrightTimeoutError as ex:
            print(f"Timeout error: {ex}")
        except Exception as ex:
            print(f"Error: {ex}")
        finally:
            saved_emails = save_emails_live(emails)
            print("\nDone.")
            print(f"Total unique emails found: {len(saved_emails)}")
            print(f"Saved to: {OUTPUT_FILE}")

            context.storage_state(path=str(AUTH_FILE))
            context.close()
            browser.close()


if __name__ == "__main__":
    main()