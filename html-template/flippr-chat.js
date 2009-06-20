if (typeof(Flippr) == "undefined") {
  Flippr={};
}

Flippr.chat = {
    getMessageHandler : function(msg) {
        match = msg.match(/(.*):(.*)/);
        var nick = null;
        var message = null;
        if (match) {
            nick = match[1];
            message = match[2];
            var d = $('<tr class="tweet_area"><td>' + nick +'</td><td>'+ message +'</td></tr>');
            $('#receivedMessages').append(d);
        }
    },
    errorCannotConnectHandler : function(msg) {
        //    alert("Cannot connect to server " + msg);
        $('#error').html(msg);
    },
    errorDisconnectedHandler : function(msg) {
        //    alert("Disconnected from server" + msg);
        $('#error').html("Disconnected.");
    },
    errorIOErrorHandler : function(msg) {
        //    alert("IOError " + msg);
        $('#error').html("IOError.");
    },
    errorSecurityErrorHandler : function(msg) {
        //    alert("Security Error " + msg);
        $('#error').html("Security Error");
    }
};

function setFlipprSendMessage () {
    if (document['BrowserChat'] && document['BrowserChat'].flipprSendMessage) {
        Flippr.chat.sendMessage = function (msg) {
            document['BrowserChat'].flipprSendMessage(msg);
        }; 
    } else {
        alert("browserchat is not defined");
    }
}
    
$(function() {
    var sendfunc = function() {
        Flippr.chat.sendMessage($('#sendingMessage').val());
        $('#sendingMessage').val('');
    };
    $('#sendButton').click(sendfunc);
    $('#sendingMessage').keypress(
        function(e) {
            // Enter key
            if (e.which == 13) { sendfunc() }
        }
    );
});

