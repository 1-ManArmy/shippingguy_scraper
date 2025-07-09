import os
import re
import json
import random
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime

CONFIG = {
    "target_url": "https://www.booking.com/",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "data_dir": Path(__file__).parent / "data",
    "hotels_dir": Path(__file__).parent / "data" / "hotels",
    "destinations_dir": Path(__file__).parent / "data" / "destinations",
    "reviews_dir": Path(__file__).parent / "data" / "reviews",
    "pricing_dir": Path(__file__).parent / "data" / "pricing",
    "api_endpoints_dir": Path(__file__).parent / "data" / "api_endpoints",
    "forms_dir": Path(__file__).parent / "data" / "forms",
    "screenshots_dir": Path(__file__).parent / "data" / "screenshots",
    "resources_dir": Path(__file__).parent / "data" / "resources",
    "cookies_dir": Path(__file__).parent / "data" / "cookies",
    "javascript_apis_dir": Path(__file__).parent / "data" / "javascript_apis",
    "search_filters_dir": Path(__file__).parent / "data" / "search_filters",
    "availability_dir": Path(__file__).parent / "data" / "availability",
    "logs_dir": Path(__file__).parent / "data" / "logs",
    "raw_pages_dir": Path(__file__).parent / "data" / "raw_pages",
    "reports_dir": Path(__file__).parent / "data" / "reports",
    "customers_dir": Path(__file__).parent / "data" / "customers",
    "guests_dir": Path(__file__).parent / "data" / "guests",
    "bookings_dir": Path(__file__).parent / "data" / "bookings",
    "confirmations_dir": Path(__file__).parent / "data" / "confirmations",
    "tickets_dir": Path(__file__).parent / "data" / "tickets",
    "backend_data_dir": Path(__file__).parent / "data" / "backend_data",
    "hidden_apis_dir": Path(__file__).parent / "data" / "hidden_apis",
    "internal_endpoints_dir": Path(__file__).parent / "data" / "internal_endpoints",
    "auth_tokens_dir": Path(__file__).parent / "data" / "auth_tokens",
    "session_data_dir": Path(__file__).parent / "data" / "session_data",
    "payment_data_dir": Path(__file__).parent / "data" / "payment_data",
    "reservation_data_dir": Path(__file__).parent / "data" / "reservation_data",
    "user_profiles_dir": Path(__file__).parent / "data" / "user_profiles",
    "booking_flows_dir": Path(__file__).parent / "data" / "booking_flows",
    "internal_configs_dir": Path(__file__).parent / "data" / "internal_configs",
    "database_leaks_dir": Path(__file__).parent / "data" / "database_leaks",
    "admin_panels_dir": Path(__file__).parent / "data" / "admin_panels",
    "debug_info_dir": Path(__file__).parent / "data" / "debug_info",
    "max_depth": 20,
    "delay_range": (2, 5),
    "domains": ["booking.com", "bstatic.com", "bookingplanner.com"],
    "max_pages": 10000
}

visited = set()
results = {
    "pages": [],
    "cookies": [],
    "endpoints": [],
    "api_keys": [],
    "resources": [],
    "hotels": [],
    "destinations": [],
    "search_data": [],
    "pricing_data": [],
    "reviews": [],
    "forms": [],
    "javascript_apis": [],
    "booking_flows": [],
    "user_data": [],
    "search_filters": [],
    "availability_data": [],
    "customers": [],
    "guests": [],
    "bookings": [],
    "confirmations": [],
    "tickets": [],
    "backend_data": [],
    "hidden_apis": [],
    "internal_endpoints": [],
    "auth_tokens": [],
    "session_data": [],
    "payment_data": [],
    "reservation_data": [],
    "user_profiles": [],
    "internal_configs": [],
    "database_leaks": [],
    "admin_panels": [],
    "debug_info": []
}

def log(msg, *args):
    print(f"[{datetime.now().isoformat()}] {msg}", *args)

def is_valid_url(url):
    """Check if URL belongs to booking.com domains"""
    if not url:
        return False
    
    parsed = urlparse(url)
    return any(domain in parsed.netloc.lower() for domain in CONFIG["domains"])

async def download_resource(url, file_path):
    """Download resources like images, documents, etc."""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    with open(file_path, "wb") as f:
                        f.write(await response.read())
                    log(f"📦 Downloaded: {file_path.name}")
    except Exception as e:
        log(f"❌ Failed to download {url}: {e}")

