from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO, BytesIO

import requests

url = "https://www.reuters.com/legal/government/tesla-appeal-over-musk-tweet-unions-tests-nlrb-authority-over-social-media-2024-01-25/"

payload = {}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,de;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Cookie': 'datadome=5DoGfdp_v7Y64hF3yeg8zmFRJvUZ_kY9APCBHhhY8Q5HnPWurio8XinFbT~guJr5RlIj0N41S2aQQNBEiMf05rg2Mb3BBC9zMM7Akw1aS8O9285Y~CC1YlyPQoYKfgLi; reuters-geo={"country":"-", "region":"-"}'
}

response = requests.request("GET", url, headers=headers, data=payload)

htmlparser = etree.HTMLParser()

# print(response.text)

news_content = etree.parse(BytesIO(response.content), htmlparser).xpath('/html/body/div[1]/div[3]/div/main/article/div[1]/div/div/div/div[2]')

full_corpus = ""

for tree_item in news_content[0]:
    if (("data-testid" in tree_item.attrib and
            tree_item.attrib["data-testid"].startswith("paragraph")) and
            tree_item.text is not None):
        print(tree_item.text)

# print("text from page:", full_corpus)

#%%
