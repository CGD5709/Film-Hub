import csv
import io
from dataclasses import dataclass
from datetime import datetime, timezone

REQUIRED_COLUMNS = {"title", "year", "genre"}
MIN_YEAR = 1888
MAX_TITLE_LENGTH = 255
MAX_DURATION_MINUTES = 1500
RATING_COLUMNS = ("rating", "vote_average")
DURATION_COLUMNS = ("duration", "runtime")


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]
    rows: list[dict[str, str]]
    headers: list[str]


class FilmCSVValidator:
    """Pure Python validator for Film-Hub CSV datasets (RFC 4180 + domain rules)."""

    def validate_file(self, file_path: str) -> ValidationResult:
        try:
            with open(file_path, mode="r", encoding="utf-8-sig", newline="") as stream:
                return self._validate_stream(stream)
        except FileNotFoundError:
            return ValidationResult(False, [f"CSV file not found: {file_path}"], [], [])
        except UnicodeDecodeError:
            return ValidationResult(False, ["CSV file must be encoded in valid UTF-8"], [], [])
        except csv.Error as exc:
            return ValidationResult(False, [f"Malformed CSV structure: {exc}"], [], [])

    def validate_content(self, content: str) -> ValidationResult:
        try:
            stream = io.StringIO(content)
            return self._validate_stream(stream)
        except csv.Error as exc:
            return ValidationResult(False, [f"Malformed CSV structure: {exc}"], [], [])

    def _validate_stream(self, stream) -> ValidationResult:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            return ValidationResult(False, ["CSV file is empty or missing header row"], [], [])

        normalized_headers = [h.strip().lower() for h in reader.fieldnames]
        if "" in normalized_headers:
            return ValidationResult(False, ["CSV header row contains empty column names"], [], normalized_headers)
        if len(set(normalized_headers)) != len(normalized_headers):
            return ValidationResult(False, ["CSV header row contains duplicate column names"], [], normalized_headers)

        missing = sorted(REQUIRED_COLUMNS - set(normalized_headers))
        if missing:
            return ValidationResult(
                False,
                [f"Missing required columns: {', '.join(missing)}"],
                [],
                normalized_headers,
            )

        errors: list[str] = []
        valid_rows: list[dict[str, str]] = []
        max_year = datetime.now(timezone.utc).year + 2
        total_rows = 0

        for row_num, raw_row in enumerate(reader, start=2):
            total_rows += 1
            if None in raw_row or any(v is None for v in raw_row.values()):
                errors.append(f"Row {row_num}: malformed CSV row (column count mismatch)")
                continue

            normalized_row = {k.strip().lower(): v.strip() for k, v in raw_row.items()}
            row_errors = self._validate_row(normalized_row, row_num, max_year)
            if row_errors:
                errors.extend(row_errors)
            else:
                valid_rows.append(normalized_row)

        if total_rows == 0:
            errors.append("CSV file must contain at least one movie row")

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            rows=valid_rows if is_valid else [],
            headers=normalized_headers,
        )

    def _validate_row(self, row: dict[str, str], row_num: int, max_year: int) -> list[str]:
        errors: list[str] = []

        title = row.get("title", "")
        if not title:
            errors.append(f"Row {row_num}: 'title' cannot be empty")
        elif len(title) > MAX_TITLE_LENGTH:
            errors.append(f"Row {row_num}: 'title' exceeds {MAX_TITLE_LENGTH} characters")

        year_raw = row.get("year", "")
        try:
            year_val = int(year_raw)
            if not (MIN_YEAR <= year_val <= max_year):
                errors.append(f"Row {row_num}: 'year' must be between {MIN_YEAR} and {max_year}")
        except ValueError:
            errors.append(f"Row {row_num}: 'year' must be a valid integer")

        if not row.get("genre", ""):
            errors.append(f"Row {row_num}: 'genre' cannot be empty")

        errors.extend(self._validate_rating(row, row_num))
        errors.extend(self._validate_duration(row, row_num))
        return errors

    def _validate_rating(self, row: dict[str, str], row_num: int) -> list[str]:
        for col in RATING_COLUMNS:
            raw_val = row.get(col, "")
            if raw_val:
                try:
                    rating = float(raw_val)
                    if not (0.0 <= rating <= 10.0):
                        return [f"Row {row_num}: '{col}' must be between 0.0 and 10.0"]
                except ValueError:
                    return [f"Row {row_num}: '{col}' must be a valid number"]
        return []

    def _validate_duration(self, row: dict[str, str], row_num: int) -> list[str]:
        for col in DURATION_COLUMNS:
            raw_val = row.get(col, "")
            if raw_val:
                try:
                    duration = int(raw_val)
                    if not (0 < duration < MAX_DURATION_MINUTES):
                        return [f"Row {row_num}: '{col}' must be between 1 and {MAX_DURATION_MINUTES - 1} minutes"]
                except ValueError:
                    return [f"Row {row_num}: '{col}' must be a valid integer"]
        return []
