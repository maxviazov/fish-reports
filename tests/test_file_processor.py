"""
Tests for file processor functionality.
"""

import sys
from pathlib import Path

# Add src to path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fish_reports.data.file_processor import FileProcessor


def test_file_processor_initialization():
    """Test FileProcessor initialization."""
    processor = FileProcessor()
    assert processor.source_data is None
    assert processor.filtered_data is None


def test_column_mapping():
    """Test that column mapping contains all required fields."""
    expected_columns = [
        'business_license',
        'base_reference', 
        'card_name',
        'foreign_name',
        'address',
        'total_packages',
        'total_weight'
    ]
    
    processor = FileProcessor()
    assert all(col in processor.COLUMN_MAPPING for col in expected_columns)


def test_load_excel_file(sample_excel_file):
    """Test loading Excel file."""
    processor = FileProcessor()
    success = processor.load_source_file(sample_excel_file)
    
    assert success is True
    assert processor.source_data is not None
    assert len(processor.source_data) == 4  # From sample data


def test_filter_data_removes_negatives(sample_excel_file):
    """Test that filtering removes negative values."""
    processor = FileProcessor()
    processor.load_source_file(sample_excel_file)
    success = processor.filter_data()
    
    assert success is True
    assert processor.filtered_data is not None
    # Should have 2 rows after removing negatives
    assert len(processor.filtered_data) == 2


def test_get_business_licenses(sample_excel_file):
    """Test getting business license numbers."""
    processor = FileProcessor()
    processor.load_source_file(sample_excel_file)
    processor.filter_data()
    
    licenses = processor.get_business_licenses()
    assert len(licenses) == 2  # After filtering negatives
    assert '123456' in licenses
    assert '789012' in licenses


def test_save_intermediate_file(sample_excel_file, temp_dir):
    """Test saving intermediate file."""
    processor = FileProcessor()
    processor.load_source_file(sample_excel_file)
    processor.filter_data()
    
    output_path = temp_dir / "intermediate.xlsx"
    success = processor.save_intermediate_file(output_path)
    
    assert success is True
    assert output_path.exists()


def test_get_summary_stats(sample_excel_file):
    """Test getting summary statistics."""
    processor = FileProcessor()
    processor.load_source_file(sample_excel_file)
    processor.filter_data()
    
    stats = processor.get_summary_stats()
    
    assert stats['total_rows'] == 2
    assert stats['total_packages'] == 30  # 10 + 20
    assert stats['total_weight_kg'] == 300.5  # 100.5 + 200.0
    assert stats['unique_licenses'] == 2