async def extract_booking_data(page, url):
    """Extract booking-specific data from the page"""
    booking_data = {}
    
    try:
        # Extract hotel data
        hotels = await page.evaluate("""
            () => {
                const hotels = [];
                const hotelCards = document.querySelectorAll('[data-testid="property-card"]');
                hotelCards.forEach(card => {
                    const hotel = {};
                    const nameEl = card.querySelector('[data-testid="title"]');
                    const priceEl = card.querySelector('[data-testid="price-and-discounted-price"]');
                    const ratingEl = card.querySelector('[data-testid="review-score"]');
                    const locationEl = card.querySelector('[data-testid="address"]');
                    
                    if (nameEl) hotel.name = nameEl.textContent.trim();
                    if (priceEl) hotel.price = priceEl.textContent.trim();
                    if (ratingEl) hotel.rating = ratingEl.textContent.trim();
                    if (locationEl) hotel.location = locationEl.textContent.trim();
                    
                    hotels.push(hotel);
                });
                return hotels;
            }
        """)
        
        # Extract destination data
        destinations = await page.evaluate("""
            () => {
                const destinations = [];
                const destElements = document.querySelectorAll('[data-testid="destination-container"]');
                destElements.forEach(dest => {
                    const name = dest.querySelector('.destination-name')?.textContent?.trim();
                    const image = dest.querySelector('img')?.src;
                    if (name) destinations.push({name, image});
                });
                return destinations;
            }
        """)
        
        # Extract search filters
        search_filters = await page.evaluate("""
            () => {
                const filters = {};
                const filterElements = document.querySelectorAll('[data-testid*="filter"]');
                filterElements.forEach(filter => {
                    const type = filter.getAttribute('data-testid');
                    const value = filter.textContent?.trim();
                    if (type && value) filters[type] = value;
                });
                return filters;
            }
        """)
        
        # Extract pricing information
        pricing_data = await page.evaluate("""
            () => {
                const pricing = [];
                const priceElements = document.querySelectorAll('[data-testid*="price"]');
                priceElements.forEach(price => {
                    const amount = price.textContent?.trim();
                    const currency = price.getAttribute('data-currency');
                    if (amount) pricing.push({amount, currency});
                });
                return pricing;
            }
        """)
        
        # Extract reviews
        reviews = await page.evaluate("""
            () => {
                const reviews = [];
                const reviewElements = document.querySelectorAll('[data-testid="review-card"]');
                reviewElements.forEach(review => {
                    const text = review.querySelector('.review-text')?.textContent?.trim();
                    const rating = review.querySelector('.review-rating')?.textContent?.trim();
                    const author = review.querySelector('.review-author')?.textContent?.trim();
                    if (text) reviews.push({text, rating, author});
                });
                return reviews;
            }
        """)
        
        # Extract availability data
        availability_data = await page.evaluate("""
            () => {
                const availability = [];
                const availElements = document.querySelectorAll('[data-testid*="availability"]');
                availElements.forEach(avail => {
                    const status = avail.textContent?.trim();
                    const date = avail.getAttribute('data-date');
                    if (status) availability.push({status, date});
                });
                return availability;
            }
        """)
        
        booking_data = {
            "hotels": hotels,
            "destinations": destinations,
            "search_filters": search_filters,
            "pricing_data": pricing_data,
            "reviews": reviews,
            "availability_data": availability_data
        }
        
    except Exception as e:
        log(f"❌ Error extracting booking data: {e}")
    
    return booking_data

async def extract_forms(page):
    """Extract all forms from the page"""
    try:
        forms = await page.evaluate("""
            () => {
                const forms = [];
                document.querySelectorAll('form').forEach(form => {
                    const formData = {
                        action: form.action,
                        method: form.method,
                        id: form.id,
                        className: form.className,
                        fields: []
                    };
                    
                    form.querySelectorAll('input, select, textarea').forEach(field => {
                        formData.fields.push({
                            name: field.name,
                            type: field.type,
                            id: field.id,
                            placeholder: field.placeholder,
                            required: field.required
                        });
                    });
                    
                    forms.push(formData);
                });
                return forms;
            }
        """)
        return forms
    except Exception as e:
        log(f"❌ Error extracting forms: {e}")
        return []

async def extract_javascript_apis(page):
    """Extract JavaScript APIs and global variables"""
    try:
        js_data = await page.evaluate(r"""
            () => {
                const apis = {};
                const globals = {};
                
                // Extract global variables
                for (let key in window) {
                    if (typeof window[key] === 'object' && window[key] !== null) {
                        try {
                            if (key.includes('booking') || key.includes('api') || key.includes('config')) {
                                globals[key] = JSON.stringify(window[key]);
                            }
                        } catch (e) {
                            globals[key] = 'Cannot serialize';
                        }
                    }
                }
                
                // Extract API endpoints from scripts
                const scripts = Array.from(document.querySelectorAll('script'));
                const apiEndpoints = [];
                scripts.forEach(script => {
                    if (script.textContent) {
                        const matches = script.textContent.match(/['"]\/api\/[^'"]+/g);
                        if (matches) {
                            apiEndpoints.push(...matches.map(m => m.replace(/['"]/g, '')));
                        }
                    }
                });
                
                return {globals, apiEndpoints};
            }
        """)
        return js_data
    except Exception as e:
        log(f"❌ Error extracting JavaScript APIs: {e}")
        return {}

