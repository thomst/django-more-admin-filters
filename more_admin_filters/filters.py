# -*- coding: utf-8 -*-
from django.contrib.admin.utils import prepare_lookup_value
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.utils import reverse_field_path
from django.contrib.admin.utils import get_model_from_relation
from django.core.exceptions import ValidationError
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.filters import AllValuesFieldListFilter
from django.contrib.admin.filters import ChoicesFieldListFilter
from django.contrib.admin.filters import RelatedFieldListFilter
from django.contrib.admin.filters import RelatedOnlyFieldListFilter


# Generic filter using a dropdown widget instead of a list.
class DropdownFilter(AllValuesFieldListFilter):
    """
    Dropdown filter for all kind of fields.
    """
    template = 'more_admin_filters/dropdownfilter.html'


class ChoicesDropdownFilter(ChoicesFieldListFilter):
    """
    Dropdown filter for fields using choices.
    """
    template = 'more_admin_filters/dropdownfilter.html'


class RelatedDropdownFilter(RelatedFieldListFilter):
    """
    Dropdown filter for relation fields.
    """
    template = 'more_admin_filters/dropdownfilter.html'


class RelatedOnlyDropdownFilter(RelatedOnlyFieldListFilter):
    """
    Dropdown filter for relation fields using limit_choices_to.
    """
    template = 'more_admin_filters/dropdownfilter.html'


class MultiSelectMixin(object):
    def queryset(self, request, queryset):
        params = Q()
        for lookup_arg, value in self.used_parameters.items():
            params |= Q(**{lookup_arg:value})
        try:
            return queryset.filter(params)
        except (ValueError, ValidationError) as e:
            # Fields may raise a ValueError or ValidationError when converting
            # the parameters to the correct type.
            raise IncorrectLookupParameters(e)

    def querystring_for_choices(self, val, changelist):
        lookup_vals = self.lookup_vals[:]
        if val in self.lookup_vals:
            lookup_vals.remove(val)
        else:
            lookup_vals.append(val)
        if lookup_vals:
            query_string = changelist.get_query_string({
                self.lookup_kwarg: ','.join(lookup_vals),
            }, [])
        else:
            query_string = changelist.get_query_string({},
                [self.lookup_kwarg])
        return query_string

    def querystring_for_isnull(self, changelist):
        if self.lookup_val_isnull:
            query_string = changelist.get_query_string({},
                [self.lookup_kwarg_isnull])
        else:
            query_string = changelist.get_query_string({
                self.lookup_kwarg_isnull: 'True',
            }, [])
        return query_string

    def has_output(self):
        return len(self.lookup_choices) > 1


class MultiSelectFilter(MultiSelectMixin, admin.AllValuesFieldListFilter):
    """
    Multi select filter for all kind of fields.
    """
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__in' % field_path
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        lookup_vals = request.GET.get(self.lookup_kwarg)
        self.lookup_vals = lookup_vals.split(',') if lookup_vals else list()
        self.lookup_val_isnull = request.GET.get(self.lookup_kwarg_isnull)
        self.empty_value_display = model_admin.get_empty_value_display()
        parent_model, reverse_path = reverse_field_path(model, field_path)
        # Obey parent ModelAdmin queryset when deciding which options to show
        if model == parent_model:
            queryset = model_admin.get_queryset(request)
        else:
            queryset = parent_model._default_manager.all()
        self.lookup_choices = (queryset
                               .distinct()
                               .order_by(field.name)
                               .values_list(field.name, flat=True))
        super(admin.AllValuesFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.used_parameters = self.prepare_used_parameters(self.used_parameters)

    def prepare_querystring_value(self, value):
        # mask all commas or these values will be used
        # in a comma-seperated-list as get-parameter
        return str(value).replace(',', '%~')

    def prepare_used_parameters(self, used_parameters):
        # remove comma-mask from list-values for __in-lookups
        for key, value in used_parameters.items():
            if not key.endswith('__in'): continue
            used_parameters[key] = [v.replace('%~', ',') for v in value]
        return used_parameters

    def choices(self, changelist):
        yield {
            'selected': not self.lookup_vals and self.lookup_val_isnull is None,
            'query_string': changelist.get_query_string({}, [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        include_none = False
        for val in self.lookup_choices:
            if val is None:
                include_none = True
                continue
            val = str(val)
            qval = self.prepare_querystring_value(val)
            yield {
                'selected': qval in self.lookup_vals,
                'query_string': self.querystring_for_choices(qval, changelist),
                'display': val,
            }
        if include_none:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': self.querystring_for_isnull(changelist),
                'display': self.empty_value_display,
            }


class MultiSelectRelatedFilter(MultiSelectMixin, admin.RelatedFieldListFilter):
    """
    Multi select filter for relation fields.
    """
    def __init__(self, field, request, params, model, model_admin, field_path):
        other_model = get_model_from_relation(field)
        self.lookup_kwarg = '%s__%s__in' % (field_path, field.target_field.name)
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        lookup_vals = request.GET.get(self.lookup_kwarg)
        self.lookup_vals = lookup_vals.split(',') if lookup_vals else list()
        self.lookup_val_isnull = request.GET.get(self.lookup_kwarg_isnull)
        super(admin.RelatedFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = self.field_choices(field, request, model_admin)
        if hasattr(field, 'verbose_name'):
            self.lookup_title = field.verbose_name
        else:
            self.lookup_title = other_model._meta.verbose_name
        self.title = self.lookup_title
        self.empty_value_display = model_admin.get_empty_value_display()

    def choices(self, changelist):
        yield {
            'selected': not self.lookup_vals and not self.lookup_val_isnull,
            'query_string': changelist.get_query_string(
                {},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]
            ),
            'display': _('All'),
        }
        for pk_val, val in self.lookup_choices:
            pk_val = str(pk_val)
            yield {
                'selected': pk_val in self.lookup_vals,
                'query_string': self.querystring_for_choices(pk_val, changelist),
                'display': val,
            }
        if self.include_empty_choice:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': self.querystring_for_isnull(changelist),
                'display': self.empty_value_display,
            }


class MultiSelectRelatedOnlyFilter(MultiSelectRelatedFilter):
    def field_choices(self, field, request, model_admin):
        pk_qs = (
            model_admin.get_queryset(request)
            .distinct()
            .values_list("%s__pk" % self.field_path, flat=True)
        )
        ordering = self.field_admin_ordering(field, request, model_admin)
        return field.get_choices(
            include_blank=False, limit_choices_to={"pk__in": pk_qs}, ordering=ordering
        )


class MultiSelectDropdownFilter(MultiSelectFilter):
    """
    Multi select dropdown filter for all kind of fields.
    """
    template = 'more_admin_filters/multiselectdropdownfilter.html'

    def choices(self, changelist):
        query_string = changelist.get_query_string({}, [self.lookup_kwarg, self.lookup_kwarg_isnull])
        yield {
            'selected': not self.lookup_vals and self.lookup_val_isnull is None,
            'query_string': query_string,
            'display': _('All'),
        }
        include_none = False
        for val in self.lookup_choices:
            if val is None:
                include_none = True
                continue

            val = str(val)
            qval = self.prepare_querystring_value(val)
            yield {
                'selected': qval in self.lookup_vals,
                'query_string': query_string,
                'display': val,
                'value': val,
                'key': self.lookup_kwarg,
            }
        if include_none:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': query_string,
                'display': self.empty_value_display,
                'value': 'True',
                'key': self.lookup_kwarg_isnull,
            }


class MultiSelectRelatedDropdownFilter(MultiSelectRelatedFilter):
    """
    Multi select dropdown filter for relation fields.
    """
    template = 'more_admin_filters/multiselectdropdownfilter.html'

    def choices(self, changelist):
        query_string = changelist.get_query_string({}, [self.lookup_kwarg, self.lookup_kwarg_isnull])
        yield {
            'selected': not self.lookup_vals and not self.lookup_val_isnull,
            'query_string': query_string,
            'display': _('All'),
        }
        for pk_val, val in self.lookup_choices:
            pk_val = str(pk_val)
            yield {
                'selected': pk_val in self.lookup_vals,
                'query_string': query_string,
                'display': val,
                'value': pk_val,
                'key': self.lookup_kwarg,
            }
        if self.include_empty_choice:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': query_string,
                'display': self.empty_value_display,
                'value': 'True',
                'key': self.lookup_kwarg_isnull,
            }


