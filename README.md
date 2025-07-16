# BookABooth - Developed in Django!
**BookABooth** is a web application for managing and booking exhibition booths.  
Originally developed by **T-Systems on site services GmbH** for the **Jade Hochschule**, the system was reimplemented using the **Django** web framework as part of my bachelor thesis.  
This project represents the reengineered version created during the thesis work and is not intended to be used in production environments.

> This repository reflects the final version of BookABooth as presented in the bachelor thesis.  
> The current state is not intended for production use, but for demonstration and evaluation purposes only.
## Setup for Development
Following steps will set up BookABooth for Development.
- Recommended, but optional: Get an IDE
- Install a current [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download) is required for TailwindCSS
- Install [Git](https://git-scm.com/downloads)
- Clone the repository to your local machine:
```bash
  git clone https://github.com/finnG030702/BookABooth_Django.git
```
- Create and activate a virtual environment:
```bash
    python -m venv venv
    source venv/bin/activate # Linux/MacOS
    venv\Scripts\activate # Windows
```
- Install Python dependencies:
```bash
    pip install -r requirements.txt
```
- Install Node.js dependencies:
```bash
    npm install
```
- Create database tables:
```bash
    python manage.py migrate
```
- Load demo data:
```bash
    python manage.py loaddata fixtures/demo_data.json
```
- Start the local development server
```bash
    python manage.py runserver
```

## Demo usage
Once the demo data has been loaded, the system contains predefined companies, users, and bookings.
You can immediately log in using one of the following credentials:
### Admin Access
```text
username: admin
password: admin
```
### Demo User Accounts
There are ten demo users available:
```text
username: demo1, demo2 ..., demo10
password: BookABooth2025!
```
These accounts can be used to test booth booking, profile features, and navigation from an exhibitor's perspective.

Feel free to explore the system as outlined in the thesis — but please note that this project is for academic purposes only.