from django import forms
from .models import Reviews, Rating, RatingStar



class ReviewForm(forms.ModelForm):
    """ Форма отзывов """

    class Meta:
        fields = ("name", "email", "text")
        model = Reviews


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating 
        fields = ("star", )