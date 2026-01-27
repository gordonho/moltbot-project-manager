from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project, Task


def project_list(request):
    """项目列表页面"""
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_detail(request, pk):
    """项目详情页面"""
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})


def project_create(request):
    """创建新项目"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if title:
            Project.objects.create(title=title, description=description)
            messages.success(request, '项目创建成功！')
            return redirect('project_list')
        else:
            messages.error(request, '项目标题不能为空！')
    
    return render(request, 'projects/project_form.html')


def project_edit(request, pk):
    """编辑项目"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.status = request.POST.get('status')
        project.result = request.POST.get('result', '')
        project.notes = request.POST.get('notes', '')
        project.save()
        
        messages.success(request, '项目更新成功！')
        return redirect('project_detail', pk=project.pk)
    
    return render(request, 'projects/project_form.html', {'project': project})


def project_delete(request, pk):
    """删除项目"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, '项目删除成功！')
        return redirect('project_list')
    
    return render(request, 'projects/project_confirm_delete.html', {'project': project})