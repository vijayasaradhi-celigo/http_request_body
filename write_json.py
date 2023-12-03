import json

records = []

# Zoom Create Meeting
connector_name = "Zoom"
connector_endpoint = "Create a meeting template from an existing meeting"
connector_uri = "POST /v2/users/:_userId/meeting_templates"
connector_uid = connector_name + ": " + connector_endpoint
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

obj["uid"] = connector_uid
records.append(obj)


# 3PL Create  a item for specific customer
connector_name = "3PL Central"
connector_endpoint = "create a item for specific customer"
connector_uri = "POST /customers/:_customerid/items"
connector_uid = connector_name + ": " + connector_endpoint
export_record = {
    "price": "300",
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
obj["uid"] = connector_uid
records.append(obj)


connector_name = "SmartRecruiters"
connector_endpoint = "Shares new messages on hireloop with users, hiring \
        teams or everyone and sends emails."

connector_uri = "POST /messages/shares"
import_fields = [
    "content",
    "correlationId",
    "shareWith.users",
    "shareWith.hiringTeamOf",
    "shareWith.everyone",
    "shareWith.openNote",
]
obj = {}
connector_uid = connector_name + ": " + connector_endpoint
export_record = {
    "content": "Test content",
    "correlation_id": 1024,
    "share_with_users": True,
    "share_with_hiring_team": True,
    "share_with_everyone": True,
    "share_with_opennote": True,
}
obj["connector_name"] = connector_name
obj["connector_endpoint"] = connector_endpoint
obj["connector_uri"] = connector_uri
obj["export_record"] = export_record
obj["import_fields"] = import_fields
obj["uid"] = connector_uid
records.append(obj)


connector_name = "Meta"
connector_endpoint = "Copy of a campaign"
connector_uri = "POST /:_campaign_id/copies"

import_fields = [
    "deep_copy",
    "end_time",
    "rename_options.rename_strategy",
    "rename_options.rename_prefix",
    "rename_options.rename_suffix",
    "start_time",
    "status_option",
]
obj = {}

connector_uid = connector_name + ": " + connector_endpoint
export_record = {
    "do_deep_copy": "True",
    "campaign_end_time": "Dec 15, 2023 12:00:00",
    "rename_strategy": "Auto",
    "rename_prefix": "Backup_",
    "rename_suffix": "meeting",
    "campaign_begin_time": "Dec 1, 2023 12:00:00",
    "status_option": "St Opt",
}
obj["connector_name"] = connector_name
obj["connector_endpoint"] = connector_endpoint
obj["connector_uri"] = connector_uri
obj["export_record"] = export_record
obj["import_fields"] = import_fields
obj["uid"] = connector_uid
records.append(obj)

connector_name = "Zoom"
connector_endpoint = "Create users"
connector_uri = "POST /v2/users"
import_fields = [
    "action",
    "user_info.email",
    "user_info.type",
    "user_info.first_name",
    "user_info.last_name",
    "user_info.display_name",
    "user_info.password",
    "user_info.plan_united_type",
    "user_info.feature.zoom_phone",
    "user_info.feature.zoom_one_type",
]  # fields= 11
obj = {}

connector_uid = connector_name + ": " + connector_endpoint
export_record = {
    "user_action": "Create",
    "email": "abc@gmail.com",
    "first_name": "Vijayasaradhi",
    "last_name": "Indurthi",
    "display_name": "Vijay",
    "password": "No idea",
    "type": "Regular",
    "plan_type": "Regular",
    "zoom_phone": "Zoom phone number",
    "zoom_type": "Zoom Type",
}
obj["connector_name"] = connector_name
obj["connector_endpoint"] = connector_endpoint
obj["connector_uri"] = connector_uri
obj["export_record"] = export_record
obj["import_fields"] = import_fields
obj["uid"] = connector_uid
records.append(obj)


fp = open("dataset.json", "w")
fp.write(json.dumps(records) + "\n")
fp.close()
