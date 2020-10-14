def singleTransform(value):
    return {
        "id": value.id,
        "name": value.name,
        "note": value.note,
        "created_at": str(value.created_at),
        "updated_at": str(value.updated_at)
    }

def transform(values):
    arr = []

    for item in values:
        arr.append(singleTransform(item))

    return arr

def singleMovie(value):
    return {
        "id": value.id,
        "movie_id": value.movie_id,
        "title": value.title,
        "poster_path": value.poster_path
    }

def transformMovies(values):
    arr = []

    for item in values:
        arr.append(singleMovie(item))

    return arr