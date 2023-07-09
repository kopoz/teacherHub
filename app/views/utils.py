from ..models import db

def create_label_like(resource_names, model_class):
    resources = []
    for name in resource_names:
        resource = model_class.query.filter_by(name=name).first()
        if not resource:
            resource = model_class(name=name)
            db.session.add(resource)
        resources.append(resource)
    return resources