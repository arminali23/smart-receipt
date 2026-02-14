## Smart Receipt AI

AI-powered mobile receipt scanner that extracts product data using OCR, categorizes items with Machine Learning, and provides spending analytics through a clean dashboard.

Built with:
	•	Backend: FastAPI, SQLite, Tesseract OCR, scikit-learn
	•	Frontend: Flutter
	•	ML: Naive Bayes product categorizer

Overview

Smart Receipt AI allows users to:
	•	Scan physical receipts via camera or gallery
	•	Automatically extract product names, quantities, and prices
	•	Categorize products using a trained ML model
	•	Analyze spending via daily, monthly, and category-based dashboards

The system combines OCR, rule-based parsing, and lightweight machine learning to provide structured financial insights from unstructured receipt images.


Backend Responsibilities
	•	Image → OCR text extraction (Tesseract)
	•	Regex-based receipt line parsing
	•	Product categorization (Naive Bayes)
	•	SQLite async database storage
	•	Dashboard aggregation APIs

Frontend Responsibilities
	•	Image capture (camera/gallery)
	•	Upload to backend
	•	Receipt list & detail view
	•	Spending dashboard with charts
	•	Category visualization with badges

## Features

Receipt Scanning
	•	Camera or gallery image selection
	•	OCR text extraction
	•	Automatic line detection (product, quantity, unit price, total)
	•	ML-based product category assignment

Machine Learning Categorization

Uses scikit-learn Naive Bayes trained on product names.

Supported categories:
	•	Food & Groceries
	•	Beverages
	•	Household
	•	Snacks
	•	Health & Beauty
	•	Other

Lightweight and fast (< 5 seconds full processing pipeline).

Dashboard Analytics
	•	Daily spending (last 30 days)
	•	Monthly spending (last 12 months)
	•	Category-based pie distribution
	•	Color-coded category insights

⸻

Tech Stack

Backend
	•	FastAPI
	•	SQLAlchemy (async)
	•	SQLite
	•	Tesseract OCR
	•	scikit-learn
	•	Uvicorn

Frontend
	•	Flutter
	•	fl_chart
	•	image_picker

## Running the App
Backend requires Tesseract OCR installed: 
``` brew install tesseract ``` 

``` 
cd backend
source ../.venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
``` 
Frontend (requires Flutter SDK):

``` 
cd frontend
flutter pub get
flutter run
``` 
The API docs will be available at http://localhost:8000/docs for testing.
