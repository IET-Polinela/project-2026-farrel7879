from django import forms
from .models import Report, CATEGORY_CHOICES

class ReportForm(forms.ModelForm):

    # 🔥 FIX CATEGORY DI SINI
    category = forms.ChoiceField(
        choices=[('', 'Pilih Kategori')] + CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Report
        fields = ['title', 'category', 'description', 'location']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan judul laporan'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi laporan'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lokasi kejadian'
            }),
        }