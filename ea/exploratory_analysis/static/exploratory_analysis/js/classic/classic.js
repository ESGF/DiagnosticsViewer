
EA_CLASSIC_VIEWER.functions = (function() {
	return {
		//todo
		echo: function(word) {
			return word + ' echo';
		},
		showButton: function (pckg) {
			if(pckg == 'lmwg') {
				//hide atm button
				$('#go_Atm_Home_Button').hide();
				
				//show land button
				$('#go_Land_Home_Button').show();
			} else {
				//show atm button
				$('#go_Atm_Home_Button').show();
				
				//hide all other buttons
				$('#go_Land_Home_Button').hide();
			}
		},
		transformClassicLinkNames: function (link_name) {
			
//			if (link_name.search('15') > -1) {
//				link_name = '15';
//			} else if (link_name.search('14') > -1) {
//				link_name = '14';
//			} else if (link_name.search('13') > -1) {
//				link_name = '13';
//			} else if (link_name.search('12') > -1) {
//				link_name = '12';
//			} else if (link_name.search('11') > -1) {
//				link_name = '11';
//			} else if (link_name.search('10') > -1) {
//				link_name = '10';
//			} else if (link_name.search('topten') > -1) {
//				link_name = 'topten';
//			} else if (link_name.search('9') > -1) {
//				link_name = '9';
//			} else if (link_name.search('8') > -1) {
//				link_name = '8';
//			} else if (link_name.search('7') > -1) {
//				link_name = '7';
//			} else if (link_name.search('6') > -1) {
//				link_name = '6';
//			} else if (link_name.search('5') > -1) {
//				link_name = '5';
//			} else if (link_name.search('4') > -1) {
//				link_name = '4';
//			} else if (link_name.search('3') > -1) {
//				link_name = '3';
//			} else if (link_name.search('2') > -1) {
//				link_name = '2';
//			} else if (link_name.search('1') > -1) {
//				link_name = '1';
//			} 
			
			return link_name;
			
		},
		expandPlot: function () {
			window.open(lastURL);
		},
		displayTableHover: function (textTableURL) {
			if($('#release').prop('disabled')) {

				$('#plotArea').empty();
				$('#provenaceArea').empty();
				$('.plot_btn').show();
				var textTableURL = "<img src=\"" + textTableURL + "\" \onerror=\"EA_CLASSIC_VIEWER.functions.imgError(this);\"/>";
				console.log('table path ' + textTableURL);
				
				console.log('html: ' + $('#plotArea').html());
				
				$('#plotArea').append('<div>' + textTableURL + '</div>');
				//$('#plotArea').append('<div>' + textTablePath + '</div>');
				$('#plotArea').show();
				//lastURL = tableURL;
				$('#provenanceArea').show();
			} 
		},
		
		displayImageClick: function (imageURL) {

			
			if($('#release').attr('disabled')) {
				$('#release').prop('disabled', false);
				
			} else {
				
				//make the button disabled
				$('#release').prop('disabled', true);
			}
			
			
		},
		
		displayImageHover: function (imageURL) {


			//$('#proveanceArea').empty()
			
			if($('#release').prop('disabled')) {
			
				$('#plotArea').empty();
				$('#provenanceArea').empty()
				$('.plot_btn').show();
				var imagePath = "<img id='displayed_image' src=\"" + imageURL + "\" \onerror=\"EA_CLASSIC_VIEWER.functions.imgError(this);\"/>";
				console.log('html: ' + $('#plotArea').html());
				
//				$('#plotArea').append('<div>' + imageURL + '</div>');
				$('#plotArea').append('<div>' + imagePath + '</div>');
				$('#plotArea').show();
				lastURL = imageURL;
			
				$('#provenanceArea').show();
				
			} else {
				
				
				
			}
			
		},
		
		
		load_sets_homepage: function (pckg,dataset,set) {

			//alert('set: ' + set + " dataset: " + dataset);
			var url = '/exploratory_analysis/classic_views_html?set=' + set + '&dataset_name=' + dataset + '&package=' + pckg;   //+ '?_=' + Math.round(Math.random() * 10000);
            console.log('url: ', url);
			
			$.ajax({
				type : "GET",
				url : url,
				cache : false,
				//data : JSON.stringify(data),
				//async : false,
				success : function(html) {
					
//					console.log('html: ' + html);

					$('#landHome').empty();
					$('#atmHome').empty();
					//alert('appending html here for pkg: ' + pckg);
					if (pckg == 'lmwg') {
						$('#landHome').append(html);
					} else {
						$('#atmHome').append(html);
					}
					
					/*
					$('.plot_links').on("click",function(){
						console.log('clicky');
					});
					*/
					
				},
				error : function(xhr, status, error) {

					console.log('error');
					if (xhr.status == 404) {
					}
				},
			});
		},
		
		
		
		load_diags_homepage: function () {
			
			var project = EA_MENU.functions.getMenuItem('#select_Project');
			var dataset = EA_MENU.functions.getMenuItem('#selectD');
			var pckg = EA_MENU.functions.getMenuItem('#selectP');
			var variables = EA_MENU.functions.getMenuItem('#selectV');
			var times = EA_MENU.functions.getMenuItem('#selectT');
			
			console.log('project: ' + project);
			console.log('dataset: ' + dataset);
			console.log('pckg: ' + pckg);
			console.log('variables: ' + variables);
			console.log('times: ' + times);
			/*
			var data = {
					"project" : project,
					"dataset" : dataset,
					"pckg" : pckg,
					"variables" : variables,
					"times" : times
				};
			*/
			
			EA_CLASSIC_VIEWER.functions.showButton(pckg);
			
			if (pckg == null) {
				pckg = 'atm';
			}
			
			
			var url = '/exploratory_analysis/classic_set_list_html?package=' + pckg; // + '?_=' + Math.round(Math.random() * 10000);

			//alert('before ajax: ' + pckg);
			
			$.ajax({
				type : "GET",
				url : url,
				cache : false,
				success : function(html) {
					
					//console.log('appending ' + html);
					
					
					$('#landHome').empty();
					$('#atmHome').empty();
					if (pckg == 'lmwg') {
						$('#landHome').append(html);
					} else {
						$('#atmHome').append(html);
					}
					
					
					//console.log('home: ' + $('#atmHome').html())
					
					$('.classic_toggle_sets').click(function() {

						
						
						console.log('id: ' + this.id);
						
						var set = EA_CLASSIC_VIEWER.functions.transformClassicLinkNames(this.id);

						
						EA_CLASSIC_VIEWER.functions.load_sets_homepage(pckg,dataset,set);
						
						
					});
					

				},
				error : function(xhr, status, error) {

					console.log('error');
					if (xhr.status == 404) {
					}
				},
			});
			
		},
		
		nodisplayImage: function () {
			if($('#release').prop('disabled')) {
				$('#plotArea').empty();
				$('#provenaceArea').empty();
			} else {
				//alert('display image');
			}
			
		},
		
		releasePlot: function() {
			$('#plotArea').empty();
			$('#provenanceArea').empty();
			$('#release').prop('disabled','true');
		},
		
		
		displayTable: function (imageURL) {

			
			if($('#release').attr('disabled')) {
				$('#release').prop('disabled', false);
				
			} else {
				$('#release').prop('disabled', true);
			}
		},
		
		imgError: function (image) {
			image.onerror = "";
			image.src = EA.noImageSource;
			return true;
		},
		
		getDatasetName: function () {
			
			var tempLastURL = lastURL;
			
			var index = tempLastURL.search("/");
			while(index >= 0) {
				tempLastURL = tempLastURL.substring(index+1);
				index = tempLastURL.search("/");
				//alert('tempLawstURL - ' + tempLastURL);
			}
			
			
			return tempLastURL;
			
		},
		
		getProvenance: function () {
			

			//$('#provenanceArea').append(lastURL);

			$('#provenanceArea').empty();
			
			var filtered_figure_name = EA_CLASSIC_VIEWER.functions.getDatasetName();
			var dataset_name = EA_MENU.functions.getMenuItem('#selectD');
			var package_name = EA_MENU.functions.getMenuItem('#selectP');
				
			var url = '/exploratory_analysis/provenance/?filename=' + filtered_figure_name + '&dataset_name=' + dataset_name + '&package=' + package_name; // + '?_=' + Math.round(Math.random() * 10000);

			
			$.ajax({
				type : "GET",
				url : url,
				cache : false,
				success : function(html) {
					
					console.log('appending ' + html);
					//$('#provenanceArea').empty();
					$('#provenanceArea').append(html);
					/*
					$('#landHome').empty();
					$('#atmHome').empty();
					if (pckg == 'lnd') {
						$('#landHome').append(html);
					} else {
						$('#atmHome').append(html);
					}
					*/
					
				},
				error: function() {
					console.log('error');
				}
			});
			
			
			return 'text';
		} 
		
	
	
	};
})();

