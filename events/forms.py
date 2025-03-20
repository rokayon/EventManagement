from django import forms
from .models import Event, Category
class StyleFromMixin:
    '''Mixin to apply styles to from fields'''
    default_classes= "border-2 border-gray-400 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 focus:outline-none"
    
    def apply_style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none rounded-md",
                    'placeholder': f"Enter {field.label.lower()}",
                
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-400  rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 focus:outline-none"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })

class EventForm(StyleFromMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category','asset','participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    def __init__(self,*arg,**kwargs):
         super().__init__(*arg,**kwargs)
         self.apply_style_widgets()

class CategoryForm(StyleFromMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
    def __init__(self,*arg,**kwargs):
         super().__init__(*arg,**kwargs)
         self.apply_style_widgets()

