# Savvy Shopper - Backend API

A comprehensive REST API backend for the Savvy Shopper multi-retailer price comparison platform. This Flask-based service aggregates product data from 12 different South African retailers across three major categories: Groceries, Clothing, and PC Components.

<video src="static/savvy-shopper-demo-1_small1.mp4" controls autoplay loop muted width="640" height="480">
  Your browser does not support the video tag.
</video>

## 🎯 Project Overview

Savvy Shopper is a full-stack price comparison application that empowers consumers to make informed purchasing decisions by tracking product prices across multiple retailers. The backend serves as the central data hub, processing web-scraped data and providing RESTful API endpoints for mobile (Flutter) and Chrome extension clients.

**Key Achievement**: This project played a pivotal role in securing my first data scientist position at Shoprite ZA, demonstrating proficiency in full-stack development, data engineering, and cloud architecture.

## 🏗️ Architecture Overview

```
Web Scrapers (Scrapy/Scrapyd) # run everyday
    ↓
Cloud Databases (DynamoDB/MongoDB/Firebase)
    ↓
ETL pipeline(simple script that downloads, cleans and uploads data)
    ↓
SQLlite database
    ↓
Flask REST API (This Repository)
    ↓                          ↓
Mobile App (Flutter)  +  Chrome Extension
```

## ✨ Features

- **Multi-Retailer Data Aggregation**: Real-time price tracking across 12 major South African retailers
- **Intelligent Price Analysis**: Algorithm-based "good buy" and "bad buy" recommendations using historical price data
- **Historical Price Tracking**: Complete price history for trend analysis
- **Competitor Price Comparison**: Side-by-side price comparisons for similar products
- **Shopping List Feature**: Multi-store price comparison for grocery lists
- **RESTful API**: Clean, documented API endpoints with Swagger UI
- **Cross-Platform Support**: Serves both mobile (iOS/Android) and web (Chrome extension) clients

## 🛍️ Supported Retailers

### Groceries (3 Stores)

- **Pick n Pay (PnP)** - `/pnp-client`, `/pnp-admin`
- **Shoprite** - `/client`, `/admin`
- **Woolworths Groceries** - `/woolies-client`, `/woolies-admin`

### Clothing (6 Stores)

- **Foschini** - `/foschini-client`, `/foschini-admin`
- **Markham** - `/markham-client`, `/markham-admin`
- **MRP** - `/mrp-client`, `/mrp-admin`
- **Sportscene** - `/sportscene-client`, `/sportscene-admin`
- **Superbalist** - `/superbalist-client`, `/superbalist-admin`
- **Woolworths Clothing** - `/woolworths-clothing-client`, `/woolworths-clothing-admin`

### PC Components & Electronics (5 Stores)

- **Computermania** - `/computermania-client`, `/computermania-admin`
- **Game** - `/game-client`, `/game-admin`
- **HiFi Corp** - `/hifi-client`, `/hifi-admin`
- **Makro** - `/makro-client`, `/makro-admin`
- **Takealot** - `/takealot-client`, `/takealot-admin`

## 🛠️ Tech Stack

### Backend Framework

- **Python 3.9.7**
- **Flask 2.1.0** - Web framework
- **Flask-RESTX 1.3.2** - REST API with Swagger documentation
- **Flask-SQLAlchemy 2.5.1** - ORM and database management
- **Flask-CORS 3.0.10** - Cross-origin resource sharing
- **Gunicorn 20.0.4** - Production WSGI server

### Databases

#### **local db**

Useed to store data locally, used to serve the mobile app.

- **SQLite** - Local product data storage

#### **cloud**

The scrappers write to these db. I used 3 databases here, as l did not have the funds to
buy the storage, so l had to stay within each service providers free tier.
This also gave me a chance to explore different database service providers.

- **MongoDB 3.11.1** - Cloud-based NoSQL storage (Shoprite data)
- **DynamoDB (via boto3)** - AWS managed NoSQL database
- **Firebase Realtime DB** - Real-time data synchronization

### Data Processing

- **Pandas 1.1.4** - Data manipulation and analysis
- **NumPy 1.21.6** - Numerical computations
- **SciPy 1.7.1** - Scientific computing
- **Seaborn 0.11.2** - Data visualization during developemt

### Cloud Services

- **AWS (boto3 1.18.56)** - DynamoDB, Lambda scheduling
- **Google Cloud Platform** - Firebase, Cloud Storage, Firestore
- **Heroku** - Web scraper hosting

