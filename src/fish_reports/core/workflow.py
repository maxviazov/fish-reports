"""
Core workflow for Fish Reports processing.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
import threading

from fish_reports.data.file_processor import FileProcessor
from fish_reports.data.report_manager import ReportManager
from fish_reports.utils.file_utils import (
    validate_file_path, create_directory_if_not_exists
)


logger = logging.getLogger(__name__)


class FishReportsWorkflow:
    """Main workflow orchestrator for Fish Reports processing."""
    
    def __init__(self, gui_callback=None):
        """
        Initialize the workflow.
        
        Args:
            gui_callback: Callback function for GUI updates
        """
        self.gui_callback = gui_callback
        self.file_processor = FileProcessor()
        self.report_manager = None
        
        # Paths
        self.source_file: Optional[Path] = None
        self.intermediate_dir: Optional[Path] = None
        self.reports_dir: Optional[Path] = None
        self.output_dir: Optional[Path] = None
        
        # Results
        self.processing_results: Dict[str, Any] = {}
        
    def set_paths(self, source_file: Path, intermediate_dir: Path, 
                  reports_dir: Path, output_dir: Path) -> bool:
        """
        Set all required paths for processing.
        
        Args:
            source_file: Path to source Excel/CSV file
            intermediate_dir: Directory for intermediate files
            reports_dir: Directory with existing reports
            output_dir: Directory for output files
            
        Returns:
            True if all paths are valid, False otherwise
        """
        try:
            # Validate source file
            if not validate_file_path(source_file):
                self._log_error(f"Исходный файл не найден или недоступен: {source_file}")
                return False
            
            # Validate and create directories
            for dir_path, name in [
                (intermediate_dir, "промежуточных файлов"),
                (reports_dir, "отчетов"),
                (output_dir, "результатов")
            ]:
                if not create_directory_if_not_exists(dir_path):
                    self._log_error(f"Не удается создать папку {name}: {dir_path}")
                    return False
            
            # Set paths
            self.source_file = source_file
            self.intermediate_dir = intermediate_dir
            self.reports_dir = reports_dir
            self.output_dir = output_dir
            
            # Initialize report manager
            self.report_manager = ReportManager(reports_dir, output_dir)
            
            self._log_info("Все пути успешно установлены")
            return True
            
        except Exception as e:
            self._log_error(f"Ошибка при установке путей: {e}")
            return False
    
    def process_files(self) -> bool:
        """
        Execute the complete file processing workflow.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self._validate_setup():
                return False
            
            self._log_info("Начинаем обработку файлов...")
            
            # Step 1: Load source file
            if not self._load_source_file():
                return False
            
            # Step 2: Filter and process data
            if not self._process_data():
                return False
            
            # Step 3: Save intermediate file
            if not self._save_intermediate_file():
                return False
            
            # Step 4: Search and copy reports
            if not self._process_reports():
                return False
            
            # Step 5: Generate summary
            self._generate_summary()
            
            self._log_info("Обработка файлов завершена успешно!")
            return True
            
        except Exception as e:
            self._log_error(f"Критическая ошибка при обработке: {e}")
            return False
    
    def process_files_async(self, completion_callback=None):
        """
        Execute file processing in a separate thread.
        
        Args:
            completion_callback: Function to call when processing is complete
        """
        def worker():
            try:
                success = self.process_files()
                if completion_callback:
                    completion_callback(success)
            except Exception as e:
                self._log_error(f"Ошибка в асинхронной обработке: {e}")
                if completion_callback:
                    completion_callback(False)
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def _validate_setup(self) -> bool:
        """Validate that all required components are set up."""
        if not all([self.source_file, self.intermediate_dir, 
                   self.reports_dir, self.output_dir]):
            self._log_error("Не все пути установлены")
            return False
        
        if not self.report_manager:
            self._log_error("ReportManager не инициализирован")
            return False
        
        return True
    
    def _load_source_file(self) -> bool:
        """Load and validate the source file."""
        if not self.source_file:
            self._log_error("Источник файла не установлен")
            return False
            
        self._log_info(f"Загружаем исходный файл: {self.source_file.name}")
        
        success = self.file_processor.load_source_file(self.source_file)
        if not success:
            self._log_error("Ошибка при загрузке исходного файла")
            return False
        
        # Log file info
        if self.file_processor.source_data is not None:
            rows, cols = self.file_processor.source_data.shape
            self._log_info(f"Загружено строк: {rows}, столбцов: {cols}")
        
        return True
    
    def _process_data(self) -> bool:
        """Filter and process the loaded data."""
        self._log_info("Фильтруем данные...")
        
        # Filter data (remove negative values)
        if not self.file_processor.filter_data():
            self._log_error("Ошибка при фильтрации данных")
            return False
        
        # Convert weights to kilograms if needed
        if not self.file_processor.convert_to_kilograms():
            self._log_error("Ошибка при конвертации весов")
            return False

        # Group data by base document and sum values
        if not self.file_processor.group_by_base_document():
            self._log_error("Ошибка при группировке данных")
            return False

        # Log processing results
        if self.file_processor.filtered_data is not None:
            processed_rows = len(self.file_processor.filtered_data)
            self._log_info(f"После обработки осталось строк: {processed_rows}")
        
        return True
    
    def _save_intermediate_file(self) -> bool:
        """Save the processed data to intermediate file."""
        if not self.intermediate_dir:
            self._log_error("Папка для промежуточных файлов не установлена")
            return False
            
        intermediate_file = self.intermediate_dir / "filtered_data.xlsx"
        self._log_info(f"Сохраняем промежуточный файл: {intermediate_file.name}")
        
        success = self.file_processor.save_intermediate_file(intermediate_file)
        if not success:
            self._log_error("Ошибка при сохранении промежуточного файла")
            return False
        
        self._log_info("Промежуточный файл успешно сохранен")
        return True
    
    def _process_reports(self) -> bool:
        """Search for and process report files."""
        if not self.report_manager:
            self._log_error("ReportManager не инициализирован")
            return False
            
        # Get business license numbers
        business_licenses = self.file_processor.get_business_licenses()
        if not business_licenses:
            self._log_warning("Не найдено номеров лицензий для поиска отчетов")
            return True
        
        self._log_info(f"Ищем отчеты для {len(business_licenses)} лицензий...")
        
        # Search for reports
        found_reports = self.report_manager.search_reports_by_license(business_licenses)
        
        if not found_reports:
            self._log_warning("Не найдено ни одного отчета")
            return True
        
        # Copy found reports
        if not self.report_manager.copy_reports_to_output():
            self._log_error("Ошибка при копировании отчетов")
            return False
        
        self._log_info(f"Скопировано отчетов для {len(found_reports)} лицензий")
        return True
    
    def _generate_summary(self):
        """Generate processing summary."""
        try:
            stats = self.file_processor.get_summary_stats()
            copy_stats = self.report_manager.get_copy_summary() if self.report_manager else {}
            
            intermediate_file_path = ""
            if self.intermediate_dir:
                intermediate_file_path = str(self.intermediate_dir / "filtered_data.xlsx")
            
            self.processing_results = {
                **stats,
                **copy_stats,
                'source_file': str(self.source_file) if self.source_file else "",
                'intermediate_file': intermediate_file_path,
                'output_directory': str(self.output_dir) if self.output_dir else ""
            }
            
            # Log summary
            self._log_info("=" * 50)
            self._log_info("СВОДКА ОБРАБОТКИ:")
            self._log_info(f"Обработано строк: {stats.get('total_rows', 0)}")
            self._log_info(f"Общий вес (кг): {stats.get('total_weight_kg', 0):.2f}")
            self._log_info(f"Общее количество упаковок: {stats.get('total_packages', 0)}")
            self._log_info(f"Найдено лицензий: {stats.get('unique_licenses', 0)}")
            self._log_info(f"Скопировано файлов отчетов: {copy_stats.get('total_files', 0)}")
            self._log_info("=" * 50)
            
        except Exception as e:
            self._log_error(f"Ошибка при создании сводки: {e}")
    
    def _log_info(self, message: str):
        """Log info message."""
        logger.info(message)
        if self.gui_callback:
            self.gui_callback(f"INFO: {message}")
    
    def _log_warning(self, message: str):
        """Log warning message."""
        logger.warning(message)
        if self.gui_callback:
            self.gui_callback(f"WARNING: {message}")
    
    def _log_error(self, message: str):
        """Log error message."""
        logger.error(message)
        if self.gui_callback:
            self.gui_callback(f"ERROR: {message}")
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results."""
        return self.processing_results.copy()
