# PowerShell setup script for Booking.com scraper
Write-Host "🚀 Setting up Booking.com Deep Scraper..." -ForegroundColor Green

# Create necessary directories
$directories = @(
    "data",
    "data/hotels",
    "data/destinations", 
    "data/reviews",
    "data/pricing",
    "data/api_endpoints",
    "data/forms",
    "data/screenshots",
    "data/resources",
    "data/cookies",
    "data/javascript_apis",
    "data/search_filters",
    "data/availability",
    "data/logs",
    "data/raw_pages",
    "data/reports",
    "data/customers",
    "data/guests",
    "data/bookings",
    "data/confirmations",
    "data/tickets",
    "data/backend_data",
    "data/hidden_apis",
    "data/internal_endpoints",
    "data/auth_tokens",
    "data/session_data",
    "data/payment_data",
    "data/reservation_data",
    "data/user_profiles",
    "data/booking_flows",
    "data/internal_configs",
    "data/database_leaks",
    "data/admin_panels",
    "data/debug_info"
)
foreach ($directory in $directories) {
    if (!(Test-Path $directory)) {
        New-Item -ItemType Directory -Path $directory
        Write-Host "📁 Created directory: $directory" -ForegroundColor Yellow
    }
}

# Install Python dependencies
Write-Host "🔧 Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

# Install Playwright browsers
Write-Host "🔧 Installing Playwright browsers..." -ForegroundColor Cyan
playwright install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Playwright browsers installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install Playwright browsers" -ForegroundColor Red
    exit 1
}

# Install system dependencies (optional)
Write-Host "🔧 Installing system dependencies..." -ForegroundColor Cyan
playwright install-deps

Write-Host "`n🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor White
Write-Host "1. Review and modify config.json if needed"
Write-Host "2. Run the scraper: python booking_spider.py"
Write-Host "3. Monitor output in the terminal"
Write-Host "4. Results will be saved in organized folders under data/"
Write-Host "   - Hotels: data/hotels/"
Write-Host "   - Destinations: data/destinations/"
Write-Host "   - Reviews: data/reviews/"
Write-Host "   - Pricing: data/pricing/"
Write-Host "   - API Endpoints: data/api_endpoints/"
Write-Host "   - Screenshots: data/screenshots/"
Write-Host "   - Reports: data/reports/"

Write-Host "`n⚠️  Important notes:" -ForegroundColor Yellow
Write-Host "- This scraper is for educational purposes only"
Write-Host "- Respect booking.com's robots.txt and terms of service"
Write-Host "- Use appropriate delays to avoid overwhelming their servers"
Write-Host "- Consider using a VPN or proxy for large-scale scraping"
