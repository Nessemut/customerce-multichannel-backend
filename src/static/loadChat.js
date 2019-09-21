function loadScript(url, callback) {
  var script = document.createElement("script")
  script.type = "text/javascript";
  if(script.readyState) {
    script.onreadystatechange = function() {
      if ( script.readyState === "loaded" || script.readyState === "complete" ) {
        script.onreadystatechange = null;
        callback();
      }
    };
  } else {
    script.onload = function() {
      callback();
    };
  }

  script.src = url;
  document.getElementsByTagName("head")[0].appendChild(script);
}


var scriptPath = "https://customerce.es/customerce-chat/chat.js";

loadScript("https://unpkg.com/react@16/umd/react.development.js", function() {
  loadScript("https://unpkg.com/react-dom@16/umd/react-dom.development.js", function() {
	var div = document.createElement('div');
	div.id = "chat_container";
	document.getElementsByTagName("body")[0].append(div);
    loadScript(scriptPath, function() {});
});
});