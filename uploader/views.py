from uploader.forms import UploadDataForm
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import uploader.models as mods

def success(request):
    return HttpResponse("Thank you for submitting an item!")

def home(request):
    return render_to_response("home.html",
        context_instance=RequestContext(request))

def submissions(request):
    items = mods.Item.objects.all()
    return render_to_response("submissions.html",
        { "items": items }, context_instance=RequestContext(request))

def upload(request):
    if request.POST:
        extra_elems = [(name, value) for (name, value) in request.POST.items()
                        if name.startswith("extra")]
        try:
            form = UploadDataForm(request.POST, request.FILES,
                extra_elems=extra_elems)
        except:
            form = UploadDataForm(request.POST, extra_elems=extra_elems)
        if form.is_valid():
            text = add_item(form.cleaned_data)
            return HttpResponseRedirect("/submissions?submitted=1")
        for field in form.fields:
            print field
        return render_to_response("upload.html", {"form": form},
            context_instance=RequestContext(request))
    form = UploadDataForm()
    return render_to_response("upload.html", {"form": form},
        context_instance=RequestContext(request))

def add_item(data):
    """ Take cleaned data from item upload form and store item """
    # Remove empty elements:
    data = [datum for datum in data.iteritems() if datum[1]]
    print data
    el_group = {}
    # el_group will be: {"language": ["en", "de"], "title": ["blah"]}
    item = mods.Item.objects.create(status="P")
    for name, value in data:
        if 'extra' in name:
            el_type = "_".join(name.split("_")[1:-1])
            el_group[el_type] = el_group.setdefault(el_type, [])
            el_group[el_type].append(value)
        elif name == 'file':
            file_obj = mods.File.objects.create(file_name=value, item=item)
        else:
            el_group[name] = el_group.setdefault(name, [])
            el_group[name].append(value)
    def add_metadata(elem, elem_class):
        if elem in el_group:
            elems = el_group[elem]
            if "language" in elem:
                elem = "language"
            for value in elems:
                kwargs = {elem.lower(): value, "item": item}
                print elem_class
                obj = elem_class.objects.create(**kwargs)
    meta_data_info = (
      ("title", mods.Title),
      ("date", mods.Date),
      ("identifier", mods.Identifier),
      ("creator", mods.Creator),
      ("publisher", mods.Publisher),
      ("description", mods.Description),
      ("linguistic_type", mods.LinguisticType),
      ("DCMI_type", mods.DCMIType),
      ("content_language", mods.ContentLanguage),
      ("subject_language", mods.SubjectLanguage),
      ("contributor", mods.Contributor),
    )

    for tup in meta_data_info:
        add_metadata(*tup)

    item.save()
    return str(data)
    
def generate_static_repo(request):
    items = mods.Item.objects.filter(status="Ar")
    return render_to_response("sr.xml", {"items": items},
        mimetype="text/xml", context_instance=RequestContext(request))
