from rest_framework import serializers
from Jobs.models import ArtistCategory, Artist


class ArtistCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ArtistCategory
        fields = ('id','name', 'details')


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id','first_name','last_name','stage_name',
                  'pictures','price','category',
                # 'is_active',
                )

        extra_kwargs ={
            'id': {
                'read_only': True
        }
        }
# class JobMaterialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= JobMaterial
#         fields=('job', 'name', 'price', 'picture',)