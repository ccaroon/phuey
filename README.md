# phuey
Wrapper around Philips Hue REST API

...a work in progress...

Only does the things I currently need it to do.

## Philips Hue API Notes
* Getting Started: https://developers.meethue.com/develop/get-started-2/
* Dev Tool/Debugger: http://<bridge_addr>/debug/clip.html
* API Docs: https://developers.meethue.com/develop/hue-api/

### Get Username for App
1. Push link button
2. POST /api `{"devicetype":"app_name#device"}`

Response:

```json
[
	{
		"success": {
			"username": "faKekjh6deadBeefDc42h688007duMmYk134hvl9"

		}
	}
]
```

### Making Requests
http://<bridge_addr>/api/<username>/...

### Misc
#### Python
* https://github.com/benknight/hue-python-rgb-converter
