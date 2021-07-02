<?php 
$pictorIsDown = false;
foreach (json_decode(file_get_contents("https://discordapp.com/api/guilds/644685390116290560/widget.json"), true)['members'] as $user) {
    if ($user["username"] == 'PICTOR') {
        $pictorIsDown = true;
    }
}
$statusFile = fopen("checkStatus.txt", "w") or die("Unable to open file!");
if($pictorIsDown){
    fwrite($statusFile,"true");

}else{
    fwrite($statusFile,"false"); // pictor down
}

fclose($statusFile);


?><!DOCTYPE html>
<html lang="en">
<head>
    <title>PICTOR: Telescope Control</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!--===============================================================================================-->
    <link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="fonts/Linearicons-Free-v1.0.0/icon-font.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="vendor/css-hamburgers/hamburgers.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="vendor/animsition/css/animsition.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="vendor/daterangepicker/daterangepicker.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="css/util.css">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <!--===============================================================================================-->
</head>
<body>
<div class="container-contact100">
    <div class="wrap-contact100">
        <form  action="" class="contact100-form validate-form" method="POST">
				<span class="contact100-form-title">
					PICTOR Telescope Control
					<hr>
				<center><font color="1E90FF" size="4"><b>ⓘ New to radio astronomy?</b></font><font color="1E90FF" size="3"><br>Click <b><u><a href="Observing_the_radio_sky_with_PICTOR.pdf" target="_blank"><font color="7BB33A" size="3">here</font></a></u></b> to learn how to use <b>PICTOR</b> and observe the radio sky!<hr></font>
                    <?php
                    $html_from_git = file_get_contents("https://raw.githubusercontent.com/0xCoto/PICTOR/master/position.html");
                    print $html_from_git;
                    ?>
                </center></span>


            <div class="wrap-input100 validate-input" data-validate="Observation name is required">
                <label class="label-input100" for="obs_name">Observation name</label>
                <input id="obs_name" class="input100" type="text" name="obs_name" placeholder="Enter a name for your observation..." required>
                <span class="focus-input100"></span>
            </div>

            <div class="wrap-input100 validate-input" data-validate="Center frequency is required">
                <label class="label-input100" for="f_center">Center frequency (MHz)</label>
                <input id="f_center" class="input100" type="number" name="f_center" min="1300" max="1700" placeholder="Enter the center frequency of your observation..." value="1420" required>
                <span class="focus-input100"></span>
            </div>

            <div class="wrap-input100">
                <div class="label-input100">Bandwidth</div>
                <div>
                    <select class="js-select2" name="bandwidth">
                        <option value="500khz">500 kHz</option>
                        <option value="1mhz">1 MHz</option>
                        <option value="2mhz">2 MHz</option>
                        <option value="2.4mhz" selected="selected">2.4 MHz</option>
                        <option value="3.2mhz">3.2 MHz</option>
                    </select>
                    <div class="dropDownSelect2"></div>
                </div>
                <span class="focus-input100"></span>
            </div>

            <div class="wrap-input100">
                <div class="label-input100">Number of channels</div>
                <div>
                    <select class="js-select2" name="channels">
                        <option value="256" >256</option>
                        <option value="512" >512</option>
                        <option value="1024">1024</option>
                        <option value="2048" selected="selected">2048</option>
                    </select>
                    <div class="dropDownSelect2"></div>
                </div>
                <span class="focus-input100"></span>
            </div>


            <div class="wrap-input100 validate-input" data-validate="Number of bins is required">
                <label class="label-input100" for="nbins">Number of bins</label>
                <input id="nbins" class="input100" type="number" name="nbins" min="100" max="20000" placeholder="Enter the number of bins..." value="100" required="">
                <span class="focus-input100"></span>
            </div>

            <div class="wrap-input100 validate-input" data-validate="Observing duration is required">
                <label class="label-input100" for="f_center">Duration (sec)</label>
                <input id="duration" class="input100" type="number" name="duration" min="10" max="600" placeholder="Enter the duration of your observation..." required="">

                <span class="focus-input100"></span>
            </div>

            <div class="wrap-input100">
                <div class="label-input100">Would you like to receive your raw data as a .csv file?</div>
                <div>
                    <select class="js-select2" name="raw_data">
                        <option value="0" selected="selected">No</option>
                        <option value="1">Yes</option>
                    </select>
                    <div class="dropDownSelect2"></div>
                </div>
                <span class="focus-input100"></span>
            </div>

            <hr>
            Please enter an email address to get notified once the observation is complete.<p style="font-size:3px;">&emsp;</p>
            <div class="wrap-input100 validate-input" data-validate = "A valid email is required.">
                <label class="label-input100" for="email">Email Address</label>
                <input id="email" class="input100" type="text" name="email" placeholder="Enter your email..." required>
                <span class="focus-input100"></span>
            </div>

            <div class="container-contact100-form-btn">
            <button class='contact100-form-btn' name='submit_btn'>Submit</button></div>
            <div id="currentlyInUseMessage" style="display:none; color: orangered">
                The telescope is currently observing. Please wait until it's done before submitting your observation!
            </div>
            <div id="currentlyOffline" style="display:none; color: red">
                The telescope is currently under maintenance. Please check back in a few hours!
            </div>

            <!-- <hr><font color="#ff6348" size="3"><b>🚀 <font color="#e84118" size="3"><u>NEW</u>:</font></b> You can now <u><a href="https://community.pictortelescope.com" target="_blank"><font color="#05c46b" size="3"><b>join the PICTOR Community</b></font></a></u> and share your observations with others!</font>
