import sys

from dcim.models import Region
from startup_script_utils import load_yaml, split_params

regions = load_yaml("/opt/netbox/initializers/regions.yml")

if regions is None:
    sys.exit()

optional_assocs = {"parent": (Region, "name")}

for params in regions:

    for assoc, details in optional_assocs.items():
        if assoc in params:
            model, field = details
            query = {field: params.pop(assoc)}

            params[assoc] = model.objects.get(**query)

    matching_params, defaults = split_params(params)
    region, created = Region.objects.get_or_create(**matching_params, defaults=defaults)

    if created:
        print("🌐 Created region", region.name)
