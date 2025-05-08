var error_content = context.getVariable("error.content");
var proxy_name = context.getVariable("apiproxy.name");
var messageid = context.getVariable("messageid");
var response_content = context.getVariable("response.content");
var response_code = context.getVariable("error.status.code");
var request_method = context.getVariable("request.verb");
var state = context.getVariable("error.state");
var proxy_url = context.getVariable("request.uri");
var target_url = context.getVariable("request.url");
//
// Build the payload with the stringified input
var payload = {
    
   "message": proxy_name,
    "level": "Error",
    "error_content" : error_content,
    "messageid" : messageid,
    "response_content" : response_content,
    "response_code" : response_code,
    "method": request_method,
    "state":state,
    "proxy_url": proxy_url,
    "target_url" : target_url
    
};

// Set the stringified payload for New Relic
context.setVariable("newRelicPayload", JSON.stringify(payload));