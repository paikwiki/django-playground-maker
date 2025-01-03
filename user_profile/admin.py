from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = _("프로필")
    verbose_name_plural = _("프로필 목록")
    fields = ("nickname", "description", "profile_image", "profile_image_preview")

    readonly_fields = ("profile_image_preview",)

    def profile_image_preview(self, instance):
        image_url = (
            instance.profile_image.url
            if instance.profile_image
            else "/static/images/profile.png"
        )

        return mark_safe(
            f'<img src="{image_url}" style="max-width: 140px; height: auto;" />'
        )

    profile_image_preview.allow_tags = True
    profile_image_preview.short_description = _("프로필 이미지 미리보기")


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("개인 정보"), {"fields": ("first_name", "last_name", "email")}),
        (_("로그인 이력"), {"fields": ("last_login", "date_joined")}),
    )

    readonly_fields = ("last_login", "date_joined")

    def description(self, instance):
        return (
            instance.user_profile.description
            if hasattr(instance, "user_profile")
            else "No description"
        )

    def profile_image(self, instance):
        if hasattr(instance, "user_profile") and instance.user_profile.profile_image:
            return instance.user_profile.profile_image.url
        return "No profile image"

    description.short_description = "Profile Description"
    profile_image.short_description = "Profile Image URL"


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
