"""
City management utilities for Fish Reports processing.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class CityManager:
    """Manages city codes and validation for Fish Reports processing."""

    def __init__(self, cities_file_path: Optional[Path] = None):
        """
        Initialize the city manager.

        Args:
            cities_file_path: Path to Excel file with city codes
        """
        self.cities_file_path = cities_file_path or Path(__file__).parent.parent.parent.parent / "cities" / "רשימת יישובים מעודכנת 21.4.24.xlsx"
        self.city_codes: Dict[str, str] = {}
        self.code_to_city: Dict[str, str] = {}
        self._load_city_data()

    def _load_city_data(self):
        """Load city codes from Excel file."""
        try:
            if not self.cities_file_path.exists():
                logger.warning(f"City codes file not found: {self.cities_file_path}")
                return

            df = pd.read_excel(self.cities_file_path)

            # Check required columns
            required_cols = ['שם רשות', 'קוד רשות']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                logger.error(f"Missing required columns in cities file: {missing_cols}")
                return

            # Create mappings
            for _, row in df.iterrows():
                city_name = str(row['שם רשות']).strip()
                city_code = str(row['קוד רשות']).strip()

                if city_name and city_code:
                    self.city_codes[city_name] = city_code
                    self.code_to_city[city_code] = city_name

            logger.info(f"Loaded {len(self.city_codes)} city codes from {self.cities_file_path}")

        except Exception as e:
            logger.error(f"Error loading city data: {e}")

    def extract_city_from_address(self, full_address: str) -> Optional[str]:
        """
        Extract city name from full address.

        Args:
            full_address: Full address string (e.g., "אשדוד, העצמאות 87")

        Returns:
            City name or None if not found
        """
        if not full_address or not isinstance(full_address, str):
            return None

        # Split by comma and take the first part (city name)
        parts = full_address.split(',', 1)
        city_name = parts[0].strip()

        # Clean up common prefixes/suffixes that might not be in the official list
        city_name = city_name.replace('א.', '').replace('ע.', '').strip()

        return city_name if city_name else None

    def get_city_code(self, city_name: str) -> Optional[str]:
        """
        Get city code for a given city name.

        Args:
            city_name: City name in Hebrew

        Returns:
            City code or None if not found
        """
        if not city_name:
            return None

        # Direct lookup
        if city_name in self.city_codes:
            return self.city_codes[city_name]

        # Try case-insensitive search
        city_name_lower = city_name.lower()
        for name, code in self.city_codes.items():
            if name.lower() == city_name_lower:
                return code

        # Try partial match (first few characters)
        for name, code in self.city_codes.items():
            if name.lower().startswith(city_name_lower[:3]):
                logger.info(f"Partial city match: '{city_name}' -> '{name}' (code: {code})")
                return code

        logger.warning(f"City code not found for: '{city_name}'")
        return None

    def get_city_name(self, city_code: str) -> Optional[str]:
        """
        Get city name for a given city code.

        Args:
            city_code: City code

        Returns:
            City name or None if not found
        """
        return self.code_to_city.get(city_code)

    def validate_city_match(self, address_city: str, report_city_code: Optional[str]) -> bool:
        """
        Validate if address city matches the report city code.

        Args:
            address_city: City name from address
            report_city_code: City code from report

        Returns:
            True if cities match, False otherwise
        """
        if not address_city or not report_city_code:
            return False

        # Get city code for the address city
        address_city_code = self.get_city_code(address_city)

        if not address_city_code:
            logger.warning(f"Could not find city code for address city: '{address_city}'")
            return False

        # Compare codes (case-insensitive)
        match = address_city_code.lower() == report_city_code.lower()

        if match:
            logger.info(f"City match: '{address_city}' ({address_city_code}) == '{report_city_code}'")
        else:
            logger.warning(f"City mismatch: '{address_city}' ({address_city_code}) != '{report_city_code}'")

        return match

    def get_city_code_by_name(self, city_name: str) -> Optional[str]:
        """
        Alias for get_city_code for backward compatibility.

        Args:
            city_name: City name in Hebrew

        Returns:
            City code or None if not found
        """
        return self.get_city_code(city_name)

    def is_valid_city_code(self, city_code: str) -> bool:
        """
        Check if a city code is valid.

        Args:
            city_code: City code to validate

        Returns:
            True if valid, False otherwise
        """
        return city_code in self.code_to_city
        return self.city_codes.copy()

    def get_all_cities(self) -> Dict[str, str]:
        """Get all available cities with their codes."""
        return self.code_to_city.copy()
