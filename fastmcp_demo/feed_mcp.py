from fastmcp import FastMCP
import feedparser

mcp = FastMCP(name="FreeCodeCamp Feed Searcher API")


@mcp.tool()
def fcc_news_search(query: str, max_results: int = 3):
    """
    Search for news articles in the FreeCodeCamp RSS feed that match the query.
    """
    feed_url = "https://www.freecodecamp.org/news/rss/"
    feed = feedparser.parse(feed_url)

    matching_articles = []
    for entry in feed.entries:
        if (
            query.lower() in entry.title.lower()
            or query.lower() in entry.summary.lower()
        ):
            matching_articles.append({"title": entry.title, "link": entry.link})

    if not matching_articles:
        return "No matching articles found."

    return matching_articles or [{"messages": "No matching articles found."}]


@mcp.tool()
def fcc_youtube_search(query: str, max_results: int = 3):
    """
    Get the latest videos from the FreeCodeCamp YouTube channel.
    """
    feed_url = (
        "https://www.youtube.com/feeds/videos.xml?channel_id=UC8butISFwT-Wl7EV0hUK0BQ"
    )
    feed = feedparser.parse(feed_url)

    latest_videos = []
    query_lower = query.lower()

    for entry in feed.entries:
        title = entry.get("title", "")
        if query_lower in title.lower():
            latest_videos.append({"title": entry.title, "link": entry.link})
        if len(latest_videos) >= max_results:
            break  # unlikely to occur

    return latest_videos or [{"messages": "No matching articles found."}]


@mcp.tool()
def secret_message():
    """Return a secret message"""
    return "Keep exploring and take risks!"


if __name__ == "__main__":
    mcp.run()
