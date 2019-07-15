<!DOCTYPE html>
<html lang="en">
<head>
	<title>PICTOR: Telescope Control</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
	<link rel="stylesheet" type="text/css" href="fonts/Linearicons-Free-v1.0.0/icon-font.min.css">
	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
	<link rel="stylesheet" type="text/css" href="vendor/css-hamburgers/hamburgers.min.css">
	<link rel="stylesheet" type="text/css" href="vendor/animsition/css/animsition.min.css">
	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
	<link rel="stylesheet" type="text/css" href="vendor/daterangepicker/daterangepicker.css">
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
</head>
<body>
	<div class="container-contact100">
		<div class="wrap-contact100">
			<form  action="" class="contact100-form validate-form" method="POST">
				<span class="contact100-form-title">
					PICTOR Telescope Control
					<hr>
				</span>


				<div class="wrap-input100 validate-input" data-validate="Observation name is required">
					<label class="label-input100" for="obs_name">Observation name</label>
					<input id="obs_name" class="input100" type="text" name="obs_name" placeholder="Enter a name for your observation..." required>
					<span class="focus-input100"></span>
				</div>

				<div class="wrap-input100 validate-input" data-validate="Center frequency is required">
					<label class="label-input100" for="f_center">Center frequency (MHz)</label>
					<input id="f_center" class="input100" type="number" name="f_center" min="1300" max="1700" placeholder="Enter the center frequency of your observation..." required>
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
							<option value="1024"  selected="selected">1024</option>
							<option value="2048"  >2048</option>
						</select>
						<div class="dropDownSelect2"></div>
					</div>
					<span class="focus-input100"></span>
				</div>


                <div class="wrap-input100 validate-input" data-validate="Number of bins is required">
                    <label class="label-input100" for="nbins">Number of bins</label>
                    <input id="nbins" class="input100" type="number" name="nbins" min="100" max="100000" placeholder="Enter the number of bins..." required>
                    <span class="focus-input100"></span>
                </div>

				<div class="wrap-input100 validate-input" data-validate="Observing duration is required">
					<label class="label-input100" for="f_center">Duration (sec)</label>
                    <input id="duration" class="input100" type="number" name="duration" min="10" max="36000" placeholder="Enter the duration of your observation..." required>
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
					<button class="contact100-form-btn"  name="submit_btn">
                        Submit
					</button>
				</div>
				<div id="currentlyInUseMessage" style="display:none; color: red">
					The telescope is currently observing. Please wait until it's done before submitting your observation!
				</div>
				<hr>
				PICTOR is a free-to-use open source radio telescope that allows anyone to make continuous and spectral drift-scan observations of the radio sky in the 1300~1700 MHz regime.
        <br><br>
				<p style="font-size:95%;">Contact: <a style="font-size:95%;" href="mailto:0xcoto@protonmail.com">0xcoto@protonmail.com</a></p>
				<p style="font-size:95%;">GitHub: <a style="font-size:95%;" href="https://github.com/0xCoto/PICTOR" target="_blank">https://github.com/0xCoto/PICTOR</a></p>
			</form>

			<div class="contact100-more flex-col-c-m" style="background-image: url('images/bg-01.jpg');">
			</div>
		</div>
	</div>





	<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
	<script src="vendor/animsition/js/animsition.min.js"></script>
	<script src="vendor/bootstrap/js/popper.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
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
	<script src="vendor/daterangepicker/moment.min.js"></script>
	<script src="vendor/daterangepicker/daterangepicker.js"></script>
	<script src="vendor/countdowntime/countdowntime.js"></script>
	<script src="js/main.js"></script>


<script>

$(function() {
    getLastObservedFile(parseLastObservedFileAndUpdateUi);
});

function getLastObservedFile(callback)
{
    $.get("/last_obs.txt", function(data) { callback(data); } );
}
function parseLastObservedFileAndUpdateUi(fileContents) {
    var lines = fileContents.split("\n");

    var durationLine = lines[5];
    var durationInSeconds = parseInt(durationLine.split("=")[1].replace("'", ""));

    var startTimeLine = lines[8];
    var startTimeInSeconds = parseInt(startTimeLine.split("=")[1].replace("'", ""));

    var currentTimeUnix = Math.round((new Date()).getTime() / 1000);
    var timeToWait = startTimeInSeconds - currentTimeUnix + durationInSeconds;

	$(".contact100-form-btn").hide();
	$("#currentlyInUseMessage").show();

    setTimeout(
      function()
      {
        $(".contact100-form-btn").show();
		$("#currentlyInUseMessage").hide();
      }, timeToWait * 1000);
}

</script>
</body>
</html>
<?php
if(isset($_REQUEST['submit_btn']))
{


    //Getting all the values
    $date = new DateTime();
    $obs_name = $_POST["obs_name"];
    $f_center= $_POST["f_center"];
    $bandwidth = $_POST["bandwidth"];
    $obs_datetime = $_POST["obs_datetime"];
    $channels = $_POST["channels"];
    $nbins = $_POST["nbins"];
    $duration = $_POST["duration"];
    $email = $_POST["email"];
    $check = random_int(10000000, 99999999);
    $time = $date->getTimestamp();

    //Writing away
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



    fclose($myfile);

    $message = "Your observation request has been successfully submitted! Once the observation is carried out, you will receive an email with the observation data.";
    echo "<script type='text/javascript'>alert('$message');</script>";



}

?>
