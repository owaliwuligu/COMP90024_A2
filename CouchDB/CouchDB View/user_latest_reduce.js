function (keys, values, rereduce) {
    var latest = "Mon Jan 01 00:00:00 +0000 1000";
    for (time in values)
    {
        var strs_latest = new Array();
        strs_latest = latest.split(" ");
        var strs_time = new Array();
        strs_time = values[time].split(" ");
        if (strs_latest[7] < strs_time[7])
        {
            latest = values[time];
        }
        else if (strs_latest[7] == strs_time[7])
        {
            var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            if (months.indexOf(strs_latest[1]) < months.indexOf(strs_time[1]))
            {
                latest = values[time];
            }
            else if (months.indexOf(strs_latest[1]) == months.indexOf(strs_time[1]))
            {
                if (strs_latest[2] < strs_time[2])
                {
                    latest = values[time];
                }
                else if (strs_latest[2] == strs_time[2])
                {
                    if (strs_latest[3] < strs_time[3])
                    {
                        latest = values[time];
                    }
                }
            }
        }
    }
    return latest;
}