async def extract_hidden_gems(page, url):
    """Extract hidden backend data - the real gems that frontend doesn't show"""
    hidden_gems = {}
    
    try:
        # Extract booking IDs and confirmation codes
        booking_data = await page.evaluate(r"""
            () => {
                const bookingData = {};
                const text = document.documentElement.innerHTML;
                
                // Booking IDs (various formats)
                const bookingPatterns = [
                    /booking[_-]?id['":\s]*['"]?([A-Z0-9]{8,})/gi,
                    /confirmation[_-]?number['":\s]*['"]?([A-Z0-9]{6,})/gi,
                    /reservation[_-]?id['":\s]*['"]?([A-Z0-9]{8,})/gi,
                    /booking[_-]?reference['":\s]*['"]?([A-Z0-9]{6,})/gi,
                    /pin[_-]?code['":\s]*['"]?([0-9]{4,8})/gi,
                    /ticket[_-]?number['":\s]*['"]?([A-Z0-9]{6,})/gi
                ];
                
                bookingPatterns.forEach(pattern => {
                    const matches = [...text.matchAll(pattern)];
                    matches.forEach(match => {
                        const type = match[0].split(/[_:'"]/)[0];
                        if (!bookingData[type]) bookingData[type] = [];
                        bookingData[type].push(match[1]);
                    });
                });
                
                return bookingData;
            }
        """)
        
        # Extract customer/guest data
        customer_data = await page.evaluate(r"""
            () => {
                const customers = {};
                const text = document.documentElement.innerHTML;
                
                // Customer data patterns
                const patterns = {
                    emails: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
                    phones: /[+]?[0-9]{1,3}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}/g,
                    names: /guest[_-]?name['":\s]*['"]?([A-Za-z\s]{2,30})/gi,
                    addresses: /address['":\s]*['"]?([A-Za-z0-9\s,.-]{10,})/gi,
                    creditCards: /[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}/g,
                    passports: /passport[_-]?number['":\s]*['"]?([A-Z0-9]{6,10})/gi
                };
                
                Object.keys(patterns).forEach(key => {
                    const matches = [...text.matchAll(patterns[key])];
                    customers[key] = matches.map(m => m[1] || m[0]);
                });
                
                return customers;
            }
        """)
        
        # Extract payment and transaction data
        payment_data = await page.evaluate(r"""
            () => {
                const payments = {};
                const text = document.documentElement.innerHTML;
                
                // Payment patterns
                const paymentPatterns = [
                    /payment[_-]?id['":\s]*['"]?([A-Z0-9]{8,})/gi,
                    /transaction[_-]?id['":\s]*['"]?([A-Z0-9]{8,})/gi,
                    /order[_-]?id['":\s]*['"]?([A-Z0-9]{8,})/gi,
                    /invoice[_-]?number['":\s]*['"]?([A-Z0-9]{6,})/gi,
                    /amount['":\s]*['"]?([0-9]{1,6}\.[0-9]{2})/gi,
                    /currency['":\s]*['"]?([A-Z]{3})/gi,
                    /card[_-]?token['":\s]*['"]?([A-Z0-9]{16,})/gi
                ];
                
                paymentPatterns.forEach(pattern => {
                    const matches = [...text.matchAll(pattern)];
                    const type = pattern.source.split(/[_:'"]/)[0];
                    payments[type] = matches.map(m => m[1]);
                });
                
                return payments;
            }
        """)
        
        # Extract hidden APIs and internal endpoints
        hidden_apis = await page.evaluate(r"""
            () => {
                const apis = {};
                const scripts = Array.from(document.querySelectorAll('script'));
                
                scripts.forEach(script => {
                    if (script.textContent) {
                        const text = script.textContent;
                        
                        // Internal API patterns
                        const apiPatterns = [
                            /['"]\/internal\/[^'"]+/g,
                            /['"]\/admin\/[^'"]+/g,
                            /['"]\/api\/v[0-9]+\/[^'"]+/g,
                            /['"]\/backend\/[^'"]+/g,
                            /['"]\/private\/[^'"]+/g,
                            /['"]\/system\/[^'"]+/g,
                            /['"]\/debug\/[^'"]+/g
                        ];
                        
                        apiPatterns.forEach(pattern => {
                            const matches = [...text.matchAll(pattern)];
                            matches.forEach(match => {
                                const endpoint = match[0].replace(/['"]/g, '');
                                const type = endpoint.split('/')[1];
                                if (!apis[type]) apis[type] = [];
                                apis[type].push(endpoint);
                            });
                        });
                    }
                });
                
                return apis;
            }
        """)
        
        # Extract authentication tokens and session data
        auth_data = await page.evaluate(r"""
            () => {
                const authData = {};
                const text = document.documentElement.innerHTML;
                
                // Auth patterns
                const authPatterns = [
                    /access_token['":\s]*['"]?([A-Za-z0-9._-]{20,})/gi,
                    /refresh_token['":\s]*['"]?([A-Za-z0-9._-]{20,})/gi,
                    /session_id['":\s]*['"]?([A-Za-z0-9._-]{20,})/gi,
                    /csrf[_-]?token['":\s]*['"]?([A-Za-z0-9._-]{20,})/gi,
                    /jwt['":\s]*['"]?([A-Za-z0-9._-]{20,})/gi,
                    /bearer[\s]+([A-Za-z0-9._-]{20,})/gi,
                    /authorization['":\s]*['"]?bearer\s+([A-Za-z0-9._-]{20,})/gi
                ];
                
                authPatterns.forEach(pattern => {
                    const matches = [...text.matchAll(pattern)];
                    const type = pattern.source.split(/[_:'"]/)[0];
                    authData[type] = matches.map(m => m[1]);
                });
                
                return authData;
            }
        """)
        
        # Extract database leaks and debug information
        debug_data = await page.evaluate(r"""
            () => {
                const debugData = {};
                const text = document.documentElement.innerHTML;
                
                // Debug patterns
                const debugPatterns = [
                    /database[_-]?error['":\s]*['"]?([^'"]{20,})/gi,
                    /sql[_-]?query['":\s]*['"]?([^'"]{20,})/gi,
                    /stack[_-]?trace['":\s]*['"]?([^'"]{50,})/gi,
                    /debug[_-]?info['":\s]*['"]?([^'"]{20,})/gi,
                    /error[_-]?message['":\s]*['"]?([^'"]{20,})/gi,
                    /exception['":\s]*['"]?([^'"]{20,})/gi
                ];
                
                debugPatterns.forEach(pattern => {
                    const matches = [...text.matchAll(pattern)];
                    const type = pattern.source.split(/[_:'"]/)[0];
                    debugData[type] = matches.map(m => m[1]);
                });
                
                return debugData;
            }
        """)
        
        # Extract internal configurations
        config_data = await page.evaluate("""
            () => {
                const configs = {};
                
                // Look for configuration objects
                for (let key in window) {
                    if (typeof window[key] === 'object' && window[key] !== null) {
                        if (key.toLowerCase().includes('config') || 
                            key.toLowerCase().includes('settings') ||
                            key.toLowerCase().includes('env') ||
                            key.toLowerCase().includes('constants')) {
                            try {
                                configs[key] = JSON.parse(JSON.stringify(window[key]));
                            } catch (e) {
                                configs[key] = 'Cannot serialize';
                            }
                        }
                    }
                }
                
                return configs;
            }
        """)
        
        # Extract admin panel indicators
        admin_data = await page.evaluate("""
            () => {
                const adminData = {};
                const text = document.documentElement.innerHTML.toLowerCase();
                
                // Admin indicators
                const adminPatterns = [
                    'admin panel',
                    'dashboard',
                    'control panel',
                    'management interface',
                    'staff portal',
                    'internal tools',
                    'system administration'
                ];
                
                adminPatterns.forEach(pattern => {
                    if (text.includes(pattern)) {
                        adminData[pattern] = true;
                    }
                });
                
                // Look for admin URLs
                const links = Array.from(document.querySelectorAll('a[href]'));
                const adminLinks = links.filter(link => 
                    link.href.includes('/admin') || 
                    link.href.includes('/dashboard') ||
                    link.href.includes('/manage') ||
                    link.href.includes('/staff')
                );
                
                adminData.adminLinks = adminLinks.map(link => link.href);
                
                return adminData;
            }
        """)
        
        hidden_gems = {
            "booking_data": booking_data,
            "customer_data": customer_data,
            "payment_data": payment_data,
            "hidden_apis": hidden_apis,
            "auth_data": auth_data,
            "debug_data": debug_data,
            "config_data": config_data,
            "admin_data": admin_data
        }
        
    except Exception as e:
        log(f"❌ Error extracting hidden gems: {e}")
    
    return hidden_gems

