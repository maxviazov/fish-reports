"""
Entry point for the Fish Reports application.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def main():
    """Main entry point for the application."""
    from fish_reports.gui.main_window import FishReportsApp
    
    app = FishReportsApp()
    app.run()

if __name__ == "__main__":
    main()
