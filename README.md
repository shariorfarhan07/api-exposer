# Product API Documentation

A high-performance REST API built with FastAPI for serving product data with advanced filtering, pagination, search, and sorting capabilities.

## Features

- **Pagination**: Navigate through large datasets efficiently
- **Advanced Filtering**: Filter by category, brand, price range, rating, and availability
- **Full-text Search**: Search across title, description, brand, and tags
- **Flexible Sorting**: Sort by any field in ascending or descending order
- **Field Selection**: Choose which fields to return in the response
- **CORS Enabled**: Ready for frontend integration
- **Auto-generated Documentation**: Interactive API docs at `/docs`
- **Order Capture**: Create and retrieve user orders with persistent storage

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Verify data file**:
Ensure `db.json` exists in the project root with your product data.

## Running the Server

### Development Mode
```bash
uvicorn main:app --reload
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://127.0.0.1:8000`

### Docker Compose
```bash
docker compose up --build
```

This builds the image and runs it with the API exposed at `http://127.0.0.1:4000`.

## Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Root Endpoint
```
GET /
```
Returns API information and available endpoints.

**Example Response**:
```json
{
  "message": "Product API",
  "version": "1.0.0",
  "endpoints": {
    "products": "/products",
    "documentation": "/docs",
    "redoc": "/redoc"
  },
  "total_products": 1000
}
```

---

### Get All Products
```
GET /products
```

Returns paginated product list with optional filtering, searching, and sorting.

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (starts at 1) |
| `limit` | integer | 10 | Items per page (max 100) |
| `search` | string | - | Search term (searches title, description, brand, tags) |
| `sortBy` | string | - | Field name to sort by |
| `order` | string | asc | Sort order: `asc` or `desc` |
| `fields` | string | - | Comma-separated field names to return |
| `category` | string | - | Filter by exact category name |
| `brand` | string | - | Filter by exact brand name |
| `minPrice` | float | - | Minimum price filter |
| `maxPrice` | float | - | Maximum price filter |
| `minRating` | float | - | Minimum rating filter |
| `availabilityStatus` | string | - | Filter by availability status |

#### Response Format
```json
{
  "page": 1,
  "limit": 10,
  "totalItems": 1000,
  "totalPages": 100,
  "data": [...]
}
```

---

### Get Product by ID
```
GET /products/{product_id}
```
---

### Create Order
```
POST /orders
```

Create an order for a specific user.

**Request Body**
```json
{
  "userId": "user-123",
  "items": [
    {
      "productId": "173530386",
      "quantity": 2,
      "price": 22.9
    }
  ],
  "totalAmount": 45.8,
  "status": "pending",
  "notes": "Deliver between 9 AM - 12 PM",
  "metadata": {
    "paymentMethod": "bkash"
  }
}
```

**Success Response (201)**
```json
{
  "userId": "user-123",
  "items": [
    {
      "productId": "173530386",
      "quantity": 2,
      "price": 22.9
    }
  ],
  "totalAmount": 45.8,
  "status": "pending",
  "notes": "Deliver between 9 AM - 12 PM",
  "metadata": {
    "paymentMethod": "bkash"
  },
  "id": "8f1c31ab-1e50-4fe1-b3f3-f118c63c3d2d",
  "createdAt": "2025-11-12T07:45:00.123456"
}
```

---

### Get Orders for a User
```
GET /users/{userId}/orders
```

Retrieve all orders for a given user. Returns an empty list if no orders are found.

**Example**
```bash
curl "http://127.0.0.1:8002/users/user-123/orders"
```

---

### Get All Orders
```
GET /orders
```

Returns every order currently stored by the API.

---

Returns a single product by its ID.

**Example**:
```bash
GET /products/173530386
```

---

### Get All Categories
```
GET /products/categories
```

Returns all unique product categories.

**Example Response**:
```json
{
  "total": 45,
  "categories": ["Beauty", "Electronics", "Clothing", ...]
}
```

---

### Get All Brands
```
GET /products/brands
```

Returns all unique product brands.

**Example Response**:
```json
{
  "total": 120,
  "brands": ["Apple", "Samsung", "Nike", ...]
}
```

---

## Usage Examples

### Basic Pagination
```bash
# Get first page with 10 items (default)
curl "http://127.0.0.1:8000/products"

# Get second page with 20 items
curl "http://127.0.0.1:8000/products?page=2&limit=20"

# Get page 5 with 50 items per page
curl "http://127.0.0.1:8000/products?page=5&limit=50"
```

### Filtering

```bash
# Filter by category
curl "http://127.0.0.1:8000/products?category=Beauty"

# Filter by brand
curl "http://127.0.0.1:8000/products?brand=Laura%20Mercier"

# Filter by price range
curl "http://127.0.0.1:8000/products?minPrice=10&maxPrice=50"

# Filter by minimum rating
curl "http://127.0.0.1:8000/products?minRating=4.5"

# Filter by availability
curl "http://127.0.0.1:8000/products?availabilityStatus=In%20Stock"

# Combine multiple filters
curl "http://127.0.0.1:8000/products?category=Beauty&minPrice=20&maxPrice=100&minRating=4"
```

