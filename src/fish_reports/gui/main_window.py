"""
Main GUI window for Fish Reports application.
"""

import json
import logging
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from ttkthemes import ThemedTk

from fish_reports.core.workflow import FishReportsWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class FishReportsApp:
    """Main application window for Fish Reports processing."""

    def __init__(self):
        """Initialize the application."""
        self.root = ThemedTk(theme="arc")
        self.root.title("Fish Reports Processing System")
        self.root.geometry("800x600")

        # Настройка стиля
        self.style = ttk.Style()
        self.style.configure('TLabelframe', padding=10)
        self.style.configure('TLabelframe.Label', font=('Arial', 10, 'bold'))
        self.style.configure('TButton', padding=5)
        self.style.configure('Primary.TButton', padding=6)
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))

        # Directory paths
        self.source_file: Optional[Path] = None
        self.intermediate_dir: Optional[Path] = None
        self.reports_dir: Optional[Path] = None
        self.output_dir: Optional[Path] = None

        # Workflow
        self.workflow = FishReportsWorkflow(gui_callback=self._log_message)

        self._create_widgets()
        self._setup_layout()

        # Load saved configuration
        self._load_configuration()

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")

        # Title
        self.title_label = ttk.Label(
            self.main_frame,
            text="Система обработки отчетов о рыбе",
            style="Title.TLabel"
        )

        # Directory selection frame
        self.dirs_frame = ttk.LabelFrame(
            self.main_frame,
            text="Выбор директорий",
            padding="10"
        )

        # Source directory
        self.source_label = ttk.Label(self.dirs_frame, text="Исходный файл:")
        self.source_var = tk.StringVar()
        self.source_entry = ttk.Entry(
            self.dirs_frame,
            textvariable=self.source_var,
            width=50,
            state="readonly"
        )
        self.source_button = ttk.Button(
            self.dirs_frame,
            text="Выбрать...",
            command=self._select_source_file
        )

        # Intermediate directory
        self.intermediate_label = ttk.Label(
            self.dirs_frame,
            text="Промежуточные файлы:"
        )
        self.intermediate_var = tk.StringVar()
        self.intermediate_entry = ttk.Entry(
            self.dirs_frame,
            textvariable=self.intermediate_var,
            width=50,
            state="readonly"
        )
        self.intermediate_button = ttk.Button(
            self.dirs_frame,
            text="Выбрать...",
            command=self._select_intermediate_dir
        )

        # Reports directory
        self.reports_label = ttk.Label(self.dirs_frame, text="Файлы отчетов:")
        self.reports_var = tk.StringVar()
        self.reports_entry = ttk.Entry(
            self.dirs_frame,
            textvariable=self.reports_var,
            width=50,
            state="readonly"
        )
        self.reports_button = ttk.Button(
            self.dirs_frame,
            text="Выбрать...",
            command=self._select_reports_dir
        )

        # Output directory
        self.output_label = ttk.Label(
            self.dirs_frame,
            text="Копии для משרד הבריאות:"
        )
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(
            self.dirs_frame,
            textvariable=self.output_var,
            width=50,
            state="readonly"
        )
        self.output_button = ttk.Button(
            self.dirs_frame,
            text="Выбрать...",
            command=self._select_output_dir
        )

        # Progress frame
        self.progress_frame = ttk.LabelFrame(
            self.main_frame,
            text="Прогресс обработки",
            padding="10"
        )

        self.progress_var = tk.StringVar(value="Готов к работе")
        self.progress_label = ttk.Label(
            self.progress_frame,
            textvariable=self.progress_var
        )

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode="indeterminate"
        )

        # Log frame
        self.log_frame = ttk.LabelFrame(
            self.main_frame,
            text="Лог операций",
            padding="10"
        )

        self.log_text = tk.Text(
            self.log_frame,
            height=10,
            wrap=tk.WORD
        )

        self.log_scrollbar = ttk.Scrollbar(
            self.log_frame,
            orient="vertical",
            command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)

        # Buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)

        self.process_button = ttk.Button(
            self.buttons_frame,
            text="Начать обработку",
            command=self._start_processing,
            state="disabled",
            style="Primary.TButton"
        )

        self.clear_button = ttk.Button(
            self.buttons_frame,
            text="Очистить лог",
            command=self._clear_log
        )

        self.exit_button = ttk.Button(
            self.buttons_frame,
            text="Выход",
            command=self.root.quit
        )

    def _setup_layout(self):
        """Setup the layout of widgets."""
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Title
        self.title_label.grid(row=0, column=0, pady=(0, 20))

        # Directories frame
        self.dirs_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.dirs_frame.columnconfigure(1, weight=1)

        # Source file
        self.source_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.source_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.source_button.grid(row=0, column=2)

        # Intermediate directory
        self.intermediate_label.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.intermediate_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(10, 0))
        self.intermediate_button.grid(row=1, column=2, pady=(10, 0))

        # Reports directory
        self.reports_label.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.reports_entry.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady=(10, 0))
        self.reports_button.grid(row=2, column=2, pady=(10, 0))

        # Output directory
        self.output_label.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.output_entry.grid(row=3, column=1, sticky="ew", padx=(0, 10), pady=(10, 0))
        self.output_button.grid(row=3, column=2, pady=(10, 0))

        # Progress frame
        self.progress_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.progress_frame.columnconfigure(0, weight=1)

        self.progress_label.grid(row=0, column=0, sticky="w")
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(5, 0))

        # Log frame
        self.log_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)

        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_scrollbar.grid(row=0, column=1, sticky="ns")

        # Buttons frame
        self.buttons_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))

        self.process_button.grid(row=0, column=0, padx=(0, 10))
        self.clear_button.grid(row=0, column=1, padx=(0, 10))
        self.exit_button.grid(row=0, column=2)

    def _select_source_file(self):
        """Select source file."""
        filename = filedialog.askopenfilename(
            title="Выберите исходный файл",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.source_var.set(filename)
            self.source_file = Path(filename)
            self._log_message(f"Выбран исходный файл: {filename}")
            self._save_configuration()
            self._check_ready()

    def _select_intermediate_dir(self):
        """Select intermediate directory."""
        dirname = filedialog.askdirectory(
            title="Выберите папку для промежуточных файлов"
        )
        if dirname:
            self.intermediate_var.set(dirname)
            self.intermediate_dir = Path(dirname)
            self._log_message(f"Выбрана папка для промежуточных файлов: {dirname}")
            self._save_configuration()
            self._check_ready()

    def _select_reports_dir(self):
        """Select reports directory."""
        dirname = filedialog.askdirectory(
            title="Выберите папку с файлами отчетов"
        )
        if dirname:
            self.reports_var.set(dirname)
            self.reports_dir = Path(dirname)
            self._log_message(f"Выбрана папка с файлами отчетов: {dirname}")
            self._save_configuration()
            self._check_ready()

    def _select_output_dir(self):
        """Select output directory."""
        dirname = filedialog.askdirectory(
            title="Выберите папку для копий отчетов"
        )
        if dirname:
            self.output_var.set(dirname)
            self.output_dir = Path(dirname)
            self._log_message(f"Выбрана папка для копий отчетов: {dirname}")
            self._save_configuration()
            self._check_ready()

    def _check_ready(self):
        """Check if all directories are selected and enable processing."""
        if all([
            self.source_file,
            self.intermediate_dir,
            self.reports_dir,
            self.output_dir
        ]):
            self.process_button.configure(state="normal")
            self._log_message("Все папки выбраны. Готов к обработке.")
        else:
            self.process_button.configure(state="disabled")

    def _start_processing(self):
        """Start the processing workflow."""
        try:
            # Validate all paths are set
            if not all([self.source_file, self.intermediate_dir, self.reports_dir, self.output_dir]):
                messagebox.showerror("Ошибка", "Не все пути выбраны")
                return

            self._log_message("Начинаем обработку файлов...")
            self.progress_var.set("Настройка обработки...")
            self.progress_bar.start()

            # Clear directories before processing
            self._clear_directories()

            # Disable the process button to prevent multiple runs
            self.process_button.configure(state="disabled")            # Set up workflow paths
            if not all([self.source_file, self.intermediate_dir, self.reports_dir, self.output_dir]):
                self._log_message("ОШИБКА: Не все пути установлены")
                self._finish_processing(False)
                return

            success = self.workflow.set_paths(
                self.source_file,  # type: ignore
                self.intermediate_dir,  # type: ignore
                self.reports_dir,  # type: ignore
                self.output_dir  # type: ignore
            )

            if not success:
                self._finish_processing(False)
                return

            # Start processing asynchronously
            self.workflow.process_files_async(self._finish_processing)

        except Exception as e:
            self._log_message(f"ОШИБКА: {e}")
            self._finish_processing(False)

    def _finish_processing(self, success: bool):
        """Finish processing and show results."""
        self.progress_bar.stop()
        self.process_button.configure(state="normal")

        if success:
            self.progress_var.set("Обработка завершена успешно")
            self._log_message("Обработка файлов завершена успешно!")

            # Show results summary
            results = self.workflow.get_results()
            if results:
                summary = f"""Результаты обработки:
• Обработано строк: {results.get('total_rows', 0)}
• Общий вес (кг): {results.get('total_weight_kg', 0):.2f}
• Общее количество упаковок: {results.get('total_packages', 0)}
• Найдено лицензий: {results.get('unique_licenses', 0)}
• Скопировано файлов отчетов: {results.get('total_files', 0)}

Результаты сохранены в: {results.get('output_directory', '')}"""
                messagebox.showinfo("Обработка завершена", summary)
            else:
                messagebox.showinfo("Готово", "Обработка файлов завершена успешно!")
        else:
            self.progress_var.set("Ошибка при обработке")
            self._log_message("Обработка завершена с ошибками!")
            messagebox.showerror("Ошибка", "Произошла ошибка при обработке файлов. Проверьте лог для деталей.")

    def _clear_log(self):
        """Clear the log text."""
        self.log_text.delete(1.0, tk.END)

    def _log_message(self, message: str):
        """Add a message to the log."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def _load_configuration(self):
        """Load saved configuration."""
        try:
            config_file = Path.home() / ".fish_reports_gui_config.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # Set paths from config
                if config.get('source_file'):
                    self.source_file = Path(config['source_file'])
                    self.source_var.set(str(self.source_file))

                if config.get('intermediate_dir'):
                    self.intermediate_dir = Path(config['intermediate_dir'])
                    self.intermediate_var.set(str(self.intermediate_dir))

                if config.get('reports_dir'):
                    self.reports_dir = Path(config['reports_dir'])
                    self.reports_var.set(str(self.reports_dir))

                if config.get('output_dir'):
                    self.output_dir = Path(config['output_dir'])
                    self.output_var.set(str(self.output_dir))

                self._log_message("Конфигурация загружена")
                self._check_ready()
        except Exception as e:
            self._log_message(f"Не удалось загрузить конфигурацию: {e}")

    def _save_configuration(self):
        """Save current configuration."""
        try:
            config = {
                'source_file': str(self.source_file) if self.source_file else "",
                'intermediate_dir': str(self.intermediate_dir) if self.intermediate_dir else "",
                'reports_dir': str(self.reports_dir) if self.reports_dir else "",
                'output_dir': str(self.output_dir) if self.output_dir else ""
            }

            config_file = Path.home() / ".fish_reports_gui_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            self._log_message("Конфигурация сохранена")
        except Exception as e:
            self._log_message(f"Не удалось сохранить конфигурацию: {e}")

    def _clear_directories(self):
        """Clear intermediate and output directories before processing."""
        try:
            # Clear intermediate directory
            if self.intermediate_dir and self.intermediate_dir.exists():
                self._log_message("Очищаем директорию промежуточных файлов...")
                for file_path in self.intermediate_dir.glob("*"):
                    if file_path.is_file():
                        file_path.unlink()
                self._log_message("Директория промежуточных файлов очищена")

            # Clear output directory
            if self.output_dir and self.output_dir.exists():
                self._log_message("Очищаем директорию итоговых отчетов...")
                for file_path in self.output_dir.glob("*"):
                    if file_path.is_file():
                        file_path.unlink()
                self._log_message("Директория итоговых отчетов очищена")

        except Exception as e:
            self._log_message(f"Ошибка при очистке директорий: {e}")

    def run(self):
        """Run the application main loop."""
        self._log_message("Приложение запущено. Выберите необходимые папки для начала работы.")
        self.root.mainloop()


if __name__ == '__main__':
    app = FishReportsApp()
    app.run()
