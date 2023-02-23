from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from edugamesapp.forms import TaskForm
from edugamesapp.models import Task

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

class Tasklistview(ListView):
    model=Task
    template_name = 'index.html'
    context_object_name = 'task1'

class TaskDetailview(DetailView):
    model=Task
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateview(UpdateView):
    model=Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail/',kwargs={'pk':self.object.id})

class TaskDeleteview(DeleteView):
    model=Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvindex')

# Create your views here.
def index(request):
    task1 = Task.objects.all()
    if request.method=='POST':
        task=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')
        task=Task(task=task,priority=priority,date=date)
        task.save()
        return redirect('/')
    return render(request,"index.html",{'task1':task1})

def delete(request,task_id):
    task2=Task.objects.get(id=task_id)
    if request.method=='POST':
        task2.delete()
        return redirect('/')
    return render(request,"delete.html")

def update(request,id):
    task=Task.objects.get(id=id)
    f=TaskForm(request.POST or None,instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')

    return render(request,"edit.html",{'f':f,'task':task})