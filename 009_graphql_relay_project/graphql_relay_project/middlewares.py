from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTMiddleware:
    
    # 認証が必要なリゾルバ
    protected_resolvers = ('createColumn', 'updateColumn', 'deleteColumn')
    
    def resolve(self, next, root, info, **args):
        if info.field_name not in self.protected_resolvers:
            return next(root, info, **args)
        
        # 認証処理
        request = info.context
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            raise Exception('認証情報がありません')
        try:
            # トークンの検証
            user_auth_tuple = JWTAuthentication().authenticate(request) # (user, token)
            # print(user_auth_tuple)
            info.context.user = user_auth_tuple[0]
        except Exception as e:
            raise e
        return next(root, info, **args)