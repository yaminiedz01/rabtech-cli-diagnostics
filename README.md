# RabTech Python Engineering Projects

A collection of Python projects developed during the RabTech Academy
Python Software Engineering Virtual Internship Program.

The repository demonstrates Python programming, CLI development,
OOP, data persistence, web scraping, REST APIs, JWT authentication,
and end-to-end automation.

---

## Projects

### Task 02 — CLI Diagnostics Tool

A command-line diagnostic tool that checks:

- Python version and executable path
- Disk space
- Environment variables
- JSON formatted diagnostic output

### Task 03 — Inventory Management System

An object-oriented inventory system demonstrating:

- Class hierarchy and inheritance
- Polymorphism
- Custom exceptions
- JSON persistence
- CSV persistence
- Unit testing

The project achieved over 90% test coverage.

### Task 04 — Web Scraping Pipeline

An automated web scraping pipeline using:

- Python
- Requests
- BeautifulSoup
- Retry logic
- Custom User-Agent headers
- Rate limiting
- CSV data extraction
- JSON summary statistics

### Task 05 — Secure Inventory API

A FastAPI microservice providing:

- User registration
- Secure login
- bcrypt password hashing
- JWT Bearer authentication
- Protected CRUD operations
- Pydantic validation
- Swagger/OpenAPI documentation
- Postman API collection

### Task 06 — Enterprise Python Automation Capstone

An end-to-end automated inventory reporting application.

The application connects to the FastAPI inventory service,
authenticates using JWT, retrieves inventory data, processes
statistics, and generates PDF and JSON reports.

---

# Task 06 — Automated Inventory Report Generator

## Project Overview

The Automated Inventory Report Generator is an end-to-end Python
automation application built as the Enterprise Python Automation
Capstone Project.

It integrates a backend API, authentication, data processing,
report generation, and automated scheduling into a single workflow.

## Architecture

```text
                ┌──────────────────────┐
                │   FastAPI Inventory  │
                │         API          │
                └──────────┬───────────┘
                           │
                           │ JWT Login
                           ▼
                ┌──────────────────────┐
                │  Report Generator    │
                │       CLI            │
                └──────────┬───────────┘
                           │
                           │ Fetch Products
                           ▼
                ┌──────────────────────┐
                │   Data Processing    │
                │ & Statistics Engine  │
                └──────────┬───────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
        ┌────────────────┐   ┌────────────────┐
        │   PDF Report   │   │   JSON Report  │
        └────────────────┘   └────────────────┘
                           │
                           ▼
                 Automated Scheduling