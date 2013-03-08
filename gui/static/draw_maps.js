var head_heatmap = null;
var tohead_heatmap = null;
var config = {


};
var first_half_len = 100;
var second_half_len = 100;

window.onload = function drawField() {
	var right_upper = $("#right_upper");
	var right_lower = $("#right_lower");

	var paper_upper = new Raphael(document.getElementById('right_upper'), right_upper.width(), right_upper.height());
	var paper_lower = new Raphael(document.getElementById('right_lower'), right_lower.width(), right_lower.height());

	var rect_upper = paper_upper.rect(0, 0, right_upper.width(), right_upper.height());
	var rect_lower = paper_lower.rect(0, 0, right_lower.width(), right_lower.height());

	rect_upper.attr(
		{
			fill: "#FFFFFF",
		}
	);

	rect_lower.attr(
		{
			fill: "#FFFFFF",
		}
	);


	var left_goal_upper = paper_upper.rect(0, 155, 30, 80);
	left_goal_upper.attr(
		{
			fill: "#FFF",
		}
	);
	var left_goal_lower = paper_lower.rect(0, 155, 30, 80);
	left_goal_lower.attr(
		{
			fill: "#FFF",
		}
	);
	var right_goal_upper = paper_upper.rect(550, 155, 30, 80);
	right_goal_upper.attr(
		{
			fill: "#FFF",
		}
	);
	var right_goal_lower = paper_lower.rect(550, 155, 30, 80);
	right_goal_lower.attr(
		{
			fill: "#FFF",
		}
	);
	
	var mid_line_upper = paper_upper.path("M290 0 L290 390");
	var mid_line_lower = paper_lower.path("M290 0 L290 390");	

	var mid_circle_upper = paper_upper.circle(290, 195, 35);
	var mid_circle_lower = paper_lower.circle(290, 195, 35);

	var left_d_upper = paper_upper.rect(0, 80, 100, 230); 
	var left_d_lower = paper_lower.rect(0, 80, 100, 230);
	var right_d_upper = paper_upper.rect(480, 80, 100, 230);
	var right_d_lower = paper_lower.rect(480, 80, 100, 230);

	var left_dot = paper_upper.circle(290, 195, 1);
	var right_dot = paper_lower.circle(290, 195, 1);
	
	var left_dcircle_upper = paper_upper.path("M100 165C100 165 130 195 100 225");
	var left_dcircle_lower = paper_lower.path("M100 165C100 165 130 195 100 225");

	var right_dcircle_upper = paper_upper.path("M480 165C480 165 450 195 480 225");
	var right_dcircle_lower = paper_lower.path("M480 165C480 165 450 195 480 225");
};

function clearCanvas() {
	var canvas;
	if($("#right_upper canvas").length) {
		$("#right_upper canvas").remove();
	}
	if($("#right_lower canvas").length) {
		$("#right_lower canvas").remove();
	}
	$("#right_upper_pass_count").html("");
	$("#right_lower_pass_count").html("");

};

function doNothing(data) {
	$("#loader").hide();
};

function updateTimes(time) {
	first_half_len = time.time1;
	second_half_len = time.time2;
};

