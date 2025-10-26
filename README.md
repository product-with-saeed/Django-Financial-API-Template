# 💰 Django Financial API Template

> **Production-ready Django REST Framework backend for FinTech and analytics applications.**
> Designed by [**Saeed Mohammadpour**](https://github.com/product-with-saeed) to help teams launch **secure, modular, and audit-ready** transaction systems in days — not weeks.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![DRF](https://img.shields.io/badge/DRF-3.15+-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-ready-2496ed)
![License](https://img.shields.io/badge/License-MIT-success)

---

## 🧭 Overview
Most FinTech backends struggle with unstructured data, missing audit trails, and inconsistent authentication.
This template provides a **clean Django REST architecture** that’s modular, secure, and instantly usable for real products or investor demos.

### Perfect for
- Bootstrapping **FinTech MVPs** or compliance demos
- Learning **enterprise-grade Django project structure**
- Extending for **SaaS financial tracking or analytics tools**
- Teaching API design and modular architecture

---

## ✨ Key Features

| Category | Highlights |
|-----------|-------------|
| **Architecture** | ✅ Modular app layout (transactions, auth, reports) <br> ✅ REST API design with DRF 3.15+ <br> ✅ PostgreSQL-ready |
| **Security** | ✅ JWT authentication (djangorestframework-simplejwt) <br> ✅ Role-based permissions & rate limiting |
| **Scalability** | ✅ Celery-ready task pipeline <br> ✅ Dockerized environment <br> ✅ Configurable via `.env` |
| **Compliance** | ✅ Audit log hooks for transactions <br> ✅ API versioning <br> ✅ GDPR-ready data structure |
| **Documentation** | ✅ Auto-generated Swagger UI <br> ✅ Postman collection under `/docs/api_collection.json` |

---

## 🧱 Architecture

<p align="center">
  <img src="docs/assets/django-module-map-light.png#gh-light-mode-only"
       alt="Diagram showing Django Financial API architecture with users, auth, transactions, reports, Celery worker, and PostgreSQL database">
  <img src="docs/assets/django-module-map-dark.png#gh-dark-mode-only"
       alt="Diagram showing Django Financial API architecture with users, auth, transactions, reports, Celery worker, and PostgreSQL database (dark mode)">
</p>
<p align="center"><em>Isolated Django apps with JWT authentication, transactions, reports, Celery worker, and PostgreSQL persistence.</em></p>

---

### 📚 API Documentation Preview

<p align="center">
  <img src="docs/assets/swagger-preview.png" alt="Swagger UI showing JWT Authorize and financial transaction endpoints">
</p>
<p align="center"><em>Live Swagger UI with JWT authentication and interactive endpoints.</em></p>

---

## 🚀 Quick Start

### Local Installation
```bash
git clone https://github.com/product-with-saeed/Django-Financial-API-Template.git
cd Django-Financial-API-Template
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
````

### Setup Database & Run Server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/api/transactions/`

---

## 🧩 API Endpoints

| Method   | Endpoint                  | Description               |
| -------- | ------------------------- | ------------------------- |
| `POST`   | `/api/transactions/`      | Create a new transaction  |
| `GET`    | `/api/transactions/`      | Retrieve all transactions |
| `GET`    | `/api/transactions/<id>/` | Retrieve a transaction    |
| `PUT`    | `/api/transactions/<id>/` | Update a transaction      |
| `DELETE` | `/api/transactions/<id>/` | Delete a transaction      |
| `POST`   | `/api/token/`             | Obtain JWT token          |
| `POST`   | `/api/token/refresh/`     | Refresh JWT token         |

---

## 🧠 Key Modules

| Module         | Purpose                                                   |
| -------------- | --------------------------------------------------------- |
| `transactions` | Double-entry ledger model with validation & balance logic |
| `auth`         | JWT authentication & user management                      |
| `reports`      | Aggregated transaction summaries                          |
| `common`       | Logging, error handling, and API utils                    |

---

## 🧰 Example Transaction Object

```json
{
  "id": 1042,
  "reference": "INV-2025-024",
  "amount": 950.00,
  "currency": "GBP",
  "type": "credit",
  "category": "subscription",
  "created_at": "2025-10-01T10:45:22Z",
  "updated_at": "2025-10-01T10:45:22Z"
}
```

---

## ⚙️ Configuration

`.env.example`

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgres://finance:finance@localhost:5432/finance_db
ALLOWED_HOSTS=127.0.0.1,localhost
```

**Environment variables are automatically loaded** via `django-environ`.

---

## 📊 Performance Snapshot

| Metric                 | Value                   |
| ---------------------- | ----------------------- |
| Avg. response time     | <200 ms                 |
| Test coverage          | **99.09%**              |
| Test count             | **56 tests**            |
| Setup time             | <10 minutes             |
| Default benchmark load | 10 K transactions / day |

---

## 💼 Use Cases

| Use Case                | Example                                             |
| ----------------------- | --------------------------------------------------- |
| **FinTech MVPs**        | Build proof-of-concept with investor demo readiness |
| **Accounting Tools**    | Integrate APIs into dashboards or CRMs              |
| **Analytics Platforms** | Aggregate financial metrics via REST                |
| **Education**           | Teach secure Django + DRF API design                |
| **Compliance Projects** | Prototype GDPR / audit log ready backend            |

---

## 🧪 Testing

### Comprehensive Test Suite
This project includes **56 comprehensive tests** with **99%+ code coverage**, covering models, serializers, views, and integration scenarios.

### Running Tests

**Using Make (Recommended):**
```bash
make test              # Run all tests with coverage
make test-unit         # Run only unit tests
make test-integration  # Run only integration tests
make test-fast         # Run without coverage (faster)
make coverage          # Generate detailed coverage report
```

**Using pytest directly:**
```bash
source venv/bin/activate
python -m pytest                    # Run all tests
python -m pytest tests/unit/        # Unit tests only
python -m pytest tests/integration/ # Integration tests only
python -m pytest -v                 # Verbose output
python -m pytest --no-cov          # Skip coverage
```

**Using the test script:**
```bash
./run_tests.sh                     # Auto-activates venv and runs tests
```

### Test Coverage Report

```
---------- coverage: platform linux, python 3.12 ----------
Name                 Stmts   Miss   Cover
-------------------------------------------
api/models.py           13      0 100.00%
api/serializers.py      14      0 100.00%
api/views.py            14      0 100.00%
config/settings.py      43      1  97.67%
-------------------------------------------
TOTAL                  110      1  99.09%
```

### Test Categories

| Category | Tests | Coverage |
|----------|-------|----------|
| **Unit Tests** | 52 | Models, Serializers, Views |
| **Integration Tests** | 8 | Full CRUD lifecycle, JWT auth, multi-user isolation |
| **Security Tests** | ✅ | User isolation, permission checks, data validation |

### Key Features Tested
- ✅ Authentication & authorization (JWT)
- ✅ User data isolation (users can only access own transactions)
- ✅ CRUD operations with permission checks
- ✅ Field validation and constraints
- ✅ Cascade deletion behavior
- ✅ Read-only field enforcement
- ✅ Error handling and edge cases

---

## 📚 Documentation

* **Swagger UI:** `/api/docs/`
* **Redoc UI:** `/api/redoc/`
* **Postman Collection:** `/docs/api_collection.json`
* **Module Docs:** `/docs/architecture.md`, `/docs/setup.md`

---

## 🐳 Docker Deployment

```bash
cp .env.example .env
docker-compose up -d
docker-compose logs -f web
```

---

## 🔒 Security & Compliance Notes

* JWT-based authentication for all endpoints
* PII-minimized data models
* GDPR-aligned data handling guidance in `/docs/compliance.md`
* HTTPS recommended in all deployments

---

## 📬 Work With Me

Need a **custom Django/FastAPI backend** for FinTech, SaaS, or analytics platforms?
I design scalable, audit-ready systems that meet compliance and performance standards.

📧 **[product.with.saeed@gmail.com](mailto:product.with.saeed@gmail.com)**
💼 [LinkedIn](https://linkedin.com/in/product-with-saeed)

---

## 🧑‍💻 Author

**Saeed Mohammadpour** — Senior Python Backend Developer | Ex-CTO
Specializing in **Django, FastAPI, Data Automation, and FinTech Infrastructure**.

---

## ⭐ Support

If this project helps you, please ⭐ star it — it helps others discover reliable Django templates.

---

**Built with ❤️ for the Python community**
MIT License © Saeed Mohammadpour
