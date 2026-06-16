"""Example test steps — demonstrates the framework against a public website."""


def run(browser):
    """Test scenario: visit Wikipedia and search for something."""

    # Step 1: Navigate directly to the stable search page
    browser.navigate("https://en.wikipedia.org/wiki/Special:Search")

    # Step 2: Click the search input
    browser.click("#searchText")

    # Step 3: Type a search term
    browser.fill("#searchText", "Automated testing")

    # Step 4: Click the search button
    browser.click("#searchform button[type='submit']")

    # Step 5: Wait for results page to load
    browser.wait("#firstHeading")

    # Step 6: Take a final screenshot of the result page
    browser.screenshot("Result page loaded")
