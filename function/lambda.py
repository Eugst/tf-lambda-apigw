import re, json

REPLACE_MAP = {
    "ABN":       "ABN AMRO",
    "ING":       "ING Bank",
    "Rabo":      "Rabobank",
    "Triodos":   "Triodos Bank",
    "Volksbank": "de Volksbank",
}

def replaceWord(src, lookFor, replaceWith):
    extra = replaceWith.replace(lookFor, "")
    return re.sub(rf"(?<!{extra})\b{lookFor}\b(?!{extra})", replaceWith, src)

def main(txt):
    for lookFor, replaceWith in REPLACE_MAP.items():
        txt = replaceWord(txt, lookFor, replaceWith)
    return txt

def body_checks(request):
    if "string" not in request:
        raise ValueError("the request doesn't contain the right key")
    if type(request["string"]) !=str:
        raise ValueError("the request doesn't contain the right type of key")
    if len(request["string"]) > 250:
        raise ValueError("the request key is too long")

def handler(event, context):
    try:
        if "body" not in event:
            raise ValueError("the request missed body")
        request = json.loads(event["body"])
        body_checks(request)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "string": main(request["string"])
            }),
            "isBase64Encoded": False
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Bad input"
            }),
            "isBase64Encoded": False
        }
    
