#!/usr/bin/env python3
"""
ISBN Lookup Tool

A Python tool that fetches comprehensive book information from multiple sources using ISBN numbers.
This tool queries various APIs to gather complete book metadata including title, authors, 
publication date, description, subjects, and cover images.

Author: Your Name
Version: 1.0.0
License: MIT
"""

import requests
import time
import json
import sys
import os
from typing import Dict, List, Optional, Tuple, Callable
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('isbn_lookup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BookInfo:
    """Data class to represent book information"""
    
    def __init__(self, title: str = "Unknown Title", authors: List[str] = None,
                 publish_date: str = "Unknown Publish Date", description: str = "Unknown Description",
                 subject: str = "Unknown Subject", cover_image: str = "No Cover Image",
                 isbn: str = "", source: str = ""):
        self.title = title
        self.authors = authors or ["Unknown Author"]
        self.publish_date = publish_date
        self.description = description
        self.subject = subject
        self.cover_image = cover_image
        self.isbn = isbn
        self.source = source
        self.book = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "title": self.title,
            "authors": self.authors,
            "publish_date": self.publish_date,
            "description": self.description,
            "subject": self.subject,
            "cover_image": self.cover_image,
            "isbn": self.isbn,
            "book": self.book,
            "source": self.source
        }
    
    def is_complete(self) -> bool:
        """Check if all fields have meaningful values"""
        return (self.title != "Unknown Title" and
                self.authors != ["Unknown Author"] and
                self.publish_date != "Unknown Publish Date" and
                self.description != "Unknown Description" and
                self.subject != "Unknown Subject" and
                self.cover_image != "No Cover Image")


