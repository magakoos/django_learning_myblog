from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

from django.contrib.sites.models import get_current_site

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.template import loader

from django.core.mail import send_mail


class BlogegRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    # It is union CreateUserForm and PasswordResetForm.save with my marks.
    def save(self, domain_override=None,
        subject_template_name='registration/registration_subject.txt',
        email_template_name='registration/registration_email.html',
        use_https=False, token_generator=default_token_generator,
        from_email=None, request=None, commit=True):

        # Add user into base
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = False
            user.save()
        

        # Create and send email
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
        }
        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(subject, email, from_email, [user.email])

        # Finish create new user
        return user
