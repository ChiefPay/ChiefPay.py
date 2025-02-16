from datetime import datetime


class Utils:
    @staticmethod
    def validate_date(date: str) -> bool:
        """
        Validates that the provided date
        """
        try:
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            return True
        except ValueError:
            raise ValueError(f"Invalid date format: {date}. Expected format is YYYY-MM-DDTHH:MM:SS.sssZ")
