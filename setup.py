#!/usr/bin/env python3
"""
Setup script for Booking.com scraper
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Booking.com Deep Scraper...")
    
    # Create necessary directories
    directories = [
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
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install Playwright browsers
    if not run_command("playwright install", "Installing Playwright browsers"):
        return False
    
    # Install additional system dependencies for Playwright
    if not run_command("playwright install-deps", "Installing system dependencies"):
        print("⚠️  System dependencies installation failed, but continuing...")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Review and modify config.json if needed")
    print("2. Run the scraper: python booking_spider.py")
    print("3. Monitor output in the terminal")
    print("4. Results will be saved in organized folders under data/")
    print("   - Hotels: data/hotels/")
    print("   - Destinations: data/destinations/")
    print("   - Reviews: data/reviews/")
    print("   - Pricing: data/pricing/")
    print("   - API Endpoints: data/api_endpoints/")
    print("   - Screenshots: data/screenshots/")
    print("   - Reports: data/reports/")
    print("   - Customer Data: data/customers/")
    print("   - Booking IDs: data/bookings/")
    print("   - Confirmations: data/confirmations/")
    print("   - Backend Data: data/backend_data/")
    print("   - Hidden APIs: data/hidden_apis/")
    print("   - Auth Tokens: data/auth_tokens/")
    print("   - Payment Data: data/payment_data/")
    
    print("\n⚠️  Important notes:")
    print("- This scraper is for educational purposes only")
    print("- Respect booking.com's robots.txt and terms of service")
    print("- Use appropriate delays to avoid overwhelming their servers")
    print("- Consider using a VPN or proxy for large-scale scraping")

if __name__ == "__main__":
    main()
