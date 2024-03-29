# Scrapy settings for twitterlinkscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'twitterlinkscraper'

SPIDER_MODULES = ['twitterlinkscraper.spiders']
NEWSPIDER_MODULE = 'twitterlinkscraper.spiders'

# SPIDER_MODULES = ['twitterlinkscraper.twitterlinkscraper.spiders']
# NEWSPIDER_MODULE = 'twitterlinkscraper.twitterlinkscraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'twitterlinkscraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# FEED_URI = "results.json"
# FEEDS = {
#     'data.jsonl': {'format': 'jsonlines', 'overwrite': True}
# }
PROXY_POOL_ENABLED = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 50000
CONCURRENT_REQUESTS_PER_DOMAIN=2
SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'
REACTOR_THREADPOOL_MAXSIZE = 30
LOG_LEVEL = 'ERROR'
# COOKIES_ENABLED = False
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 30
ROTATING_PROXY_LIST_PATH = '/http_proxies.txt'
# PROXY
# PROXY = 'http://127.0.0.1:8888/?noconnect'

# SCRAPOXY
# API_SCRAPOXY = 'http://127.0.0.1:8889/api'
# API_SCRAPOXY_PASSWORD = 'ShadowSlash247'

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'twitterlinkscraper.middlewares.TwitterlinkscraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'twitterlinkscraper.middlewares.RotateUserAgentMiddleware': 535,
   'twitterlinkscraper.middlewares.ShowHeadersMiddleware': 540,
   'twitterlinkscraper.middlewares.TwitterlinkscraperDownloaderMiddleware': 543,
   # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
   # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
   # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
   # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
}
# DOWNLOADER_MIDDLEWARES = {
#    'twitterlinkscraper.twitterlinkscraper.middlewares.RotateUserAgentMiddleware': 535,
#    'twitterlinkscraper.twitterlinkscraper.middlewares.ShowHeadersMiddleware': 540,
#    'twitterlinkscraper.twitterlinkscraper.middlewares.TwitterlinkscraperDownloaderMiddleware': 543,
#    # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#    # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'twitterlinkscraper.pipelines.TwitterlinkscraperPipeline': 300,
}
# ITEM_PIPELINES = {
#    'twitterlinkscraper.twitterlinkscraper.pipelines.TwitterlinkscraperPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

USERAGENTS = [
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]