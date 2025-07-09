# Booking.com Deep Scraper

A comprehensive web scraper designed to extract detailed information from Booking.com with high depth crawling capabilities.

## ⚠️ Legal Notice

This scraper is for educational and research purposes only. Please ensure you:
- Respect Booking.com's robots.txt file
- Comply with their Terms of Service
- Use appropriate delays between requests
- Do not overwhelm their servers
- Consider the legal implications in your jurisdiction

## 🚀 Features

- **Deep Crawling**: Crawls up to 20 levels deep with configurable limits
- **Comprehensive Data Extraction**:
  - Hotel information (names, prices, ratings, locations)
  - Destination data
  - Search filters and pricing
  - User reviews and ratings
  - Availability information
  - API endpoints and authentication flows
  - Hidden elements and JavaScript APIs
  - Forms and user data patterns
- **Resource Management**:
  - Downloads images, documents, and other resources
  - Takes screenshots of each page
  - Saves cookies and session data
- **Anti-Detection Features**:
  - Randomized delays
  - Realistic user agent
  - Browser fingerprint masking
  - Request throttling

## 📋 Requirements

- Python 3.8+
- Windows/Linux/macOS
- At least 2GB RAM
- 5GB free disk space (for screenshots and downloads)

## 🛠️ Installation

1. **Clone or download** this repository
2. **Run the setup script**:
   ```powershell
   # For Windows (PowerShell)
   .\setup.ps1
   
   # Or using Python
   python setup.py
   ```

## 🔧 Configuration

Edit `config.json` to customize scraper behavior:

```json
{
    "scraper_config": {
        "target_url": "https://www.booking.com/",
        "max_depth": 20,
        "max_pages": 10000,
        "delay_range": [2, 5],
        "screenshot_enabled": true,
        "headless_mode": false
    }
}
```

## 🏃‍♂️ Usage

Run the scraper:
```bash
python booking_spider.py
```

The scraper will:
1. Start from booking.com homepage
2. Crawl through all internal links
3. Extract comprehensive data from each page
4. Save results to `downloads-booking/`
5. Take screenshots of each page
6. Generate detailed reports

## 📊 Output

The scraper generates several output files:

- `booking_scrape_results_YYYYMMDD_HHMMSS.json` - Full scraped data
- `booking_scrape_summary_YYYYMMDD_HHMMSS.json` - Summary statistics
- `screenshots-booking/` - Page screenshots
- `downloads-booking/` - Downloaded resources

### Data Structure

```json
{
    "pages": [...],           // Page-level data
    "hotels": [...],          // Hotel information
    "destinations": [...],    // Destination data
    "search_filters": [...],  // Search and filter options
    "pricing_data": [...],    // Pricing information
    "reviews": [...],         // User reviews
    "availability_data": [...], // Availability status
    "endpoints": [...],       // API endpoints
    "api_keys": [...],        // Found API keys/tokens
    "resources": [...],       // Downloaded resources
    "forms": [...],           // Form structures
    "javascript_apis": [...], // JavaScript APIs
    "cookies": [...]          // Session cookies
}
```

## 🔍 Extracted Data Types

### Hotel Data
- Hotel names and descriptions
- Pricing information
- Ratings and reviews
- Location details
- Amenities and features
- Availability status

### Search & Filters
- Search parameters
- Filter options
- Sort mechanisms
- Date ranges
- Location filters

### Technical Data
- API endpoints
- Authentication flows
- JavaScript configurations
- Form structures
- Hidden elements
- Session management

## ⚙️ Advanced Configuration

### Depth Control
```python
CONFIG["max_depth"] = 25  # Maximum crawl depth
CONFIG["max_pages"] = 50000  # Maximum pages to crawl
```

### Rate Limiting
```python
CONFIG["delay_range"] = (3, 8)  # Delay between requests (seconds)
```

### Resource Filtering
```python
# Block specific resource types
blocked_resources = ["image", "media", "font"]
```

## 🛡️ Anti-Detection

The scraper includes several anti-detection mechanisms:

- **Realistic browsing patterns**: Random delays and navigation
- **Browser fingerprinting**: Masked automation indicators
- **Request throttling**: Configurable delays between requests
- **User agent rotation**: Realistic browser identification
- **Cookie management**: Proper session handling

## 🔧 Troubleshooting

### Common Issues

1. **Playwright installation fails**:
   ```bash
   pip install --upgrade playwright
   playwright install
   ```

2. **Memory issues**:
   - Reduce `max_pages` in config
   - Enable `headless_mode`
   - Disable screenshots

3. **Rate limiting**:
   - Increase delay ranges
   - Reduce concurrent requests
   - Use proxy rotation

4. **Data extraction issues**:
   - Check CSS selectors in config
   - Update element patterns
   - Review page structure changes

## 📈 Performance Tips

- Use headless mode for faster execution
- Disable screenshots for production runs
- Implement proxy rotation for large-scale scraping
- Monitor memory usage during long runs
- Use SSD storage for better I/O performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is provided for educational and research purposes only. Users are responsible for ensuring their use complies with applicable laws and website terms of service. The authors assume no responsibility for misuse or any legal consequences arising from the use of this software.

## 🔗 Related Projects

- [Scrapy](https://scrapy.org/) - Professional web scraping framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing library
- [Selenium](https://selenium.dev/) - Web automation toolkit
- [Playwright](https://playwright.dev/) - Modern web automation
