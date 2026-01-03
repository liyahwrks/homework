from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas.album import Album


router = APIRouter()
templates = Jinja2Templates(directory="templates")

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


@router.get("/", response_class=HTMLResponse)
async def album_list(request: Request):
    context = {
        "request": request,
        "title": "Список альбомов в продаже",
        "albums": albums
    }

    return templates.TemplateResponse("album_list.html", context=context)

@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    context = {
        "request": request,
        "title": "About Us",
    }
    return templates.TemplateResponse("about.html", context=context)


@router.get("/albums/{album_id}/", response_class=HTMLResponse)
async def album_details(request: Request, album_id: int):

    album = None
    for a in albums:
        if a.id == album_id: 
            album = a
            break
    
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    context = {
        "request": request,
        "album": album
    }

    return templates.TemplateResponse("album_detail.html", context=context)