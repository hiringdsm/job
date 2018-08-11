def validate(values, data):
    # validation
    validation_errors = []

    for val in values:
        splitted = val.split(":")

        val = splitted[0]
        val_type = splitted[1]

        if val in data:
            if val_type == "integer":
                if not type(data[val]) is int:
                    validation_errors.append("'{}' must be an integer.".format(val))
            elif val_type == "string":
                if not type(data[val]) is str:
                    validation_errors.append("'{}' must be an string.".format(val))
                else:
                    val_min_value = int(splitted[2].split("-")[1])
                    val_max_value = int(splitted[3].split("-")[1])

                    if len(data[val]) < val_min_value:
                        validation_errors.append("'{}' must be at least {} characters in length.".format(val, val_min_value))

                    if len(data[val]) > val_max_value:
                        validation_errors.append("'{}' must not exceed {} characters in length.".format(val, val_max_value))

            elif val_type == "boolean":
                if not type(data[val]) is bool:
                    validation_errors.append("'{}' must be a boolean.".format(val))

        else:
            validation_errors.append("'{}' is required".format(val))
