import requests
import json

# تست آدرس‌های مختلف API
urls = [
    "https://api.digikala.com/v1/search/?category=mobile-phone",
    "https://api.digikala.com/v1/categories/mobile-phone/search/",
    "https://www.digikala.com/ajax/search/?category=mobile-phone",
    "https://www.digikala.com/front-end/search/?category=mobile-phone",
    "https://www.digikala.com/search/category-mobile-phone/?ajax=True",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

for url in urls:
    print(f"\n📡 تست: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   وضعیت: {response.status_code}")
        
        if response.status_code == 200:
            # بررسی اینکه آیا پاسخ JSON است
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                data = response.json()
                print(f"   ✅ JSON معتبر")
                if 'data' in data or 'products' in str(data):
                    print(f"   🎯 محصولات پیدا شد!")
                    break
            else:
                print(f"   ❌ JSON نیست: {content_type[:30]}")
    except Exception as e:
        print(f"   ❌ خطا: {e}")