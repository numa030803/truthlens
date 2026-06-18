from newspaper import Article

def extract_from_url(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title + " " + article.text[:2000]
    except Exception as e:
        return f"Could not extract article: {str(e)}"

if __name__ == "__main__":
    text = extract_from_url("https://timesofindia.indiatimes.com")
    print(text[:500])