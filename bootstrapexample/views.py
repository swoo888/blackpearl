from django.shortcuts import render


def test(request):
    return render(request, 'bootstrapexample/test.html',)
