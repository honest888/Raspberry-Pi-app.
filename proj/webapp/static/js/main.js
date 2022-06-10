$(document).ready(function() {
    // Initial data update
    showUpdate(data);

    // Set up relay buttons
    for (var eid in CONFIG.ON_OFF_SCRIPTS) {
        (function(eid) {
            $("#" + eid).click(function() {
                $.post("/run-onoff", {"gpio": CONFIG.ON_OFF_SCRIPTS[eid]})
                .done(function(data) {
                    showUpdate(data);
                });
            });
        })(eid);
    }

    // Other buttons (ie power)
    for (var eid in CONFIG.OTHER_BUTTONS) {
        $("#" + eid).click(function() {
            $.post("/run-other", {"script": CONFIG.OTHER_BUTTONS[eid]})
            .done(function(data) {
                showUpdate(data);
            });
        });
    }

    // Periodically update data
    setInterval(doUpdate, CONFIG.UPDATE_INTERVAL * 1000);

    // Periodically request a humidity update
    setInterval(function() {
        $.post("/run-other", {"script": CONFIG.UPDATE_TEMP})
        .done(function(data) {
            showUpdate(data);
        });
    }, CONFIG.HUMIDITY_INTERVAL * 1000);

    // Button flash animation
    setInterval(function() {
        $(".flash-on-danger").each(function() {
            var $this = $(this);
            if ($this.hasClass("flash1")) {
                $this.removeClass("flash1").addClass("flash2");
            } else {
                $this.removeClass("flash2").addClass("flash1");
            }
        });
    }, CONFIG.FLASH_INTERVAL * 1000);
});

function doUpdate() {
    $.get("/get-data")
    .done(function(data) {
        showUpdate(data);
    })
    .fail(function(resp) {
        console.error("Failed to update data:", resp);
    });
}

function showUpdate(data) {
    // Time
    $("#current-time").text(data.time);

    // Temp
    if (data.temp.Temp) {
        $("#temp").html(data.temp.Temp.replace("*", "&deg;"));
    } else {
        $("#temp").text("?");
    }

    $("#humid").html(data.temp.Humidity || "?"); // Using .html instead of .text so you can style these if you ever choose to

    // GPIO buttons
    for (var eid in data.gpio) {
        var val = data.gpio[eid];
        if (val !== null) {
            $("#" + eid).toggleClass("on", val);
        } else {
            $("#" + eid).removeClass("on");
        }
    }

    // Sensor measurements
    for (var eid in data.measurements) {
        var val = data.measurements[eid];
        if (val !== null) {
            $("#" + eid).find(".text").html(val); // Using .html instead of .text so you can style these if you ever choose to
        } else {
            $("#" + eid).find(".text").text("?");
        }
    }

    // Battery
    if (data.battery.volts !== undefined) {
        // Percent tweening
        var val = getValueFromThreshold(data.battery.volts, CONFIG.BATTERY_THRESHOLDS);
        var nextVal = getNextValueFromThreshold(data.battery.volts, CONFIG.BATTERY_THRESHOLDS);
        console.log("val:", val, "next:", nextVal);
        var percent = val.percent;

        if (nextVal.percent !== val.percent) {
            var diffV = nextVal.measure - val.measure;
            var diffP = nextVal.percent - val.percent;
            var off = (data.battery.volts - val.measure) / diffV;
            percent = percent + diffP * off;
        }

        percent = Math.min(100, Math.max(0, percent));

        // Update display
        $("#battery").find(".text").text(Math.floor(percent) + "% (" + Math.floor(data.battery.volts * 100) / 100 + "V)");
        $("#battery").find(".battery .fill").css({
            "top": (100 - percent) + "%",
            "background-color": val.color
        });

        // Text flashing
        $("#battery_level").find(".text").toggleClass("flashing", data.battery.volts <= CONFIG.BATTERY_FLASH);
    }

    // Gas
    $("#co2").text(data.gas.co2_text);
    $("#co2").toggleClass("flashing", !data.gas.co2_ok);
    $("#gas").text(data.gas.gas_text);
    $("#gas").toggleClass("flashing", !data.gas.gas_ok);
}

function getValueFromThreshold(measure, thresholds) {
    var val = thresholds[0];

    for (var i = 1; i < thresholds.length; i++) { // Skip first; we've already used it as the baseline
        var entry = thresholds[i];
        if (measure >= entry.measure) {
            val = entry;
        }
    }

    return val;
}

function getNextValueFromThreshold(measure, thresholds) {
    var val = thresholds[0];
    var index = 0;

    for (var i = 1; i < thresholds.length; i++) { // Skip first; we've already used it as the baseline
        var entry = thresholds[i];
        if (measure >= entry.measure) {
            val = entry;
            index = i;
        }
    }

    return thresholds[Math.min(thresholds.length - 1, index + 1)];
}
