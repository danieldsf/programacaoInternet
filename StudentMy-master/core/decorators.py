from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """
    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.who_is == 'ST',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.who_is == 'TE',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator