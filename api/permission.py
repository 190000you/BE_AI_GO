from rest_framework import permissions

class IsOnerAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # URL에서 userId를 추출
        userId = view.kwargs.get('userId')
        # 인증된 사용자의 ID(여기서는 userId 라고 가정)와 URL의 userId가 같은지 확인
        return (str(request.user.userId) == str(userId)) or request.user.is_superuser == True

    def has_object_permission(self, request, view, obj):
        # 객체 수준 권한 검사에서도 동일한 검사 수행
        return obj.userId == request.user.userId or request.user.is_superuser == True
