"""
مدیریت ذخیره‌سازی داده‌ها در فایل اکسل - نسخه اصلاح شده
"""

import pandas as pd
import os
from datetime import datetime
import logging
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from config import Config

class ExcelHandler:
    """کلاس مدیریت ذخیره‌سازی در اکسل"""
    
    def __init__(self):
        self.config = Config
        self.setup_output_dir()
        self.setup_logging()
    
    def setup_logging(self):
        """تنظیم سیستم لاگ‌گیری"""
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.propagate = False
    
    def setup_output_dir(self):
        """ایجاد پوشه خروجی اگر وجود نداشته باشد"""
        if not os.path.exists(self.config.OUTPUT_DIR):
            os.makedirs(self.config.OUTPUT_DIR)
            print(f"📁 پوشه {self.config.OUTPUT_DIR} ایجاد شد")
    
    def save_to_excel(self, products_data, filename=None):
        """
        ذخیره داده‌ها در فایل اکسل
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"digikala_mobiles_{timestamp}.xlsx"
        
        filepath = os.path.join(self.config.OUTPUT_DIR, filename)
        
        try:
            if not products_data:
                self.logger.warning("⚠️ هیچ داده‌ای برای ذخیره وجود ندارد")
                return None
            
            # تبدیل به DataFrame
            df = pd.DataFrame(products_data)
            
            # حذف ردیف‌های تکراری بر اساس عنوان
            df = df.drop_duplicates(subset=['title'], keep='first')
            
            # مرتب‌سازی بر اساس عنوان
            df = df.sort_values('title')
            
            # ذخیره در اکسل
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='محصولات', index=False)
                
                # تنظیم عرض ستون‌ها
                worksheet = writer.sheets['محصولات']
                
                column_widths = {
                    'A': 50,  # عنوان
                    'B': 20,  # قیمت
                    'C': 20,  # قیمت اصلی
                    'D': 15,  # درصد تخفیف
                    'E': 15,  # موجودی
                    'F': 50   # لینک
                }
                
                for col, width in column_widths.items():
                    worksheet.column_dimensions[col].width = width
            
            self.logger.info(f"✅ داده‌ها با موفقیت در {filepath} ذخیره شدند")
            self.logger.info(f"📊 تعداد رکوردها: {len(df)}")
            
            # ذخیره نسخه با نام ثابت
            latest_filepath = os.path.join(self.config.OUTPUT_DIR, self.config.EXCEL_FILENAME)
            df.to_excel(latest_filepath, index=False)
            self.logger.info(f"💾 نسخه جدید در {latest_filepath} ذخیره شد")
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"❌ خطا در ذخیره‌سازی فایل اکسل: {e}")
            return None