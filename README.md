# ISBN Lookup Tool

A Python tool that fetches comprehensive book information from multiple sources using ISBN numbers. This tool queries various APIs to gather complete book metadata including title, authors, publication date, description, subjects, and cover images.

## Features

- **Multiple Data Sources**: Queries 6 different APIs to maximize data coverage
  - Google Books API
  - OpenLibrary API
  - Internet Archive API
  - OpenAlex API
  - OpenLibrary Covers API
  - AbeBooks Covers API
- **Smart Data Merging**: Combines results from multiple sources to provide complete book information
- **Batch Processing**: Processes multiple ISBNs from a text file
- **JSON Output**: Saves results in structured JSON format
- **Error Handling**: Graceful handling of API failures and network issues
- **Rate Limiting**: Built-in delays to respect API rate limits

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/IsbnLookup.git
cd IsbnLookup

# Run the setup script (installs dependencies and creates sample files)
python setup.py
```

### Basic Usage

```bash
# Look up a single ISBN
python isbn_lookup.py 9780134685991

# Process multiple ISBNs from file (create isbn.txt first)
python isbn_lookup.py

# Set up the project (installs dependencies and creates sample files)
python setup.py
```

## Usage

## Detailed Usage

### Traditional Batch Processing

1. Create an `isbn.txt` file with one ISBN per line:

```txt
9780134685991
978-0-596-52068-7
9781449355739
```

2. Run the batch processor:

```bash
python isbn_lookup.py
```

3. Results will be saved to `isbn.json` with detailed book information.

### Programmatic Usage

You can also use the improved object-oriented API directly in your Python code:

```python
from isbn_lookup import ISBNLookup

# Create lookup instance with default settings
lookup = ISBNLookup()

# Get details for a single ISBN
book_info = lookup.get_book_details("9780134685991")
if book_info:
    print(f"Title: {book_info['title']}")
    print(f"Authors: {', '.join(book_info['authors'])}")
    print(f"Published: {book_info['publish_date']}")
    print(f"Sources: {', '.join(book_info.get('sources', []))}")

# Custom configuration
lookup = ISBNLookup(timeout=15, delay=0.5)
book_info = lookup.get_book_details("9780134685991")

# Batch processing with custom files
lookup.process_isbn_file("my_books.txt", "results.json")
```

### Command Line Usage

You can also use the tool from the command line for single ISBN lookups:

```bash
# Look up a single ISBN
python isbn_lookup.py 9780134685991

# Process multiple ISBNs from file (default behavior)
python isbn_lookup.py
```

## Output Format

The tool generates a JSON file with the following structure:

```json
[
  {
    "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
    "authors": ["Robert C. Martin"],
    "publish_date": "2008",
    "description": "Even bad code can function. But if code isn't clean, it can bring a development organization to its knees...",
    "subject": "Computer programming, Software engineering",
    "cover_image": "https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg",
    "isbn": "9780132350884",
    "book": true,
    "sources": ["Google Books", "OpenLibrary"]
  }
]
```

## API Sources

### Primary Sources (with full metadata)

- **Google Books**: Most comprehensive source with descriptions, categories, and cover images
- **OpenLibrary**: Extensive collection with detailed subject information
- **Internet Archive**: Historical and academic texts

### Secondary Sources (specialized data)

- **OpenAlex**: Academic and research publications
- **OpenLibrary Covers**: High-quality book cover images
- **AbeBooks Covers**: Alternative cover image source

## Error Handling

The tool includes robust error handling:

- Continues processing even if some APIs fail
- Provides detailed error messages for debugging
- Merges partial results from multiple sources
- Handles network timeouts and rate limits

## Configuration

The tool includes several configuration options for customization:

### Runtime Configuration

```python
from isbn_lookup import ISBNLookup

# Custom timeout and delay settings
lookup = ISBNLookup(timeout=15, delay=0.5)

# Process with custom file names
lookup.process_isbn_file("my_books.txt", "my_results.json")
```

### Configuration File

The tool supports a `config.ini` file for persistent settings:

```ini
[API_SETTINGS]
timeout = 10
delay = 0.3
max_retries = 3

