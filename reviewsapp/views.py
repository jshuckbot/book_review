from django.shortcuts import render


def index(request):
    name = request.GET.get("name") or "world"
    print(name)
    return render(request, "base.html", {"name": name})