# Filter for annotated attributes.
# NOTE: The code is more or less the same than admin.FieldListFilter but
# we must not subclass it. Otherwise django's filter setup routine wants a real
# model field.
class BaseAnnotationFilter(admin.ListFilter):
    """
    Baseclass for annotation-list-filters.
    """
    attribute_name = None
    nullable_attribute = None

    @classmethod
    def init(cls, attribute_name, nullable=True):
        """
        Since filters are listed as classes in ModelAdmin.list_filter we are
        not able to initialize the filter within the ModelAdmin.
        We use this classmethod to setup a filter-class for a specific annotated
        attribute::

            MyModelAdmin(admin.ModelAdmin):
                list_filter = [
                    MyAnnotationListFilter.init('my_annotated_attribute'),
                ]
        """
        attrs = dict(attribute_name=attribute_name, nullable=nullable)
        cls = type('cls.__name__' + attribute_name, (cls,), attrs)
        return cls

    def __init__(self, request, params, model, model_admin):
        self.title = self.attribute_name
        super().__init__(request, params, model, model_admin)
        for p in self.expected_parameters():
            if p in params:
                value = params.pop(p)
                self.used_parameters[p] = prepare_lookup_value(p, value)

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        try:
            return queryset.filter(**self.used_parameters)
        except (ValueError, ValidationError) as e:
            # Fields may raise a ValueError or ValidationError when converting
            # the parameters to the correct type.
            raise IncorrectLookupParameters(e)


# NOTE: The code is more or less the same than admin.BooleanFieldListFilter but
# we must not subclass it. Otherwise django's filter setup routine wants a real
# model field.
class BooleanAnnotationFilter(BaseAnnotationFilter):
    """
    Filter for annotated boolean-attributes.
    """
    def __init__(self, request, params, model, model_admin):
        self.lookup_kwarg = '%s__exact' % self.attribute_name
        self.lookup_kwarg2 = '%s__isnull' % self.attribute_name
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_val2 = params.get(self.lookup_kwarg2)
        super().__init__(request, params, model, model_admin)
        if (self.used_parameters and self.lookup_kwarg in self.used_parameters and
                self.used_parameters[self.lookup_kwarg] in ('1', '0')):
            self.used_parameters[self.lookup_kwarg] = bool(int(self.used_parameters[self.lookup_kwarg]))

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg2]

    def choices(self, changelist):
        for lookup, title in (
                (None, _('All')),
                ('1', _('Yes')),
                ('0', _('No'))):
            yield {
                'selected': self.lookup_val == lookup and not self.lookup_val2,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_kwarg2]),
                'display': title,
            }
        if self.nullable_attribute:
            yield {
                'selected': self.lookup_val2 == 'True',
                'query_string': changelist.get_query_string({self.lookup_kwarg2: 'True'}, [self.lookup_kwarg]),
                'display': _('Unknown'),
            }
