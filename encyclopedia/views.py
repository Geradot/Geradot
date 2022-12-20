from django import forms
from django.shortcuts import render
from . import util

import random
import markdown

class PageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control col-8 col-sm-10", "required": True}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control col-8 col-sm-10", "required": True}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page (request, title):
    converted_page = convert_to_html(title) 
    return render(request, f"encyclopedia/{'page' if converted_page is not None else '404'}.html", {
        "title": title,
        "content": converted_page
    }) 

def convert_to_html(title):
    content = util.get_entry(title)
    md = markdown.Markdown() 
    return md.convert(content) if content is not None else content

def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        results_of_search = []
        query = request.POST['q']
        for entry in entries:
            if query.lower() == entry.lower():
                return render(request, "encyclopedia/page.html", {
                    "title": entry,
                    "content": convert_to_html(entry) 
                })
            elif query.lower() in entry.lower():
                results_of_search.append(entry)
        if len(results_of_search) == 0:
            return render(request, "encyclopedia/search.html", {
                "text": "No search results" 
            })
        else:   
            return render(request, "encyclopedia/search.html", {
                "results": results_of_search
            })

error_message = "<p class='alert alert-danger col-8 col-sm-10'>This page already exists.</p>"
def create(request):
    page_title = "Create a new page"
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "title": page_title,
            "form": PageForm()
        })
    else:
        form = PageForm(request.POST)
        if form.is_valid():
            if (util.get_entry(form.cleaned_data["title"]) is not None):
                return render(request, "encyclopedia/create.html", {
                    "title": page_title,
                    "form": form,
                    "error_message": error_message 
                }) 
            else:
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"] 
                util.save_entry(title, content)
                return render(request, "encyclopedia/page.html", {
                    'title': title,
                    'content': convert_to_html(title)
                })
                
def edit(request, title):
    if request.method == "POST":
        page_title = f"Edit a {title} page"
        content = util.get_entry(title)
        
        return render(request, "encyclopedia/edit.html", {
            "page_title": page_title,
            "title": title,
            "content": content
        })

def save(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page_title = f"Edit a {form.cleaned_data['title']} page",
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"] 
            util.save_entry(title, content)
            return render(request, "encyclopedia/page.html", {
                'successful_page': True,
                'page_title': page_title,
                'title': title,
                'content': convert_to_html(title)
            })
    else:
        return render(request, "encyclopedia/404.html", {
            'requested_page': "requested"
        })

def random_page(request):
    allPages = util.list_entries()
    title = random.choice(allPages)
    content = convert_to_html(title)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": content
    })