### Additional Tools

- **Requests 2.28.1** - HTTP library
- **Python-dotenv 0.17.1** - Environment configuration

## 📁 Project Structure

```
nothing_to_see_here/
├── app.py                          # Application entry point
├── update_db.py                    # Database update script
├── requirements.txt                # Python dependencies
├── config/
│   └── config.py                   # Configuration settings
├── keys/                           # API keys and credentials
│   ├── e-clothing.json
│   ├── e-grocery.json
│   └── pc-components.json
├── website/                        # Main application package
│   ├── __init__.py                 # Flask app initialization & routing
│   ├── data.sqlite                 # SQLite database
│   ├── grocery/                    # Grocery store modules
│   │   ├── pnp/
│   │   │   ├── pnp_api.py         # API endpoints
│   │   │   ├── pnp_models.py      # Database models
│   │   │   └── db_helper_pnp.py   # Database operations
│   │   ├── shoprite/
│   │   └── woolies/
│   ├── clothing/                   # Clothing store modules
│   │   ├── foschini/
│   │   ├── markham/
│   │   ├── mrp/
│   │   ├── sportscene/
│   │   ├── superbalist/
│   │   └── woolworths_clothing/
│   ├── pc/                         # PC components store modules
│   │   ├── computermania/
│   │   ├── game/
│   │   ├── hifi/
│   │   ├── makro/
│   │   └── takealot/
│   └── dummy_objects/              # Helper utilities
│       ├── firebase_helper.py
│       ├── dynamo_db_helper.py
│       └── product_change_value.py
├── updates_logs/                   # Database update logs
│   ├── errors.txt
│   ├── successful.txt
│   ├── failed_to_update.txt
│   └── response_to_update.txt
└── installation_files/
    ├── Procfile                    # Heroku deployment config
    └── requirements.txt            # python dependencies
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nothing_to_see_here
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory with your credentials:

```env
# Database configurations
MONGODB_URI=your_mongodb_connection_string
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region

# Firebase configuration
FIREBASE_CREDENTIALS_PATH=keys/e-grocery.json

# Flask configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

### 5. Initialize Database

```bash
python
>>> from website import db
>>> db.create_all()
>>> exit()
```

## 💻 Usage

### Running the Development Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Running in Production

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

### Accessing API Documentation

Navigate to: `http://localhost:5000/docs`

This provides interactive Swagger UI documentation for all API endpoints.

## 🔄 Updating the Database

The `update_db.py` script fetches fresh product data from web scrapers and updates the SQLite database.

### Configuration

Edit `update_db.py` to select which stores to update:

```python
stores = [
    PnPAdmin,           # Pick n Pay
    ShopriteAdmin,      # Shoprite
    WooliesAdmin,       # Woolworths Groceries

    ComputermaniaAdmin, # Computermania
    GameAdmin,          # Game
    HifiAdmin,          # HiFi Corp
    MakroAdmin,         # Makro
    TakealotAdmin,      # Takealot

    MarkhamAdmin,       # Markham
    MrpAdmin,           # MRP
    SportsceneAdmin,    # Sportscene
    WoolworthsClothingAdmin,  # Woolworths Clothing
    FoschiniAdmin,      # Foschini
    SuperbalistAdmin,   # Superbalist
]
```

### Running the Update Script

```bash
python update_db.py
```

### Update Logs

Monitor the update process through log files in `updates_logs/`:

- **successful.txt** - Successfully updated stores with timestamps
- **failed_to_update.txt** - Stores that failed to update
- **errors.txt** - Detailed error messages and stack traces
- **response_to_update.txt** - API response summaries

### Retry Logic

The script automatically retries failed updates up to 3 times before marking a store as failed.

## 📡 API Endpoints

### Client Endpoints (GET)

Retrieve product data for end-users:

**Groceries:**

- `GET /client` - Shoprite products
- `GET /pnp-client` - Pick n Pay products
- `GET /woolies-client` - Woolworths products

**Clothing:**

- `GET /foschini-client` - Foschini products
- `GET /markham-client` - Markham products
- `GET /mrp-client` - MRP products
- `GET /sportscene-client` - Sportscene products
- `GET /superbalist-client` - Superbalist products
- `GET /woolworths-clothing-client` - Woolworths Clothing products

**PC Components:**

- `GET /computermania-client` - Computermania products
- `GET /game-client` - Game products
- `GET /hifi-client` - HiFi Corp products
- `GET /makro-client` - Makro products
- `GET /takealot-client` - Takealot products

