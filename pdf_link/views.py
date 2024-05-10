from django.shortcuts import render,redirect
from pdf_link.models import *
from datetime import datetime,timedelta

# Create your views here.
def menu_pdf(request):

    return render(request, 'home_pdf.html')

def lista_pdf_admin(request):

    return render(request, 'home_pdf.html')

def lista_pdf(request):

    return render(request, 'home_pdf.html')


def crear_pdf(request):

    if request.method == 'POST':
            fecha_I = datetime.strptime(request.POST['Fecha_ingreso_t'], '%Y-%m-%d').date()
            fecha_E = datetime.strptime(request.POST['Fecha_ingreso_AU'], '%Y-%m-%d').date()



            try: 
                archivo_adjunto = request.FILES['archivo_adjunto']
            except:
                archivo_adjunto = ""

            id_excel = request.POST['soporte']
            archivo_adjunto = request.POST['formato']

            Pdf_link.objects.create(
                  

            )
        
        
    return redirect('menu_pdf')


    return render(request, 'crear_pdf_link.html')