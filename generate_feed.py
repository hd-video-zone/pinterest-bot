import datetime
import html

# Initial products list
products = [
    {
        "title": "Aesthetic Oversized Cable Knit Sweater",
        "link": "https://www.amazon.com/dp/B08XYZ1234?tag=iamkieravox-20",
        "image": "https://m.media-amazon.com/images/I/71wK7YQZqNL._AC_UY1000_.jpg",
        "desc": "Cozy aesthetic fall outfit inspiration. Trending casual oversized knit sweater on Amazon. #ad #amazonfinds #fashion"
    },
    {
        "title": "High Waisted Ribbed Seamless Flare Leggings",
        "link": "https://www.amazon.com/dp/B07ABC5678?tag=iamkieravox-20",
        "image": "https://m.media-amazon.com/images/I/61r5t12abcL._AC_UY1000_.jpg",
        "desc": "Super soft workout and athleisure everyday leggings. Trendy gym aesthetic look. #ad #amazonfashion #activewear"
    },
    {
        "title": "Neutral Minimalist Two-Piece Lounge Set",
        "link": "https://www.amazon.com/dp/B09DEF9012?tag=iamkieravox-20",
        "image": "https://m.media-amazon.com/images/I/71aBcDeFgHL._AC_UY1000_.jpg",
        "desc": "Aesthetic comfy loungewear set for stay-at-home days. Cozy style finds. #ad #amazonfinds #loungewear"
    }
]

rss_items = []
now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

for p in products:
    item = f"""
    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{html.escape(p['link'])}</link>
      <description>{html.escape(p['desc'])}</description>
      <enclosure url="{html.escape(p['image'])}" type="image/jpeg" length="0"/>
      <pubDate>{now}</pubDate>
      <guid>{html.escape(p['link'])}</guid>
    </item>
    """
    rss_items.append(item)

rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Kiera Vox Amazon Finds</title>
  <link>https://hd-video-zone.github.io/pinterest-bot/feed.xml</link>
  <description>Amazon Fashion and Lifestyle Finds</description>
  <lastBuildDate>{now}</lastBuildDate>
  {''.join(rss_items)}
</channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_content.strip())

print("feed.xml successfully generated!")
