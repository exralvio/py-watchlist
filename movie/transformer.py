def transformSingle(value):
    return {
        "id": value.id,
        "title": value.title,
        "overview": value.overview,
        "poster_path": value.poster_path,
        "release_date": value.release_date,
        "vote_average": value.vote_average
    }

def transform(values):
    arr = []

    for item in values:
        arr.append(transformSingle(item))
    
    return arr