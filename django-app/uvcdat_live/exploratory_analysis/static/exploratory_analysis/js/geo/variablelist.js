var queryString = '';

//assemble the query string
var hostname = location.hostname;
var port = location.port;
var url = 'http://' + hostname + ':' + port + '/exploratory_analysis/variables/' + this.innerHTML;

var dataList = ["tropics_warming_th_q_co2"]
var packList = ["lmwg"]
var varList = ["TLAI","GPP","NEE","HR","ER","NPP","QVEGT","QVEGE","QSOIL","GROSSNMIN"]
var timeList = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","DJF","MAM","JJA","SON","ANN"]

$(document).ready(function() {
	/*
	 *  This is how you would populate multiselect dynamically, but currently useless?
	 */
	/*
	$.ajax({
		url : url,
		global : false,
		type : 'GET',
		dataType : 'json',
		data : queryString,
		success : function(data) {
			$(function() {
				$("#selectV").multiselect().multiselectfilter();
			});

			$("#selectV").multiselect({
				multiple : false,
				header : "Select an option",
				height : "400",
				noneSelectedText : "Select an Option",
				selectedList : 1
			});

			var variableList = data['variables'];
			d3.select("#selectV").selectAll("option").data(variableList).enter().append("option").attr("value", String).text(String);
			$("#selectD").multiselect("refresh");

		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert('variables textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);

		}
	});
	*/

	
	
	
	
	
	
	
	//init Dataset multiselect
	$(function() {
		$("#selectD").multiselect().multiselectfilter();
	});

	$("#selectD").multiselect({
		multiple : false,
		header : "Select an option",
		noneSelectedText : "tropics_warming_th_q_co2",
		selectedList : 1
	});

	d3.select("#selectD").selectAll("option").data(dataList).enter().append("option").attr("value", String).text(String);

	//init Variable multiselect
	$(function() {
		$("#selectV").multiselect().multiselectfilter();
	});

	$("#selectV").multiselect({
		multiple : false,
		header : "Select an option",
		noneSelectedText : "Select an Option",
		selectedList : 1
	});

	d3.select("#selectV").selectAll("option").data(varList).enter().append("option").attr("value", String).text(String);
	
	//init Time multiselect
	$(function() {
		$("#selectT").multiselect().multiselectfilter();
	});

	$("#selectT").multiselect({
		multiple : false,
		header : "Select an option",
		noneSelectedText : "Select an Option",
		selectedList : 1
	});

	d3.select("#selectT").selectAll("option").data(timeList).enter().append("option").attr("value", String).text(String);
	
    //init Package multiselect
	$(function() {
		$("#selectP").multiselect().multiselectfilter();
	});

	$("#selectP").multiselect({
		multiple : false,
		header : "Select an option",
		noneSelectedText : "Select an Option",
		selectedList : 1
	});

	d3.select("#selectP").selectAll("option").data(packList).enter().append("option").attr("value", String).text(String);
	
	$("#selectD").multiselect("refresh");
	$("#selectV").multiselect("refresh");
	$("#selectP").multiselect("refresh");
	$("#selectT").multiselect("refresh");
	
	
});

/*
$('.dropdown-dataset-menu').on('click','a',function() {

var queryString = '';

//assemble the query string
var hostname = location.hostname;
var port = location.port;
var url = 'http://' + hostname + ':' + port + '/exploratory_analysis/variables/' + this.innerHTML;

console.log('querying: ' + url);

$.ajax({
url: url,
global: false,
type: 'GET',
dataType: 'json',
data: queryString,
success: function(data) {

var variableList = data['variables'];
$('.dropdown-variable-menu').empty();

//console.log(variableList);
for (var i=0;i<variableList.length;i++) {
var variable = variableList[i];
console.log('variable: ' + variable);
$('.dropdown-variable-menu').append('<li class="variable_menu" id="' + variable + '"><a href="#">' + variable + '</a></li>');
}

$('#dropdown-variable-container').show();

},
error: function( jqXHR, textStatus, errorThrown ) {
alert('variables textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);

}
});

$('#dataset_name').empty();
$('#dataset_name').append(this.innerHTML);

});
*/

//});