-->
<hr>
            <b>PICTOR</b>, located in <b>Agrinio, Greece</b>, is a free-to-use open source radio telescope that allows anyone to make continuous and spectral drift-scan observations of the radio sky in the <b>1300~1700 MHz</b>  regime. Special thanks to Konstantinos Bakolitsas for providing his dish.

            <br><br>
            <p style="font-size:95%;">Contact: <a style="font-size:95%;" href="mailto:0xcoto@protonmail.com">0xcoto@protonmail.com</a></p>
            <p style="font-size:95%;">GitHub: <a style="font-size:95%;" href="https://github.com/0xCoto/PICTOR" target="_blank">https://github.com/0xCoto/PICTOR</a></p>
            <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
        </form>

        <div class="contact100-more flex-col-c-m" style="background-image: url('images/bg-01.jpg');">
        </div>
    </div>
</div>





<!--===============================================================================================-->
<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
<script src="vendor/animsition/js/animsition.min.js"></script>
<!--===============================================================================================-->
<script src="vendor/bootstrap/js/popper.js"></script>
<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
<script src="vendor/select2/select2.min.js"></script>
<script>
    $(".js-select2").each(function(){
        $(this).select2({
            minimumResultsForSearch: 20,
            dropdownParent: $(this).next('.dropDownSelect2')
        });
    })
    $(".js-select2").each(function(){
        $(this).on('select2:open', function (e){
            $(this).parent().next().addClass('eff-focus-selection');
        });
    });
    $(".js-select2").each(function(){
        $(this).on('select2:close', function (e){
            $(this).parent().next().removeClass('eff-focus-selection');
        });
    });

</script>
<!--===============================================================================================-->
<script src="vendor/daterangepicker/moment.min.js"></script>
<script src="vendor/daterangepicker/daterangepicker.js"></script>
<!--===============================================================================================-->
<script src="vendor/countdowntime/countdowntime.js"></script>
<!--===============================================================================================-->
<script src="js/main.js"></script>


