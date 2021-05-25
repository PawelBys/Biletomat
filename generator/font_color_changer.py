import os

from django.shortcuts import redirect, render

def change_font_color(request):
    f = os.getenv('FONT_COLOR')
    if (f == "black"):
        os.environ['FONT_COLOR'] = "red"
    else:
        os.environ['FONT_COLOR'] = "black"

    path = request.POST.get('path_to_return')
    return redirect(path)

