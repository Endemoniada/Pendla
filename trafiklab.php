<?php

// Input
$api = $_GET['api'];            // options:  realtimedepartures
                                //           typeahead
$url = False;

// Get JSON data
if ($api == "realtimedepartures") {
    // API-nyckel för pendla.py
    $api_key = "72e87e92af514d73830ba8cf89b8197d";

    $siteid = $_GET['siteid'];
    $url = "http://api.sl.se/api2/realtimedepartures.json?key=".$api_key."&siteid=".$siteid."&timewindow=60";
}
else if ($api == "typeahead") {
    // API-nyckel för findstation.py
    $api_key = "e24b05ad190347b3aa55284738027712";

    $searchstring = $_GET['searchstring'];
    $stationsonly = $_GET['stationsonly'];
    $maxresults = $_GET['maxresults'];
    $url = "http://api.sl.se/api2/typeahead.json?key=".$api_key."&searchstring=".$searchstring."&stationsonly=".$stationsonly."&maxresults=".$maxresults;
}
else {
    http_response_code(404);    # Bad Request
    exit();
}

// Output
if ($url != False) {
    $handle = fopen($url, "rb");
    $api_data = stream_get_contents($handle);
    echo $api_data;
}
else {
    http_response_code(404);    # Bad Request
    exit();
}

?>
