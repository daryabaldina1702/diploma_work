from django import forms

class ProgramIdForm(forms.Form):
    work_program_id = forms.IntegerField(label='ID программы')