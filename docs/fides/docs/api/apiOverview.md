# API Overview

The `fidesctl` API is exceedingly formulaic, so much so that it's easier to grasp the API by understanding the formula, rather than reading through a list of endpoints. The fundamental idea is that there's a set of five endpoints for each fides resource. These endpoints let you...

* Create an instance of a particular resource type (E.g `POST /policy`).
* Retrieve all instances of a resource type (`GET /policy`).
* Retrieve a specific instance (`GET /policy/{fides_key}`).
* Modify a specific instance (`POST /policy/{fides_key}`)
* Delete a specific instance (`DELETE /policy/{fides_key}`)

That's about all there is to it. There are an additional four endpoints that we'll look at later, but these quadruplet endpoints make up the core of the `fidesctl` API. The following sections go into more detail.


## Nine top-level URLs

The API comprises nine top-level URLs. Five of the URLs map to the modeling resources...

* `/organization`
* `/policy`
* `/registry`
* `/system`
* `/dataset`

...and the other four map to the taxonomic resources:

* `/data_category`
* `/data_qualifier`
* `/data_subject`
* `/data_use`


### Top-level URL methods

All of these top-level URLs define `POST` and `GET` methods:

* `POST` creates a new instance of the resource. The payload of the request is given as a JSON object, and takes the same form as the manifest file for that resource but without the top-level property that identifies the resource type. We'll look at an example later. 

* `GET` retrieves all of the instances of the resource. The response body is an array of objects that, again, take the same form as the manifest file for that resource.

## Nine sub-URLs

The nine top-level URLs define sub-URLs that locate a specific instance of a resource type, where the instance is identified by fides key:

* `/organization/{fides_key}`
* `/policy/{fides_key}`
* `/registry/{fides_key}`
* _and so on_

### Sub-URL methods

Each of these sub-URLs define `POST`, `GET`, and `DELETE` methods:

* `POST` completely rewrites the instance. The payload is the same as the payload in the `POST /resource_type` endpoint. 

* `GET` retrieves the instance.

* `DELETE` deletes the instance.

## Request Headers

For the `POST` methods, you must include a `Content-Type` header set to `/application/json`

```
Content-Type: application/json
```

The other methods don't require request headers. 


## HTTP Statuses

### Success

* A successful `POST /resource_type` call returns `201`. 

* A successful `DELETE /resource_type/{fides_key}` returns `204` (which means there's no response body).

* All other successful calls return `200`.


### Failure

* If you pass an invalid `fides_key` path parameter to an instance endpoint (regardless of the method), the call returns `404`.

* If you pass invalid data in the request body of a `POST`, the call returns `422`.


## Other endpoints

There are four other endpoints:

* `GET /health` pings the API server to see if it's up and running. The call returns `200` if it's up and ready to receive messages, and `404` if not.

* All of the  taxonomic URLs _except_ for `/data_subject` define the `GET /resource_type/visualize/{figure_type}` endpoint. The endpoint draws the resources as a hierarchical graph and returns the drawing as  an HTML file. The `figure_type` path parameter must be one of `sunburst`, `sankey`, or `text` If successful, it returns `200`; if you specify an invalid `figure_type`, it returns `400`.

## cURL calls

<<>>

### GET /organization

<<>>

### GET /policy

<<>>