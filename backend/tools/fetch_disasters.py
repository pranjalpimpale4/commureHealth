import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import dateutil.parser

class DisasterFetcher:
    def __init__(self):
        self.sources = ["ReliefWeb", "GDACS", "EMSC"]
        self.now = datetime.now(timezone.utc)
        self.one_year_ago = self.now - timedelta(days=365)

    def is_recent(self, date_str):
        try:
            dt = dateutil.parser.parse(date_str)
            return dt >= self.one_year_ago
        except:
            return False

    def format_date(self, d):
        try:
            return dateutil.parser.parse(d).astimezone(timezone.utc).isoformat()
        except:
            return None

    def fetch_reliefweb(self):
        url = "https://api.reliefweb.int/v1/disasters?appname=crew-ai-agent&profile=full&limit=100"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            return [
                {
                    "source": "ReliefWeb",
                    "type": ", ".join(t["name"] for t in f.get("type", [])) or None,
                    "country": ", ".join(c["name"] for c in f.get("country", [])) or None,
                    "location": f.get("name", None),
                    "latitude": None,
                    "longitude": None,
                    "date": self.format_date(f.get("date", {}).get("created")),
                    "headline": f.get("name", "No headline"),
                    "status": f.get("status", None)
                }
                for f in (item["fields"] for item in data.get("data", []))
                if f.get("date", {}).get("created") and self.is_recent(f.get("date", {}).get("created"))
            ]
        except Exception as e:
            print(f"[ReliefWeb Error] {e}")
            return []

    def fetch_gdacs(self):
        try:
            feed = requests.get("https://www.gdacs.org/xml/rss.xml", timeout=10)
            soup = BeautifulSoup(feed.content, "xml")
            return [
                {
                    "source": "GDACS",
                    "type": "Disaster",
                    "country": None,
                    "location": None,
                    "latitude": float(item.find("geo:lat").text) if item.find("geo:lat") else None,
                    "longitude": float(item.find("geo:long").text) if item.find("geo:long") else None,
                    "date": self.format_date(item.pubDate.text.strip()),
                    "headline": item.title.text.strip(),
                    "status": "reported"
                }
                for item in soup.find_all("item")
                if self.is_recent(item.pubDate.text.strip())
            ]
        except Exception as e:
            print(f"[GDACS Error] {e}")
            return []

    def fetch_emsc(self):
        try:
            feed = requests.get("https://www.emsc-csem.org/service/rss/rss.php?typ=emsc", timeout=10)
            soup = BeautifulSoup(feed.content, "xml")
            return [
                {
                    "source": "EMSC",
                    "type": "Earthquake",
                    "country": None,
                    "location": None,
                    "latitude": float(item.find("geo:lat").text) if item.find("geo:lat") else None,
                    "longitude": float(item.find("geo:long").text) if item.find("geo:long") else None,
                    "date": self.format_date(item.pubDate.text.strip()),
                    "headline": item.title.text.strip(),
                    "status": "reported"
                }
                for item in soup.find_all("item")
                if self.is_recent(item.pubDate.text.strip())
            ]
        except Exception as e:
            print(f"[EMSC Error] {e}")
            return []

    def get_disasters(self):
        print("🌐 Fetching disasters from ReliefWeb, GDACS, and EMSC...")
        return self.fetch_reliefweb() + self.fetch_gdacs() + self.fetch_emsc()
        print(f"✅ Total disasters fetched: {len(all_disasters)}")
        print(f"📰 Sample headlines: {[d['headline'] for d in all_disasters if d.get('headline')][:5]}")
        return all_disasters
