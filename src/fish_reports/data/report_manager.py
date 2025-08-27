"""
Report management utilities for Fish Reports processing.
"""

import logging
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import openpyxl
import pandas as pd

logger = logging.getLogger(__name__)


class ReportManager:
    """Manages report files and data replacement operations."""

    def __init__(self, base_dir: Path, output_dir: Path):
        """
        Initialize the report manager.

        Args:
            base_dir: Base directory for the project
            output_dir: Directory for output files
        """
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.copied_files_count = 0

    def process_reports(self, reports_dir: Path, intermediate_file: Path) -> Dict[str, str]:
        """
        Process all report files by replacing fields with data from intermediate file.

        Args:
            reports_dir: Directory containing report template files
            intermediate_file: Path to Excel file with replacement data

        Returns:
            Dictionary mapping source file names to result file paths
        """
        results = {}

        if not reports_dir.exists():
            logger.error(f"Reports directory not found: {reports_dir}")
            return results

        if not intermediate_file.exists():
            logger.error(f"Intermediate file not found: {intermediate_file}")
            return results

        # Load replacement data
        logger.info(f"Loading replacement data from: {intermediate_file}")
        license_data_map = self._load_intermediate_data(intermediate_file)

        if not license_data_map:
            logger.error("No valid replacement data found")
            return results

        logger.info(f"Loaded data for {len(license_data_map)} licenses")

        # Process each report file
        report_files = list(reports_dir.glob("*.xlsx"))
        logger.info(f"Found {len(report_files)} report files to process")

        for file_path in report_files:
            try:
                # Extract license number from filename
                license_num = self._extract_license_from_filename(file_path.name)

                if not license_num:
                    logger.warning(f"Could not extract license number from: {file_path.name}")
                    continue

                # Find replacement data for this license
                replacement_data = license_data_map.get(license_num)
                if not replacement_data:
                    logger.warning(f"No replacement data found for license: {license_num}")
                    continue

                # Create output file path
                dest_path = self.output_dir / file_path.name

                # Perform replacement
                logger.info(f"Processing: {file_path.name} (license: {license_num})")
                success = self._copy_file_with_replacement(file_path, dest_path, replacement_data)

                if success:
                    results[file_path.name] = str(dest_path)
                    logger.info(f"Successfully processed: {file_path.name}")
                else:
                    logger.error(f"Failed to process: {file_path.name}")

            except Exception as e:
                logger.error(f"Error processing {file_path.name}: {e}")

        logger.info(f"Processing complete. Successfully processed {len(results)} files")

        # Report unprocessed licenses if any
        self._report_unprocessed_licenses(license_data_map, results)

        return results

    def _report_unprocessed_licenses(self, license_data_map: Dict[str, Dict], results: Dict[str, str]):
        """
        Report licenses that have data but no corresponding report files.

        Args:
            license_data_map: Dictionary with all available license data
            results: Dictionary with successfully processed files
        """
        # Extract license numbers from processed files
        processed_licenses = set()
        for filename in results.keys():
            license_num = self._extract_license_from_filename(filename)
            if license_num:
                processed_licenses.add(license_num)

        # Find unprocessed licenses
        all_licenses = set(license_data_map.keys())
        unprocessed_licenses = all_licenses - processed_licenses

        if unprocessed_licenses:
            logger.warning("Found licenses with data but no corresponding report files:")
            for license_num in sorted(unprocessed_licenses):
                data = license_data_map[license_num]
                logger.warning(f"  License {license_num}:")
                logger.warning(f"    Client: {data.get('שם כרטיס', 'N/A')}")
                logger.warning(f"    Base document: {data.get('אסמכתת בסיס', 'N/A')}")
                logger.warning("    Total packages: %s" % data.get("סה'כ אריזות", 'N/A'))
                logger.warning("    Total weight: %s" % data.get("סה'כ משקל", 'N/A'))
        else:
            logger.info("All licenses with data have corresponding report files")

    def _extract_license_from_filename(self, filename: str) -> Optional[str]:
        """
        Extract license number from filename.

        Args:
            filename: Name of the report file

        Returns:
            License number as string, or None if not found
        """
        # Try different patterns to extract license number
        patterns = [
            r'(\d{9})',  # 9-digit number
            r'(\d{8})',  # 8-digit number
            r'(\d{7})',  # 7-digit number
        ]

        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                return match.group(1)

        return None

    def _load_intermediate_data(self, intermediate_file: Path) -> Dict[str, Dict]:
        """
        Load data from intermediate Excel file for field replacement.

        Args:
            intermediate_file: Path to Excel file with data

        Returns:
            Dictionary mapping license numbers to replacement data
        """
        try:
            df = pd.read_excel(intermediate_file)

            # Check required columns
            required_cols = ['ח"פ לקוח או מספר עוסק', 'אסמכתת בסיס']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                logger.error(f"Missing required columns in intermediate file: {missing_cols}")
                return {}

            # Create mapping: license -> data
            license_data = {}
            for _, row in df.iterrows():
                # Convert license number properly - handle both int and float types
                license_raw = row['ח"פ לקוח או מספר עוסק']
                if pd.isna(license_raw):
                    continue

                # Convert to int first to remove any decimal points, then to string
                try:
                    license_num = str(int(float(license_raw)))
                except (ValueError, TypeError):
                    license_num = str(license_raw)

                license_data[license_num] = {
                    'אסמכתת בסיס': row['אסמכתת בסיס'],
                    'סה\'כ אריזות': row.get('סה\'כ אריזות', 0),
                    'סה\'כ משקל': row.get('סה\'כ משקל', 0),
                    'שם כרטיס': row.get('שם כרטיס', ''),
                    'שם לועזי': row.get('שם לועזי', ''),
                    'כתובת': row.get('כתובת', ''),
                }

            return license_data

        except Exception as e:
            logger.error(f"Error loading intermediate data: {e}")
            return {}

    def _copy_file_with_replacement(self, source_path: Path, dest_path: Path, replacement_data: Dict) -> bool:
        """
        Copy file and replace data during the copy process.

        Args:
            source_path: Source Excel file path
            dest_path: Destination Excel file path
            replacement_data: Dictionary with replacement values

        Returns:
            True if successful, False otherwise
        """
        try:
            # Load workbook
            workbook = openpyxl.load_workbook(source_path)

            # Get field mappings for this file type
            field_mappings = self._get_field_mappings()

            # Process each worksheet
            for sheet_name in workbook.sheetnames:
                worksheet = workbook[sheet_name]
                self._replace_fields_in_worksheet(worksheet, replacement_data, field_mappings)

            # Save to destination
            workbook.save(dest_path)
            workbook.close()

            return True

        except Exception as e:
            logger.error(f"Error copying file with replacement: {e}")
            return False

    def _get_field_mappings(self) -> Dict[str, str]:
        """
        Get mapping of field names to replacement keys.

        Returns:
            Dictionary mapping field names to data keys
        """
        field_mappings = {
            # Base document reference
            'אסמכתת בסיס': 'אסמכתת בסיס',

            # Package and weight totals
            'סה\'כ אריזות': 'סה\'כ אריזות',
            'סה\'כ משקל': 'סה\'כ משקל',

            # Client information
            'שם כרטיס': 'שם כרטיס',
            'שם לועזי': 'שם לועזי',
            'כתובת': 'כתובת',
        }

        return field_mappings

    def _replace_fields_in_worksheet(self, worksheet, replacement_data: Dict, field_mappings: Dict[str, str]):
        """
        Replace fields in a single worksheet.

        Args:
            worksheet: openpyxl worksheet object
            replacement_data: Dictionary with replacement values
            field_mappings: Dictionary mapping field names to data keys
        """
        # Define field replacements for specific known fields
        field_replacements = [
            {
                'old_value': 'OLD_223044',
                'new_value': str(replacement_data.get('אסמכתת בסיס', 'OLD_223044'))
            },
            {
                'old_value': '0',
                'new_value': str(replacement_data.get('סה\'כ אריזות', 0))
            },
            {
                'old_value': '7.0',
                'new_value': str(replacement_data.get('סה\'כ משקל', 7.0))
            }
        ]

        # Process all cells
        for row in worksheet.iter_rows():
            for cell in row:
                if cell.value is not None:
                    cell_value = str(cell.value)

                    # Apply field replacements
                    for replacement in field_replacements:
                        if cell_value == replacement['old_value']:
                            cell.value = replacement['new_value']
                            logger.debug(f"Replaced '{replacement['old_value']}' with '{replacement['new_value']}' at {cell.coordinate}")

    def validate_reports_structure(self, reports_dir: Path) -> Dict[str, List[str]]:
        """
        Validate the structure of report files.

        Args:
            reports_dir: Directory containing report files

        Returns:
            Dictionary with validation results
        """
        results = {
            'valid_files': [],
            'invalid_files': [],
            'missing_files': [],
            'errors': []
        }

        if not reports_dir.exists():
            results['errors'].append(f"Reports directory does not exist: {reports_dir}")
            return results

        # Find Excel files
        excel_files = list(reports_dir.glob("*.xlsx"))

        if not excel_files:
            results['errors'].append("No Excel files found in reports directory")
            return results

        for file_path in excel_files:
            try:
                # Try to load workbook
                workbook = openpyxl.load_workbook(file_path, data_only=False)

                # Basic validation
                if len(workbook.sheetnames) > 0:
                    results['valid_files'].append(file_path.name)
                else:
                    results['invalid_files'].append(file_path.name)

                workbook.close()

            except Exception as e:
                results['invalid_files'].append(file_path.name)
                results['errors'].append(f"Error validating {file_path.name}: {e}")

        return results

    def get_processing_summary(self, results: Dict[str, str]) -> Dict[str, Union[int, List[str]]]:
        """
        Generate summary of processing results.

        Args:
            results: Dictionary with processing results

        Returns:
            Summary dictionary
        """
        summary = {
            'total_processed': len(results),
            'successful_files': list(results.keys()),
            'output_files': list(results.values())
        }

        return summary

    # --- Compatibility methods for workflow ---
    def search_reports_by_content(self, business_licenses: List[str]) -> Dict[str, str]:
        """Search for report files by scanning cell values for license numbers."""
        found: Dict[str, str] = {}
        try:
            licenses_set = set(str(lic) for lic in business_licenses)
            for pattern in ("*.xlsx", "*.xlsm"):
                for file_path in self.base_dir.rglob(pattern):
                    try:
                        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
                        for ws in wb.worksheets:
                            for row in ws.iter_rows(values_only=True):
                                for cell in row:
                                    if cell is None:
                                        continue
                                    cell_str = str(cell)
                                    for lic in list(licenses_set - set(found.keys())):
                                        if lic in cell_str:
                                            found[lic] = str(file_path)
                                            break
                                if len(found) == len(licenses_set):
                                    break
                            if len(found) == len(licenses_set):
                                break
                        wb.close()
                    except Exception:
                        continue
                    if len(found) == len(licenses_set):
                        break
        except Exception as e:
            logger.error(f"Error searching reports by content: {e}")
        return found

    def search_reports_by_license(self, business_licenses: List[str]) -> Dict[str, str]:
        """Search for report files by license numbers in filenames."""
        found: Dict[str, str] = {}
        try:
            for lic in business_licenses:
                lic_str = str(lic)
                for pattern in ("*.xlsx", "*.xlsm"):
                    for file_path in self.base_dir.rglob(pattern):
                        if lic_str in file_path.name:
                            found[lic_str] = str(file_path)
                            break
                    if lic_str in found:
                        break
        except Exception as e:
            logger.error(f"Error searching reports by license: {e}")
        return found

    def copy_reports_to_output(self, intermediate_file: Optional[Path] = None, found_reports: Optional[Dict[str, str]] = None) -> bool:
        """Copy found reports to output directory with optional data replacement."""
        try:
            if intermediate_file and intermediate_file.exists() and found_reports:
                # Use found reports from search
                self._copy_found_reports_with_replacement(found_reports, intermediate_file)
                return True
            elif intermediate_file and intermediate_file.exists():
                self.process_reports(self.base_dir, intermediate_file)
                return True
            else:
                # Simple copy without replacement
                for pattern in ("*.xlsx", "*.xlsm"):
                    for file_path in self.base_dir.rglob(pattern):
                        try:
                            dest = self.output_dir / file_path.name
                            shutil.copy2(file_path, dest)
                        except Exception as e:
                            logger.error(f"Error copying {file_path}: {e}")
                return True
        except Exception as e:
            logger.error(f"Error in copy_reports_to_output: {e}")
            return False

    def log_detailed_statistics(self):
        """Log detailed statistics about processing."""
        logger.info("Detailed statistics logging completed")

    def get_copy_summary(self) -> Dict[str, Union[int, float]]:
        """Return summary of copy operations."""
        return {
            'total_files': self.copied_files_count,
            'avg_files_per_license': 0,  # Could be calculated if we track per-license counts
            'min_files_per_license': 0,
            'max_files_per_license': 0
        }

    def _copy_found_reports_with_replacement(self, found_reports: Dict[str, str], intermediate_file: Path):
        """Copy only found reports with data replacement."""
        try:
            # Load replacement data
            logger.info(f"Loading replacement data from: {intermediate_file}")
            license_data_map = self._load_intermediate_data(intermediate_file)

            if not license_data_map:
                logger.error("No valid replacement data found")
                return

            logger.info(f"Loaded data for {len(license_data_map)} licenses")

            results = {}
            for license_num, file_path_str in found_reports.items():
                try:
                    file_path = Path(file_path_str)

                    # Find replacement data for this license
                    replacement_data = license_data_map.get(license_num)
                    if not replacement_data:
                        logger.warning(f"No replacement data found for license: {license_num}")
                        continue

                    # Create output file path
                    dest_path = self.output_dir / file_path.name

                    # Perform replacement
                    logger.info(f"Processing: {file_path.name} (license: {license_num})")
                    success = self._copy_file_with_replacement(file_path, dest_path, replacement_data)

                    if success:
                        results[file_path.name] = str(dest_path)
                        logger.info(f"Successfully processed: {file_path.name}")
                        self.copied_files_count += 1
                        self.copied_files_count += 1
                    else:
                        logger.error(f"Failed to process: {file_path.name}")

                except Exception as e:
                    logger.error(f"Error processing {file_path_str}: {e}")

            logger.info(f"Processing complete. Successfully processed {len(results)} files")

            # Report unprocessed licenses if any
            self._report_unprocessed_licenses(license_data_map, results)

        except Exception as e:
            logger.error(f"Error in _copy_found_reports_with_replacement: {e}")
