$(document).ready(function() {
	var update_list = function(query) {
		$.getJSON('search_task/', {search: query}, function(data) {
			$("#tasks").text("");
			var task_list = []
			var cnt = data.tasks.length;
			task_list.push("<table>\n");
			for (var i = 0; i < 10; ++i) {
				task_list.push("<tr>\n");
				for (var j = 0; j * 10 + i < cnt; ++j) {
					var name = data.tasks[j*10+i].name
					var s = "<td><a href=task/" + name + ">" + name + "</a></td>\n";
					task_list.push(s);
				}
				task_list.push("</tr>\n");
			}
			task_list.push("</table>\n");
			$("#tasks").append( task_list.join(''));
			
		});
	}
	update_list('');
	var search_task = function() {
		var query;
		query = $(this).val();
		update_list(query);
	}
	$('#search').keyup(search_task)

});


