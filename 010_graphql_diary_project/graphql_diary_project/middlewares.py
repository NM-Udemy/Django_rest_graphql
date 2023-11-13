from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTMiddleware:
    
    protected_resolvers = ('createDiary', 'updateDiary', 'deleteDiary')
    
    def resolve(self, next, root, info, **args):
        if info.field_name not in self.protected_resolvers:
            return next(root, info, **args)

        request = info.context
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            raise Exception('認証情報がありません')
        try:
            user_auth_tuple = JWTAuthentication().authenticate(request)
            info.context.user = user_auth_tuple[0]
        except Exception as e:
            raise e
        return next(root, info, **args)
