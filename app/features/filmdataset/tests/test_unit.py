"""Pure unit tests for the filmdataset feature (CSV validation & movie metrics)."""

import pytest

from app.features.dataset.models import DataSet
from app.features.filmdataset.models import FilmDataset
from app.features.filmdataset.services import FilmMetricsService
from app.features.filmdataset.validator import FilmCSVValidator

pytestmark = pytest.mark.unit

SAMPLE_MOVIES_CSV = (
    "title,year,genre,director,duration,rating,votes\n"
    "The Godfather,1972,Crime,Francis Ford Coppola,175,9.2,1900000\n"
    "Pulp Fiction,1994,Crime,Quentin Tarantino,154,8.9,2100000\n"
    "Inception,2010,Science Fiction,Christopher Nolan,148,8.8,2400000\n"
    "Spirited Away,2001,Animation,Hayao Miyazaki,125,8.6,790000\n"
    "Cinema Paradiso,1988,Drama,Giuseppe Tornatore,155,8.5,270000\n"
)


def test_validator_accepts_valid_csv_content():
    result = FilmCSVValidator().validate_content(SAMPLE_MOVIES_CSV)

    assert result.is_valid is True
    assert result.errors == []
    assert len(result.rows) == 5
    assert result.headers == ["title", "year", "genre", "director", "duration", "rating", "votes"]


def test_validator_normalizes_uppercase_headers_and_utf8_bom(tmp_path):
    csv_path = tmp_path / "bom_movies.csv"
    content = "\ufeff TITLE , Year , GENRE \nMatrix,1999,Science Fiction\n"
    csv_path.write_bytes(content.encode("utf-8"))

    result = FilmCSVValidator().validate_file(str(csv_path))

    assert result.is_valid is True
    assert result.headers == ["title", "year", "genre"]
    assert result.rows == [{"title": "Matrix", "year": "1999", "genre": "Science Fiction"}]


def test_validator_rejects_missing_required_columns():
    csv_text = "title,year\nInception,2010\n"
    result = FilmCSVValidator().validate_content(csv_text)

    assert result.is_valid is False
    assert any("genre" in err for err in result.errors)


def test_validator_rejects_empty_and_header_only_csv():
    assert FilmCSVValidator().validate_content("").is_valid is False
    header_only = FilmCSVValidator().validate_content("title,year,genre\n")
    assert header_only.is_valid is False
    assert any("at least one movie row" in err for err in header_only.errors)


def test_validator_rejects_empty_or_duplicate_headers():
    empty_col = FilmCSVValidator().validate_content("title,,year,genre\nA,x,2000,Drama\n")
    dup_col = FilmCSVValidator().validate_content("title,year,genre,title\nA,2000,Drama,A\n")

    assert empty_col.is_valid is False
    assert dup_col.is_valid is False


def test_validator_rejects_column_count_mismatch():
    csv_text = "title,year,genre\nInception,2010,Sci-Fi,Extra\n"
    result = FilmCSVValidator().validate_content(csv_text)

    assert result.is_valid is False
    assert any("Row 2" in err for err in result.errors)


def test_validator_rejects_invalid_title_year_and_genre():
    long_title = "A" * 256
    csv_text = (
        "title,year,genre\n"
        ",2010,Action\n"
        f"{long_title},2010,Action\n"
        "Old Film,1800,Drama\n"
        "Future Film,2099,Drama\n"
        "Bad Year,notanint,Drama\n"
        "No Genre,2020,\n"
    )
    result = FilmCSVValidator().validate_content(csv_text)

    assert result.is_valid is False
    assert len(result.errors) == 6


def test_validator_rejects_invalid_rating_and_duration():
    csv_text = (
        "title,year,genre,rating,duration\n"
        "Too High,2020,Drama,11.5,100\n"
        "Negative Rating,2020,Drama,-0.5,100\n"
        "Bad Rating,2020,Drama,abc,100\n"
        "Zero Duration,2020,Drama,7.5,0\n"
        "Huge Duration,2020,Drama,7.5,1600\n"
        "Bad Duration,2020,Drama,7.5,long\n"
    )
    result = FilmCSVValidator().validate_content(csv_text)

    assert result.is_valid is False
    assert len(result.errors) == 6


def test_validator_handles_missing_file_and_invalid_utf8(tmp_path):
    missing_res = FilmCSVValidator().validate_file(str(tmp_path / "does_not_exist.csv"))
    assert missing_res.is_valid is False

    bad_utf8 = tmp_path / "latin1.csv"
    bad_utf8.write_bytes(b"\xff\xfeinvalid")
    utf8_res = FilmCSVValidator().validate_file(str(bad_utf8))
    assert utf8_res.is_valid is False
    assert any("UTF-8" in err for err in utf8_res.errors)


def test_metrics_service_computes_expected_movie_metrics():
    assert FilmMetricsService.compute([]) == {
        "total_movies": 0,
        "min_year": None,
        "max_year": None,
        "primary_genre": None,
        "avg_rating": None,
    }

    validation = FilmCSVValidator().validate_content(SAMPLE_MOVIES_CSV)
    metrics = FilmMetricsService.compute(validation.rows)

    assert metrics == {
        "total_movies": 5,
        "min_year": 1972,
        "max_year": 2010,
        "primary_genre": "Crime",
        "avg_rating": 8.8,
    }


def test_metrics_service_handles_multi_genres_vote_average_and_missing_ratings():
    rows = [
        {"title": "A", "year": "2000", "genre": "Action, Drama", "vote_average": "8.0"},
        {"title": "B", "year": "2005", "genre": "Drama|Sci-Fi", "vote_average": "9.0"},
    ]
    metrics = FilmMetricsService.compute(rows)
    assert metrics["primary_genre"] == "Drama"
    assert metrics["avg_rating"] == 8.5

    no_rating = FilmMetricsService.compute([{"title": "C", "year": "2010", "genre": "Comedy"}])
    assert no_rating["avg_rating"] is None


def test_view_template_uses_polymorphic_film_template():
    assert DataSet.view_template(None) == "dataset/view_dataset.html"
    assert FilmDataset.view_template(None) == "filmdataset/view_filmdataset.html"
