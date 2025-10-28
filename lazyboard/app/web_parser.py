from time import sleep

import requests
from bs4 import BeautifulSoup
from db.db import insert_jobs
from scraper.score import retrieve_job_score


def fetch_job_page(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
    }

    try:
        sleep(0.5)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def parse_job_html(html, url):
    if "linkedin" in url:
        return parse_linkedin(html, url)
    elif "indeed" in url:
        return parse_indeed(html, url)
    elif "welcometothejungle" in url:
        return parse_wttj(html, url)
    elif "hellowork" in url or "regionsjob" in url:
        return parse_hellowork(html, url)
    else:
        return parse_generic(html, url)


def parse_generic(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title = (soup.find("h1") or {}).get_text(strip=True) if soup.find("h1") else ""

    company = ""
    for tag, cls in [("div", "company"), ("meta", {"property": "og:site_name"})]:
        el = soup.find(tag, class_=cls) if isinstance(cls, str) else soup.find(tag, cls)
        if el:
            company = (
                el.get_text(strip=True) if el.name != "meta" else el.get("content", "")
            )
            break

    location = ""
    for tag, cls in [("div", "location"), ("span", "companyLocation")]:
        el = soup.find(tag, class_=cls)
        if el:
            location = el.get_text(strip=True)
            break

    type = (
        (soup.find("span", class_="job-type") or {}).get_text(strip=True)
        if soup.find("span", class_="job-type")
        else ""
    )

    score = retrieve_job_score(title)

    return {
        "title": title,
        "company": company,
        "location": location,
        "site": "other",
        "url": url,
        "type": type,
        "score": score,
    }


def parse_linkedin(html, url):
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.find("h1") or {}).get_text(strip=True) if soup.find("h1") else ""

    company = ""
    for sel in ["a.topcard__org-name-link", "span.topcard__flavor"]:
        el = soup.select_one(sel)
        if el:
            company = el.get_text(strip=True)
            break

    location = ""
    for sel in [
        "span.topcard__flavor.topcard__flavor--bullet",
        "div.jobs-unified-top-card__bullet",
    ]:
        el = soup.select_one(sel)
        if el:
            location = el.get_text(strip=True)
            break

    return build_job_dict(title, company, location, "linkedin", url)


def parse_indeed(html, url):
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.find("h1") or {}).get_text(strip=True) if soup.find("h1") else ""

    company = ""
    for sel in ["span.companyName", "div.icl-u-lg-mr--sm.icl-u-xs-mr--xs"]:
        el = soup.select_one(sel)
        if el:
            company = el.get_text(strip=True)
            break

    location = ""
    for sel in ["div.jobsearch-JobInfoHeader-subtitle", "span.companyLocation"]:
        el = soup.select_one(sel)
        if el:
            location = el.get_text(strip=True)
            break

    return build_job_dict(title, company, location, "indeed", url)


def parse_wttj(html, url):
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.find("h2") or {}).get_text(strip=True) if soup.find("h2") else ""

    company = ""
    location = ""
    metadata_block = soup.find(attrs={"data-testid": "job-metadata-block"})
    if metadata_block:
        company_link = metadata_block.find("a", href=True)
        if company_link:
            company_name_tag = company_link.find_next_sibling()
            if company_name_tag:
                company = company_name_tag.get_text(strip=True)
            else:
                company = company_link.get_text(strip=True)

        location_icon = metadata_block.find("i", attrs={"name": "location"})
        if location_icon:
            location_span = location_icon.find_next_sibling("span")
            if location_span:
                location = location_span.get_text(strip=True)

    return build_job_dict(title, company, location, "welcometothejungle", url)


def parse_hellowork(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title = ""
    title_selectors = [
        ("span", {"data-cy": "jobTitle"}),
        ("h1", None),
    ]
    for tag, attrs in title_selectors:
        el = soup.find(tag, attrs) if attrs else soup.find(tag)
        if el:
            title = el.get_text(strip=True)
            break

    company = ""
    title_h1 = soup.find("h1", id="main-content")
    if title_h1:
        company_tag = title_h1.find("a", href=True, title=True)
        if company_tag:
            company = company_tag.get_text(strip=True)

    location = ""
    if title_h1:
        next_ul = title_h1.find_next("ul")
        if next_ul:
            first_li = next_ul.find("li")
            if first_li:
                location = first_li.get_text(strip=True)

    return build_job_dict(title, company, location, "hellowork", url)


def build_job_dict(title, company, location, site, url):
    score = retrieve_job_score(title)
    return {
        "title": title,
        "company": company,
        "location": location,
        "site": site,
        "url": url,
        "type": "",
        "score": score,
    }


def add_job_entry(url):
    html = fetch_job_page(url)
    if not html:
        print(f"Failed to fetch job page: {url}")
        return False
    job = parse_job_html(html, url)
    insert_jobs([job])
    return True
