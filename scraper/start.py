import uuid
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig,BrowserConfig,CacheMode
from llmMarkdownToJson import markdown_to_json
import os
import json
from utils import write_file
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import asyncio
from dotenv import load_dotenv
import requests
load_dotenv()




async def scrape(url: str, name: str, css_selector: str):
    # WAT IS ER TE DOEN IN BREDA
    browser_config = BrowserConfig(
                headless=True,  
            )
    crawler = AsyncWebCrawler(config=browser_config)
    md_generator = DefaultMarkdownGenerator(
                options={
                    "ignore_images": True,    
                    "escape_html": False,  
                    "body_width": 80                          
                }            
            )
    crawler_cfg = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown_generator=md_generator, 
    wait_for=f"css:{css_selector}",
    css_selector=css_selector,
    delay_before_return_html=2.5,
    )
    result = None
    await crawler.start()
    crawlerResult = await crawler.arun(url,config=crawler_cfg)
    if crawlerResult.success:        
        # write_file(crawlerResult.markdown_v2.raw_markdown, f"scraped/{name}.md")      
        result = await markdown_to_json(crawlerResult.markdown_v2.raw_markdown)          
        for row in result:  
            row["id"] = str(uuid.uuid4())
            row["name"] = name
        # write_file(json.dumps(result, indent=2), f"scraped/{name}.json")      
    else:
        print(f"Failed: {url} - Error: {result.error_message}")
        
        

    return result


if not os.path.exists("scraped"):
    os.makedirs("scraped")


scrapeUrls = [{"url":"https://www.mezz.nl/programma/",
              "name":"mezz",
              "css_selector":".program__item"},
              {"url":"https://poppodiumphoenix.nl/events/lijst/pagina/1/",
              "name":"phoenix",
              "css_selector":".tribe-events-calendar-list"},
              {"url":"https://poppodiumphoenix.nl/events/lijst/pagina/2/",
              "name":"phoenix",
              "css_selector":".tribe-events-calendar-list"},
              {"url":"https://cafelievense.nl/event-agenda/",
              "name":"cafelievense",
              "css_selector":".et_pb_blog_grid"},
              {"url":"https://pier15.nl/agenda/",
              "name":"pier15",
              "css_selector":".agenda-loop"},
              {"url":"https://www.013.nl/programma",
              "name":"013",
              "css_selector":"#main"},
              {"url":"https://stekbreda.nl/agenda", 
              "name":"stek breda",
              "css_selector":".pixelbones"},
            #   {"url":"https://www.explorebreda.com/nl/evenementen?categories=culinair&categories=festival&categories=overige-evenementen&categories=pubquiz&categories=film&categories=gaming-technologie&categories=exposities-kunst&categories=literatuur&categories=muziek-concerten&categories=theater-toneel-dans&page=1",
            #   "name":"vvv",
            #   "css_selector":"#__next"},
            #   {"url":"https://www.explorebreda.com/nl/evenementen?categories=culinair&categories=festival&categories=overige-evenementen&categories=pubquiz&categories=film&categories=gaming-technologie&categories=exposities-kunst&categories=literatuur&categories=muziek-concerten&categories=theater-toneel-dans&page=2", 
            #   "name":"vvv",
            #   "css_selector":"#__next"}, 
            # {"url":"https://www.explorebreda.com/nl/evenementen?categories=culinair&categories=festival&categories=overige-evenementen&categories=pubquiz&categories=film&categories=gaming-technologie&categories=exposities-kunst&categories=literatuur&categories=muziek-concerten&categories=theater-toneel-dans&page=3", 
            #   "name":"vvv",
            #   "css_selector":"#__next"},     
            #   {"url":"https://www.explorebreda.com/nl/evenementen?categories=culinair&categories=festival&categories=overige-evenementen&categories=pubquiz&categories=film&categories=gaming-technologie&categories=exposities-kunst&categories=literatuur&categories=muziek-concerten&categories=theater-toneel-dans&page=4", 
            #   "name":"vvv",
            #   "css_selector":"#__next"},              
              ]
async def start():
    results=[]
    for url in scrapeUrls:
        result = await scrape(url["url"], url["name"], url["css_selector"])
        results.extend(result)
        

    url = 'https://api.jsonbin.io/v3/b/67a62d28ad19ca34f8fb87a3'
    headers = {
    'Content-Type': 'application/json',
    'X-Access-Key': os.environ.get("JSON_BIN_KEY")
    }
    
    req = requests.put(url, json=results, headers=headers)
    print(f"response jsonbin {req.text}")
    
    return results


