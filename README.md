# Stat Manager

A comprehensive baseball/softball league management application built with Python and PySide6.

## Features

- **League Management**: Track teams, players, and league statistics
- **Player Statistics**: Manage batting and pitching statistics
- **Data Persistence**: SQLite database with CSV export/import
- **Visualization**: Interactive charts and graphs
- **Modern UI**: Clean, responsive interface with custom themes

## Project Structure

```
stat_man_g/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
│
├── src/                     # Main source code
│   ├── core/                # Core business logic
│   │   ├── linked_list.py   # League data structure
│   │   ├── team.py          # Team class
│   │   ├── player.py        # Player and Pitcher classes
│   │   ├── node.py          # Linked list node
│   │   ├── game.py          # Game logic
│   │   └── stack.py         # Stack data structure
│   │
│   ├── ui/                  # User interface components
│   │   ├── main_window.py   # Main application window
│   │   ├── dialogs/         # Dialog windows
│   │   ├── views/           # Main view components
│   │   └── styles/          # Application styles
│   │
│   ├── data/                # Data operations
│   │   ├── load/            # CSV loading functionality
│   │   ├── save/            # Database and CSV export
│   │   └── database/        # Database utilities
│   │
│   ├── visualization/       # Charts and graphs
│   ├── utils/               # Utility functions
│   └── config/              # Configuration
│
├── data/                    # Runtime data
│   ├── database/            # SQLite database
│   ├── exports/             # CSV exports
│   └── images/              # User images
│
├── assets/                  # Static assets
│   └── icons/               # Application icons
│
├── tests/                   # Unit tests
├── docs/                    # Documentation
└── archive/                 # Archived/deprecated code
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd stat_man_g
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Linux/Mac
   # or
   myenv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

### Key Features

#### League Management
- Create and manage teams
- Add players with detailed statistics
- Track wins, losses, and averages

#### Data Import/Export
- **Load**: Import league data from CSV files
- **Save**: Export data to CSV or save to database
- Timestamp-based file organization

#### Statistics Tracking
- Offensive statistics (batting average, hits, runs, etc.)
- Pitching statistics (ERA, strikeouts, wins, etc.)
- Team statistics and rankings

#### Visualization
- Team performance graphs
- Player stat breakdowns
- Interactive leaderboards

## Development

### Code Organization

The project follows a modular architecture:

- **Core (`src/core/`)**: Business logic independent of UI
- **UI (`src/ui/`)**: PySide6 interface components
- **Data (`src/data/`)**: Persistence layer (SQLite + CSV)
- **Utils (`src/utils/`)**: Shared utilities

### Import Convention

Use absolute imports from the `src` package:
```python
from src.core.team import Team
from src.ui.dialogs.add_player import AddPlayerDialog
from src.data.load.load_csv import load_all_csv_to_db
```

### Database Schema

The application uses SQLite with four main tables:
- `league`: League information and administrators
- `team`: Team data, roster, and statistics
- `player`: Player offensive statistics
- `pitcher`: Pitcher-specific statistics

### Contributing

1. Create a new branch for your feature
2. Follow the existing code style
3. Update tests as needed
4. Submit a pull request

## License

See LICENSE.md for details.

## Notes

- Database is cleared on startup and shutdown (session-based)
- Images are stored as file paths in `data/images/`
- CSV exports include timestamps for version control
- The application supports multiple themes via the Styles module

## Troubleshooting

### Import Errors
If you encounter import errors after restructuring:
```bash
python update_imports.py
```

### Database Issues
If the database becomes corrupted:
```bash
rm data/database/League.db
```
The application will create a new database on next startup.

### Virtual Environment
If packages aren't found, ensure your virtual environment is activated:
```bash
source myenv/bin/activate  # Linux/Mac
```

## Future Enhancements

- User authentication system
- Multi-league support
- Advanced statistical analysis
- Web-based interface
- Mobile companion app

---

For questions or support, please open an issue on the repository.

