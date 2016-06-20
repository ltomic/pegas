$(document).ready(function() {
	var user = $("h2[data-name='user']:visible").text();
	var task = $("h1[data-name='task']:visible").text();
	var refresh = 0;
	console.log(task);
	console.log(user);
	var update_list = function() {
		$.getJSON('/paas/list_submissions', {user: user, task: task}, function(data) {
			refresh = 0;
			console.log(1);
			$("#subs").text("");
			var out = []
			out.push("<table>\n");
			var cnt = data.subs.length;
			for (var i = 0; i < cnt; ++i) {
				var sub = data.subs[i];
				var id = "<a href=/paas/task/" + task + "/" + sub.id + ">";
				id += sub.id + "</a>";
				var s = id + "|" + sub.date + "|" +	sub.verdict + "|";
				s += sub.time + "|" + sub.memory;
				if (sub.verdict == "In queue" || sub.verdict == "Running") refresh = 1;
				out.push("<tr><td>" + s + "</td></tr>\n");
			}
			if (refresh == 0) clearInterval(intervalid);
			$("#subs").append( out.join(''));
		});
	}
	update_list();
	var intervalid = setInterval(update_list, 1000);
});
