var data_file = document.currentScript.getAttribute('data_file');


$(document).ready(function(){
    $.getJSON(data_file, function(json) {

        var players = Object.values(json)

        players.sort((a,b) => (a.grade < b.grade) ? 1 : ((b.grade < a.grade) ? -1 : 0))

        console.log(players)

        $.each(players, function(title, values){
            if (title == 0) {
                $("#goat_grade").append(`<div><b><p>Season ${values.year - 1}-${values.year}: ${values.league_grade}</p></b></div>`)
            }


            var player_div = 
            `
            <div>
                <p><b>${title + 1}</b>: ${values.name} | ${values.grade}</p>
            </div>
            `
            // <p class="artist" style="font-size: 10px">${values.asboyer_score}</p>

        $('#goat_grade').append(player_div)
        });
    });

});
