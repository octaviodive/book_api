from django.shortcuts import render
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect, render
import requests
from main.models import Book, Comment 
import json 
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from reportlab.lib.units import inch
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



# Create your views here.

@login_required(login_url='login')
def search_by_id(request):
    info = {}
    id_book =  None 
    title = None
    publication_date = None
    data = None
    if  'id' in request.GET:
        id = request.GET['id']  
        url = 'https://www.etnassoft.com/api/v1/get/?id=%s' % id
        response = requests.get(url)
        if response.json():

            info = response.json()[0]
            id_book = int(info['ID'])    
            title = info['title']
            publication_date = int(info['publisher_date'])
            print(response.json())

            for key, value in info.items():
                print(f'{key}: {value}')

            if Book.objects.filter(id_book=id_book).exists():
                pass  
                          
            else:
                book = Book.objects.create(id_book=id_book, title=title, publication_date=publication_date)
                book.save()
            
            data = Book.objects.get(id_book=id_book)

            return render(request, 'main/home.html', {'book': data, 'info': info})
        else:
            pass

        
    return render(request, 'main/home.html', {'book': data} )

@login_required(login_url='login')
def details(request, pk):
    book = Book.objects.get(id_book=pk)
    
    if request.method == 'POST':
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            text = request.POST.get('text')
            comment = Comment.objects.create(book = book , user = request.user, text = text)
            comment.save()
    else:
        cf = CommentForm()
       
    context ={
      'book': book,  
      'comment_form':cf,
      }   
       
    return render(request, 'main/detail.html', context)

@login_required(login_url='login')
def csv_file(request, *args, **kwargs):
    id = kwargs.get('pk')      
    url = 'https://www.etnassoft.com/api/v1/get/?id=%s' % id
    data = requests.get(url)
    info = data.json()[0].items()
    print(data.json())
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=book.csv'
    write = csv.writer(response)
    header = []
    row = []
    for key,value in info:
        header.append(key) 
        row.append(value) 

    write.writerow(header)
    write.writerow(row)

    return response

@login_required(login_url='login')
def pdf_file(request, pk):
    # Create Bytestream buffer
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    book = Book.objects.get(id_book=pk)

    lines = [
		f'ID : {book.id_book} ',
		f'Title: {book.title}',
        f'Publication date: {book.publication_date}',
        ]

    for line in lines:
        textob.textLine(line)
        
    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename='book.pdf')




    
    

