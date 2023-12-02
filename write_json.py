import json

records = []

# Zoom Create Meeting
connector_name = "Zoom"
connector_endpoint = "Create a meeting"
export_record = {
    "id": "1048576",
    "meeting_name": "Daily Standup meeting",
    "repeat": "True",
    "override": "True",
}
import_fields = ["meeting_id", "name", "save_recurrence", "overwrite"]

obj = {}
obj["connector_name"] = connector_name
obj["connector_endpoint"] = connector_endpoint
obj["export_record"] = export_record
obj["import_fields"] = import_fields

records.append(obj)


# 3PL Create  a item for specific customer
connector_name = "3PL Central"
connector_endpoint = "create a item for specific customer"
export_record = {
    "price": "300",
    "currency": "Dollar",
    "item": {"sku": "123456", "description": "The best item"},
    "inventory": {
        "unit_identifier": "Inv U id",
        "inventory_method": "Inv meth",
        "inventory_also": "True",
    },
    "secondary_unit": {"unit_identifier": "Count", "inventory_units_per_unit": 10},
    "package_unit": {
        "imperial": {
            "net_weight": "200g",
            "length": "30cm",
            "width": "20cm",
            "height": "40cm",
            "weight": "300g",
        },
        "unit_identifier": {"name": "cm"},
        "inventory_units_per_unit": "100",
    },
}
import_fields = [
    "sku",
    "description",
    "options.inventoryUnit.unitIdentifier.name",
    "options.inventoryUnit.inventoryMethod",
    "options.secondaryUnit.inventoryAlso",
    "options.secondaryUnit.unitIdentifier.name",
    "options.secondaryUnit.inventoryUnitsPerUnit",
    "options.packageUnit.imperial.netWeight",
    "options.packageUnit.imperial.length",
    "options.packageUnit.imperial.width",
    "options.packageUnit.imperial.height",
    "options.packageUnit.imperial.weight",
    "options.packageUnit.unitIdentifier.name",
    "options.packageUnit.inventoryUnitsPerUnit",
]

obj = {}
obj["connector_name"] = connector_name
obj["connector_endpoint"] = connector_endpoint
obj["export_record"] = export_record
obj["import_fields"] = import_fields

records.append(obj)


fp = open("dataset.json", "w")
fp.write(json.dumps(records) + "\n")
fp.close()
