# 🔗 Link Scraper

A Django web application that scrapes all `<a>` tags from any given URL and displays the data in a table with interactive features. It also provides visual link analytics using **Matplotlib** charts.

---

## 📌 Features

- 🔍 Scrape anchor tags from any website
- 📋 Copy individual links with one click
- 📄 Export scraped links to CSV
- 🗑️ Delete links from the table
- 📊 Visualize link data using Matplotlib charts
- ✨ Clean and responsive UI with Tailwind CSS
- ⚡ Instant "Copied!" popup using JavaScript

---

## ⚙️ Tech Stack

- **Backend:** Django
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Web Scraping:** BeautifulSoup
- **Charts & Visualization:** Matplotlib
- **Data Export:** Pandas
- **Database:** SQLite

---

## 🗂 Project Structure



---

## 📊 Link Analysis with Matplotlib

After scraping, the app analyzes and visualizes:

- **Top domains** by frequency
- **Pie chart** showing distribution of link domains

These charts are generated dynamically using **Matplotlib**, rendered as PNG, and embedded in the results page using base64 encoding.

---

## 🧪 Installation

```bash
git clone https://github.com/Saymakh88/Web-scraper.git
cd mysite
python -m venv myenv
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