async def crawl(page, url, depth=0):
    if url in visited or depth > CONFIG["max_depth"] or len(visited) > CONFIG["max_pages"]:
        return
    visited.add(url)

    log(f"🌐 Crawling: {url} (depth {depth})")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(2)  # Let page load completely
    except Exception as err:
        log(f"❌ Failed to load: {url} ({err})")
        return

    # Take screenshot
    try:
        screenshot_path = CONFIG["screenshots_dir"] / f"screenshot_{len(visited)}.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        log(f"📸 Screenshot saved: {screenshot_path.name}")
    except Exception as e:
        log(f"❌ Screenshot failed: {e}")

    # Wait for dynamic content
    await asyncio.sleep(random.uniform(2, 4))

    # Collect all links
    links = await page.evaluate("""
        () => {
            const links = [];
            document.querySelectorAll('a[href]').forEach(link => {
                const href = link.href;
                if (href && (href.includes('booking.com') || href.includes('bstatic.com'))) {
                    links.push(href);
                }
            });
            return [...new Set(links)];
        }
    """)

    # Collect hidden elements
    hidden_elements = await page.evaluate("""
        () => {
            const hidden = [];
            document.querySelectorAll('*').forEach(el => {
                const style = window.getComputedStyle(el);
                if (style.display === 'none' || style.visibility === 'hidden') {
                    const text = el.textContent?.trim();
                    if (text && text.length > 0) {
                        hidden.push(text);
                    }
                }
            });
            return hidden;
        }
    """)

    # Collect cookies
    cookies = await page.context.cookies()
    results["cookies"].extend(cookies)

    # Collect endpoints (authentication, API, booking flows)
    endpoints = [href for href in links if any(keyword in href.lower() for keyword in 
                ["auth", "api", "login", "booking", "payment", "checkout", "reservation"])]
    results["endpoints"].extend(endpoints)

    # Collect API keys and tokens
    page_content = await page.content()
    api_patterns = [
        r"(api_key|apikey|token|secret|key)[\s]*[:=][\s]*['\"]([A-Za-z0-9_\-]+)['\"]",
        r"(api_key|token|secret)=([A-Za-z0-9_\-]+)",
        r"Bearer\s+([A-Za-z0-9_\-\.]+)",
        r"(access_token|refresh_token)[\s]*[:=][\s]*['\"]([A-Za-z0-9_\-]+)['\"]"
    ]
    
    for pattern in api_patterns:
        matches = re.findall(pattern, page_content, re.I)
        api_keys = [m[1] if isinstance(m, tuple) else m for m in matches]
        results["api_keys"].extend(api_keys)

    # Collect downloadable resources
    resources = await page.evaluate("""
        () => {
            const resources = [];
            document.querySelectorAll('a[href], img[src], link[href]').forEach(el => {
                const url = el.href || el.src;
                if (url && /\\.(jpg|jpeg|png|gif|pdf|docx|xlsx|zip|json|xml|css|js)$/i.test(url)) {
                    resources.push(url);
                }
            });
            return [...new Set(resources)];
        }
    """)
    results["resources"].extend(resources)

    # Extract booking-specific data
    booking_data = await extract_booking_data(page, url)
    results["hotels"].extend(booking_data.get("hotels", []))
    results["destinations"].extend(booking_data.get("destinations", []))
    results["search_filters"].append(booking_data.get("search_filters", {}))
    results["pricing_data"].extend(booking_data.get("pricing_data", []))
    results["reviews"].extend(booking_data.get("reviews", []))
    results["availability_data"].extend(booking_data.get("availability_data", []))

    # Extract hidden gems - the real valuable backend data
    hidden_gems = await extract_hidden_gems(page, url)
    results["bookings"].extend(hidden_gems.get("booking_data", {}).get("booking", []))
    results["confirmations"].extend(hidden_gems.get("booking_data", {}).get("confirmation", []))
    results["tickets"].extend(hidden_gems.get("booking_data", {}).get("ticket", []))
    results["customers"].append(hidden_gems.get("customer_data", {}))
    results["payment_data"].append(hidden_gems.get("payment_data", {}))
    results["hidden_apis"].append(hidden_gems.get("hidden_apis", {}))
    results["auth_tokens"].append(hidden_gems.get("auth_data", {}))
    results["debug_info"].append(hidden_gems.get("debug_data", {}))
    results["internal_configs"].append(hidden_gems.get("config_data", {}))
    results["admin_panels"].append(hidden_gems.get("admin_data", {}))
    results["backend_data"].append(hidden_gems)

    # Extract forms
    forms = await extract_forms(page)
    results["forms"].extend(forms)

    # Extract JavaScript APIs
    js_data = await extract_javascript_apis(page)
    results["javascript_apis"].append(js_data)

    # Extract user data patterns
    user_data = await page.evaluate("""
        () => {
            const userData = [];
            const patterns = ['email', 'phone', 'name', 'address', 'card', 'passport'];
            patterns.forEach(pattern => {
                const elements = document.querySelectorAll(`[placeholder*="${pattern}"], [name*="${pattern}"], [id*="${pattern}"]`);
                elements.forEach(el => {
                    userData.push({
                        type: pattern,
                        element: el.tagName,
                        name: el.name,
                        id: el.id,
                        placeholder: el.placeholder
                    });
                });
            });
            return userData;
        }
    """)
    results["user_data"].extend(user_data)

    # Save page data
    results["pages"].append({
        "url": url,
        "depth": depth,
        "title": await page.title(),
        "links": links,
        "hidden_elements": hidden_elements,
        "endpoints": endpoints,
        "api_keys": len([k for k in results["api_keys"] if k]),
        "resources": len(resources),
        "booking_data": booking_data,
        "forms": len(forms),
        "timestamp": datetime.now().isoformat()
    })

    # Download some resources (limit to avoid overwhelming)
    for resource in resources[:5]:  # Limit to first 5 resources per page
        try:
            file_name = os.path.basename(resource.split("?")[0])
            if file_name:
                file_path = CONFIG["resources_dir"] / file_name
                await download_resource(resource, file_path)
        except Exception as e:
            log(f"❌ Resource download error: {e}")

    # Random delay to avoid rate limiting
    delay = random.uniform(*CONFIG["delay_range"])
    await asyncio.sleep(delay)

    # Recursively crawl valid internal links
    valid_links = [link for link in links if is_valid_url(link) and link not in visited]
    random.shuffle(valid_links)  # Randomize crawling order
    
    for link in valid_links[:10]:  # Limit to 10 links per page to manage depth
        if len(visited) < CONFIG["max_pages"]:
            await crawl(page, link, depth + 1)

