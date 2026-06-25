from django import forms
from .models import Report, CATEGORY_CHOICES

class ReportForm(forms.ModelForm):

    def clean_category(self):

        category = self.cleaned_data['category']

        mapping = {
            'Infrastruktur': 'infra',
            'Kebersihan': 'kebersihan',
            'Lingkungan': 'lingkungan',
            'Keamanan': 'keamanan',
            'Transportasi': 'transportasi',
        }

        return mapping.get(category, category)

    category = forms.CharField()

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