for (var key in EA_CLASSIC_VIEWER.functions) {
	//console.log('functions key: ' + key);
}


$(document).ready(function() {
	
	//alert('document ready in classic.js');
	
	
	
	$('#go_Land_Home_Button').click(function(){
		EA_CLASSIC_VIEWER.functions.load_diags_homepage();
	});
	
	$('#go_Atm_Home_Button').click(function(){
		EA_CLASSIC_VIEWER.functions.load_diags_homepage();
	});
	
	/**/
	$('#selectP').change(function() {
		
		//EA_MENU.functions.changeMenuSelections();
		
		EA_CLASSIC_VIEWER.functions.load_diags_homepage();
		
	}); 
	
	$('#selectD').change(function() {
		
		//EA_MENU.functions.changeMenuSelections();
		
		EA_CLASSIC_VIEWER.functions.load_diags_homepage();
		
	}); 
	
	
	
	
	
	
});











//BELOW to be removed 8-2-15
/*

var clicked = 0;
var lastURL = "";

function showButton(pckg) {
	if(pckg == 'lnd') {
		//hide atm button
		$('#go_Atm_Home_Button').hide();
		
		//show land button
		$('#go_Land_Home_Button').show();
	} else {
		//show atm button
		$('#go_Atm_Home_Button').show();
		
		//hide all other buttons
		$('#go_Land_Home_Button').hide();
	}
	
}
*/

