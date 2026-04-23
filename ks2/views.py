from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import KS2Form, WorkItem
from .forms import KS2FormModelForm, WorkItemForm


def ks2_list(request):
    """Список всех форм КС-2"""
    forms_list = KS2Form.objects.all()
    return render(request, 'ks2/ks2_list.html', {'forms_list': forms_list})


def ks2_create(request):
    """Создание новой формы КС-2"""
    if request.method == 'POST':
        form = KS2FormModelForm(request.POST)
        if form.is_valid():
            ks2_instance = form.save()
            return redirect('ks2_edit', pk=ks2_instance.pk)
    else:
        form = KS2FormModelForm()
    
    return render(request, 'ks2/ks2_form.html', {
        'form': form,
        'title': 'Создать новую форму КС-2',
        'action': 'create'
    })


def ks2_edit(request, pk):
    """Редактирование формы КС-2 с добавлением работ"""
    ks2_instance = get_object_or_404(KS2Form, pk=pk)
    works = ks2_instance.works.all()
    
    # Проверка ограничения на количество работ (не больше 15)
    max_works = 15
    works_count = works.count()
    can_add_work = works_count < max_works
    
    if request.method == 'POST':
        # Обновление основных данных
        form = KS2FormModelForm(request.POST, instance=ks2_instance)
        if form.is_valid():
            form.save()
            
            # Добавление новой работы (если нажата соответствующая кнопка)
            if 'add_work' in request.POST and can_add_work:
                work_form = WorkItemForm(request.POST)
                if work_form.is_valid():
                    work = work_form.save(commit=False)
                    work.ks2_form = ks2_instance
                    work.save()
                    return redirect('ks2_edit', pk=ks2_instance.pk)
            else:
                return redirect('ks2_list')
    else:
        form = KS2FormModelForm(instance=ks2_instance)
    
    work_form = WorkItemForm()
    
    # Вычисляем итоговую сумму
    total_amount = sum(work.quantity * work.price for work in works)
    
    return render(request, 'ks2/ks2_edit.html', {
        'form': form,
        'work_form': work_form,
        'works': works,
        'ks2_instance': ks2_instance,
        'total_amount': total_amount,
        'can_add_work': can_add_work,
        'max_works': max_works,
        'works_count': works_count,
    })


def ks2_delete_work(request, pk, work_pk):
    """Удаление работы из формы КС-2"""
    ks2_instance = get_object_or_404(KS2Form, pk=pk)
    work = get_object_or_404(WorkItem, pk=work_pk, ks2_form=ks2_instance)
    work.delete()
    return redirect('ks2_edit', pk=pk)


def ks2_delete(request, pk):
    """Удаление формы КС-2"""
    ks2_instance = get_object_or_404(KS2Form, pk=pk)
    if request.method == 'POST':
        ks2_instance.delete()
        return redirect('ks2_list')
    return render(request, 'ks2/ks2_confirm_delete.html', {'ks2_instance': ks2_instance})

