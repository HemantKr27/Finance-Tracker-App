from app.main import main
from app.database.models import create_tables

if __name__ == "__main__":
    main()
    # Initialize the tables (only need to run once)
    create_tables()