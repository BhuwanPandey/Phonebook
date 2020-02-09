from django.shortcuts import render
from .models import Phonebook
# Create your views here.
import os 
def showdata(req):
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # MEDIA_ROOT=os.path.join(BASE_DIR,'media\\')
    post=Phonebook.objects.all()
    names=[]
    contact=[]
    images_status=[]
    images_link=[]
    for p in post:
        names.append(p.name)
        contact.append(p.contact)
        # image_path=MEDIA_ROOT + str(p.images)
        images_link.append(p.images)
        if len(str(p.images)) >0:
            images_status.append('True')
        else:
            images_status.append('False')
    totaldata=zip(names,contact,images_status,images_link)
    return render(req,'home.html',{'posts':totaldata})