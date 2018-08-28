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

function generateAllFramesRow(player_number=0, frame_count=10) {
	var tr = $('<tr>').addClass('frames_row_ordinary');
	tr.append($('<td>').addClass('player_num').text(player_number));
	for (var i = 0; i < frame_count; i++) {
		tr.append($('<td>').addClass('frame_cell').append(generateFrameCell(i == frame_count - 1)));
	}
	tr.append($('<td>').addClass('total_score'));
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
		tbody.append(generateAllFramesRow(0, frame_count));
	}
	
	table.append(thead);
	table.append(tbody);
	
	return table;
}

var updateVar = null;

function createNewGame() {
	$.post('/games').done(function(data){
		if (updateVar) window.clearInterval(updateVar);
		
		$('#start_game').unbind('click');
		//$('.throw_ball').unbind('click');
		$('#add_player').unbind('click');
		
		$('#throw_ball_input').children().remove();
		
		for (var i = 0; i <= 10; i++) {
			var pin = $('<input type="button" class="throw_ball" value="'+i+'"/>');
			pin.click(function() {
				throwBall(data.game_id, $(this).val());
			});
			pin.appendTo($('#throw_ball_input'));
		}
		
		$('.game_table').remove();
		var t = generateGameTable();
		t.appendTo($('body'));
		$('#start_game').show().click(() => startGame(data.game_id));
		$('#add_player').show().click(() => addPlayer(data.game_id));
		$('#throw_ball').click(function() {
			var num_pins = $('#num_pins_input').val();
			throwBall(data.game_id, num_pins);
		});
		
		alert('Game id is ' + data.game_id);
	});
}

function startGame(game_id) {
	$.ajax({
		method: 'PUT',
		url: '/games/'+game_id,
		data: {action: 'start'}
	}).done(function(data) {
		updateVar = window.setInterval(() => getGameScore(game_id), 2000);
		$('#start_game').hide();
		$('#add_player').hide();
		$('#throw_ball_input').show();
		alert('The game ' + data.game_id + ' is started!');
	});
}

function addPlayer(game_id) {
	$.ajax({
		method: 'PUT',
		url: '/games/'+game_id,
		data: {action: 'add_player'}
	}).done(function(data) {
		$('.game_table').first().children('tbody').append(generateAllFramesRow(data.num_players - 1));
	}).fail(function(data) {
		alert(data.responseJSON.message);
	});
}

function throwBall(game_id, num_pins) {
	$.ajax({
		method: 'PUT',
		url: '/games/'+game_id,
		data: {action: 'throw', num_pins: num_pins}
	}).done(function(data) {
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
			
			var arr = data.game.scores.map(x => x.score);
			console.log(arr);
			var max_score = Math.max(...arr);
			var winner = arr.indexOf(max_score);
			
			alert('The game ' + game_id + ' is finished. Player ' + winner + ' wins with ' + max_score + ' points');
		}
	})
	.fail(function(data) {
		console.log(data.message);
	});
}

function updateGameScore(data) {
	$.each($('.game_table').first().children('tbody').children('tr'),
		function (player_index, x) {

			var scores = data.game.scores[player_index];
			
			if (data.game.current_player == player_index) $(x).addClass('frame_row_current');
			else $(x).removeClass('frame_row_current');
			
			$.each($(x).find('.frame_score'), function(frame_index, y) {
				if (frame_index <= scores.current_frame_num) {
					$(y).text(scores.frames[frame_index].score);
				}
			});
			
			$.each($(x).find('.frame_table'), function(frame_index, y) {
				if (frame_index <= scores.current_frame_num) {
					
					var frame_data = scores.frames[frame_index];
					var throw_scores = frame_data.throw_scores;
					var captions = ['-','-','-'];
					
					if (frame_data.last_frame == false) {
						if (frame_data.strike == true) {
							captions[0] = 'X';
						}
						else if (frame_data.spare == true) {
							captions = [throw_scores[0],'/','-'];
						}
						else {
							captions = [throw_scores[0],throw_scores[1],'-'];
						}
					}
					else {
						if (frame_data.spare == true) {
							captions = [throw_scores[0],'/', frame_data.throws_done == 3 ? throw_scores[2] : ''];
						}
						else if (frame_data.strike == true) {
							captions = ['X',throw_scores[1] == 10 ? 'X' : throw_scores[1],throw_scores[2] == 10 ? 'X' : throw_scores[2]];
						}
						else {
							captions = [throw_scores[0],throw_scores[1], '-'];
						}
						
						
					}
					
					var cond = (frame_data.last_frame == false) && (frame_data.strike == true);
					cond = cond || (frame_data.last_frame == true) && (scores.finished == true);
					
					for (var i = 0; i < (cond ? throw_scores.length : frame_data.throws_done); i++) {
						$($(y).find('td')[i]).text(captions[i]);
					}
					
				}
			});

			$(x).find('.total_score').text(data.game.scores[player_index].score);
			
		}
	);
}

