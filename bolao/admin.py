from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import BettingPool, AccessToken

@admin.register(BettingPool)
class BettingPoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'is_active', 'total_tokens', 'active_tokens')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    actions = ['generate_tokens']

    def total_tokens(self, obj):
        return obj.access_tokens.count()
    total_tokens.short_description = 'Total de Tokens'

    def active_tokens(self, obj):
        return obj.access_tokens.filter(is_active=True).count()
    active_tokens.short_description = 'Tokens Ativos'

    def generate_tokens(self, request, queryset):
        total = 0
        for pool in queryset:
            # Gera 5 tokens para cada bolão selecionado
            for _ in range(5):
                # Token válido por 7 dias e pode ser usado apenas uma vez
                expires = timezone.now() + timedelta(days=7)
                pool.generate_access_token(max_uses=1, expires_at=expires)
                total += 1
        
        self.message_user(request, f'{total} tokens foram gerados com sucesso!')
    generate_tokens.short_description = 'Gerar tokens de acesso (5 por bolão)'

@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'pool', 'created_at', 'expires_at', 'max_uses', 'uses', 'is_active', 'is_valid_status')
    list_filter = ('is_active', 'pool', 'created_at')
    search_fields = ('token', 'pool__name')
    readonly_fields = ('token', 'created_at', 'uses')
    actions = ['deactivate_tokens', 'extend_expiration']

    def is_valid_status(self, obj):
        return obj.is_valid()
    is_valid_status.boolean = True
    is_valid_status.short_description = 'Válido'

    def deactivate_tokens(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} tokens foram desativados.')
    deactivate_tokens.short_description = 'Desativar tokens selecionados'

    def extend_expiration(self, request, queryset):
        # Estende a validade dos tokens por mais 7 dias
        for token in queryset:
            if token.expires_at:
                token.expires_at = token.expires_at + timedelta(days=7)
            else:
                token.expires_at = timezone.now() + timedelta(days=7)
            token.save()
        
        self.message_user(request, f'Data de expiração estendida para {queryset.count()} tokens.')
    extend_expiration.short_description = 'Estender validade por 7 dias'
