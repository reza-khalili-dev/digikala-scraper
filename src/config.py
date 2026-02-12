"""
تنظیمات پیکربندی اسکرپر - نسخه نهایی
"""

class Config:
    # تنظیمات دیجی‌کالا
    BASE_URL = "https://www.digikala.com"
    MOBILE_CATEGORY_URL = "https://api.digikala.com/v1/categories/mobile-phone/search/"
    
    # تنظیمات اسکرپر
    SCRAPER_MODE = "api"
    MAX_PRODUCTS = 50
    HEADLESS_MODE = False
    
    # تنظیمات ذخیره‌سازی
    OUTPUT_DIR = "output"
    EXCEL_FILENAME = "digikala_mobiles.xlsx"
    
    # تنظیمات رابط کاربری
    APP_TITLE = "Digikala Mobile Category Scraper"
    THEME = "darkly"