[OUTPUT_SETTINGS]
default_output_file = isbn.json
default_input_file = isbn.txt
pretty_print = true
```

### API Priority

You can customize which APIs are queried and in what order by modifying the `apis` list in the `get_book_details()` method.

## Rate Limiting

The tool includes a 0.3-second delay between API calls to respect rate limits. You can adjust this in the `get_book_details()` function.

## Dependencies

- `requests>=2.25.1`: For HTTP API calls
- `typing-extensions>=4.0.0`: For enhanced type hints
- Built-in modules: `json`, `time`, `logging`, `sys`, `os`

## Project Structure

```txt
IsbnLookup/
├── README.md              # This documentation
├── isbn_lookup.py         # Main improved implementation
├── setup.py               # Setup and installation script
├── requirements.txt       # Python dependencies
├── config.ini            # Configuration file
├── LICENSE               # Apache 2.0 License
├── isbn.txt              # Sample input file (created by setup.py)
├── isbn_lookup.log       # Generated log file (created during execution)
└── isbn.json             # Generated results file (created during execution)
```

## Backward Compatibility

This is the improved version of the original ISBN lookup script. The tool has been completely rewritten with modern Python practices and enhanced functionality.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

1. **No results found**:

   - Verify the ISBN format is correct (10 or 13 digits)
   - Check your internet connection
   - Some very new or obscure books may not be in the databases
   - Try running with a single ISBN first: `python isbn_lookup.py 9780134685991`

2. **API errors**:

   - The tool will continue with other APIs if one fails
   - Check the console output or `isbn_lookup.log` for specific error messages
   - Some APIs may have temporary outages

3. **Rate limiting**:

   - If you encounter rate limits, increase the delay: `ISBNLookup(delay=1.0)`
   - Consider processing ISBNs in smaller batches
   - The default 0.3-second delay should work for most use cases

4. **File not found errors**:

   - Make sure `isbn.txt` exists in the same directory
   - Run `python setup.py` to create sample files
   - Check file permissions

5. **Import errors**:
   - Install dependencies: `pip install -r requirements.txt`
   - Make sure you're using Python 3.6+

### Debug Mode

For detailed debugging, you can enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from isbn_lookup import ISBNLookup
lookup = ISBNLookup()
```

### Getting Help

- Check the log file: `isbn_lookup.log` (created when you run the tool)
- Review the configuration: `config.ini`
- Create sample files: `python setup.py`

## Changelog

### v2.0.0 - Major Rewrite (Current)

- ✨ **New**: Object-oriented architecture with `ISBNLookup` class
- ✨ **New**: Command-line interface for single ISBN lookup
- ✨ **New**: Comprehensive logging system with file output
- ✨ **New**: Type hints and modern Python features
- ✨ **New**: Configuration file support
- ✨ **New**: Setup script for easy installation
- 🔧 **Improved**: Better error handling and recovery
- 🔧 **Improved**: Smart data merging algorithm
- 🔧 **Improved**: Session management for better performance
- 🔧 **Improved**: UTF-8 support for international characters
- 🔧 **Improved**: Progress tracking and status reporting
- 📚 **Documentation**: Complete rewrite of README with examples

### v1.0.0 - Initial Release

- Initial release
- Support for 6 different APIs
- Batch processing from text files
- JSON output format
- Basic error handling and rate limiting

## New Features & Improvements

### 🏗️ **Modern Architecture**

- **Object-Oriented Design**: Clean `ISBNLookup` class with configurable parameters
- **Data Classes**: Structured `BookInfo` class for better data handling
- **Type Hints**: Full type annotations for better IDE support and code clarity
- **Session Management**: Reusable HTTP sessions for better performance

### 🔧 **Enhanced Functionality**

- **Command Line Interface**: Single ISBN lookup or batch processing
- **Smart Data Merging**: Intelligently combines results from multiple sources
- **Early Termination**: Stops searching when complete data is found
- **Comprehensive Logging**: Detailed logs with configurable levels
- **Error Recovery**: Graceful handling of API failures with fallback options

### 📊 **Better Output**

- **Source Tracking**: Shows which APIs provided the data
- **Progress Indicators**: Real-time feedback during batch processing
- **Structured Logging**: Separate log files for debugging and monitoring
- **UTF-8 Support**: Proper handling of international characters

### ⚙️ **Configuration Options**

- **Configurable Timeouts**: Adjust request timeouts for different network conditions
- **Rate Limiting**: Customizable delays between API calls
- **Flexible File Handling**: Custom input/output file names
- **API Priority**: Choose which sources to query first

## What's New in Version 2.0

### 🎯 **Key Improvements**

1. **Professional Architecture**: Complete rewrite with object-oriented design
2. **Enhanced CLI**: Support for both single ISBN lookup and batch processing
3. **Smart Data Processing**: Intelligent merging and early termination when complete data is found
4. **Comprehensive Logging**: Detailed logs with multiple levels and file output
5. **Better Error Handling**: Graceful failure handling with detailed error messages
6. **Configuration Support**: Customizable settings via code or configuration files
7. **Type Safety**: Full type hints for better development experience
8. **Professional Setup**: Easy installation and configuration process

### 🔄 **Migration Guide**

If you're upgrading from the original version:

1. **Fresh Start**: This version is a complete rewrite with modern Python practices
2. **Enhanced Features**: Use the new CLI interface for single ISBN lookup or batch processing
3. **Easy Setup**: Run `python setup.py` to get started quickly

```bash
# New usage options
python isbn_lookup.py                    # Batch processing
python isbn_lookup.py 9780134685991     # Single ISBN lookup
python setup.py                         # Setup and install dependencies
```
