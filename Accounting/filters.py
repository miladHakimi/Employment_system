import django_filters


class UserFilter(django_filters.FilterSet):
    LOOK_UP_CHOICES = [('prog', 'Programmer'), ('mech', 'Mechanical Engineer'),
                       ('metal', 'Metak Engineer')]

    field = django_filters.ChoiceFilter(
        choices=LOOK_UP_CHOICES,
        field_name='fieldsOfExpertise',
        lookup_expr='exact',
    )

    class Meta:
        model = Ad
        fields = ['field']