### Admin Endpoints (GET/POST)

Manage and update product databases:

- `GET/POST /admin` - Shoprite admin
- `GET/POST /pnp-admin` - Pick n Pay admin
- `GET/POST /woolies-admin` - Woolworths admin
- _(Similar pattern for all stores)_

### Product Search Endpoints

Search for specific products by title:

- `GET /get-product-data/<string:title>` - Shoprite
- `GET /pnp-get-product-data/<string:title>` - Pick n Pay
- `GET /woolies-get-product-data/<string:title>` - Woolworths
- `GET /computermania-get-product-data/<string:title>` - Computermania
- `GET /hifi-get-product-data/<string:title>` - HiFi Corp
- `GET /takealot-get-product-data/<string:title>` - Takealot
- `GET /game-get-product-data/<string:title>` - Game
- `GET /makro-get-product-data/<string:title>` - Makro
- `GET /foschini-get-product-data/<string:title>` - Foschini
- `GET /markham-get-product-data/<string:title>` - Markham
- `GET /sportscene-get-product-data/<string:title>` - Sportscene
- `GET /woolworths-clothing-get-product-data/<string:title>` - Woolworths Clothing
- `GET /superbalist-get-product-data/<string:title>` - Superbalist
- `GET /mrp-get-product-data/<string:title>` - MRP

### Home Endpoint

- `GET /` - Welcome message

## 🗄️ Database Architecture

### SQLite (Primary Storage)

- **Location**: `website/data.sqlite`
- **Purpose**: Local storage for all product data
- **Models**: Separate tables for each retailer

### MongoDB

- **Purpose**: Shoprite data storage
- **Connection**: Via PyMongo client

### DynamoDB

- **Stores**: Makro, MRP, Game
- **Connection**: Via boto3 AWS SDK

### Firebase Realtime Database

- **Stores**: HiFi Corp, Takealot, Computermania, Clothing stores
- **Connection**: Via firebase-admin SDK

## 🔐 Security & Configuration

- API keys and credentials stored in `keys/` directory (not committed to version control)
- Environment variables managed via `.env` file
- CORS enabled for cross-origin requests
- Firebase service account authentication

## 📊 Data Flow

1. **Web Scrapers** (Scrapy/Scrapyd on Heroku) scrape retailer websites
2. **AWS Lambda** triggers scheduled scraping jobs
3. **Scraped Data** stored in MongoDB/DynamoDB/Firebase
4. **update_db.py** fetches data and syncs to SQLite
5. **Flask API** serves data to clients via REST endpoints
6. **Mobile App & Chrome Extension** consume API data

## 🧪 Testing

API endpoints can be tested using:

- **Swagger UI**: `http://localhost:5000/docs`
- **Postman Collection**: `savvy-shopper.postman_collection.json`
- **cURL**: Manual endpoint testing

Example:

```bash
curl http://localhost:5000/pnp-client
curl http://localhost:5000/pnp-get-product-data/milk
```

## 📝 Logging

The application maintains comprehensive logs:

- **api_logs.log** - General API request/response logs
- **updates_logs/** - Database update operation logs

## 🚢 Deployment

### Heroku Deployment

The `installation_files/Procfile` contains Heroku deployment configuration:

```
web: gunicorn app:app
```

Deploy to Heroku:

```bash
git push heroku main
```

## 🤝 Contributing

This is a portfolio project. For collaboration inquiries, please reach out directly.

## 📄 License

All rights reserved. This project is for portfolio demonstration purposes.

## 👨‍💻 Developer

Developed as a solo full-stack project, encompassing:

- Web scraping architecture (Python/Scrapy)
- Backend API development (Flask/Python)
- Database design and management (SQLite/MongoDB/DynamoDB/Firebase)
- Mobile application (Flutter)
- Browser extension (JavaScript/HTML/CSS)
- Cloud infrastructure (AWS/GCP/Heroku)
- Data science and analytics (Pandas/NumPy)

## 🎓 Impact

This project was instrumental in launching my career as a data scientist at Shoprite ZA, demonstrating:

- Full-stack development capabilities
- Cloud architecture proficiency
- Data engineering skills
- Problem-solving and independent project management
- Cross-platform development expertise

## 📞 Contact

For inquiries about this project or collaboration opportunities, please reach out through GitHub.

---

**Built with ❤️ by Taku**

Flask + Python + AWS + Firebase | 2020
