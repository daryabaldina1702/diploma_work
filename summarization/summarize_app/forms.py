from django import forms

class ProgramIdForm(forms.Form):
    work_program_id = forms.IntegerField(label='ID программы')

class SummarizationForm(forms.Form):
    description_id = forms.IntegerField(label='ID рабочей программы')
    max_length = forms.IntegerField(label='Длина текста (в словах)', required=False)
    special_token = forms.BooleanField(label='Улучшение модели специальными токенами', required=False, widget=forms.CheckboxInput)
    truncation = forms.BooleanField(label='Нужно ли обрезать текст', required=False, widget=forms.CheckboxInput)

    def clean(self):
        cleaned_data = super().clean()
        # Проверяем, является ли значение для description_id целым числом
        description_id = cleaned_data.get('description_id')
        if description_id is not None and not isinstance(description_id, int):
            raise forms.ValidationError("ID описания должен быть целым числом.")
        return cleaned_data

