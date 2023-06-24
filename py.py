class TransferSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField()
    from_user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    def get_from_user(self, obj):
        return obj.from_user.username

    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_user'].queryset = (
                self.fields['from_user'].queryset.filter(
                    username=self.context['request'].user.username)
            )

    def validate(self, data):
        try:
            data['to_user'] = User.objects.get(username=data['to_user'])
        except Exception:
            raise serializers.ValidationError(
                "Нет такого пользователя")
        return data

    class Meta:
        model = Transfer
        fields = ('id', 'from_user', 'to_user', 'amount')
        read_only_fields = ('id', )
