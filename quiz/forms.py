from django import forms


class QuizCreationForm(forms.Form):
    title = forms.CharField()
    option1 = forms.CharField()
    option2 = forms.CharField()
    correct_option = forms.ChoiceField(
        choices=(("op1", "op1"), ("op2", "op2"), ("all", "all"), ("none", "none"))
    )
