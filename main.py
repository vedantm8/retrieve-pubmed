from pymed import PubMed
from datetime import datetime, timedelta

# Initialize PubMed client
pubmed = PubMed(tool="MyTool", email="my@email.address")

# Compute date range (last 30 days)
today = datetime.today()
past_30_days = today - timedelta(days=30)
start_date = past_30_days.strftime("%Y/%m/%d")
end_date = today.strftime("%Y/%m/%d")

# Construct your query
query = f"""
(
    regn5458 OR "regn 5458" OR linvoseltamab OR regn5459 OR "regn 5459" OR bcmaxcd3 OR
    "bispecific t cell engager therap*" OR
    (
        "bispecific t cell engager*" AND
        ("b cell maturation antigen" OR bcma* OR "cd3 antigen" OR "cd3 antibody")
    ) OR
    (
        ("b cell maturation antigen" OR bcma OR "cd3 antigen" OR "cd3 antibody" OR bcma*cd3) AND
        "bispecific antibody"
    ) OR
    (
        ("b cell maturation antigen" OR bcma OR "cd3 antigen" OR "cd3 antibody" OR bcma*cd3) AND
        ("t lymphocyte activation" OR "tcr cd3 complex" OR "t cell receptor cd3 complex" OR "tcr cd3") AND
        "bispecific antibody"
    )
)
AND english[lang]
AND humans[MeSH Terms]
AND ("{start_date}"[Date - Publication] : "{end_date}"[Date - Publication])
"""

# Query PubMed for matching articles (up to 100 results)
results = pubmed.query(query, max_results=100)

# Process and print matching articles
for article in results:
    article_id = article.pubmed_id.split("\n")[0]
    title = article.title
    publication_date = article.publication_date
    abstract = article.abstract
    keywords = article.keywords or []

    # Clean keywords
    if None in keywords:
        keywords = [k for k in keywords if k]

    print(f"PubMed URL: https://pubmed.ncbi.nlm.nih.gov/{article_id}/")
    print(f"Date: {publication_date}")
    print(f"Title: {title}")
    print(f"Keywords: {', '.join(keywords)}")
    print(f"Abstract: {abstract}\n{'-' * 80}\n")
