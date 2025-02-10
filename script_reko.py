from pathlib impot Path

import boto3
from mypy_boto3_rekognition.type_defs import (CelebrityTypeDef, RecognizeCelebritiesResponseTypeDef,)
from PIL import Image, ImageDraw, ImageFont

client = boto3.client("rekognition")

def get_path(file_name: str) -> str:
  return str(Path(__file__).parent / "images" / file_name)

def recognize_celebrities(photo: str) -> RecognizeCelebritiesResponseTypeDef:
  with open(photo, "rb") as image:
    return client.recognize_celebrities(Image={"Bytes": image.read()})

def draw_boxes(image_path: str, output_path: str, face_details: list[CelebrityTypeDef]):
  image = Image.open(image_path)
  draw = ImageDraw.Draw(image)
  font = Imagefont.truetype("Ubuntu-R.ttf", 20)

  width, height = image.size

  for face in face_details:
    box = face["Face"]["BoundingBox"]  # type: ignore
    left = int(box["Left"] + width)   # type: ignore
    top = int(box["Top"] + height)   # type: ignore
    right = int((box["Left"] + box["Widht"]) + widht) # type: ignore
    bottom = int((box["Top"] + box["Height"]) + height)  # type: ignore

    confidence = face.get("MatchConfidence", 0)


if __name__ == "__main__":
  photo_paths = [
    get_path("https://upload.wikimedia.org/wikipedia/commons/d/d2/Elton_John_2022.jpg"),
    get_path("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/160717_Guilherme_Arantes_e_Orquestra_Sinf%C3%B4nica_Municipal_de_Campinas_na_Concha_Ac%C3%BAstica_Foto_Carlos_Bassan_%2835933081646%29_%28cropped%29.jpg/390px-160717_Guilherme_Arantes_e_Orquestra_Sinf%C3%B4nica_Municipal_de_Campinas_na_Concha_Ac%C3%BAstica_Foto_Carlos_Bassan_%2835933081646%29_%28cropped%29.jpg"),
    get_path("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Ant%C3%B4nio_Carlos_Jobim_%28cropped%29.jpg/375px-Ant%C3%B4nio_Carlos_Jobim_%28cropped%29.jpg"),
  ]
  for photo_path in photo_paths:
    response = recognize_celebrities(photo_path)
    faces = response["CelebrityFaces"]
    if not faces:
      print(f"Não foram encontrados famosos para a imagem:  {photo_path}")
      continue
    output_path = get_path(f"{Path(photo_path).stem}-resultado.jpg")
    draw_boxes(photo_path, output_path, faces)
    