/*
function load_diags_homepage() {
	
	//alert('run diags');
	
	var project = getMenuItem('#select_Project');
	var dataset = getMenuItem('#selectD');
	var pckg = getMenuItem('#selectP');
	var variables = getMenuItem('#selectV');
	var times = getMenuItem('#selectT');
	
	console.log('project: ' + project);
	console.log('dataset: ' + dataset);
	console.log('pckg: ' + pckg);
	console.log('variables: ' + variables);
	console.log('times: ' + times);
	
	//var data = {
	//		"project" : project,
	//		"dataset" : dataset,
	//		"pckg" : pckg,
	//		"variables" : variables,
	//		"times" : times
	//	};
	
	
	EA_CLASSIC_VIEWER.functions.showButton(pckg);
	
	if (pckg == null) {
		pckg = 'atm';
	}
	
	
	var url = '/exploratory_analysis/classic_set_list_html?package=' + pckg; // + '?_=' + Math.round(Math.random() * 10000);

	
	$.ajax({
		type : "GET",
		url : url,
		cache : false,
		success : function(html) {
			
			//console.log('appending ' + html);
			
			$('#landHome').empty();
			$('#atmHome').empty();
			if (pckg == 'lnd') {
				$('#landHome').append(html);
			} else {
				$('#atmHome').append(html);
			}
			
			
			//console.log('home: ' + $('#atmHome').html())
			
			$('.classic_toggle_sets').click(function() {

				
				
				console.log('id: ' + this.id);
				
				var set = EA_CLASSIC_VIEWER.functions.transformClassicLinkNames(this.id);

				
				load_sets_homepage(pckg,set);
				
				
				
				
				//var index = this.id.search('_');

				//var set = this.id.substring(index + 1);
				

				//alert('classic toggle sets ' + set);
				
				//load_sets_homepage(pckg,set);
				
				
				
			});
			

		},
		error : function(xhr, status, error) {

			console.log('error');
			if (xhr.status == 404) {
			}
		},
	});
	
}
*/


//amwgmaster map is looking for:
//topten,so,1,2,3,4,4a,5,6,7,8,9,10,11,12,13,14,15
/*
function transformClassicLinkNames(link_name) {
	
	if (link_name.search('15') > -1) {
		link_name = '15';
	} else if (link_name.search('14') > -1) {
		link_name = '14';
	} else if (link_name.search('13') > -1) {
		link_name = '13';
	} else if (link_name.search('12') > -1) {
		link_name = '12';
	} else if (link_name.search('11') > -1) {
		link_name = '11';
	} else if (link_name.search('10') > -1) {
		link_name = '10';
	} else if (link_name.search('topten') > -1) {
		link_name = 'topten';
	} else if (link_name.search('9') > -1) {
		link_name = '9';
	} else if (link_name.search('8') > -1) {
		link_name = '8';
	} else if (link_name.search('7') > -1) {
		link_name = '7';
	} else if (link_name.search('6') > -1) {
		link_name = '6';
	} else if (link_name.search('5') > -1) {
		link_name = '5';
	} else if (link_name.search('4') > -1) {
		link_name = '4';
	} else if (link_name.search('3') > -1) {
		link_name = '3';
	} else if (link_name.search('2') > -1) {
		link_name = '2';
	} else if (link_name.search('1') > -1) {
		link_name = '1';
	} 
	
	return link_name;
	
}
*/

/*
function load_sets_homepage(pckg,set) {
	var url = '/exploratory_analysis/classic_views_html?set=' + set; //+ '?_=' + Math.round(Math.random() * 10000);
	
	$.ajax({
		type : "GET",
		url : url,
		cache : false,
		//data : JSON.stringify(data),
		//async : false,
		success : function(html) {
			
			console.log('html: ' + html);

			$('#landHome').empty();
			$('#atmHome').empty();
			if (pckg == 'lnd') {
				$('#landHome').append(html);
			} else {
				$('#atmHome').append(html);
			}
			
			
			//$('.plot_links').on("click",function(){
			//	console.log('clicky');
			//});
			
			
		},
		error : function(xhr, status, error) {

			console.log('error');
			if (xhr.status == 404) {
			}
		},
	});
}
*/



