from django.shortcuts import redirect, render
from .models import Task
from .forms import NewTaskForm

# Create your views here.
def index(request):
    tasks = Task.objects.all()
    print(tasks)

    return render(request, 'task/index.html', {"tasks":tasks})


def detail(request,pk):
    
    task = Task.objects.get(pk = pk)
    return render(request, 'task/detail.html', {"task":task})

def new(request):
    if request.method== 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid ():
            form.save()
            return redirect('/')
    else:
        form = NewTaskForm()

    return render(request, 'task/new.html',{'form':form})

def update(request,pk):
    
    task = Task.objects.get(pk = pk)
    return render(request, 'task/update.html', {"task":task})