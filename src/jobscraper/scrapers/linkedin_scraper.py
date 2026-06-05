import requests
from bs4 import BeautifulSoup

from ..site_utils.linkedin.locations import LOCATION
from ..site_utils.linkedin.companies import COMPANY

DATE_POSTED = {
    "Past month": "r2592000",
    "Past week": "r604800",
    "Past 24 hours": "r86400",
}
EXPERIENCE_LEVEL = {
    "Internship": "1",
    "Entry level": "2",
    "Associate": "3",
    "Mid-Senior level": "4",
    "Director": "5",
    "Executive": "6",
}
REMOTE = {
    "On-site": "1",
    "Remote": "2",
    "Hybrid": "3",
}


def add_linkedin_arguments(parser):
    parser.add_argument("--keywords", type=str, nargs="*")
    parser.add_argument("--location", type=str)
    parser.add_argument("--date-posted", type=str, choices=DATE_POSTED.keys())
    parser.add_argument("--experience-level", type=str, choices=EXPERIENCE_LEVEL.keys(), nargs="+")
    parser.add_argument("--company", type=str, nargs="*")
    parser.add_argument("--remote", type=str, choices=REMOTE.keys(), nargs="+")
    parser.add_argument("--easy-apply", action="store_true")


def scrape_linkedin(args):
    queries = []
    if args.keywords:
        queries.append(f"keywords={'%20'.join(args.keywords)}")
    if args.location:
        queries.append(f"geoId={LOCATION[args.location]}")
    if args.date_posted:
        queries.append(f"f_TPR={DATE_POSTED[args.date_posted]}")
    if args.experience_level:
        levels = [EXPERIENCE_LEVEL[level] for level in args.experience_level]
        queries.append(f"f_E={'%2C'.join(levels)}")
    if args.company:
        companies = [COMPANY[company] for company in args.company]
        queries.append(f"f_C={'%2C'.join(companies)}")
    if args.remote:
        remotes = [REMOTE[remote] for remote in args.remote]
        queries.append(f"f_WT={'%2C'.join(remotes)}")
    if args.easy_apply:
        queries.append("f_AL=true")

    URL = "https://www.linkedin.com/jobs/search/?"
    if queries:
        URL += "&".join(queries)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    jobs_list = soup.find("ul", class_="jobs-search__results-list")
    
    job_cards = jobs_list.find_all("div", class_="base-card")

    for card in job_cards:
        title_element = card.find("h3", class_="base-search-card__title")
        company_element = card.find("h4", class_="base-search-card__subtitle").a
        location_element = card.find("span", class_="job-search-card__location")
        print(title_element.text.strip())
        print(company_element.text.strip())
        print(location_element.text.strip())
        link_url = card.find("a", class_="base-card__full-link")["href"]
        print(f"Apply here: {link_url}\n")
