# Data Structure Documentation

This document describes the organized folder structure for storing scraped data from Booking.com.

## 📁 Folder Structure

```
data/
├── hotels/                 # Hotel-specific data
├── destinations/           # Destination and location data
├── reviews/               # User reviews and ratings
├── pricing/               # Pricing and rate information
├── api_endpoints/         # API endpoints and authentication data
├── forms/                 # Form structures and user input fields
├── screenshots/           # Page screenshots
├── resources/             # Downloaded images, documents, etc.
├── cookies/               # Session cookies and tracking data
├── javascript_apis/       # JavaScript APIs and global variables
├── search_filters/        # Search filters and sorting options
├── availability/          # Room/hotel availability data
├── logs/                  # Error logs and debugging information
├── raw_pages/             # Raw page data and metadata
└── reports/               # Summary reports and statistics
```

## 📊 Data Types and Contents

### 🏨 Hotels (`data/hotels/`)
Contains detailed information about hotels including:
- Hotel names and descriptions
- Property details and amenities
- Location information
- Contact details
- Property types and categories
- Hotel chains and brands

**File Format**: `hotels_YYYYMMDD_HHMMSS.json`

### 🌍 Destinations (`data/destinations/`)
Geographic and destination-related data:
- City and country information
- Popular destinations
- Destination images and descriptions
- Travel guides and recommendations
- Location coordinates
- Regional information

**File Format**: `destinations_YYYYMMDD_HHMMSS.json`

### ⭐ Reviews (`data/reviews/`)
User-generated content and feedback:
- Review text and ratings
- Review authors and dates
- Review categories (cleanliness, service, location, etc.)
- Helpful votes and interactions
- Review responses from hotels
- Review verification status

**File Format**: `reviews_YYYYMMDD_HHMMSS.json`

### 💰 Pricing (`data/pricing/`)
Financial and rate information:
- Room rates and pricing tiers
- Currency information
- Seasonal pricing variations
- Discounts and promotions
- Tax and fee information
- Payment terms and conditions

**File Format**: `pricing_YYYYMMDD_HHMMSS.json`

### 🔗 API Endpoints (`data/api_endpoints/`)
Technical integration data:
- REST API endpoints
- Authentication mechanisms
- API keys and tokens
- Request/response formats
- Rate limiting information
- OAuth flows and callbacks

**File Format**: `endpoints_YYYYMMDD_HHMMSS.json`, `api_keys_YYYYMMDD_HHMMSS.json`

### 📝 Forms (`data/forms/`)
User interface and interaction data:
- Form structures and fields
- Input validation rules
- Required/optional fields
- Form submission endpoints
- User flow patterns
- Search forms and filters

**File Format**: `forms_YYYYMMDD_HHMMSS.json`

### 📸 Screenshots (`data/screenshots/`)
Visual documentation:
- Full-page screenshots
- Timestamped captures
- Page loading states
- Error pages and messages
- User interface elements
- Mobile and desktop views

**File Format**: `screenshot_N.png` (where N is sequential number)

### 📦 Resources (`data/resources/`)
Downloaded media and documents:
- Hotel images and galleries
- PDF documents and brochures
- Icon files and graphics
- CSS and JavaScript files
- Maps and location images
- User-uploaded content

**File Format**: Original filenames preserved

### 🍪 Cookies (`data/cookies/`)
Session and tracking data:
- Session cookies
- Authentication tokens
- User preferences
- Tracking pixels
- Analytics data
- Third-party cookies

**File Format**: `cookies_YYYYMMDD_HHMMSS.json`

### 🔧 JavaScript APIs (`data/javascript_apis/`)
Client-side technical data:
- Global JavaScript variables
- API configurations
- Client-side routing
- Widget configurations
- Third-party integrations
- Frontend frameworks data

**File Format**: `javascript_apis_YYYYMMDD_HHMMSS.json`

### 🔍 Search Filters (`data/search_filters/`)
Search and filtering mechanisms:
- Available filter options
- Filter categories and values
- Search suggestions
- Auto-complete data
- Popular searches
- Filter combinations

**File Format**: `search_filters_YYYYMMDD_HHMMSS.json`

### 📅 Availability (`data/availability/`)
Booking and availability information:
- Room availability status
- Booking calendars
- Occupancy rates
- Booking restrictions
- Minimum stay requirements
- Cancellation policies

**File Format**: `availability_YYYYMMDD_HHMMSS.json`

### 📋 Logs (`data/logs/`)
System and error information:
- Error messages and stack traces
- Crawl progress logs
- Performance metrics
- Debug information
- System warnings
- Rate limiting notices

**File Format**: `error_log_YYYYMMDD_HHMMSS.txt`

### 📄 Raw Pages (`data/raw_pages/`)
Complete page data and metadata:
- Full HTML content
- Page metadata
- URL structures
- Response headers
- Load times
- Page relationships

**File Format**: `raw_pages_YYYYMMDD_HHMMSS.json`

### 📊 Reports (`data/reports/`)
Summary and analytical data:
- Crawl statistics
- Data quality metrics
- Performance reports
- Coverage analysis
- Error summaries
- Completion status

**File Format**: `booking_scrape_summary_YYYYMMDD_HHMMSS.json`, `booking_scrape_complete_YYYYMMDD_HHMMSS.json`

## 🔒 Data Security and Privacy

### .gitignore Protection
All data folders are protected by .gitignore to prevent accidental uploads:
- Entire `data/` directory is excluded
- Individual file patterns are blocked
- Sensitive information is filtered out

### Data Handling Best Practices
- Personal information is anonymized where possible
- API keys and tokens are stored securely
- Cookie data is handled according to privacy regulations
- User consent and terms of service are respected

## 📈 Usage Examples

### Loading Hotel Data
```python
import json
from pathlib import Path

# Load latest hotel data
hotels_dir = Path("data/hotels")
latest_file = max(hotels_dir.glob("hotels_*.json"))
with open(latest_file) as f:
    hotels = json.load(f)
```

### Analyzing Reviews
```python
# Load and analyze reviews
reviews_dir = Path("data/reviews")
all_reviews = []
for file in reviews_dir.glob("reviews_*.json"):
    with open(file) as f:
        all_reviews.extend(json.load(f))

# Calculate average ratings
ratings = [review.get('rating', 0) for review in all_reviews]
average_rating = sum(ratings) / len(ratings)
```

### Monitoring API Endpoints
```python
# Check for new API endpoints
endpoints_dir = Path("data/api_endpoints")
for file in endpoints_dir.glob("endpoints_*.json"):
    with open(file) as f:
        endpoints = json.load(f)
        print(f"Found {len(endpoints)} API endpoints")
```

## 🚀 Automation and Processing

The data structure supports automated processing:
- Batch processing of similar data types
- Time-series analysis with timestamped files
- Data validation and quality checks
- Automated report generation
- Real-time monitoring and alerts

## 📅 Data Retention and Cleanup

- Files are timestamped for easy identification
- Old data can be archived or deleted based on retention policies
- Summary reports preserve key metrics even after raw data cleanup
- Error logs help debug issues with older crawls
