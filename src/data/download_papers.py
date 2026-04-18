import arxiv
import os

def download_ml_papers(query='all:"retrieval augmented generation" OR all:"large language models"', max_results=5, output_dir="data/raw"):
    """
    Downloads arXiv papers matching the given query to the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the arxiv client
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    print(f"Searching for {max_results} papers on arXiv...")
    
    for result in client.results(search):
        paper_id = result.get_short_id().replace('/', '_')
        title = result.title.replace('\n', ' ')
        filename = f"{paper_id}.pdf"
        filepath = os.path.join(output_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Downloading: {title} ({paper_id})")
            result.download_pdf(dirpath=output_dir, filename=filename)
        else:
            print(f"Already exists: {title} ({paper_id})")
            
    print("Download complete!")

if __name__ == "__main__":
    # Download 5 recent papers related to RAG and LLMs
    download_ml_papers(max_results=5)
