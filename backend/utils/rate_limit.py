class MockLimiter:
    def limit(self, limit_value):
        def decorator(func):
            return func
        return decorator

limiter = MockLimiter()