<script>


    $(function() {
        getLastObservedFile(parseLastObservedFileAndUpdateUi);
        getStatusFile(parseStatus);
    });

    function getLastObservedFile(callback)
    {
        $.get("/last_obs_duration.txt", function(data) { callback(data); } );
    }
    function getStatusFile(callback)
    {
        $.get("/checkStatus.txt", function(data) { callback(data); } );
    }
    function parseStatus(fileContents) {
        var status = fileContents

        if (1==1) {
            $("#currentlyOffline").hide();
            $("#currentlyInUseMessage").hide();
            $(".contact100-form-btn").show();
            online = true;
        }
        else if (status == "false") {
            //$(".contact100-form-btn").hide();
            $("#currentlyInUseMessage").hide();
            $("#currentlyOffline").show();
            online = false;
        }
    }
    function parseLastObservedFileAndUpdateUi(fileContents) {
        var lines = fileContents.split("\n");


        var durationLine = lines[5];
        var durationInSeconds = parseInt(durationLine.split("=")[1].replace("'", ""));

        var startTimeLine = lines[7];
        var startTimeInSeconds = parseInt(startTimeLine.split("=")[1].replace("'", ""));

        var currentTimeUnix = Math.round((new Date()).getTime() / 1000);
        var timeToWait = startTimeInSeconds - currentTimeUnix + durationInSeconds;

        //$(".contact100-form-btn").hide();
        $("#currentlyInUseMessage").show();

        setTimeout(
            function()
            {
                if (online) {
                    $(".contact100-form-btn").show();
                    $("#currentlyInUseMessage").hide();
                }
            }, timeToWait * 1000);
    }

</script>
</body>
</html>

<?php
if(isset($_REQUEST['submit_btn']))
{
    // getting all the value's
    $date = new DateTime();
    $obs_name = $_POST["obs_name"];
    $f_center= $_POST["f_center"];
    $bandwidth = $_POST["bandwidth"];

    $channels = $_POST["channels"];
    $nbins = $_POST["nbins"];
    $duration = $_POST["duration"];
    $email = $_POST["email"];
    $check = random_int(10000000, 99999999);
    $time = $date->getTimestamp();
	if(isset($_POST["raw_data"]) && $_POST["raw_data"] == "1"){
		$data = 1;
	}
	else {
		$data = 0;
	}
    // Writing away
    $writeObs = fopen("last_obs_duration.txt", "w") or die("Unable to open file!");
    fwrite($writeObs, "obs_name="."'"."0"."'"."\n");
    fwrite($writeObs, "f_center="."'"."0"."'"."\n");
    fwrite($writeObs, "bandwidth="."'"."0"."'"."\n");
    fwrite($writeObs, "channels="."'"."0"."'"."\n");
    fwrite($writeObs, "nbins="."'"."0"."'"."\n");
    fwrite($writeObs, "duration="."'".$duration."'"."\n");
    fwrite($writeObs, "id="."'"."0"."'"."\n");
    fwrite($writeObs, "obs_time="."'". $time."'"."\n");
    fclose($writeObs);
    
    $myfile = fopen("last_obs.txt", "w") or die("Unable to open file!");
    fwrite($myfile, "obs_name="."'".$obs_name."'"."\n");
    fwrite($myfile, "f_center="."'".$f_center."'"."\n");
    fwrite($myfile, "bandwidth="."'".$bandwidth."'"."\n");
    fwrite($myfile, "channels="."'".$channels."'"."\n");
    fwrite($myfile, "nbins="."'".$nbins."'"."\n");
    fwrite($myfile, "duration="."'".$duration."'"."\n");
    fwrite($myfile, "email="."'".$email."'"."\n");
    fwrite($myfile, "id="."'".$check."'"."\n");
    fwrite($myfile, "obs_time="."'". $time."'"."\n");
	fwrite($myfile, "raw_data="."'". $data."'"."\n");
    fclose($myfile);

    $message = "Your observation request has been successfully submitted! Once the observation is carried out, you will receive an email with the observation data.";
    echo "<script type='text/javascript'>alert('$message');</script>";



}

?>
