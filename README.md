# Digikala Mobile Category Scraper

A powerful and fast Python application to scrape product data from Digikala's mobile phone category using official API. This tool features a modern GUI and exports data to Excel format.

![Digikala Scraper](screenshot.png)

## 🚀 Features

- **Fast API-based scraping** - No browser automation needed, 10x faster than Selenium
- **Modern Persian GUI** - Fully RTL interface with right-to-left support
- **Excel Export** - Automatically saves data to formatted Excel files
- **Real-time Logging** - Live operation log with Persian text support
- **No Rate Limiting** - Optimized requests to avoid blocking
- **Lightweight** - Minimal dependencies, runs on any Python 3.7+ system

## 📋 Requirements

- Python 3.7 or higher
- pip package manager

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/digikala-scraper.git
cd digikala-scraper

pip install -r requirements.txt

Usage
Run the application:

python run.py

How it works:
Launch the application

Enter the number of products (10-100)

Click "Start Scraping" (شروع اسکرپ)

Wait for the process to complete

Save results to Excel

Open the output folder to view files

digikala-scraper/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── scraper.py         # API scraper class
│   ├── gui.py            # RTL GUI interface
│   └── excel_handler.py   # Excel export handler
├── output/               # Generated Excel files
├── tests/               # Test files
├── run.py              # Application entry point
├── requirements.txt    # Dependencies
├── README.md          # This file
├── CONTRIBUTING.md   # Contribution guidelines
└── LICENSE           # MIT License


Configuration
Edit src/config.py to customize:

class Config:
    MAX_PRODUCTS = 50           # Default product count
    OUTPUT_DIR = "output"       # Export directory
    EXCEL_FILENAME = "digikala_mobiles.xlsx"
    SCRAPER_MODE = "api"        # API mode (no Selenium)

📊 Output Format
The scraper exports the following data to Excel:

Title - Product name (Persian)

Price - Current selling price

Original Price - Original price before discount

Discount - Discount percentage

Availability - In stock status

Link - Product URL

🌐 API Endpoint
This tool uses Digikala's official API:  

https://api.digikala.com/v1/categories/mobile-phone/search/

🤝 Contributing
Contributions are welcome! Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

⚠️ Disclaimer
This tool is for educational purposes only. Web scraping may be against Digikala's terms of service. Use responsibly and at your own risk. The developers are not responsible for any misuse of this software.

👨‍💻 Author
Your Name

GitHub: @yourusername

🙏 Acknowledgments
Digikala for providing the API

Python community for excellent libraries

All contributors and users

📧 Contact
For support or questions, please open an issue in the GitHub repository.

Made with ❤️ for the Persian developer community