class ISBNLookup:
    """Main class for ISBN lookup functionality"""
    
    def __init__(self, timeout: int = 10, delay: float = 0.3):
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ISBN-Lookup-Tool/1.0 (Educational Use)'
        })
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make HTTP request with error handling"""
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {url}: {e}")
            return None
    
    def _clean_isbn(self, isbn: str) -> str:
        """Clean ISBN by removing hyphens and spaces"""
        return isbn.replace("-", "").replace(" ", "")
    
    def fetch_from_google_books(self, isbn: str) -> Optional[BookInfo]:
        """Fetch book information from Google Books API"""
        logger.info("Querying Google Books API")
        
        data = self._make_request(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
        if not data or data.get("totalItems", 0) == 0:
            return None
        
        book_info = data["items"][0]["volumeInfo"]
        categories = book_info.get("categories", [])
        subject = ", ".join(categories) if categories else "Unknown Subject"
        
        return BookInfo(
            title=book_info.get("title", "Unknown Title"),
            authors=book_info.get("authors", ["Unknown Author"]),
            publish_date=book_info.get("publishedDate", "Unknown Publish Date"),
            description=book_info.get("description", "Unknown Description"),
            subject=subject,
            cover_image=book_info.get("imageLinks", {}).get("thumbnail", "No Cover Image"),
            isbn=isbn,
            source="Google Books"
        )
    
    def fetch_from_openlibrary(self, isbn: str) -> Optional[BookInfo]:
        """Fetch book information from OpenLibrary API"""
        logger.info("Querying OpenLibrary API")
        
        data = self._make_request(
            f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=details&format=json"
        )
        if not data:
            return None
        
        book_details = data.get(f"ISBN:{isbn}", {}).get("details", {})
        if not book_details:
            return None
        
        authors = [author.get("name", "Unknown Author") for author in book_details.get("authors", [])]
        subjects = book_details.get("subjects", [])
        subject = ", ".join(subjects[:3]) if subjects else "Unknown Subject"
        
        description = book_details.get("description", "Unknown Description")
        if isinstance(description, dict):
            description = description.get("value", "Unknown Description")
        
        return BookInfo(
            title=book_details.get("title", "Unknown Title"),
            authors=authors,
            publish_date=book_details.get("publish_date", "Unknown Publish Date"),
            description=description,
            subject=subject,
            cover_image=book_details.get("cover", {}).get("large", "No Cover Image"),
            isbn=isbn,
            source="OpenLibrary"
        )
    
    def fetch_from_internet_archive(self, isbn: str) -> Optional[BookInfo]:
        """Fetch book information from Internet Archive API"""
        logger.info("Querying Internet Archive API")
        
        data = self._make_request(
            f"https://archive.org/advancedsearch.php?q=isbn:{isbn}&fl=identifier,title,creator,date,description,subject&output=json"
        )
        if not data:
            return None
        
        docs = data.get("response", {}).get("docs", [])
        if not docs:
            return None
        
        doc = docs[0]
        cover = f"https://archive.org/services/img/{doc['identifier']}"
        
        return BookInfo(
            title=doc.get("title", "Unknown Title"),
            authors=[doc.get("creator", "Unknown Author")],
            publish_date=doc.get("date", "Unknown Publish Date"),
            description=doc.get("description", "Unknown Description"),
            subject=", ".join(doc.get("subject", [])) if doc.get("subject") else "Unknown Subject",
            cover_image=cover,
            isbn=isbn,
            source="Internet Archive"
        )
    
    def fetch_from_openalex(self, isbn: str) -> Optional[BookInfo]:
        """Fetch book information from OpenAlex API"""
        logger.info("Querying OpenAlex API")
        
        clean_isbn = self._clean_isbn(isbn)
        search_queries = [
            f"https://api.openalex.org/works?search={clean_isbn}",
            f"https://api.openalex.org/works?filter=primary_location.source.issn:{clean_isbn}",
        ]
        
        for url in search_queries:
            data = self._make_request(url, {"mailto": "research@example.com"})
            if not data:
                continue
            
            results = data.get("results", [])
            if not results:
                continue
            
            work = results[0]
            authors = [a["author"]["display_name"] for a in work.get("authorships", [])] or ["Unknown Author"]
            concepts = [c["display_name"] for c in work.get("concepts", [])][:3]
            subject = ", ".join(concepts) if concepts else "Unknown Subject"
            
            abstract = work.get("abstract_inverted_index", None)
            description = "Abstract available" if abstract else "Unknown Description"
            
            return BookInfo(
                title=work.get("title", "Unknown Title"),
                authors=authors,
                publish_date=str(work.get("publication_year", "Unknown Publish Date")),
                description=description,
                subject=subject,
                cover_image="No Cover Image",
                isbn=isbn,
                source="OpenAlex"
            )
        
        return None
    
    def fetch_from_openlibrary_covers(self, isbn: str) -> Optional[BookInfo]:
        """Fetch book cover from OpenLibrary Covers API"""
        logger.info("Querying OpenLibrary Covers API")
        
        try:
            cover_response = self.session.get(f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg")
            cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg" if cover_response.status_code == 200 else "No Cover Image"
            
            data = self._make_request(f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json")
            if not data or f"ISBN:{isbn}" not in data:
                return None
            
            book_data = data[f"ISBN:{isbn}"]
            authors = [author.get("name", "Unknown Author") for author in book_data.get("authors", [])]
            
            return BookInfo(
                title=book_data.get("title", "Unknown Title"),
                authors=authors,
                publish_date=book_data.get("publish_date", "Unknown Publish Date"),
                description="Unknown Description",
                subject="Unknown Subject",
                cover_image=cover_url,
                isbn=isbn,
                source="OpenLibrary Covers"
            )
        except Exception as e:
            logger.error(f"OpenLibrary Covers API error: {e}")
            return None
    
    def fetch_from_abebooks_covers(self, isbn: str) -> Optional[BookInfo]:
        """Fetch book cover from AbeBooks API"""
        logger.info("Querying AbeBooks Covers API")
        
        try:
            cover_url = f"https://pictures.abebooks.com/isbn/{isbn}-us-300.jpg"
            cover_response = self.session.get(cover_url)
            
            if cover_response.status_code == 200:
                return BookInfo(
                    title="Unknown Title",
                    authors=["Unknown Author"],
                    publish_date="Unknown Publish Date",
                    description="Unknown Description",
                    subject="Unknown Subject",
                    cover_image=cover_url,
                    isbn=isbn,
                    source="AbeBooks Covers"
                )
        except Exception as e:
            logger.error(f"AbeBooks Covers API error: {e}")
        
        return None
    
    def merge_book_data(self, results: List[BookInfo]) -> BookInfo:
        """Merge book data from multiple sources"""
        merged = BookInfo(isbn=results[0].isbn if results else "")
        sources = []
        
        for result in results:
            if result:
                sources.append(result.source)
                
                # Prefer non-default values
                if result.title != "Unknown Title":
                    merged.title = result.title
                
                if result.authors != ["Unknown Author"] and result.authors:
                    merged.authors = result.authors
                
                if result.publish_date != "Unknown Publish Date":
                    merged.publish_date = result.publish_date
                
                if result.description != "Unknown Description":
                    merged.description = result.description
                
                if result.subject != "Unknown Subject":
                    merged.subject = result.subject
                
                if result.cover_image != "No Cover Image":
                    merged.cover_image = result.cover_image
        
        # Add sources information to the merged result
        merged_dict = merged.to_dict()
        merged_dict["sources"] = sources
        
        return merged_dict
    
    def get_book_details(self, isbn: str) -> Optional[Dict]:
        """Get book details from multiple APIs"""
        logger.info(f"Fetching details for ISBN: {isbn}")
        
        apis: List[Tuple[str, Callable]] = [
            ("Google Books", self.fetch_from_google_books),
            ("OpenLibrary", self.fetch_from_openlibrary),
            ("Internet Archive", self.fetch_from_internet_archive),
            ("OpenLibrary Covers", self.fetch_from_openlibrary_covers),
            ("OpenAlex", self.fetch_from_openalex),
            ("AbeBooks Covers", self.fetch_from_abebooks_covers)
        ]
        
        results = []
        
        for api_name, api_function in apis:
            try:
                result = api_function(isbn)
                if result:
                    logger.info(f"✅ Found data from {result.source}")
                    results.append(result)
                    
                    # Return immediately if we have complete data
                    if result.is_complete():
                        return result.to_dict()
                else:
                    logger.warning(f"❌ No data from {api_name}")
            except Exception as e:
                logger.error(f"❌ Error with {api_name}: {e}")
            
            time.sleep(self.delay)
        
        if results:
            return self.merge_book_data(results)
        else:
            logger.warning("No book details found from any source")
            return None
    
    def process_isbn_file(self, input_file: str = "isbn.txt", output_file: str = "isbn.json"):
        """Process ISBNs from file and save results"""
        if not os.path.exists(input_file):
            logger.error(f"Input file '{input_file}' not found")
            return
        
        all_books = []
        
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                isbns = [line.strip() for line in f if line.strip()]
            
            logger.info(f"Processing {len(isbns)} ISBNs")
            
            for i, isbn in enumerate(isbns, 1):
                logger.info(f"Processing ISBN {i}/{len(isbns)}: {isbn}")
                
                book_info = self.get_book_details(isbn)
                if book_info:
                    all_books.append(book_info)
                    if 'sources' in book_info:
                        logger.info(f"Sources used: {', '.join(book_info['sources'])}")
                else:
                    logger.warning(f"No information found for ISBN: {isbn}")
            
            # Save results
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_books, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to {output_file}")
            logger.info(f"Successfully processed {len(all_books)} out of {len(isbns)} ISBNs")
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Command line usage
        isbn = sys.argv[1]
        lookup = ISBNLookup()
        result = lookup.get_book_details(isbn)
        
        if result:
            print(json.dumps(result, indent=2))
        else:
            print("No book information found")
            sys.exit(1)
    else:
        # Batch processing
        lookup = ISBNLookup()
        lookup.process_isbn_file()


if __name__ == "__main__":
    main()
