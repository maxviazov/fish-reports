"""
File processing utilities for Fish Reports.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class FileProcessor:
    """Handles processing of source files and filtering data."""

    # Column names in Hebrew
    COLUMN_MAPPING = {
        'business_license': 'מספר עוסק מורשה',
        'base_document': 'אסמכתת בסיס',  # Internal name (backward compatibility)
        'base_reference': 'אסמכתת בסיס',  # Alias expected by tests
        'card_name': 'שם כרטיס',
        'foreign_name': 'שם לועזי',
        'address': 'כתובת',
        'total_packages': 'סה\'כ אריזות',
        'total_weight': 'סה\'כ משקל'
    }

    def __init__(self):
        """Initialize the file processor."""
        self.source_data: Optional[pd.DataFrame] = None
        self.filtered_data: Optional[pd.DataFrame] = None

    def load_source_file(self, file_path: Path) -> bool:
        """
        Load the source file.

        Args:
            file_path: Path to the source file

        Returns:
            True if successful, False otherwise
        """
        try:
            if file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.source_data = pd.read_excel(file_path)
            elif file_path.suffix.lower() == '.csv':
                self.source_data = pd.read_csv(file_path)
            else:
                logger.error(f"Unsupported file format: {file_path.suffix}")
                return False

            logger.info(f"Loaded source file: {file_path}")
            logger.info(f"Data shape: {self.source_data.shape}")
            return True

        except Exception as e:
            logger.error(f"Error loading source file {file_path}: {e}")
            return False

    def filter_data(self) -> bool:
        """
        Filter the source data according to requirements.

        Returns:
            True if successful, False otherwise
        """
        if self.source_data is None:
            logger.error("No source data loaded")
            return False

        try:
            # Get required columns (ensure uniqueness in order to avoid duplicate base document columns
            # because we now have aliases 'base_document' and 'base_reference' pointing to the same Hebrew header)
            seen = set()
            required_columns: List[str] = []
            for col in self.COLUMN_MAPPING.values():
                if col not in seen:
                    seen.add(col)
                    required_columns.append(col)

            # Check if all required columns exist
            missing_columns = [col for col in required_columns
                             if col not in self.source_data.columns]
            if missing_columns:
                logger.error(f"Missing columns: {missing_columns}")
                return False

            # Select only required columns
            self.filtered_data = self.source_data[required_columns].copy()

            # Remove rows with negative values in packages and weight columns
            packages_col = self.COLUMN_MAPPING['total_packages']
            weight_col = self.COLUMN_MAPPING['total_weight']

            # Convert to numeric, replacing non-numeric values with NaN
            self.filtered_data[packages_col] = pd.to_numeric(
                self.filtered_data[packages_col], errors='coerce'
            )
            self.filtered_data[weight_col] = pd.to_numeric(
                self.filtered_data[weight_col], errors='coerce'
            )

            # Remove rows with negative values
            initial_count = len(self.filtered_data)
            self.filtered_data = self.filtered_data[
                (self.filtered_data[packages_col] >= 0) &
                (self.filtered_data[weight_col] >= 0)
            ]
            removed_count = initial_count - len(self.filtered_data)

            logger.info(f"Removed {removed_count} rows with negative values")
            logger.info(f"Filtered data shape: {self.filtered_data.shape}")

            return True

        except Exception as e:
            logger.error(f"Error filtering data: {e}")
            return False

    def convert_to_kilograms(self) -> bool:
        """
        Convert weight values from grams to kilograms.

        Returns:
            True if successful, False otherwise
        """
        if self.filtered_data is None:
            logger.error("No filtered data available")
            return False

        try:
            weight_col = self.COLUMN_MAPPING['total_weight']

            # Convert weights from grams to kilograms (divide by 1000)
            original_weights = self.filtered_data[weight_col].copy()
            self.filtered_data[weight_col] = self.filtered_data[weight_col] / 1000.0

            # Log conversion details
            total_original = original_weights.sum()
            total_converted = self.filtered_data[weight_col].sum()

            logger.info(f"Конвертация весов: {total_original:.0f}г -> {total_converted:.2f}кг")
            logger.info("Weight conversion from grams to kilograms completed")
            return True

        except Exception as e:
            logger.error(f"Error converting weights: {e}")
            return False

    def group_by_base_document(self) -> bool:
        """
        Group data by base document (אסמכתת בסיס) AND address to preserve separate entries for each address.

        Returns:
            True if successful, False otherwise
        """
        if self.filtered_data is None:
            logger.error("No filtered data to group")
            return False

        try:
            base_doc_col = self.COLUMN_MAPPING['base_document']
            packages_col = self.COLUMN_MAPPING['total_packages']
            weight_col = self.COLUMN_MAPPING['total_weight']
            business_license_col = self.COLUMN_MAPPING['business_license']
            address_col = self.COLUMN_MAPPING['address']

            logger.info(f"Grouping data by {base_doc_col} and {address_col}")

            # Group by base document AND address to preserve separate entries for each address
            # This ensures each address gets its own report file
            groupby_cols = [base_doc_col, address_col]

            # Group by base document and address, sum packages and weight
            # Keep other important columns (take first value from group)
            aggregation = {
                packages_col: 'sum',
                weight_col: 'sum',
                business_license_col: 'first',  # Keep license number
                'שם כרטיס': 'first',  # Keep business name
                'שם לועזי': 'first',  # Keep foreign name
            }

            # Add any other columns that exist (take first value)
            for col in self.filtered_data.columns:
                if col not in aggregation and col not in groupby_cols:
                    aggregation[col] = 'first'

            grouped_data = self.filtered_data.groupby(groupby_cols).agg(aggregation).reset_index()

            logger.info(f"Grouped {len(self.filtered_data)} rows into {len(grouped_data)} groups by document + address")
            logger.info(f"Total packages after grouping: {grouped_data[packages_col].sum():.2f}")
            logger.info(f"Total weight after grouping: {grouped_data[weight_col].sum():.2f} kg")

            # Update the filtered data with grouped results
            self.filtered_data = grouped_data

            return True

        except Exception as e:
            logger.error(f"Error grouping data by base document and address: {e}")
            return False

    def save_intermediate_file(self, output_path: Path) -> bool:
        """
        Save the filtered data to an intermediate file.

        Args:
            output_path: Path where to save the intermediate file

        Returns:
            True if successful, False otherwise
        """
        if self.filtered_data is None:
            logger.error("No filtered data to save")
            return False

        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create a copy for saving with standardized column names
            data_to_save = self.filtered_data.copy()

            # License column is already in the correct format
            # No need to rename since all components use the same column name

            # Save to Excel format
            data_to_save.to_excel(output_path, index=False)

            logger.info(f"Saved intermediate file: {output_path}")
            logger.info(f"Columns in saved file: {list(data_to_save.columns)}")
            return True

        except Exception as e:
            logger.error(f"Error saving intermediate file {output_path}: {e}")
            return False

    def get_business_licenses(self) -> List[str]:
        """
        Get list of unique business license numbers.

        Returns:
            List of business license numbers
        """
        if self.filtered_data is None:
            return []

        license_col = self.COLUMN_MAPPING['business_license']
        licenses = self.filtered_data[license_col].dropna().unique().tolist()
        # Convert to string and remove '.0' suffix for float numbers
        license_strings = []
        for license in licenses:
            license_str = str(license)
            if license_str.endswith('.0'):
                license_str = license_str[:-2]
            license_strings.append(license_str)
        return license_strings

    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics of the filtered data.

        Returns:
            Dictionary with summary statistics
        """
        if self.filtered_data is None:
            return {}

        packages_col = self.COLUMN_MAPPING['total_packages']
        weight_col = self.COLUMN_MAPPING['total_weight']

        return {
            'total_rows': len(self.filtered_data),
            'total_packages': self.filtered_data[packages_col].sum(),
            'total_weight_kg': self.filtered_data[weight_col].sum(),
            'unique_licenses': len(self.get_business_licenses())
        }