function drawHeatMaps(data) {
		clearCanvas();

	    // heatmap configuration
	    var head_config = {
	        element: document.getElementById("right_upper"),
	        radius: 15,
	        opacity: 100,
			gradient: data.gradient_head
	    };
	    
	    //creates and initializes the heatmap
	    head_heatmap = h337.create(head_config);		 
	    head_heatmap.store.setDataSet(data.data_head);

	    //Doing it for tohead now
	    var tohead_config = {
	        element: document.getElementById("right_lower"),
	        radius: 15,
	        opacity: 100,
			gradient: data.gradient_tohead
	    };
	    
	    //creates and initializes the heatmap
	    tohead_heatmap = h337.create(tohead_config);
	    tohead_heatmap.store.setDataSet(data.data_tohead);
	    $("#loader").hide();

};
function drawPassMaps(data) {
	// data contains head and tohead
	// data = {'head':[(x1,y1,x2,y2), (x1,y1,x2,y2)....], 'tohead':[(x1,y1,x2,y2), (x1,y1,x2,y2), ...]}
	clearCanvas();
	$("#loader").hide();
	// Drawing starts here
	var canvas_html = "<canvas width='580' height='390' style='position: absolute; top: 0px; left: 0px; z-index: 10000000;''></canvas>";
	$("#right_upper").append(canvas_html);
	$("#right_lower").append(canvas_html);
	var ctx1 = $("#right_upper canvas")[0].getContext('2d');

	var data_head = data['head'];
	var data_tohead = data['tohead'];	

	var head_pass_count = 0;
	var tohead_pass_count = 0;
	for(var i=0;i<data_head.length;i++) {
		var x1 = data_head[i][0];
		var y1 = data_head[i][1];
		var x2 = data_head[i][2];
		var y2 = data_head[i][3];

		ctx1.beginPath();
		ctx1.moveTo(x1,y1);
		ctx1.lineTo(x2,y2);
		ctx1.stroke();

		ctx1.beginPath();
	    ctx1.arc(x1, y1, 4, 0, 2 * Math.PI, false);
	    ctx1.fillStyle = 'green';
	    ctx1.fill();
	    ctx1.stroke();

	    head_pass_count++;

	}

	var ctx2 = $("#right_lower canvas")[0].getContext('2d');
	for(var i=0;i<data_tohead.length;i++) {
		var x1 = data_tohead[i][0];
		var y1 = data_tohead[i][1];
		var x2 = data_tohead[i][2];
		var y2 = data_tohead[i][3];
		
		ctx2.beginPath();
		ctx2.moveTo(x1,y1);
		ctx2.lineTo(x2,y2);
		ctx2.stroke();

		ctx2.beginPath();
	    ctx2.arc(x1, y1, 4, 0, 2 * Math.PI, false);
	    ctx2.fillStyle = 'green';
	    ctx2.fill();
	    ctx2.stroke();
	    tohead_pass_count++;
	}

	$("#right_upper_pass_count").html("Pass Count for Head Player :" +  head_pass_count);
	$("#right_lower_pass_count").html("Pass Count for ToHead Player : " + tohead_pass_count);
};

$(function() {
	$( "#slider_range" ).slider({
		range: true,
		min: 0,
		max: 90,
		values: [ 0,  90 ],
		slide: function( event, ui ) {
			var first_val = "";
			var second_val = "";
			
			var total_len = first_half_len + second_half_len;
			
			if(ui.values[0] <= 45) {
				first_val = ui.values[0].toString();
			}
			else if(ui.values[0]>45 && ui.values[0]<=first_half_len) {
				first_val = "45 + " + (ui.values[0]-45).toString();
			}
			else if(ui.values[0]>=first_half_len && ui.values[0]<=(90 + first_half_len-45)) {
				first_val = (ui.values[0] - (first_half_len-45)).toString(); 
			}
			else {
				first_val = "90 + " + (ui.values[0] - (first_half_len+45)).toString();
			}

			if(ui.values[1] <= 45) {
				second_val = ui.values[1].toString();
			}
			else if(ui.values[1]>45 && ui.values[1]<=first_half_len) {
				second_val = "45 + " + (ui.values[1]-45).toString();
			}
			else if(ui.values[1]>=first_half_len && ui.values[1]<=(90 + first_half_len-45)) {
				second_val = (ui.values[1] - (first_half_len-45)).toString(); 
			}
			else {
				second_val = "90 + " + (ui.values[1] - (first_half_len+45)).toString();
			}

			$( "#time_range" ).val(first_val.toString() + " mins - " + second_val.toString() + " mins");


		},
		change: function( event, ui ) {
			$( "#loader" ).show();
			Dajaxice.gui.dataEverything(Dajax.process, {'event':$('#id_event_type').val(),'fixture_name':$('#id_match_name').val(),
										'head_player_name':$('#id_head_player').val(),
										'tohead_player_name':$('#id_tohead_player').val(),
										'time1':$("#slider_range").slider("values", 0),
										'time2':$("#slider_range").slider("values", 1)
									}); 

		}

	});
		$( "#time_range" ).val($("#slider_range").slider("values", 0) + " mins - " + $("#slider_range").slider("values",1) + " mins");
	});
