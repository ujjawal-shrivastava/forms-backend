from ariadne import ObjectType
from apps.auth_jwt.decorators import login_required
from apps.auth_jwt.exceptions import LoginRequiredError, FormDoesNotExistError
from django.contrib.auth import get_user_model
from .models import Form, Response
from math import ceil
from datetime import datetime
from django.db.models import Sum


form = ObjectType("Form")
public_form = ObjectType("PublicForm")
forms = ObjectType("Forms")
response = ObjectType("Response")


def resolve_public_form(_,info,formid): 
    try:
        form = Form.objects.get(formid=formid)
    except Form.DoesNotExist:
        raise FormDoesNotExistError
    if form and form.isPublished:
        form.views +=1
        form.save()
        return form
    else :
        raise FormDoesNotExistError

@login_required
def resolve_get_form(_,info,formid):
    user = get_user_model().objects.prefetch_related('forms').get(email=info.context.user.email)
    try:
        form = user.forms.get(formid=formid)
    except Form.DoesNotExist:
        raise FormDoesNotExistError

    return form



@login_required 
def resolve_forms(_,info,input):
    user = get_user_model().objects.prefetch_related('forms').get(email=info.context.user.email)
    if user and user.is_active:
        forms=None
        if input["open"]=="ALL":
            forms = user.forms.all()    
        elif input["open"]=="OPEN":
            forms = user.forms.filter(isOpen=True)
        elif input["open"]=="CLOSED":
            forms = user.forms.filter(isOpen=False)

        if input["published"]=="ALL":
            forms = forms.all()
        elif input["published"]=="PUBLISHED":
            forms =forms.filter(isPublished=True)
        elif input["published"]=="SAVED":
            forms = forms.filter(isPublished=False)

        forms=forms.order_by('-added')
        
        total = user.forms.count()
        totalPages = ceil(forms.count()/10)
        currentPage=input["page"]
        forms = forms[(currentPage-1)*10:((currentPage-1)*10)+10]

        return {"forms":forms,"total":total,"currentPage":currentPage,"totalPages":totalPages}        



@public_form.field("formid")
@form.field("formid")
def resolve_form_id(obj,*_):
    return obj.formid

@public_form.field("title")
@form.field("title")
def resolve_form_title(obj,*_):
    return obj.title

@public_form.field("description")
@form.field("description")
def resolve_form_description(obj,*_):
    return obj.description

@public_form.field("bgtheme")
@form.field("bgtheme")
def resolve_form_bgtheme(obj,*_):
    return obj.bgtheme

@public_form.field("open")
@form.field("open")
def resolve_form_open(obj,*_):
    return obj.isOpen

@form.field("published")
def resolve_form_published(obj,*_):
    return obj.isPublished


@form.field("author")
def resolve_form_author(obj,*_):
    return obj.author

@form.field("data")
def resolve_form_data(obj,*_):
    return obj.data

@form.field("views")
def resolve_form_views(obj,*_):
    return obj.views


@form.field("responses")
def resolve_form_views(obj,*_):
    return obj.responses.count()

@form.field("added")
def resolve_form_added(obj,*_):
    return obj.added.strftime("%d/%m/%Y, %H:%M:%S")

@form.field("updated")
def resolve_form_updated(obj,*_):
    return obj.updated.strftime("%d/%m/%Y, %H:%M:%S")


@public_form.field("author")
def resolve_public_form_author(obj,*_):
    return obj.author.name

@public_form.field("verified")
def resolve_public_form_verified(obj,*_):
    return obj.author.verified

@public_form.field("data")
def resolve_public_form_data(obj,*_):
    if obj.isPublished and obj.isOpen:
        return obj.data
    return ""


@login_required
def resolve_save_form(_,info,input):
    user = get_user_model().objects.prefetch_related('forms').get(email=info.context.user.email)
    if user is None:
        raise LoginRequiredError()
    else:
        if input["formid"]:
            form = user.forms.get(formid=input["formid"])
            if form:
                form.formid = input["formid"]
                form.title = input["title"]
                form.description = input["description"]
                form.bgtheme = input["bgtheme"]
                form.isOpen = input["open"]
                form.data = input["data"]
                form.save()
        else:
            form = Form.objects.create(
                title = input["title"],
                description = input["description"],
                bgtheme = input["bgtheme"],
                isOpen = input["open"],
                data = input["data"],
                author = user
            )
        return form

@login_required
def resolve_delete_form(_,info,formid):
    user = get_user_model().objects.get(email=info.context.user.email)
    if user is None:
        raise LoginRequiredError()
    else:
        form = user.forms.get(formid=formid)
        if form:
            form.delete()
            return True
        else:
            return False

@login_required
def resolve_publish_form(_,info,formid):
    user = get_user_model().objects.get(email=info.context.user.email)
    if user is None:
        raise LoginRequiredError()
    else:
        form = user.forms.get(formid=formid)
        if form:
            form.isPublished = True
            form.save()
            return True
        else:
            return False

@login_required
def resolve_unpublish_form(_,info,formid):
    user = get_user_model().objects.get(email=info.context.user.email)
    if user is None:
        raise LoginRequiredError()
    else:
        form = user.forms.get(formid=formid)
        if form:
            form.isPublished = False
            form.save()
            return True
        else:
            return False





def resolve_add_response(_,info,formid,data):
    try: 
        form = Form.objects.get(formid=formid)
    except form.DoesNotExist:
        raise FormDoesNotExistError()
    
    response = Response.objects.create(
        data=data,
        form = form
    )
    
    return {
        "responseid":response.responseid, 
        "formid":response.form.formid, 
        "data":response.data, 
        "added":response.added.strftime("%d/%m/%Y, %H:%M:%S")
        }


@login_required 
def resolve_responses(_,info,formid):
    user = get_user_model().objects.prefetch_related('forms').get(email=info.context.user.email)
    if user and user.is_active:
        try:
            form = user.forms.prefetch_related('responses').get(formid=formid)
        except Form.DoesNotExist:
            raise FormDoesNotExistError
        form_responses=form.responses.order_by('-added')
        responses = []
        for res in form_responses:
            new_res = {
                "responseid":res.responseid, 
                "formid":res.form.formid, 
                "data":res.data, 
            "added":res.added.strftime("%d/%m/%Y, %H:%M:%S")
            }
            responses.append(new_res)
        total = form_responses.count()
        return {"responses":responses,"total":total}


@login_required
def resolve_user_data(_,info):
    user = get_user_model().objects.get(email=info.context.user.email)
    if user and user.is_active:
        form = Form.objects.filter(author=user)
        form_count = form.count()
        responses_count = Response.objects.filter(form__author=user).count()
        views_count = form.aggregate(Sum('views'))
        views_count = views_count['views__sum']
        if(!views_count) views_count=0

        return {
            "forms":form_count,
            "responses":responses_count,
            "views":views_count
        }
