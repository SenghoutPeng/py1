from django.shortcuts import render, redirect
from django.conf import settings
import urllib.request
import urllib.parse
import json

def api_call(path, method='GET', data=None):
    url = f"{settings.SERVICE_URL.rstrip('/')}/{path.lstrip('/')}"
    req_data = None
    if data:
        req_data = urllib.parse.urlencode(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=req_data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"API Error calling {url}: {e}")
        return {}

def home(request):
    depts_data = api_call('api/departments/')
    students_data = api_call('api/students/')
    
    departments = depts_data.get('departments', [])
    students = students_data.get('students', [])
    for s in students:
        s['department'] = {'name': s.get('department_name')}
    return render(request, 'admin_home.html', {'departments': departments, 'students': students})

def department_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            api_call('api/departments/', method='POST', data={'name': name})
        return redirect('admin_home')
    return render(request, 'department_form.html')

def department_edit(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            api_call(f'api/departments/{id}/', method='POST', data={'action': 'edit', 'name': name})
        return redirect('admin_home')
    
    dept = api_call(f'api/departments/{id}/')
    return render(request, 'department_form.html', {'department': dept})

def department_delete(request, id):
    if request.method == 'POST':
        api_call(f'api/departments/{id}/', method='POST', data={'action': 'delete'})
        return redirect('admin_home')
    
    dept = api_call(f'api/departments/{id}/')
    return render(request, 'confirm_delete.html', {'obj': dept, 'type': 'Department'})

def student_create(request):
    if request.method == 'POST':
        student_code = request.POST.get('student_code')
        name = request.POST.get('name')
        email = request.POST.get('email')
        department_id = request.POST.get('department_id')
        
        if student_code and name and email and department_id:
            api_call('api/students/', method='POST', data={
                'student_code': student_code,
                'name': name,
                'email': email,
                'department_id': department_id
            })
        return redirect('admin_home')
    
    depts_data = api_call('api/departments/')
    departments = depts_data.get('departments', [])
    return render(request, 'student_form.html', {'departments': departments})

def student_edit(request, id):
    if request.method == 'POST':
        student_code = request.POST.get('student_code')
        name = request.POST.get('name')
        email = request.POST.get('email')
        department_id = request.POST.get('department_id')
        
        api_call(f'api/students/{id}/', method='POST', data={
            'action': 'edit',
            'student_code': student_code,
            'name': name,
            'email': email,
            'department_id': department_id
        })
        return redirect('admin_home')
    
    student = api_call(f'api/students/{id}/')
    depts_data = api_call('api/departments/')
    departments = depts_data.get('departments', [])
    student['department'] = {'id': student.get('department_id')}
    
    return render(request, 'student_form.html', {'student': student, 'departments': departments})

def student_delete(request, id):
    if request.method == 'POST':
        api_call(f'api/students/{id}/', method='POST', data={'action': 'delete'})
        return redirect('admin_home')
    
    student = api_call(f'api/students/{id}/')
    return render(request, 'confirm_delete.html', {'obj': student, 'type': 'Student'})
