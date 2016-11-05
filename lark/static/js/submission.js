$(document).ready(function() {
	var id = $("span[data-name='id']:visible").text();
	console.log(id);
	var refresh = 0;
	var update_list = function() {
		$.getJSON('/list_test_result', {sub_id: id}, function(data) {
			refresh = 0;
			$("#tests").text("");
			$("#main").text("");
			var sub = data.sub;
			var s = "<p>" + sub.id + "|" + sub.date + "|" + sub.verdict + "|";
			s += sub.time + "|" + sub.memory + "</p>\n";
			if (sub.verdict == "In queue" || sub.verdict == "Running") refresh = 1;
			$("#main").append(s);
			var out = [];
			out.push("<table>\n");
			var cnt = data.results.length;
			for (var i = 0; i < cnt; ++i) {
				var test = data.results[i];
				var s = "<p>" + test.index + "|" + test.time + "|";
				s += test.memory + "|" + test.verdict + "</p>\n";
				if (test.verdict == "In queue" || test.verdict == "Running") refresh = 1;
				out.push("<tr><td>" + s + "</td></tr>\n");
			}
			if (cnt == 0) refresh = 1;
			if (sub.verdict == 'Compilation error') refresh = 0;
			if (refresh == 0) clearInterval(intervalid);
			$("#tests").append( out.join(''));
		});
	}
	update_list();
	var intervalid = setInterval(update_list, 100);
});
