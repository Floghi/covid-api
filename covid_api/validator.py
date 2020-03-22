from db import allowed_countries
# validators
class ValidationFailed(Exception):
  def __init__(self, message):
    self.message = message

def validate_list_input(data):
  if "size" not in data:
    raise ValidationFailed("size parameter is mandatory.")
  try:
    int(data["size"])
  except:
    raise ValidationFailed("size must be a integer.")
  if "sort" not in data:
    raise ValidationFailed("sort parameter is mandatory.")
  if data["sort"] not in ["asc", "desc"]:
    raise ValidationFailed("sort is an enum value [asc, desc].")
  if "offset" in data:
    try:
      int(data["offset"])
    except:
      raise ValidationFailed("offset must be a integer.")
  if "country" in data:
    if data["country"] not in allowed_countries + ["null"]:
        raise ValidationFailed("country is an enum value {}".format(allowed_countries + ["null"]))


def validate_statistics_input(data):
  if "size" not in data:
    raise ValidationFailed("size parameter is mandatory.")
  try:
    int(data["size"])
  except:
    raise ValidationFailed("size must be a integer.")
  if "sort" not in data:
    raise ValidationFailed("sort parameter is mandatory.")
  if data["sort"] not in ["asc", "desc"]:
    raise ValidationFailed("sort is an enum value [asc, desc].")
  if "offset" in data:
    try:
      int(data["offset"])
    except:
      raise ValidationFailed("offset must be a integer.")

