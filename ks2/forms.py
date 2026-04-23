from django import forms
from .models import KS2Form, WorkItem


class KS2FormModelForm(forms.ModelForm):
    """Форма для ввода данных КС-2"""
    
    class Meta:
        model = KS2Form
        fields = [
            'investor', 'okpo_investor',
            'customer', 'okpo_customer',
            'contractor', 'okpo_contractor',
            'construction', 'object_name', 'okdp',
            'document_number', 'contract_number', 'contract_date',
            'day_contract', 'month_contract', 'year_contract',
            'report_from', 'report_to',
            'smeta',
            'surrender_position', 'surrender_signature',
            'accept_position', 'accept_signature',
        ]
        widgets = {
            'investor': forms.TextInput(attrs={'class': 'form-control'}),
            'okpo_investor': forms.TextInput(attrs={'class': 'form-control'}),
            'customer': forms.TextInput(attrs={'class': 'form-control'}),
            'okpo_customer': forms.TextInput(attrs={'class': 'form-control'}),
            'contractor': forms.TextInput(attrs={'class': 'form-control'}),
            'okpo_contractor': forms.TextInput(attrs={'class': 'form-control'}),
            'construction': forms.TextInput(attrs={'class': 'form-control'}),
            'object_name': forms.TextInput(attrs={'class': 'form-control'}),
            'okdp': forms.TextInput(attrs={'class': 'form-control'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_number': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'day_contract': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60px; display: inline-block;'}),
            'month_contract': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60px; display: inline-block;'}),
            'year_contract': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 80px; display: inline-block;'}),
            'report_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'report_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'smeta': forms.TextInput(attrs={'class': 'form-control'}),
            'surrender_position': forms.TextInput(attrs={'class': 'form-control'}),
            'surrender_signature': forms.TextInput(attrs={'class': 'form-control'}),
            'accept_position': forms.TextInput(attrs={'class': 'form-control'}),
            'accept_signature': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'investor': 'Инвестор',
            'okpo_investor': 'ОКПО инвестора',
            'customer': 'Заказчик',
            'okpo_customer': 'ОКПО заказчика',
            'contractor': 'Подрядчик',
            'okpo_contractor': 'ОКПО подрядчика',
            'construction': 'Наименование строительства',
            'object_name': 'Объект',
            'okdp': 'ОКДП',
            'document_number': 'Номер документа',
            'contract_number': 'Номер договора',
            'contract_date': 'Дата договора',
            'day_contract': 'День',
            'month_contract': 'Месяц',
            'year_contract': 'Год',
            'report_from': 'Отчет с',
            'report_to': 'Отчет по',
            'smeta': 'Стоимость по смете',
            'surrender_position': 'Должность сдающего',
            'surrender_signature': 'ФИО сдающего',
            'accept_position': 'Должность принимающего',
            'accept_signature': 'ФИО принимающего',
        }


class WorkItemForm(forms.ModelForm):
    """Форма для добавления работы"""
    
    class Meta:
        model = WorkItem
        fields = ['position', 'name', 'number_pricelist', 'unit_of_measurement', 'quantity', 'price']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20-30'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наименование работы'}),
            'number_pricelist': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '-'}),
            'unit_of_measurement': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Выберите ед. изм.'),
                ('м2', 'м²'),
                ('м3', 'м³'),
                ('м', 'м'),
                ('м.пог.', 'м.пог.'),
                ('шт', 'шт'),
                ('точка', 'точка'),
                ('комплект', 'комплект'),
                ('час', 'час'),
                ('смена', 'смена'),
                ('кг', 'кг'),
                ('тонна', 'т'),
                ('л', 'л'),
            ]),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'min': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'position': '№ позиции',
            'name': 'Наименование работы',
            'number_pricelist': '№ прейскуранта',
            'unit_of_measurement': 'Ед. измерения',
            'quantity': 'Количество',
            'price': 'Цена за ед.',
        }
