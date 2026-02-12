import sys
import os

from src.gui import ScraperGUI

# مسیر کامل src رو اضافه کن
SRC_PATH = r"G:\arsalan\programming\scraper projects\digikala-scraper\src"
sys.path.insert(0, SRC_PATH)

print("🚀 در حال راه‌اندازی اسکرپر دیجی‌کالا...")
print(f"📁 مسیر: {SRC_PATH}")

# مستقییم import کن
exec(open(os.path.join(SRC_PATH, 'gui.py')).read())

# برنامه رو اجرا کن
app = ScraperGUI()
app.mainloop()