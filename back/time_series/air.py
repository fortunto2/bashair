from statistics import mean

from config.influx import query_api


def get_air_values_mean(bucket='air', field='pm25', start='-1h', measurement="air"):
    print(bucket, field, start)
    field_mean = None

    tables = query_api.query(
        f"""
        from(bucket: "{bucket}")
          |> range(start: {start})
          |> filter(fn: (r) => r["_measurement"] == "{measurement}")
          |> filter(fn: (r) => r["_field"] == "{field}")
          |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
          |> yield(name: "mean")
        """
    )

    if tables:
        field_mean = round(mean([table.records[0]['_value'] for table in tables]), 1)
        print(field_mean)

    # for table in tables:
    #     print('-----------')
    #     for row in table.records:
    #         pprint(row.values)

    return field_mean


if __name__ == "__main__":

    get_air_values_mean(field='pm25')
    get_air_values_mean(field='pm10')
    get_air_values_mean(field='aqi')
    get_air_values_mean(field='temperature')
