from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import json
import math
from pathlib import Path
from datetime import datetime
from uuid import uuid4

# Helper to perform case-insensitive substring matching
def _matches(value: Optional[str], query: str) -> bool:
    if value is None:
        return False
    return query.lower() in value.lower()

# Initialize FastAPI app
app = FastAPI(
    title="Product API",
    description="REST API for product data with pagination, filtering, search, and sorting",
    version="1.0.0",
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Load products data at startup
PRODUCTS: List[Dict[str, Any]] = []
ORDERS: List[Dict[str, Any]] = []

ORDERS_PATH = Path(__file__).parent / "orders.json"


def _load_orders() -> List[Dict[str, Any]]:
    if not ORDERS_PATH.exists():
        return []
    try:
        with open(ORDERS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("orders", [])
    except (json.JSONDecodeError, OSError):
        return []


def _save_orders() -> None:
    ORDERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ORDERS_PATH, "w", encoding="utf-8") as f:
        json.dump({"orders": ORDERS}, f, ensure_ascii=False, indent=2)

@app.on_event("startup")
async def load_products():
    """Load products from db.json at startup"""
    global PRODUCTS
    db_path = Path(__file__).parent / "db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        PRODUCTS = data.get("products", [])
    print(f"Loaded {len(PRODUCTS)} products from db.json")
    global ORDERS
    ORDERS = _load_orders()
    print(f"Loaded {len(ORDERS)} orders from orders.json")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Product API",
        "version": "1.0.0",
        "endpoints": {
            "products": "/products",
            "documentation": "/docs",
            "redoc": "/redoc"
        },
        "total_products": len(PRODUCTS),
        "total_orders": len(ORDERS),
    }


@app.get("/products")
async def get_products(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    search: Optional[str] = Query(None, description="Search in title, description, tags, and brand"),
    sortBy: Optional[str] = Query(None, description="Field to sort by (e.g., price, rating, title)"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to return"),
    # Dynamic filters
    category: Optional[str] = Query(None, description="Filter by category"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    minPrice: Optional[float] = Query(None, description="Minimum price"),
    maxPrice: Optional[float] = Query(None, description="Maximum price"),
    minRating: Optional[float] = Query(None, description="Minimum rating"),
    availabilityStatus: Optional[str] = Query(None, description="Filter by availability status"),
):
    """
    Get products with support for:
    - Pagination: ?page=1&limit=10
    - Filtering: ?category=Beauty&brand=Essence&minPrice=10&maxPrice=50
    - Search: ?search=mascara
    - Sorting: ?sortBy=price&order=desc
    - Field selection: ?fields=id,title,price,brand
    
    All filters can be combined.
    """
    
    # Start with all products
    filtered_data = PRODUCTS.copy()
    
    # Apply category filter
    if category:
        filtered_data = [
            item for item in filtered_data 
            if _matches(item.get("category"), category)
        ]
    
    # Apply brand filter
    if brand:
        filtered_data = [
            item for item in filtered_data 
            if _matches(item.get("brand"), brand)
        ]
    
    # Apply price range filters
    if minPrice is not None:
        filtered_data = [
            item for item in filtered_data 
            if item.get("price", 0) >= minPrice
        ]
    
    if maxPrice is not None:
        filtered_data = [
            item for item in filtered_data 
            if item.get("price", 0) <= maxPrice
        ]
    
    # Apply rating filter
    if minRating is not None:
        filtered_data = [
            item for item in filtered_data 
            if item.get("rating", 0) >= minRating
        ]
    
    # Apply availability status filter
    if availabilityStatus:
        filtered_data = [
            item for item in filtered_data 
            if _matches(item.get("availabilityStatus"), availabilityStatus)
        ]
    
    # Apply search
    if search:
        search_lower = search.lower()
        filtered_data = [
            item for item in filtered_data
            if (
                search_lower in (item.get("title") or "").lower()
                or search_lower in (item.get("description") or "").lower()
                or search_lower in (item.get("brand") or "").lower()
                or any(search_lower in str(tag).lower() for tag in item.get("tags") or [])
            )
        ]
    
    # Apply sorting
    if sortBy:
        reverse = order.lower() == "desc"
        try:
            # Handle nested fields and missing values
            def get_sort_key(item):
                value = item.get(sortBy)
                # Handle None values - put them at the end
                if value is None:
                    return float('inf') if not reverse else float('-inf')
                # Convert to string for comparison if needed
                if isinstance(value, (int, float)):
                    return value
                return str(value).lower()
            
            filtered_data = sorted(filtered_data, key=get_sort_key, reverse=reverse)
        except (TypeError, KeyError):
            # If sorting fails, just continue without sorting
            pass
    
    # Calculate pagination
    total_items = len(filtered_data)
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 0
    
    # Apply pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_data = filtered_data[start:end]
    
    # Apply field selection
    if fields:
        selected_fields = [f.strip() for f in fields.split(",")]
        paginated_data = [
            {key: value for key, value in item.items() if key in selected_fields}
            for item in paginated_data
        ]
    
    # Return 404 if no products found
    if not paginated_data and page > total_pages and total_pages > 0:
        raise HTTPException(
            status_code=404, 
            detail=f"Page {page} not found. Total pages: {total_pages}"
        )
    
    # Build response
    return {
        "page": page,
        "limit": limit,
        "totalItems": total_items,
        "totalPages": total_pages,
        "data": paginated_data,
    }


@app.get("/products/categories")
async def get_categories():
    """Get all unique categories"""
    categories = list(set(
        product.get("category") 
        for product in PRODUCTS 
        if product.get("category")
    ))
    return {
        "total": len(categories),
        "categories": sorted(categories)
    }


@app.get("/products/brands")
async def get_brands():
    """Get all unique brands"""
    brands = list(set(
        product.get("brand") 
        for product in PRODUCTS 
        if product.get("brand")
    ))
    return {
        "total": len(brands),
        "brands": sorted(brands)
    }


@app.get("/products/{product_id}")
async def get_product_by_id(product_id: str):
    """Get a single product by ID"""
    product = next(
        (item for item in PRODUCTS if item.get("id") == product_id),
        None
    )
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")
    
    return product


class OrderItem(BaseModel):
    productId: str = Field(..., description="Identifier of the product in this order item")
    quantity: int = Field(1, ge=1, description="Quantity of the product")
    price: Optional[float] = Field(default=None, ge=0, description="Optional price for the item")


class OrderCreate(BaseModel):
    userId: str = Field(..., description="Unique identifier for the user placing the order")
    items: List[OrderItem] = Field(default_factory=list, description="Products included in the order")
    totalAmount: Optional[float] = Field(default=None, ge=0, description="Total value of the order")
    status: str = Field(default="pending", description="Current status of the order")
    notes: Optional[str] = Field(default=None, description="Additional notes for the order")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata for the order")


class Order(OrderCreate):
    id: str = Field(..., description="Unique order identifier")
    createdAt: datetime = Field(..., description="Timestamp when the order was created")


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create a new order"""
    new_order = Order(
        id=str(uuid4()),
        createdAt=datetime.utcnow(),
        **order.model_dump()
    )
    ORDERS.append(new_order.model_dump(mode="json"))
    _save_orders()
    return new_order


@app.get("/orders", response_model=List[Order])
async def list_orders():
    """Retrieve all orders"""
    return [Order(**order) for order in ORDERS]


@app.get("/users/{user_id}/orders", response_model=List[Order])
async def get_orders_by_user(user_id: str):
    """Retrieve all orders for a specific user"""
    user_orders = [
        Order(**order)
        for order in ORDERS
        if order.get("userId") == user_id
    ]
    return user_orders

