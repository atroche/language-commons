from django import forms
from django.core.exceptions import ValidationError
import re
from datetime import datetime
from uploader.models import LINGUISTIC_TYPES, DCMI_TYPES
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import Layout, Fieldset, Row, HTML

def date_validator(date_str):
    """
    Check to see if date_str conforms to OLAC standard.
    If it's not, raise an error.
    """
    valid_formats = ("%Y", "%Y-%m", "%Y-%m-%d")
    date = None
    for date_format in valid_formats:
        try:
            date = datetime.strptime(date_str, date_format)
            return date_str
        except:
            continue
    regex = "^\[.*\]|[0-9]{4}-[0-9]{4}$"
    if re.match(regex, date_str):
        return date_str
    raise ValidationError("Date string must conform to correct format, or be enclosed in square brackets.")

class UploadDataForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        """
        Need to override constructor because of all the dynamic form elements.
        It basically works out which of the elements submitted via 'request' to
        the form are 'extra' ones, then adds them to the form's internal
        field structure in the right order.
        """
        self.file = kwargs.get("file", None)
        extra_elems = []
        if 'extra_elems' in kwargs:
            extra_elems = kwargs.pop('extra_elems')
        super(UploadDataForm, self).__init__(*args, **kwargs)
        num_extra_elems = {}
        extra_elems.reverse()
        for name, value in extra_elems:
            split_elem = name.split("_")
            elem_type = "_".join(split_elem[1:-1])
            elem_label = " ".join(word.capitalize() for word in split_elem[1:-1])
            if "linguistic_type" in elem_type:
                self.fields[name] = forms.ChoiceField(initial=value,
                    label=elem_label, required=False, choices=LINGUISTIC_TYPES)
            elif "DCMI" in elem_type:
                self.fields[name] = forms.ChoiceField(initial=value,
                    label=elem_label, required=False, choices=DCMI_TYPES)
            elif "description" in elem_type:
                self.fields[name] = forms.CharField(initial=value,
                    label=elem_label, required=False, widget=forms.Textarea)
            else:
                self.fields[name] = forms.CharField(initial=value,
                    label=elem_label, required=False)
            if "date" in elem_type:
                self.fields[name].validators=[date_validator]
            num_extra_elems.setdefault(elem_type, 0)
            num_extra_elems[elem_type] += 1
            self.fields.keyOrder.insert(
                self.fields.keyOrder.index(elem_type)+num_extra_elems[elem_type],
                name)
            self.fields.keyOrder.pop()

    title = forms.CharField(required=False)
    date = forms.CharField(required=False, validators=[date_validator],
    help_text='Exact dates must be of the following format YYYY, YYYY-MM, YYYY-MM-DD, or YYYY-YYYY. Inexact dates must be wrapped in square brackets and can take any format, like so: [Twentieth Century]')
    creator = forms.CharField(required=False)
    publisher = forms.CharField(required=False)
    contributor = forms.CharField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    linguistic_type = forms.ChoiceField(required=False,
        choices=LINGUISTIC_TYPES, label="Linguistic Type",
        help_text='See <a href="http://www.language-archives.org/REC/type.html#Linguistic Data Type">here</a> for details.')
    DCMI_type = forms.ChoiceField(required=False, label="DCMI Type",
        choices=DCMI_TYPES,
        help_text='See <a href="http://dublincore.org/documents/dcmi-type-vocabulary/">here</a> for details.')
    content_language = forms.CharField(required=False, label="Content Language",
        help_text='Enter the three character ISO 639-3 language code, \
        as listed <a href="http://www.sil.org/iso639-3/codes.asp">here</a>.')
    subject_language = forms.CharField(required=False, label='Subject Language',
        help_text='Enter the three character ISO 639-3 language code, \
        as listed <a href="http://www.sil.org/iso639-3/codes.asp">here</a>.')
    file = forms.FileField(required=True)

    rendered_fields = []
