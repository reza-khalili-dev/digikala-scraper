"""
کلاس اصلی اسکرپر دیجی‌کالا - نسخه نهایی با دسته‌بندی اصلی موبایل
"""

import time
import logging
import sys
import os
from typing import List, Dict, Optional
import re
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from config import Config


class DigikalaScraper:
    """اسکرپر محصولات دسته‌بندی موبایل دیجی‌کالا"""
    
    def __init__(self, headless=False, max_products=50):
        self.config = Config
        self.headless = headless
        self.max_products = max_products
        self.products = []
        self.session = None
        self.setup_logging()
        
        # ✅ آدرس‌های صحیح API
        self.API_BASE_URL = "https://api.digikala.com/v1"
        
        # ✅ دسته‌بندی اصلی موبایل - شامل گوشی و لوازم جانبی
        self.MOBILE_CATEGORY = "mobile-phone"
        self.CATEGORY_URL = f"{self.API_BASE_URL}/categories/{self.MOBILE_CATEGORY}/search/"
        
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
            'Referer': 'https://www.digikala.com/',
        }
        
    def setup_logging(self):
        """تنظیم سیستم لاگ‌گیری"""
        self.logger = logging.getLogger(__name__)
        if self.logger.handlers:
            self.logger.handlers.clear()
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.propagate = False
    
    def setup_session(self):
        """راه‌اندازی جلسه HTTP"""
        try:
            self.session = requests.Session()
            self.session.headers.update(self.HEADERS)
            
            # تست اتصال
            test_url = f"{self.CATEGORY_URL}?page=1"
            response = self.session.get(test_url, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("✅ اتصال به API دیجی‌کالا برقرار شد")
                return True
            else:
                self.logger.error(f"❌ خطا در اتصال: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ خطا در راه‌اندازی session: {e}")
            return False
    
    def extract_product_id(self, product_data: Dict) -> Optional[str]:
        """استخراج شناسه محصول"""
        if 'id' in product_data:
            return str(product_data['id'])
        elif 'product_id' in product_data:
            return str(product_data['product_id'])
        elif 'url' in product_data:
            url = product_data['url']
            match = re.search(r'dkp[_-]?(\d+)', url)
            if match:
                return match.group(1)
        return None
    
    def format_price(self, price) -> str:
        """فرمت‌بندی قیمت"""
        if not price:
            return "ناموجود"
        try:
            price_int = int(float(price))
            if price_int > 0:
                return f"{price_int:,} تومان"
        except:
            pass
        return "ناموجود"
    
    def scrape_mobiles(self) -> List[Dict]:
        """دریافت لیست محصولات دسته‌بندی موبایل از API"""
        
        self.logger.info("=" * 60)
        self.logger.info("🚀 شروع دریافت محصولات دسته‌بندی موبایل از API دیجی‌کالا")
        self.logger.info("=" * 60)
        
        if not self.setup_session():
            return []
        
        products_data = []
        page = 1
        max_pages = 200  # افزایش صفحات برای رسیدن به تعداد مورد نظر
        
        try:
            while len(products_data) < self.max_products and page <= max_pages:
                
                # ✅ پارامترهای درست برای API
                params = {
                    'page': page,
                    'sort': '7',  # محبوب‌ترین
                    'size': 48    # تعداد محصول در هر صفحه
                }
                
                self.logger.info(f"📄 صفحه {page}...")
                
                response = self.session.get(
                    self.CATEGORY_URL,
                    params=params,
                    timeout=15
                )
                
                if response.status_code != 200:
                    self.logger.error(f"❌ خطا در دریافت صفحه {page}: {response.status_code}")
                    break
                
                data = response.json()
                
                # استخراج محصولات
                products = []
                if 'data' in data and 'products' in data['data']:
                    products = data['data']['products']
                
                if not products:
                    self.logger.info("🏁 به انتهای لیست رسیدیم")
                    break
                
                self.logger.info(f"📱 {len(products)} محصول در صفحه {page}")
                
                # ❌ بدون هیچ فیلتری - همه محصولات دسته‌بندی موبایل رو اضافه کن
                for product in products:
                    if len(products_data) >= self.max_products:
                        break
                    
                    product_info = self.parse_product(product)
                    if product_info:
                        products_data.append(product_info)
                        
                        self.logger.info(f"   ✓ {len(products_data)}. {product_info['title'][:40]}...")
                        self.logger.info(f"     💰 {product_info['price']}")
                
                page += 1
                time.sleep(0.5)
                
            self.products = products_data
            
            self.logger.info("=" * 60)
            self.logger.info(f"✅ دریافت کامل شد! {len(self.products)} محصول از دسته‌بندی موبایل")
            if len(products_data) < self.max_products:
                self.logger.warning(f"⚠️ فقط {len(products_data)} محصول پیدا شد (درخواست: {self.max_products})")
            self.logger.info("=" * 60)
            
            return self.products
            
        except Exception as e:
            self.logger.error(f"❌ خطای کلی: {e}")
            return []
    
    def parse_product(self, product: Dict) -> Optional[Dict]:
        """تبدیل داده‌های محصول به فرمت استاندارد"""
        
        try:
            # عنوان محصول
            title = None
            if 'title_fa' in product:
                title = product['title_fa']
            elif 'title' in product:
                title = product['title']
            elif 'name' in product:
                title = product['name']
            
            if not title:
                return None
            
            # قیمت و موجودی
            price = "ناموجود"
            original_price = "ناموجود"
            discount_percent = "0%"
            availability = "ناموجود"
            
            # استخراج از default_variant
            if 'default_variant' in product:
                variant = product['default_variant']
                if variant and 'price' in variant:
                    selling = variant['price'].get('selling_price', 0)
                    rrp = variant['price'].get('rrp_price', 0)
                    
                    if selling and selling > 0:
                        price = self.format_price(selling)
                        availability = "موجود"
                        
                        if rrp and rrp > selling:
                            original_price = self.format_price(rrp)
                            discount = ((rrp - selling) / rrp) * 100
                            discount_percent = f"{int(discount)}%"
            
            # لینک محصول
            product_id = self.extract_product_id(product)
            if product_id:
                link = f"https://www.digikala.com/product/dkp-{product_id}/"
            else:
                link = product.get('url', '')
                if link and not link.startswith('http'):
                    link = f"https://www.digikala.com{link}"
            
            return {
                'title': title.strip(),
                'price': price,
                'original_price': original_price,
                'discount_percent': discount_percent,
                'availability': availability,
                'link': link,
                'id': product_id or ''
            }
            
        except Exception as e:
            return None
    
    # سازگاری با کد قدیمی
    def setup_driver(self):
        self.logger.info("ℹ️ در حالت API، نیازی به WebDriver نیست")
        return True