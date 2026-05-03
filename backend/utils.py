"""
Utility Functions Module
File: backend/utils.py
Description: Helper functions and utilities
"""


def calculate_statistics(original_text, summary_text):
    """
    Calculate summary statistics
    
    Args:
        original_text (str): Original document text
        summary_text (str): Generated summary text
        
    Returns:
        dict: Statistics dictionary
    """
    original_words = len(original_text.split())
    original_chars = len(original_text)
    summary_words = len(summary_text.split())
    summary_chars = len(summary_text)
    
    # Calculate compression ratio
    compression_ratio = 0
    if original_words > 0:
        compression_ratio = ((original_words - summary_words) / original_words) * 100
    
    return {
        'original_words': original_words,
        'original_chars': original_chars,
        'summary_words': summary_words,
        'summary_chars': summary_chars,
        'compression_ratio': compression_ratio,
        'reduction_words': original_words - summary_words,
        'reduction_percentage': compression_ratio
    }


def validate_text_length(text, max_length=8000):
    """
    Validate and truncate text if necessary
    
    Args:
        text (str): Input text
        max_length (int): Maximum allowed length
        
    Returns:
        tuple: (truncated_text, was_truncated)
    """
    if len(text) <= max_length:
        return text, False
    else:
        return text[:max_length], True


def estimate_processing_time(word_count, model_type="medium"):
    """
    Estimate processing time based on word count and model
    
    Args:
        word_count (int): Number of words in document
        model_type (str): Type of model (small/medium/large)
        
    Returns:
        int: Estimated time in seconds
    """
    # Base time per 1000 words
    time_per_1k = {
        "small": 3,   # Phi
        "medium": 5,  # Llama 2
        "large": 8    # Mistral or larger models
    }
    
    base_time = time_per_1k.get(model_type, 5)
    estimated = (word_count / 1000) * base_time
    
    return max(int(estimated), 5)  # Minimum 5 seconds


def clean_text(text):
    """
    Clean and normalize text
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
    """
    # Remove excessive whitespace
    import re
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def split_into_chunks(text, chunk_size=4000, overlap=200):
    """
    Split long text into overlapping chunks
    
    Args:
        text (str): Input text
        chunk_size (int): Size of each chunk
        overlap (int): Overlap between chunks
        
    Returns:
        list: List of text chunks
    """
    words = text.split()
    chunks = []
    
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
        
        if start >= len(words):
            break
    
    return chunks


def format_time(seconds):
    """
    Format seconds into human-readable time
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def get_file_size_mb(file_obj):
    """
    Get file size in megabytes
    
    Args:
        file_obj: File object
        
    Returns:
        float: File size in MB
    """
    try:
        return file_obj.size / (1024 * 1024)
    except:
        return 0.0


def truncate_filename(filename, max_length=30):
    """
    Truncate long filenames
    
    Args:
        filename (str): Original filename
        max_length (int): Maximum length
        
    Returns:
        str: Truncated filename
    """
    if len(filename) <= max_length:
        return filename
    
    # Keep extension
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    
    available = max_length - len(ext) - 4  # 4 for "..." and "."
    if available > 0:
        return f"{name[:available]}...{ext}"
    else:
        return filename[:max_length]


def count_sentences(text):
    """
    Count number of sentences in text
    
    Args:
        text (str): Input text
        
    Returns:
        int: Number of sentences
    """
    import re
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])


def get_reading_time(text, words_per_minute=200):
    """
    Estimate reading time for text
    
    Args:
        text (str): Input text
        words_per_minute (int): Average reading speed
        
    Returns:
        str: Estimated reading time
    """
    word_count = len(text.split())
    minutes = word_count / words_per_minute
    
    if minutes < 1:
        return "< 1 minute"
    elif minutes < 60:
        return f"{int(minutes)} minute{'s' if minutes != 1 else ''}"
    else:
        hours = minutes / 60
        return f"{hours:.1f} hour{'s' if hours != 1 else ''}"


def extract_key_stats(text):
    """
    Extract key statistics from text
    
    Args:
        text (str): Input text
        
    Returns:
        dict: Statistics dictionary
    """
    words = text.split()
    chars = len(text)
    sentences = count_sentences(text)
    paragraphs = len([p for p in text.split('\n\n') if p.strip()])
    
    return {
        'words': len(words),
        'characters': chars,
        'sentences': sentences,
        'paragraphs': paragraphs,
        'avg_word_length': chars / len(words) if words else 0,
        'avg_sentence_length': len(words) / sentences if sentences else 0
    }
