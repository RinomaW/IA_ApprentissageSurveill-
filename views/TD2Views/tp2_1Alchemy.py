from flask import render_template, request, redirect, url_for
from sqlalchemy import  func
from views.TD2Views.models import db,Artist,Album,Genre,Track,Customer,Invoice
import io
import base64
import matplotlib.pyplot as plt




def db_load():
    # Modèle Artist
    
    
    if request.method == 'POST':
        artist_id = request.form.get('artist_select')
        new_artist_name = request.form['new_artist_name']
        album_title = request.form['album_title']

        # If an existing artist is selected
        if artist_id:
            artist = Artist.query.get(artist_id)
            if artist:
                new_album = Album(Title=album_title, ArtistId=artist.ArtistId)
                db.session.add(new_album)
        # If a new artist name is provided
        elif new_artist_name:
            new_artist = Artist(Name=new_artist_name)
            db.session.add(new_artist)
            db.session.commit()  # Commit to obtain ArtistId
            new_album = Album(Title=album_title, ArtistId=new_artist.ArtistId)
            db.session.add(new_album)

        db.session.commit()  # Commit to save the album
        return redirect(url_for('Alchemy_Route'))  # Redirect after addition

    # Retrieve all artists for display
    artists = Artist.query.all()
    return render_template('TD2templates/Alchemy.html', artists=artists)



from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

# Make sure to import your Flask app context and other necessary modules


def db_load_nb_album():
  

    # Retrieve the count of albums per artist
    artist_album_counts = db.session.query(
        Artist.ArtistId,
        Artist.Name,
        func.count(Album.AlbumId).label('album_count')
    ).outerjoin(Album).group_by(Artist.ArtistId, Artist.Name).all()

    # Retrieve all artists for display
    artists = Artist.query.all()


    # Render the template with the artist album counts
    return render_template('TD2templates/Alchemy_nb_album.html', artists=artists, artist_album_counts=artist_album_counts)






from sqlalchemy import text  # Importez text depuis sqlalchemy

def popular_artists():
    results = db.session.execute(text("""
        SELECT a.Name AS Artist, COUNT(i.InvoiceId) AS NumberOfSales
        FROM artists a
        JOIN albums al ON a.ArtistId = al.ArtistId
        JOIN tracks t ON al.AlbumId = t.AlbumId
        JOIN invoice_items ii ON t.TrackId = ii.TrackId
        JOIN invoices i ON ii.InvoiceId = i.InvoiceId
        GROUP BY a.ArtistId
        ORDER BY NumberOfSales DESC
        LIMIT 10;
    """)).fetchall()  # Assurez-vous de mettre text() ici

    # Convertir les résultats en liste de dictionnaires pour le rendu
    artists = [{'name': row.Artist, 'sales': row.NumberOfSales} for row in results]
    return render_template('TD2templates/popular_artists.html', artists=artists)


def get_top_spending_customers():
    top_customers = db.session.query(
        Customer.FirstName,
        Customer.LastName,
        func.sum(Invoice.Total).label('total_spent')
    ).join(Invoice).group_by(Customer.CustomerId).order_by(func.sum(Invoice.Total).desc()).limit(10).all()
    
    return render_template('TD2templates/top_spending_customers.html', customers=top_customers)


def get_genres_and_track_count():
    genre_track_counts = db.session.query(
        Genre.Name,
        func.count(Track.TrackId).label('track_count')
    ).join(Track).group_by(Genre.GenreId).all()
    
    return genre_track_counts

def genres_histogram():
    genre_data = get_genres_and_track_count()
    
    genres = [row.Name for row in genre_data]
    track_counts = [row.track_count for row in genre_data]

    # Créer l'histogramme
    plt.figure(figsize=(12, 6))
    plt.barh(genres, track_counts, color='skyblue')
    plt.xlabel('Nombre de Pistes')
    plt.title('Nombre de Pistes par Genre Musical')
    plt.grid(axis='x')

    # Enregistrer le graphique dans un objet BytesIO pour l'afficher sur une page HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    plt.close()  # Fermer le graphique pour éviter d'afficher un autre graphique

    return render_template('TD2templates/histogram.html', plot_url=plot_url)