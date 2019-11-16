import django_filters

from Commercial.models import Ad


class UserFilter(django_filters.FilterSet):
    LOOK_UP_CHOICES = [('prog', 'Programmer'), ('mech', 'Mechanical Engineer'),
                       ('metal', 'Metak Engineer')]

    field = django_filters.ChoiceFilter(
        choices=LOOK_UP_CHOICES,
        field_name='fieldsOfExpertise',
        lookup_expr='contains',
    )

    class Meta:
        model = Ad
        fields = ['field']

