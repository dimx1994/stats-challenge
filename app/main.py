import logging

from app.data_importer import calculate_statistics
from app.models import create_all_models_waiting_postgres, save_reports

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)


def main() -> None:
    create_all_models_waiting_postgres()
    page_loads, clicks, unique_user_clicks = calculate_statistics()
    save_reports(page_loads, clicks, unique_user_clicks)


if __name__ == "__main__":
    main()
