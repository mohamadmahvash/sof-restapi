from rest_framework.metadata import BaseMetadata

class CustomMetaData(BaseMetadata):
    def determine_metadata(self, request, view):
        return {}