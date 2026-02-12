# -*- coding: utf-8 -*-
import sys
import os
import logging

# تنظیم encoding برای ویندوز
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# مسیر پروژه
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_DIR, "src")

# اضافه کردن src به مسیر پایتون
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# تنظیم لاگینگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

print("=" * 60)
print("🔍 اسکرپر حرفه‌ای دیجی‌کالا")
print("=" * 60)
print(f"📁 مسیر پروژه: {PROJECT_DIR}")
print(f"📁 مسیر src: {SRC_DIR}")
print("=" * 60)

try:
    # بررسی وجود فایل‌ها
    required_files = ['gui.py', 'scraper.py', 'config.py', 'excel_handler.py']
    for file in required_files:
        file_path = os.path.join(SRC_DIR, file)
        if os.path.exists(file_path):
            print(f"✅ {file} پیدا شد")
        else:
            print(f"❌ {file} پیدا نشد!")
    
    print("\n🚀 در حال اجرای برنامه...")
    print("=" * 60)
    
    # ایمپورت و اجرا
    from gui import ScraperGUI
    
    app = ScraperGUI()
    app.mainloop()
    
except ImportError as e:
    print(f"\n❌ خطا در ایمپورت: {e}")
    print("\n💡 راه‌حل:")
    print("1. مطمئن شوید در پوشه اصلی پروژه هستید")
    print("2. دستور زیر را اجرا کنید:")
    print(f"   cd {PROJECT_DIR}")
    print("   python run.py")
    
except Exception as e:
    print(f"\n❌ خطای ناشناخته: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n" + "=" * 60)
    input("برای خروج Enter را بزنید...")