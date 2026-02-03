import time


def scroll_until_done(page, pause=1.5, max_attempts=5):
    """
    Scrolls until no new content is loaded.

    pause: seconds to wait after each scroll
    max_attempts: how many times height can stay the same before stopping
    """

    last_height = page.evaluate("document.body.scrollHeight")
    same_height_count = 0

    while True:
        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(pause)

        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == last_height:
            same_height_count += 1
            if same_height_count >= max_attempts:
                print("✅ Reached end of infinite scroll")
                break
        else:
            same_height_count = 0
            last_height = new_height
