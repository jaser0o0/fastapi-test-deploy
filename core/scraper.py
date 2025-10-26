"""
Pinterest web scraper for FitFindr.
Scrapes fashion items from Pinterest based on style keywords.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import re

class PinterestScraper:
    """Pinterest scraper for fashion items."""
    
    def __init__(self):
        self.base_url = "https://www.pinterest.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_pinterest(self, keyword: str, max_items: int = 20) -> List[Dict]:
        """
        Search Pinterest for fashion items.
        
        Args:
            keyword: Search keyword (e.g., "vintage streetwear")
            max_items: Maximum number of items to return
            
        Returns:
            List of fashion items with metadata
        """
        print(f"🔍 Searching Pinterest for: {keyword}")
        
        # For hackathon demo, we'll use mock data but structure it like real Pinterest results
        mock_items = self._generate_mock_items(keyword, max_items)
        
        # In a real implementation, you would:
        # 1. Navigate to Pinterest search
        # 2. Parse HTML for pins
        # 3. Extract image URLs, titles, descriptions
        # 4. Handle pagination
        
        return mock_items
    
    def _generate_mock_items(self, keyword: str, count: int) -> List[Dict]:
        """Generate mock Pinterest items for demo purposes."""
        
        # Style categories based on keyword
        style_categories = {
            "vintage": ["vintage", "retro", "classic", "timeless"],
            "streetwear": ["street", "urban", "casual", "cool"],
            "formal": ["elegant", "sophisticated", "professional"],
            "casual": ["relaxed", "comfortable", "everyday"],
            "bohemian": ["boho", "free-spirited", "artistic"],
            "minimalist": ["clean", "simple", "modern"]
        }
        
        # Determine style category
        detected_style = "casual"
        for style, keywords in style_categories.items():
            if any(kw in keyword.lower() for kw in keywords):
                detected_style = style
                break
        
        # Mock item templates
        item_templates = [
            {
                "type": "top",
                "templates": [
                    "Vintage Band T-Shirt", "Oversized Hoodie", "Cropped Sweater", 
                    "Button-Up Shirt", "Graphic Tee", "Blouse"
                ]
            },
            {
                "type": "bottom", 
                "templates": [
                    "High-Waisted Jeans", "Cargo Pants", "Midi Skirt", 
                    "Wide-Leg Trousers", "Shorts", "Pencil Skirt"
                ]
            },
            {
                "type": "outerwear",
                "templates": [
                    "Denim Jacket", "Leather Jacket", "Blazer", 
                    "Cardigan", "Bomber Jacket", "Trench Coat"
                ]
            },
            {
                "type": "shoes",
                "templates": [
                    "Sneakers", "Boots", "Heels", "Sandals", 
                    "Loafers", "Ankle Boots"
                ]
            },
            {
                "type": "accessories",
                "templates": [
                    "Crossbody Bag", "Statement Necklace", "Sunglasses", 
                    "Scarf", "Belt", "Watch"
                ]
            }
        ]
        
        items = []
        for i in range(count):
            # Select random item type
            item_type_data = random.choice(item_templates)
            item_name = random.choice(item_type_data["templates"])
            
            # Generate item data
            item = {
                "id": f"pinterest_{i+1}",
                "title": f"{item_name} - {detected_style.title()} Style",
                "description": f"Perfect {detected_style} {item_name.lower()} for your wardrobe",
                "image_url": f"https://picsum.photos/300/400?random={i+1}",
                "source_url": f"https://pinterest.com/pin/{i+1}",
                "style": detected_style,
                "category": item_type_data["type"],
                "price_range": self._generate_price_range(item_type_data["type"]),
                "colors": random.sample(["black", "white", "navy", "beige", "gray", "brown"], 2),
                "sizes": ["XS", "S", "M", "L", "XL"],
                "brand": random.choice(["Zara", "H&M", "Urban Outfitters", "ASOS", "Forever 21"]),
                "likes": random.randint(10, 1000),
                "saves": random.randint(5, 500),
                "created_at": "2024-01-15T10:30:00Z",
                "tags": [detected_style, item_type_data["type"], keyword.split()[0]]
            }
            items.append(item)
        
        return items
    
    def _generate_price_range(self, category: str) -> str:
        """Generate realistic price range based on category."""
        price_ranges = {
            "top": ["$15-30", "$25-50", "$40-80"],
            "bottom": ["$20-40", "$35-60", "$50-100"],
            "outerwear": ["$40-80", "$60-120", "$100-200"],
            "shoes": ["$30-60", "$50-100", "$80-150"],
            "accessories": ["$10-25", "$20-50", "$40-80"]
        }
        return random.choice(price_ranges.get(category, ["$20-50"]))
    
    def scrape_real_pinterest(self, keyword: str, max_items: int = 20) -> List[Dict]:
        """
        Real Pinterest scraping implementation.
        Note: This is a simplified version for demo purposes.
        """
        try:
            # Construct search URL
            search_url = f"{self.base_url}/search/pins/?q={keyword.replace(' ', '%20')}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find pin elements (this selector may need adjustment)
            pin_elements = soup.find_all('div', {'data-test-id': 'pin'})
            
            items = []
            for i, pin in enumerate(pin_elements[:max_items]):
                try:
                    # Extract pin data
                    img_element = pin.find('img')
                    link_element = pin.find('a')
                    
                    if img_element and link_element:
                        item = {
                            "id": f"pinterest_real_{i+1}",
                            "title": img_element.get('alt', f'{keyword} item {i+1}'),
                            "image_url": img_element.get('src', ''),
                            "source_url": urljoin(self.base_url, link_element.get('href', '')),
                            "style": keyword,
                            "category": "unknown",
                            "created_at": "2024-01-15T10:30:00Z"
                        }
                        items.append(item)
                        
                except Exception as e:
                    print(f"Error parsing pin {i}: {e}")
                    continue
            
            return items
            
        except Exception as e:
            print(f"Error scraping Pinterest: {e}")
            # Fallback to mock data
            return self._generate_mock_items(keyword, max_items)

def scrape_pinterest(keyword: str, max_items: int = 20) -> List[Dict]:
    """
    Main function to scrape Pinterest for fashion items.
    
    Args:
        keyword: Search keyword
        max_items: Maximum number of items to return
        
    Returns:
        List of fashion items
    """
    scraper = PinterestScraper()
    
    # For hackathon demo, use mock data
    # In production, you might want to use: scraper.scrape_real_pinterest(keyword, max_items)
    return scraper.search_pinterest(keyword, max_items)

def filter_items_by_style(items: List[Dict], target_style: str) -> List[Dict]:
    """
    Filter items by style preference.
    
    Args:
        items: List of items to filter
        target_style: Target style to filter by
        
    Returns:
        Filtered list of items
    """
    if not target_style:
        return items
    
    target_style_lower = target_style.lower()
    filtered_items = []
    
    for item in items:
        # Check if item matches target style
        item_style = item.get('style', '').lower()
        item_title = item.get('title', '').lower()
        item_description = item.get('description', '').lower()
        
        if (target_style_lower in item_style or 
            target_style_lower in item_title or 
            target_style_lower in item_description):
            filtered_items.append(item)
    
    return filtered_items

def get_trending_styles() -> List[str]:
    """Get list of trending fashion styles."""
    return [
        "vintage streetwear",
        "minimalist chic", 
        "bohemian",
        "athleisure",
        "cottagecore",
        "dark academia",
        "y2k",
        "normcore"
    ]