async def main():
    log("🚀 Automation started: Booking.com Deep Scraper")
    
    # Create directories
    create_directories()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Set to True for headless mode
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--start-maximized",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        
        context = await browser.new_context(
            user_agent=CONFIG["user_agent"],
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        
        page = await context.new_page()
        
        # Block unnecessary resources to speed up crawling
        await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media"] else route.continue_())
        
        try:
            await crawl(page, CONFIG["target_url"])
            
            # Save data to organized folders
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            await save_data_to_folders(timestamp)
            
            # Save complete results
            out_file = CONFIG["reports_dir"] / f"booking_scrape_complete_{timestamp}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            
            # Save summary
            summary = {
                "scrape_info": {
                    "timestamp": timestamp,
                    "target_url": CONFIG["target_url"],
                    "max_depth": CONFIG["max_depth"],
                    "max_pages": CONFIG["max_pages"]
                },
                "statistics": {
                    "total_pages": len(results["pages"]),
                    "total_hotels": len(results["hotels"]),
                    "total_destinations": len(results["destinations"]),
                    "total_reviews": len(results["reviews"]),
                    "total_pricing_data": len(results["pricing_data"]),
                    "total_endpoints": len(results["endpoints"]),
                    "total_api_keys": len(results["api_keys"]),
                    "total_resources": len(results["resources"]),
                    "total_forms": len(results["forms"]),
                    "total_cookies": len(results["cookies"]),
                    "total_search_filters": len(results["search_filters"]),
                    "total_availability_data": len(results["availability_data"])
                },
                "data_locations": {
                    "hotels": f"data/hotels/hotels_{timestamp}.json",
                    "destinations": f"data/destinations/destinations_{timestamp}.json",
                    "reviews": f"data/reviews/reviews_{timestamp}.json",
                    "pricing": f"data/pricing/pricing_{timestamp}.json",
                    "api_endpoints": f"data/api_endpoints/endpoints_{timestamp}.json",
                    "forms": f"data/forms/forms_{timestamp}.json",
                    "cookies": f"data/cookies/cookies_{timestamp}.json",
                    "javascript_apis": f"data/javascript_apis/javascript_apis_{timestamp}.json",
                    "search_filters": f"data/search_filters/search_filters_{timestamp}.json",
                    "availability": f"data/availability/availability_{timestamp}.json",
                    "raw_pages": f"data/raw_pages/raw_pages_{timestamp}.json",
                    "screenshots": "data/screenshots/",
                    "resources": "data/resources/"
                }
            }
            
            summary_file = CONFIG["reports_dir"] / f"booking_scrape_summary_{timestamp}.json"
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            log(f"✅ Full site crawl complete! Results saved to organized folders")
            log(f"📊 Summary saved to: {summary_file}")
            log(f"📈 Total pages crawled: {len(results['pages'])}")
            log(f"🏨 Hotels found: {len(results['hotels'])}")
            log(f"🌍 Destinations found: {len(results['destinations'])}")
            log(f"⭐ Reviews collected: {len(results['reviews'])}")
            
        except Exception as err:
            log(f"❌ Error during crawl: {err}")
            # Save error log
            error_file = CONFIG["logs_dir"] / f"error_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(error_file, "w", encoding="utf-8") as f:
                f.write(f"Error: {err}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            
        finally:
            await browser.close()
            log("🛑 Automation finished. Browser closed.")

def create_directories():
    """Create all necessary directories for organized data storage"""
    directories = [
        CONFIG["data_dir"],
        CONFIG["hotels_dir"],
        CONFIG["destinations_dir"],
        CONFIG["reviews_dir"],
        CONFIG["pricing_dir"],
        CONFIG["api_endpoints_dir"],
        CONFIG["forms_dir"],
        CONFIG["screenshots_dir"],
        CONFIG["resources_dir"],
        CONFIG["cookies_dir"],
        CONFIG["javascript_apis_dir"],
        CONFIG["search_filters_dir"],
        CONFIG["availability_dir"],
        CONFIG["logs_dir"],
        CONFIG["raw_pages_dir"],
        CONFIG["reports_dir"],
        CONFIG["customers_dir"],
        CONFIG["guests_dir"],
        CONFIG["bookings_dir"],
        CONFIG["confirmations_dir"],
        CONFIG["tickets_dir"],
        CONFIG["backend_data_dir"],
        CONFIG["hidden_apis_dir"],
        CONFIG["internal_endpoints_dir"],
        CONFIG["auth_tokens_dir"],
        CONFIG["session_data_dir"],
        CONFIG["payment_data_dir"],
        CONFIG["reservation_data_dir"],
        CONFIG["user_profiles_dir"],
        CONFIG["booking_flows_dir"],
        CONFIG["internal_configs_dir"],
        CONFIG["database_leaks_dir"],
        CONFIG["admin_panels_dir"],
        CONFIG["debug_info_dir"]
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        log(f"📁 Created directory: {directory.name}")

async def save_data_to_folders(timestamp):
    """Save collected data to organized folders"""
    try:
        # Save hotels data
        if results["hotels"]:
            hotels_file = CONFIG["hotels_dir"] / f"hotels_{timestamp}.json"
            with open(hotels_file, "w", encoding="utf-8") as f:
                json.dump(results["hotels"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved hotels data: {hotels_file.name}")
        
        # Save destinations data
        if results["destinations"]:
            destinations_file = CONFIG["destinations_dir"] / f"destinations_{timestamp}.json"
            with open(destinations_file, "w", encoding="utf-8") as f:
                json.dump(results["destinations"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved destinations data: {destinations_file.name}")
        
        # Save reviews data
        if results["reviews"]:
            reviews_file = CONFIG["reviews_dir"] / f"reviews_{timestamp}.json"
            with open(reviews_file, "w", encoding="utf-8") as f:
                json.dump(results["reviews"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved reviews data: {reviews_file.name}")
        
        # Save pricing data
        if results["pricing_data"]:
            pricing_file = CONFIG["pricing_dir"] / f"pricing_{timestamp}.json"
            with open(pricing_file, "w", encoding="utf-8") as f:
                json.dump(results["pricing_data"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved pricing data: {pricing_file.name}")
        
        # Save API endpoints
        if results["endpoints"]:
            endpoints_file = CONFIG["api_endpoints_dir"] / f"endpoints_{timestamp}.json"
            with open(endpoints_file, "w", encoding="utf-8") as f:
                json.dump(results["endpoints"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved API endpoints: {endpoints_file.name}")
        
        # Save forms data
        if results["forms"]:
            forms_file = CONFIG["forms_dir"] / f"forms_{timestamp}.json"
            with open(forms_file, "w", encoding="utf-8") as f:
                json.dump(results["forms"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved forms data: {forms_file.name}")
        
        # Save cookies
        if results["cookies"]:
            cookies_file = CONFIG["cookies_dir"] / f"cookies_{timestamp}.json"
            with open(cookies_file, "w", encoding="utf-8") as f:
                json.dump(results["cookies"], f, indent=2, ensure_ascii=False, default=str)
            log(f"💾 Saved cookies data: {cookies_file.name}")
        
        # Save JavaScript APIs
        if results["javascript_apis"]:
            js_apis_file = CONFIG["javascript_apis_dir"] / f"javascript_apis_{timestamp}.json"
            with open(js_apis_file, "w", encoding="utf-8") as f:
                json.dump(results["javascript_apis"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved JavaScript APIs: {js_apis_file.name}")
        
        # Save search filters
        if results["search_filters"]:
            filters_file = CONFIG["search_filters_dir"] / f"search_filters_{timestamp}.json"
            with open(filters_file, "w", encoding="utf-8") as f:
                json.dump(results["search_filters"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved search filters: {filters_file.name}")
        
        # Save availability data
        if results["availability_data"]:
            availability_file = CONFIG["availability_dir"] / f"availability_{timestamp}.json"
            with open(availability_file, "w", encoding="utf-8") as f:
                json.dump(results["availability_data"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved availability data: {availability_file.name}")
        
        # Save raw pages data
        if results["pages"]:
            pages_file = CONFIG["raw_pages_dir"] / f"raw_pages_{timestamp}.json"
            with open(pages_file, "w", encoding="utf-8") as f:
                json.dump(results["pages"], f, indent=2, ensure_ascii=False, default=str)
            log(f"💾 Saved raw pages data: {pages_file.name}")
        
        # Save API keys (if any found)
        if results["api_keys"]:
            api_keys_file = CONFIG["api_endpoints_dir"] / f"api_keys_{timestamp}.json"
            with open(api_keys_file, "w", encoding="utf-8") as f:
                json.dump(results["api_keys"], f, indent=2, ensure_ascii=False)
            log(f"💾 Saved API keys: {api_keys_file.name}")
        
        # Save hidden gems - the real valuable data
        if results["customers"]:
            customers_file = CONFIG["customers_dir"] / f"customers_{timestamp}.json"
            with open(customers_file, "w", encoding="utf-8") as f:
                json.dump(results["customers"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved customer data: {customers_file.name}")
        
        if results["bookings"]:
            bookings_file = CONFIG["bookings_dir"] / f"bookings_{timestamp}.json"
            with open(bookings_file, "w", encoding="utf-8") as f:
                json.dump(results["bookings"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved booking IDs: {bookings_file.name}")
        
        if results["confirmations"]:
            confirmations_file = CONFIG["confirmations_dir"] / f"confirmations_{timestamp}.json"
            with open(confirmations_file, "w", encoding="utf-8") as f:
                json.dump(results["confirmations"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved confirmation codes: {confirmations_file.name}")
        
        if results["tickets"]:
            tickets_file = CONFIG["tickets_dir"] / f"tickets_{timestamp}.json"
            with open(tickets_file, "w", encoding="utf-8") as f:
                json.dump(results["tickets"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved ticket numbers: {tickets_file.name}")
        
        if results["payment_data"]:
            payment_file = CONFIG["payment_data_dir"] / f"payment_data_{timestamp}.json"
            with open(payment_file, "w", encoding="utf-8") as f:
                json.dump(results["payment_data"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved payment data: {payment_file.name}")
        
        if results["hidden_apis"]:
            hidden_apis_file = CONFIG["hidden_apis_dir"] / f"hidden_apis_{timestamp}.json"
            with open(hidden_apis_file, "w", encoding="utf-8") as f:
                json.dump(results["hidden_apis"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved hidden APIs: {hidden_apis_file.name}")
        
        if results["auth_tokens"]:
            auth_tokens_file = CONFIG["auth_tokens_dir"] / f"auth_tokens_{timestamp}.json"
            with open(auth_tokens_file, "w", encoding="utf-8") as f:
                json.dump(results["auth_tokens"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved auth tokens: {auth_tokens_file.name}")
        
        if results["debug_info"]:
            debug_file = CONFIG["debug_info_dir"] / f"debug_info_{timestamp}.json"
            with open(debug_file, "w", encoding="utf-8") as f:
                json.dump(results["debug_info"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved debug info: {debug_file.name}")
        
        if results["internal_configs"]:
            configs_file = CONFIG["internal_configs_dir"] / f"internal_configs_{timestamp}.json"
            with open(configs_file, "w", encoding="utf-8") as f:
                json.dump(results["internal_configs"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved internal configs: {configs_file.name}")
        
        if results["admin_panels"]:
            admin_file = CONFIG["admin_panels_dir"] / f"admin_panels_{timestamp}.json"
            with open(admin_file, "w", encoding="utf-8") as f:
                json.dump(results["admin_panels"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved admin panel data: {admin_file.name}")
        
        if results["backend_data"]:
            backend_file = CONFIG["backend_data_dir"] / f"backend_data_{timestamp}.json"
            with open(backend_file, "w", encoding="utf-8") as f:
                json.dump(results["backend_data"], f, indent=2, ensure_ascii=False)
            log(f"💎 Saved backend data: {backend_file.name}")
        
    except Exception as e:
        log(f"❌ Error saving data to folders: {e}")
