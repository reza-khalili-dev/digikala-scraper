"""
رابط گرافیکی اسکرپر دیجی‌کالا - نسخه نهایی با راست‌چین (بدون خطا)
"""

# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import os
import sys

# اضافه کردن مسیر فعلی به sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# IMPORT ماژول‌های اصلی
try:
    from config import Config
    from scraper import DigikalaScraper
    from excel_handler import ExcelHandler
    IMPORT_SUCCESS = True
except Exception as e:
    IMPORT_SUCCESS = False
    print(f"خطا در import: {e}")

class ScraperGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # تنظیمات اولیه
        self.title("دیجی‌کالا اسکرپر")
        self.geometry("900x700")
        self.configure(bg='#f0f0f0')
        
        # متغیرها
        self.scraper = None
        self.excel_handler = ExcelHandler() if IMPORT_SUCCESS else None
        self.is_running = False
        self.products_data = []
        
        # مقدار پیش‌فرض
        self.max_products = 50
        
        self.setup_ui()
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # فریم اصلی
        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # عنوان - راست‌چین
        title_label = tk.Label(
            main_frame,
            text="🔍 اسکرپر حرفه‌ای دیجی‌کالا",
            font=("Tahoma", 18, "bold"),
            fg="#0066cc",
            bg='#f0f0f0',
            justify='right',
            anchor='e'
        )
        title_label.pack(pady=(0, 20), anchor='e')
        
        # فریم تنظیمات
        settings_frame = tk.LabelFrame(
            main_frame,
            text="تنظیمات",
            font=("Tahoma", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # تعداد محصول - راست‌چین (جابجایی ستون‌ها)
        tk.Label(
            settings_frame,
            text="تعداد محصول:",
            bg='#f0f0f0',
            font=("Tahoma", 10),
            justify='right',
            anchor='e'
        ).grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        
        self.product_count = tk.IntVar(value=self.max_products)
        self.product_spinbox = tk.Spinbox(
            settings_frame,
            from_=10,
            to=100,
            increment=5,
            textvariable=self.product_count,
            width=10,
            font=("Tahoma", 10),
            justify='right'
        )
        self.product_spinbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        # تنظیم ستون‌ها
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=0)
        
        # فریم دکمه‌ها
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=(0, 20))
        
        # دکمه شروع
        self.start_btn = tk.Button(
            button_frame,
            text="شروع اسکرپ",
            command=self.start_scraping,
            bg="#4CAF50",
            fg="white",
            font=("Tahoma", 10, "bold"),
            width=15,
            height=1,
            cursor="hand2",
            justify='right'
        )
        self.start_btn.pack(side=tk.RIGHT, padx=5)
        
        # دکمه توقف
        self.stop_btn = tk.Button(
            button_frame,
            text="توقف",
            command=self.stop_scraping,
            bg="#f44336",
            fg="white",
            font=("Tahoma", 10, "bold"),
            width=15,
            height=1,
            state=tk.DISABLED,
            cursor="hand2",
            justify='right'
        )
        self.stop_btn.pack(side=tk.RIGHT, padx=5)
        
        # دکمه ذخیره
        self.save_btn = tk.Button(
            button_frame,
            text="ذخیره در اکسل",
            command=self.save_to_excel,
            bg="#2196F3",
            fg="white",
            font=("Tahoma", 10, "bold"),
            width=15,
            height=1,
            state=tk.DISABLED,
            cursor="hand2",
            justify='right'
        )
        self.save_btn.pack(side=tk.RIGHT, padx=5)
        
        # دکمه باز کردن
        self.open_btn = tk.Button(
            button_frame,
            text="باز کردن فایل",
            command=self.open_excel_file,
            bg="#757575",
            fg="white",
            font=("Tahoma", 10, "bold"),
            width=15,
            height=1,
            cursor="hand2",
            justify='right'
        )
        self.open_btn.pack(side=tk.RIGHT, padx=5)
        
        # نوار پیشرفت
        self.progress_bar = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 20))
        
        # لاگ
        log_frame = tk.LabelFrame(
            main_frame,
            text="لاگ عملیات",
            font=("Tahoma", 10, "bold"),
            bg='#f0f0f0'
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # ❌ حذف justify='right' از ScrolledText - مشکل اصلی اینجا بود
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg='white'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ✅ اعمال راست‌چین با tag
        self.log_text.tag_configure('persian', justify='right')
        self.log_text.tag_configure('ltr', justify='left')
        
        # آمار - راست‌چین
        self.stats_label = tk.Label(
            main_frame,
            text="تعداد محصولات: 0",
            fg="#0066cc",
            bg='#f0f0f0',
            font=("Tahoma", 10, "bold"),
            justify='right',
            anchor='e'
        )
        self.stats_label.pack(pady=(10, 0), anchor='e')
        
        # پیام شروع
        self.log("✅ برنامه آماده است")
        self.log("👉 دکمه 'شروع اسکرپ' را کلیک کنید")
    
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        
        # پاک کردن تگ‌های قبلی
        self.log_text.tag_delete('timestamp', 'persian', 'english')
        
        # تنظیم تگ‌ها
        self.log_text.tag_configure('timestamp', justify='left', font=("Consolas", 9))
        self.log_text.tag_configure('persian', justify='right', font=("Tahoma", 9))
        self.log_text.tag_configure('english', justify='left', font=("Consolas", 9))
        
        # درج timestamp (چپ‌چین)
        self.log_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # تشخیص و درج متن
        is_persian = any('\u0600' <= c <= '\u06FF' or c in '،؟✅👉🔍📱💰📄⚠️❌🔧📝💾📂🚀' for c in message)
        
        if is_persian:
            # متن فارسی - راست‌چین
            self.log_text.insert(tk.END, f"{message}\n", 'persian')
        else:
            # متن انگلیسی - چپ‌چین
            self.log_text.insert(tk.END, f"{message}\n", 'english')
        
        self.log_text.see(tk.END)
        self.update()
    
    def start_scraping(self):
        if self.is_running:
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.DISABLED)
        
        self.log_text.delete(1.0, tk.END)
        self.log("=" * 50)
        self.log("شروع اسکرپ...")
        self.log("=" * 50)
        
        max_products = self.product_count.get()
        self.log(f"تعداد محصول درخواستی: {max_products}")
        
        self.progress_bar.start(10)
        
        # اجرا در thread جدا
        thread = threading.Thread(target=self.run_scraping, args=(max_products,), daemon=True)
        thread.start()
    
    def run_scraping(self, max_products):
        try:
            if IMPORT_SUCCESS:
                self.scraper = DigikalaScraper(headless=False, max_products=max_products)
                products = self.scraper.scrape_mobiles()
            else:
                # حالت تست
                self.log("⚠️ حالت تست - ماژول اصلی یافت نشد")
                time.sleep(2)
                products = []
                for i in range(min(5, max_products)):
                    products.append({
                        'title': f'محصول تست {i+1}',
                        'price': f'{i+1}00,000 تومان',
                        'original_price': f'{i+1}50,000 تومان',
                        'discount_percent': '20%',
                        'availability': 'موجود',
                        'link': '#'
                    })
            
            if products:
                self.products_data = products
                self.log(f"✅ اسکرپ کامل شد - {len(products)} محصول")
                self.after(0, lambda: self.stats_label.config(text=f"تعداد محصولات: {len(products)}"))
                self.after(0, lambda: self.save_btn.config(state=tk.NORMAL))
                self.after(0, lambda: messagebox.showinfo("موفقیت", f"{len(products)} محصول استخراج شد"))
            else:
                self.log("❌ محصولی یافت نشد")
                
        except Exception as e:
            self.log(f"❌ خطا: {str(e)}")
            self.after(0, lambda: messagebox.showerror("خطا", str(e)))
        
        finally:
            self.after(0, self.scraping_complete)
    
    def stop_scraping(self):
        self.is_running = False
        self.log("⏹️ توقف اسکرپ")
        if self.scraper and hasattr(self.scraper, 'driver') and self.scraper.driver:
            try:
                self.scraper.driver.quit()
            except:
                pass
    
    def scraping_complete(self):
        self.is_running = False
        self.progress_bar.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("✅ پایان عملیات")
    
    def save_to_excel(self):
        if self.products_data and self.excel_handler:
            self.log("💾 ذخیره در اکسل...")
            try:
                filepath = self.excel_handler.save_to_excel(self.products_data)
                self.log(f"✅ ذخیره شد: {filepath}")
                messagebox.showinfo("موفقیت", f"فایل ذخیره شد:\n{filepath}")
            except Exception as e:
                self.log(f"❌ خطا: {str(e)}")
                messagebox.showerror("خطا", str(e))
        else:
            messagebox.showwarning("هشدار", "داده‌ای وجود ندارد")
    
    def open_excel_file(self):
        output_dir = "output"
        if os.path.exists(output_dir):
            os.startfile(output_dir)
            self.log("📂 پوشه خروجی باز شد")
        else:
            self.log("📂 پوشه خروجی وجود ندارد")
    
    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno("خروج", "عملیات در حال اجراست. خارج می‌شوید؟"):
                self.stop_scraping()
                self.destroy()
        else:
            self.destroy()

if __name__ == "__main__":
    app = ScraperGUI()
    app.mainloop()