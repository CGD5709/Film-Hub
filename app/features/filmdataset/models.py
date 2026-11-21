from app import db
from app.features.dataset.models import DataSet


class FilmDataset(DataSet):
    __tablename__ = "film_dataset"

    id = db.Column(db.Integer, db.ForeignKey("data_set.id"), primary_key=True)
    csv_filename = db.Column(db.String(255), nullable=False)
    total_movies = db.Column(db.Integer, nullable=False, default=0)
    min_year = db.Column(db.Integer, nullable=True)
    max_year = db.Column(db.Integer, nullable=True)
    primary_genre = db.Column(db.String(120), nullable=True)
    avg_rating = db.Column(db.Float, nullable=True)
    file_size = db.Column(db.Integer, nullable=False, default=0)
    checksum = db.Column(db.String(64), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "film",
    }

    def files(self):
        return []

    def get_files_count(self):
        return 1 if self.csv_filename else 0

    def get_file_total_size(self):
        return self.file_size or 0

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "csv_filename": self.csv_filename,
                "total_movies": self.total_movies,
                "min_year": self.min_year,
                "max_year": self.max_year,
                "primary_genre": self.primary_genre,
                "avg_rating": self.avg_rating,
                "checksum": self.checksum,
                "preview_url": f"/filmdataset/{self.id}/preview",
            }
        )
        return data

    def __repr__(self):
        return f"FilmDataset<{self.id}>"
