"""
Test configuration and fixtures.
"""

import pytest
from pathlib import Path
import tempfile
import pandas as pd


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = {
        'מספר עוסק מורשה': ['123456', '789012', '345678', '901234'],
        'אסמכתת בסיס': ['REF001', 'REF002', 'REF003', 'REF004'],
        'שם כרטיס': ['Company A', 'Company B', 'Company C', 'Company D'],
        'שם לועזי': ['Company A Ltd', 'Company B Inc', 'Company C Corp', 'Company D LLC'],
        'כתובת': ['Address 1', 'Address 2', 'Address 3', 'Address 4'],
        'סה\'כ אריזות': [10, 20, -5, 15],  # One negative value
        'סה\'כ משקל': [100.5, 200.0, -50.0, 150.25]  # One negative value
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_excel_file(temp_dir, sample_data):
    """Create a sample Excel file for testing."""
    file_path = temp_dir / "test_source.xlsx"
    sample_data.to_excel(file_path, index=False)
    return file_path
