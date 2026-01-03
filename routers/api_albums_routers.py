from fastapi import APIRouter, HTTPException, Query
from schemas.album import Album

router = APIRouter()

albums = [
    Album(
        id=1,
        title='Square Up',
        year=2018,
        description='Альбом доступен в двух версиях «BLACK» и «PINK». Содержит четыре трека, с ведущим синглом «Ddu-Du Ddu-Du».',
        price=2370,
        picture_path='/pictures/1.jpeg'
    ),
    Album(
        id=2,
        title='Kill This Love',
        year=2019,
        description='Содержит пять треков, с одноимённым заглавным треком и «Don’t Know What to Do» в качестве второго сингла.',
        price=1990,
        picture_path='/pictures/2.png'
    ),
    Album(
        id=3,
        title='The Album',
        year=2020,
        description='Для альбома Blackpink записали 8 новых песен и работали с множеством продюсеров, включая Тедди Парка, Томми Брауна, R. Tee, Mr. Franks и 24. Окончательный список композиций составил 8 песен, в том числе коллаборации «Ice Cream» с Селеной Гомес и «Bet You Wanna» с Карди Би.',
        price=3500,
        picture_path='/pictures/3.jpg'
    ),
    Album(
        id=4,
        title='Born Pink',
        year=2022,
        description='Альбом, сочетающий элементы попа, хип-хопа и электроники, включает хиты "Shut Down" и "Pink Venom"',
        price=3500,
        picture_path='/pictures/4.jpeg'
    ),
]


@router.get("/", response_model=list[Album])
async def albums_list(
    year: int = Query(None, description="Year of release"),
    title: str = Query(None, description="The title of album"),
    min_price: int = Query(None, description="Minimum price"),
    max_price: int = Query(None, description="Maximum price")
):
    result = albums
    
    if year is not None:
        result = [album for album in result if album.year == year]
    
    if title is not None:
        result = [album for album in result if title.lower() in album.title.lower()]
    
    if min_price is not None:
        result = [album for album in result if album.price >= min_price]
    
    if max_price is not None:
        result = [album for album in result if album.price <= max_price]
    
    return result


@router.get("/{album_id}/", response_model=Album)
async def album_details(album_id: int):

    album = None
    for a in albums:
        if a.id == album_id:
            album = a
            break
    
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    return album


@router.post("/", response_model=Album, status_code=201)
async def album_create(album: Album):

    for a in albums:
        if a.id == album.id:
            raise HTTPException(status_code=409, detail="Album with this ID already exists")
    
    albums.append(album)
    return album


@router.put("/{album_id}/", response_model=Album)
async def album_update(album_id: int, album: Album):

    album_to_update = None
    index = -1
    
    for i, a in enumerate(albums):
        if a.id == album_id:
            album_to_update = a
            index = i
            break
    
    if not album_to_update:
        raise HTTPException(status_code=404, detail="Album not found")
    
    album.id = album_id 
    albums[index] = album
    
    return album


@router.delete("/{album_id}/")
async def album_delete(album_id: int):

    album_to_delete = None
    index = -1
    
    for i, a in enumerate(albums):
        if a.id == album_id:
            album_to_delete = a
            index = i
            break
    
    if not album_to_delete:
        raise HTTPException(status_code=404, detail="Album not found")
    
    deleted_album = albums.pop(index)
    
    return {'message': f'Album "{deleted_album.title}" (ID: {deleted_album.id}) deleted successfully'}