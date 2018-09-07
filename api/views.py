import io
import json 
import random
import base64
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from django.core import serializers



from PIL import Image, ImageDraw



from google.cloud import vision
from google.cloud.vision import types
from .models import Image
from .serializers import ImageSerializer

class ImageView(APIView):
  	
  	parser_classes = (MultiPartParser, FormParser)
  	
  	def post(self, request, *args, **kwargs):
	    
	    file_serializer = FileSerializer(data=request.data)
	    if file_serializer.is_valid(): 

	      file_serializer.save()
	      return Response(file_serializer.data, 

	status=status.HTTP_201_CREATED)
	    else:
	      return Response(file_serializer.errors, 
	status=status.HTTP_400_BAD_REQUEST)

class ImageAnalysis(APIView):

  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid(): 
      
      print('Query received: ', file_serializer.data['query'])

    created_number = random.randint(5000, 7000)    
    image = file_serializer.data['file']
    decoded_file = base64.b64decode(image)
    filename = './media/arrived.jpg'
    with open(filename, 'wb') as f:
      f.write(decoded_file)

    
    img_need_to_turn = Image.open(filename).rotate(90)
    img_need_to_turn.save('./media/arrived%s.jpg'%created_number, 'JPEG')

    arrived = './media/arrived%s.jpg'%created_number
    query = file_serializer.data['query']
    serie = random.randint(9000, 11000)
    serie_2 = random.randint(13000, 17000)

    ########## Turn 1
    turn = 0
    vects = self.get_text_position(arrived, turn, query)
    
    im_stage_1 = Image.open(arrived)
    im2_stage_2 = im_stage_1.crop([ vects[0].x, vects[0].y, vects[2].x, vects[2].y ]) 
    im2_stage_2.save('./analysed/output-magic-crop%s.jpg' %serie, 'JPEG') 
    print('Image ready, done.')

    ########## Turn 2
    turn = turn+1
    vects_2 = self.get_text_position('./analysed/output-magic-crop%s.jpg' %serie, turn, query)          
   
    
    # image_ready = im3.rotate(90)
    im_stage_3 = Image.open('./analysed/output-magic-crop%s.jpg' %serie)
    
    im_stage_4 = im_stage_3.crop([ vects_2[1].x-5, vects_2[2].y, vects_2[5].x+10, vects_2[4].y ]) 
    im_stage_4.save('./analysed/output-magic-crop-sec%s.jpg' %serie_2, 'JPEG')
    print('Find the query, done.')

    ######### Turn 3
    turn = turn+1 
    analysed = self.get_text_position('./analysed/output-magic-crop-sec%s.jpg' %serie_2, turn, query) 
    return Response(json.dumps(analysed))
    

  def get_text_position(self, request, turn, query):
    
    # file_serializer = FileSerializer(data=request.data)
  
    print('Getting position')

    client = vision.ImageAnnotatorClient()
    
    with io.open(request, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)

    crop_hints_params = types.CropHintsParams( aspect_ratios=[1.77])
    image_context = types.ImageContext( crop_hints_params=crop_hints_params)
        
    response = client.text_detection(image=image, image_context=image_context)
    # print(response)
    case = turn
    # query = query
    texts = response.text_annotations
    document_vertices = texts[0].bounding_poly.vertices

    print('Turn number: ', case)    
   

    for text in texts:
        
        if (case == 0 ):
            print('Response: ', text.description.replace('$','',3).replace('.','',3).replace(',','',3).isdigit() == True )
            # print('\n"{}"'.format(text.description.replace(' ','\n',90).replace(')','',20).replace('(','',20).replace(':','',20)))
            vertices_ready = document_vertices
            return vertices_ready
      
        elif ( case == 1 and (text.description.replace(' ','\n',90).replace(')','',20).replace('(','',20).replace(':','',20)).lower() == '%s' %query.lower()):
            print('Response: ', text.description.replace('$','',3).replace('.','',3).replace(',','',3).isdigit() == True )    
            vertices,description = text.bounding_poly.vertices,text.description
            
            dx0,dx1,dx2,dx3,yx0,yx1,yx2,yx3 = document_vertices[0],document_vertices[1],document_vertices[2],document_vertices[3],vertices[0],vertices[1],vertices[2],vertices[3] 
            # print(dx0, yx0, dx1, yx1, dx2, yx2, dx3, yx3)
            vertices_ready = (dx0, yx0, dx1, yx1, dx2, yx2, dx3, yx3)
            print(vertices_ready)
            return vertices_ready
            
        elif ( case == 2 and text.description.replace('$','',3).replace('.','',3).replace(',','',3).isdigit() == True ):
            print('Response: ', text.description.replace('$','',3).replace('.','',3).replace(',','',3).isdigit() == True )
            vertices, description = text.bounding_poly.vertices, text.description
            # print('All content : ', texts[0].bounding_poly.vertices)

            print('Location of %s : '%query, text.bounding_poly.vertices)
            print('The %s is : '%query, description)
            print('If you are using find_it this value could be wrong.')
            
            return description

 
       


