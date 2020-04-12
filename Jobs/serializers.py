from rest_framework import serializers
from Jobs.models import ArtistCategory, Artist


class ArtistCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ArtistCategory
        fields = ('id','name', 'details','summary', 'image','no_providers','total_transactions_amount', 'reviews','no_running_services')


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id','details','location','job_delivery_time',
                  'pictures','budget','job_category_id',
                #   'created_by','status',
                  'base_charge_amount',
                  'job_category',
                #   'provider_arrival','before_pictures','after_pictures','part_replacement_required','provider_job_cost',
                #   'agree_job_cost','user_provided_cost','total_cost', 'provider_complete_job','user_signoff_on_job',
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