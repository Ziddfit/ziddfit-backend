class AnalyticsReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Only the 'analytics' app reads from the replica.
        Everything else (Plan, Users, etc.) stays on the main DB.
        """
        if model._meta.app_label == 'analytics':
            return 'replica'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Safety First: Always write to the primary 'default' DB.
        Replicas are read-only; trying to write to them will crash your app.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow connections between models because 'replica' is a mirror of 'default'.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Migrations only ever happen on the 'default' DB. 
        Postgres handles the syncing to the replica automatically.
        """
        return db == 'default'