
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission


# CONSTANTS
START_USER_PERMISSIONS = ['comment']


# Functions
def user_gain_perms(user, models_list):
    """
    User gets all permissions (create, change, delete) from list of models

    user = User
    models_list = list of models
    """
    permissions =[]
    for model in models_list:
        model_perm = Permission.objects.filter(codename__icontains=model)
        permissions += model_perm
    user.user_permissions = permissions


# Views
def account(request):
    data = {}

    data['user'] = request.user

    template = loader.get_template('registration/account.html')
    context = RequestContext(request, data)
    return HttpResponse(template.render(context))


def registration_confirm(request, uidb64=None, token=None,
                         template_name='registration/registration_confirm.html',
                         token_generator=default_token_generator,
                         post_registration_redirect=None,
                         current_app=None, extra_context=None):
    """
    View that checks the hash in a registration link and take permitions for
    to add, change and remove comment.
    """
    UserModel = get_user_model()

    assert uidb64 is not None and token is not None  # checked by URLconf
    # if registration_redirect is None:
    #     registration_redirect = reverse('registration_complete')
    # else:
    #     registration_redirect = resolve_url(post_registration_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True

        # Make user active and set permissions
        user.is_active = True
        user.save()
        user_gain_perms(user, START_USER_PERMISSIONS)

        # return HttpResponseRedirect(post_registration_redirect)
    else:
        validlink = False
    context = {
        'validlink': validlink,
        'user': user,
        'uid':uid,
        'uidb64': uidb64,
        'token': token
    }
    if extra_context is not None:
        context.update(extra_context)

    template = loader.get_template(template_name)
    context = RequestContext(request, context)
    return HttpResponse(template.render(context))
    # return TemplateResponse(request, template_name, context,
    #                         current_app=current_app)
