import codecs
import itertools
import os
import uuid

os.environ['path'] += r';E:\Python\Python38\Lib\site-packages\cairosvg' # Hack to get cairosvg working on Windows, the dir is going to be wherever you put libcairo-2.dll
import cairosvg

from io import BytesIO
from PIL import Image

# We should automate this, but I'm trying to hurry
defaultColors = [
        "#662D91",
        "#FF0000",
        "#00FFFF",
        "#FCEE21",
        ]

colorList = [
    [
        "#662D91",
        "#FF0000",
        "#00FFFF",
        "#FCEE21",
    ],
    [
        "#040004",
        "#4B000F",
        "#FA023C",
        "#C8FF00",
    ],
    [
        "#434D53",
        "#72AD75",
        "#FFAB07",
        "#E9D558",    
    ],
    [
        "#0E2430",
        "#FC3A51",
        "#F5B349",
        "#E8D5B7",
    ],
    [
        "#070743",
        "#169D99",
        "#B9CC01",
        "#FAE894",
    ],
    [
        "#36173D",
        "#FF4845",
        "#FFC55F",
        "#FFEC5E"
    ],
]

def changeColor(fileName, newColor):
   with codecs.open(fileName, encoding='utf-8', errors='ignore') as f:
      svg = f.read()

   for i in range(len(defaultColors)):
      svg = svg.replace(defaultColors[i], newColor[i])

   svgBytes = str.encode(svg)
   out = BytesIO()
   cairosvg.svg2png(bytestring=svgBytes, write_to=out)
   png = Image.open(out)

   return png

def generateImages(rule, combos):
   rule = rule.split(' ')
   base = rule[0]
   accessoryList = rule[1:]
   for combo in combos:
      for color in colorList:
         monster = changeColor('inputs/' + base, color)
         for idx, img in enumerate(combo):

            (accessory, offset) = accessoryList[idx].split(":")
            offset = [int(off) for off in offset.split(",")]

            out = BytesIO()
            cairosvg.svg2png(url='inputs/' + accessory + '/' + img, write_to=out)
            accessoryImg = Image.open(out)
            monster.paste(accessoryImg, offset, accessoryImg)

         monster.save('outputs/' + str(uuid.uuid4()) + '.png')

def generateSVGCombos(rule):
   rule = rule.split(' ')
   SVGCombos = []
   for category in rule[1:]:
      category = category.split(":")[0]
      SVGCombos.append(os.listdir('inputs/' + category))
   SVGCombos = itertools.product(*SVGCombos)
   return SVGCombos

def main():
   os.makedirs('outputs', exist_ok=True)
   with open('inputs/rules.txt') as rules:
      for rule in rules:
         SVGCombos = generateSVGCombos(rule)
         generateImages(rule, SVGCombos)


if __name__ == '__main__':
   main()