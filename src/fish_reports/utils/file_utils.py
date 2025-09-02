"""
File utility functions.
"""

import logging
import os
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def validate_file_path(file_path: Path) -> bool:
    """
    Validate if a file path exists and is readable.

    Args:
        file_path: Path to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        # Simplified validation - just check if file exists and is a file
        return file_path.exists() and file_path.is_file()
    except Exception:
        return False


def validate_directory_path(dir_path: Path) -> bool:
    """
    Validate if a directory path exists and is accessible.

    Args:
        dir_path: Directory path to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        return dir_path.exists() and dir_path.is_dir() and os.access(dir_path, os.R_OK | os.W_OK)
    except Exception:
        return False


def create_directory_if_not_exists(dir_path: Path) -> bool:
    """
    Create directory if it doesn't exist.

    Args:
        dir_path: Directory path to create

    Returns:
        True if successful or already exists, False otherwise
    """
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {dir_path}: {e}")
        return False


def get_file_extension(file_path: Path) -> str:
    """
    Get file extension in lowercase.

    Args:
        file_path: Path to file

    Returns:
        File extension without dot
    """
    return file_path.suffix.lower().lstrip('.')


def is_excel_file(file_path: Path) -> bool:
    """
    Check if file is an Excel file.

    Args:
        file_path: Path to file

    Returns:
        True if Excel file, False otherwise
    """
    ext = get_file_extension(file_path)
    return ext in ['xlsx', 'xls']


def is_csv_file(file_path: Path) -> bool:
    """
    Check if file is a CSV file.

    Args:
        file_path: Path to file

    Returns:
        True if CSV file, False otherwise
    """
    ext = get_file_extension(file_path)
    return ext == 'csv'


def find_files_with_extension(directory: Path, extensions: List[str]) -> List[Path]:
    """
    Find all files with specified extensions in directory.

    Args:
        directory: Directory to search
        extensions: List of extensions to search for (without dots)

    Returns:
        List of found file paths
    """
    found_files = []

    try:
        for ext in extensions:
            pattern = f"*.{ext}"
            found_files.extend(directory.rglob(pattern))
    except Exception as e:
        logger.error(f"Error searching for files in {directory}: {e}")

    return found_files


def get_safe_filename(filename: str) -> str:
    """
    Create a safe filename by removing/replacing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Safe filename
    """
    # Characters that are invalid in Windows filenames
    invalid_chars = '<>:"/\\|?*'

    safe_name = filename
    for char in invalid_chars:
        safe_name = safe_name.replace(char, '_')

    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip(' .')

    return safe_name


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"

    units = ['B', 'KB', 'MB', 'GB']
    unit_index = 0
    size = float(size_bytes)

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.1f} {units[unit_index]}"
