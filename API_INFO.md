# 🚀 Product API - Now Running!

## ✅ Server Status
**STATUS:** ✅ RUNNING  
**URL:** http://127.0.0.1:8002  
**Process ID:** 793917  
**Total Products:** 1000

---

## 📍 Quick Access URLs

### Interactive Documentation
- **Swagger UI:** http://127.0.0.1:8002/docs
- **ReDoc:** http://127.0.0.1:8002/redoc
- **Root Info:** http://127.0.0.1:8002/

### Main Endpoints
- **All Products:** http://127.0.0.1:8002/products
- **Get Categories:** http://127.0.0.1:8002/products/categories
- **Get Brands:** http://127.0.0.1:8002/products/brands
- **Product by ID:** http://127.0.0.1:8002/products/{product_id}
- **Create Order (POST):** http://127.0.0.1:8002/orders
- **List Orders:** http://127.0.0.1:8002/orders
- **Orders by User:** http://127.0.0.1:8002/users/{userId}/orders

---

## 🎯 Quick Test Examples

### Basic Queries
```bash
# Get first page (10 items)
curl "http://127.0.0.1:8002/products"

# Get 20 items
curl "http://127.0.0.1:8002/products?limit=20"

# Get page 2
curl "http://127.0.0.1:8002/products?page=2&limit=10"
```

### Search
```bash
# Search for "mascara"
curl "http://127.0.0.1:8002/products?search=mascara"

# Search for "lipstick"
curl "http://127.0.0.1:8002/products?search=lipstick"
```

### Filtering
```bash
# Filter by category
curl "http://127.0.0.1:8002/products?category=Beauty"

# Filter by brand
curl "http://127.0.0.1:8002/products?brand=Essence"

# Price range
curl "http://127.0.0.1:8002/products?minPrice=10&maxPrice=50"

# Minimum rating
curl "http://127.0.0.1:8002/products?minRating=4.5"

# Combine filters
curl "http://127.0.0.1:8002/products?category=Beauty&minPrice=20&maxPrice=100"
```

### Sorting
```bash
# Sort by price (ascending)
curl "http://127.0.0.1:8002/products?sortBy=price&order=asc"

# Sort by rating (descending - highest first)
curl "http://127.0.0.1:8002/products?sortBy=rating&order=desc"

# Sort by title
curl "http://127.0.0.1:8002/products?sortBy=title&order=asc"
```

### Field Selection
```bash
# Get only specific fields
curl "http://127.0.0.1:8002/products?fields=id,title,price,brand"

# Essential fields only
curl "http://127.0.0.1:8002/products?fields=id,title,price,rating"
```

### Complex Queries
```bash
# Search + Filter + Sort + Field Selection
curl "http://127.0.0.1:8002/products?search=lipstick&category=Beauty&sortBy=rating&order=desc&fields=id,title,price,rating&limit=5"

# Price range with rating filter
curl "http://127.0.0.1:8002/products?minPrice=10&maxPrice=30&minRating=4&sortBy=price&order=asc"
```

### Specific Product
```bash
# Get product by ID
curl "http://127.0.0.1:8002/products/173530386"

# Create an order (POST)
curl -X POST "http://127.0.0.1:8002/orders" \
  -H "Content-Type: application/json" \
  -d '{
        "userId": "user-123",
        "items": [
          {"productId": "173530386", "quantity": 2, "price": 22.9}
        ],
        "totalAmount": 45.8,
        "status": "pending",
        "metadata": {"paymentMethod": "bkash"}
      }'

# Fetch orders for a user
curl "http://127.0.0.1:8002/users/user-123/orders"

# List all orders
curl "http://127.0.0.1:8002/orders"
```

### Helper Endpoints
```bash
# Get all categories (452 total)
curl "http://127.0.0.1:8002/products/categories"

# Get all brands
curl "http://127.0.0.1:8002/products/brands"
```

---

## 🛑 Server Management

### Check Server Status
```bash
# Check if server is running
lsof -i :8002

# View server logs
tail -f /home/farhan.exabyting_bKash.com/Music/API\ Exposer/server.log
```

### Stop Server
```bash
# Find and kill the process
pkill -f "uvicorn main:app"

# Or kill by PID
kill 793917
```

### Restart Server
```bash
cd '/home/farhan.exabyting_bKash.com/Music/API Exposer'
python3 -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload
```

---

## 📊 API Response Format

All product queries return:
```json
{
  "page": 1,
  "limit": 10,
  "totalItems": 1000,
  "totalPages": 100,
  "data": [
    {
      "id": "...",
      "title": "...",
      "description": "...",
      "category": "...",
      "price": 0.0,
      "discountPercentage": 0.0,
      "rating": 0.0,
      "stock": 0,
      "tags": [],
      "brand": "...",
      "sku": "...",
      "weight": 0,
      "dimensions": {...},
      "warrantyInformation": "...",
      "shippingInformation": "...",
      "availabilityStatus": "...",
      "reviews": [...],
      "returnPolicy": "...",
      "minimumOrderQuantity": 1,
      "meta": {...},
      "images": [...],
      "thumbnail": "..."
    }
  ]
}
```

---

## 📚 Full Documentation

For complete documentation with detailed examples, see:
- [README.md](README.md)
- Interactive Swagger Docs: http://127.0.0.1:8002/docs

---

## 🎉 Features

✅ Pagination (page & limit)  
✅ Full-text search  
✅ Multi-field filtering  
✅ Flexible sorting  
✅ Field selection  
✅ CORS enabled  
✅ Auto-reload on code changes  
✅ 1000 products loaded  
✅ 452 unique categories  
✅ Interactive API documentation  

---

**Server Log:** `/home/farhan.exabyting_bKash.com/Music/API Exposer/server.log`  
**Last Updated:** November 12, 2025

