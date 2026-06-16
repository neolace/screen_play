"""Example test steps — demonstrates the framework against a public website."""


def run(browser):
    """Test scenario: visit Wikipedia and search for something."""

    # Step 1: Navigate directly to the stable search page
    browser.navigate("https://en.wikipedia.org/wiki/Special:Search")

    # Step 2: Click the search input
    browser.click("#searchText input")

    # Step 3: Type a search term
    browser.fill("#searchText input", "Automated testing")

    # Step 4: Navigate to the stable results URL for the typed query
    browser.navigate(
        "https://en.wikipedia.org/w/index.php?search=Automated+testing&title=Special:Search&ns0=1"
    )

    # Step 5: Wait for results page to load
    browser.wait("#firstHeading")

    # Step 6: Take a final screenshot of the result page
    browser.screenshot("Result page loaded")