### Searching

```bash
# Search for "mascara" in title, description, brand, and tags
curl "http://127.0.0.1:8000/products?search=mascara"

# Search with filters
curl "http://127.0.0.1:8000/products?search=lipstick&category=Beauty&minRating=4"

# Search and paginate
curl "http://127.0.0.1:8000/products?search=phone&page=1&limit=5"
```

### Sorting

```bash
# Sort by price (ascending)
curl "http://127.0.0.1:8000/products?sortBy=price&order=asc"

# Sort by price (descending)
curl "http://127.0.0.1:8000/products?sortBy=price&order=desc"

# Sort by rating (highest first)
curl "http://127.0.0.1:8000/products?sortBy=rating&order=desc"

# Sort by title alphabetically
curl "http://127.0.0.1:8000/products?sortBy=title&order=asc"

# Sort with filters
curl "http://127.0.0.1:8000/products?category=Electronics&sortBy=price&order=asc"
```

### Field Selection

```bash
# Return only id, title, and price
curl "http://127.0.0.1:8000/products?fields=id,title,price"

# Return only essential fields
curl "http://127.0.0.1:8000/products?fields=id,title,price,brand,rating"

# Field selection with filtering
curl "http://127.0.0.1:8000/products?category=Beauty&fields=id,title,price,brand"
```

### Complex Queries

```bash
# Search for "wireless" products in Electronics, 
# price between $50-$200, rating above 4,
# sorted by price descending, showing only key fields
curl "http://127.0.0.1:8000/products?search=wireless&category=Electronics&minPrice=50&maxPrice=200&minRating=4&sortBy=price&order=desc&fields=id,title,price,rating,brand"

# Get affordable Beauty products with good ratings
curl "http://127.0.0.1:8000/products?category=Beauty&maxPrice=30&minRating=4.5&sortBy=rating&order=desc&page=1&limit=10"

# Search and filter clothing items
curl "http://127.0.0.1:8000/products?search=shirt&category=Clothing&availabilityStatus=In%20Stock&sortBy=price&order=asc"
```

### Getting Product Details

```bash
# Get specific product by ID
curl "http://127.0.0.1:8000/products/173530386"

# Get all categories
curl "http://127.0.0.1:8000/products/categories"

# Get all brands
curl "http://127.0.0.1:8000/products/brands"
```

## Example Responses

### Successful Product List Response
```json
{
  "page": 1,
  "limit": 2,
  "totalItems": 1000,
  "totalPages": 500,
  "data": [
    {
      "id": "173530386",
      "title": "Laura Mercier Caviar Stick Eye Color Sugar Frost",
      "description": "Caviar Stick Eye Shadow glides seamlessly onto lids...",
      "category": "Eye Shadow Stick",
      "price": 22.9,
      "discountPercentage": 0.0,
      "rating": 4.0,
      "stock": 6,
      "tags": ["Reviewers highlighted: ease of use, blending, glide"],
      "brand": "Laura Mercier",
      "sku": "173530386",
      "weight": 0,
      "dimensions": {
        "width": 0.2,
        "height": 5.1,
        "depth": 0.2
      },
      "warrantyInformation": "Not specified",
      "shippingInformation": "Delivery available",
      "availabilityStatus": "In Stock",
      "reviews": [...],
      "returnPolicy": "Free 90-day returns",
      "minimumOrderQuantity": 1,
      "meta": {...},
      "images": [...],
      "thumbnail": "https://..."
    }
  ]
}
```

### Error Response (404)
```json
{
  "detail": "Page 200 not found. Total pages: 100"
}
```

### Single Product Response
```json
{
  "id": "173530386",
  "title": "Laura Mercier Caviar Stick Eye Color Sugar Frost",
  "description": "...",
  "category": "Eye Shadow Stick",
  "price": 22.9,
  "rating": 4.0,
  ...
}
```

## Performance Tips

1. **Use Field Selection**: Request only the fields you need to reduce payload size
   ```
   ?fields=id,title,price,brand
   ```

2. **Optimize Page Size**: Use appropriate `limit` values (10-50 for most cases)
   ```
   ?page=1&limit=20
   ```

3. **Combine Filters**: Apply filters before sorting to reduce processing time
   ```
   ?category=Beauty&minRating=4&sortBy=price
   ```

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 404 | Resource not found (invalid page or product ID) |
| 422 | Validation error (invalid query parameters) |

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: Lightning-fast ASGI server
- **Pydantic**: Data validation using Python type annotations
- **Python 3.8+**: Core programming language

## CORS Configuration

CORS is enabled for all origins, allowing the API to be accessed from any frontend application. This is suitable for development and can be restricted in production.

## License

This API is provided as-is for product data exposure and management.

## Support

For issues or questions:
1. Check the interactive documentation at `/docs`
2. Review the examples in this README
3. Verify your query parameters match the expected format

---

**API Version**: 1.0.0  
**Last Updated**: 2024

