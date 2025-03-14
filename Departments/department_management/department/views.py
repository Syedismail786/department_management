from django.shortcuts import render, redirect, get_object_or_404
from .froms import DepartmentForm
from .models import Department


def department_dashboard(request):
    departments = Department.objects.filter(status=True)  # Only active departments
    if 'search' in request.GET:
        search_query = request.GET['search']
        departments = departments.filter(dept_name__icontains=search_query)
    return render(request, 'dashboard.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'add_department.html', {'form': form})

def edit_department(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_dashboard')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'edit_department.html', {'form': form, 'department': department})

def delete_department(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    if request.method == 'POST':
        department.status = False  # Soft delete: Set status to inactive
        department.save()
        return redirect('department_dashboard')
    return render(request, 'delete_department.html', {'department': department})
