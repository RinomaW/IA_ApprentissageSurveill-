from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String, Float

db = SQLAlchemy()

class Artist(db.Model):
    __tablename__ = 'artists'
    ArtistId: Mapped[int] = mapped_column(Integer, primary_key=True)
    Name: Mapped[str] = mapped_column(String, nullable=False)
    albums: Mapped[list['Album']] = relationship('Album', backref='artist', lazy=True)

class Album(db.Model):
    __tablename__ = 'albums'
    AlbumId: Mapped[int] = mapped_column(Integer, primary_key=True)
    Title: Mapped[str] = mapped_column(String, nullable=False)
    ArtistId: Mapped[int] = mapped_column(ForeignKey('artists.ArtistId'))

class Invoice(db.Model):
    __tablename__ = 'invoices'
    InvoiceId: Mapped[int] = mapped_column(Integer, primary_key=True)
    CustomerId: Mapped[int] = mapped_column(ForeignKey('customers.CustomerId'))
    Total: Mapped[float] = mapped_column(Float)  # Assuming there's a Total field for the invoice
    customer: Mapped['Customer'] = relationship('Customer', backref='invoices', lazy=True)

class InvoiceLine(db.Model):
    __tablename__ = 'invoice_lines'
    InvoiceLineId: Mapped[int] = mapped_column(Integer, primary_key=True)
    InvoiceId: Mapped[int] = mapped_column(ForeignKey('invoices.InvoiceId'))
    TrackId: Mapped[int] = mapped_column(ForeignKey('tracks.TrackId'))
    UnitPrice: Mapped[float] = mapped_column(Float)
    Quantity: Mapped[int] = mapped_column(Integer)

class Genre(db.Model):
    __tablename__ = 'genres'
    GenreId: Mapped[int] = mapped_column(Integer, primary_key=True)
    Name: Mapped[str] = mapped_column(String, nullable=False)

class Track(db.Model):
    __tablename__ = 'tracks'
    TrackId: Mapped[int] = mapped_column(Integer, primary_key=True)
    GenreId: Mapped[int] = mapped_column(ForeignKey('genres.GenreId'))

class Customer(db.Model):
    __tablename__ = 'customers'
    CustomerId: Mapped[int] = mapped_column(Integer, primary_key=True)
    FirstName: Mapped[str] = mapped_column(String, nullable=False)
    LastName: Mapped[str] = mapped_column(String, nullable=False)
    Email: Mapped[str] = mapped_column(String, nullable=False)
    # Vous pouvez ajouter d'autres champs si nécessaire, comme l'adresse, le pays, etc.
