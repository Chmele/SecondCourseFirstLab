from import_export import resources
from .models import Segment

class SegmentResource(resources.ModelResource):
    class Meta:
        model = Segment