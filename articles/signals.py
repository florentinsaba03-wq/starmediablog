import requests

def ping_google():
    sitemap_url = "https://starmediablog.onrender.com/sitemap.xml"
    ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"

    try:
        requests.get(ping_url)
    except:
        pass