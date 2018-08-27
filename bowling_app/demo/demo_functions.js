function generateFrameCell(last_frame=false) {
	var colspan = last_frame ? '3' : '2';
	
	var table = $('<table>').addClass('frame_table');
	var tries_row = $('<tr>').append($('<td style="border-top: none"/>'.repeat(colspan)));
	var score_row = $('<tr>').append($('<td>').attr('colspan',colspan));
	table.append(tries_row).append(score_row);
	
	table.find('td').first().addClass('first_try').css('width', Math.floor((100)/colspan)+'%');
	$(table.find('td')[colspan-1]).addClass('last_try').css('width', Math.floor((100)/colspan)+'%');
	table.find('td').last().addClass('frame_score');
	
	return table;
}

function generateAllFramesRow(frame_count=10) {
	var tr = $('<tr>');
	tr.append($('<td>').addClass('player_num')); // player number
	for (var i = 0; i < frame_count; i++) {
		tr.append($('<td>').addClass('frame_cell').append(generateFrameCell(i == frame_count - 1)));
	}
	tr.append($('<td>').addClass('total_score')); // total score
	return tr;
}

function generateGameTable(num_players=1, frame_count=10) {
	var table = $('<table>').addClass('game_table');
	var thead = $('<thead>').addClass('game_table_header');
	var tr = $('<tr>');
	for (var i = 0; i < frame_count + 2; i++) {
		var text = i;
		if (i == 0) text = 'Player';
		if (i == frame_count + 1) text = 'Total';
		tr.append($('<th>').text(text));
	}
	thead.append(tr);
	
	var tbody = $('<tbody>');
	for (var i = 0; i < num_players; i++) {
		tbody.append(generateAllFramesRow(frame_count));
	}
	
	table.append(thead);
	table.append(tbody);
	
	return table;
}

var updateVar = null;

function createNewGame() {
	$.post('/games').done(function(data){
		if (updateVar) window.clearInterval(updateVar);
		$('.game_table').remove();
		var game_id_el = $('<input type="hidden" id="game_id" />').val(data.game_id);
		var t = generateGameTable();
		t.appendTo($('body'));
		game_id_el.appendTo($('body'));
		$('#start_game').show().click(() => startGame(data.game_id));
		$('#throw_ball').click(function() {
			var num_pins = $('#num_pins_input').val();
			throwBall(data.game_id, num_pins);
		});
	});
}

function startGame(game_id) {
	$.ajax({
		method: 'PUT',
		url: '/games/'+game_id,
		data: {action: 'start'}
	}).done(function() {
		updateVar = window.setInterval(() => getGameScore(game_id), 2000);
	});
}

function throwBall(game_id, num_pins) {
	$.ajax({
		method: 'PUT',
		url: '/games/'+game_id,
		data: {action: 'throw', num_pins: num_pins}
	}).done(function(data) {
		//window.setInterval(() => getGameScore(game_id), 2000);
		if (data.finished == true) {
			if (updateVar) window.clearInterval(updateVar);
			getGameScore(game_id);
		}
	}).fail(function(data) {
		alert(data.responseJSON.message);
	});
}

function getGameScore(game_id) {
	$.get('/games/' + game_id).done(function(data) {
		updateGameScore(data);
		if (data.game.finished == true) {
			if (updateVar) window.clearInterval(updateVar);
		}
	})
	.fail(function(data) {
		console.log(data.message);
	});
}

function updateGameScore(data) {
	//data.game.scores;
	$.each($('.game_table').first().children('tbody').children('tr'),
		function (player_index, x) {
			//data.game.scores[index].score;
			//data.game.scores[index].frames[];
			var scores = data.game.scores[player_index];
			$.each($(x).find('.frame_score'), function(frame_index, y) {
				if (frame_index <= scores.current_frame_num) $(y).text(scores.frames[frame_index].score);
			});
//			.text(data.game.scores[player_index].score);
			$(x).find('.total_score').text(data.game.scores[player_index].score);
		}
	);
}

