$(document).ready(function(){
  $("#jquery_jplayer_1").jPlayer({
    /*ready: function () {
      $(this).jPlayer("setMedia", {
        m4a: "http://www.jplayer.org/audio/m4a/Miaow-07-Bubble.m4a",
        oga: "http://www.jplayer.org/audio/ogg/Miaow-07-Bubble.ogg"
      });
    },*/
    swfPath: "/static/scripts/libs/Jplayer.swf",
    supplied: "mp3",
    solution:"html,flash",
    size: "cssClass"
  });
  
  $('.play-song').live('click', function(event) {
  	
 		if ($(this).parent().parent().hasClass('jplayer_playlist_current')) {
 			$("#jquery_jplayer_1").jPlayer("stop");
 			$('.jplayer_playlist_current div .play-song img').attr("src","/static/images/play_big.png");
 			$('.jplayer_playlist_current').removeClass('jplayer_playlist_current');
 		}else{
 			$('.jplayer_playlist_current div .play-song img').attr("src","/static/images/play_big.png");
		      $(this).children().attr("src","/static/images/playback_stop.png");
		      var index = $(this).parent().parent().index();
		      playSong(index+1);
 		}
  	  
  });
  $('.love-song').click(function() {
  		$('.jplayer_playlist_current div .play-song').trigger('click');
      	var sume = 1;
      	var vote = parseInt($(this).siblings('.song-artist-info').children().children().html());
      	if ($(this).hasClass('liked')) {
      		$(this).toggleClass('liked',false);
      		sume = -1;
      		$(this).siblings('.song-artist-info').children().children().html(vote-1);
      	}else{
      		//$(this).siblings('.song-artist-info').children().children().html('');
      		$(this).siblings('.song-artist-info').children().children().html(vote+1);
      		$(this).toggleClass('liked',true);
      	}
      
      var $clicked = $(this).parent().parent();
      
      //if(previousAll.length > 0) {
		//send to server
		var id = $(this).attr('rel');
		var eventId = $clicked.parent().attr('rel');
		
		$.ajax({
		   type: "POST",
		   url: "/setlist/update",
		   dataType: "json",
		   data: {idevent: eventId , idsong: id, sum: sume},
		   success: function(data)
		   {
		   		if (data) {
		   			moveSong($clicked,data['position'],sume);		   			
		   		}
		   }
	 	});
    });
    
});

$("#jplayer_playlist ul").sortable();
var $list = $('.song-list ul');

function playSong(i){
	var $next_song 		= $list.find('li:nth-child('+ i +')');
	var mp3u				= $next_song.find('.song-url').html();
	//var ogg				= $next_song.find('.mp_ogg').html();
	$list.find('.jplayer_playlist_current').removeClass("jplayer_playlist_current");
	$next_song.addClass("jplayer_playlist_current");
	$("#jquery_jplayer_1").jPlayer("setMedia", 
	{
		mp3: mp3u
	}).jPlayer("play");
}

function moveSong(clicked,index,sume){
	
	if (sume < 1) {
		var nextAll = clicked.nextUntil($('.song-container:nth-child('+(index+2)+')'));
		
		var bottom = $(nextAll[nextAll.length-1]);
		
	    var next = $(nextAll[0]);

	    // how far up do we need to move the clicked LI?
	    var botof = clicked.offset().top;
	    
	    var moveDown = bottom.offset().top - clicked.offset().top;
	
	    // how far down do we need to move the previous siblings?
	    var moveUp =  (next.offset().top + next.outerHeight()) - (clicked.offset().top + clicked.outerHeight()) ;
	    
	    clicked.css('position', 'relative');
	    nextAll.css('position', 'relative');
	    clicked.animate({'top': moveDown});
	    nextAll.animate({'top': -moveUp}, {complete: function() {
	      // rearrange the DOM and restore positioning when we're done moving
	      //clicked.parent().prepend(clicked);
	      $(clicked).insertAfter(bottom);
	      	clicked.css({'position': 'static', 'top': 0});
	      	nextAll.css({'position': 'static', 'top': 0}); 
    	  }});
    	  
	}else{
		//previousAll for visual
		//var previousAllV = clicked.prevUntil('li:nth-child('+(index)+')');
		
		// all the LIs above the clicked to index position
		var previousAll = clicked.prevUntil('.song-container:nth-child('+index+')');
		
		// top LI for VISUAL
		var top = $(previousAll[previousAll.length-1]);//$($list+' li:nth-child('+index+')'); //$(previousAll[previousAll.length - 1]);
		
		//top LI for DOM
		//var topD = $(previousAll[previousAll.length - (index)]);
		
		// immediately previous LI
		var previous = $(previousAll[0]);
		
		// how far up do we need to move the clicked LI?
		var topof = clicked.offset().top;
		
		var moveUp = clicked.offset().top/*clicked.attr('offset')/*attr('offset')*/ - top.offset().top/*attr('offset')*/;
		
		// how far down do we need to move the previous siblings?
		var moveDown = (clicked.offset().top + clicked.outerHeight()) - (previous.offset().top + previous.outerHeight());
		
		// let's move stuff
		clicked.css('position', 'relative');
		previousAll.css('position', 'relative');
		clicked.animate({'top': -moveUp});
		previousAll.animate({'top': moveDown}, {complete: function() {
		  // rearrange the DOM and restore positioning when we're done moving
		  //clicked.parent().prepend(clicked);
		  $(clicked).insertBefore(top);
		  clicked.css({'position': 'static', 'top': 0});
		  previousAll.css({'position': 'static', 'top': 0}); 
		}});
    }
}

$('.date-event').html(formatDate($('.date-event').html()));

function formatDate(dateIn){
	var peluOut = new AnyTime.Converter({
		format:"%Y-%m-%d %H:%i:%s"
	});
	
	var date = peluOut.parse(dateIn);
	
	var defaultConv = new AnyTime.Converter({
		format: "%M %d, %Z at %h:%i%p"
	});
	
	return defaultConv.format(date);
}
