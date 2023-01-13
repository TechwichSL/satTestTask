### Test Task for sentinel 2

using two simple commands below we can run the application.
```
pip3 install -r requirements.txt
uvicorn main:app --reload
```

after running the server following three endpoints are available. inputs should be passed to endpoints using **form data**:

http://127.0.0.1:8000/attributes:

sample CURL:
`curl --location --request POST 'http://127.0.0.1:8000/attributes' \
--form 'file=@"/home/amzmohammad/Downloads/S2L2A_2022-06-09.tiff"'`
sample output:
```
{
    "imageSize": {
        "height": 1384,
        "width": 2186
    },
    "bandsCount": 12,
    "boundingBox": [
        -0.00839,
        38.747216,
        0.2381,
        38.878028
    ],
    "crs": "EPSG:4326"
}
```

http://127.0.0.1:8000/thumbnail

sample CURL:
`curl --location --request POST 'http://127.0.0.1:8000/thumbnail' \
--form 'file=@"/home/amzmohammad/Pictures/Screenshot from 2022-06-02 12-01-22.png"'`
sample output: The image is directly the response of this service.


http://127.0.0.1:8000/ndvi

sample CURL:
`curl --location --request POST 'http://127.0.0.1:8000/ndvi' \
--form 'file=@"/home/amzmohammad/Downloads/S2L2A_2022-06-09.tiff"' \
--form 'palette="Accent"'`
sample output: The image is directly the response of this service.

**Also, a postman collection is included in the repository for the ease of testing endpoints.**