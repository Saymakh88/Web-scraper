from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
from .models import Link
import pandas as pd
import matplotlib.pyplot as plt
import io, urllib, base64
from urllib.parse import urlparse

def scrape(request):
    site = request.POST.get("site", "") if request.method == "POST" else ""
    
    # Handle POST request for scraping
    if request.method == "POST":
        if site:
            try:
                page = requests.get(site)
                soup = BeautifulSoup(page.text, 'html.parser')
                for link in soup.find_all('a'):
                    link_address = link.get('href')
                    link_text = link.string
                    if link_address:
                        Link.objects.create(address=link_address, name=link_text)
            except:
                pass  # Optional: Add error logging
        return redirect('/')

    # Handle GET request for displaying data and analytics
    data = Link.objects.all()
    df = pd.DataFrame(data.values())
    
    chart = None
    scatter_chart = None
    stats = None

    if not df.empty and 'address' in df.columns and 'name' in df.columns:
        df["domain"] = df["address"].apply(lambda x: urlparse(x).netloc)

        def categorize_link(href):
            if href.startswith("mailto:"):
                return "Email"
            elif any(href.endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
                return "Document"
            elif 'facebook.com' in href or 'twitter.com' in href or 'linkedin.com' in href:
                return "Social"
            elif urlparse(href).netloc == urlparse(site).netloc:
                return "Internal"
            else:
                return "External"

        df["category"] = df["address"].apply(lambda x: categorize_link(x))

        stats = {
            "total_links": len(df),
            "unique_domains": df["domain"].nunique(),
            "most_common_domain": df["domain"].mode()[0] if not df["domain"].mode().empty else "N/A"
        }

        # Bar Chart: Top 5 Domains
        domain_counts = df["domain"].value_counts().head(5)
        plt.figure(figsize=(6, 4))
        domain_counts.plot(kind="bar", color="skyblue")
        plt.title("Top 5 Domains")
        plt.xlabel("Domain")
        plt.ylabel("Link Count")
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        chart = urllib.parse.quote(base64.b64encode(buf.read()))
        buf.close()

        # Chart: Scatter Plot - Domain vs Avg Name Length
        df['name_length'] = df['name'].apply(lambda x: len(x) if x else 0)
        domain_numeric = df.groupby("domain")["name_length"].mean().reset_index()
        plt.figure(figsize=(6, 4))
        plt.scatter(domain_numeric["domain"], domain_numeric["name_length"], color='red')
        plt.xticks(rotation=45)
        plt.title("Domain vs Avg Name Length")
        plt.xlabel("Domain")
        plt.ylabel("Avg Name Length")
        plt.tight_layout()
        buf2 = io.BytesIO()
        plt.savefig(buf2, format="png")
        buf2.seek(0)
        scatter_chart = urllib.parse.quote(base64.b64encode(buf2.read()))
        buf2.close()

   
    return render(request, 'myapp/result.html', {
        'data': data,
        'chart': chart,
        'scatter_chart': scatter_chart,
        'stats': stats
    })

# ✅ Clear all data view 
def clear(request):
    Link.objects.all().delete()
    return redirect('/')