VERSION = (1, 0)
__version__ = ".".join(map(str, VERSION))


from .filters import (
    MultiSelectChoicesFilter, MultiSelectChoicesDropdownFilter,
    MultiSelectFilter, MultiSelectRelatedFilter, MultiSelectDropdownFilter,
    MultiSelectRelatedDropdownFilter, DropdownFilter, ChoicesDropdownFilter,
    RelatedDropdownFilter, BooleanAnnotationFilter
)