/*
function displayImageClick(imageURL) {

	
	if($('#release').attr('disabled')) {
		//alert('disabled');
		$('#release').prop('disabled', false);
		
	} else {
		//alert('not disabled: ' + $('#release').attr('disabled'));
		$('#release').prop('disabled', true);
	}
	
	
}
*/

/*
function imgError(image) {
	image.onerror = "";
	image.src = EA.noImageSource;
	return true;
}
*/

/*
function displayImageHover(imageURL) {

	if($('#release').prop('disabled')) {
	
		$('#plotArea').empty();
		$('.plot_btn').show();
		var imagePath = "<img src=\"" + imageURL + "\" \onerror=\"imgError(this);\"/>";
		console.log('html: ' + $('#plotArea').html());
		
		$('#plotArea').append('<div>' + imageURL + '</div>');
		$('#plotArea').append('<div>' + imagePath + '</div>');
		$('#plotArea').show();
		lastURL = imageURL;
	
	} else {
		
		
		
	}
	
}
*/

/*

function nodisplayImage() {
	//alert($('#release').prop('disabled'))
	if($('#release').prop('disabled')) {
		$('#plotArea').empty();
	} else {
		//alert('display image');
	}
	
}
*/

/*
function releasePlot() {
	$('#plotArea').empty();
	$('#release').prop('disabled','true');
}
*/

/*
function displayTable(imageURL) {

	
	if($('#release').attr('disabled')) {
		$('#release').prop('disabled', false);
		
	} else {
		$('#release').prop('disabled', true);
	}
}
*/

/*
function displayTableHover(textTableURL) {
	if($('#release').prop('disabled')) {
		
		$('#plotArea').empty();
		$('.plot_btn').show();
		var textTableURL = "<img src=\"" + textTableURL + "\" \onerror=\"imgError(this);\"/>";
		console.log('table path ' + textTableURL);
		
		console.log('html: ' + $('#plotArea').html());
		
		$('#plotArea').append('<div>' + textTableURL + '</div>');
		//$('#plotArea').append('<div>' + textTablePath + '</div>');
		$('#plotArea').show();
		lastURL = tableURL;
	
	} 
	

}
*/

/* Table code here
if (clicked != 1) {
	textTableURL = textTableURL;
	if (textTableURL.endsWith('.json')) {
		var tableHTML = '<table id="r22" width="100%" height="600" cellspacing="0"><thead><tr><th>Name</th><th>Position</th><th>Office</th><th>Extn.</th><th>Start date</th><th>Salary</th> </tr></thead><tfoot><tr><th>Name</th><th>Position</th><th>Office</th><th>Extn.</th><th>Start date</th><th>Salary</th></tr></tfoot></table>';
		document.getElementById("plotArea").style.visibility = 'visible';
		document.getElementById("plotArea").innerHTML = '' + tableHTML;

		//$(document).ready(function(){
		$('#r22').DataTable({
			"ajax" : {
				"url" : textTableURL,
				"dataSrc" : ""
			},
			"columns" : [{
				"data" : "name"
			}, {
				"data" : "position"
			}, {
				"data" : "office"
			}, {
				"data" : "extn"
			}, {
				"data" : "start_date"
			}, {
				"data" : "salary"
			}]
			//} );
		});
	} else {
		document.getElementById("plotArea").style.visibility = 'visible';
		document.getElementById("plotArea").innerHTML = '<iframe src="' + textTableURL + '" width=100% height=800 frameborder=0 ></iframe>';
	}

}
*/


/*
function expandPlot() {
	window.open(lastURL);
}
*/




//Taken out 7-29-15
//<button id="release" class="btn btn-default plot_btn" type="button" onclick="releasePlot()" style="display:none">Release
//<!-- <span class="glyphicon glyphicon-new-window"></span> -->
//</button>

//$('.plot_btn').show();
/*
alert('imgURL : ' + 
		imageURL );

$('.plot_btn').show();
var imagePath = "<img src=\"" + imageURL + "\" \onerror=\"imgError(this);\"/>";
document.getElementById("plotArea").style.visibility = 'visible';
//document.getElementById("plotArea").innerHTML = imagePath;
//document.getElementById("plotArea").innerHTML = '<div>' + imageURL + '</div>';

console.log('html: ' + $('#plotArea').html());

$('#plotArea').append('<div>' + imagePath + '</div>');
$('#plotArea').show();
lastURL = imageURL;
clicked = 1;
*/
