from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, Task


def project_list(request):
    """项目列表页面"""
    # 获取搜索查询参数
    query = request.GET.get('q')
    status_filter = request.GET.get('status', '')
    
    if request.method == 'POST':
        # 处理直接状态更新
        project_id = request.POST.get('project_id')
        new_status = request.POST.get('status')
        if project_id and new_status:
            try:
                project = Project.objects.get(pk=project_id)
                project.status = new_status
                project.save()
                messages.success(request, '项目状态更新成功！')
            except Project.DoesNotExist:
                messages.error(request, '项目不存在！')
        return redirect('project_list')
    
    # 获取所有项目
    projects = Project.objects.all()
    
    # 如果有状态过滤，则应用过滤
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    # 如果有搜索查询，则进行全文检索
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(result__icontains=query) |
            Q(notes__icontains=query)
        )
    
    # 获取所有可能的状态值用于过滤选项
    all_statuses = Project.STATUS_CHOICES
    
    # 统计各个状态的项目数量
    total_count = Project.objects.count()
    pending_count = Project.objects.filter(status='pending').count()
    in_progress_count = Project.objects.filter(status='in_progress').count()
    completed_count = Project.objects.filter(status='completed').count()
    cancelled_count = Project.objects.filter(status='cancelled').count()
    
    # 分页处理
    paginator = Paginator(projects, 10)  # 每页显示10个项目
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'projects/project_list.html', {
        'projects': page_obj,
        'query': query,
        'selected_status': status_filter,
        'all_statuses': all_statuses,
        'total_count': total_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count
    })


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